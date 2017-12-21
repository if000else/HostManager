#！usr/bin/env python #-*-coding:utf-8-*- # Author calmyan
import configparser
import os ,sys
import threading,time import paramiko,queue
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from cfg import config

class Fabric_gr(object):
     def __init__(self,gr_name):#组名
         self.gr_name='%s%s'%(config.AUTH_FILE,gr_name)#主机组用户名密码文件路径
         self.config_info=configparser.ConfigParser()#读数据对象
         self.name_l=[]#定义一个列表
         self.attr=[]
         self.file_dir=''#上传文件路径
         self.get_file=''#下载传文件路径

     def group_open(self):#打开组文件
         self.config_info.read(self.gr_name)#读取文件
         for i in range(len(self.config_info.sections())):
             self.name_l.append(self.config_info.sections()[i])#信息添加到列表
         else:
             print('主机列表:'.center(40,'='))
             for i in self.name_l:
                 print(('[%s]'%i).center(40,' '))

     def inst_attr(self,inst):#获取指令
         self.instruction=inst
         self.attr=self.instruction.split()
         self.inst_a=self.attr[0]

     def inst(self):#指令判断
         if self.inst_a in config.INST_LIST:
             return True
         else:
             return False

     def open_list(self):#创建 线程 方法
         if self.inst_a==config.PUT:
             if self.File_Dir():#查找本地文件
                 pass
             else:
                 return
         self.re_lilst=[]#定义一个列表
         for j in range(len(self.name_l)):
             sttr=self.config_info.sections()[j]#获取到对象
             user_dict={}#创建一个空字典
             for i,v in self.config_info[sttr].items():#可以循环输出 获ip 用户 密码 端口
                 user_dict[i]=v
             sttr=threading.Thread(target=self.thr_run,args=(sttr,user_dict[config.USER],user_dict[config.PWD],int(user_dict[config.PORTS])))#创建新线程
             sttr.start()#启动线程
             self.re_lilst.append(sttr)#不用JOIN,避免阻塞为串行
         else:
             for i in self.re_lilst:#等待线程 完成
                 i.join()

     def open_list2(self):#创建 线程 方法
         self.re_lilst=[]#定义一个列表
         for j in range(len(self.name_l)):
             sttr=self.config_info.sections()[j]#获取到对象
             user_dict={}#创建一个空字典
             for i,v in self.config_info[sttr].items():#可以循环输出 获ip 用户 密码 端口
                 user_dict[i]=v
             sttr=threading.Thread(target=self.ssh_run,args=(sttr,user_dict[config.USER],user_dict[config.PWD],int(user_dict[config.PORTS])))#创建新线程
             sttr.start()#启动线程
             self.re_lilst.append(sttr)#不用JOIN,避免阻塞为串行
         else:
             for i in self.re_lilst:#等待线程 完成
                 i.join()


     def thr_run(self,addrs,user,paswd,ports):#传输通道
         try:
             transport=paramiko.Transport((addrs,ports))#传输模块  Transport  服务器地址 端口
             transport.connect(username=user,password=paswd)#用户名,,密码
             sftp=paramiko.SFTPClient.from_transport(transport)#调用传输方法
             print('[%s]连接成功!'%addrs)
             self.file_dir='%s/%s'%(config.FILE_DIR,self.attr[1])#上传文件路径
             if self.inst_a==config.PUT:
                 sftp.put(self.file_dir,self.attr[2])#上传文件 ,本地路径文件  ,服务器的路径文件
                 print('【%s】文件上传完成！'%addrs)
             elif self.inst_a==config.GET:
                 self.get_file='%s/%s_%s'%(config.GET_FILE_DIR,addrs,self.attr[2])#下载文件路径
                 print(self.get_file)
                 sftp.get(self.attr[1],self.get_file)#下载文件 ,服务器的路径文件 ,本地路径文件
                 print('【%s】文件下载完成！'%addrs)
             else:
                 print('【%s】文件相关操作失败！'%addrs)
                 pass
         except Exception as e:
             print(e)

     def File_Dir(self):#判断文件是否存在
         file=self.attr[1]

         print(file)
         self.file_dir='%s/%s'%(config.FILE_DIR,file)#文件路径
         if os.path.isfile(self.file_dir):
             print('成功找到文件！')
             return True
         else:
             print('文件不存在！')
             return False
     def ssh_run(self,addrs,user,paswd,ports):#ssh
         ssh =paramiko.SSHClient()#创建一个SSH连接对象
         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#允许连接不在KNOV_HOSTs文件中的主机 自动添加
         try:
             ssh.connect(hostname=addrs,port=ports,username=user,password=paswd)#连接,主机 端口  用户名 密码
             print('[%s]连接成功!'%addrs)
         except Exception as e:
             print(e)
             return
         stdin,stdout,stderr=ssh.exec_command(self.instruction)#.exec_command 为执行命令,返回结果  ,标准输入,标准输出,标准错误,错误与输出只会返回其一
         result=stdout.read()#获取结果
         try:
             if len(result)<1:#如果为空 返回错误信息
                 result=stderr.read()
                 print(addrs.center(60,'='))
                 print(result.decode())
             else:
                 print(addrs.center(60,'='))
                 print(result.decode())
         except Exception as e:
             print(e)


info_l='''--------指令帮助--------
     上传文件：  put file /home/tmp/file （指令  本地文件 服务端位置文件）
     下载文件：  get /home/tmp/file file （指令  服务端位置文件 本地文件）
     其他指令：  ssh相关命令 如 df   pwd  ifconfig ls等
     查看帮助：  helps
     返回上层：  quit
     退出程序：  exit
 '''


def loging():
     print(info_l)
     while True:
         s=os.listdir(config.AUTH_FILE)
         print('主机组'.center(60,'='))
         for i,v in enumerate(s):
             print('编号：%s    组名：%s'%(i,v))
         gr_name=input('选择组:')
         if gr_name=='exit':
             exit()
         if gr_name=='helps':
             print(info_l)
             continue
         try:
             gr_file=s[int(gr_name)]

             lst=Fabric_gr(gr_file)#实例连接
             lst.group_open()#打开
             while True:
                 #print(info_l)
                 inst=input('指令>>>:')
                 if inst=='exit':
                     exit()
                 if inst=='quit':
                     continue
                 if inst=='helps':
                     print(info_l)
                     continue
                 lst.inst_attr(inst)#获取指令
                 if lst.inst():#指令判断
                     lst.open_list()#开启线程创建
                 else:
                     lst.open_list2()
                 pass
         except ValueError as e:
             print