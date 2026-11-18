import socket #import the network module
#set the target host and port range
HOST = "localhost"
for port in range(30000,40001):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP socket
    s.settimeout(1) # set a timeout
    result=s.connect_ex((HOST,port))#connect and keep the result
    # print result
    if result == 0:
        print(f"Port {port} is open")
    s.close()#close the socket
