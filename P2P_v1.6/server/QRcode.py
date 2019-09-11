

import tkinter
import pyqrcode
import pyotp
from tkinter import *


key = pyotp.random_base32()
print (key)
totp = pyotp.TOTP(key)
print("Current OTP:", totp.now())

key = "23BFEXOO3JXO3QY4" 
link = pyotp.totp.TOTP(key).provisioning_uri("Receiver", issuer_name="P2P Software")
code = pyqrcode.create(link)
print (code)
code_xbm = code.xbm(scale=5)

code_bmp = tkinter.BitmapImage(data=code_xbm)
print(code_bmp)
code_bmp.config(foreground="black")
code_bmp.config(background="white")
label = Label(image=code_bmp)
print(label)
label.grid(row=5,columnspan=3)
label.after(60000, label.destroy)


