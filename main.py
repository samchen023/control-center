import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter.tix import WINDOW
from tkinter import *
import tkinter.font as tkFont
import webbrowser
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.request
import io
from PIL import Image, ImageTk

APP_VERSION = "v1.2.0"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="",
        client_secret="",
        redirect_uri="http://localhost:8888/callback",
        scope="user-read-playback-state",
    )
)


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


def update_current_track():
    current_track = sp.current_playback()
    if current_track is not None and "item" in current_track:
        track_name = current_track["item"]["name"]
        track_label.config(text="Currently Playing: " + track_name)
        image_url = current_track["item"]["album"]["images"][0]["url"]
        with urllib.request.urlopen(image_url) as url:
            image_data = url.read()
        image = Image.open(io.BytesIO(image_data))
        # Resize the image to 100x100 pixels
        image = image.resize((100, 100), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)
        image_label.config(image=photo_image)
        image_label.image = photo_image  # keep a reference to avoid garbage collection
    else:
        track_label.config(text="No music is currently playing.")
        image_label.config(image=None)
    root.after(1000, update_current_track)


def createspotifyWindow():
    # Create GUI window
    spotify = tk.Toplevel()
    spotify.title("OAuth2 Client Credentials")

    client_id_label = tk.Label(spotify, text="Client ID:")
    client_id_label.grid(row=0, column=0)
    client_id_entry = tk.Entry(spotify)
    client_id_entry.grid(row=0, column=1)

    client_secret_label = tk.Label(spotify, text="Client Secret:")
    client_secret_label.grid(row=1, column=0)
    client_secret_entry = tk.Entry(spotify, show="*")
    client_secret_entry.grid(row=1, column=1)

    submit_button = tk.Button(spotify, text="Submit", command=submit)
    submit_button.grid(row=2, column=1)

    output_label = tk.Label(spotify)
    output_label.grid(row=3, column=0, columnspan=2)

    def submit():
        # Get values from entry fields
        client_id = client_id_entry.get()
        client_secret = client_secret_entry.get()


root = tk.Tk()
root.title("program")
root.geometry("1000x450")


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

speedtest_frame = Frame(root)
speedtest_frame.pack(side="left")
speedtest_frame.config(height=10)

text = tk.Text(speedtest_frame)
text.grid(row=0, column=0, padx=10, pady=10)
text.config(width=50, height=5)

button = ttk.Button(speedtest_frame, text="Run Speedtest", command=run_speedtest)
button.grid(row=0, column=1, padx=10, pady=10)

refresh_label.config(text="", fg="green")


music_frame = Frame(root)
music_frame.pack(padx=20, pady=20)
music_frame.config(bg="#182329", width=50)

spotify_label = tk.Label(
    music_frame, font=("microsoft yahei", 16), fg="#1DB954", text="Spotify"
)
spotify_label.pack()
spotify_label.config(bg="#182329")

track_label = tk.Label(music_frame, font=("microsoft yahei", 16), fg="#ffffff")
track_label.pack()
track_label.config(bg="#182329")

image_label = tk.Label(music_frame)
image_label.pack()
image_label.config(bg="#182329")

on_submit()
root.after(1000, update_current_track)
root.mainloop()
