import json
import sys
import tkinter as tk
from pathlib import Path

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
CONFIG = ROOT / "config.json"

def main():
    with CONFIG.open("r", encoding="utf-8") as file:
        config = json.load(file)

    app = tk.Tk()
    app.title(config["name"])
    app.geometry("900x560")
    app.minsize(750, 480)
    app.configure(bg="#10131c")

    title = tk.Label(
        app,
        text="STARCORE",
        font=("Arial", 30, "bold"),
        fg="#a78bfa",
        bg="#10131c"
    )
    title.pack(pady=(30, 5))

    subtitle = tk.Label(
        app,
        text="MINECRAFT JAVA LAUNCHER",
        font=("Arial", 10),
        fg="#94a3b8",
        bg="#10131c"
    )
    subtitle.pack()

    panel = tk.Frame(app, bg="#1c2230", padx=25, pady=25)
    panel.pack(pady=35, padx=50, fill="x")

    tk.Label(
        panel,
        text="Game Configuration",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#1c2230"
    ).pack(anchor="w")

    tk.Label(
        panel,
        text=f'Minecraft Version: {config["minecraft"]}',
        font=("Arial", 12),
        fg="#cbd5e1",
        bg="#1c2230"
    ).pack(anchor="w", pady=12)

    tk.Label(
        panel,
        text="Platform: Windows x64",
        font=("Arial", 11),
        fg="#94a3b8",
        bg="#1c2230"
    ).pack(anchor="w")

    buttons = tk.Frame(app, bg="#10131c")
    buttons.pack(pady=10)

    for label in ["Versions", "Settings", "Mods"]:
        tk.Button(
            buttons,
            text=label,
            font=("Arial", 11, "bold"),
            bg="#293247",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            width=14,
            pady=12
        ).pack(side="left", padx=8)

    tk.Button(
        app,
        text="LAUNCH GAME",
        font=("Arial", 14, "bold"),
        bg="#7c3aed",
        fg="white",
        activebackground="#6d28d9",
        activeforeground="white",
        relief="flat",
        width=25,
        pady=14
    ).pack(pady=25)

    tk.Label(
        app,
        text="STARCORE | Experimental Build",
        font=("Arial", 9),
        fg="#64748b",
        bg="#10131c"
    ).pack(side="bottom", pady=15)

    app.mainloop()

if __name__ == "__main__":
    main()
