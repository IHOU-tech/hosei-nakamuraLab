import csv
import matplotlib.pyplot as plt

x = []
y = []

with open("odom_xy.csv", "r") as f:
    reader = csv.reader(f)

    # 跳过标题行
    next(reader)

    for row in reader:
        if len(row) >= 2:
            try:
                x.append(float(row[0]))
                y.append(float(row[1]))
            except ValueError:
                pass

plt.figure(figsize=(8, 8))

# 实际 odom
plt.plot(x, y, label="Odom trajectory")

# 起点 / 终点
plt.scatter(x[0], y[0], s=80, label="Start")
plt.scatter(x[-1], y[-1], marker="x", s=100, label="End")

# 理论 1m × 1m
ideal_x = [0, 1, 1, 0, 0]
ideal_y = [0, 0, 1, 1, 0]

plt.plot(ideal_x, ideal_y, "--", label="Ideal 1m x 1m")

plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("YP-Spur 1m x 1m Odometry")

plt.axis("equal")
plt.grid(True)
plt.legend()

plt.savefig("odom_trajectory_1x1.png", dpi=200, bbox_inches="tight")
plt.show()
