# 左右車輪の対応確認

YP-Spur上の `w_r`，`w_l` と実機の左右車輪の対応関係を確認する。

## YP-Spur公式実装による確認

YP-Spur公式リポジトリ：

https://docs.ros.org/en/melodic/api/ypspur/html/libypspur_8c.html

公式APIでは，車輪速度指令が以下のように定義されている。

```c
YP_wheel_vel(double r, double l)
```

また，車輪加速度についても以下の順序で定義されている。

```c
YP_set_wheel_accel(double r, double l)
```

したがって，引数の順序は，

```text
r : Right wheel
l : Left wheel
```

である。

YP-Spur公式リポジトリおよびAPI定義から，第1引数が右車輪，第2引数が左車輪であることを確認した。

`ypspur-interpreter` の

```text
wheel_vel 2 0
```

は内部で

```c
YP_wheel_vel(2, 0)
```

として渡されるため，第1引数が右車輪，第2引数が左車輪の速度指令となる。

## 実機による確認

最初に車輪速度を0にする。

```text
wheel_vel 0 0
```

次に左右車輪の加速度を設定する。

```text
set_wheel_accel 5 5
```

### 右車輪

```text
wheel_vel 2 0
```

確認結果：

- 右車輪のみが回転


### 左車輪

```text
wheel_vel 0 2
```

確認結果：

- 左車輪のみが回転
