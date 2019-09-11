import socket

s = socket.socket()
host_name = socket.gethostname() 
host_ip = socket.gethostbyname(host_name) 
print("Hostname :  ",host_name) 
print("IP : ",host_ip) 
host = socket.gethostname()
port = input (str("Please enter the port number: "))
s.bind((host,port))
filename = input(str("Please enter the filename of the file : "))
file = open(filename , 'rb')
file_data = file.read(1024)
s.listen(5)
print(host + " , " + host_ip + " server has started!")
print("Waiting for any incoming connections ... ")

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    data = conn.recv(1024)
    print('Server received', repr(data))

    fname= str(filename)
    f = open(fname,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()

    conn.send(file_data)
    print("Data has been transmitted successfully")
    conn.close()

