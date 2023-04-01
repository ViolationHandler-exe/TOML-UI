# noinspection PyCompatibility
import tkinter as tk
# noinspection PyCompatibility
from tkinter import filedialog
# noinspection PyCompatibility
import tkinter.ttk as ttk
# noinspection PyCompatibility
import sys
# noinspection PyCompatibility
import re
import toml
import json
import tomlkit


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # Get the current position of the mouse
        x, y = self.widget.winfo_pointerxy()

        # Calculate the position of the tooltip
        tooltip_x = x + 25
        tooltip_y = y + 20

        # Create the tooltip window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry("+%d+%d" % (tooltip_x, tooltip_y))

        # Create the tooltip label
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "9", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()


def windowDeleterSet():
    global windowDeleter
    windowDeleter = False


class TomlConfigUI:
    twoLetterWords = ["as", "up", "in", "of", "do", "to", "is", "it",
                      "on", "no", "us", "at", "go", "an", "my", "me",
                      "as", "he", "we", "so", "be", "by", "or", "do",
                      "if", "ok", "bi"]
    originalVar_Name = {}
    toml_path = None
    toml_data = None
    doc = None

    def typeMethod(self, value):
        try:
            value = int(value)
        except ValueError:
            if value.__contains__("."):
                value = float(value)
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif "[" in value and "]" in value:
                parse = value.replace("'", "\"")
                value = json.loads(parse)
            else:
                return value
        return value

    def save_to_toml(self):
        # Loop through the entry fields and update the corresponding values in the toml_data dictionary
        for i, (title, variables) in enumerate(self.toml_data.items()):
            for j, (variable, _) in enumerate(variables.items()):
                if isinstance(_, dict):
                    for j, (variable_in_dict, value) in enumerate(_.items()):
                        value = self.entry_varDict[variable_in_dict].get()
                        if isinstance(value, bool):
                            pass
                        else:
                            value = self.typeMethod(value)
                        _[variable_in_dict] = value
                        self.doc[title][variable][variable_in_dict] = value
                else:
                    value = self.entry_varDict[variable].get()
                    if isinstance(value, bool):
                        pass
                    else:
                        value = self.typeMethod(value)
                    self.doc[title][variable] = value
        # Write the updated dictionary to the original TOML file
        with open(self.toml_path, "w") as toml_file:
            toml_file.write(tomlkit.dumps(self.doc))

    def on_mousewheel(self, event):
        # Check if Control key is held down
        if event.state & 0x4:
            # Horizontal scrolling
            self.canvas.xview_scroll(int(-1 * (event.delta / 80)), "units")
        else:
            # Vertical scrolling
            self.canvas.yview_scroll(int(-1 * (event.delta / 80)), "units")

    def open_file(self):
        global windowDeleter
        global theme
        theme = window.tk.call('ttk::style', 'theme', 'use')
        windowDeleter = True
        self.x_pos = self.window.winfo_x()
        self.y_pos = self.window.winfo_y()
        TomlConfigUI(theme, self.x_pos, self.y_pos)

    # Function to handle when the entry box is clicked.
    def on_entry_click(self, event):
        mode = self.style.theme_use()
        if self.entry_var.get() == self.search_entry_default:
            self.entry_var.set("")
            # Required to keep proper coloring of entered text after clicking entry box to type.
            if mode == "light mode":
                self.entry.config(fg='black')
            elif mode == "dark mode":
                self.entry.config(fg='white')

    # Function to handle when the entry box loses focus.
    def on_focus_out(self, event):
        if self.entry_var.get() == "":
            mode = self.style.theme_use()
            self.entry_var.set(self.search_entry_default)
            self.entry.config(fg='light grey')
            # Required to keep proper coloring of default search entry after changing between light and dark mode.
            if mode == "light mode":
                self.entry.config(fg='grey')
            elif mode == "dark mode":
                self.entry.config(fg='#f7f7f7')

    # Given a filename, returns the portion of the filename that comes before the last period.
    def get_extension(self, filename):
        pos = filename.rfind(".")
        if pos == -1:
            return None
        else:
            return filename[pos + 1:]

    # Given a filepath, returns the portion of the filename that comes before the last period.
    def get_filename(self, filepath):
        pos = filepath.rfind("/")
        pos2 = filepath.rfind(".")
        if pos == -1:
            return None
        else:
            return filepath[pos + 1:pos2]

    # Function to handle the search button click.
    def search(self):
        search_text = self.entry_var.get().lower()
        # Unhighlight previously highlighted label, if any
        if self.highlighted_label:
            self.highlighted_label.config(background=self.original_color)

        # Search for the text in the labels, able to use the actual variable name with no spaces either
        results = []
        for i, child in enumerate(self.frame.winfo_children()):
            if i == 0:
                initial_Size = child.winfo_y()
            if i == len(self.frame.winfo_children()) - 1:
                final_Size = child.winfo_y()
            if isinstance(child, tk.Label) and (
                    search_text in child.cget('text').lower() or search_text in child.cget('text').lower().replace(" ",
                                                                                                                   "") or search_text.replace(
                " ", "") in child.cget('text').lower().replace(" ", "")):
                results.append(child.cget('text'))

        # Highlight the first label that matches the search text, if any
        if results:
            for child in self.frame.winfo_children():
                if isinstance(child, tk.Label) and (
                        search_text in child.cget('text').lower() or search_text in child.cget('text').lower().replace(
                    " ", "") or search_text.replace(" ", "") in child.cget('text').lower().replace(" ", "")):
                    # Get the ACTUAL size of the UI, and use that as the total size of canvas/UI to divide by
                    label_y = final_Size - initial_Size
                    # Then subtracts the other weird way to find the height from the normal way to find the height,
                    # only after multiplying the weird height by 5 to correct for wrong location that it scrolls to
                    scroll_position = (child.winfo_y() - (child.winfo_height() * 5)) / label_y
                    # Highlight the label
                    self.original_color = child.cget('background')
                    if self.style.theme_use() == "dark mode":
                        child.config(background='blue')
                    else:
                        child.config(background='yellow')
                    self.highlighted_label = child
                    self.canvas.yview_moveto(scroll_position)
                    self.result_label.config(text="")
                    break
        else:
            self.result_label.config(text="No results found.", font="bold")
            # Clear the highlighted label
            self.highlighted_label = None

    # Mode = Default Theme
    def __init__(self, mode='light mode', xPosition=None, yPosition=None):
        size_of_window = "525x900"
        self.Dark_Mode_Hex = '#0A0A0A'
        self.Light_Mode_Hex = '#f0f0f0'
        self.LightGreen_Hex = '#6bcc6b'
        self.LightRed_Hex = '#ff8585'
        self.checkboxDict = {}

        def toggle_theme(current_theme=None):
            self.frame.focus()
            # Get the current theme (This means the theme it USED to be, and is going to be the opposite after this)
            if current_theme is None:
                current_theme = self.style.theme_use()

            if current_theme == 'light mode':
                # Switch to the dark theme
                self.style.theme_use('dark mode')
                theme_switch(current_theme, self.Dark_Mode_Hex, self.Light_Mode_Hex)
            else:
                # Switch to the light theme
                self.style.theme_use('light mode')
                theme_switch(current_theme, self.Light_Mode_Hex, 'black')

        def theme_switch(current_theme, bg, fg):
            # Update the colors of the widgets
            self.result_label.config(background=bg, foreground=fg)
            insertColor = "black"
            if current_theme == "light mode":
                insertColor = "white"
                if self.entry_var.get() == self.search_entry_default:
                    self.entry.config(background=bg, foreground='light grey', insertbackground="white")
                else:
                    self.entry.config(background=bg, foreground='white', insertbackground="white")
                self.frame.configure(bg=self.Dark_Mode_Hex)
                self.canvas.configure(bg=self.Dark_Mode_Hex)
                window.configure(bg=self.Dark_Mode_Hex)
                self.Dark_Mode_toggle_button.config(background=bg, foreground=fg, text="Light Mode", activebackground='dark grey')
                self.save_button.config(background=bg, foreground=fg, activebackground='dark grey')
                self.open_button.config(background=bg, foreground=fg, activebackground='dark grey')
                self.search_button.config(background=bg, foreground=fg, activebackground='dark grey')
            else:
                insertColor = "black"
                if self.entry_var.get() == self.search_entry_default:
                    self.entry.config(background=bg, foreground='grey', insertbackground="black")
                else:
                    self.entry.config(background=bg, foreground='black', insertbackground="black")
                self.canvas.configure(bg=self.Light_Mode_Hex)
                self.frame.configure(bg=self.Light_Mode_Hex)
                window.configure(bg=self.Light_Mode_Hex)
                self.Dark_Mode_toggle_button.config(background=bg, foreground=fg, text="Dark Mode", activebackground='dark grey')
                self.save_button.config(background=bg, foreground=fg, activebackground='dark grey')
                self.open_button.config(background=bg, foreground=fg, activebackground='dark grey')
                self.search_button.config(background=bg, foreground=fg)

            for widget in self.frame.winfo_children():
                if isinstance(widget, tk.Label):
                    if widget.cget('bg') == "yellow":
                        widget.config(background="blue", foreground=fg)
                    elif widget.cget('bg') == "blue":
                        widget.config(background="yellow", foreground=fg)
                    else:
                        widget.config(background=bg, foreground=fg)
                elif isinstance(widget, tk.Entry):
                    widget.config(background=bg, foreground=fg, insertbackground=insertColor)

        def openTOML():
            self.toml_path = filedialog.askopenfilename(title="Select TOML file")
            global file_type
            file_type = self.get_extension(self.toml_path)
            if str(self.toml_path) == "":
                sys.stderr.write(
                    "Error: self.toml_path is NULL/empty, which likely means no file was selected. Please try "
                    "again, but select a file this time.")
                return
            elif file_type != "toml":
                sys.stderr.write("Error: Please input a TOML file, otherwise this will not work.\n")
                return
            # Parse TOML file
            with open(self.toml_path, 'r') as f:
                self.toml_string = f.read()
                self.doc = tomlkit.parse(self.toml_string)
                self.toml_data = toml.loads(self.toml_string)

        try:
            openTOML()
        except FileNotFoundError as e:
            sys.stderr.write("Error: File not Found!" + "\n")

        # Create a way to allow tabs of the TOML files in the UI, probably creating a list of self.toml_paths and keep them until
        # they are closed, which means neeeding a way to tell if a TOML file is closed or not after it being opened.

        # I essentially need a list of the file paths, then after it also need a way to tell if one of those file paths
        # has closed, to remove it from the list, along with that a way to determine which TOML file its on, and save THAT
        # toml file rather than either all of them or a different TOML file

        # noinspection PyTypeChecker
        file_type = self.get_extension(self.toml_path)

        global window
        # This already has printed the error, now it just needs to stop creating the window without exiting program.
        if str(self.toml_path) == "" or file_type != "toml":
            return
        self.filename = self.get_filename(self.toml_path)
        print("You opened: ", self.filename, ".toml", sep="")
        self.entries = {}

        if windowDeleter is True:
            window.destroy()
        # Create main window
        window = tk.Tk()
        window.title("TOML Config UI")
        if xPosition is not None and yPosition is not None:
            window.geometry(f"+{xPosition}+{yPosition}")
        self.style = ttk.Style()
        self.window = window

        # Create a light theme (called clam originally)
        self.style.theme_create('light mode', parent='clam')
        self.style.theme_settings('light mode', {})

        # Create a dark theme (called xpnative originally)
        self.style.theme_create('dark mode', parent='xpnative')
        self.style.theme_settings('dark mode', {})
        self.style.theme_use(mode)

        # Set size here
        window.geometry(size_of_window)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        self.window = window

        # Create canvas and scrollbar for vertical AND horizontal scrolling using Ctrl Key
        self.canvas = tk.Canvas(window, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='NSEW')

        self.master = self.canvas

        self.scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='NS')

        self.horizontal_scrollbar = tk.Scrollbar(window, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.horizontal_scrollbar.grid(row=1, column=0, sticky='EW')

        # Create a frame inside the canvas for placing labels and entries
        self.frame = tk.Frame(self.canvas)
        self.frame.configure(bg=self.Light_Mode_Hex)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # Bind canvas to scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.config(xscrollcommand=self.horizontal_scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Populate the UI with the labels and entries
        self._create_widgets()

        # Create Save and Open button
        self.save_button = tk.Button(window, text="Save", font='TkDefaultFont 14 bold', command=self.save_to_toml, cursor="hand2")
        self.open_button = tk.Button(window, text="Open", font='TkDefaultFont 14 bold', command=self.open_file, cursor="hand2")
        self.open_button.grid(row=0, column=0, sticky='N', padx=(50, 0), pady=(35, 10))
        self.save_button.grid(row=0, column=0, sticky='N', padx=(0, 100), pady=(35, 10))

        # Create a Search box entry + Button
        self.entry_var = tk.StringVar()
        self.search_entry_default = "Search for Variable:"
        self.entry_var.set(self.search_entry_default)
        self.entry = tk.Entry(window, width=25, textvariable=self.entry_var, fg='grey')
        self.entry.bind('<FocusIn>', self.on_entry_click)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.grid(row=0, column=0, sticky='N', padx=(0, 325), pady=(8, 10))

        # Button for Search Box
        self.search_button = tk.Button(window, text="Search", command=self.search, cursor="hand2")
        self.search_button.grid(row=0, column=0, sticky='N', padx=(0, 100), pady=(3, 10))
        self.result_label = tk.Label(window)
        self.result_label.grid(row=0, column=0, sticky='N', padx=(363, 0), pady=(0, 10))

        # Button for Dark/Light Mode
        # Maybe change dark Mode Button location to be in bottom? Same with search maybe?
        self.Dark_Mode_toggle_button = tk.Button(window, text='Dark Mode', command=toggle_theme, cursor="hand2")
        self.Dark_Mode_toggle_button.grid(row=0, column=0, sticky='N', padx=(52, 0), pady=(3, 10))

        # Convert Light Mode into Dark Mode if it was originally in Dark Mode
        if mode == 'dark mode':
            toggle_theme("light mode")

        # Set to False to allow self.search function to work properly
        self.highlighted_label = False
        self.original_color = False

        # Bring to front for initial opening, but allow it to not remain on top forever.
        self.window.lift()

        # Run main loop
        self.run()

    def run(self):
        # Deconify required to actually lift to front using window.lift()
        self.window.deiconify()
        window.mainloop()

    def toolTipComments(self):
        def remove_after_equals(s):
            # Match the pattern of any whitespace, followed by any number of characters, followed by the '=' sign
            pattern = s.split('=')[0].strip()
            pattern = pattern.replace('"', '')
            return pattern

        def remove_tabs(s):
            return s.replace('\t', '')

        tomlComments = tomlkit.dumps(self.doc)
        lines = tomlComments.split('\n')
        prev_line = ''
        # Comment retrieving loop that makes sure 90% (or more) comment types are allowed into tooltips
        for i in range(len(lines)):
            line = lines[i]
            comments = remove_tabs(prev_line)
            rangeValues = remove_tabs(line)
            if ("true" in line.lower() or "false" in line.lower()) and "=" in line:
                variable = remove_after_equals(lines[i])
                self.variableComments[variable] = variable, comments
            if "allowed values" in line.lower():
                variable = remove_after_equals(lines[i + 1])
                self.variableComments[variable] = variable, comments, rangeValues
                self.rowValue += 1
            elif line.istitle() and "range" in line.lower():
                variable = remove_after_equals(lines[i + 1])
                self.variableComments[variable] = variable, comments, rangeValues
                self.rowValue += 1
            elif "=[" in line.replace(" ", ""):
                variable = remove_after_equals(lines[i])
                self.variableComments[variable] = variable, comments
            elif '= "' in line.lower():
                variable = remove_after_equals(lines[i])
                self.variableComments[variable] = variable, comments, rangeValues
            prev_line = line

    def varProcess(self, var_name, var_value=None):
        oldVar_Name = var_name
        # Fix for fully capitalized variable names
        if all(c.isupper() for c in var_name if c.isalpha()):
            var_name = var_name.lower()
        var_name = var_name.replace("_", " ")
        var_name = var_name.replace("-", "      ")
        # Takes care of capitals in 'HP', converting to 'Hp'
        match = re.search(r'[A-Z]{2}', var_name)

        if match:
            if any(x.isupper() for x in var_name):
                for i in range(len(var_name) - 1):
                    if var_name[i].isupper() and var_name[i + 1].isupper():
                        var_name = var_name[:i + 1] + var_name[i + 1].lower() + var_name[i + 2:]
                        break

        # Adds a space between all characters that start with a Capital Letter
        var_name = re.sub(r'([A-Z])', r' \1', var_name)
        # Capitalizes all words/letters that are separated by a space.
        var_name = " ".join(var_name.split()).title()
        if "By" in var_name:
            var_name = var_name.replace("By", "by")
        if any(x.isupper() for x in var_name):
            for i in range(len(var_name) - 1):
                if (len(var_name) == i + 2 and i != 0 and var_name[i] and var_name[i + 1].islower() and var_name[
                    i - 1].isspace()) or \
                        (len(var_name) != i + 2 and i != 0 and var_name[i + 2].isspace() and (
                                var_name[i - 1].isspace())) or \
                        (var_name[i].isupper() and i == 0 and len(var_name) >= i + 2 and var_name[i + 2].isspace()) or \
                        (i != 0 and len(var_name) > i + 2 and var_name[i - 1].isspace() and var_name[
                            i + 2].isspace() and var_name[i].isupper()):
                    if var_name[i:i + 2].lower() in self.twoLetterWords:
                        pass
                        if var_name[2] == " ":
                            pass
                        else:
                            var_name = var_name[:i] + var_name[i:i + 1].lower() + var_name[i + 1:i + 2] + var_name[
                                                                                                          i + 2:]
                    else:
                        var_name = var_name[:i + 1] + var_name[i + 1:i + 2].capitalize() + var_name[i + 2:]

        if var_value is not None:
            if isinstance(var_value, bool):
                var_value = str(var_value).lower()
            # Truncate the input value to 4 decimal places
            if isinstance(var_value, float) and len(str(var_value).split('.')[1]) > 4:
                var_value = round(var_value, 4)
                # Round up the last digit of the decimal place by one
                if str(var_value).split('.')[1][-1] != '0':
                    var_value = round(var_value + 0.0001, 4)

        # Fixes weird capitalization issue in "n't" type contraction words in variable names.
        if "n'T" in var_name:
            var_name = var_name.replace("n'T", "n't")

        if var_name == "":
            self.originalVar_Name[self.key] = oldVar_Name
        else:
            self.originalVar_Name[var_name] = oldVar_Name

        if var_value is not None:
            return var_name, var_value
        else:
            return var_name

    def checkbox_changed(self):
        self.entry_var.get()
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                if widget.cget("bg") == "red" or widget.cget("bg") == "green":
                    val = bool(self.entry_varDict[self.checkboxDict[widget]].get())
                    if val is True:
                        widget.config(text="true", foreground="black", activebackground=self.LightGreen_Hex)
                    else:
                        widget.config(text="false", foreground="black", activebackground=self.LightRed_Hex)
        self.frame.focus()

    def _create_widgets(self):
        global keys
        self.subTables = {}  # CATEGORIES/Sub Tables
        self.entryArray = {}
        self.entry_varDict = {}

        # Sort config data by keys to ensure consistent order
        keys = self.toml_data.keys()

        self.variableComments = {}
        self.rowValue = 0  # Used for ToolTip Comments
        self.row = 0  # Used to progress the UI labels/entry boxes to next rows
        self.toolTipComments()

        # Checks for Unlabeled Categories, and labels them "Unlabeled Category" (PRETTY SURE ONLY CHECKS FOR UNLABELED CATEGORY IN BEGINNING)
        # It also adds spacing to the top, so it is below the save/open buttons
        self.initialKey = False
        for key in keys:
            value = self.toml_data[key]
            variables = self._flatten_variables(value)

            # Groups
            if variables[0][0] == "":
                self.label = tk.Label(self.frame, text="Unlabeled Category", font='TkDefaultFont 16 bold')
                # This part is spacing portion (75, 0)
                self.label.grid(row=self.row, column=0, sticky='W', pady=(75, 0))
                self.row += 1
                break
            else:
                if not self.initialKey:
                    self.initialKey = key
                break

        self.value = 0
        for key in keys:
            self.key = key
            value = self.toml_data[self.key]
            variables = self._flatten_variables(value)
            if variables[0][0] != "":
                # Create a label for the group
                self.table_name = self.key
                self.label = tk.Label(self.frame, text=self.key, font='TkDefaultFont 16 bold')
                # If category is first category on UI, add spacing to the top, so it is below the save/open buttons
                if self.initialKey == key:
                    self.label.grid(row=self.row, column=0, sticky='W', pady=(75, 0))
                else:
                    self.label.grid(row=self.row, column=0, sticky='W', pady=(10, 0))
            self.create_UI(variables)
            self.row += 1

    def create_entries(self, var_value, var_name):
        if "[" in str(var_value) and "]" in str(var_value):
            # Separate into arrays/words and then use that as a multiplier
            lengthStr = int(len(str(var_value)) * (1.4 / 2))
            self.entry = tk.Entry(self.frame, font='TkDefaultFont 12', textvariable=self.entry_var,
                                  width=8 + lengthStr)  # (length*10))
            self.entry.grid(row=self.row + 1, column=1, padx=10, sticky='w')
        elif isinstance(var_value, str) and ("true" in var_value.lower() or "false" in var_value.lower()):
            self.entry_var = tk.BooleanVar(value=False)
            color = self.LightRed_Hex
            if "true" in var_value.lower():
                self.entry_var.set(True)
                color = self.LightGreen_Hex
            self.checkbox = tk.Checkbutton(self.frame, variable=self.entry_var, onvalue=True, offvalue=False, cursor="hand2",
                                           command=self.checkbox_changed, indicatoron=False, text=var_value,
                                           bg='red', selectcolor='green', foreground="black", width=12, activebackground=color)
            self.checkbox.grid(row=self.row + 1, column=1, padx=10, sticky='w')
            self.checkboxDict[self.checkbox] = var_name
        else:
            self.entry = tk.Entry(self.frame, font='TkDefaultFont 12', textvariable=self.entry_var, width=10)
            self.entry.grid(row=self.row + 1, column=1, padx=10, sticky='w')

    def create_toolTips(self, var_value):
        if "true" in var_value.lower() or "false" in var_value.lower() or "[" in var_value:
            if self.defaultVar_name in self.variableComments and self.variableComments[self.defaultVar_name][
                        0] == self.defaultVar_name:
                comment = self.variableComments[self.defaultVar_name][1]
                if "#" in comment:
                    if len(comment) > 150:
                        array = comment.split(" ")
                        halfArray = len(array) // 2
                        ToolTip(self.varLabel, " ".join(array[:halfArray]) + '\n      ' + " ".join(array[halfArray:]))
                    else:
                        ToolTip(self.varLabel, comment)
        else:
            if self.defaultVar_name in self.variableComments and self.variableComments[self.defaultVar_name][
                0] == self.defaultVar_name:
                comment = self.variableComments[self.defaultVar_name][1]
                try:
                    rangeValues = self.variableComments[self.defaultVar_name][2]
                except IndexError:
                    rangeValues = None
                if "#" not in comment:
                    if rangeValues is not None:
                        ToolTip(self.varLabel, rangeValues)
                elif rangeValues is None:
                    ToolTip(self.varLabel, comment)
                elif str(self.defaultVar_value).__contains__(':'):
                    ToolTip(self.varLabel, comment)
                else:

                    ToolTip(self.varLabel, comment + "\n" + rangeValues)

    def create_UI(self, variables):
        self.labelNumber = {}
        for var_name, var_value in variables:
            self.defaultVar_name = var_name
            if self.defaultVar_name == "":
                self.defaultVar_name = self.key
            self.defaultVar_value = var_value
            var_name, var_value = self.varProcess(var_name, var_value)

            for k, v in self.subTables.items():
                # V = the dict of all key and value combos.
                first_key, first_value = next(iter(v.items()))
                first_key = self.varProcess(first_key)
                table_name = k

                if var_name == first_key:
                    if self.label is not None:
                        self.row += 1
                        k = self.varProcess(k)
                        self.varLabel = tk.Label(self.frame, text=k, font='TkDefaultFont 13 bold')
                        # Checks if first row
                        if "'row': 0" in str(self.label.grid_info()):
                            self.varLabel.grid(row=self.row, column=0, sticky='W', padx=30)
                        else:
                            self.varLabel.grid(row=self.row, column=0, sticky='W', padx=30, pady=(5, 0))
                        self.subTables.pop(table_name)
                        break
                else:
                    break
            if len(str(var_value)) > 400:
                print("There was a value that was too long to be inputted. \nVar Name: '" + var_name +
                      "' in table: '" + self.table_name + "'\nValue =",
                      var_value)
                var_value = "(**ERROR STRING ENTRY TOO LONG**)"
            self.entry_var = tk.StringVar(value=str(var_value))

            if var_name == "":
                var_name = self.varProcess(self.key)

            # Create the Entry Boxes
            self.create_entries(var_value, self.defaultVar_name)
            self.entryArray[self.value] = self.entry_var


            self.varLabel = tk.Label(self.frame, text=var_name, font='TkDefaultFont 12')
            self.entry_varDict[self.originalVar_Name[var_name]] = self.entry_var
            self.labelNumber[self.value] = self.varLabel
            self.varLabel.grid(row=self.row + 1, column=0, sticky='W', padx=10)
            var_value = str(var_value)

            # Create comments in ToolTip form
            self.create_toolTips(var_value)
            self.row += 1
            self.value += 1

    def _flatten_variables(self, value, prefix=""):
        variables = []
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, dict):
                    self.subTables[k] = v
                ## USED FOR SPECIFICALLY SUB TABLES!
                if prefix and k.startswith(prefix + "_"):
                    self.subTables[k] = k[len(prefix) + 1:]
                    k = k[len(prefix) + 1:]
                    variables.append((k, v))
                else:
                    if isinstance(v, dict):
                        pass
                    variables += self._flatten_variables(v, k)
        else:
            variables.append((prefix, value))
        return variables


windowDeleterSet()
TomlConfigUI()
