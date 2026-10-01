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
│   ├── figures/
│   ├── odom_xy.csv
│   └── plot_odom.py
│
├── calibration/
├── docs/
│
├── params/
│   ├── icart_original.param
│   ├── icart_calibration.param
│   └── icart_final.param
│
├── ros2/
│   ├── icart_ypspur_ros2_bridge.yaml
│   └── teleop/
│       └── ps3_teleop.py
│
└── tests/
    ├── radius/
    │   └── line_10m.c
    ├── tread/
    │   └── spin_10turns.c
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

## `params/`

YP-Spurで使用するi-Cart-miniのパラメータを保存する。

- `icart_original.param`：初期パラメータ
- `icart_calibration.param`：キャリブレーション作業用
- `icart_final.param`：キャリブレーション後の最終パラメータ

各パラメータの意味および調整方法は，パラメータファイル内のコメントに記載する。

## `tests/`

### `radius/`

`line_10m.c`

RADIUSのキャリブレーション用。  
10 m直進を複数回行い，実測距離の平均が指令距離に一致するようにRADIUSを調整する。

目安：

```text
10 m × 約5回
```

### `square/`

`square_2m.c`

2 m × 2 mの正方形軌跡を走行するテスト。

RADIUSおよびTREAD調整後の直進・90°旋回精度を確認する。

### `figure8/`

`figure8_1m.c`

1辺1 mの直線移動を組み合わせた8字型軌跡を走行する。

左右旋回を含む複合走行により，走行誤差や旋回誤差を確認する。

## `ros2/`

i-Cart-miniで使用するROS 2関連の設定ファイルを保存する。

### ypspur_ros2_bridge

ROS 2とYP-Spur間の通信には以下を使用する。

- Repository: `dlab-ut/ypspur_ros2_bridge`
- GitHub: https://github.com/dlab-ut/ypspur_ros2_bridge

設定ファイル：

```text
ros2/icart_ypspur_ros2_bridge.yaml
```

主なTopic：

```text
/cmd_vel
/odom
/joy
```

### PS3 Teleop

```text
ros2/teleop/ps3_teleop.py
```

PS3コントローラからi-Cart-miniを操作する。

主な操作：

- `R1`：デッドマン
- `R2`：前進
- `L2`：後退
- 左スティック左右：旋回
- `□ / ○`：左 / 右 90°旋回
- `△ / ×`：前 / 後 1 m移動

## `analysis/`

オドメトリデータの解析および走行軌跡の描画に使用する。

## `calibration/`

RADIUS，TREADなどのキャリブレーション結果を記録する。

## `docs/`

ハードウェア構成，セットアップ方法，実験手順などのドキュメントを保存する。

## Git管理対象外

ROS bagおよびコンパイル後の実行ファイルは `.gitignore` に登録し，GitHubには保存しない。
