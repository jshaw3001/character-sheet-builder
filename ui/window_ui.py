import tkinter as tk
from tkinter import ttk
from ui.builder_ui import BuilderApp
from ui.sheet_ui import SheetApp

import sv_ttk

class WindowApp(tk.Tk):
    def __init__(self, title, size):
        super().__init__()

        # Main setup
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        sv_ttk.set_theme("dark")

        # Frame setup
        self.navi_bar = NaviBar(self)
        self.navi_bar.grid(row=0, column=0, sticky="ew")

        self.container = tk.Frame(self)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid(row=1, column=0, sticky="nsew")

        self.builder_frame = BuilderApp(self.container)
        self.sheet_frame = SheetApp(self.container)

        self.builder_frame.grid(row=0, column=0, sticky="nsew")
        self.sheet_frame.grid(row=0, column=0, sticky="nsew")

        self.show_builder()

        # Run the main loop
        self.mainloop()

    def show_builder(self):
        self.builder_frame.tkraise()

    def show_sheet(self):
        self.sheet_frame.tkraise()

class NaviBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)  # Left spacer
        self.grid_columnconfigure(3, weight=1)  # Right spacer

        self.builder_button = ttk.Button(self, text="Builder", command=master.show_builder)
        self.builder_button.grid(row=0, column=1, padx=(0, 4), pady=8)

        self.sheet_button = ttk.Button(self, text="Sheet", command=master.show_sheet)
        self.sheet_button.grid(row=0, column=2, padx=(4, 0), pady=8)
