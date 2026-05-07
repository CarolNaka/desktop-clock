import tkinter as tk
from datetime import datetime


class Clock(tk.Frame):
    def __init__(self, master, settings):
        super().__init__(master, bg=settings["background_color"])
        self.settings = settings

        self.time_label = tk.Label(
            self,
            fg=settings["text_color"],
            bg=settings["background_color"]
        )
        self.time_label.pack(expand=True)

        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        cfg = self.settings

        if cfg["time_format"] == "12h":
            fmt = "%I:%M %p" if not cfg["show_seconds"] else "%I:%M:%S %p"
        else:
            fmt = "%H:%M" if not cfg["show_seconds"] else "%H:%M:%S"

        self.time_label.config(
            text=now.strftime(fmt),
            font=(cfg["font_family"], cfg["font_size"], "bold")
        )

        self.after(1000, self.update_clock)

    def apply_settings(self):
        cfg = self.settings

        self.configure(bg=cfg["background_color"])

        self.time_label.configure(
            fg=cfg["text_color"],
            bg=cfg["background_color"]
        )