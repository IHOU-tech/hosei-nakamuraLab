#!/usr/bin/env python3

import rclpy

from rclpy.node import Node

from nav_msgs.msg import (
    Odometry,
    Path
)

from geometry_msgs.msg import (
    PoseStamped
)


class OdomToPath(Node):

    def __init__(self):

        super().__init__('odom_to_path')

        self.path = Path()

        self.publisher = self.create_publisher(
            Path,
            '/odom_path',
            10
        )

        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.get_logger().info(
            '/odom -> /odom_path'
        )

    def odom_callback(self, msg):

        pose = PoseStamped()

        pose.header = msg.header

        pose.pose = msg.pose.pose

        self.path.header = msg.header

        self.path.poses.append(
            pose
        )

        self.publisher.publish(
            self.path
        )


def main():

    rclpy.init()

    node = OdomToPath()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()