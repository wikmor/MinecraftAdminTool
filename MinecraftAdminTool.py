import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox

import yaml


class MinecraftAdminTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minecraft Admin Tool")
        self.geometry("600x400")

        self.content_analyzer_var = tk.BooleanVar()
        self.content_analyzer_checkbox = tk.Checkbutton(
            self, text="Enable Content Analyzer", variable=self.content_analyzer_var,
            command=self.toggle_content_analyzer
        )
        self.content_analyzer_checkbox.pack(pady=10)

        self.discord_integration_var = tk.BooleanVar()
        self.discord_integration_checkbox = tk.Checkbutton(
            self, text="Enable Discord Integration", variable=self.discord_integration_var,
            command=self.toggle_discord_integration
        )
        self.discord_integration_checkbox.pack(pady=10)

        self.show_db_button = tk.Button(self, text="Show Database Table", command=self.show_database_table)
        self.show_db_button.pack(pady=10)

        self.browse_formats_button = tk.Button(self, text="Browse YAML Files in /formats",
                                               command=self.browse_yaml_files)
        self.browse_formats_button.pack(pady=10)

        self.yaml_file_path = "/home/wiktor/servers/1.21/plugins/LPC-Pro/config.yml"

    def toggle_content_analyzer(self):
        self.update_yaml("content_analyzer", self.content_analyzer_var.get())

    def toggle_discord_integration(self):
        self.update_yaml("discord_integration", self.discord_integration_var.get())

    def update_yaml(self, key, value):
        try:
            with open(self.yaml_file_path, 'r') as file:
                data = yaml.safe_load(file)

            data[key] = value

            with open(self.yaml_file_path, 'w') as file:
                yaml.dump(data, file)

            messagebox.showinfo("Success", f"{key} has been updated to {value}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update YAML file: {str(e)}")

    def show_database_table(self):
        db_window = tk.Toplevel(self)
        db_window.title("Database Table")
        db_window.geometry("600x400")

        try:
            connection = sqlite3.connect("/home/wiktor/servers/1.21/plugins/LPC-Pro/data.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM messages")
            rows = cursor.fetchall()

            text_widget = tk.Text(db_window)
            text_widget.pack(expand=True, fill="both")
            for row in rows:
                text_widget.insert(tk.END, f"{row}\n")

            connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load database: {str(e)}")

    def browse_yaml_files(self):
        default_directory = os.path.join("/home/wiktor/servers/1.21/plugins/LPC-Pro/", "formats")
        directory = filedialog.askdirectory(title="Select /formats Directory", initialdir=default_directory)
        if directory:
            yaml_files = [f for f in os.listdir(directory) if f.endswith('.yml') or f.endswith('.yaml')]
            if not yaml_files:
                messagebox.showinfo("Info", "No YAML files found in the selected directory.")
                return

            yaml_window = tk.Toplevel(self)
            yaml_window.title("YAML Files")
            yaml_window.geometry("600x400")

            text_widget = tk.Text(yaml_window)
            text_widget.pack(expand=True, fill="both")

            for file_name in yaml_files:
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()
                    text_widget.insert(tk.END, f"--- {file_name} ---\n{content}\n\n")


if __name__ == "__main__":
    app = MinecraftAdminTool()
    app.mainloop()
