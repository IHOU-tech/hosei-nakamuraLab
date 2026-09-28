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
車輪半径，トレッド，左右車輪の対応関係などを確認するためのテストプログラムを保存する。
radius/
車輪半径（RADIUS）のキャリブレーション用。
現在は，ロボットを10 m直進させるテストプログラムを保存している。
line 10 0 0

### `tread/`
トレッド（TREAD）のキャリブレーション用。
原地旋回を10回以上行い，最終的な姿勢誤差を確認する予定。
wheel_check/
左右の車輪とYP-Spur上の w_l，w_r の対応関係を確認するためのプログラムを保存する。
片方の車輪速度を0に設定し，もう片方のみを回転させることで確認する。
analysis/
オドメトリデータの解析用ファイルを保存する。
- odom_xy.csv
  - オドメトリから取得したXY座標
- plot_odom.py
  - 軌跡描画用Pythonスクリプト
- figures/
  - 走行軌跡などの解析結果画像
calibration/
RADIUS，TREADなどのキャリブレーション結果を記録する。
ros2/
ROS 2関連の設定ファイル，launch方法，topic情報などを保存する。
docs/
ハードウェア構成，セットアップ方法，実験手順などのドキュメントを保存する。
キャリブレーション
タイヤ空気圧
左右タイヤの空気圧を同一にした状態でキャリブレーションを行う。
現在の設定：
200 kPa

### `RADIUS`
車輪半径のキャリブレーションでは，少なくとも10 m直進させ，指令距離と実際の走行距離を比較する。
使用するテスト：
tests/radius/line_10m.c

### `TREAD`
トレッドのキャリブレーションでは，ロボットを原地で10回以上旋回させ，旋回後の姿勢誤差を確認する。
左右車輪の確認
w_l と w_r の片方を0に設定し，それぞれ個別に指令を与える。
これにより，指定した側の車輪のみが回転することを確認する。
注意事項
ROS bagのデータはファイルサイズが大きくなるため，本リポジトリでは管理しない。
以下のディレクトリは .gitignore によりGitの管理対象外としている。
rosbag/
rosbag2_*/
build/
install/
log/   
