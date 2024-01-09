# newAccount.py
import tkinter as tk
import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox
import hashlib
import json

# Database connection setup
with open("./assets/mongodb.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']
    
client = MongoClient(conn_str)
db = client['partnerlink']
users_col = db['users']

def hash_password(password):
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def add_new_user(name_entry, email_entry, password_entry, return_to_main):
    # Retrieve data from fields
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Check if the email already exists in the database
    if users_col.count_documents({"email": email}) == 0:
        if name and email and password:  # Ensure all fields are filled out
            # All fields are filled, create new user document
            new_user = {
                "name": name,
                "email": email,
                "passwordHash": hash_password(password)
            }
            users_col.insert_one(new_user)
            messagebox.showinfo("Success", "New user account created successfully.")
            return_to_main()  # Return to the main menu
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "An account with this email already exists.")

def create_new_account_form(root, return_to_main):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    entry_style = {"font": ("Roboto Medium", 20), "width": 300, "height": 40}

    # Create form elements\
    ctk.CTkLabel(background_frame, text="Create New User", font=("Roboto Medium", 40)).pack(pady=15)

    ctk.CTkLabel(background_frame, text="Name", font=("Roboto Medium", 25)).pack()
    name_entry = ctk.CTkEntry(background_frame, placeholder_text="Enter the name", **entry_style)
    name_entry.pack(pady=10)

    ctk.CTkLabel(background_frame, text="Email", font=("Roboto Medium", 25)).pack()
    email_entry = ctk.CTkEntry(background_frame, placeholder_text="Enter the email", **entry_style)
    email_entry.pack(pady=10)

    ctk.CTkLabel(background_frame, text="Password", font=("Roboto Medium", 25)).pack()
    password_entry = ctk.CTkEntry(background_frame, placeholder_text="Enter a password", show="*", **entry_style)
    password_entry.pack(pady=10)

    submit_button = ctk.CTkButton(background_frame, width=200, height=40, text="Create Account", command=lambda: add_new_user(name_entry, email_entry, password_entry, return_to_main), font=("Roboto Medium", 30), bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    submit_button.pack(pady=10)

    back_button = ctk.CTkButton(background_frame, width=200, height=40, text="Back", command=return_to_main, font=("Roboto Medium", 30), bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    back_button.pack(pady=10)

# Additional functionality as needed
