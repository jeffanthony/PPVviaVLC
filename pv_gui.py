import os
import subprocess
import uuid
import tkinter as tk
from tkinter import filedialog, messagebox

DEFAULT_VLC_COMMAND = "vlc"

class PVGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PV Broadcaster")
        self.geometry("420x320")
        self.stream_path = tk.StringVar()
        self.token = tk.StringVar(value=self._generate_token())
        self.port = tk.StringVar(value="8080")
        self.vlc_path = tk.StringVar(value=DEFAULT_VLC_COMMAND)
        self.vlc_proc = None
        self._create_widgets()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self):
        tk.Label(self, text="PV Streaming UI", font=("Helvetica", 14)).pack(pady=10)

        tk.Button(self, text="Select video file", command=self._select_file).pack(pady=5)
        tk.Label(self, textvariable=self.stream_path).pack(pady=5)

        path_frame = tk.Frame(self)
        path_frame.pack(pady=5)
        tk.Label(path_frame, text="VLC path:").pack(side=tk.LEFT)
        tk.Entry(path_frame, textvariable=self.vlc_path, width=30).pack(side=tk.LEFT)
        tk.Button(path_frame, text="Browse", command=self._select_vlc).pack(side=tk.LEFT, padx=2)

        port_frame = tk.Frame(self)
        port_frame.pack(pady=5)
        tk.Label(port_frame, text="Port:").pack(side=tk.LEFT)
        tk.Entry(port_frame, textvariable=self.port, width=6).pack(side=tk.LEFT)

        token_frame = tk.Frame(self)
        token_frame.pack(pady=5)
        tk.Button(token_frame, text="New token", command=self._refresh_token).pack(side=tk.LEFT)
        tk.Entry(token_frame, textvariable=self.token, width=20, state="readonly").pack(side=tk.LEFT, padx=2)
        tk.Button(token_frame, text="Copy", command=self._copy_token).pack(side=tk.LEFT)

        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Start stream", command=self._start_stream).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Stop stream", command=self._stop_stream).pack(side=tk.LEFT, padx=5)

    def _select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.stream_path.set(path)

    def _select_vlc(self):
        path = filedialog.askopenfilename(title="Select VLC executable")
        if path:
            self.vlc_path.set(path)

    def _refresh_token(self):
        self.token.set(self._generate_token())

    def _copy_token(self):
        self.clipboard_clear()
        self.clipboard_append(self.token.get())

    def _generate_token(self):
        return uuid.uuid4().hex[:8]

    def _start_stream(self):
        if not self.stream_path.get():
            messagebox.showwarning("Missing file", "Please select a video file to stream.")
            return
        cmd = [self.vlc_path.get(), self.stream_path.get(), "--sout",
               f"#duplicate{{dst=display,dst=std{{access=http,mux=ts,dst=:{self.port.get()}}}}}"]
        try:
            self.vlc_proc = subprocess.Popen(cmd)
            messagebox.showinfo("Streaming", f"Stream started on http://localhost:{self.port.get()}\nToken: {self.token.get()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _stop_stream(self):
        if self.vlc_proc:
            self.vlc_proc.terminate()
            self.vlc_proc = None
            messagebox.showinfo("Stopped", "Streaming stopped")

    def _on_close(self):
        self._stop_stream()
        self.destroy()

if __name__ == "__main__":
    app = PVGUI()
    app.mainloop()
