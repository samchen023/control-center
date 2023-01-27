import tkinter as tk
import subprocess
from tkinter.tix import WINDOW
from tkinter import *


def on_submit():
    p = subprocess.Popen('ssid.cmd', shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, encoding='gb2312')
    output = p.communicate()[0]
    text_field.config(state="normal")
    text_field.delete(1.0, tk.END)
    text_field.insert(tk.END, output)
    text_field.config(state="disabled")


root = tk.Tk()
root.title("program")

menu = tk.Menu(root)


root.config(menu=menu)

submenu1 = tk.Menu(activebackground="gray", tearoff=0)
menu.add_cascade(label="menu1", menu=submenu1)

submenu1.add_command(label="refresh", )
submenu1.add_separator()
submenu1.add_command(label="exit", command=root.destroy)

submenu2 = tk.Menu(tearoff=0)
menu.add_cascade(label="menu2", menu=submenu2)

label = tk.Label(root, text="Connected WIFI:")
label.pack()

text_field = tk.Text(root)
text_field.pack()
text_field.config(state="disabled")

on_submit()
root.mainloop()
