import math

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def normalize_angle(a):
    while a > math.pi:
        a -= 2.0 * math.pi
    while a < -math.pi:
        a += 2.0 * math.pi
    return a


class PS3Teleop(Node):

    def __init__(self):
        super().__init__('ps3_teleop')

        # ---------- コントローラ入力番号 ----------
        self.AXIS_STEER = 0
        self.AXIS_L2 = 2
        self.AXIS_R2 = 5

        self.BTN_CROSS = 0
        self.BTN_CIRCLE = 1
        self.BTN_SQUARE = 2
        self.BTN_TRIANGLE = 3
        self.BTN_R1 = 5

        # ---------- 手動操作時の速度 ----------
        self.max_linear = 0.5       # m/s
        self.max_angular = 1.50      # rad/s

        # ---------- 自動動作時の速度 ----------
        self.auto_linear = 0.25      # m/s
        self.auto_angular = 0.7     # rad/s

        self.target_distance = 1.0
        self.target_angle = math.pi / 2.0

        self.deadzone = 0.10
        self.joy_timeout = 0.5

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.joy_sub = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.latest_joy = None
        self.last_joy_time = None

        self.have_odom = False
        self.odom_x = 0.0
        self.odom_y = 0.0
        self.odom_yaw = 0.0

        self.prev_buttons = []

        # action:
        # None
        # forward
        # backward
        # turn_left
        # turn_right
        self.action = None

        self.start_x = 0.0
        self.start_y = 0.0
        self.start_yaw = 0.0

        self.timer = self.create_timer(0.02, self.control_loop)

        self.get_logger().info('PS3 i-Cart teleop started')
        self.get_logger().info('Hold R1 to enable robot motion')

    # --------------------------------------------------

    def odom_callback(self, msg):
        self.odom_x = msg.pose.pose.position.x
        self.odom_y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation

        # Quaternion -> planar yaw
        siny_cosp = 2.0 * (
            q.w * q.z +
            q.x * q.y
        )

        cosy_cosp = 1.0 - 2.0 * (
            q.y * q.y +
            q.z * q.z
        )

        self.odom_yaw = math.atan2(
            siny_cosp,
            cosy_cosp
        )

        self.have_odom = True

    # --------------------------------------------------

    def button_rising(self, buttons, index):
        if index >= len(buttons):
            return False

        old = 0

        if index < len(self.prev_buttons):
            old = self.prev_buttons[index]

        return buttons[index] == 1 and old == 0

    # --------------------------------------------------

    def joy_callback(self, msg):
        self.latest_joy = msg
        self.last_joy_time = self.get_clock().now()

        buttons = msg.buttons

        r1 = (
            len(buttons) > self.BTN_R1
            and buttons[self.BTN_R1] == 1
        )

        # R1を離したら自動動作を即座にキャンセル
        if not r1:
            if self.action is not None:
                self.get_logger().warn(
                    'R1 released - action cancelled'
                )

            self.action = None

        # 自動動作はR1を押している間のみ開始可能
        if r1 and self.action is None:

            if not self.have_odom:
                pass

            elif self.button_rising(
                buttons,
                self.BTN_SQUARE
            ):
                self.start_turn(+1)

            elif self.button_rising(
                buttons,
                self.BTN_CIRCLE
            ):
                self.start_turn(-1)

            elif self.button_rising(
                buttons,
                self.BTN_TRIANGLE
            ):
                self.start_move(+1)

            elif self.button_rising(
                buttons,
                self.BTN_CROSS
            ):
                self.start_move(-1)

        self.prev_buttons = list(buttons)

    # --------------------------------------------------

    def start_move(self, direction):
        self.start_x = self.odom_x
        self.start_y = self.odom_y

        if direction > 0:
            self.action = 'forward'
            self.get_logger().info(
                'AUTO: forward 1.0 m'
            )
        else:
            self.action = 'backward'
            self.get_logger().info(
                'AUTO: backward 1.0 m'
            )

    # --------------------------------------------------

    def start_turn(self, direction):
        self.start_yaw = self.odom_yaw

        if direction > 0:
            self.action = 'turn_left'
            self.get_logger().info(
                'AUTO: turn left 90 deg'
            )
        else:
            self.action = 'turn_right'
            self.get_logger().info(
                'AUTO: turn right 90 deg'
            )

    # --------------------------------------------------

    def trigger_value(self, axis):
        # PS3:
        # released = +1
        # fully pressed = -1
        return clamp(
            (1.0 - axis) / 2.0,
            0.0,
            1.0
        )

    # --------------------------------------------------

    def publish_stop(self):
        self.cmd_pub.publish(Twist())

    # --------------------------------------------------

    def control_loop(self):

        # joyメッセージをまだ受信していない場合
        if self.latest_joy is None:
            self.publish_stop()
            return

        # Joy信号がタイムアウトした場合
        if self.last_joy_time is None:
            self.publish_stop()
            return

        elapsed = (
            self.get_clock().now()
            - self.last_joy_time
        ).nanoseconds / 1e9

        if elapsed > self.joy_timeout:
            self.action = None
            self.publish_stop()
            return

        joy = self.latest_joy

        if len(joy.buttons) <= self.BTN_R1:
            self.publish_stop()
            return

        # R1 = デッドマンボタン
        if joy.buttons[self.BTN_R1] != 1:
            self.action = None
            self.publish_stop()
            return

        # 自動動作を優先
        if self.action is not None:
            self.execute_auto_action()
            return

        # ---------- 手動操作 ----------

        if len(joy.axes) <= 5:
            self.publish_stop()
            return

        r2 = self.trigger_value(
            joy.axes[self.AXIS_R2]
        )

        l2 = self.trigger_value(
            joy.axes[self.AXIS_L2]
        )

        linear = self.max_linear * (
            r2 - l2
        )

        steer = joy.axes[self.AXIS_STEER]

        if abs(steer) < self.deadzone:
            steer = 0.0

        angular = self.max_angular * steer

        cmd = Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular

        self.cmd_pub.publish(cmd)

    # --------------------------------------------------

    def execute_auto_action(self):

        cmd = Twist()

        # ===== 1 m movement =====

        if self.action in (
            'forward',
            'backward'
        ):

            dx = self.odom_x - self.start_x
            dy = self.odom_y - self.start_y

            travelled = math.sqrt(
                dx * dx +
                dy * dy
            )

            remaining = (
                self.target_distance
                - travelled
            )

            if remaining <= 0.01:
                self.publish_stop()

                self.get_logger().info(
                    f'AUTO complete: '
                    f'{travelled:.3f} m'
                )

                self.action = None
                return

            # 目標に近づいたら減速
            speed = self.auto_linear

            if remaining < 0.20:
                speed = max(
                    0.05,
                    self.auto_linear
                    * remaining / 0.20
                )

            if self.action == 'backward':
                speed *= -1.0

            cmd.linear.x = speed

            self.cmd_pub.publish(cmd)
            return

        # ===== 90 degree rotation =====

        if self.action in (
            'turn_left',
            'turn_right'
        ):

            delta = normalize_angle(
                self.odom_yaw
                - self.start_yaw
            )

            if self.action == 'turn_left':
                progress = delta
                direction = +1.0
            else:
                progress = -delta
                direction = -1.0

            progress = max(
                0.0,
                progress
            )

            remaining = (
                self.target_angle
                - progress
            )

            if remaining <= math.radians(1.0):
                self.publish_stop()

                self.get_logger().info(
                    'AUTO complete: '
                    f'{math.degrees(progress):.1f} deg'
                )

                self.action = None
                return

            speed = self.auto_angular

            if remaining < math.radians(20):
                speed = max(
                    0.15,
                    self.auto_angular
                    * remaining
                    / math.radians(20)
                )

            cmd.angular.z = (
                direction * speed
            )

            self.cmd_pub.publish(cmd)

    # --------------------------------------------------


def main(args=None):
    rclpy.init(args=args)

    node = PS3Teleop()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publish_stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
