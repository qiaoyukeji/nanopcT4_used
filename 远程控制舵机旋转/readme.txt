1. 运行起 frpc 内网穿透服务，让外网可以直接访问到本地设备，使用的是 natfrp 提供的服务，使用 http 协议
    /usr/local/bin/frpc
    /usr/local/bin/frpc.ini

2. 在本地运行起 index.py （使用 web.py 搭建的本地 http 服务器），用以接收通过内网穿透发送过来的 http get请求，获取 get 请求传递过来的参数。
    python index.py 8888

3. 使用 python 调用 C程序，将 http get 请求中解析出来的数据传入 duoji.c 编译后的文件中，用以驱动舵机旋转。

注意：
1. 舵机控制引脚（自然引脚）为 7、11，对应 Wpi 引脚为 7、0.
2. frpc 安装控制目录在 /usr/local/bin/frpc
3. frpc 需要使用 http 协议，使用自己的域名（通过Cname方式绑定提供的域名IP）
4. python 中函数内如果需要修改全局参数的值，需要在函数内、参数前加上关键字 global ,否则会报错      
5. 本地 http 服务器访问端口需要与 frpc 配置的端口一致（端口：8888），运行该 py 程序时，需要在末尾加上端口号，如：python index.py 8888