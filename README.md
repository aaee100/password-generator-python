
# Password Generator

A desktop password generator built with **Python** and **Tkinter**. It creates multiple passwords using Python's `secrets` module for security-focused random generation.

## Features

- Generate multiple passwords with a chosen length
- Lowercase-only, uppercase-only, and mixed-case letter modes
- Choose the required uppercase-letter count in mixed-case mode
- Include or exclude numbers
- Select individual symbols; every selected symbol appears at least once in each password
- Securely shuffle generated characters
- Display passwords locally without saving or transmitting them
- Uses only the Python standard library

## Requirements and installation

- Python 3.7 or newer
- Tkinter (included with many Python installations; some Linux distributions package it separately)

Clone the repository and run the application:

```bash
git clone https://github.com/yourusername/password-generator-python.git
cd password-generator-python
python password_generator.py
```

No `pip install` step is required.

## How to use

1. Enter the password length and number of passwords.
2. Choose lowercase-only, uppercase-only, or mixed-case mode.
3. In mixed-case mode, set the number of uppercase letters.
4. Choose whether to include letters and numbers.
5. Select any symbols that should appear in every password.
6. Click **Generate Passwords**.

## Character-selection behavior

The letter-case setting controls the case of letters; it does not prevent the other enabled character types from being used.

- **Lowercase Only:** letter characters are lowercase. Enabled numbers can be selected for remaining positions, and every selected symbol is included at least once.
- **Uppercase Only:** letter characters are uppercase. Enabled numbers can be selected for remaining positions, and every selected symbol is included at least once.
- **Mixed Case:** the requested uppercase letters are added first. Remaining letter positions use lowercase letters; enabled numbers and selected symbols may also be used.

**Include Letters** controls whether letters are available, and **Include Numbers** adds digits to the fill pool. Each selected symbol is guaranteed at least once. Numbers are eligible for selection but are not guaranteed to appear in every password.

In mixed-case mode, the uppercase count must be between zero and the password length. If uppercase letters are requested, **Include Letters** must be enabled.

## Input validation

The application checks that password length and password count are positive integers, that the mixed-case uppercase count is within the password length, that at least one character type is enabled, and that required uppercase letters and selected symbols fit in the requested length.

## Secure random generation

The application uses Python's built-in `secrets` module rather than `random`. Generated passwords are displayed locally and are not written to a file or sent to an external service. Avoid sharing generated passwords or storing them in an unprotected location.

## Example configuration

```text
Password Length: 16
Number of Passwords: 5
Letter Case: Mixed Case
Uppercase Letters: 3
Include Letters: Yes
Include Numbers: Yes
Symbols: ! @ # $
```

Each result contains at least three uppercase letters and at least one of each selected symbol. Remaining characters are selected from the enabled character pool.

## Project structure

```text
password-generator-python/
├── password_generator.py
├── screenshots/
│   └── main-window.png
├── requirements.txt
├── .gitignore
└── README.md
```

## Possible future improvements

- Copy passwords to the clipboard
- Add a password-strength estimate
- Add presets and custom symbol sets
- Exclude ambiguous characters
- Add a button to clear the output

## License

This project is available for educational and portfolio purposes.
