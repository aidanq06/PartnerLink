import requests
from bs4 import BeautifulSoup
import customtkinter as ctk
from tkinter import messagebox, Listbox, Scrollbar
import json
from pymongo import MongoClient
import re

# MongoDB connection string
with open("./assets/variables.json", 'r') as file:
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

def submit_data(company_name_text, type_dropdown, email_text, phone_text, partners_col, return_to_main):
    # Retrieve data from Text fields
    company_name = company_name_text.get("1.0", 'end').strip()
    business_type = type_dropdown.get()
    email = email_text.get("1.0", 'end').strip()
    phone_number = phone_text.get("1.0", 'end').strip()

    # Validate email and format phone number
    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return
    phone_number = format_phone_number(phone_number)

    # Check if all fields are filled out
    if all([company_name, business_type, email, phone_number]):
        # All fields are filled, submit data to MongoDB
        new_partner = {
            "companyName": company_name,
            "type": business_type,
            "contactEmail": email,
            "contactPhone": phone_number,
        }
        partners_col.insert_one(new_partner)
        messagebox.showinfo("Success", "Partner added successfully.")
        return_to_main()  # Return to the main menu
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def scrape_business_info(query, location):
    search_url = f"https://www.yellowpages.com/search?search_terms={query}&geo_location_terms={location}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    business_info = []
    for result in soup.find_all('div', class_='result'):
        name = result.find('a', class_='business-name').text.strip()
        address_tag = result.find('div', class_='street-address')
        address = address_tag.text.strip() if address_tag else 'No address available'
        contact_info = result.find('div', class_='phones phone primary').text.strip() if result.find('div', 'phones phone primary') else 'No contact info available'
        
        business_info.append({
            'name': name,
            'address': address,
            'contact_info': contact_info
        })
    return business_info

def display_businesses(root, return_to_search, businesses):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    ctk.CTkLabel(background_frame, text="Recommended Partners", font=("Roboto Medium", 30)).pack(pady=15)

    listbox_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    listbox_frame.pack(fill='both', expand=True, padx=20, pady=20)

    scrollbar = Scrollbar(listbox_frame)
    scrollbar.pack(side="right", fill="y")

    listbox = Listbox(listbox_frame, font=("Roboto Medium", 18), selectmode="single", yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=listbox.yview)

    details_label = ctk.CTkLabel(background_frame, text="", font=("Roboto Medium", 18))
    details_label.pack(pady=10)

    def on_select(event):
        selected_index = listbox.curselection()
        if selected_index:
            selected_business = businesses[selected_index[0]]
            details_label.configure(text=f"Address: {selected_business['address']}\nContact: {selected_business['contact_info']}")

    listbox.bind('<<ListboxSelect>>', on_select)

    for business in businesses:
        listbox.insert("end", business['name'])

    button_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    button_frame.pack(pady=20)

    back_button = ctk.CTkButton(button_frame, width=250, height=55, text="Back", command=return_to_search, font=("Roboto Medium", 25), bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    back_button.grid(row=0, column=0, padx=10, pady=(0,5))

    add_partner_button = ctk.CTkButton(button_frame, width=250, height=55, text="Add Partner", command=lambda: add_partner(businesses[listbox.curselection()[0]] if listbox.curselection() else None), font=("Roboto Medium", 25), bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    add_partner_button.grid(row=0, column=1, padx=10, pady=(0,5))

def add_partner(business):
    if business:
        # Add business to your database
        new_partner = {
            "companyName": business['name'],
            "contactPhone": business['contact_info']
        }
        partners_col.insert_one(new_partner)
        messagebox.showinfo("Partner Added", f"{business['name']} has been added as a partner!")
    else:
        messagebox.showwarning("No Selection", "Please select a business to add as a partner.")

def create_search_form(root, return_to_main):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    entry_style = {"font": ("Roboto Medium", 25), "width": 300, "height": 40}

    ctk.CTkLabel(background_frame, text="Search for New Partners", font=("Roboto Medium", 40)).pack(pady=15)

    form_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    form_frame.pack(pady=10)

    # Query field
    query_label = ctk.CTkLabel(form_frame, text="Search Term", font=("Roboto Medium", 25))
    query_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    query_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g., education", **entry_style)
    query_entry.grid(row=0, column=1, padx=10, pady=10)

    # Location field
    location_label = ctk.CTkLabel(form_frame, text="Location", font=("Roboto Medium", 25))
    location_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    location_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g., Tampa, FL", **entry_style)
    location_entry.grid(row=1, column=1, padx=10, pady=10)

    button_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    button_frame.pack(pady=20)

    search_button = ctk.CTkButton(button_frame, width=250, height=55, text="Search", command=lambda: search_and_display_partners(root, lambda: create_search_form(root, return_to_main), query_entry.get(), location_entry.get()), font=("Roboto Medium", 25), bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    search_button.grid(row=0, column=0, padx=10, pady=(0,5))

    back_button = ctk.CTkButton(button_frame, width=250, height=55, text="Back", command=return_to_main, font=("Roboto Medium", 25), bg_color="transparent", fg_color="black", hover_color="#444444", text_color="white")
    back_button.grid(row=0, column=1, padx=10, pady=(0,5))

def search_and_display_partners(root, return_to_search, query, location):
    businesses = scrape_business_info(query, location)
    display_businesses(root, return_to_search, businesses)

# Example usage:
# if __name__ == "__main__":
#     root = ctk.CTk()
#     root.geometry("800x600")
#     create_search_form(root, lambda: print("Return to main"))
#     root.mainloop()
