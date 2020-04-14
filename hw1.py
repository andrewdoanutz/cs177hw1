import message_pb2
import socket
import binascii
import array

def send(server,typeCode,keyVal=None,key=None):
    print("Sending message to server...")
    if(typeCode==0):
        r=message_pb2.type0()
        r.type=0

    elif(typeCode==2):
        r=message_pb2.type2()
        r.type=2

    elif(typeCode==4):
        
        if key not in keyVal:
            r=message_pb2.type5()
            r.type=5
        else:
            r=message_pb2.type4()
            r.type=4
            r.value=keyVal[key]

    elif(typeCode==5):
        r=message_pb2.type5()
        r.type=5

    elif(typeCode==7):
        r=message_pb2.type7()
        r.type=7
        r.count=len(keyVal)
        
    lenMessage=(bytes([r.ByteSize()]))
    if(len(lenMessage)<2):
        lenMessage=b"\x00"+lenMessage
    server.send(lenMessage)
    print("len:",lenMessage,"sent message:",r,"in bytes:",r.SerializeToString())
    server.send(r.SerializeToString())
    


def parseMessage(typeCode,message,keyVal):
    if(typeCode==0):
        r=message_pb2.type0()
        r.ParseFromString(message)
    elif(typeCode==1):
        r=message_pb2.type1()
        r.ParseFromString(message)
        keyVal[r.key]=r.value
    elif(typeCode==3):
        r=message_pb2.type3()
        r.ParseFromString(message)
    elif(typeCode==6):
        r=message_pb2.type6()
        r.ParseFromString(message)
    elif(typeCode==8):
        r=message_pb2.type8()
        r.ParseFromString(message)
    elif(typeCode==9):
        r=message_pb2.type9()
        r.ParseFromString(message)
    else:
        return None
    return r

def sendMessage(server,typeCode,message,keyVal):
    #send based on recieved type
    if(typeCode==1):
        send(server,2)
    elif(typeCode==3):
        send(server,4,keyVal,message.key)
    elif(typeCode==6):
        send(server,7,keyVal)
    elif(typeCode==8):
        print(message.error)
    elif(typeCode==9):
        print(message.flag)
        


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ipAdd = "cs177.seclab.cs.ucsb.edu"
port = 59871
server.connect((ipAdd, port))

keyVal={}



while(True):
    send(server,typeCode=0)
    print("\nWaiting for server reply...")
    recMess=b""
    while(len(recMess)<2):
        recMess+=server.recv(1)
    size=int.from_bytes(recMess, byteorder='big')
    print("server reply for size:",recMess,"size:",size)
    recMess=b""
    while(len(recMess)<size):
        recMess+=server.recv(1)
    typeCode=parseMessage(0,recMess,keyVal)
    typeCode=typeCode.type
    # recMess=recMess[:-1]
    parsed=parseMessage(typeCode,recMess,keyVal)
    print("server reply:",recMess,"type:",typeCode,"parsed:",parsed)

    sendMessage(server,typeCode,parsed,keyVal)


