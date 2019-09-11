from tkinter import *
from tkinter import messagebox
from socket import *
from tkinter import filedialog
import time
import datetime
import _thread
import os
import socket

def my_server(show_1,HOST,PORT):


    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    tcpTimeSrvrSock = socket.socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(10)
    currentDT = datetime.datetime.now()
    e_file_1 = e_file.get()
    
    

    while True:
        show_1.insert(END,"waiting for connection...")
        show_1.insert(END,"\n")
        #print ('waiting for connection...')

        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()

        #print ('...connected from:', addr)
        show_1.insert(END,"connected {}".format(addr))
        show_1.insert(END,"\n")

        filename= str(e_file_1)
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
        tcpTimeClientSock.send(bytes("Thank you for connecting", 'utf-8'))
        tcpTimeClientSock.close()

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

#l_file=Label(root,text="File Name")
#l_file.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")
file_select = Button(root, text="Select File", command=lambda:fileDialog())
file_select.grid(row=4, column=0, padx=8, pady=8, sticky="NSNESWSE")
#selectbutton()

e_file=Entry(root , text = "", textvariable=file)
e_file.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
#e_file.insert(END,"file.txt")


message_label=Label(root,text="System Logs",font=("Arial,12"))
message_label.grid(row=5,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

scrollbar_y =Scrollbar(root)
scrollbar_y.grid(row=6, column=3,rowspan=6)

show_1=Text(root,height=8, width=35, yscrollcommand=scrollbar_y.set, bg="light Grey",fg="White")
show_1.grid(row=6, column=0,rowspan=3,columnspan=3,sticky="NSEW")

start_btn = Button(root,text="Start Server", command=lambda:connect())
start_btn.grid(row=15,column=0,padx=10,pady=10,sticky="nsew")



def connect():
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0
            



root.mainloop()





