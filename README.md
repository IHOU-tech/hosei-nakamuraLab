# 実機ロボット走行制御・キャリブレーション

本リポジトリでは，中村研究室で使用している移動ロボットの走行制御，YP-Spurパラメータ，キャリブレーション用プログラム，ROS 2設定，および走行結果の解析データを管理する。

## 使用環境

- Ubuntu 24.04
- ROS 2 Jazzy
- YP-Spur
- 2輪差動駆動方式

## ディレクトリ構成

```text
.
├── analysis/
│   ├── data/
│   │   └── square_2m_01.csv
│   ├── figures/
│   ├── plot_trajectory.py
│   └── record_odom.py
│
├── calibration/
│   ├── tread_calibration.md
│   └── wheel_mapping.md
│
├── params/
│   ├── icart_original.param
│   ├── icart_calibration.param
│   └── icart_final.param
│
├── ros2/
│   ├── icart_ypspur_ros2_bridge.yaml
│   ├── path/
│   │   └── odom_to_path.py
│   └── teleop/
│       └── ps3_teleop.py
│
└── tests/
    ├── radius/
    │   └── line_10m.c
    ├── square/
    │   └── square_2m.c
    └── figure8/
        └── figure8_1m.c
```
### TREAD（トレッド）の校正

TREAD の校正は専用のテストプログラムを使用せず，
YP-Spur のコマンドを用いて実機で行う。

1. `GL` でグローバル座標系に切り替える
2. `set_pos 0 0 0` で座標系をリセットする
3. `vel 0 1` 等でその場旋回させ，実機を n 周させる
   - 本実験では n = 10 を基準とする
4. n 周後に `spin 0` を実行し，0 deg 方向を向かせる
5. 初期の基準方向に対する実機の角度誤差 Δθ [rad] を測定する
6. 次式で TREAD を更新する

```math
\mathrm{TREAD}_{\mathrm{new}}
=
\frac{2\pi n}{2\pi n + \Delta\theta}
\mathrm{TREAD}_{\mathrm{old}}
```

7. Δθが十分小さくなるまで繰り返す

## `analysis/`

オドメトリデータの記録，解析および走行軌跡の描画に使用する。

## `calibration/`

RADIUS，TREAD，左右車輪の対応など，実機キャリブレーションに関する手順と結果を保存する。

## `docs/`

ハードウェア構成，セットアップ方法，実験手順などのドキュメントを保存する。

## `params/`

YP-Spurで使用するi-Cart-miniのパラメータファイルを保存する。

## `ros2/`

ROS 2 Bridge，PS3コントローラ操作，Odometry Path表示などのROS 2関連ファイルを保存する。

## `rosbag/`

走行実験時に記録したROS 2 bagデータを保存する。

## `tests/`

RADIUS校正，正方形走行，8字走行などの実機走行試験用プログラムを保存する。
