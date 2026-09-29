#include <stdio.h>
#include <unistd.h>
#include <ypspur.h>

int main(int argc, char *argv[])
{
    double x, y, theta;

    setvbuf(stdout, 0, _IONBF, 0);

    // YP-Spur初期化
    if (Spur_init() < 0)
    {
        fprintf(stderr, "ERROR : cannot open spur.\n");
        return -1;
    }

    // 走行速度・加速度
    Spur_set_vel(0.2);
    Spur_set_accel(0.5);

    // 初期位置を (0, 0, 0) に設定
    Spur_set_pos_GL(0.0, 0.0, 0.0);

    printf("Radius calibration start\n");
    printf("Target distance: 10.0 m\n");

    // x = 10.005 m のラインで停止
    Spur_stop_line_GL(
        10.0 + 0.005,
        0.0,
        0.0
    );

    // x = 10.0 m のラインを越えるまで待機
    while (!Spur_over_line_GL(
        10.0,
        0.0,
        0.0))
    {
        Spur_get_pos_GL(
            &x,
            &y,
            &theta
        );

        printf(
            "x = %.3f m, y = %.3f m, theta = %.3f rad\n",
            x,
            y,
            theta
        );

        usleep(100000);
    }

    Spur_stop();

    Spur_get_pos_GL(
        &x,
        &y,
        &theta
    );

    printf("\nFinished\n");
    printf(
        "Final odometry: x = %.3f m, y = %.3f m, theta = %.3f rad\n",
        x,
        y,
        theta
    );

    Spur_free();

    return 0;
}