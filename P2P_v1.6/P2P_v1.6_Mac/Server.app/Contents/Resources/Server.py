from tkinter import *
from tkinter import messagebox
from socket import *
from tkinter import filedialog
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

import time
import datetime
import _thread
import os
import socket
import base64
import buffer
import pyotp

    
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
def rsa_decryption():
    show_1.insert(END,"Decrypt AES key with Private key.")
    show_1.insert(END,"\n")
    f = open('download/key.encrypted', 'rb')
    encrypted = f.read()
    with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted = original_message
    f = open('download/key.encrypted', 'wb')
    f.write(decrypted)
    f.close()

    print (decrypted)


                
root = Tk()
root.title("P2P File Transfer")
file = StringVar()
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

start_btn = Button(root,text="Register", command=lambda:register())
start_btn.grid(row=0,column=2,padx=10,pady=10,sticky="nsew")

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

#l_key=Label(root,text="Public Key")
#l_key.grid(row=4, column=0, padx=8, pady=8, sticky="NSNESWSE")

#e_key=Entry(root)
#e_key.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

#l_file=Label(root,text="File Name")
#l_file.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")
file_select = Button(root, text="Save File", command=lambda:fileDialog())
file_select.grid(row=4, column=0, padx=8, pady=8, sticky="NSNESWSE")
#selectbutton()

e_file=Entry(root , text = "", textvariable=file)
e_file.grid(row=4, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
#e_file.insert(END,"file.txt")

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

start_btn = Button(root,text="Start Server", command=lambda:verify())
start_btn.grid(row=16,column=0,padx=10,pady=10,sticky="nsew")

copyright_label=Label(root,text="© Created by Jia Da Wu",font=("Arial,12"))
copyright_label.grid(row=18,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")


e_file_v = e_file.get()
filename = str(e_file_v)
print (filename)
rsa_key_generator()
aes_encryption()

def register():
    root.destroy()
    import otp

def verify():
    key="23BFEXOO3JXO3QY4"
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
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0

def my_server(show_1,HOST,PORT):

    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    s = socket.socket(AF_INET,SOCK_STREAM)
    s.bind(ADDR)
    s.listen(10)
    try:
        os.mkdir('download')
    except FileExistsError:
        pass
    print("Waiting for a connection.....")
    show_1.insert(END,"Waiting for a connection.....")
    show_1.insert(END,"\n")

    while True:
        conn, addr = s.accept()
        print("Got a connection from ", addr)
        show_1.insert(END,"connected {}".format(addr))
        show_1.insert(END,"\n")
        p_key = 'p_key.encrypted'
        f = open(p_key,'rb')
        l = f.read(1024)
        conn.sendall (l)
                
        connbuf = buffer.Buffer(conn)

        while True:
            hash_type = connbuf.get_utf8()
            if not hash_type:
                break
            print('hash type: ', hash_type)

            file_name = connbuf.get_utf8()
            if not file_name:
                break
            file_name = os.path.join('download',file_name)
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
                    show_1.insert(END,'File incomplete.  Missing',remaining,'bytes.')
                    show_1.insert(END,"\n")
                else:
                    print('File received successfully.')
        print('Connection closed.')
        show_1.insert(END,'file name: key.encrypted')
        show_1.insert(END,"\n")
        show_1.insert(END,'file name: file.encrypted')
        show_1.insert(END,"\n")
        show_1.insert(END,'Files received successfully!')
        show_1.insert(END,"\n")
        conn.close()

        rsa_decryption()
        aes_decryption()


def fileDialog():
    e_file.delete(0,END)
    filepath = filedialog.asksaveasfilename(initialdir="/", title = "Save File Location")
    e_file.insert(END,filepath)

def aes_decryption():
            e_file_v = e_file.get()
            filename = str(e_file_v)
            show_1.insert(END,"Decrypt file with AES key.")
            show_1.insert(END,"\n")            
            f = open('download/key.encrypted', 'rb')
            data = f.read()
            key = data # Can only use kdf once
            print (key)
            input_file = 'download/file.encrypted'
            output_file = filename
            print (output_file)
            with open(input_file, 'rb') as f:
                data = f.read()

            fernet = Fernet(key)
            encrypted = fernet.decrypt(data)

            with open(output_file, 'wb') as f:
                f.write(encrypted)
            show_1.insert(END,"Successfully Decrypted!")
            show_1.insert(END,"\n")
            show_1.see(END)
    
root.mainloop()
