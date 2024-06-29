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
schools_col = db['schools']

def hash_password(password):
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def validate_school_code(school, code, status_label):
    school_doc = schools_col.find_one({"school": school})
    if school_doc and school_doc['code'] == code:
        status_label.configure(text="School code is correct", text_color="green")
        return True
    else:
        status_label.configure(text="Incorrect school code", text_color="red")
        return False

def add_new_user(name_entry, email_entry, password_entry, school_entry, code_entry, status_label, return_to_main):
    # Retrieve data from fields
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    school = school_entry.get()
    code = code_entry.get()

    # Validate the school code
    if not validate_school_code(school, code, status_label):
        return

    # Check if the email already exists in the database
    if users_col.count_documents({"email": email}) == 0:
        if name and email and password and school and code:  # Ensure all fields are filled out
            # All fields are filled, create new user document
            new_user = {
                "name": name,
                "email": email,
                "passwordHash": hash_password(password),
                "school": school
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

    # Create form elements
    ctk.CTkLabel(background_frame, text="Create New Account", font=("Roboto Medium", 40)).pack(pady=15)

    form_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    form_frame.pack(pady=10)

    # Name field
    name_label = ctk.CTkLabel(form_frame, text="Name", font=("Roboto Medium", 25))
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    name_entry = ctk.CTkEntry(form_frame, placeholder_text="John Doe", **entry_style)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Email field
    email_label = ctk.CTkLabel(form_frame, text="Email", font=("Roboto Medium", 25))
    email_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    email_entry = ctk.CTkEntry(form_frame, placeholder_text="test@gmail.com", **entry_style)
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    # Password field
    password_label = ctk.CTkLabel(form_frame, text="Password", font=("Roboto Medium", 25))
    password_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
    password_entry = ctk.CTkEntry(form_frame, placeholder_text="********", show="*", **entry_style)
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    # School dropdown
    school_label = ctk.CTkLabel(form_frame, text="School", font=("Roboto Medium", 25))
    school_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
    school_entry = ctk.CTkComboBox(form_frame, values=["Select a high school", "Steinbrenner High School", "River Ridge High School", "Middleton High School", "Strawberry Crest High School", "Mitchell High School", "East Lake High School", "Gulf High School", "Riverview High School", "Winddale High School"], **entry_style)
    school_entry.grid(row=3, column=1, padx=10, pady=10)

    # School code field
    code_label = ctk.CTkLabel(form_frame, text="School Code", font=("Roboto Medium", 25))
    code_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
    code_entry = ctk.CTkEntry(form_frame, **entry_style)
    code_entry.grid(row=4, column=1, padx=10, pady=10)

    # Status label for school code validation
    status_label = ctk.CTkLabel(form_frame, text="", font=("Roboto Medium", 18))
    status_label.grid(row=5, column=0, columnspan=2, pady=10)

    # Buttons
    button_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    button_frame.pack(pady=20)

    submit_button = ctk.CTkButton(button_frame, width=250, height=55, text="Create Account", 
                                  command=lambda: add_new_user(name_entry, email_entry, password_entry, school_entry, code_entry, status_label, return_to_main), 
                                  font=("Roboto Medium", 25), bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    submit_button.grid(row=0, column=0, padx=10, pady=(0,5))

    back_button = ctk.CTkButton(button_frame, width=250, height=55, text="Back", command=return_to_main, font=("Roboto Medium", 25), 
                                bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    back_button.grid(row=0, column=1, padx=10, pady=(0,5))

    # Bind the school code validation to the school code entry
    code_entry.bind("<KeyRelease>", lambda event: validate_school_code(school_entry.get(), code_entry.get(), status_label))

# Additional functionality as needed
