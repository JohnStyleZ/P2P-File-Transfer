from tkinter import *
from tkinter import messagebox
from socket import *
from tkinter import filedialog
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import time
import datetime
import _thread
import os
import socket
import base64

def my_server(show_1,HOST,PORT):


    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    tcpTimeSrvrSock = socket.socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(5)
    currentDT = datetime.datetime.now()
    e_file_1 = e_file.get()
    e_key_v = str(e_key.get())
    output_file = 'file.encrypted'

    encryption()

    while True:
        show_1.insert(END,"waiting for connection...")
        show_1.insert(END,"\n")
        #print ('waiting for connection...')

        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()

        #print ('...connected from:', addr)
        show_1.insert(END,"connected {}".format(addr))
        show_1.insert(END,"\n")

        filename= output_file
        f = open(filename,'rb')
        l = f.read(1024)
        
        show_1.insert(END,"Done sending")
        show_1.insert(END,"\n")
        
        while (l):
            tcpTimeClientSock.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)
            
        f.close()        
        print("Done sending")
        #tcpTimeClientSock.send(bytes("Thank you for connecting", 'utf-8'))
        tcpTimeClientSock.close()
def encryption():
        #encryption start from here
    e_file_1 = e_file.get()
    e_key_v = str(e_key.get())
    password_provided = e_key_v # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = b'\xea\x1d\xee\xed\x97\xc3\x9d#\nc\x08\x80\xff\xe2\x85\xff' # this key was generated from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    print (key)
    input_file = e_file_1
    output_file = 'file.encrypted'

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
        
    filename = output_file
    file = open(filename , 'rb')
    file_data = file.read(1024)

    
def fileDialog():
    filepath = filedialog.askopenfilename(initialdir="/", title = "Select a File")
    e_file.insert(END,filepath)

root = Tk()
root.title("P2P File Transfer")
file = StringVar()
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

label = Label(root, text="Server Software ", font="Arial,16",bg="black",fg="White")
label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="NSNESWSE")

l_host=Label(root,text="Host Name/IP")
l_host.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

e_host=Entry(root)
e_host.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
e_host.insert(END,host_ip)


l_port=Label(root,text="Port")
l_port.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")

e_port=Entry(root)
e_port.grid(row=3, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
e_port.insert(END,8000)

l_key=Label(root,text="Public Key")
l_key.grid(row=4, column=0, padx=8, pady=8, sticky="NSNESWSE")

e_key=Entry(root)
e_key.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

#l_file=Label(root,text="File Name")
#l_file.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")
file_select = Button(root, text="Select File", command=lambda:fileDialog())
file_select.grid(row=5, column=0, padx=8, pady=8, sticky="NSNESWSE")
#selectbutton()

e_file=Entry(root , text = "", textvariable=file)
e_file.grid(row=5, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
#e_file.insert(END,"file.txt")


message_label=Label(root,text="System Logs",font=("Arial,12"))
message_label.grid(row=6,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

scrollbar_y =Scrollbar(root)
scrollbar_y.grid(row=7, column=3,rowspan=6)

show_1=Text(root,height=8, width=35, yscrollcommand=scrollbar_y.set, bg="light Grey",fg="White")
show_1.grid(row=7, column=0,rowspan=3,columnspan=3,sticky="NSEW")

start_btn = Button(root,text="Start Server", command=lambda:connect())
start_btn.grid(row=16,column=0,padx=10,pady=10,sticky="nsew")

copyright_label=Label(root,text="© Created by Jia Da Wu",font=("Arial,12"))
copyright_label.grid(row=18,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

def connect():
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0
            



root.mainloop()





