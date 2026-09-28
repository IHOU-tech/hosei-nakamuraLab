#include <math.h>
#include <stdio.h>
#include <unistd.h>
#include <ypspur.h>

int main(int argc, char* argv[])
{
    double x, y, theta;

    setvbuf(stdout, 0, _IONBF, 0);

    // YP-Spur 初始化
    if (Spur_init() < 0)
    {
        fprintf(stderr, "ERROR : cannot open spur.\n");
        return -1;
    }

    // 初始速度
    Spur_set_vel(0.2);
    Spur_set_accel(1.0);
    Spur_set_angvel(M_PI / 2.0);
    Spur_set_angaccel(M_PI / 2.0);

    // 当前位置设为原点
    Spur_set_pos_GL(0, 0, 0);

    // ========================================
    // 1. (0,0) -> (1,0)
    // ========================================
    printf("line 1 : (0,0) -> (1,0)\n");

    Spur_stop_line_GL(1.0, 0.0, 0.0);

    while (!Spur_over_line_GL(
        1.0 - 0.005,
        0.0,
        0.0))
    {
        usleep(100000);
    }

    // ========================================
    // 转 90°
    // ========================================
    printf("spin 90 deg\n");

    Spur_spin_GL(M_PI / 2.0);

    while (!Spur_near_ang_GL(
        M_PI / 2.0,
        M_PI / 18.0))
    {
        usleep(100000);
    }

    // 后续稍微提高速度（保持官方 run-test 逻辑）
    Spur_set_vel(0.3);
    Spur_set_accel(1.0);
    Spur_set_angvel(M_PI);
    Spur_set_angaccel(M_PI);

    // ========================================
    // 2. (1,0) -> (1,1)
    // ========================================
    printf("line 2 : (1,0) -> (1,1)\n");

    Spur_stop_line_GL(
        1.0,
        1.0,
        M_PI / 2.0);

    while (!Spur_over_line_GL(
        1.0,
        1.0 - 0.005,
        M_PI / 2.0))
    {
        usleep(100000);
    }

    // ========================================
    // 转 180°
    // ========================================
    printf("spin 180 deg\n");

    Spur_spin_GL(M_PI);

    while (!Spur_near_ang_GL(
        M_PI,
        M_PI / 18.0))
    {
        usleep(100000);
    }

    // ========================================
    // 3. (1,1) -> (0,1)
    // ========================================
    printf("line 3 : (1,1) -> (0,1)\n");

    Spur_stop_line_GL(
        0.0,
        1.0,
        M_PI);

    while (!Spur_over_line_GL(
        0.0 + 0.005,
        1.0,
        M_PI))
    {
        usleep(100000);
    }

    // ========================================
    // 转 -90°
    // ========================================
    printf("spin -90 deg\n");

    Spur_spin_GL(-M_PI / 2.0);

    while (!Spur_near_ang_GL(
        -M_PI / 2.0,
        M_PI / 18.0))
    {
        usleep(100000);
    }

    // ========================================
    // 4. (0,1) -> (0,0)
    // ========================================
    printf("line 4 : (0,1) -> (0,0)\n");

    Spur_stop_line_GL(
        0.0,
        0.0,
        -M_PI / 2.0);

    while (!Spur_over_line_GL(
        0.0,
        0.0 + 0.005,
        -M_PI / 2.0))
    {
        usleep(100000);
    }

    // ========================================
    // 最后转回 0°
    // ========================================
    printf("spin 0 deg\n");

    Spur_spin_GL(0.0);

    while (!Spur_near_ang_GL(
        0.0,
        M_PI / 18.0))
    {
        usleep(100000);
    }

    Spur_stop();

    // 等机器人完全停止
    usleep(4000000);

    Spur_free();

    printf("Finished.\n");
    printf("Hit Ctrl-C to exit.\n");

    // 持续显示最终位置
    while (1)
    {
        Spur_get_pos_GL(&x, &y, &theta);

        printf(
            "x = %f m, y = %f m, theta = %f deg\n",
            x,
            y,
            theta * 180.0 / M_PI
        );

        usleep(1000000);
    }

    return 0;
}