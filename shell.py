import paramiko, sys, os, socket, select, getpass, termios, tty
from paramiko.py3compat import u

tran = paramiko.Transport(('10.0.0.3', 1212,))
tran.start_client()
tran.auth_password('root', 'huayiqiu')
# 打开一个通道
chan = tran.open_session()
# 获取一个终端
chan.get_pty()
# 激活器
chan.invoke_shell()

# 获取原tty属性
oldtty = termios.tcgetattr(sys.stdin)
try:
    # 为tty设置新属性
    # 默认当前tty设备属性：
    #   输入一行回车，执行
    #   CTRL+C 进程退出，遇到特殊字符，特殊处理。
    # 这是为原始模式，不认识所有特殊符号
    # 放置特殊字符应用在当前终端，如此设置，将所有的用户输入均发送到远程服务器
    tty.setraw(sys.stdin.fileno())  # 恢复终端原始状态，每按一个键就发送
    chan.settimeout(0.0)

    while True:
        # 监视 用户输入 和 远程服务器返回数据（socket）
        # 阻塞，直到句柄可读
        r, w, e = select.select([chan, sys.stdin], [], [], 1)
        if chan in r:  # 获取服务返回的内容
            try:
                x = u(chan.recv(1024))
                if len(x) == 0:
                    print('\r\n*** EOF\r\n')
                    break
                sys.stdout.write(x)
                sys.stdout.flush()
            except socket.timeout:
                pass
        if sys.stdin in r:  # 发送命令
            x = sys.stdin.read(1)  # 读取一个字符
            if len(x) == 0:
                break
            chan.send(x)  # 发送一个字符

finally:
    # 重新设置终端属性,将终端状态还原
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

chan.close()
tran.close()