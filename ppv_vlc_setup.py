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
VLC_STATUS_URL = "https://update.videolan.org/vlc/status-win-x64"


def get_latest_vlc_info():
    """Return the latest VLC version and download URL."""
    try:
        with urllib.request.urlopen(VLC_STATUS_URL) as response:
            lines = response.read().decode().splitlines()
            return lines[0].strip(), lines[1].strip()
    except Exception:
        return None, None


def get_installed_vlc_version(path):
    """Return the version string of the VLC executable at *path*."""
    try:
        output = subprocess.check_output(
            [path, "--version"], stderr=subprocess.STDOUT, text=True, timeout=5
        )
        first_line = output.splitlines()[0]
        for token in first_line.split():
            if token[0].isdigit():
                return token
    except Exception:
        pass
    return None

class PPVviaVLCSetup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PPVviaVLC Setup")
        self.vlc_path = tk.StringVar()
        self.create_widgets()
        # Automatically ensure VLC is installed and up to date on launch
        self.ensure_vlc()

    def create_widgets(self):
        tk.Label(self, text="PPVviaVLC Setup").pack(pady=10)
        tk.Button(self, text="I already have VLC installed", command=self.find_vlc).pack(pady=5)
        tk.Button(self, text="Install/Update VLC", command=self.ensure_vlc).pack(pady=5)
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

    def download_vlc(self, url=None):
        if url is None:
            _, url = get_latest_vlc_info()
        installer_path = os.path.join(os.getcwd(), "vlc_installer.exe")
        try:
            messagebox.showinfo("Download", "Downloading VLC installer...")
            urllib.request.urlretrieve(url, installer_path)
            messagebox.showinfo("Download complete", f"Installer saved to {installer_path}\nRunning installer...")
            subprocess.Popen([installer_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download VLC: {e}")
        self.find_vlc()

    def ensure_vlc(self):
        """Install VLC if missing or update if an older version is installed."""
        self.find_vlc()
        path = self.vlc_path.get().replace("Found VLC at ", "").replace("Using VLC at ", "")
        latest_ver, url = get_latest_vlc_info()
        if not latest_ver:
            messagebox.showwarning("VLC", "Could not determine latest VLC version.")
            return

        if not path or not os.path.exists(path):
            if messagebox.askyesno("Install VLC", f"VLC {latest_ver} is not installed. Install now?"):
                self.download_vlc(url)
            return

        installed_ver = get_installed_vlc_version(path)
        if installed_ver and installed_ver != latest_ver:
            if messagebox.askyesno("Update VLC", f"Update VLC from {installed_ver} to {latest_ver}?"):
                self.download_vlc(url)
        else:
            messagebox.showinfo("VLC", "VLC is up to date.")

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
