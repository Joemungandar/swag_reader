# Quelle: https://stackoverflow.com/questions/4443786/how-do-i-create-a-date-picker-in-tkinter

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry

def calendar_big():
    def print_sel():
        print(cal.selection_get())
    top = tk.Toplevel(root)
    cal = Calendar(top,
                   font="Arial 14", selectmode='day',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()

def calendar_small():
    top = tk.Toplevel(root)

    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    s = ttk.Style(root)
    s.theme_use('clam')
    ttk.Button(root, text='Großer Kalendar', command=calendar_big).pack(padx=10, pady=10)
    ttk.Button(root, text='Kleiner Kalendar', command=calendar_small).pack(padx=10, pady=10)
    root.mainloop()