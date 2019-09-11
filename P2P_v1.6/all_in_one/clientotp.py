from tkinter import *
import tkinter
import pyotp
import pyqrcode
from tkinter import messagebox
import time
import os
from server import *
from client import *
def otp():
    def countDown():
        lbl2 = Label(text="Please scan the QR-Code within")
        lbl2.grid(row=3, columnspan=3,padx=8, pady=8, sticky="NSNESWSE")
        lbl2.config(height=1, font=('times', 20, 'bold'))
        lbl2.after(60000, lbl2.destroy)
        lbl1 = Label()
        lbl1.grid(row=4,columnspan=3,padx=8, pady=8)
        lbl1.config(height=1, font=('times', 20, 'bold'))
        lbl1.config(bg='yellow')
        
        for k in range(60, 0, -1):
            lbl1["text"] = k
            top1.update()
            time.sleep(1)
        lbl1.config(bg='red')
        lbl1.config(fg='white')
        lbl1["text"] = "Time's up!"


    def back():
        top1.withdraw()
        top1.deiconify()
        #s_software()
        
        
    top1 = toplevel()
    top1.title("Authencation Register")


    passcode = Label (top1, text="Passcode")
    passcode.grid(row=1, column=0, padx=8, pady=8, sticky="NSNESWSE")

    passcode_entry = Entry (top1)
    passcode_entry.grid(row=1, column=1, padx=8, pady=8, sticky="NSNESWSE")

    button = Button (top1, text="Generate QRCode", command=lambda:qrcode())
    button.grid(row=2, columnspan=3,padx=8, pady=8, sticky="NSNESWSE")

    returnbtn=Button(top1, text="Return to main page", command=lambda:back())
    returnbtn.grid(row=10, columnspan=3,padx=8, pady=8, sticky="NSNESWSE")
    #lbl1.grid(row=4, column=1 ,padx=8, pady=8, sticky="NSNESWSE")
    #lbl1 = Label(top1, text="123")
    #lbl1.grid(row=3, column=2,padx=8, pady=8, sticky="NSNESWSE")




    def qrcode():
        key="V7WZN7PYDPBOUJ3J"
        totp = pyotp.TOTP(key)
        pcode=totp.now()
        print (pcode)
        passcode= str(passcode_entry.get())
        print (passcode)
        print (pcode)
        if passcode == pcode:
            import clientQRcode
            countDown()
        else:
            messagebox.showinfo("Invaild", "Incorrect passcode, please try again!")




    top1.mainloop()
