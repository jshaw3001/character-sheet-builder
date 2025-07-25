import os
import re
import json
import tkinter as tk
from tkinter import ttk, messagebox
from models.character import Character
from logic.ability_roll import ability_roll
from logic.ability_modifier import score_to_modifier

class SheetApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        #widgets
        self.header = Header(self, "Character Sheet Viewer")
        self.character_selector = CharacterSelector(self, self.log_to_console)
        self.console = tk.Text(self, height=4, state="disabled", bg="#222", fg="#fff")
        self.console.pack(side="bottom", fill="x", padx=10, pady=10)

    def log_to_console(self, message):
        self.console.config(state="normal")
        self.console.insert("end", message + "\n")
        self.console.see("end")
        self.console.config(state="disabled")

class Header(ttk.Label):
    def __init__(self, master, text):
        super().__init__(master, text=text)
        self.pack(pady=5)

class CharacterSelector(ttk.Frame):
    def __init__(self, master, log_callback=None):
        super().__init__(master)
        self.pack(pady=5)
        self.log_callback = log_callback
        
        self.current_desc = None # Tracks current character description

        self.create_widgets()
    
    def create_widgets(self):
        self.label = ttk.Label(self, text="Select Character:")
        self.label.pack(pady=5)

        self.character_list = ttk.Combobox(self, state="readonly")
        self.character_list.pack(pady=5)
        self.load_characters()

        self.character_list.bind("<<ComboboxSelected>>", self.load_character)
        self.character_list.bind("<Button-1>", lambda e: self.load_characters())  # Refresh on click

    def load_characters(self):
        characters_dir = "characters"
        os.makedirs("characters", exist_ok=True)
        
        files = [f for f in os.listdir(characters_dir) if f.endswith('.json')]
        # Display names of characters instead of filenames
        display_names = []
        self.display_to_file = {}
        for f in files:
            try:
                with open(os.path.join(characters_dir, f), 'r') as file:
                    data = json.load(file)
                    name = data.get("name", "Unknown")
                    char_class = data.get("class", "Unknown")
                    display = f"{name} ({char_class})"
                    display_names.append(display)
                    self.display_to_file[display] = f
            except Exception:
                continue # Skip files that can't be read

        self.character_list['values'] = display_names

    def load_character(self, event=None):
        selected_display = self.character_list.get()
        selected_file = self.display_to_file.get(selected_display)

        if not selected_file:
            return
        
        filepath = os.path.join("characters", selected_file)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                character = Character.from_dict(data)
                if self.current_desc is not None:
                    self.current_desc.destroy()
                self.current_desc = CharacterDescription(self.master, character, self.log_callback)
                self.current_desc.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load character: {e}")

class CharacterDescription(ttk.Frame):
    def __init__(self, master, character, log_callback=None):
        super().__init__(master)
        self.character = character
        self.log_callback = log_callback
        self.create_widgets()

    def create_widgets(self):
        name_label = ttk.Label(self, text=f"Name: {self.character.name}")
        name_label.pack(pady=5)

        class_label = ttk.Label(self, text=f"Class: {self.character.char_class}")
        class_label.pack(pady=5)

        level_label = ttk.Label(self, text=f"Level: {self.character.level}")
        level_label.pack(pady=5)    
        
        stats_table = AbilitiesFrame(self, self.character.stats, self.log_callback)
        stats_table.pack(pady=5)

        skills_frame = SkillsFrame(self, self.character.skills, self.character.stats, self.log_callback)
        skills_frame.pack(pady=5)

        
class AbilitiesFrame(ttk.Frame):
    def __init__(self, master, stats, log_callback=None):
        super().__init__(master)
        self.stats = stats
        self.log_callback = log_callback
        self.create_widgets()

    def create_widgets(self):
        abilities_header = ttk.Label(self, text="Abilities:")
        abilities_header.pack(pady=5)

        abilities_grid = AbilitiesGrid(self, self.stats, self.log_callback)
        abilities_grid.pack(pady=5)

class AbilitiesGrid(ttk.Frame):
    def __init__(self, master, stats, log_callback=None):
        super().__init__(master)
        self.stats = stats
        self.log_callback = log_callback
        self.create_widgets()

    def create_widgets(self):
        for i, (stat, value) in enumerate(self.stats.items()):
            stat_label = ttk.Label(self, text=str(stat), width=10, justify=tk.CENTER, anchor="center")
            stat_label.grid(row=0, column=i, padx=5, pady=2)
            stat_value = ttk.Label(self, text=str(value), width=5, justify=tk.CENTER, anchor="center")
            stat_value.grid(row=1, column=i, padx=5, pady=2)
            modifier = score_to_modifier(value)
            stat_roll = ttk.Button(self, text=f"Roll ({modifier:+})", command=lambda s=stat: self.roll_stat(s))
            stat_roll.grid(row=2, column=i, padx=5, pady=2)

    def roll_stat(self, stat):
        roll, modifier, total = ability_roll(self.stats[stat])
        if self.log_callback:
            self.log_callback(f"Rolled {stat}: dice={roll} modifier={modifier}  total={total}")

class SkillsFrame(ttk.Frame):
    def __init__(self, master, skills, stats, log_callback=None):
        super().__init__(master)
        self.skills = skills
        self.stats = stats
        self.log_callback = log_callback
        self.create_widgets()

    def create_widgets(self):
        skills_header = ttk.Label(self, text="Skills:")
        skills_header.pack(pady=5)

        for skill in self.skills:
            skill_label = ttk.Label(self, text=f"{skill.name}: {skill.description} ({skill.dice_formula})")
            skill_label.pack(pady=2)  # Adjust padding as needed
            match = re.search(r"\+(\w+)", skill.dice_formula)
            if match:
                stat_name = match.group(1)
                stat_value = self.stats.get(stat_name, 0)
                modifier = score_to_modifier(stat_value)
            else:
                modifier = 0
            skill_roll = ttk.Button(self, text=f"Roll ({modifier:+})", command=lambda sk=skill: self.roll_skill(sk))
            skill_roll.pack(pady=2)

    def roll_skill(self, skill):
        roll, modifier, total = skill.roll(self.stats)
        if self.log_callback:
            self.log_callback(f"Rolled {skill.name}: dice={roll} modifier={modifier}  total={total}")
