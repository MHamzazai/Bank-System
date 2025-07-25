# Bank Management System - Python (Console Based)

## Overview

This is a console-based Bank Management System written in Python. It allows users to create accounts, log in, and perform basic banking operations like checking balance, depositing funds, withdrawing money, and using fast cash features. User data is stored and managed using a `users.json` file.

## Features

* Create a new account with name, password, and initial balance.
* Log in with existing account credentials.
* Deposit money and update balance.
* Withdraw money with balance validation.
* Fast cash withdrawals from preset amounts.
* Check current account balance and last activity time.
* Secure login and signup with input validation.

## Folder Structure

```
├── main.py              # Entry point of the application
├── users.json           # Stores user data persistently (auto-generated)
└── README.md            # Documentation file
```

## Getting Started

### Requirements

* Python 3.8+
* No external libraries required (only built-in modules)

### How to Run

1. Save the script to a file, e.g., `main.py`
2. Open your terminal or command prompt.
3. Run the application:

   ```bash
   python main.py
   ```

## Usage

Upon launching:

1. Choose to either log in or sign up.

2. If signing up, you will:

   * Enter a valid name (letters only, min. 3 characters).
   * Set a password (4–10 characters).
   * Set an initial balance or default to 0.

3. Once logged in, you can:

   * Check balance
   * Deposit money
   * Withdraw money
   * Use fast cash options
   * Exit the system

## Data Persistence

All user actions are recorded in the `users.json` file, including:

* Signup and login records
* Deposits and withdrawals
* Fast cash transactions

The JSON file uses the following structure:

```json
{
  "Signups": [ ... ],
  "Logins": [ ... ],
  "Deposits": [ ... ],
  "WithDrawals": [ ... ],
  "FastCash": [ ... ]
}
```

## Code Structure

* `main()` — Main program flow.
* `CheckLogin` — Handles login/signup prompt.
* `UserDetails` — Manages user credentials and account creation.
* `ConvertAndSave` — Saves login/signup records.
* `Deposit`, `Withdrawal`, `FastCash` — Handle financial operations.
* `Bank` — Central interface class for performing actions.
* `LoadAndSaveDataMixin` — Shared methods for reading/writing `users.json`.

## Notes

* All user names must contain only letters.
* Passwords must be unique across accounts.
* The application limits login attempts and introduces a 10-second cooldown for failed attempts.

## License

This project is open source and free to use.

---

> Developed by M. Hamza | Bank System Project in Python | Console Application
