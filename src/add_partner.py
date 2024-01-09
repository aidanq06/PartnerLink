import tkinter as tk
import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox
import re
import json

# MongoDB connection string
with open("./assets/mongodb.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']
    
# Connect to MongoDB
client = MongoClient(conn_str)
db = client['partnerlink']
partners_col = db['partners']


def is_valid_email(email):
    """Check if the email is valid."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def format_phone_number(phone_number):
    """Format the phone number to include dashes."""
    phone_number = phone_number.replace('-', '')  # Remove existing dashes
    return '-'.join([phone_number[:3], phone_number[3:6], phone_number[6:]])

def submit_data(company_name_text, type_dropdown, email_text, phone_text, resources_text, description_text, partners_col, return_to_main):
    # Retrieve data from Text fields
    company_name = company_name_text.get("1.0", tk.END).strip()
    business_type = type_dropdown.get()
    email = email_text.get("1.0", tk.END).strip()
    phone_number = phone_text.get("1.0", tk.END).strip()
    resources = resources_text.get("1.0", tk.END).strip()
    description = description_text.get("1.0", tk.END).strip()

    # Validate email and format phone number
    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return
    phone_number = format_phone_number(phone_number)

    # Check if all fields are filled out
    if all([company_name, business_type, email, phone_number, resources, description]):
        # All fields are filled, submit data to MongoDB
        new_partner = {
            "companyName": company_name,
            "type": business_type,
            "contactEmail": email,
            "contactPhone": phone_number,
            "resources": resources,
            "description": description
        }
        partners_col.insert_one(new_partner)
        messagebox.showinfo("Success", "Partner added successfully.")
        return_to_main()  # Return to the main menu
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
        
def create_add_partner_form(root, return_to_main):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()
    customfont = ("Roboto Medium", 20)
    textfont = ("Roboto Medium", 12)
    entry_bg = 'white'  # Background color for text entries
    entry_border_color = 'black'  # Border color for text entries
    entry_border_width = 1  # Border width for text entries

    # Create main background frame
    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    # Left and right frames for layout
    left_frame = ctk.CTkFrame(background_frame, width=500, height=500, bg_color='white', fg_color="white")
    left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=20)
    right_frame = ctk.CTkFrame(background_frame, width=500, height=500, bg_color='white', fg_color="white")
    right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=20)

    # Function to create bordered text entry
    def bordered_text_entry(parent, width, height, font):
        border_frame = ctk.CTkFrame(parent, bg_color=entry_border_color, width=width, height=height)
        border_frame.pack_propagate(False)  # Prevents the frame from resizing to fit the text entry
        text_entry = tk.Text(border_frame, font=font, bg=entry_bg, bd=0, highlightthickness=entry_border_width)
        text_entry.pack(fill='both', expand=True)
        return border_frame, text_entry
    

    company_name_label = ctk.CTkLabel(left_frame, text="Add New Partner", font=("Roboto Medium", 40, "underline"), anchor='w')
    company_name_label.pack(fill='x', pady=10)

    # Company or Business Name Field
    
    company_name_label = ctk.CTkLabel(left_frame, text="Company Name", font=customfont, anchor='w')
    company_name_label.pack(fill='x', pady=(10,5))
    company_name_frame, company_name_entry = bordered_text_entry(left_frame, 400, 30, ("Roboto Medium", 16))
    company_name_frame.pack(fill='x', pady=(0, 20))

    # Type of Business Dropdown
    type_label = ctk.CTkLabel(left_frame, text="Type of Business", font=customfont, anchor='w')
    type_label.pack(fill='x', pady=(0, 5))
    business_types = ["For-Profit Organization", "Non-Profit Organization", "Government Affiliated", "Local Business", "Corporate Business"]
    type_dropdown = ctk.CTkOptionMenu(left_frame, values=business_types, font=("Roboto Medium", 16), fg_color="#cfcfcf", text_color="black", button_color="#444444", button_hover_color="#444444")
    type_dropdown.pack(fill='x', pady=(0, 20))

    # Contact Email Field
    email_label = ctk.CTkLabel(left_frame, text="Contact Email", font=customfont, anchor='w')
    email_label.pack(fill='x', pady=(0, 5))
    email_frame, email_entry = bordered_text_entry(left_frame, 400, 30, ("Roboto Medium", 16))
    email_frame.pack(fill='x', pady=(0, 20))

    # Contact Phone Field
    phone_label = ctk.CTkLabel(left_frame, text="Contact Phone Number", font=customfont, anchor='w')
    phone_label.pack(fill='x', pady=(0, 5))
    phone_frame, phone_entry = bordered_text_entry(left_frame, 400, 30, ("Roboto Medium", 16))
    phone_frame.pack(fill='x', pady=(0, 20))

    # Resources Field
    resources_label = ctk.CTkLabel(right_frame, text="Resources", font=customfont, anchor='w')
    resources_label.pack(fill='x', pady=(0, 5))
    resources_frame, resources_entry = bordered_text_entry(right_frame, 400, 100, textfont)
    resources_frame.pack(fill='x', pady=(0, 20))

    # Description Field on the right frame
    description_label = ctk.CTkLabel(right_frame, text="Description", font=customfont, anchor='w')
    description_label.pack(fill='x', pady=(0, 5))
    description_frame, description_text = bordered_text_entry(right_frame, 400, 150, textfont)
    description_frame.pack(fill='x', pady=(0, 20))

    # Submit and Back Buttons under the description
    submit_button = ctk.CTkButton(
        right_frame,
        text="Submit",
        width=250,
        height=40,
        font=("Roboto Medium", 20),
        fg_color="black",
        text_color="white",
        hover_color="#444444",
        command=lambda: submit_data(
            company_name_entry,
            type_dropdown,
            email_entry,
            phone_entry,
            resources_entry,
            description_text,
            partners_col,
            return_to_main
        )
    )
    submit_button.pack(pady=(0,10))

    back_button = ctk.CTkButton(
        right_frame,
        text="Back",
        width=250,
        height=40,
        font=("Roboto Medium", 20),
        fg_color="black",
        text_color="white",
        hover_color="#444444",
        command=return_to_main
    )
    back_button.pack()


# Additional functions and logic as needed
