# noinspection PyCompatibility
import tkinter as tk
# noinspection PyCompatibility
from tkinter import filedialog
# noinspection PyCompatibility
import tkinter.ttk as ttk
# noinspection PyCompatibility
import sys
# noinspection PyCompatibility
import tkinter.font as font
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
        # Loop through the entr3y fields and update the corresponding values in the toml_data dictionary
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
        if event.state & 0x4:  # Check if Control key is held down
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
        TomlConfigUI(theme)

    def on_entry_click(self, event):
        mode = self.style.theme_use()
        """Function to handle when the entry box is clicked."""
        if self.entry_var.get() == self.search_entry_default:
            self.entry_var.set("")
        if mode == "light mode":
            self.entry.config(fg='black')
        elif mode == "dark mode":
            self.entry.config(fg='white')

    def on_focus_out(self, event):
        """Function to handle when the entry box loses focus."""
        if self.entry_var.get() == "":
            mode = self.style.theme_use()
            self.entry_var.set(self.search_entry_default)
            self.entry.config(fg='light grey')
            if mode == "light mode":
                self.entry.config(fg='grey')
            elif mode == "dark mode":
                self.entry.config(fg='#f7f7f7')

    def get_extension(self, filename):
        """
        Given a filename, returns the portion of the filename that comes before the last period.
        """
        pos = filename.rfind(".")
        if pos == -1:
            return None
        else:
            return filename[pos+1:]

    def search(self):
        """Function to handle the search button click."""
        search_text = self.entry_var.get().lower()

        # Unhighlight previously highlighted label, if any
        if self.highlighted_label:
            self.highlighted_label.config(background=self.original_color)

        # Search for the text in the labels, able to use the actual variable name with no spaces too
        results = []
        for i, child in enumerate(self.frame.winfo_children()):
            if i == 0:
                initial_Size = child.winfo_y()
            if i == len(self.frame.winfo_children())-1:
                final_Size = child.winfo_y()
            if isinstance(child, tk.Label) and (search_text in child.cget('text').lower() or search_text in child.cget('text').lower().replace(" ", "") or search_text.replace(" ", "") in child.cget('text').lower().replace(" ", "")):
                results.append(child.cget('text'))

        # Highlight the first label that matches the search text, if any
        if results:
            for child in self.frame.winfo_children():
                if isinstance(child, tk.Label) and (search_text in child.cget('text').lower() or search_text in child.cget('text').lower().replace(" ", "") or search_text.replace(" ", "") in child.cget('text').lower().replace(" ", "")):
                    # Get the ACTUAL size of the UI, and use that as the total size of canvas/UI to divide by
                    label_y = final_Size-initial_Size
                    # Then subtracts the other weird way to find the height from the normal way to find the height,
                    # only after multiplying the weird height by 5 to correct for wrong location that it scrolls to
                    scroll_position = (child.winfo_y()-(child.winfo_height()*5)) / label_y
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
    def __init__(self, mode='light mode'):
        self.doc = None
        size_of_window = "525x900"
        self.toml_path = None
        DARK_MODE_HEX_VALUE = '#0A0A0A'
        LIGHT_MODE_HEX_VALUE = '#f0f0f0'
        def toggle_theme(current_theme=None):
            # Get the current theme (This means the theme it USED to be, and is going to be the opposite after this)
            if current_theme is None:
                current_theme = self.style.theme_use()
            def theme_switch(bg, fg):
                # Update the colors of the widgets
                self.result_label.config(background=bg, foreground=fg)
                self.save_button.config(background=bg, foreground=fg)
                self.open_button.config(background=bg, foreground=fg)
                if current_theme == "light mode":
                    if self.entry_var.get() == self.search_entry_default:
                        self.entry.config(background=bg, foreground='light grey')
                    else:
                        self.entry.config(background=bg, foreground='white')
                    self.Dark_Mode_toggle_button.config(background=bg, foreground=fg, text="Light Mode")
                else:
                    if self.entry_var.get() == self.search_entry_default:
                        self.entry.config(background=bg, foreground='grey')
                    else:
                        self.entry.config(background=bg, foreground='black')
                    self.Dark_Mode_toggle_button.config(background=bg, foreground=fg, text="Dark Mode")
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
                        widget.config(background=bg, foreground=fg)

            if current_theme == 'light mode':
                # Switch to the dark theme
                background_color = DARK_MODE_HEX_VALUE
                foreground_color = LIGHT_MODE_HEX_VALUE
                self.style.theme_use('dark mode')
                self.frame.configure(bg=DARK_MODE_HEX_VALUE)
                self.canvas.configure(bg=DARK_MODE_HEX_VALUE)
                window.configure(bg=DARK_MODE_HEX_VALUE)
                theme_switch(background_color, foreground_color)
            else:
                # Switch to the light theme
                background_color = LIGHT_MODE_HEX_VALUE
                foreground_color = 'black'
                self.style.theme_use('light mode')
                self.canvas.configure(bg=LIGHT_MODE_HEX_VALUE)
                self.frame.configure(bg=LIGHT_MODE_HEX_VALUE)
                window.configure(bg=LIGHT_MODE_HEX_VALUE)
                theme_switch(background_color, foreground_color)

        def openTOML():
            self.toml_path = filedialog.askopenfilename(title="Select TOML file")
            global file_type
            file_type = self.get_extension(self.toml_path)
            if file_type != "toml":
                sys.stderr.write("Error: Please input a TOML file, otherwise this will not work.")
                return
            # Parse TOML file
            with open(self.toml_path, 'r') as f:
                self.toml_string = f.read()
                self.doc = tomlkit.parse(self.toml_string)
                self.toml_data = toml.loads(self.toml_string)

        try:
            openTOML()
        except FileNotFoundError as e:
            sys.stderr.write("Error: File not Found!"+"\n")

        # Create a way to allow tabs of the TOML files in the UI, probably creating a list of self.toml_paths and keep them until
        # they are closed, which means neeeding a way to tell if a TOML file is closed or not after it being opened.

        # I essentially need a list of the file paths, then after it also need a way to tell if one of those file paths
        # has closed, to remove it from the list, along with that a way to determine which TOML file its on, and save THAT
        # toml file rather than either all of them or a different TOML file

        # noinspection PyTypeChecker
        file_type = self.get_extension(self.toml_path)

        global window
        if str(self.toml_path) == "":
            sys.stderr.write("Error: self.toml_path is NULL/empty, which likely means no file was selected. Please try "
                             "again, but select a file this time.")
            return
        elif file_type != "toml":
            sys.stderr.write("Error: Please input a TOML file, otherwise this will not work.")
            return
        self.filename = self.toml_path
        self.entries = {}

        if windowDeleter is True:
            window.destroy()
        # Create main window
        window = tk.Tk()
        window.title("TOML Config UI")
        self.style = ttk.Style()

        # Create a light theme (called clam originally)
        self.style.theme_create('light mode', parent='alt', settings={
            'TLabel': {'configure': {'background': LIGHT_MODE_HEX_VALUE, 'foreground': 'black'}},
            'TButton': {'configure': {'background': LIGHT_MODE_HEX_VALUE, 'foreground': 'black'}}
        })

        # Create a dark theme (called xpnative originally)
        self.style.theme_create('dark mode', parent='alt', settings={
            'TLabel': {'configure': {'background': DARK_MODE_HEX_VALUE, 'foreground': LIGHT_MODE_HEX_VALUE}},
            'TButton': {'configure': {'background': DARK_MODE_HEX_VALUE, 'foreground': LIGHT_MODE_HEX_VALUE}}
        })
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
        self.frame.configure(bg=LIGHT_MODE_HEX_VALUE)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # Bind canvas to scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.config(xscrollcommand=self.horizontal_scrollbar.set)
        self.canvas.bind('<Configure>', self._on_canvas_resize)

        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)


        # Populate the UI with the labels and entries
        self._create_widgets()

        # Create Save and Open button
        self.save_button = tk.Button(window, text="Save", font='TkDefaultFont 14 bold', command=self.save_to_toml)
        self.open_button = tk.Button(window, text="Open", font='TkDefaultFont 14 bold', command=self.open_file)
        self.open_button.grid(row=0, column=0, sticky='N', padx=(50, 0), pady=(35, 10))
        self.save_button.grid(row=0, column=0, sticky='N', padx=(0, 100), pady=(35, 10))

        # Create a Search Entry box + Button
        self.entry_var = tk.StringVar()
        self.search_entry_default = "Search for Variable:"
        self.entry_var.set(self.search_entry_default)
        self.entry = tk.Entry(window, width=25, textvariable=self.entry_var, fg='grey')
        self.entry.bind('<FocusIn>', self.on_entry_click)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.grid(row=0, column=0, sticky='N', padx=(0, 325), pady=(8, 10))

        # Button for Search Box
        self.search_button = tk.Button(window, text="Search", command=self.search)
        self.search_button.grid(row=0, column=0, sticky='N', padx=(0, 100), pady=(3, 10))
        self.result_label = tk.Label(window)
        self.result_label.grid(row=0, column=0, sticky='N', padx=(363, 0), pady=(0, 10))

        # Button for Dark/Light Mode
        # Maybe change dark Mode Button location to be in bottom? Same with search maybe?
        self.Dark_Mode_toggle_button = tk.Button(window, text='Dark Mode', command=toggle_theme)
        self.Dark_Mode_toggle_button.grid(row=0, column=0, sticky='N', padx=(52, 0), pady=(3, 10))

        # Convert Light Mode into Dark Mode if it was originally in Dark Mode
        if mode == 'dark mode':
            toggle_theme("light mode")

        # Set to False to allow self.search function to work properly
        self.highlighted_label = False
        self.original_color = False

        # Run main loop
        self.run()

    def run(self):
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
        for i in range(len(lines)):
            line = lines[i]
            comments = remove_tabs(prev_line)
            rangeValues = remove_tabs(line)
            if ("true" in line.lower() or "false" in line.lower()) and "=" in line:
                variable = remove_after_equals(lines[i])
                self.variableComments[variable] = variable, comments
            if "allowed values" in line.lower():
                variable = remove_after_equals(lines[i+1])
                self.variableComments[variable] = variable, comments, rangeValues
                self.rowValue += 1
            elif line.istitle() and "range" in line.lower():
                variable = remove_after_equals(lines[i+1])
                self.variableComments[variable] = variable, comments, rangeValues
                self.rowValue += 1
            elif "=[" in line.replace(" ", ""):
                variable = remove_after_equals(lines[i])
                self.variableComments[variable] = variable, comments
            elif '= "' in line.lower():
                variable = remove_after_equals(lines[i])
                self.variableComments[variable] = variable, comments, rangeValues
            #FIX METHOD BELOW PLEASE
            prev_line = line

    def varProcess(self, var_name, var_value=None):
        oldVar_Name = var_name
        var_name = var_name.replace("_", " ")
        var_name = var_name.replace("-", "      ")
        # Takes care of capitals in 'HP', converting to 'Hp'
        match = re.search(r'[A-Z]{2}', var_name)

        if match:
            if any(x.isupper() for x in var_name):
                for i in range(len(var_name)-1):
                    if var_name[i].isupper() and var_name[i+1].isupper():
                        var_name = var_name[:i+1] + var_name[i+1].lower() + var_name[i+2:]
                        break
        # Adds a space between all characters that start with a Capital Letter
        var_name = re.sub(r'([A-Z])', r' \1', var_name)
        # Capitalizes all words/letters that are separated by a space.
        var_name = " ".join(var_name.split()).title()
        if "By" in var_name:
            var_name.replace("By", "by")
        if any(x.isupper() for x in var_name):
            for i in range(len(var_name)-1):
                if (var_name[i] and var_name[i+1].islower() and var_name[i-1].isspace() and len(var_name) == i+2) or (len(var_name) != i+2 and var_name[i+2].isspace() and (var_name[i-1].isspace())) or (var_name[i].isupper() and i == 0 and len(var_name) >= i+2 and var_name[i+2].isspace()) or (var_name[i-1].isspace() and var_name[i+2].isspace() and var_name[i].isupper()):
                    if var_name[i:i+2].lower() in self.twoLetterWords:
                        pass
                        if var_name[2] == " ":
                            pass
                        else:
                            var_name = var_name[:i] + var_name[i:i+1].lower() + var_name[i+1:i+2] + var_name[i+2:]
                    else:
                        var_name = var_name[:i+1] + var_name[i+1:i+2].capitalize() + var_name[i+2:]
        if var_value is not None:
            if isinstance(var_value, bool):
                var_value = str(var_value).lower()
            # Truncate the input value to 4 decimal places
            if isinstance(var_value, float) and len(str(var_value).split('.')[1]) > 4:
                var_value = round(var_value, 4)
                # Round up the last digit of the decimal place by one
                if str(var_value).split('.')[1][-1] != '0':
                    var_value = round(var_value + 0.0001, 4)
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
                self.label = tk.Label(self.frame, text=self.key, font='TkDefaultFont 16 bold')
                # If category is first category on UI, add spacing to the top, so it is below the save/open buttons
                if self.initialKey == key:
                    self.label.grid(row=self.row, column=0, sticky='W', pady=(75, 0))
                else:
                    self.label.grid(row=self.row, column=0, sticky='W', pady=(10, 0))
            self.create_UI(variables)
            self.row += 1

    def create_entries(self, var_value):
        if "[" in str(var_value) and "]" in str(var_value):
            # Separate into arrays/words and then use that as a multiplier
            lengthStr = int(len(str(var_value))*(1.4/2))
            self.entry = tk.Entry(self.frame, font='TkDefaultFont 12', textvariable=self.entry_var, width=8 + lengthStr)#(length*10))
            self.entry.grid(row=self.row + 1, column=1, padx=10, sticky='w')
        elif isinstance(var_value, str) and ("true" in var_value.lower() or "false" in var_value.lower()):
            self.entry_var = tk.BooleanVar(value=False)
            if "true" in var_value.lower():
                self.entry_var.set(True)
            checkbox = tk.Checkbutton(self.frame, variable=self.entry_var, onvalue=True, offvalue=False,
                                      command=self.checkbox_changed, indicatoron=False,
                                      bg='red', selectcolor='green', fg='green', activebackground='green', width=12)
            checkbox.grid(row=self.row + 1, column=1, padx=10, sticky='w')
        else:
            self.entry = tk.Entry(self.frame, font='TkDefaultFont 12', textvariable=self.entry_var, width=10)
            self.entry.grid(row=self.row + 1, column=1, padx=10, sticky='w')

    def create_toolTips(self, var_value):
        if "true" in var_value.lower() or "false" in var_value.lower() or "[" in var_value:
            if self.defaultVar_name in self.variableComments and self.variableComments[self.defaultVar_name][0] == self.defaultVar_name:
                comment = self.variableComments[self.defaultVar_name][1]
                if "#" in comment:
                    if len(comment) > 150:
                        array = comment.split(" ")
                        halfArray = len(array)//2
                        ToolTip(self.varLabel, " ".join(array[:halfArray])+'\n      '+" ".join(array[halfArray:]))
                    else:
                        ToolTip(self.varLabel, comment)
        else:
            if self.defaultVar_name in self.variableComments and self.variableComments[self.defaultVar_name][0] == self.defaultVar_name:
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
                print("There was a value that was too long to be inputted. \nVar Name =", var_name, "\nValue =", var_value)
                var_value = "(**ERROR STRING ENTRY TOO LONG**)"
            self.entry_var = tk.StringVar(value=str(var_value))
            # Create the Entry Boxes
            self.create_entries(var_value)
            self.entryArray[self.value] = self.entry_var
            # Create Variable Labels for Sub Tables

            # print(self.subTables.items())
            # print(type(self.subTables.items()))
            # if isinstance(self.subTables.items(), dict_items):
            #     print("dict")
            # if self.subTables.items() is []:
            #     print("pog")

            if var_name == "":
                self.varLabel = tk.Label(self.frame, text=self.key, font='TkDefaultFont 12')
                self.entry_varDict[self.originalVar_Name[self.key]] = self.entry_var
                self.labelNumber[self.value] = self.varLabel
            else:
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

    def _on_canvas_resize(self, event):
        # Update the scroll region to encompass the entire frame
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


windowDeleterSet()
TomlConfigUI()
