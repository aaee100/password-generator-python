

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import secrets
import string


def generate_passwords():
    try:
        length = int(length_var.get())
        count = int(count_var.get())
        mode = letter_case_var.get()
        capitals = int(capitals_var.get()) if mode == "mixed" else 0

        if length <= 0 or count <= 0:
            raise ValueError("Length and count must be greater than zero.")

        if mode == "mixed" and not 0 <= capitals <= length:
            raise ValueError(
                "Uppercase count must be between 0 and the password length."
            )

        symbols = [
            symbol for symbol, var in symbol_vars.items() if var.get()
        ]
        use_letters = include_letters_var.get()
        use_numbers = include_numbers_var.get()

        if not use_letters and not use_numbers and not symbols:
            messagebox.showwarning(
                "Selection Error",
                "Please select at least one character type."
            )
            return

        if mode == "mixed" and capitals > 0 and not use_letters:
            messagebox.showerror(
                "Selection Error",
                "Enable 'Include Letters' to add uppercase letters."
            )
            return

        required = capitals + len(symbols)

        if required > length:
            messagebox.showerror(
                "Length Error",
                "The uppercase-letter and selected-symbol requirements "
                "exceed the password length."
            )
            return

        # Build the character pool.
        pool = ""

        if use_letters:
            if mode == "lower":
                pool += string.ascii_lowercase
            elif mode == "upper":
                pool += string.ascii_uppercase
            else:
                pool += string.ascii_lowercase

        if use_numbers:
            pool += string.digits

        pool += "".join(symbols)

        results = []

        for _ in range(count):
            chars = []

            # Add the required uppercase letters.
            if mode == "mixed":
                chars.extend(
                    secrets.choice(string.ascii_uppercase)
                    for _ in range(capitals)
                )

            # Include every selected symbol at least once.
            chars.extend(symbols)

            # Fill the remaining positions.
            remaining = length - len(chars)

            if remaining > 0:
                if not pool:
                    messagebox.showerror(
                        "Character Pool Error",
                        "No characters are available to fill the password."
                    )
                    return

                chars.extend(
                    secrets.choice(pool)
                    for _ in range(remaining)
                )

            # Shuffle the password characters.
            secrets.SystemRandom().shuffle(chars)

            results.append("".join(chars))

        # Display each password on a separate line.
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "\n".join(results))
        output_box.config(state="disabled")

    except ValueError as error:
        messagebox.showerror(
            "Input Error",
            str(error) or "Please enter valid numbers."
        )


# --------------------------------------------------
# GUI setup
# --------------------------------------------------

root = tk.Tk()
root.title("Password Generator")
root.geometry("450x600")
root.resizable(True, True)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")


# --------------------------------------------------
# Password length
# --------------------------------------------------

ttk.Label(
    frame,
    text="Password Length:"
).pack(anchor="w")

length_var = tk.StringVar(value="12")

ttk.Entry(
    frame,
    textvariable=length_var
).pack(fill="x")


# --------------------------------------------------
# Number of passwords
# --------------------------------------------------

ttk.Label(
    frame,
    text="Number of Passwords:"
).pack(anchor="w", pady=(10, 0))

count_var = tk.StringVar(value="5")

ttk.Entry(
    frame,
    textvariable=count_var
).pack(fill="x")


# --------------------------------------------------
# Letter case selection
# --------------------------------------------------

ttk.Label(
    frame,
    text="Letter Case:"
).pack(anchor="w", pady=(10, 0))

letter_case_var = tk.StringVar(value="mixed")

ttk.Radiobutton(
    frame,
    text="Lowercase Only",
    variable=letter_case_var,
    value="lower"
).pack(anchor="w")

ttk.Radiobutton(
    frame,
    text="Uppercase Only",
    variable=letter_case_var,
    value="upper"
).pack(anchor="w")

ttk.Radiobutton(
    frame,
    text="Mixed Case",
    variable=letter_case_var,
    value="mixed"
).pack(anchor="w")


# --------------------------------------------------
# Uppercase count
# --------------------------------------------------

ttk.Label(
    frame,
    text="Number of Uppercase Letters (if mixed):"
).pack(anchor="w")

capitals_var = tk.StringVar(value="2")

ttk.Entry(
    frame,
    textvariable=capitals_var
).pack(fill="x")


# --------------------------------------------------
# Include numbers
# --------------------------------------------------

include_numbers_var = tk.BooleanVar(value=True)

ttk.Checkbutton(
    frame,
    text="Include Numbers (0-9)",
    variable=include_numbers_var
).pack(anchor="w", pady=(10, 0))


# --------------------------------------------------
# Include letters
# --------------------------------------------------

include_letters_var = tk.BooleanVar(value=True)

ttk.Checkbutton(
    frame,
    text="Include Letters",
    variable=include_letters_var
).pack(anchor="w")


# --------------------------------------------------
# Symbol selection
# --------------------------------------------------

ttk.Label(
    frame,
    text="Select Symbols to Include:"
).pack(anchor="w", pady=(10, 0))

symbol_frame = ttk.Frame(frame)
symbol_frame.pack(fill="x")

symbol_vars = {}

symbol_list = list("!@#$%^&*()_+-=[]{}|;:,.<>?")

columns = 6

for index, symbol in enumerate(symbol_list):
    var = tk.BooleanVar()
    symbol_vars[symbol] = var

    checkbox = ttk.Checkbutton(
        symbol_frame,
        text=symbol,
        variable=var
    )

    checkbox.grid(
        row=index // columns,
        column=index % columns,
        sticky="w"
    )


# --------------------------------------------------
# Generate button
# --------------------------------------------------

ttk.Button(
    frame,
    text="Generate Passwords",
    command=generate_passwords
).pack(pady=15)


# --------------------------------------------------
# Output area
# --------------------------------------------------

output_box = scrolledtext.ScrolledText(
    root,
    height=10,
    wrap=tk.WORD,
    state="disabled"
)

output_box.pack(
    padx=10,
    fill="both",
    expand=True
)


# --------------------------------------------------
# Start application
# --------------------------------------------------

root.mainloop()
