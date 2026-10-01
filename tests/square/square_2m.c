#include <math.h>
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

    // 旋回速度・角加速度
    Spur_set_angvel(1.0);
    Spur_set_angaccel(1.0);

    // 初期位置 (0, 0, 0)
    Spur_set_pos_GL(0.0, 0.0, 0.0);

    printf("2 m x 2 m square test start\n");


    // ========================================
    // 1. (0, 0) -> (2, 0)
    // ========================================

    printf("Line 1 : (0, 0) -> (2, 0)\n");

    // x = 2.005 m のラインで停止
    Spur_stop_line_GL(
        2.0 + 0.005,
        0.0,
        0.0
    );

    // x = 2.0 m のラインを越えるまで待機
    while (!Spur_over_line_GL(
        2.0,
        0.0,
        0.0))
    {
        usleep(100000);
    }

    Spur_stop();

    // 左に90°旋回
    Spur_spin_GL(M_PI / 2.0);

    while (!Spur_near_ang_GL(
        M_PI / 2.0,
        M_PI / 180.0))
    {
        usleep(100000);
    }


    // ========================================
    // 2. (2, 0) -> (2, 2)
    // ========================================

    printf("Line 2 : (2, 0) -> (2, 2)\n");

    // y = 2.005 m のラインで停止
    Spur_stop_line_GL(
        2.0,
        2.0 + 0.005,
        M_PI / 2.0
    );

    // y = 2.0 m のラインを越えるまで待機
    while (!Spur_over_line_GL(
        2.0,
        2.0,
        M_PI / 2.0))
    {
        usleep(100000);
    }

    Spur_stop();

    // 左に90°旋回
    Spur_spin_GL(M_PI);

    while (!Spur_near_ang_GL(
        M_PI,
        M_PI / 180.0))
    {
        usleep(100000);
    }


    // ========================================
    // 3. (2, 2) -> (0, 2)
    // ========================================

    printf("Line 3 : (2, 2) -> (0, 2)\n");

    // -X方向なので、目標より5 mm先は x = -0.005 m
    Spur_stop_line_GL(
        -0.005,
        2.0,
        M_PI
    );

    // x = 0.0 m のラインを越えるまで待機
    while (!Spur_over_line_GL(
        0.0,
        2.0,
        M_PI))
    {
        usleep(100000);
    }

    Spur_stop();

    // 左に90°旋回
    Spur_spin_GL(-M_PI / 2.0);

    while (!Spur_near_ang_GL(
        -M_PI / 2.0,
        M_PI / 180.0))
    {
        usleep(100000);
    }


    // ========================================
    // 4. (0, 2) -> (0, 0)
    // ========================================

    printf("Line 4 : (0, 2) -> (0, 0)\n");

    // -Y方向なので、目標より5 mm先は y = -0.005 m
    Spur_stop_line_GL(
        0.0,
        -0.005,
        -M_PI / 2.0
    );

    // y = 0.0 m のラインを越えるまで待機
    while (!Spur_over_line_GL(
        0.0,
        0.0,
        -M_PI / 2.0))
    {
        usleep(100000);
    }

    Spur_stop();


    // ========================================
    // 最終姿勢を0 radに戻す
    // ========================================

    Spur_spin_GL(0.0);

    while (!Spur_near_ang_GL(
        0.0,
        M_PI / 180.0))
    {
        usleep(100000);
    }

    Spur_stop();

    // 最終オドメトリ表示
    Spur_get_pos_GL(
        &x,
        &y,
        &theta
    );

    printf("\nSquare test finished\n");
    printf(
        "Final odometry: x = %.3f m, y = %.3f m, theta = %.3f rad\n",
        x,
        y,
        theta
    );

    Spur_free();

    return 0;
}