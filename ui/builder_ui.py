import tkinter as tk
from tkinter import ttk
from data.classes import classes
from data.point_buy import POINT_POOL, point_cost, total_points_spent, remaining_points

import sv_ttk


def start_app():
    root = tk.Tk()
    root.title("Basic RPG Character Sheet Builder")
    root.maxsize(900, 600)
    root.geometry("900x600")
    root.resizable(False, False)

    header = ttk.Label(root, text="Character Sheet Builder")
    header.pack(pady=5)

    ttk.Label(root, text="Name:").pack(pady=10)
    name_input = ttk.Entry(root)
    name_input.pack()

    class_names = list(classes.keys())

    selected_class = tk.StringVar()

    class_header = ttk.Label(root, text="Select a class:")
    class_header.pack(pady=10)

    class_dropdown = ttk.Combobox(root, textvariable=selected_class, values=class_names, state="readonly")
    class_dropdown.current(0)
    class_dropdown.pack()

    abilities_text = "Scaling abilities: "
    abilities_label = ttk.Label(root, text=abilities_text, wraplength=400)
    abilities_label.pack(pady=10)

    description_text = "Description: "
    description_label = ttk.Label(root, text=description_text, wraplength=400)
    description_label.pack(pady=10)

    def show_class_info(event=None):
        cls = selected_class.get()
        info = classes.get(cls, {})
        desc = info.get("description", "No description.")
        scrs = info.get("abilities", "No abilities.")
        description_label.config(text=desc)
        abilities_label.config(text=abilities_text + " and ".join(scrs))

    class_dropdown.bind("<<ComboboxSelected>>", show_class_info)

    abl_title = ttk.Label(root, text="Abilities:")
    abl_title.pack(pady=20)

    ability_frame = tk.Frame(root)
    ability_frame.pack()
    
    ath_title = ttk.Label(ability_frame, text="Athletics (ATH)")
    brv_title = ttk.Label(ability_frame, text="Bravery (BRV)")
    wit_title = ttk.Label(ability_frame, text="Wit (WIT)")
    chm_title = ttk.Label(ability_frame, text="Charm (CHM)")

    ath_spin = ttk.Spinbox(ability_frame, width=5, from_=4, to=8, state="readonly")
    brv_spin = ttk.Spinbox(ability_frame, width=5, from_=4, to=8, state="readonly")
    wit_spin = ttk.Spinbox(ability_frame, width=5, from_=4, to=8, state="readonly")
    chm_spin = ttk.Spinbox(ability_frame, width=5, from_=4, to=8, state="readonly")

    ath_title.grid(row=0, column=0)
    ath_spin.grid(row=1, column=0)
    brv_title.grid(row=0, column=1)
    brv_spin.grid(row=1, column=1)
    wit_title.grid(row=0, column=2)
    wit_spin.grid(row=1, column=2)
    chm_title.grid(row=0, column=3)
    chm_spin.grid(row=1, column=3)
    

    button = ttk.Button(root, text="Create")
    button.pack()

    sv_ttk.set_theme("dark")

    root.mainloop()