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
│
└── tests/
    ├── radius/
    │   └── line_10m.c
    ├── tread/
    └── wheel_check/

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
