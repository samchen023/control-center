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
    output = subprocess.run([r"path\to\speedtest.exe"],
                            capture_output=True, text=True)
    text.insert(tk.END, output.stdout)


root = tk.Tk()
root.title("program")
root.geometry("400x240")

menu = tk.Menu(root)


root.config(menu=menu)

submenu1 = tk.Menu(activebackground="gray", tearoff=0)
menu.add_cascade(label="file", menu=submenu1)

submenu1.add_command(label="exit", command=root.destroy)

submenu2 = tk.Menu(tearoff=0)
menu.add_cascade(label="menu2", menu=submenu2)

label = tk.Label(root, text="Connected WIFI:")
label.pack()

text_field = tk.Text(root)
text_field.pack()
text_field.config(font=("Microsoft JhengHei UI", 14))
text_field.config(state="disabled")

label = tk.Label(root, text="Speedtest")
label.pack()

text = tk.Text(root)
text.pack()

button = tk.Button(root, text="Run Speedtest", command=run_speedtest)
button.pack()

on_submit()
root.mainloop()
