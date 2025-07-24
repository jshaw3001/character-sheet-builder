import tkinter as tk
from tkinter import ttk
from data.classes import classes
from data.point_buy import POINT_POOL, point_cost, total_points_spent, remaining_points, ABILITY_NAMES

import sv_ttk


class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()

        #main setup
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        sv_ttk.set_theme("dark")

        #widgets
        self.header = Header(self, title)
        self.name = Name(self)
        self.class_selector = ClassSelect(self)
        self.ability_title = AbilityTitle(self)
        self.ability_points = Abilities(self)

        #run
        self.mainloop()

class Header(ttk.Label):
    def __init__(self, master, text):
        super().__init__(master, text=text)
        self.pack(pady=5)

class Name(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(pady=5)

        self.create_widgets()
    
    def create_widgets(self):
        name_label = ttk.Label(self, text="Name:")
        name_input = ttk.Entry(self)
        name_label.pack(pady=5)
        name_input.pack()

class ClassSelect(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.class_names = list(classes.keys())
        self.selected_class = tk.StringVar()
        self.abilities_text = "Scaling abilities: "
        self.description_text = "Description: "
        self.pack(pady=5)

        self.create_widgets()

    
    def create_widgets(self):
        class_header = ttk.Label(self, text="Select a class:")
        class_header.pack(pady=10)

        class_dropdown = ttk.Combobox(self, textvariable=self.selected_class, values=self.class_names, state="readonly")
        class_dropdown.current(0)
        class_dropdown.pack()

        self.abilities_label = ttk.Label(self, text=self.abilities_text, wraplength=400)
        self.abilities_label.pack(pady=10)

        self.description_label = ttk.Label(self, text=self.description_text, wraplength=400)
        self.description_label.pack(pady=10)

        self.show_class_info()

        class_dropdown.bind("<<ComboboxSelected>>", self.show_class_info)

    def show_class_info(self, event=None):
        cls = self.selected_class.get()
        info = classes.get(cls, {})
        desc = info.get("description", "No description.")
        scrs = info.get("abilities", "No abilities.")
        self.description_label.config(text=desc)
        self.abilities_label.config(text=self.abilities_text + " and ".join(scrs))

class AbilityTitle(ttk.Label):
    def __init__(self, master):
        super().__init__(master, text="Abilities:")
        self.pack(pady=5)

class Abilities(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(pady=5)
        self.abilities = {name: tk.IntVar(value=4) for name in ABILITY_NAMES}
        self.spinners = {}
        self.cost_labels = {}
        self.points_remaining = tk.IntVar(value=POINT_POOL)

        for name, var in self.abilities.items():
            var.trace_add("write", lambda *args, n=name: self.validate_and_update(n))

        self.create_widgets()
        self.update_remaining_points()
        self.update_cost_labels()

    def create_widgets(self):
        for i, name in enumerate(ABILITY_NAMES):
            ttk.Label(self, text=name).grid(row=i, column=0, padx=10, pady=5)
            spin = ttk.Spinbox(
                self,
                from_=4,
                to=8,
                textvariable=self.abilities[name],
                width=5,
                state="readonly"
            )
            spin.grid(row=i, column=1)
            self.spinners[name] = spin

            cost_label = ttk.Label(self, text="")
            cost_label.grid(row=i, column=2, padx=10)
            self.cost_labels[name] = cost_label

            spin.bind("<Up>", lambda e, n=name: self.increment_ability(n), "break")
            spin.bind("<Down>", lambda e, n=name: self.decrement_ability(n), "break")
            spin.bind("<MouseWheel>", lambda e, n=name: self.increment_ability(n) if e.delta > 0 else self.decrement_ability(n), "break")

        self.remaining_label = ttk.Label(self, text=f"Points remaining: {self.points_remaining.get()}")
        self.remaining_label.grid(row=len(ABILITY_NAMES), column=1, pady=10)

    def update_cost_labels(self):
        for name, var in self.abilities.items():
            val = var.get()
            if val < 8:
                cost = point_cost(val + 1) - point_cost(val)
                self.cost_labels[name].config(text=f"Cost: {cost}")
            else:
                self.cost_labels[name].config(text="Max")

    def increment_ability(self, name):
        val = self.abilities[name].get()
        if val < 8:
            current_scores = {n: var.get() for n, var in self.abilities.items()}
            current_scores[name] = val + 1
            points_left = remaining_points(current_scores)
            if points_left >= 0:
                self.abilities[name].set(val + 1)
                # update_remaining_points will be called by trace
            # else: do nothing

    def decrement_ability(self, name):
        val = self.abilities[name].get()
        if val > 4:
            self.abilities[name].set(val - 1)
            # update_remaining_points will be called by trace

    def validate_and_update(self, changed_name):
        # Ensure no ability is above 8 or below 4, and points are not negative
        current_scores = {n: var.get() for n, var in self.abilities.items()}
        # Clamp values
        for n, var in self.abilities.items():
            if var.get() < 4:
                var.set(4)
            elif var.get() > 8:
                var.set(8)
        # Check points
        points_left = remaining_points(current_scores)
        if points_left < 0:
            # Revert the last change
            # Find which ability changed and revert it
            var = self.abilities[changed_name]
            old_val = var.get()
            # Try decrementing if above 4, else incrementing if below 8
            if old_val > 4:
                var.set(old_val - 1)
            elif old_val < 8:
                var.set(old_val + 1)
            # After revert, update points
            current_scores = {n: var.get() for n, var in self.abilities.items()}
            points_left = remaining_points(current_scores)
        self.points_remaining.set(points_left)
        self.remaining_label.config(text=f"Points remaining: {points_left}")
        self.update_cost_labels()

    def update_remaining_points(self):
        current_scores = {name: var.get() for name, var in self.abilities.items()}
        points_left = remaining_points(current_scores)
        self.points_remaining.set(points_left)
        self.remaining_label.config(text=f"Points remaining: {points_left}")
        self.update_cost_labels()
     