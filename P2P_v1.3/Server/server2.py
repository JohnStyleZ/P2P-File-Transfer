from tkinter import *
from tkinter import messagebox
from socket import *

import time
import datetime
import _thread


def my_server(show_1,HOST,PORT):


    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(5)
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
        tcpTimeClientSock.send(l)
        print("Done sending")
        #tcpTimeClientSock.send(b 'Thank you for connecting')
        #tcpTimeClientSock.close()
        
root = Tk()
root.title("P2P File Transfer")
file = StringVar()

l_host=Label(root,text="Host Name/IP")
l_host.grid(row=1, column=0, padx=8, pady=8, sticky="NSNESWSE")

e_host=Entry(root)
e_host.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
e_host.insert(END,'127.0.0.1')


l_port=Label(root,text="Port")
l_port.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

e_port=Entry(root)
e_port.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
e_port.insert(END,12121)

l_file=Label(root,text="File Name")
l_file.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")


e_file=Entry(root , textvariable=file)
e_file.grid(row=3, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
e_file.insert(END,"file.txt")


message_label=Label(root,text="Client Message",font=("Arial,12"))
message_label.grid(row=4,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

scrollbar_y =Scrollbar(root)
scrollbar_y.grid(row=5, column=3,rowspan=6)

show_1=Text(root,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="light Grey",fg="White")
show_1.grid(row=4, column=0,rowspan=3,columnspan=3,sticky="NSEW")

start_btn = Button(root,text="Start Server", command=lambda:connect())
start_btn.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")



def connect():
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            #start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0


root.mainloop()





