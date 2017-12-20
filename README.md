##类 Fabric 主机管理程序

### 作者介绍：

Author：Yaoqing Wang

Nickname:Huayiqiu

Blog:http://www.cnblogs.com/iforelse

类 Fabric 主机管理程序开发：
1. 运行程序列出主机组或者主机列表
2. 选择指定主机或主机组
3. 选择让主机或者主机组执行命令或者向其传输文件（上传/下载）
4. 充分使用多线程或多进程
5. 不同主机的用户名密码、端口可以不同


    *admin 123456* to login in local system

    *admin 123456*  to login in server


运行：先运行server.py,启动服务，然后运行ftp.py

详细请看.jpg

目录结构：

`SimpleFTP/`

`　　|-- bin/`

`　　　　| |-- ftp.py`

`　　|`

`　　|-- conf/`

`　　　　| |-- settings.py`

`　　|-- database/`

`　　　　|　|-- client/`

`　　　　|　|-- server/`

`　　　　|　|-- users/`

`　　　　| `

`　　|-- report/`

`　　　　|　|-- log/`

`　　　　|　|  |-- access.log`

`　　　　|　|  |-- client.log`

`　　　　|　|  |-- server.log`

`　　　　|　|  |-- services.log`
        
`　　　　| `

`　　|-- modules/`

`　　　　| |-- display.py`

`　　　　| |-- log.py`

`　　　　| |-- main.py`

`　　　　| |-- server.py`

`　　　　| |-- funcs.py`


`　　　　|`

`　　|-- README`
