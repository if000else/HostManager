# 类 Fabric 主机管理程序开发：
# 1. 运行程序列出主机组或者主机列表
# 2. 选择指定主机或主机组
# 3. 选择让主机或者主机组执行命令或者向其传输文件（上传/下载）
# 4. 充分使用多线程或多进程
# 5. 不同主机的用户名密码、端口可以不同
import paramiko,threading,pickle,os

Base_path = os.path.dirname(os.path.abspath(__file__))
config_path = Base_path +'/files/config'
#主机配置信息管理
list_host = [{'host':'192.168.117.236','port':22,'user':'ubuntu1','password':'ubuntu1','group':1},
             {'host':'192.168.117.237','port':22,'user':'ubuntu2','password':'ubuntu2','group':1},
             {'host':'192.168.117.239','port':22,'user':'ubuntu3','password':'ubuntu3','group':2},
             {'host':'192.168.117.240','port':22,'user':'aaa','password':'bbb','group':2}]
def pickle_dump(path,file):
    #存入配置文件
    with open(path,'wb') as f:
        pickle.dump(file,f)
#pickle_dump(config_path,list_host)
def pickle_load(path):
    #取出配置文件
    with open(path,'rb') as f:
        list_host_new = pickle.load(f)
    return list_host_new
# list_host_new = pickle_load(config_path)
# print(list_host_new)


class Paramiko_sshd(object):
    #sshd类
    def __init__(self,host,port,user,password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def sshd_command(self,command):
        #ssh远程主机执行命令，并返回结果
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(self.host,self.port,self.user,self.password)
            std_in,std_out,std_err = ssh_client.exec_command(command)
            print(self.host.center(30,'*'))
            print(command.upper().center(30,'='))
            for line in std_out:
                print(line.strip('\n'))
            ssh_client.close()
        except Exception as e:
            print(e)
    def sshd_upload_file(self,server_path,local_path):
        #上传文件
        try:
            t = paramiko.Transport((self.host,self.port))
            t.connect(username=self.user,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(local_path,server_path)
            t.close()
            print(self.host.center(30, '*'))
            print('上传成功')
        except Exception as e:
            print(e)
    def sshd_down_file(self,server_path,local_path):
        #下载文件
        try:
            t = paramiko.Transport((self.host, self.port))
            t.connect(username=self.user, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.get(server_path, local_path)
            t.close()
            print(self.host.center(30, '*'))
            print('下载成功')
        except Exception as e:
            print(e)
def help():
    #帮助信息
    command_option = input('''
    *************请选择***********
    1.执行命令
    2.上传文件
    3.下载文件
    4.返回
    5.退出程序
    ''').strip()
    return command_option

def review():
    while 1:
        #展示界面
        list_host_new = list_host#pickle_load(config_path)
        host_group_1 = []
        host_group_2 = []
        for line in list_host_new:
            if line['group'] == 1:
                host_group_1.append(line)
            else:
                host_group_2.append(line)
        print('group-1'.center(30,'='))
        for line_1 in host_group_1:
            print('host:',line_1['host'],'port:',line_1['port'])
        print('group-2'.center(30,'='))
        for line_2 in host_group_2:
            print('host:',line_2['host'],'port:',line_2['port'])

        group_select = input('请输入您要操作的主机组：\033[1;35m group-1 \033[0m | \033[1;35m group-2 \033[0m '
                             '或输入\033[1;35mexit\033[0m退出程序 ==>').strip()
        if group_select in ['group-1','group-2']:
            if group_select == 'group-1':     #增加中间变量，来确定是对组一操作还是对组二进行操作
                group_sure = host_group_1
            else:
                group_sure = host_group_2
            while 1:
                command_option = help()
                if command_option == '1':
                    command = input('请输入执行的命令：').strip()
                    for line_3 in group_sure:
                        sshd = Paramiko_sshd(line_3['host'],line_3['port'],line_3['user'],line_3['password'])
                        t = threading.Thread(target=sshd.sshd_command,args=(command,))
                        t.start()
                        t.join()

                elif command_option == '2':
                    server_path = input('请输入上传到的服务器目录：').strip()
                    local_path = input('请输入本地文件目录：').strip()
                    for line_3 in group_sure:
                        sshd = Paramiko_sshd(line_3['host'],line_3['port'],line_3['user'],line_3['password'])
                        t = threading.Thread(target=sshd.sshd_upload_file,args=(server_path,local_path,))
                        t.start()
                        t.join()

                elif command_option == '3':
                    server_path = input('请输入下载的服务器目录文件路径：').strip()
                    local_path = input('请输入存放到本地的路径：').strip()
                    for line_3 in group_sure:
                        sshd = Paramiko_sshd(line_3['host'],line_3['port'],line_3['user'],line_3['password'])
                        t = threading.Thread(target=sshd.sshd_down_file,args=(server_path,local_path,))
                        t.start()
                        t.join()
                elif command_option == '4':
                    break
                elif command_option == '5':
                    exit()
                else:
                    print('%s为非法命令，请重新输入！'%command_option)
        elif group_select == 'exit':
            break
        else:
            print('%s为非法命令，请重新输入！'%group_select)



if __name__ =='__main__':
    review()