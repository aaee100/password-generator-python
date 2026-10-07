import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import secrets
import string


def generate_passwords():
    try:
        length = int(length_var.get())
        count = int(count_var.get())
        letter_case = letter_case_var.get()
        num_capitals = int(capitals_var.get()) if letter_case == "mixed" else 0

        if length <= 0 or count <= 0:
            raise ValueError("Length and count must be greater than zero.")

        if letter_case == "mixed" and num_capitals < 0:
            raise ValueError("Uppercase count cannot be negative.")

        # Collect selected symbols.
        selected_symbols = [
            symbol for symbol, var in symbol_vars.items()
            if var.get()
        ]

        num_symbols = len(selected_symbols)

        include_letters = include_letters_var.get()
        include_numbers = include_numbers_var.get()

        if not include_letters and not include_numbers and not selected_symbols:
            messagebox.showwarning(
                "Selection Error",
                "Please select at least one character type."
            )
            return

        # Check whether the required characters fit in the password.
        required_length = num_capitals + num_symbols

        if required_length > length:
            messagebox.showerror(
                "Length Error",
                "Too many required characters for the selected password length."
            )
            return

        passwords = []

        for _ in range(count):
            password_chars = []

            # Add required uppercase letters.
            if letter_case == "mixed":
                password_chars.extend(
                    secrets.choice(string.ascii_uppercase)
                    for _ in range(num_capitals)
                )

            elif letter_case == "upper":
                password_chars.extend(
                    secrets.choice(string.ascii_uppercase)
                    for _ in range(length)
                )

            elif letter_case == "lower":
                password_chars.extend(
                    secrets.choice(string.ascii_lowercase)
                    for _ in range(length)
                )

            # Add at least one of every selected symbol.
            if selected_symbols:
                password_chars.extend(selected_symbols)

            # If the password is already full, no more characters are needed.
            remaining_length = length - len(password_chars)

            if remaining_length > 0:

                # Build the pool of characters used to fill the password.
                char_pool = ""

                if include_letters:
                    if letter_case == "lower":
                        char_pool += string.ascii_lowercase

                    elif letter_case == "upper":
                        char_pool += string.ascii_uppercase

                    elif letter_case == "mixed":
                        char_pool += string.ascii_lowercase

                if include_numbers:
                    char_pool += string.digits

                if selected_symbols:
                    char_pool += "".join(selected_symbols)

                if not char_pool:
                    messagebox.showerror(
                        "Character Pool Error",
                        "Character pool is empty. Check your selections."
                    )
                    return

                # Fill the remaining password characters securely.
                password_chars.extend(
                    secrets.choice(char_pool)
                    for _ in range(remaining_length)
                )

            # Securely shuffle the characters.
            secrets.SystemRandom().shuffle(password_chars)

            password = "".join(password_chars)
            passwords.append(password)

        # Display generated passwords.
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "\n".join(passwords))
        output_box.config(state="disabled")

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers for length, count, "
            "and uppercase letters."
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

symbol_list = list("!@#$%^&*()_+-=[]{}|;:,.<>?")

symbol_vars = {}

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