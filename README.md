# 🔐 Celil Selcuk's Password Manager

![Password Manager Demo](PM.gif) A simple desktop password manager I built in Python, with the GUI made using the customTkinter library. Stores your passwords encrypted so they're never saved in plaintext, and protected behind a master code so only you can access it.

---

## Getting Started

You'll need Python 3.10+ installed. Then just install the one dependency:

```bash
pip install customtkinter
```

Then run:

```bash
python main.py
```
For the best experience, rename `main.py` to `main.pyw` and create a desktop shortcut so you can open it without a terminal. To do this, right click `main.pyw` → Send to → Desktop (create shortcut). Double clicking the shortcut will launch the app directly with no console window. Through the shortcut's properties, you can edit its icon on the desktop.

First time you open it, you'll be asked to create a mastercode. You'll need this every time you open the app, so don't forget it — there's no way to recover it.

---

## Authentication

Every time you launch the app you'll be prompted to enter your mastercode before anything is accessible. You get 3 attempts before the app closes. If you cancel the prompt at any point, the app closes.

If you want to change your mastercode, use the **Update mastercode** button inside the app. You'll be asked for a new one and it'll overwrite the old one immediately.

---

## How to Use

Type a username into the username field and a password into the password field, then hit the button for what you want to do.

**Add a password** — saves a new username and password pair. Won't let you add the same username twice.

**Get a password** — type in a username and it'll show you the password stored for it.

**Update user's password** — type in an existing username and a new password to replace the old one.

**List all users** — shows every username you've saved.

**Delete a user** — removes a username and its password completely.

**Update mastercode** — lets you overwrite your current mastercode with a new one.

---

## A Few Things to Note

- Usernames and passwords can't contain spaces
- Your passwords and mastercode are stored in your AppData folder, not in the project folder
- The mastercode is hashed — if you forget it, delete `mastercode.txt` from `AppData/Roaming/PM/` and you'll be prompted to create a new one on next launch
- Passwords are encrypted using a custom algorithm inspired by card deck shuffling. A character set is shuffled using two randomly generated keys and by interleaving and cutting the decks according to these keys, producing a unique substitution mapping that changes with every character encrypted. The two keys are stored alongside the ciphertext and are required to decrypt — without them the password can't be recovered
---

## Project Structure

```
Password Manager/
├── main.py              # Main app
├── encrypt_decrypt.py   # Handles encryption and decryption of user's passwords
├── images/
│   └── lock.ico         # App icon
```

Data is stored at:
```
C:\Users\<User>\AppData\Roaming\PM\
├── passwords.txt
└── mastercode.txt
```
