import paramiko,sys,os,select

Hosts = {
    '10.0.0.3':1212,
    '10.0.0.4':1212,

}
username = 'admin'
password = '123456'
port=1212
while True:
    print("Welcome!")
    user = input("input username:").strip()
    psd = input("input password:").strip()
    if user == username and psd == password:
        while True:
            host_list=[]
            for key,host in enumerate(Hosts.keys(),1):
                print(key,host)
                host_list.append((key,host))
            inp = int(input("input:"))
            print("Hosts List:")
            for num in host_list:
                if inp == num[0]:
                    print(num[1])
                    print("port:",Hosts[num[1]])
                    break
        else:
            pass
    else:
        print("not match!")
    break
else:
    pass

class WindosShell(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port
        # self.username = 'root'
        # self.password = 'huayiqiu'
        self.tran = paramiko.Transport((self.host, self.port))
        self.tran.connect(username="root", password='huayiqiu')
        self.ssh = paramiko.SSHClient()
        self.ssh._transport = self.tran
        # 打开一个通道
        chan = self.tran.open_session()
        # 获取一个终端
        chan.get_pty()
        # 激活器
        chan.invoke_shell()
    def listen(self):
        while True:
            # 监视用户输入和服务器返回数据
            # sys.stdin 处理用户输入
            # chan 是之前创建的通道，用于接收服务器返回信息
            readable, writeable, error = select.select([self.chan, sys.stdin, ], [], [], 1)
            if self.chan in readable:
                try:
                    x = self.chan.recv(1024)
                    if len(x) == 0:
                        print('\r\n*** EOF\r\n',)
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except self.socket.timeout:
                    pass
            if sys.stdin in readable:
                inp = sys.stdin.readline()
                self.chan.sendall(inp)
"""
tran = paramiko.Transport(('10.0.0.3', 1212))
tran.connect(username="root",password='huayiqiu')
ssh = paramiko.SSHClient()
ssh._transport = tran
# 打开一个通道
chan = tran.open_session()
# 获取一个终端
chan.get_pty()
# 激活器
chan.invoke_shell()

#########
# 利用sys.stdin,肆意妄为执行操作
# 用户在终端输入内容，并将内容发送至远程服务器
# 远程服务器执行命令，并将结果返回
# 用户终端显示内容
#########

def windows_shell(chan):
    import threading

    print("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.")

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                print('*** EOF ***')
                break
            # sys.stdout.write(str(data))
            # sys.stdout.flush()
            print(data.decode())
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass

shell = windows_shell(chan)
chan.close()
tran.close()
"""