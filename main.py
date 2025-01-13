import tkinter as tk
from tkinter import ttk
import pyperclip

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Query builder")

        self.drop_var = tk.StringVar()
        self.drop_var.set("ID")  # Default value

        # Define output format for each dropdown option
        self.format_strings = {
            'UPC': "UPC in ({})",
            'RETAILER STORE': "CAST([Desc2] As varchar(1000)) IN ({})",
            'DBKEY': "DBKey IN ({})",
            'RESET TIMING AND RETAILER STORE': "CAST([Desc10] As varchar(1000)) = N'{}' AND CAST([Desc2] As varchar(1000)) IN ({})",
            'STATE': "CAST([Desc5] As varchar(1000)) IN ({})",
            'TDLINX': "CAST([Desc21] As varchar(1000)) IN ({})",
            'ID': "ID in ({})",
            'OTHEROPTION': "OTHEROPTION in ({})"
        }

        self.year_var = tk.StringVar()
        self.year_var.set("2022")  # Default year

        self.season_var = tk.StringVar()
        self.season_var.set("SPRING")  # Default season

        self.init_ui()

    def init_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.drop = ttk.Combobox(self.root, textvariable=self.drop_var, width=50)
        self.drop['values'] = (
            'ID', 'UPC', 'OTHEROPTION', 'RETAILER STORE', 'DBKEY', 'RESET TIMING AND RETAILER STORE', 'STATE', 'TDLINX'
        )
        self.drop.grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.drop.bind("<<ComboboxSelected>>", self.update_ui)

        self.year_drop = ttk.Combobox(self.root, textvariable=self.year_var, state='disabled', width=50)
        self.year_drop['values'] = list(range(2000, 2031))  # Years from 2000 to 2030
        self.year_drop.grid(column=0, row=1, padx=10, pady=5, sticky="w")

        self.season_drop = ttk.Combobox(self.root, textvariable=self.season_var, state='disabled', width=50)
        self.season_drop['values'] = ('SPRING', 'SUMMER', 'FALL')
        self.season_drop.grid(column=0, row=2, padx=10, pady=5, sticky="w")

        self.text_frame = tk.Frame(self.root)
        self.text_frame.grid(column=1, row=0, rowspan=3, padx=10, pady=5, sticky="nsew")

        self.text = tk.Text(self.text_frame, height=20, width=40)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.button = tk.Button(self.root, text="Copy to clipboard", command=self.copy_to_clipboard, width=30)
        self.button.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text, width=30)
        self.clear_button.grid(column=0, row=4, columnspan=2, padx=10, pady=5)

    def update_ui(self, event):
        if self.drop_var.get() == 'RESET TIMING AND RETAILER STORE':
            self.year_drop.config(state='normal')
            self.season_drop.config(state='normal')
        else:
            self.year_drop.config(state='disabled')
            self.season_drop.config(state='disabled')
        # Clear the text input
        self.text.delete("1.0", "end")

    def clear_text(self):
        self.text.delete("1.0", "end")

    def copy_to_clipboard(self):
        values = self.text.get("1.0", "end-1c").split('\n')  # Split input by new lines
        values = [val for val in values if val]  # Remove empty strings
        values_str = ','.join(f"'{val}'" for val in values)  # Format as strings and join

        if self.drop_var.get() == 'RESET TIMING AND RETAILER STORE':
            result = self.format_strings[self.drop_var.get()].format(
                f"{self.year_var.get()} {self.season_var.get()}", values_str
            )
        else:
            result = self.format_strings[self.drop_var.get()].format(values_str)

        pyperclip.copy(result)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
