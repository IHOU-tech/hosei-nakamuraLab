#include <math.h>
#include <stdio.h>
#include <unistd.h>
#include <ypspur.h>

int main(int argc, char *argv[])
{
    double x, y, theta;

    setvbuf(stdout, 0, _IONBF, 0);

    if (Spur_init() < 0)
    {
        fprintf(stderr, "ERROR : cannot open spur.\n");
        return -1;
    }

    // 角速度・角加速度
    Spur_set_angvel(M_PI / 2.0);
    Spur_set_angaccel(M_PI / 2.0);

    // 初期位置・姿勢
    Spur_set_pos_GL(0.0, 0.0, 0.0);

    printf("Tread calibration start\n");
    printf("Rotate 10 turns\n");

    // 10回転 = 20π rad
    Spur_spin_GL(20.0 * M_PI);

    while (!Spur_near_ang_GL(20.0 * M_PI, M_PI / 180.0))
    {
        Spur_get_pos_GL(&x, &y, &theta);

        printf("theta = %.3f rad (%.2f deg)\n",
               theta,
               theta * 180.0 / M_PI);

        usleep(100000);
    }

    printf("\n10 turns finished.\n");
    printf("Check the actual heading.\n");
    printf("Press ENTER to execute spin 0.\n");

    getchar();

    // spin 0
    Spur_spin_GL(0.0);

    while (!Spur_near_ang_GL(0.0, M_PI / 180.0))
    {
        Spur_get_pos_GL(&x, &y, &theta);

        printf("theta = %.3f rad (%.2f deg)\n",
               theta,
               theta * 180.0 / M_PI);

        usleep(100000);
    }

    Spur_stop();

    printf("spin 0 finished\n");

    Spur_free();

    return 0;
}