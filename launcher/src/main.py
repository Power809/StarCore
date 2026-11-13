import json
import tkinter as tk
from tkinter import messagebox
import account_manager as accounts
from paths import CONFIG_PATH

BG = "#0b0b14"
PANEL = "#151525"
PANEL2 = "#202039"
PURPLE = "#8b5cf6"
LIGHT = "#c4b5fd"
WHITE = "#ffffff"
MUTED = "#9292aa"

def main():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = json.load(file)

    app = tk.Tk()
    app.title("STARCORE")
    app.geometry("1100x680")
    app.minsize(900, 580)
    app.configure(bg=BG)

    def clear():
        for widget in app.winfo_children():
            widget.destroy()

    def label(parent, text, size=11, color=WHITE, bold=False):
        return tk.Label(
            parent,
            text=text,
            font=("Arial", size, "bold" if bold else "normal"),
            fg=color,
            bg=parent.cget("bg")
        )

    def make_entry(parent, password=False):
        entry = tk.Entry(
            parent,
            font=("Arial", 12),
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            show="*" if password else ""
        )
        entry.pack(fill="x", pady=8, ipady=10)
        return entry

    def header(subtitle):
        label(app, "STARCORE", 30, LIGHT, True).pack(pady=(35, 5))
        label(app, subtitle, 10, MUTED).pack()

    def show_login():
        clear()
        header("MINECRAFT JAVA LAUNCHER")

        panel = tk.Frame(app, bg=PANEL, padx=35, pady=25)
        panel.pack(pady=35, padx=300, fill="x")

        label(panel, "LOGIN TO STARCORE", 17, WHITE, True).pack(pady=(0, 15))
        username = make_entry(panel)
        password = make_entry(panel, True)
        status = label(panel, "", 10, "#f87171")
        status.pack()

        def login():
            if accounts.verify_login(username.get(), password.get()):
                show_home(username.get().strip())
            else:
                status.config(text="Incorrect username or password.")

        tk.Button(
            panel, text="LOGIN", command=login,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Arial", 12, "bold"), pady=12
        ).pack(fill="x", pady=12)

        tk.Button(
            panel, text="CREATE AN ACCOUNT",
            command=show_register, bg=PANEL, fg=LIGHT,
            relief="flat"
        ).pack()

        username.focus_set()

    def show_register():
        clear()
        header("CREATE YOUR STARCORE ACCOUNT")

        panel = tk.Frame(app, bg=PANEL, padx=35, pady=22)
        panel.pack(pady=25, padx=300, fill="x")

        label(panel, "REGISTER", 17, WHITE, True).pack(pady=(0, 10))
        username = make_entry(panel)
        password = make_entry(panel, True)
        confirm = make_entry(panel, True)
        status = label(panel, "", 10, "#f87171")
        status.pack()

        def register():
            if password.get() != confirm.get():
                status.config(text="Passwords do not match.")
                return
            try:
                accounts.create_account(username.get(), password.get())
                messagebox.showinfo("STARCORE", "Account created successfully.")
                show_login()
            except ValueError as error:
                status.config(text=str(error))

        tk.Button(
            panel, text="CREATE ACCOUNT", command=register,
            bg=PURPLE, fg=WHITE, relief="flat",
            font=("Arial", 12, "bold"), pady=12
        ).pack(fill="x", pady=10)

        tk.Button(
            panel, text="BACK TO LOGIN", command=show_login,
            bg=PANEL, fg=LIGHT, relief="flat"
        ).pack()

    def show_home(username):
        clear()

        sidebar = tk.Frame(app, bg="#10101d", width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        label(sidebar, "STARCORE", 21, LIGHT, True).pack(pady=(28, 35))

        content = tk.Frame(app, bg=BG)
        content.pack(side="left", fill="both", expand=True)

        page_title = label(content, "HOME", 19, WHITE, True)
        page_title.pack(anchor="w", padx=28, pady=(25, 12))

        pages = {}

        def show_page(name):
            page_title.config(text=name.upper())
            for widget in pages["area"].winfo_children():
                widget.destroy()

            area = pages["area"]

            if name == "Home":
                hero = tk.Frame(area, bg="#241747", height=205)
                hero.pack(fill="x", pady=(0, 16))
                hero.pack_propagate(False)

                label(hero, "MINECRAFT", 28, WHITE, True).pack(anchor="w", padx=25, pady=(30, 5))
                label(hero, "THE WORLD AWAITS...", 12, LIGHT, True).pack(anchor="w", padx=27)
                label(hero, "Explore. Build. Survive.", 10, WHITE).pack(anchor="w", padx=27, pady=8)

                row = tk.Frame(area, bg=BG)
                row.pack(fill="x", pady=5)

                news = tk.Frame(row, bg=PANEL, padx=18, pady=15)
                news.pack(side="left", fill="both", expand=True, padx=(0, 8))
                label(news, "LATEST NEWS", 13, LIGHT, True).pack(anchor="w")
                label(news, "Welcome to STARCORE!", 11).pack(anchor="w", pady=12)
                label(news, "More updates coming soon.", 9, MUTED).pack(anchor="w")

                version = tk.Frame(row, bg=PANEL, padx=18, pady=15)
                version.pack(side="left", fill="both", expand=True, padx=(8, 0))
                label(version, "GAME VERSION", 13, LIGHT, True).pack(anchor="w")

                selected = tk.StringVar(value="1.20.1")
                tk.OptionMenu(version, selected, "1.20.1", "1.21.1", "1.19.2").pack(anchor="w", pady=12)

                def launch_notice():
                    messagebox.showinfo(
                        "STARCORE",
                        "Game launching is not available yet."
                    )

                tk.Button(
                    area, text="▶  LAUNCH GAME",
                    command=launch_notice,
                    bg=PURPLE, fg=WHITE,
                    font=("Arial", 14, "bold"),
                    relief="flat", pady=15
                ).pack(fill="x", pady=18)

                stats = tk.Frame(area, bg=BG)
                stats.pack(fill="x")

                for title, value in [
                    ("RUNTIME", "Java"),
                    ("MEMORY", "Auto"),
                    ("RESOLUTION", "Auto"),
                    ("PERFORMANCE", "Ready")
                ]:
                    card = tk.Frame(stats, bg=PANEL, padx=12, pady=12)
                    card.pack(side="left", fill="both", expand=True, padx=4)
                    label(card, title, 9, MUTED, True).pack(anchor="w")
                    label(card, value, 12, LIGHT, True).pack(anchor="w", pady=5)

            else:
                panel = tk.Frame(area, bg=PANEL, padx=25, pady=25)
                panel.pack(fill="x", pady=10)
                label(panel, name.upper(), 18, LIGHT, True).pack(anchor="w")
                label(panel, "This section is under development.", 11, MUTED).pack(anchor="w", pady=15)

                if name == "Account":
                    label(panel, "Username: " + username, 11).pack(anchor="w", pady=5)

                if name == "About":
                    label(panel, "STARCORE Launcher 0.1.0", 11).pack(anchor="w", pady=5)

        for name in ["Home", "Versions", "Mods", "Settings", "Account", "About"]:
            tk.Button(
                sidebar, text=name,
                command=lambda n=name: show_page(n),
                bg="#10101d", fg=WHITE,
                activebackground=PANEL2,
                activeforeground=LIGHT,
                relief="flat", anchor="w",
                font=("Arial", 11, "bold"),
                padx=22, pady=13
            ).pack(fill="x", padx=8, pady=2)

        tk.Button(
            sidebar, text="LOG OUT",
            command=show_login,
            bg=PANEL2, fg=LIGHT,
            relief="flat", pady=10
        ).pack(side="bottom", fill="x", padx=15, pady=20)

        pages["area"] = tk.Frame(content, bg=BG)
        pages["area"].pack(fill="both", expand=True, padx=28, pady=10)

        show_page("Home")

    show_login()
    app.mainloop()

if __name__ == "__main__":
    main()
