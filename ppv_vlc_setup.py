import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import urllib.request

VERSION = "0.1"
VLC_DEFAULT_PATHS = [
    r"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    r"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
]

class PPVviaVLCSetup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PPVviaVLC Setup")
        self.vlc_path = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="PPVviaVLC Setup").pack(pady=10)
        tk.Button(self, text="I already have VLC installed", command=self.find_vlc).pack(pady=5)
        tk.Button(self, text="Download and install VLC", command=self.download_vlc).pack(pady=5)
        tk.Button(self, text="Check for updates", command=self.check_updates).pack(pady=5)
        tk.Button(self, text="Quit", command=self.quit).pack(pady=5)
        tk.Label(self, textvariable=self.vlc_path).pack(pady=10)

    def find_vlc(self):
        for path in VLC_DEFAULT_PATHS:
            if os.path.exists(path):
                self.vlc_path.set(f"Found VLC at {path}")
                return
        messagebox.showinfo("VLC not found", "VLC executable not found in default locations. Please locate vlc.exe.")
        file_path = filedialog.askopenfilename(title="Locate vlc.exe", filetypes=[("VLC", "vlc.exe")])
        if file_path:
            self.vlc_path.set(f"Using VLC at {file_path}")
        else:
            self.vlc_path.set("VLC not selected")

    def download_vlc(self):
        url = "https://get.videolan.org/vlc/last/win64/vlc-3.0.18-win64.exe"
        installer_path = os.path.join(os.getcwd(), "vlc_installer.exe")
        try:
            messagebox.showinfo("Download", "Downloading VLC installer...")
            urllib.request.urlretrieve(url, installer_path)
            messagebox.showinfo("Download complete", f"Installer saved to {installer_path}\nRunning installer...")
            subprocess.Popen([installer_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download VLC: {e}")
        self.find_vlc()

    def check_updates(self):
        # stub for checking updates of this tool and VLC
        current_version = VERSION
        remote_url = "https://raw.githubusercontent.com/example/PPVviaVLC/main/VERSION"
        try:
            with urllib.request.urlopen(remote_url) as response:
                latest = response.read().decode().strip()
            if latest != current_version:
                messagebox.showinfo("Update Available", f"A new version {latest} is available. Current version: {current_version}")
            else:
                messagebox.showinfo("Up to date", "You are using the latest version.")
        except Exception:
            messagebox.showwarning("Update check failed", "Could not check for updates.")
        # check VLC version by running vlc --version if path set
        path = self.vlc_path.get().replace("Found VLC at ", "").replace("Using VLC at ", "")
        if path and os.path.exists(path):
            try:
                result = subprocess.check_output([path, "--version"], stderr=subprocess.STDOUT, text=True, timeout=5)
                version_line = result.splitlines()[0]
                messagebox.showinfo("VLC version", version_line)
            except Exception:
                pass

if __name__ == "__main__":
    app = PPVviaVLCSetup()
    app.mainloop()
