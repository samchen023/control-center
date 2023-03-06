import tkinter as tk
import subprocess
from tkinter.tix import WINDOW
from tkinter import *
import tkinter.font as tkFont


def on_submit():
    p = subprocess.Popen('ssid.cmd', shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, encoding='gb2312')
    output = p.communicate()[0]
    text_field.config(state="normal")
    text_field.delete(1.0, tk.END)
    if output.strip() == "None":
        text_field.insert(tk.END, "Disconnected")
    else:
        text_field.insert(tk.END, output)
    text_field.config(state="disabled")


def run_speedtest():
    output = subprocess.run(['python', 'speedtest.py'],
                            capture_output=True, text=True)
    text.insert(tk.END, output.stdout)


def createNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.geometry("400x200")
    label = tk.Label(newWindow, text="Connected WIFI:")


root = tk.Tk()
root.title("program")
root.geometry("550x300")


menu = tk.Menu(root)


root.config(menu=menu)

submenu1 = tk.Menu(activebackground="gray", tearoff=0)
menu.add_cascade(label="file", menu=submenu1)

submenu1.add_command(label="exit", command=root.destroy)
submenu1.add_command(label="info", command=createNewWindow)

submenu2 = tk.Menu(tearoff=0)
menu.add_cascade(label="menu2", menu=submenu2)

label = tk.Label(root, text="Connected WIFI:")
label.pack(side="top")


text_field = tk.Text(root)
text_field.pack(side="top")
text_field.config(font=("Microsoft JhengHei UI", 14))
text_field.config(state="disabled")
text_field.config(width=50, height=5)

label = tk.Label(root, text="Speedtest")
label.pack(side="left")

text = tk.Text(root)
text.pack(side="left")
text.config(width=50, height=5)


button = tk.Button(root, text="Run Speedtest", command=run_speedtest)
button.pack(side="left")

on_submit()
root.mainloop()
