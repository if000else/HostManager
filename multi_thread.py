import time,paramiko,threading

Hosts = {
    {"h1":("10.0.0.3",1212,"G1")},
    {"h2":("10.0.0.4",1212,"G1")},
    {"h3":("10.0.0.5",1212,"G2")},
    {"h4":("10.0.0.6",1212,"G3")},
}


class Manager(object):
    '''
    initialize hosts connection
    '''
    def __init__(self):
        ###ping hosts to confirm connection
        for hosts in Hosts:
            if hosts

