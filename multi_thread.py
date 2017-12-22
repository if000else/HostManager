import time,paramiko,threading,os

Hosts = {
    "g1":[("10.0.0.3",1212),("10.0.0.4",1212,)],
    "g2":[("10.0.0.5",1212,)],
    "g3":[("10.0.0.6",1212,)],
}



help_menu = '''\033[1;32;1m
----------------------------------------
Please select/input according to prompt.
1.select  select group/host
2.put  upload files to selected hosts
3.get  download files to selected hosts
----------------------------------------\033[0m
'''


def login():
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


def put(choice):
    print("hh",choice)


def get(choice):
    print("hh", choice)





if __name__ == '__main__':

    choice = [] # global var
    a = login()
    while a:
        print(help_menu)
        inp = input("please input(1,2,3,b):")
        if inp == '1':
            while inp != 'b':
                for group in Hosts.keys():  # print group
                    print("[%s]\n" % group,end='----\n')
                    # for host in Hosts[group]:  # print host
                    #     print(host)
                inp = input("Input group:")
                if inp in Hosts.keys():
                    choice = Hosts[inp]
                    trace = {}
                    for i,host in enumerate(choice,1):
                        print(i,host)
                        trace.setdefault(str(i),host)
                    inp = input("chose num:")
                    if inp in trace:
                        choice.clear()
                        choice.append(trace[inp])
            else:
                print("You have choose:", choice)

        elif inp == '2':
            if choice:
                get(choice)
            else:
                print("Please select hosts!")
        elif inp == '3':
            if choice:
                get(choice)
            else:
                print("Please select hosts!")
        elif inp == 'b':
            pass
        else:
            print("Invalid input!")


