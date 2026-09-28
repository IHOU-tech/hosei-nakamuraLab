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

    // 走行パラメータ
    Spur_set_vel(0.2);
    Spur_set_accel(0.5);

    // 初期位置 (0, 0, 0)
    Spur_set_pos_GL(0, 0, 0);

    printf("Radius calibration start\n");
    printf("Move straight for 10 m\n");

    // x = 10 m で停止
    Spur_stop_line_GL(10.0, 0.0, 0.0);

    while (!Spur_over_line_GL(10.0 - 0.005, 0.0, 0.0))
    {
        Spur_get_pos_GL(&x, &y, &theta);

        printf("x = %.3f, y = %.3f, theta = %.3f\n",
               x, y, theta);

        usleep(100000);
    }

    Spur_stop();

    printf("Finished\n");

    Spur_free();

    return 0;
}