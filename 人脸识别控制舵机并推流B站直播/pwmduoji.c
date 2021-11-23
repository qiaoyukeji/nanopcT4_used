#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

#include <wiringPi.h>
#include <softPwm.h>

#define RANGE 200     /* 1 means 100 us , 200 means 20 ms 1等于100微妙，200等于20毫秒 */



void foo(int pinN,int moveAngle);
// 接收一个输入度数
int fmain(int num,int moveAngle)
{
    // pinN 为nanopc-T4 开发板上的引脚（以 Wpi脚 计数，通过 gpio readall 命令查看 wpi 引脚标号）
    int pinN_1=7;
    int pinN_2=0;

    wiringPiSetup() ;
    //设置舵机控制引脚
 	// int	moveAngle_1	= 90;
	// int	moveAngle_2	= 90;
	wiringPiSetup();                        /* wiringpi初始化 */
	softPwmCreate( pinN_1, 0, RANGE );     /* 创建一个使舵机转到90的pwm输出信号 */
    delay(500);
	softPwmWrite( pinN_1, 0 );
	softPwmCreate( pinN_2, 0, RANGE );     /* 创建一个使舵机转到90的pwm输出信号 */
    delay(500);
	softPwmWrite( pinN_2, 0 );


        if(num==0||num==1){
            if(num==0){
            moveAngle=moveAngle-5;
            }
            if(num==1){
                moveAngle=moveAngle+5;
            }
            foo(pinN_1,moveAngle);
        }

        if(num==2||num==3){
            if(num==2){
            moveAngle=moveAngle-5;
            }
            if(num==3){
                moveAngle=moveAngle+5;
            }
            foo(pinN_2,moveAngle);
        }
        
        if(moveAngle>180||moveAngle<0){
            printf("已到头！");

        }
        printf("%d\n", num);
	printf("%d\n", moveAngle);
	// printf("%d\n", moveAngle);

	

	return moveAngle;
}

void foo(int pinN,int moveAngle){
     
     int degree;
	degree = 5 +  moveAngle  / 180.0 * 20.0;
      softPwmWrite( pinN, degree ); /* 再次复写pwm输出 */
    delay(200);
    softPwmWrite( pinN, 0 );
    delay(100);
    printf("%d\n",degree);

    printf("函数执行完了");
}

// gcc -Wall -o pwmduoji pwmduoji.c -lwiringPi -lwiringPiDev -lpthread -lrt -lm -lcrypt -shared