#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <softPwm.h>
// gcc -Wall -o demo2 demo2.c -lwiringPi -lwiringPiDev -lpthread -lrt -lm -lcrypt -shared

#define RANGE 200     /* 1 means 100 us , 200 means 20 ms 1等于100微妙，200等于20毫秒 */

void foo(int pinN,int moveAngle);
// 接收一个输入度数
int main(void)
{
    // pinN 为nanopc-T4 开发板上的引脚（以 Wpi脚 计数，通过 gpio readall 命令查看 wpi 引脚标号）
    int pinN_1=7;
    int pinN_2=0;
    int num=-1;
    wiringPiSetup() ;
    //设置舵机控制引脚
 	int	moveAngle_1	= 90;
	int	moveAngle_2	= 90;
	wiringPiSetup();                        /* wiringpi初始化 */
	softPwmCreate( pinN_1, 0, RANGE );     /* 创建一个使舵机转到90的pwm输出信号 */
	softPwmCreate( pinN_2, 0, RANGE );     /* 创建一个使舵机转到90的pwm输出信号 */

    for(;;){
        num=-1;
        printf("请输入移动方向，0表示左，1表示右,2表示上，3表示下\n");
        scanf("%d",&num);
        if(num==0||num==1){
            if(num==0){
            // 每次调节+-5度
            moveAngle_1=moveAngle_1-5;
            }
            if(num==1){
                moveAngle_1=moveAngle_1+5;
            }
            foo(pinN_1,moveAngle_1);
        }

        if(num==2||num==3){
            if(num==2){
            moveAngle_2=moveAngle_2-5;
            }
            if(num==3){
                moveAngle_2=moveAngle_2+5;
            }
            foo(pinN_2,moveAngle_2);
        }
        
        if(moveAngle_1>180||moveAngle_1<0||moveAngle_2>180||moveAngle_2<0){
            printf("已到头！");
            break;
        }
        printf("%d\n", num);
	printf("%d\n", moveAngle_1);
	printf("%d\n", moveAngle_2);

    }
	return 0;
}

void foo(int pinN,int moveAngle){
     
    int degree;
    // 将角度转化为pwm值（0-180：5ms-25ms）
	degree = 5 +  moveAngle  / 180.0 * 20.0;    
    softPwmWrite( pinN, degree ); /* pwm输出脉冲控制舵机旋转 */
    delay(500);

    printf("函数执行完了");
}