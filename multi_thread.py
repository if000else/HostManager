import time,paramiko,threading,queue

Hosts = {
    "G1":[("10.0.0.3",1212),("10.0.0.4",1212)],
    "G2":[("10.0.0.5",1212)],
    "G3":[("10.0.0.6",1212)]
}



help_menu = '''\033[1;32;1m
----------------------------------------
Please select/input according to prompt.
1.select  select group/host
2.run   run the muti hosts command line
----------------------------------------\033[0m
'''


def login():
    '''
    login local system
    :return:
    '''
    print("welcome!")
    # user = input("username:").strip()
    # psd = input("password:").strip()
    user = 'admin'
    psd = '123456'
    if user == 'admin' and psd == '123456':
        print("login success!")
        return 1
    else:
        print("login failed.")
        return 0

class multi_hosts(object):
    '''
    by instance a class with host/hosts,must be list type
    '''
    def __init__(self,host):
        '''
        import a list with tuple as items [(1,2)]
        :param host:
        '''
        self.lock = threading.Lock()
        self.host = host
        self.run()

    def put(self,host,comm):
        '''
        send files
        sftp.put('D:/New folder/oldboy.txt','/tmp/from_windows')
        :param host:
        :param comm:
        :return:
        '''
        list_comm= comm.split()
        tran = paramiko.Transport(host)
        tran.connect(username='root', password='huayiqiu')
        sftp = paramiko.SFTPClient.from_transport(tran)
        try:
            with self.lock:
                sftp.put(list_comm[1], list_comm[2])
                res = "\033[1;32;1mtask [put] is finished!\033[0m"
                # self.lock.acquire()
                print(res)
        except Exception as e:
            print(e)
        finally:
            # self.lock.release()
            sftp.close()
    def get(self,host,comm):
        '''
        recv files
        sftp.get('D:/New folder/oldboy.txt','/tmp/from_windows')
        :param host:
        :param comm:
        :return:
        '''
        list_comm = comm.split()
        tran = paramiko.Transport(host)
        tran.connect(username='root', password='huayiqiu')
        sftp = paramiko.SFTPClient.from_transport(tran)
        try:
            with self.lock:
                sftp.get(list_comm[1], list_comm[2])
                res = "\033[1;32;1mtask [get] is finished!\033[0m"
                # self.lock.acquire()
                print(res)
        except Exception as e:
            print(e)
        finally:
            # self.lock.release()
            sftp.close()

    def exec_comm(self,host,comm):
        '''
        exec ssh command
        :param host:
        :param comm:
        :return:
        '''
        tran = paramiko.Transport(host)
        tran.connect(username='root',password='huayiqiu')
        ssh = paramiko.SSHClient()
        ssh._transport = tran
        try:
            with self.lock:
                stdin,stdout,stderr = ssh.exec_command(comm)
                # self.lock.acquire()
                print("\033[1;32;1mresult from host [%s]:\033[0m"%host[0])
                for line in stderr:
                    print(line)
                for line in stdout:
                    print(line)
        except Exception as e:
            print("error:",e)
        finally:
            # self.lock.release()
            ssh.close()

    def run(self,):
        '''
        how to interaction with host/hosts
        :return:
        '''
        while True:
            print("--------------------------------------------\n"
                  "if you want to transfer files,use as follows:\n"
                  "put  D:/linux/test.txt /data/test.txt\n"
                  "get  /data/test.txt D:/linux/test.txt\n"
                  "--------------------------------------------\n")
            comm = input("command:").strip()
            if comm.startswith("put"):
                for h in self.host:
                    t = threading.Thread(target=self.put,args=((h,comm)))
                    t.start()
            elif comm.startswith("get"):
                for h in self.host:
                    t = threading.Thread(target=self.get,args=((h,comm)))
                    t.start()
            elif comm == 'b':
                break
            else:
                for h in self.host:
                    t = threading.Thread(target=self.exec_comm,args=((h,comm)))
                    t.start()


if __name__ == '__main__':

    choice = [] # global var
    trace = {}
    a = login()
    while a:
        print(help_menu)
        inp = input("please input(1,2,b):")
        if inp == '1':
            while inp != 'b':
                trace.clear()
                for i,group in enumerate(Hosts.keys(),1):  # print group
                    print("%s.%s\n" %(i,group))
                    trace.setdefault(str(i),group)
                    # for host in Hosts[group]:  # print host
                    #     print(host)
                inp = input("Input group:")
                if inp in trace:
                    choice=Hosts[trace[inp]].copy()
                    trace.clear()
                    for i,host in enumerate(choice,1):
                        print(i,host)
                        trace[str(i)] = host
                    inp = input("choose num:")
                    if inp in trace:
                        choice.clear()
                        choice.append(trace[inp])
                        print("You have choose:", choice)
                        break
                    else:
                        print("invalid input!")
                else:
                    print("invalid input!")
            else:
                print("You have choose:")
                for i,host in enumerate(choice,1):
                    print(i,host)

        elif inp == '2':
            if choice:
                multi = multi_hosts(choice)
            else:
                print("Please select hosts!")

        elif inp == 'b':
            pass
        else:
            print("Invalid input!")


