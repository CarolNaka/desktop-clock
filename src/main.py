import tkinter as tk
from clock import Clock
from panel import Panel

# Initial settings
settings = {
    "background_color": "#1a1a2e",
    "text_color": "#e0e0e0",
    "font_family": "Consolas",
    "font_size": 72,
    "show_seconds": True,
    "time_format": "24h",
}

window = tk.Tk()
window.title("NeoClock")
window.configure(bg=settings["background_color"])
window.resizable(True, True)
window.geometry("700x200")

# Settings panel (left)
panel_frame = tk.Frame(window, bg="#2a2a3e", width=220)
panel_frame.pack(side="left", fill="y")
panel_frame.pack_propagate(False)

# Clock area (right)
clock_frame = tk.Frame(window, bg=settings["background_color"])
clock_frame.pack(side="left", fill="both", expand=True)

# Components
clock = Clock(clock_frame, settings)
clock.place(relx=0.5, rely=0.5, anchor="center")

panel = Panel(panel_frame, settings, clock)
panel.pack(fill="both", expand=True)

window.mainloop()