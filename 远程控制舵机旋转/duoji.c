#include <wiringPi.h>
# include <stdio.h>
# include <stdlib.h>

// gcc -Wall -o duoji duoji.c -lwiringPi -lwiringPiDev -lpthread -lrt -lm -lcrypt -shared

void foo(int pinN,int moveAngle);


// 接收一个输入度数
int fmain(int num,int moveAngle_1)
{
    // pinN 为nanopc-T4 开发板上的引脚（以 Wpi脚 计数，通过 gpio readall 命令查看 wpi 引脚标号）
    int pinN_1=7;
    int pinN_2=0;

    wiringPiSetup() ;

    // for(;;){
    //     moveAngle_1=1365;
    //     moveAngle_2=1365;
    //     break;
    // }
    //设置舵机控制引脚
    pinMode (pinN_1, OUTPUT) ;
    pinMode (pinN_2, OUTPUT) ;
    //旋转到90度

    // foo(pinN_1,moveAngle_1);
    // foo(pinN_2,moveAngle_2);
    
        // printf("请输入移动方向，0表示左，1表示右,2表示上，3表示下\n");
        // scanf("%d",&num);
        if(num==0||num==1){
            if(num==0){
            moveAngle_1=moveAngle_1-50;
            }
            if(num==1){
                moveAngle_1=moveAngle_1+50;
            }
            foo(pinN_1,moveAngle_1);
        }

        
        
        if(moveAngle_1>2400||moveAngle_1<320){
            printf("已到头！");

        }
    
	printf("%d\n", num);
	printf("%d\n", moveAngle_1);

	return moveAngle_1;
}

void foo(int pinN,int moveAngle){
     // 给舵机一段时间的反应，持续输出控制值
    for (int i = 0; i < 200; i++)
    {
    digitalWrite(pinN,HIGH);
    delayMicroseconds(moveAngle);
    digitalWrite(pinN,LOW);
    delayMicroseconds(2500-moveAngle);
    }
    printf("1");
}