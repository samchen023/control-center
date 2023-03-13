import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter.tix import WINDOW
from tkinter import *
import tkinter.font as tkFont
import webbrowser
import requests

APP_VERSION = "v1.1.0"


def on_submit():
    p = subprocess.Popen(
        "ssid.cmd",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="gb2312",
    )
    output = p.communicate()[0]
    text_field.config(state="normal")
    text_field.delete(1.0, tk.END)
    if output.strip() == "None":
        text_field.insert(tk.END, "Disconnected")
    else:
        text_field.insert(tk.END, output)
    text_field.config(state="disabled")


def refreshtext():
    refresh_label.config(text="Refreshed", fg="green")
    root.after(2500, hide_refresh_label)


def refreshwifi():
    refreshtext()
    on_submit()


def run_speedtest():
    output = subprocess.run(["python", "speed.py"], capture_output=True, text=True)
    text.insert(tk.END, output.stdout)


def callback(url):
    webbrowser.open_new(url)


def createinfoWindow():
    newWindow = tk.Toplevel(root)
    newWindow.geometry("400x200")
    newWindow.title("Info")
    label = ttk.Label(newWindow, text="Made by Samchen023")
    label.pack(side="top")
    version_label = ttk.Label(newWindow, text=f"App Version: {APP_VERSION}")
    version_label.pack()
    link1 = Label(newWindow, text="Github", fg="blue", cursor="hand2")
    link1.pack()
    link1.bind(
        "<Button-1>", lambda e: callback("https://github.com/samchen023/control-center")
    )


def createupdateWindow():
    repo_owner = "samchen023"
    repo_name = "control-center"

    response = requests.get(
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases?per_page=1"
    )
    if response.status_code == 200:
        try:
            release_data = response.json()[0]
            latest_release_tag_name = release_data["name"]
            if latest_release_tag_name == APP_VERSION:
                message = f"You are running version {APP_VERSION}."
                show_button = False
            elif latest_release_tag_name < APP_VERSION:
                message = f"You are running a beta version {APP_VERSION}."
                show_button = False
            else:
                message = f"A new version ({latest_release_tag_name}) is available. You are running version {APP_VERSION}."
                show_button = True
        except (KeyError, IndexError):
            message = "Failed to retrieve release data from GitHub"
            show_button = False
    else:
        message = "Failed to retrieve release data from GitHub"
        show_button = False

    newWindow = tk.Toplevel(root)
    newWindow.geometry("400x100")
    newWindow.title(f"UPDATE")
    label = ttk.Label(newWindow, text=message)
    label.pack(padx=10, pady=10)
    if show_button:
        button = ttk.Button(
            newWindow,
            text="UPDATE",
            command=lambda: webbrowser.open(release_data["html_url"]),
        )
        button.pack(padx=10, pady=10)
    close_button = ttk.Button(newWindow, text="Close", command=newWindow.destroy)
    close_button.pack(padx=10, pady=10)


def hide_refresh_label():
    refresh_label.config(text="")


root = tk.Tk()
root.title("program")
root.geometry("550x350")


menu = tk.Menu(root)


root.config(menu=menu)

submenu1 = tk.Menu(activebackground="gray", tearoff=0)
menu.add_cascade(label="file", menu=submenu1)


submenu1.add_command(label="INFO", command=createinfoWindow)
submenu1.add_command(label="EXIT", command=root.destroy)

submenu2 = tk.Menu(tearoff=0)
menu.add_cascade(label="help", menu=submenu2)
submenu2.add_command(label="Update", command=createupdateWindow)

label = ttk.Label(root, text="Connected WIFI:")
label.pack(side="top", pady=5)


text_field = tk.Text(root)
text_field.pack(side="top")
text_field.config(font=("Microsoft JhengHei UI", 14), width=50, height=5)
text_field.config(state="disabled")
text_field.config(width=50, height=5)

refresh_button = ttk.Button(root, text="Refresh WIFI", command=refreshwifi)
refresh_button.pack(side="top", padx=10, pady=5)

refresh_label = tk.Label(root, text="", font=("Microsoft JhengHei UI", 10))
refresh_label.pack(side="top")

label = ttk.Label(root, text="Speedtest")
label.pack(side="top", pady=5)

text = tk.Text(root)
text.pack(side="left")
text.config(width=50, height=5)


button = ttk.Button(root, text="Run Speedtest", command=run_speedtest)
button.pack(side="top", padx=10, pady=5)

refresh_label.config(text="", fg="green")

on_submit()
root.mainloop()
