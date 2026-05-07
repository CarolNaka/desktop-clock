import tkinter as tk
from tkinter import colorchooser

AVAILABLE_FONTS = [
    "Consolas",
    "Arial",
    "Courier New",
    "Segoe UI",
    "Verdana"
]


class Panel(tk.Frame):
    def __init__(self, master, settings, clock):
        super().__init__(master, bg="#2a2a3e", width=220)

        self.pack_propagate(False)

        self.settings = settings
        self.clock = clock

        tk.Label(
            self,
            text="Settings",
            bg="#2a2a3e",
            fg="white",
            font=("Consolas", 13, "bold")
        ).pack(pady=(20, 10))

        self._section("Colors")
        self._color_button("Background", "background_color")
        self._color_button("Text", "text_color")

        self._section("Font")
        self._font_dropdown()
        self._font_size_slider()

        self._section("Format")
        self._seconds_toggle()
        self._format_toggle()

    def _section(self, title):
        tk.Label(
            self,
            text=title.upper(),
            bg="#2a2a3e",
            fg="#888",
            font=("Consolas", 9)
        ).pack(anchor="w", padx=16, pady=(14, 2))

    def _color_button(self, label, key):
        frame = tk.Frame(self, bg="#2a2a3e")
        frame.pack(fill="x", padx=16, pady=3)

        tk.Label(
            frame,
            text=label,
            bg="#2a2a3e",
            fg="white",
            font=("Consolas", 10)
        ).pack(side="left")

        preview = tk.Label(frame, bg=self.settings[key], width=3)
        preview.pack(side="right")

        def choose_color():
            color = colorchooser.askcolor(color=self.settings[key])[1]

            if color:
                self.settings[key] = color
                preview.configure(bg=color)
                self.clock.apply_settings()

        preview.bind("<Button-1>", lambda e: choose_color())

    def _font_dropdown(self):
        frame = tk.Frame(self, bg="#2a2a3e")
        frame.pack(fill="x", padx=16, pady=3)

        tk.Label(
            frame,
            text="Font",
            bg="#2a2a3e",
            fg="white",
            font=("Consolas", 10)
        ).pack(side="left")

        var = tk.StringVar(value=self.settings["font_family"])

        menu = tk.OptionMenu(
            frame,
            var,
            *AVAILABLE_FONTS,
            command=lambda value: self._apply("font_family", value)
        )

        menu.configure(
            bg="#3a3a5e",
            fg="white",
            font=("Consolas", 9),
            highlightthickness=0
        )

        menu.pack(side="right")

    def _font_size_slider(self):
        frame = tk.Frame(self, bg="#2a2a3e")
        frame.pack(fill="x", padx=16, pady=3)

        tk.Label(
            frame,
            text="Size",
            bg="#2a2a3e",
            fg="white",
            font=("Consolas", 10)
        ).pack(anchor="w")

        slider = tk.Scale(
            frame,
            from_=24,
            to=120,
            orient="horizontal",
            bg="#2a2a3e",
            fg="white",
            highlightthickness=0,
            troughcolor="#3a3a5e",
            command=lambda value: self._apply("font_size", int(value))
        )

        slider.set(self.settings["font_size"])
        slider.pack(fill="x")

    def _seconds_toggle(self):
        var = tk.BooleanVar(value=self.settings["show_seconds"])

        def toggle():
            self.settings["show_seconds"] = var.get()

        tk.Checkbutton(
            self,
            text="Show seconds",
            variable=var,
            command=toggle,
            bg="#2a2a3e",
            fg="white",
            selectcolor="#3a3a5e",
            font=("Consolas", 10),
            activebackground="#2a2a3e",
            activeforeground="white"
        ).pack(anchor="w", padx=16, pady=3)

    def _format_toggle(self):
        var = tk.StringVar(value=self.settings["time_format"])

        frame = tk.Frame(self, bg="#2a2a3e")
        frame.pack(fill="x", padx=16, pady=3)

        tk.Label(
            frame,
            text="Format",
            bg="#2a2a3e",
            fg="white",
            font=("Consolas", 10)
        ).pack(anchor="w")

        for option in ["24h", "12h"]:
            tk.Radiobutton(
                frame,
                text=option,
                variable=var,
                value=option,
                command=lambda value=option: self._apply("time_format", value),
                bg="#2a2a3e",
                fg="white",
                selectcolor="#3a3a5e",
                activebackground="#2a2a3e",
                activeforeground="white",
                font=("Consolas", 10)
            ).pack(side="left", padx=4)

    def _apply(self, key, value):
        self.settings[key] = value
        self.clock.apply_settings()