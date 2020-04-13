import message_pb2
import socket
import struct

def readyMessage(message,typeCode,key=None,value=None,count=None,error=None,flag=None):
    message.Clear()
    message.type=typeCode
    if(key is not None):
        message.key=key

    if value is not None:
        message.value=value

    if count is not None:
        message.count=count
    if error is not None:
        message.error=error
    if flag is not None:
        message.flag=flag
        
def send(server,message):
    server.send(bytes(message.ByteSize()))
    server.send(message.SerializeToString())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ipAdd = "cs177.seclab.cs.ucsb.edu"
port = 25592
server.connect((ipAdd, port))

sendMessage=message_pb2.totalMessage()

readyMessage(sendMessage,typeCode=0)
send(server,sendMessage)

print("Waiting for server reply...")
recMessage=server.recv(2)
decoded=int.from_bytes(recMessage, byteorder='big')
print("server reply:",recMessage,"decoded:",decoded)
r=message_pb2.totalMessage()
r.ParseFromString(recMessage)
print(r)

print("Waiting for server reply...")
recMessage=server.recv(decoded)
decoded=int.from_bytes(recMessage, byteorder='big')
print("server reply:",recMessage,"decoded:",decoded)

# readyMessage(sendMessage,typeCode=7,count=0)
# send(server,sendMessage)

# print("Waiting for server reply...")
# recMessage=server.recv(2)
# decoded=int.from_bytes(recMessage, byteorder='big')
# print("server reply:",recMessage,"decoded:",decoded)