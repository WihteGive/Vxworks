#Vxhunter(TableBegin,ImageBase)，该函数的作用是利用符号表修复Vxworks固件中的函数名称
import ida_bytes
import binascii
def GetName(Ad):
    name=bytes()
    while(1):
        ascii=ida_bytes.get_byte(Ad)
        if(ascii==0):
            break
        Ad=Ad+1
        name=name+chr(ascii)
    return name
def Vxhunter(begin,ImageBase):
    Now=MBegin=begin+ImageBase-0x64
    while(1):
        tmp=[]
        for i in range(0,16,4):
            tmp.append(ida_bytes.get_32bit(Now+i))
        if(tmp[0]!=0):
            break;
        if(tmp[3]==458752):
            FunName=GetName(tmp[1])
            print('位于'+str(hex(tmp[2]))+'函数名称为：'+FunName)
            MakeNameEx(tmp[2],FunName,0)
        Now=Now+32
    print('符号表开头为:'+str(hex(MBegin)))
Vxhunter(833380,0x308000)