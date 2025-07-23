from tkinter import *

def start_app():
    window = Tk() #instantiate an instance of a window
    window.geometry("420x420")
    window.title("Bro Code first GUI program")

    window.config(background="#5cfcff")

    window.mainloop() #place window on computer screen, listen for events