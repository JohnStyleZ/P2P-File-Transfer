# from tkinter import *
# import tkinter as tk

# root=tk.Tk()
# frame = tk.Frame(root, width=40, height=40) #their units in pixels
# # button1 = tk.Button(frame, text="btn")
# serverbtn=tk.Button(frame, text="Server", font=("Arial",30))

# frame.grid_propagate(False) #disables resizing of frame
# frame.columnconfigure(0, weight=1) #enables button to fill frame
# frame.rowconfigure(0,weight=1) #any positive number would do the trick

# frame.grid(row=1,column=4,padx=100,pady=100, sticky="NSNESWSE") #put frame where the button should be
# # button1.grid(sticky="wens") #makes the button expand

# #serverbtn=tk.Button(frame, text="Server", font=("Arial",30))
# serverbtn.grid(row=1,column=4,padx=100,pady=100, sticky="NSNESWSE")

# # clientbtn=tk.Button(frame, text="Client", font=("Arial",30))
# # clientbtn.grid(row=1, column=5,padx=1window.destroy()00,pady=100, sticky="NSNESWSE")
# root.mainloop()

from tkinter import *
from client import client
from server import s_software
window = Tk ()
window.title(" ")
#window.geometry('600x400')

label = Label (window, text="P2P Transfer", font=("Arial", 30))
label.grid(columnspan=4, row=0)

btn = Button(window, text ="Receive", font=("Arial",30), bg = "white", command=lambda:startserver())
btn.config(height = 5, width = 10)
btn.grid(column = 0, row = 1, padx=50, pady=30, sticky="NSNESWSE")

btn2 = Button(window, text = "Send", font=("Arial",30), bg = "white", command=lambda:startclient())
btn2.config(height = 5, width = 10)
btn2.grid(column = 1, row = 1, padx=50, pady=30,sticky="NSNESWSE")

# slabel = Label (window, text="     Server - to recieve file", font=("Arial", 10))
# slabel.grid(column=0, row=5)

# clabel = Label (window, text="Client - to send file", font=("Arial", 10))
# clabel.grid(column=0, row=6)

def startserver():
	s_software()

def startclient():
	client()



window.mainloop()