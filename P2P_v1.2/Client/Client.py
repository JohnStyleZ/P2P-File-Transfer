from tkinter import *
from tkinter import messagebox
from socket import *
import socket
import time
import datetime
import _thread
import sys


        
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


e_data=Entry(root , textvariable=file)
e_data.grid(row=3, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
e_data.insert(END,"file.txt")


message_label=Label(root,text="Client Message",font=("Arial,12"))
message_label.grid(row=4,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

scrollbar_y =Scrollbar(root)
scrollbar_y.grid(row=5, column=3,rowspan=6)

show_1=Text(root,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="light Grey",fg="White")
show_1.grid(row=4, column=0,rowspan=3,columnspan=3,sticky="NSEW")

start_btn = Button(root,text="Receive from Server", command=lambda:connect())
start_btn.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")



def connect():
            e_data_v = e_data.get()
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())


            HOST, PORT = e_host_v, e_port_v
            data = e_data_v
            filename= str(e_data_v)
            # Create a socket (SOCK_STREAM means a TCP socket)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Connect to server and receive data
                s.connect((HOST, PORT))
                s.sendall(bytes(data + "\n", "utf-8"))

                with open(filename,'wb') as f:
                    print('file opened')
                    while True:
                        print('receiving data...')
                        data = s.recv(1024)
                        print('data=%s', (data))
                        show_1.insert(END,'File Receiving... !')
                        show_1.insert(END,'\n')
                        if not data:
                            break
                        f.write(data)
                        #show_1.insert(END,'File Receiving... !')
                        #show_1.insert(END,'\n')


            f.close()
            show_1.insert(END,'File Received !')
            show_1.insert(END,'\n')
            s.close()

root.mainloop()

      

