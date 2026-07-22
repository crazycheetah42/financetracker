# Imports
from logic import read_file, write_file
import tkinter as tk
from tkinter import ttk # More modern widgets than regular tk

# Setting up the window
root = tk.Tk()
root.title("Finance Tracker")
root.geometry("600x800")
root.configure(bg="white")

style = ttk.Style(root)
style.configure("TFrame", background="white")
style.configure("TLabel", background="white", foreground="black")

heading = ttk.Label(root, text="Finance Tracker", font=("Fira Code Regular", 24))
heading.pack(pady=20)

input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

purpose_label = ttk.Label(input_frame, text="Expense/income description:")
purpose_label.pack(anchor="w")

purpose_input = tk.Entry(input_frame, width=40, bg="white")
purpose_input.pack(pady=(5, 0))

def run_ui():
    root.mainloop()