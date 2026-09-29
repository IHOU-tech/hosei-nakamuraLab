#include <math.h>
#include <stdio.h>
#include <unistd.h>
#include <ypspur.h>

void spin_and_wait(double target)
{
    Spur_spin_GL(target);

    while (!Spur_near_ang_GL(
        target,
        M_PI / 180.0))
    {
        usleep(10000);
    }
}

int main(int argc, char *argv[])
{
    setvbuf(stdout, 0, _IONBF, 0);

    if (Spur_init() < 0)
    {
        fprintf(stderr, "ERROR : cannot open spur.\n");
        return -1;
    }

    // 角速度・角加速度
    Spur_set_angvel(M_PI / 2.0);
    Spur_set_angaccel(M_PI / 2.0);

    // 初期姿勢 = 0 rad
    Spur_set_pos_GL(
        0.0,
        0.0,
        0.0
    );

    printf("TREAD calibration start\n");
    printf("Rotate 10 turns\n\n");

    for (int i = 0; i < 10; i++)
    {
        // 0 -> 90 deg
        spin_and_wait(M_PI / 2.0);

        // 90 -> 180 deg
        spin_and_wait(M_PI);

        // 180 -> 270 deg (-90 deg)
        spin_and_wait(-M_PI / 2.0);

        // 270 -> 360 deg (0 deg)
        spin_and_wait(0.0);

        printf("Rotation %d / 10 completed\n", i + 1);
    }

    printf("\n10 turns completed.\n");
    printf("Check the actual robot heading.\n");
    printf("Press ENTER to execute spin 0.\n");

    getchar();

    // 最終姿勢を0 radに設定
    Spur_spin_GL(0.0);

    while (!Spur_near_ang_GL(
        0.0,
        M_PI / 180.0))
    {
        usleep(10000);
    }

    Spur_stop();

    printf("spin 0 finished\n");

    Spur_free();

    return 0;
}