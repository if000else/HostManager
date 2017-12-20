import paramiko

# transport = paramiko.Transport(('10.0.0.5', 1212))
# transport.connect(username='root', password='huayiqiu')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.0.0.5',1212,username='root',password='huayiqiu')

stdin, stdout, stderr = ssh.exec_command('df')
for i in stdout:
    print(i)
ssh.close()