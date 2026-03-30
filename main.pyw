import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import encrypt_decrypt
import hashlib


PATH_FOR_USER = os.path.join(os.environ["APPDATA"], "PM", "passwords.txt")
os.makedirs(os.path.dirname(PATH_FOR_USER), exist_ok=True)

PATH_FOR_MASTER = os.path.join(os.environ["APPDATA"], "PM", "mastercode.txt")
os.makedirs(os.path.dirname(PATH_FOR_MASTER), exist_ok=True)

class EntryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.labelName = ctk.CTkLabel(self, corner_radius=10, text="USERNAME:")
        self.labelName.grid(row=0, column=0, padx=15, pady=10)
        self.entryName = ctk.CTkEntry(self, width=300, corner_radius=10)
        self.entryName.grid(row=0, column=1, padx=15, pady=10)
        
        self.labelPassword = ctk.CTkLabel(self, corner_radius=10, text="PASSWORD:")
        self.labelPassword.grid(row=1, column=0, padx=15, pady=15)
        self.entryPassword = ctk.CTkEntry(self, width=300, corner_radius=10, show="*")
        self.entryPassword.grid(row=1, column=1, padx=15, pady=15)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        WIDTH = 500
        HEIGHT = 280
        
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.title("Celil Selcuk's Password Manager")
        self.iconbitmap("images/lock.ico")
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        
        self.entry_frame = EntryFrame(self)
        self.entry_frame.grid(row=0, column=0, padx=15, pady=15, sticky = "ew", columnspan=2)
        
        self.buttonAdd = ctk.CTkButton(self, corner_radius=10, border_width=2, fg_color="#175CE6", hover_color="#316FE8", border_color="#636469", text="Add a password", command=self.add)
        self.buttonAdd.grid(row=2, column=0, padx=15, pady=8, sticky="we")

        self.buttonGet = ctk.CTkButton(self, corner_radius=10, border_width=2, fg_color="#175CE6", hover_color="#316FE8", border_color="#636469", text="Get a password", command=self.get)
        self.buttonGet.grid(row=2, column=1, padx=15, pady=8, sticky="we")

        self.buttonList = ctk.CTkButton(self, corner_radius=10, border_width=2, fg_color="#175CE6", hover_color="#316FE8", border_color="#636469", text="List all users", command=self.getlist)
        self.buttonList.grid(row=3, column=0, padx=15, pady=8, sticky="we")

        self.buttonUpdate = ctk.CTkButton(self, corner_radius=10, border_width=2, fg_color="#175CE6", hover_color="#316FE8", border_color="#636469", text="Update user's password", command=self.update)
        self.buttonUpdate.grid(row=4, column=0, padx=15, pady=8, sticky="we")

        self.buttonDelete = ctk.CTkButton(self, corner_radius=10, border_width=2, fg_color="#175CE6", hover_color="#316FE8", border_color="#636469", text="Delete a user", command=self.delete)
        self.buttonDelete.grid(row=3, column=1, padx=15, pady=8, sticky="we")

        self.buttonUpdateMC = ctk.CTkButton(self, corner_radius=10, border_width=2, fg_color="#175CE6", hover_color="#316FE8", border_color="#636469", text="Update mastercode", command=self.change_mastercode)
        self.buttonUpdateMC.grid(row=4, column=1, padx=15, pady=8, sticky="we")

        try:
            if os.path.getsize(PATH_FOR_MASTER) == 0:
                self.ask_set_mastercode()
            else:
                self.authenticate()
        except FileNotFoundError:
            self.ask_set_mastercode()

    def file_content_to_dict(self):
        up_pair = {}
        with open(PATH_FOR_USER, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().split()
                up_pair.update({line[0]: [line[1],line[2],line[3]]})
        return up_pair
    
    @staticmethod
    def hash_mc(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def retreive_hashed_mc():
        with open(PATH_FOR_MASTER, "r") as f:
            return f.read()
    
    def ask_set_mastercode(self):
        while True:
            dialog = ctk.CTkInputDialog(text="Make a mastercode to use when accessing passwords:", title="MASTERCODE CREATION", button_fg_color="#175CE6", button_hover_color="#316FE8")
            res = dialog.get_input()
            if res is None:
                exit()
            if res != "" and " " not in res:
                break
            messagebox.showwarning("WARNING", "Please enter a mastercode and don't use any spaces.")
        mc = self.hash_mc(res)
        with open(PATH_FOR_MASTER, "w") as f:
            f.write(mc)
        messagebox.showinfo("SUCCESS", "Mastercode successfully created!")

    def ask_check_mastercode(self):
        dialog = ctk.CTkInputDialog(text="Enter your mastercode so we know it's you.", title = "AUTHENTICATION", button_fg_color="#175CE6", button_hover_color="#316FE8")
        res = dialog.get_input()
        if res is not None:
            return self.hash_mc(res) == self.retreive_hashed_mc()
        else:
            exit()

    def authenticate(self):
        valid = self.ask_check_mastercode()
        attempts = 0
        while not valid:
            attempts+=1
            if attempts >= 3:
                exit()
            messagebox.showwarning("WARNING", f"That's not the password, {3-attempts} attempts left")
            valid = self.ask_check_mastercode()

    def change_mastercode(self):
        entered = False
        while True:
            dialog = ctk.CTkInputDialog(text="Enter your new mastercode", title="OVERWRITE MASTERCODE", button_fg_color="#175CE6", button_hover_color="#316FE8")
            res = dialog.get_input()
            if res is None:
                break
            if res != "" and " " not in res:
                entered = True
                break
            messagebox.showwarning("WARNING", "Enter a new mastercode without spaces.")
        if entered:
            with open(PATH_FOR_MASTER, "w") as master_f:
                master_f.write(self.hash_mc(res))
            messagebox.showinfo("SUCCESS", "You have updated your mastercode. Remember it!")

    def add(self):
        username = self.entry_frame.entryName.get()
        password = self.entry_frame.entryPassword.get()

        if not os.path.isfile(PATH_FOR_USER):
            open(PATH_FOR_USER, "w").close()

        try:
            credentials = self.file_content_to_dict()
            if (username != "" and " " not in username) and (password != "" and " " not in password):
                if username not in credentials:
                    with open(PATH_FOR_USER, "a") as password_file:
                        encrypted_password, c, s = encrypt_decrypt.encrypt(password)
                        password_file.write(f"{username} {encrypted_password} {c} {s}\n")
                    messagebox.showinfo("SUCCESS", "Info has been added.")
                    self.entry_frame.entryName.delete(0, tk.END)
                    self.entry_frame.entryPassword.delete(0, tk.END)
                else:
                    messagebox.showerror("ERROR", f"{username} has been used before.")
            else:
                messagebox.showwarning("WARNING", "Make sure both fields are not empty and don't contain spaces.")
        except Exception as e:
            messagebox.showerror("ERROR", e)

    def get(self):
        username = self.entry_frame.entryName.get()
        if username != "":
            try:
                credentials = self.file_content_to_dict()
            except FileNotFoundError:
                messagebox.showerror("ERROR", "No passwords saved yet.")
                return
                        
            if username in credentials:
                password = encrypt_decrypt.decrypt(credentials[username][0], int(credentials[username][1]), int(credentials[username][2]))
                messagebox.showinfo("SUCCESS", f"The password for {username} is {password}")
                self.entry_frame.entryName.delete(0, tk.END)
                self.entry_frame.entryPassword.delete(0, tk.END)
            else:
                messagebox.showerror("ERROR", "That username has no password associated with it.")
        else:
            messagebox.showwarning("WARNING", "Username must not be empty.")
    
    def getlist(self):
        try:
            credentials = self.file_content_to_dict()
        except FileNotFoundError:
            messagebox.showerror("ERROR", "No passwords saved yet.")
            return

        if not credentials:
            messagebox.showerror("ERROR", "The passwords file is empty.")
        else:
            res = ""
            for i,username in enumerate(credentials):
                res += f"Entry {i+1}: {username}\n"
            messagebox.showinfo("Current list of users", res)
        
    def update(self):
        username = self.entry_frame.entryName.get()
        new_password = self.entry_frame.entryPassword.get()
        updated = False
        if (username != "" and " " not in username) and (new_password != "" and " " not in new_password):
            new_password_e, c, s = encrypt_decrypt.encrypt(new_password)
            try:
                with open(PATH_FOR_USER, "r") as password_file:
                    pairs = password_file.readlines()                    
                with open(PATH_FOR_USER, "w") as password_file:
                    for pair in pairs:
                        if pair.split()[0] == username:
                            new_pair = pair.split()
                            new_pair[1], new_pair[2], new_pair[3] = new_password_e, str(c), str(s)
                            new_line = " ".join(new_pair)
                            password_file.write(new_line + "\n")
                            updated = True
                        else:
                            password_file.write(pair)
                if updated:
                    messagebox.showinfo("SUCCESS", f"{username}'s password has been updated.")
                    self.entry_frame.entryName.delete(0, tk.END)
                    self.entry_frame.entryPassword.delete(0, tk.END)
                else:
                    messagebox.showerror("ERROR", f"{username} doesn't exist")
            except FileNotFoundError:
                messagebox.showerror("ERROR", "No passwords saved yet.")
            except Exception as e:
                messagebox.showerror("ERROR", e)
        else:
            messagebox.showwarning("WARNING", "Make sure both fields are not empty and don't contain spaces.")
            
    def delete(self):
        username = self.entry_frame.entryName.get()
        if username != "":
            try:
                with open(PATH_FOR_USER, "r") as password_file:
                    pairs = password_file.readlines()
                    
                with open(PATH_FOR_USER, "w") as password_file:
                    deleted = False
                    if pairs:
                        for pair in pairs:
                            if pair.split()[0] != username:
                                password_file.write(pair)
                            else:
                                deleted = True
                        if deleted:
                            messagebox.showinfo("SUCCESS", f"Deleted {username} and its password.")
                            self.entry_frame.entryName.delete(0, tk.END)
                            self.entry_frame.entryPassword.delete(0, tk.END)
                        else:
                            messagebox.showerror("ERROR", f"{username} does not exist.")
                        
                    else:
                        messagebox.showerror("ERROR", f"The passwords file is empty.")
            except FileNotFoundError:
                messagebox.showerror("ERROR", "No passwords saved yet.")
        else:
            messagebox.showwarning("WARNING", "Username must not be empty.")

ctk.set_appearance_mode("system")
app = App()
app.mainloop()
