import json
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import account_manager as accounts

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
CONFIG = ROOT / "config.json"

BG = "#10131c"
PANEL = "#1c2230"
PURPLE = "#7c3aed"
TEXT = "#ffffff"
MUTED = "#94a3b8"

def main():
    with CONFIG.open("r", encoding="utf-8") as file:
        config = json.load(file)

    app = tk.Tk()
    app.title("STARCORE")
    app.geometry("900x560")
    app.minsize(750, 480)
    app.configure(bg=BG)

    def clear():
        for widget in app.winfo_children():
            widget.destroy()

    def make_entry(parent, placeholder="", password=False):
        entry = tk.Entry(
            parent,
            font=("Arial", 12),
            bg="#293247",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            show="*" if password else "",
        )
        entry.pack(fill="x", pady=8, ipady=10)
        return entry

    def header(subtitle):
        tk.Label(
            app, text="STARCORE",
            font=("Arial", 30, "bold"),
            fg="#a78bfa", bg=BG
        ).pack(pady=(35, 5))

        tk.Label(
            app, text=subtitle,
            font=("Arial", 10),
            fg=MUTED, bg=BG
        ).pack()

    def show_login():
        clear()
        header("MINECRAFT JAVA LAUNCHER")

        panel = tk.Frame(app, bg=PANEL, padx=35, pady=25)
        panel.pack(pady=35, padx=180, fill="x")

        tk.Label(
            panel, text="Login to STARCORE",
            font=("Arial", 17, "bold"),
            fg=TEXT, bg=PANEL
        ).pack(pady=(0, 15))

        username = make_entry(panel, "Username")
        password = make_entry(panel, "Password", True)
        status = tk.Label(panel, text="", fg="#f87171", bg=PANEL)
        status.pack()

        def login():
            if accounts.verify_login(username.get(), password.get()):
                show_home(username.get().strip())
            else:
                status.config(text="Incorrect username or password.")

        tk.Button(
            panel, text="LOGIN",
            command=login,
            font=("Arial", 12, "bold"),
            bg=PURPLE, fg=TEXT,
            relief="flat", pady=12
        ).pack(fill="x", pady=12)

        tk.Button(
            panel, text="Create an account",
            command=show_register,
            font=("Arial", 10),
            bg=PANEL, fg="#c4b5fd",
            relief="flat"
        ).pack()

        username.focus_set()

    def show_register():
        clear()
        header("CREATE YOUR STARCORE ACCOUNT")

        panel = tk.Frame(app, bg=PANEL, padx=35, pady=22)
        panel.pack(pady=25, padx=180, fill="x")

        tk.Label(
            panel, text="Register",
            font=("Arial", 17, "bold"),
            fg=TEXT, bg=PANEL
        ).pack(pady=(0, 10))

        username = make_entry(panel, "Username")
        password = make_entry(panel, "Password", True)
        confirm = make_entry(panel, "Confirm password", True)
        status = tk.Label(panel, text="", fg="#f87171", bg=PANEL)
        status.pack()

        def register():
            if password.get() != confirm.get():
                status.config(text="Passwords do not match.")
                return

            try:
                accounts.create_account(username.get(), password.get())
                messagebox.showinfo(
                    "STARCORE",
                    "Account created successfully. Please log in."
                )
                show_login()
            except ValueError as error:
                status.config(text=str(error))

        tk.Button(
            panel, text="CREATE ACCOUNT",
            command=register,
            font=("Arial", 12, "bold"),
            bg=PURPLE, fg=TEXT,
            relief="flat", pady=12
        ).pack(fill="x", pady=10)

        tk.Button(
            panel, text="Back to login",
            command=show_login,
            font=("Arial", 10),
            bg=PANEL, fg="#c4b5fd",
            relief="flat"
        ).pack()

        username.focus_set()

    def show_home(username):
        clear()
        header("MINECRAFT JAVA LAUNCHER")

        panel = tk.Frame(app, bg=PANEL, padx=25, pady=25)
        panel.pack(pady=30, padx=50, fill="x")

        tk.Label(
            panel, text=f"Welcome, {username}",
            font=("Arial", 16, "bold"),
            fg=TEXT, bg=PANEL
        ).pack(anchor="w")

        tk.Label(
            panel, text=f'Minecraft Version: {config["minecraft"]}',
            font=("Arial", 12),
            fg="#cbd5e1", bg=PANEL
        ).pack(anchor="w", pady=12)

        tk.Label(
            panel, text="Platform: Windows x64",
            font=("Arial", 11),
            fg=MUTED, bg=PANEL
        ).pack(anchor="w")

        buttons = tk.Frame(app, bg=BG)
        buttons.pack(pady=10)

        for label in ["Versions", "Settings", "Mods"]:
            tk.Button(
                buttons, text=label,
                font=("Arial", 11, "bold"),
                bg="#293247", fg=TEXT,
                relief="flat", width=14, pady=12
            ).pack(side="left", padx=8)

        tk.Button(
            app, text="LAUNCH GAME",
            font=("Arial", 14, "bold"),
            bg=PURPLE, fg=TEXT,
            relief="flat", width=25, pady=14
        ).pack(pady=20)

        tk.Button(
            app, text="LOG OUT",
            command=show_login,
            font=("Arial", 10, "bold"),
            bg="#293247", fg=TEXT,
            relief="flat", width=15, pady=8
        ).pack()

        tk.Label(
            app, text="STARCORE | Experimental Build",
            font=("Arial", 9),
            fg="#64748b", bg=BG
        ).pack(side="bottom", pady=12)

    show_login()
    app.mainloop()

if __name__ == "__main__":
    main()
