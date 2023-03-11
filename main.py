import tkinter as tk
import subprocess
from tkinter.tix import WINDOW
from tkinter import *
import tkinter.font as tkFont
import webbrowser
import requests

APP_VERSION = "v1.0.0"


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

    refresh_label.config(text="Text Refreshed", fg="green")
    root.after(2500, hide_refresh_label)


def run_speedtest():
    output = subprocess.run(["python", "speed.py"], capture_output=True, text=True)
    text.insert(tk.END, output.stdout)


def callback(url):
    webbrowser.open_new(url)


def createNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.geometry("400x200")
    newWindow.title("Info")
    label = tk.Label(newWindow, text="Made by Samchen023")
    label.pack(side="top")
    version_label = tk.Label(newWindow, text=f"App Version: {APP_VERSION}")
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
            if latest_release_tag_name <= APP_VERSION:
                message = f"You are running version {APP_VERSION}, which is up to date."
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
    label = tk.Label(newWindow, text=message)
    label.pack(padx=10, pady=10)
    if show_button:
        button = tk.Button(
            newWindow,
            text="UPDATE",
            command=lambda: webbrowser.open(release_data["html_url"]),
        )
        button.pack(padx=10, pady=10)
    close_button = tk.Button(newWindow, text="Close", command=newWindow.destroy)
    close_button.pack(padx=10, pady=10)


def hide_refresh_label():
    refresh_label.config(text="")


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
label.pack(side="top", pady=5)


text_field = tk.Text(root)
text_field.pack(side="top")
text_field.config(font=("Microsoft JhengHei UI", 14), width=50, height=5)
text_field.config(state="disabled")
text_field.config(width=50, height=5)

refresh_button = tk.Button(root, text="Refresh", command=on_submit)
refresh_button.pack(side="top", padx=10, pady=5)
refresh_label = tk.Label(root, text="", font=("Microsoft JhengHei UI", 10))
refresh_label.pack(side="top")

label = tk.Label(root, text="Speedtest")
label.pack(side="top", pady=5)

text = tk.Text(root)
text.pack(side="left")
text.config(width=50, height=5)


button = tk.Button(root, text="Run Speedtest", command=run_speedtest)
button.pack(side="top", padx=10, pady=5)

refresh_label.config(text="", fg="green")

on_submit()
root.mainloop()
