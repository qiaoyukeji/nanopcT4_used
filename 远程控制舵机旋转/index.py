import web
import ctypes  
moveAngle_1=1435
ll = ctypes.cdll.LoadLibrary   
lib = ll("./duoji")

urls = (
  '/', 'index'
)


class index():

    def GET(self):
        print(web.input().num)
        # moveAngle_1=lib.fmain(web.input().num,moveAngle_1)

        return moveDUoji(int(web.input().num))

 
def moveDUoji(num):
    # 必须使用 global  声明 moveAngle_1 为全局变量，否则函数内尝试改变全局就会报错
    # https://blog.csdn.net/sinat_40304087/article/details/115701595
    global moveAngle_1
    moveAngle_1=lib.fmain(num,moveAngle_1)
    print(num)
    print(moveAngle_1)


    



if __name__== "__main__":
    app= web.application(urls,globals())
    app.run()

# 命令行带端口号