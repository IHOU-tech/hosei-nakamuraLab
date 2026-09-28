# i-Cart-mini 走行制御・キャリブレーション

本リポジトリでは，中村研究室で使用している移動ロボット **i-Cart-mini** の走行制御，YP-Spurパラメータ，キャリブレーション用プログラム，および走行結果の解析データを管理する。

## 使用環境

- Ubuntu 24.04
- ROS 2 Jazzy
- YP-Spur
- TF-2MD3-R6
- i-Cart-mini
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
│
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
│       ├── ps3_teleop.py
│       └── README.md
│
└── tests/
    ├── radius/
    │   └── line_10m.c
    ├── tread/
    │   └── spin_10turns.c
    └── wheel_check/
        └── wheel_individual_test.c
```

### `params/`
YP-Spurで使用するi-Cart-miniのパラメータファイルを保存する。
- icart_original.param
  - 初期パラメータ
- icart_calibration.param
  - キャリブレーション作業中に使用するパラメータ
- icart_final.param
  - キャリブレーション後に使用するパラメータ
### `tests/`

i-Cart-miniの走行パラメータを確認・キャリブレーションするためのテストプログラムを保存する。

#### `radius/`

車輪半径（RADIUS）のキャリブレーション用。

`line_10m.c` では，ロボットを10 m直進させ，指令距離と実際の走行距離を比較する。

```text
tests/radius/line_10m.c
```

主な内容：

- 初期位置を `(0, 0, 0)` に設定
- 速度 `0.2 m/s`
- 加速度 `0.5 m/s²`
- 10 m直進
- 走行中の `x, y, theta` を表示
- 10 m地点付近で停止

コンパイル例：

```bash
cd ~/デスクトップ/i-Cart/tests/radius
gcc line_10m.c -o line_10m -lypspur
```

#### `tread/`

トレッド（TREAD）のキャリブレーション用。

`spin_10turns.c` では，ロボットを原地で10回転させた後，実際の向きを確認し，Enterキー入力後に `spin 0` を実行する。

```text
tests/tread/spin_10turns.c
```

主な内容：

- 初期姿勢を `0 rad` に設定
- 10回転（`20π rad`）の原地旋回
- 旋回中の角度を表示
- 10回転後に実際の姿勢を確認
- Enterキー入力後に `spin 0` を実行

コンパイル例：

```bash
cd ~/デスクトップ/i-Cart/tests/tread
gcc spin_10turns.c -o spin_10turns -lypspur -lm
```

#### `wheel_check/`

左右車輪とYP-Spur上の `w_r`，`w_l` の対応関係を確認するためのテストプログラム。

`wheel_individual_test.c` では，一方の車輪速度を0に設定し，もう一方の車輪のみを回転させる。

```text
tests/wheel_check/wheel_individual_test.c
```

確認内容：

- `w_r = 2.0`, `w_l = 0.0`
  - 右車輪のみが回転することを確認
- `w_r = 0.0`, `w_l = 2.0`
  - 左車輪のみが回転することを確認

コンパイル例：

```bash
cd ~/デスクトップ/i-Cart/tests/wheel_check
gcc wheel_individual_test.c -o wheel_individual_test -lypspur
```

### テストプログラムの実行ファイルについて

コンパイルによって生成される以下の実行ファイルはGit管理対象外としている。

```text
tests/radius/line_10m
tests/tread/spin_10turns
tests/wheel_check/wheel_individual_test
```

これらは `.gitignore` に登録している。

### robot parameter

```text
# =========================
# Basic settings
# =========================

VERSION 4                  # パラメータファイル形式
VOLT 24                    # 電源電圧 [V]
CONTROL_CYCLE 0.015        # 制御周期 [s]
CYCLE 0.001                # 内部周期 [s]
TORQUE_FINENESS 0.000001   # トルク分解能


# =========================
# Motor / Encoder
# =========================

MOTOR_PHASE 3              # モータ相数
COUNT_REV 400              # エンコーダ分解能 [count/rev]
ENCODER_TYPE 2             # エンコーダ方式
MOTOR_R 0.800              # モータ端子間抵抗 [ohm]
MOTOR_VC 729               # モータ速度定数関連
MOTOR_TC 0.0131            # モータトルク定数 [N·m/A]
GEAR 75                    # 減速比


# =========================
# Robot geometry
# =========================

TREAD 0.395                # 左右駆動輪間距離 [m]
RADIUS[0] -0.0830          # 車輪0 有効半径 [m]
RADIUS[1] 0.0830           # 車輪1 有効半径 [m]


# =========================
# Robot dynamics
# =========================

MASS 16.5                  # 車体質量 [kg]
MOMENT_INERTIA 1.352       # 車体慣性モーメント [kg·m^2]
TIRE_M_INERTIA 0.00260     # 車輪慣性モーメント [kg·m^2]
MOTOR_M_INERTIA 0.000000148 # モータロータ慣性 [kg·m^2]

TORQUE_MAX 0.0825          # 基準最大トルク [N·m]
TORQUE_LIMIT 0.66          # トルク制限


# =========================
# Trajectory control
# =========================

L_C1 0.01                  # 軌道追従制御パラメータ
L_K1 800                   # 軌道追従ゲイン K1
L_K2 300                   # 軌道追従ゲイン K2
L_K3 200                   # 軌道追従ゲイン K3
L_DIST 0.6                 # 先読み距離関連 [m]


# =========================
# Motion limits
# =========================

MAX_VEL 0.9                # 最大並進速度 [m/s]
MAX_W 3.14                 # 最大角速度 [rad/s]
MAX_ACC_V 1.8              # 最大並進加速度 [m/s^2]
MAX_ACC_W 6.28             # 最大角加速度 [rad/s^2]
MAX_CENTRI_ACC 1.96        # 最大向心加速度 [m/s^2]


