import scapy
import socket
import time
from scapy.all import *
class socket_sturct:
    def __init__(self, src,dst,SrcPort,DstPort,_type):
        self.connect=0
        self.src=src
        self.dst=dst
        self.SrcPort=SrcPort
        self.DstPort=DstPort
        self.sock=socket.socket(socket.AF_INET,_type)
        self.sock.bind((self.src,self.SrcPort))
class Resend:
    def __init__(self,packages,OldDst):
        self.packages=packages
        self.TCP=[]
        self.OldDst=OldDst
        self.Rename={'DstDir':{},'DstPortDir':{},'SrcPortDir':{},'SrcDir':{}}#储存要修改的键值对
    def REDst(self,OldDst,Dst):
        self.Rename['DstDir'][OldDst]=Dst
    def REDstPort(self,OldDstPort,DstPort):
        self.Rename['DstPortDir'][OldDstPort]=DstPort
    def RESrc(self,OldSrc,Src):
        self.Rename['SrcDir'][OldSrc]=Src
    def RESrcPort(self,OldSrcPort,SrcPort):
        self.Rename['SrcPortDir'][OldSrcPort]=SrcPort

    def SendPackage(self,count,package):
        pass
        IP=package[count]
        if(package[count].name=='Ethernet'):
            IP=package[count].payload
            if(IP.name!='NoPayload'):
                if(IP.dst==self.OldDst):
                    tmp={'Dst':IP.dst,'Src':IP.src,'DstPort':IP.dport,'SrcPort':IP.sport}

                    #遍历是否需要修改端口
                    for name,data in tmp.items():
                        if( data in self.Rename[name+'Dir']):
                            tmp[name]=self.Rename[name+'Dir'][data]
                    #遍历是否需要修改端口

                    #TCP包
                    if(IP.payload.name=='TCP'):
                        TCP=IP.payload
                        #判断是否已经存在套接字,如果存在则发生负载
                        index=0
                        for i in range(len(self.TCP)):    
                            if(self.TCP[i].src==tmp['Src'] and self.TCP[i].dst==tmp['Dst'] and  self.TCP[i].SrcPort==tmp['SrcPort'] and self.TCP[i].DstPort==tmp['DstPort']):
                                index=1
                                if(TCP.payload):
                                    try:
                                        self.TCP[i].sock.send(TCP.payload.load)
                                        print('第%d个包发送成功',count)
                                        return 1
                                    except WindowsError:
                                        self.TCP[i].sock.close()
                                        del self.TCP[i]
                                        return 0
                                else:
                                    return 1

                        #判断是否已经存在套接字,如果存在则发生负载

                        #生成一个新的套接字，比发送负载
                        if(not index):
                            try:
                                self.TCP.append(socket_sturct(tmp['Src'],tmp['Dst'],tmp['SrcPort'],tmp['DstPort'],socket.SOCK_STREAM))
                                self.TCP[-1].sock.connect((tmp['Dst'],tmp['DstPort']))
                                self.TCP[-1].connect=1

                                if(TCP.payload):
                                    self.TCP[-1].sock.send(TCP.payload.load)
                                    print('第%d个包发送成功',count)
                                    return 1
                            except WindowsError:
                                del self.TCP[-1]
                                return 0

                        #生成一个新的套接字,并发送负载
                   
                    #TCP包

                    else:
                        UDP=IP.payload
                        socket_tmp=socket.socket(socket.AF_INTF,socket.SOCK_DGRAM)
                        socket_tmp.bind((tmp['Src'],tmp['SrcPort']))
                        socket_tmp.sendto(UDP.payload,((tmp['Dst'],tmp['DstPort'])))
                else:
                    return 1
            else:
                return 1


    def begin(self):
        for i in range(len(self.packages.res)):
            a=0
            while not a:
                a=self.SendPackage(i,package)