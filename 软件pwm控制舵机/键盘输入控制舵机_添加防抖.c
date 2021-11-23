/* file name=sg90.c */
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

#include <wiringPi.h>
#include <softPwm.h>

#define RANGE 200     /* 1 means 100 us , 200 means 20 ms 1等于100微妙，200等于20毫秒 */

int move( int pin, int moveAngle )
{
	int degree;
	degree = 5 +  moveAngle  / 180.0 * 20.0;

	softPwmWrite( pin, degree ); /* 再次复写pwm输出 */
	delay( 200 );
	printf("%d\n",degree);
	printf("%d\n",moveAngle);
	// softPwmStop(pin);
	// 输入 pwm 后，给 pwm 为 0，防抖
	softPwmWrite( pin, 0 );
    return 0;
}

int main( void )
{
	int	num;
	int	pinN_1	= 7;
	int	pinN_2	= 0;

	int	moveAngle_1	= 90;
	int	moveAngle_2	= 90;
	wiringPiSetup();                        /* wiringpi初始化 */
	softPwmCreate( pinN_1, 15, RANGE );     /* 创建一个使舵机转到90的pwm输出信号 */
	delay(500);
		softPwmWrite( pinN_1, 0 );
	softPwmCreate( pinN_2, 15, RANGE );     /* 创建一个使舵机转到90的pwm输出信号 */
	delay(500);
	softPwmWrite( pinN_2, 0 );

	for (;; )
	{
		printf( "请输入移动方向，0表示左，1表示右,2表示上，3表示下\n" );
		scanf( "%d", &num );

		if ( !(( num ) >= 0 && ( num ) <= 180) ){
			printf( "degree is between 0 and 180\n" );
			exit( 0 );
		}

		if ( num == 0 || num == 1 ){
			if ( num == 0 ){
				moveAngle_1 = moveAngle_1 - 5;
			}
			if ( num == 1 ){
				moveAngle_1 = moveAngle_1 + 5;
			}
			move( pinN_1, moveAngle_1 );
		}

		if ( num == 2 || num == 3 ){
			if ( num == 2 ){
				moveAngle_2 = moveAngle_2 - 5;
			}
			if ( num == 3 ){
				moveAngle_2 = moveAngle_2 + 5;
			}
			move( pinN_2, moveAngle_2 );
		}
	}
    return 0;
}