# =========================
# Motor control gains
# =========================

GAIN_KP 60                 # 比例ゲイン
GAIN_KI 50                 # 積分ゲイン
INTEGRAL_MAX 0.05          # 積分項上限

TORQUE_NEWTON 0            # 定数トルク補償
TORQUE_VISCOS 0            # 粘性抵抗補償

```

### 調整方法

```text
# =========================
# Motor torque
# =========================

TORQUE_MAX 0.0825
# モータ最大トルク [N·m]
# 調整方法：
# ・ロボットが発進できない、低速で停止する、原地旋回できない場合は不足の可能性あり
# ・少しずつ増加させ、必要な走行・旋回が安定してできる値を確認する
# ・値を上げると加速・旋回時の駆動力が大きくなる
# ・大きすぎる場合は急激な動作、タイヤのスリップ、振動、モータ・ドライバへの負担が増える

TORQUE_LIMIT 0.66
# モータトルク制限 [N·m]
# 調整方法：
# ・実際に許可するトルクの上限
# ・TORQUE_MAXを設定していても、TORQUE_LIMITが低い場合は出力が制限される
# ・旋回や加速でトルク不足になる場合に確認する
# ・必要以上に大きくしない
# ・未定義の場合はTORQUE_MAXが使用される

# =========================
# Motor PI control
# =========================

GAIN_KP 60
# PI速度制御の比例ゲイン Kp [1/s]
# 現在の速度誤差に対して、どれだけ強く補正するかを決める
#
# Kpが小さすぎる：
# ・指令速度への追従が遅い
# ・負荷をかけると速度が落ちやすい
# ・発進や旋回の反応が鈍い
#
# Kpを大きくする：
# ・速度指令への応答が速くなる
# ・外乱や負荷に対して強くなる
#
# Kpが大きすぎる：
# ・車輪が細かく振動する
# ・速度が上下に揺れる
# ・発進・停止時にガクガクする
# ・発振する可能性がある
#
# 調整方法：
# 1. KIを小さく、または0にしてKpを調整する
# 2. 低速走行・一定速度走行・停止を確認する
# 3. 振動しない範囲でKpを少しずつ上げる
# 4. 振動が出始めたら少し下げる

GAIN_KI 50
# PI速度制御の積分ゲイン Ki [1/s^2]
# 長時間残る速度誤差を積算して補正する
#
# Kiが小さすぎる：
# ・負荷がかかったときに指令速度より少し遅い状態が残る
# ・定常偏差が残る
#
# Kiを大きくする：
# ・長時間残る速度誤差を解消しやすくなる
# ・坂道や負荷変動時の速度維持が改善する
#
# Kiが大きすぎる：
# ・オーバーシュートしやすい
# ・速度が周期的に揺れる
# ・停止後も一瞬押し続けるような挙動が出る
# ・積分飽和が起こりやすい
#
# 調整方法：
# 1. まずKpを調整する
# 2. その後Kiを0または小さい値から少しずつ上げる
# 3. 一定速度走行時に残る速度誤差が減るか確認する
# 4. 振動・オーバーシュートが出たらKiを下げる

```
### `ros2/`

i-Cart-miniで使用するROS 2関連の設定ファイルおよび操作プログラムを保存する。

#### `icart_ypspur_ros2_bridge.yaml`

i-Cart-miniとROS 2間の通信には，以下の `ypspur_ros2_bridge` を使用する。

- Repository: `dlab-ut/ypspur_ros2_bridge`
- GitHub: https://github.com/dlab-ut/ypspur_ros2_bridge

本リポジトリ内では，i-Cart-mini用に使用している設定ファイルを保存している。

```text
ros2/icart_ypspur_ros2_bridge.yaml
```

主なROS 2 Topic：

```text
/cmd_vel
/odom
/joy
```

#### `teleop/`

PS3コントローラからi-Cart-miniを操作するためのROS 2 teleopプログラムを保存する。

```text
ros2/teleop/ps3_teleop.py
```

このノードは `/joy` を購読し，操作内容に応じて `/cmd_vel` をPublishする。

制御の流れ：

```text
PS3 Controller
    ↓
joy_node
    ↓
/joy
    ↓
ps3_teleop.py
    ↓
/cmd_vel
    ↓
ypspur_ros2_bridge
    ↓
YP-Spur
    ↓
TF-2MD3
    ↓
i-Cart-mini
```

主な操作：

- `R1`
  - デッドマンボタン
  - R1を押している間のみロボット操作を有効化

- `R2`
  - 前進

- `L2`
  - 後退

- 左スティック左右
  - 左右旋回

- `□`
  - 左に90°旋回

- `○`
  - 右に90°旋回

- `△`
  - 前方へ1 m移動

- `×`
  - 後方へ1 m移動

PS3コントローラの入力割り当て：

```text
axes[0]    : 左スティック左右
axes[2]    : L2
axes[5]    : R2

buttons[0] : ×
buttons[1] : ○
buttons[2] : □
buttons[3] : △
buttons[5] : R1
```

L2 / R2は以下の値として取得される。

```text
未入力     : +1
最大入力   : -1
```

プログラム内では，0～1の値に変換して使用する。

```python
trigger = (1.0 - axis) / 2.0
```

また，`/odom` を使用して以下の自動動作を行う。

- 前進 1 m
- 後退 1 m
- 左旋回 90°
- 右旋回 90°

R1を離した場合，自動動作は即座にキャンセルされ，停止指令を送信する。


