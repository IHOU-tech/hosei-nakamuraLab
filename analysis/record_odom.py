#!/usr/bin/env python3

import argparse
import csv
import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class OdomRecorder(Node):

    def __init__(self, output_file):
        super().__init__('odom_recorder')

        self.output_file = output_file

        self.file = open(
            self.output_file,
            'w',
            newline=''
        )

        self.writer = csv.writer(self.file)

        self.writer.writerow([
            'time',
            'x',
            'y',
            'yaw'
        ])

        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.get_logger().info(
            f'Recording /odom -> {self.output_file}'
        )

    def odom_callback(self, msg):

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation

        siny_cosp = 2.0 * (
            q.w * q.z +
            q.x * q.y
        )

        cosy_cosp = 1.0 - 2.0 * (
            q.y * q.y +
            q.z * q.z
        )

        yaw = math.atan2(
            siny_cosp,
            cosy_cosp
        )

        t = (
            msg.header.stamp.sec +
            msg.header.stamp.nanosec * 1e-9
        )

        self.writer.writerow([
            t,
            x,
            y,
            yaw
        ])

        self.file.flush()

    def close_file(self):
        self.file.close()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'output',
        help='Output CSV file'
    )

    args = parser.parse_args()

    rclpy.init()

    node = OdomRecorder(
        args.output
    )

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.close_file()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()