import os
import subprocess
import uuid
import tkinter as tk
from tkinter import filedialog, messagebox

DEFAULT_VLC_COMMAND = ["vlc"]

class PVGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PV Broadcaster")
        self.geometry("400x280")
        self.stream_path = tk.StringVar()
        self.token = tk.StringVar(value=self._generate_token())
        self.vlc_proc = None
        self._create_widgets()

    def _create_widgets(self):
        tk.Label(self, text="PV Streaming UI", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self, text="Select video file", command=self._select_file).pack(pady=5)
        tk.Label(self, textvariable=self.stream_path).pack(pady=5)
        tk.Button(self, text="Generate new token", command=self._refresh_token).pack(pady=5)
        tk.Entry(self, textvariable=self.token, width=30).pack(pady=5)
        tk.Button(self, text="Start stream", command=self._start_stream).pack(pady=5)
        tk.Button(self, text="Stop stream", command=self._stop_stream).pack(pady=5)

    def _select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.stream_path.set(path)

    def _refresh_token(self):
        self.token.set(self._generate_token())

    def _generate_token(self):
        return uuid.uuid4().hex[:8]

    def _start_stream(self):
        if not self.stream_path.get():
            messagebox.showwarning("Missing file", "Please select a video file to stream.")
            return
        cmd = DEFAULT_VLC_COMMAND + [
            self.stream_path.get(),
            "--sout",
            "#duplicate{dst=display,dst=std{access=http,mux=ts,dst=:8080}}",
        ]
        try:
            self.vlc_proc = subprocess.Popen(cmd)
            messagebox.showinfo("Streaming", f"Stream started on http://localhost:8080\nToken: {self.token.get()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _stop_stream(self):
        if self.vlc_proc:
            self.vlc_proc.terminate()
            self.vlc_proc = None
            messagebox.showinfo("Stopped", "Streaming stopped")

if __name__ == "__main__":
    app = PVGUI()
    app.mainloop()
