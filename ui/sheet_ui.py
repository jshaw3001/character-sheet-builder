"""# TODO: Character Sheet UI (`sheet_ui.py`)

- [ ] Create a new Tkinter window to display a character sheet.
- [ ] Load a character JSON file from the `characters` folder.
- [ ] Parse the JSON and display:
    - Character name
    - Class
    - Level
    - Ability scores (in a grid or table)
- [ ] Use ttk widgets and sv_ttk theme for consistency.
- [ ] Add a file picker or dropdown to select which character to display.
- [ ] (Optional) Add buttons for editing or deleting characters.
- [ ] (Optional) Add a print/export to PDF feature.

**Start by:**
- Creating the basic window and layout.
- Loading and parsing a character JSON file.
- Displaying the character’s info in a readable format.

---

*Refer to your existing builder UI for ttk/sv_ttk setup and widget usage!*"""


from tkinter import *

def start_app():
    window = Tk() #instantiate an instance of a window
    window.geometry("420x420")
    window.title("Bro Code first GUI program")

    window.config(background="#5cfcff")

    window.mainloop() #place window on computer screen, listen for events