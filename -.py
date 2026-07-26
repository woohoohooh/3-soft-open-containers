import tkinter as tk
from tkinter import ttk
from pathlib import Path
import ctypes

# ==========================================
# ФАЙЛЫ
# ==========================================
ACCESS_FILE = "access.txt"

# ==========================================
# ССЫЛКИ (добавляй свои)
# ==========================================
LINKS = {
    "aistudio": "http://aistudio.google.com/"

    # "flowmusic": "https://accounts.google.com/v3/signin/identifier?opparams=%253Fredirect_to%253Dhttps%25253A%25252F%25252Fwww.flowmusic.app%25252Fauth%25253Flogin%25253Dtrue%252526redirectUrl%25253Dhttps%2525253A%2525252F%2525252Fwww.flowmusic.app&dsh=S1075829360%3A1784721197998627&access_type=offline&client_id=1032626174130-533micbc9tgsei76mqhtguq07lpoe4je.apps.googleusercontent.com&o2v=2&prompt=consent&redirect_uri=https%3A%2F%2Fsb.flowmusic.app%2Fauth%2Fv1%2Fcallback&response_type=code&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fsubscriptions.thirdparty.googleone.eligibility&service=lso&state=583ca0c4-354c-448b-8884-3be9b4bd9e8f&flowName=GeneralOAuthFlow&continue=https%3A%2F%2Faccounts.google.com%2Fsignin%2Foauth%2Fconsent%3Fauthuser%3Dunknown%26part%3DAJi8hAM0_WoU2U6K__P8c-X0iuaIIXSnsbO_nPQuOxqWBCSFc0HMpJeC9lBxjcLb1_zCU_Oyo-kdY09CKEeocpahuGM9zhFh6XwRembE42vZeqwfnbEHAgh0pS03ftDFgr_zitD9VaHt3E1WRVvlA3KwbKadhRbO_2gSG90Ob7H-mosUCC4b_AueuH9wyHtI0e-qGKjsCK4o7BdffiJEGm8CgN4ZRTsVMOp9g0WFB6IuaN8jjTtraaj72GmLKqW9Axwrv5WyQsBfHl62rymvn5o1HGA6UXm8JPw7dP4wIuI_n_uN1hZuF_rQ5nd5QPytId_e8TMWW05N08o_alZMptZ9scDA45kEetj8tIZpqK07yBSqFUBm4P5LVjoRhOp9GlIkaXpEaoKkn4AZbyPViMmC4uRmGCaJ3GtmHruOLwLYSCBzLZZcubN-YmjRvk1RfP1IIvSJcOYWaXOAjJ6WDdnngy35mlzJ7AYeD9_RBVve05XDaWL9qjQ%26flowName%3DGeneralOAuthFlow%26as%3DS1075829360%253A1784721197998627%26client_id%3D1032626174130-533micbc9tgsei76mqhtguq07lpoe4je.apps.googleusercontent.com%26requestPath%3D%252Fsignin%252Foauth%252Fconsent%23&app_domain=https%3A%2F%2Fsb.flowmusic.app&rart=ANgoxccweQq-UUawR_qZyAbtQsrsMETkIiDGXvNp8R4-CpXMyIQHRQ5DvMrlAZaS-kp31C3623bXqmXtnEWYRwo1eLbbwPPqVx6Jz9i6yp-2v0fq4fqvtV8"
}

if not Path(ACCESS_FILE).exists():
    raise FileNotFoundError(ACCESS_FILE)

with open(ACCESS_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f]

accounts = []

i = 0

while i < len(lines):
    while i < len(lines) and lines[i] == "":
        i += 1

    if i >= len(lines):
        break

    email = lines[i]
    i += 1

    while i < len(lines) and lines[i] == "":
        i += 1

    if i >= len(lines):
        raise Exception(f"Нет пароля для {email}")

    password = lines[i]
    i += 1

    accounts.append({
        "email": email,
        "password": password
    })

if not accounts:
    raise Exception("access.txt пуст")

index = 0

# ==========================================
# ФУНКЦИИ
# ==========================================
def copy(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


def copy_email():
    copy(accounts[index]["email"])
    status.config(text=f"Email copied ({index+1}/{len(accounts)})")

def copy_pass():
    copy(accounts[index]["password"])
    status.config(text=f"Password copied ({index+1}/{len(accounts)})")

def next_account():
    global index

    index = (index + 1) % len(accounts)

    email_label.config(text=accounts[index]["email"])
    pass_label.config(text=accounts[index]["password"])

    status.config(text=f"Current account: {index+1}/{len(accounts)}")




def enter(e):
    e.widget.config(bg="#3B82F6")


def leave(e):
    e.widget.config(bg="#2563EB")


def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))


def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)


# ==========================================
# ОКНО
# ==========================================
root = tk.Tk()
root.title("Email Copier")
root.geometry("700x520")
root.state("zoomed")
root.configure(bg="#111827")
root.minsize(500, 350)

# Темный title bar (Windows 10/11)
try:
    root.update()

    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

    value = ctypes.c_int(1)

    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        hwnd,
        DWMWA_USE_IMMERSIVE_DARK_MODE,
        ctypes.byref(value),
        ctypes.sizeof(value),
    )
except:
    pass

# ==========================================
# СТИЛЬ
# ==========================================
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground="#1F2937",
    background="#1F2937",
    foreground="white",
    arrowcolor="white",
)

# ==========================================
# TITLE
# ==========================================
title = tk.Label(
    root,
    text="EMAIL COPIER",
    bg="#111827",
    fg="white",
    font=("Segoe UI Semibold", 28),
)
title.pack(pady=(30, 25))


# ==========================================
# BUTTON FACTORY
# ==========================================
def make_button(text, cmd):
    b = tk.Button(
        root,
        text=text,
        command=cmd,
        bg="#2563EB",
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI Semibold", 18),
        padx=30,
        pady=15,
    )

    b.pack(pady=10)

    b.bind("<Enter>", enter)
    b.bind("<Leave>", leave)

    return b


make_button("EMAIL", copy_email)

email_label = tk.Label(
    root,
    text=accounts[index]["email"],
    bg="#111827",
    fg="white",
    font=("Consolas", 11),
)

email_label.pack(pady=(0, 12))

def link_clicked(event):
    selection = links_list.curselection()

    if not selection:
        return

    name = links_list.get(selection[0])

    copy(LINKS[name])

    status.config(text=f"Copied: {name}")


links_list = tk.Listbox(
    root,
    bg="#1F2937",
    fg="white",
    selectbackground="#2563EB",
    selectforeground="white",
    relief="flat",
    bd=0,
    highlightthickness=0,
    font=("Segoe UI", 12),
    height=min(len(LINKS), 8),
    width=55,
    activestyle="none",
)

for name in LINKS:
    links_list.insert(tk.END, name)

links_list.pack(pady=20)

links_list.bind("<ButtonRelease-1>", link_clicked)

make_button("PASS", copy_pass)

pass_label = tk.Label(
    root,
    text=accounts[index]["password"],
    bg="#111827",
    fg="white",
    font=("Consolas", 11),
)

pass_label.pack(pady=(0, 18))

# ==========================================
# COMBOBOX
# ==========================================


# ==========================================
# NEXT
# ==========================================
make_button("NEXT", next_account)

# ==========================================
# STATUS
# ==========================================
status = tk.Label(
    root,
    text=f"Current account: 1/{len(accounts)}",
    bg="#111827",
    fg="#9CA3AF",
    font=("Segoe UI", 12),
)

status.pack(pady=25)

# ==========================================
# HOTKEYS
# ==========================================
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)

root.mainloop()