#!/usr/bin/env python3

import argparse
import csv
import os

import matplotlib.pyplot as plt


def load_csv(filename):

    x = []
    y = []

    with open(filename, 'r') as f:

        reader = csv.DictReader(f)

        for row in reader:
            x.append(float(row['x']))
            y.append(float(row['y']))

    return x, y


def get_reference(mode):

    if mode == 'square':

        # 2 m × 2 m
        ref_x = [
            0.0,
            2.0,
            2.0,
            0.0,
            0.0
        ]

        ref_y = [
            0.0,
            0.0,
            2.0,
            2.0,
            0.0
        ]

        title = '2 m x 2 m Square Trajectory'

    elif mode == 'figure8':

        # 上1m → 右 → 上 → 左
        # → 下 → 左 → 下 → 右
        ref_x = [
            0.0,
            0.0,
            1.0,
            1.0,
            0.0,
            0.0,
            -1.0,
            -1.0,
            0.0
        ]

        ref_y = [
            0.0,
            1.0,
            1.0,
            2.0,
            2.0,
            1.0,
            1.0,
            0.0,
            0.0
        ]

        title = 'Figure-8 Trajectory'

    else:
        raise ValueError(
            'mode must be square or figure8'
        )

    return ref_x, ref_y, title


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'csv_file'
    )

    parser.add_argument(
        '--mode',
        required=True,
        choices=[
            'square',
            'figure8'
        ]
    )

    parser.add_argument(
        '--output',
        default=None
    )

    args = parser.parse_args()

    x, y = load_csv(
        args.csv_file
    )

    ref_x, ref_y, title = get_reference(
        args.mode
    )

    if len(x) == 0:
        print('No odometry data.')
        return

    plt.figure(
        figsize=(7, 7)
    )

    # 実測軌跡
    plt.plot(
        x,
        y,
        label='Odometry'
    )

    # 理想軌跡
    plt.plot(
        ref_x,
        ref_y,
        '--',
        label='Reference'
    )

    # 開始位置
    plt.scatter(
        x[0],
        y[0],
        marker='o',
        label='Start'
    )

    # 終了位置
    plt.scatter(
        x[-1],
        y[-1],
        marker='x',
        label='End'
    )

    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')

    plt.title(title)

    plt.axis('equal')
    plt.grid(True)
    plt.legend()

    if args.output:

        os.makedirs(
            os.path.dirname(args.output),
            exist_ok=True
        )

        plt.savefig(
            args.output,
            dpi=300,
            bbox_inches='tight'
        )

        print(
            f'Saved: {args.output}'
        )

    plt.show()


if __name__ == '__main__':
    main()