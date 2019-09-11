from tkinter import *
import tkinter
import pyotp
import pyqrcode
from tkinter import messagebox
import time 



def countDown():
    lbl2 = Label(self,text="Please scan the QRcode within")
    lbl2.grid(row=3, columnspan=3,padx=8, pady=8, sticky="NSNESWSE")
    lbl2.config(height=1, font=('times', 20, 'bold'))
    lbl2.after(60000, lbl2.destroy)
    lbl1 = Label(self)
    lbl1.grid(row=4,columnspan=3,padx=8, pady=8)
    lbl1.config(height=1, font=('times', 20, 'bold'))
    lbl1.config(bg='yellow')

    for k in range(60, 0, -1):
        lbl1["text"] = k
        self.update()
        time.sleep(1)
    lbl1.config(bg='red')
    lbl1.config(fg='white')
    lbl1["text"] = "Time's up!"


self = tkinter.Tk()
self.title("Authencation Register")


passcode = Label (self, text="Passcode")
passcode.grid(row=1, column=0, padx=8, pady=8, sticky="NSNESWSE")

passcode_entry = Entry (self)
passcode_entry.grid(row=1, column=1, padx=8, pady=8, sticky="NSNESWSE")

button = Button (self, text="Generate QRCode", command=lambda:qrcode())
button.grid(row=2, columnspan=3,padx=8, pady=8, sticky="NSNESWSE")

def qrcode():
    key="V7WZN7PYDPBOUJ3J"
    totp = pyotp.TOTP(key)
    pcode=totp.now()
    print (pcode)
    passcode= str(passcode_entry.get())
    print (passcode)
    print (pcode)
    if passcode == pcode:
        qr_code()
        countDown()
    else:
        messagebox.showinfo("Invaild", "Incorrect passcode, please try again!")

def qr_code():
    key = pyotp.random_base32()

    totp = pyotp.TOTP(key)
    print("Current OTP:", totp.now())

    key = "PL3VPSAOQ3AROS43" 
    link = pyotp.totp.TOTP(key).provisioning_uri("ISYS565", issuer_name="P2P Software")
    code = pyqrcode.create(link)
    print (code)
    code_xbm = code.xbm(scale=5)

    code_bmp = tkinter.BitmapImage(data=code_xbm)
    print(code_bmp)
    code_bmp.config(foreground="black")
    code_bmp.config(background="white")
    label = Label(self,image=code_bmp)
    print(label)
    label.grid(row=5,columnspan=3)
    label.after(60000, label.destroy)

self.mainloop()






