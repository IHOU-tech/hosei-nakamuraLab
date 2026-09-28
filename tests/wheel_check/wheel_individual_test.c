#include <stdio.h>
#include <unistd.h>
#include <ypspur.h>

int main(int argc, char *argv[])
{
    setvbuf(stdout, 0, _IONBF, 0);

    if (Spur_init() < 0)
    {
        fprintf(stderr, "ERROR : cannot open spur.\n");
        return -1;
    }

    printf("Wheel individual test start\n");

    // ========================================
    // Right wheel only
    // ========================================

    printf("\nRight wheel only\n");
    printf("w_r = 2.0, w_l = 0.0\n");

    YP_wheel_vel(2.0, 0.0);

    sleep(3);

    YP_wheel_vel(0.0, 0.0);

    printf("Stop\n");

    sleep(2);

    // ========================================
    // Left wheel only
    // ========================================

    printf("\nLeft wheel only\n");
    printf("w_r = 0.0, w_l = 2.0\n");

    YP_wheel_vel(0.0, 2.0);

    sleep(3);

    YP_wheel_vel(0.0, 0.0);

    printf("Stop\n");
    printf("\nFinished\n");

    Spur_free();

    return 0;
}