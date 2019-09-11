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
import pyotp

root = Tk()
root.title("P2P File Transfer")
file = StringVar()
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

start_btn = Button(root,text="Register", command=lambda:register())
start_btn.grid(row=0,column=2,padx=10,pady=10,sticky="nsew")

label = Label(root, text="Client Software ", font=("Arial",26),bg="black",fg="White")
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


file_select = Button(root, text="Select File", command=lambda:fileDialog())
file_select.grid(row=4, column=0, padx=8, pady=8, sticky="NSNESWSE")

e_data=Entry(root , textvariable=file)
e_data.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

code=Label(root,text="Verification Code")
code.grid(row=5, column=0, padx=8, pady=8, sticky="NSNESWSE")


e_code=Entry(root)
e_code.grid(row=5, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

message_label=Label(root,text="System Logs",font=("Arial,12"))
message_label.grid(row=6,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

scrollbar_y =Scrollbar(root)
scrollbar_y.grid(row=7, column=3,rowspan=6)

show_1=Text(root,height=8, width=35, yscrollcommand=scrollbar_y.set, bg="light Grey",fg="White")
show_1.grid(row=7, column=0,rowspan=3,columnspan=3,sticky="NSEW")

start_btn = Button(root,text="Receive from Server", command=lambda:verify())
start_btn.grid(row=16,column=0,padx=10,pady=10,sticky="nsew")

# copyright_label=Label(root,text="© Created by Jia Da Wu",font=("Arial",10))
copyright_label.grid(row=18,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

def register():
    root.destroy()
    import otp

def verify():
    key="PL3VPSAOQ3AROS43"
    totp = pyotp.TOTP(key)
    pcode=totp.now()
    print (pcode)
    passcode= str(e_code.get())
    print (passcode)
    print (pcode)
    if passcode == pcode:
        connect()
        e_code.delete(0,END)
                    
    else:
        messagebox.showinfo("Invaild", "Incorrect verication code, please try again!")
        e_code.delete(0,END)
def connect():
    
            e_data_v = e_data.get()
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
           

            HOST, PORT = e_host_v, e_port_v
            data = e_data_v
            filename= str(e_data_v)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            show_1.insert(END,"Connected to Server!")
            show_1.insert(END,"\n")
            aes_key_generator()
            show_1.insert(END,"Encrypting file with AES key...")
            show_1.insert(END,"\n")
            with open('key.key', 'rb') as f:
                data = f.read()
            key = data # Can only use kdf once
            print (key)
            input_file = e_data_v
            output_file = 'file.encrypted'

            with open(input_file, 'rb') as f:
                data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

            with open(output_file, 'wb') as f:
                f.write(encrypted)

            with open ('p_key.encrypted', 'wb') as f:
                public_key = s.recv(1024)
                print (public_key)
                f.write(public_key)
                f.close()
                show_1.insert(END,"Public key Received!")
                show_1.insert(END,"\n")
                aes_decryption()
                rsa_encryption()
            
            with s:
                sbuf = buffer.Buffer(s)

                hash_type = 'abc'
                file = 'file.encrypted'
                key = 'key.encrypted'
                files = (file + " " + key)
                files_to_send = files.split()

                for file_name in files_to_send:
                    print(file_name)
                    sbuf.put_utf8(hash_type)
                    sbuf.put_utf8(file_name)

                    file_size = os.path.getsize(file_name)
                    sbuf.put_utf8(str(file_size))

                    with open(file_name, 'rb') as f:
                        sbuf.put_bytes(f.read())
                    print('File Sent')
                    show_1.insert(END,"Files sent!")
                    show_1.insert(END,"\n")
                    show_1.see(END)

def fileDialog():
    e_data.delete(0,END)
    filepath = filedialog.askopenfilename(initialdir="/", title = "Select a File")
    e_data.insert(END,filepath)

def aes_decryption():           
            #decryption start from here
            password_provided = "isys565" # This is input in the form of a string
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
            input_file = 'p_key.encrypted'
            output_file = 'p_key.pem'

            with open(input_file, 'rb') as f:
                data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.decrypt(data)

            with open(output_file, 'wb') as f:
                f.write(encrypted)
            show_1.insert(END,"Decrypt RSA Public key with AES key!")
            show_1.insert(END,"\n")
def rsa_encryption():
    with open("p_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

    #encryption
    f = open('key.key', 'rb')
    encrypted_file = f.read()
   
    encrypted = public_key.encrypt(
            encrypted_file,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    f = open('key.encrypted', 'wb')
    f.write(encrypted)
    f.close()
    show_1.insert(END,"Encrypted AES key with RSA Public key!")
    show_1.insert(END,"\n")
def aes_key_generator():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key) # The key is type bytes still
    file.close()
    show_1.insert(END,"AES key generated!")
    show_1.insert(END,"\n")
root.mainloop()
