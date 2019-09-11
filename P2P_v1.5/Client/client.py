from tkinter import *
from tkinter import messagebox
from socket import *
from tkinter import filedialog
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

import socket
import time
import datetime
import _thread
import sys
import base64
import os
import buffer

def rsa_key_generator():
    # Generating private and public keys
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

# Storing the keys
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb') as f:
        f.write(pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb') as f:
        f.write(pem)

def aes_encryption():
    #encryption start from here
    password_provided = 'isys565' # This is input in the form of a string
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
    input_file = 'public_key.pem'
    output_file = 'p_key.encrypted'

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)
        
root = Tk()
root.title("P2P File Transfer")
file = StringVar()
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

label = Label(root, text="Client Software ", font="Arial,16",bg="black",fg="White")
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

#l_key=Label(root,text="Public Key")
#l_key.grid(row=4, column=0, padx=8, pady=8, sticky="NSNESWSE")

#e_key=Entry(root)
#e_key.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")


file_select = Button(root, text="Save File", command=lambda:fileDialog())
file_select.grid(row=4, column=0, padx=8, pady=8, sticky="NSNESWSE")

e_data=Entry(root , textvariable=file)
e_data.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")


message_label=Label(root,text="System Logs",font=("Arial,12"))
message_label.grid(row=5,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

scrollbar_y =Scrollbar(root)
scrollbar_y.grid(row=6, column=3,rowspan=6)

show_1=Text(root,height=8, width=35, yscrollcommand=scrollbar_y.set, bg="light Grey",fg="White")
show_1.grid(row=6, column=0,rowspan=3,columnspan=3,sticky="NSEW")

start_btn = Button(root,text="Receive from Server", command=lambda:connect())
start_btn.grid(row=15,column=0,padx=10,pady=10,sticky="nsew")

copyright_label=Label(root,text="© Created by Jia Da Wu",font=("Arial,12"))
copyright_label.grid(row=17,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

rsa_key_generator()
aes_encryption()
def connect():
            e_data_v = e_data.get()
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            e_key_v=str(e_key.get())

            HOST, PORT = e_host_v, e_port_v
            data = e_data_v
            filename= str(e_data_v)
            # Create a socket (SOCK_STREAM means a TCP socket)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Connect to server and receive data
                s.connect((HOST, PORT))
                #send public key to server
                p_key = 'p_key.encrypted'
                f = open(p_key,'rb')
                l = f.read(1024)
                s.send (l)
                
                s.sendall(bytes(data + "\n", "utf-8"))
                
                connbuf = buffer.Buffer(s)

                while True:
                        hash_type = connbuf.get_utf8()
                        if not hash_type:
                            break
                        print('hash type: ', hash_type)

                        file_name = connbuf.get_utf8()
                        if not file_name:
                            break
                        file_name = os.path.join('uploads',file_name)
                        print('file name: ', file_name)

                        file_size = int(connbuf.get_utf8())
                        print('file size: ', file_size )

                        with open(file_name, 'wb') as f:
                            remaining = file_size
                            while remaining:
                                chunk_size = 4096 if remaining >= 4096 else remaining
                                chunk = connbuf.get_bytes(chunk_size)
                                if not chunk: break
                                f.write(chunk)
                                remaining -= len(chunk)
                            if remaining:
                                print('File incomplete.  Missing',remaining,'bytes.')
                            else:
                                print('File received successfully.')
                print('Connection closed.')
                s.close()
                #with open(filename,'wb') as f:
                #    print('file opened')
                #    while True:
                #        try:
                #            print('receiving data...')
                #            data = s.recv(1024)
                #            print('data=%s', (data))
                #            show_1.insert(END,'File Receiving... !')
                #            show_1.insert(END,'\n')
                #            if not data:
                #                break
                #            f.write(data)
                #            show_1.insert(END,'File Received... !')
                #            show_1.insert(END,'\n')

                #        except ConnectionResetError:
                #            pass
                        

                #    f.close()
                #    show_1.insert(END,'File Received !')
                #    show_1.insert(END,'\n')
                #    s.close()
          
            #decryption start from here
            password_provided = 'isys565' # This is input in the form of a string
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
            input_file = filename
            output_file = filename

            with open(input_file, 'rb') as f:
                data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.decrypt(data)

            with open(output_file, 'wb') as f:
                f.write(encrypted)
                
def fileDialog():
    filepath = filedialog.asksaveasfilename(initialdir="/", title = "Save File Location")
    e_data.insert(END,filepath)

def aes_encryption():
    #encryption start from here
    password_provided = 'isys565' # This is input in the form of a string
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
    input_file = 'public_key.pem'
    output_file = 'p_key.encrypted'

    with open(input_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

root.mainloop()

      

