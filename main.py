import tkinter as tk
import subprocess
from tkinter.tix import WINDOW
from tkinter import *
import tkinter.font as tkFont
import webbrowser
import requests

APP_VERSION = 'v0.0.1'


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


def callback(url):
    webbrowser.open_new(url)


def createNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.geometry("400x200")
    label = tk.Label(newWindow, text="Made by Samchen023")
    label.pack(side="top")
    link1 = Label(newWindow, text="Github",
                  fg="blue", cursor="hand2")
    link1.pack()
    link1.bind(
        "<Button-1>", lambda e: callback("https://github.com/samchen023/control-center"))


def createupdateWindow():
    repo_owner = "samchen023"
    repo_name = "control-center"

    response = requests.get(
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases?per_page=1")
    if response.status_code == 200:
        try:
            release_data = response.json()[0]
            latest_release_tag_name = release_data["name"]
            if latest_release_tag_name <= APP_VERSION:
                message = f"You are running version {APP_VERSION} of {repo_name}, which is up to date."
                show_button = False
            else:
                message = f"A new version of {repo_name} ({latest_release_tag_name}) is available. You are running version {APP_VERSION}."
                show_button = True
        except (KeyError, IndexError):
            message = "Failed to retrieve release data from GitHub"
            show_button = False
    else:
        message = "Failed to retrieve release data from GitHub"
        show_button = False

    newWindow = tk.Toplevel(root)
    newWindow.geometry("600x200")
    newWindow.title(f"UPDATE")
    label = tk.Label(newWindow, text=message)
    label.pack(padx=10, pady=10)
    if show_button:
        button = tk.Button(newWindow, text="UPDATE", command=lambda: webbrowser.open(
            release_data["html_url"]))
        button.pack(padx=10, pady=10)
    close_button = tk.Button(newWindow, text="Close",
                             command=newWindow.destroy)
    close_button.pack(padx=10, pady=10)


root = tk.Tk()
root.title("program")
root.geometry("550x300")


menu = tk.Menu(root)


root.config(menu=menu)

submenu1 = tk.Menu(activebackground="gray", tearoff=0)
menu.add_cascade(label="file", menu=submenu1)


submenu1.add_command(label="INFO", command=createNewWindow)
submenu1.add_command(label="EXIT", command=root.destroy)

submenu2 = tk.Menu(tearoff=0)
menu.add_cascade(label="help", menu=submenu2)
submenu2.add_command(label="Update", command=createupdateWindow)

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
