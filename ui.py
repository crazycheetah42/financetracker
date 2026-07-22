# Imports
from logic import read_file, write_file
import tkinter as tk
from tkinter import ttk # More modern widgets than regular tk
import sv_ttk # For dark theme and better looking widgets

# Setting up the window
root = tk.Tk()
root.title("Finance Tracker")
root.geometry("600x800")

style = ttk.Style(root)
style.configure("TFrame")
style.configure("TLabel")

heading = ttk.Label(root, text="Finance Tracker", font=("Fira Code Regular", 24))
heading.pack(pady=20)

input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

purpose_label = ttk.Label(input_frame, text="Expense/income description:")
purpose_label.pack(anchor="w")

purpose_input = tk.Entry(input_frame, width=40)
purpose_input.pack(pady=(5, 0))

amount_label = ttk.Label(input_frame, text="Amount:")
amount_label.pack(anchor="w", pady=(10, 0))
amount_input = tk.Entry(input_frame, width=40)
amount_input.pack(pady=(5, 0))

transaction_type = tk.StringVar(value="Expense")
income_toggle = tk.BooleanVar(value=False)

type_label = ttk.Label(input_frame, text="Type: Expense")
type_label.pack(anchor="w", pady=(10, 0))


def update_transaction_type():
    transaction_type.set("Income" if income_toggle.get() else "Expense")
    type_label.configure(text=f"Type: {transaction_type.get()}")


type_toggle = ttk.Checkbutton(
    input_frame,
    text="Income",
    variable=income_toggle,
    command=update_transaction_type,
)
type_toggle.pack(anchor="w", pady=(5, 0))


def submit_entry():
    amount = amount_input.get().strip()
    if amount.startswith(("+", "-")):
        amount = amount[1:]
    if transaction_type.get() == "Expense":
        amount = f"-{amount}"
    else:
        amount = f"+{amount}"
    write_file(purpose_input.get(), amount)


submit_btn = ttk.Button(input_frame, text="Submit", command=submit_entry)
submit_btn.pack(pady=10)

balance_label = ttk.Label(root, text="Balance: 0.00", font=("Fira Code Regular", 16))
balance_label.pack(pady=(10, 0))

history_label = ttk.Label(root, text="Finance History", font=("Fira Code Regular", 18))
history_label.pack(pady=10)

history_frame = ttk.Frame(root)
history_frame.pack(pady=10)

# Display the saved entries in a scrollable, read-only list.
history_frame.columnconfigure(0, weight=1)
history_frame.rowconfigure(0, weight=1)

history = ttk.Treeview(
    history_frame,
    columns=("description", "amount"),
    show="headings",
    height=20,
)
history.heading("description", text="Description")
history.heading("amount", text="Amount")
history.column("description", width=350, anchor="w")
history.column("amount", width=120, anchor="e")
history.grid(row=0, column=0, sticky="nsew")

history_scrollbar = ttk.Scrollbar(
    history_frame, orient="vertical", command=history.yview
)
history_scrollbar.grid(row=0, column=1, sticky="ns")
history.configure(yscrollcommand=history_scrollbar.set)

_history_signature = None


def _format_history(data):
    """Parse each ``description, amount`` line into table columns."""
    if data is None:
        return []
    if isinstance(data, dict):
        data = list(data.items())
    elif isinstance(data, str):
        data = data.splitlines()

    result = []
    for entry in data:
        if isinstance(entry, dict):
            description = entry.get("description", entry.get("purpose", ""))
            amount = entry.get("amount", "")
        elif isinstance(entry, (tuple, list)):
            description = entry[0] if entry else ""
            amount = entry[1] if len(entry) > 1 else ""
        else:
            description, separator, amount = str(entry).partition(",")
            if not separator:
                amount = ""
        result.append((str(description).strip(), str(amount).strip()))
    return result


def refresh_history():
    global _history_signature
    try:
        rows = _format_history(read_file())
        balance = 0.0
        for _, amount in rows:
            try:
                balance += float(amount.replace(",", "").strip())
            except (AttributeError, ValueError):
                continue
        balance_label.configure(text=f"Balance: {balance:.2f}")

        signature = tuple(rows)
        if signature != _history_signature:
            _history_signature = signature
            history.delete(*history.get_children())
            for index, row in enumerate(rows):
                history.insert("", "end", iid=str(index), values=row)
    except (OSError, ValueError, TypeError):
        # Keep the last valid display if the file is temporarily unavailable.
        pass
    root.after(17, refresh_history)  # approximately 60 updates per second


def edit_history(event):
    item = history.identify_row(event.y)
    column_id = history.identify_column(event.x)
    if not item or column_id not in ("#1", "#2"):
        return

    column = "description" if column_id == "#1" else "amount"
    bounds = history.bbox(item, column)
    if not bounds:
        return

    editor = ttk.Entry(history)
    editor.insert(0, history.set(item, column))
    editor.place(x=bounds[0], y=bounds[1], width=bounds[2], height=bounds[3])
    editor.focus_set()

    def save(_event=None):
        history.set(item, column, editor.get())
        editor.destroy()

    editor.bind("<Return>", save)
    editor.bind("<FocusOut>", save)


refresh_history()


sv_ttk.set_theme("dark")

def run_ui():
    root.mainloop()