import tkinter as tk
import customtkinter as ctk
from pymongo import MongoClient
import json

# Database connection setup
with open("./assets/variables.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']
    
client = MongoClient(conn_str)
db = client['partnerlink']
users_col = db['users']

import hashlib

def hash_password(password):
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def update_account_info(user_id, name_entry, email_entry, password_entry):
    # Retrieve data from fields
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Prepare the update dictionary
    update_data = {"name": name, "email": email}

    # Only update the password if a new one has been entered
    if password:
        password_hash = hash_password(password)
        update_data['passwordHash'] = password_hash

    # Update the user document in MongoDB using the user_id
    users_col.update_one({"_id": user_id}, {"$set": update_data})

    # Provide feedback or redirect to a confirmation page
    print("Account updated successfully.")


def create_account_settings_form(root, user_id, return_to_main):

    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    # Fetch the current user information
    user_info = users_col.find_one({"_id": user_id})

    # Define common styles for widgets
    label_style = {"font": ("Roboto Medium", 25)}
    entry_style = {"font": ("Roboto Medium", 20), "width": 300, "height": 40}
    button_style = {"font": ("Roboto Medium", 30), "bg_color": "transparent", "fg_color": "black", "hover_color": "#444444", "text_color": "white", "width": 200, "height": 40}

    # Create form elements with styles
    # Name label and entry
    ctk.CTkLabel(background_frame, text="Account Settings", font=("Roboto Medium",40)).pack(pady=15)

    ctk.CTkLabel(background_frame, text="Name:", **label_style).pack()
    name_entry = ctk.CTkEntry(background_frame, placeholder_text="Enter your name", **entry_style)
    name_entry.insert(0, user_info['name'])  # Pre-fill with current name
    name_entry.pack(pady=10)

    # Email label and entry
    email_label = ctk.CTkLabel(background_frame, text="Email:", **label_style)
    email_label.pack()
    email_entry = ctk.CTkEntry(background_frame, placeholder_text="Enter your email", **entry_style)
    email_entry.insert(0, user_info['email'])  # Pre-fill with current email
    email_entry.pack(pady=10)

    # Password label and entry
    password_label = ctk.CTkLabel(background_frame, text="Password (leave blank to keep current):", font=("Roboto Medium", 20))
    password_label.pack()
    password_entry = ctk.CTkEntry(background_frame, placeholder_text="Enter a new password", show="*", **entry_style)
    password_entry.pack(pady=10)

    # Submit and Back buttons
    submit_button = ctk.CTkButton(background_frame, text="Submit", command=lambda: update_account_info(user_id, name_entry, email_entry, password_entry), **button_style)
    submit_button.pack(pady=10)
    back_button = ctk.CTkButton(background_frame, text="Back", command=return_to_main, **button_style)
    back_button.pack(pady=10)


# Additional functions and logic as needed
