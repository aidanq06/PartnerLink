import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
import customtkinter as ctk
from tkinter import messagebox
import json 
# MongoDB connection string
with open("./assets/variables.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']

# Connect to MongoDB
client = MongoClient(conn_str)
db = client['partnerlink']
partners_col = db['partners']

def delete_selected_partner(tree, partners_col, return_to_main):
    selected_item = tree.selection()
    if selected_item:
        company_name = tree.item(selected_item, 'values')[0]
        # Delete the partner from MongoDB
        partners_col.delete_one({"companyName": company_name})
        messagebox.showinfo("Success", "Partner deleted successfully.")
        # Refresh the Treeview or return to main
        create_and_show_treeview(tree.winfo_toplevel(), return_to_main)
    else:
        messagebox.showerror("Error", "Please select a partner to delete.")


def search_treeview(keyword, tree):
    # Clear current Treeview
    tree.delete(*tree.get_children())

    # Fetch data and filter based on the keyword
    search_results = [partner for partner in fetch_partners_data() if keyword.lower() in str(partner).lower()]

    # Populate Treeview with search results
    for partner in search_results:
        tree.insert('', tk.END, values=partner)


def apply_filter(filter_criterion, tree):
    # Clear current Treeview
    tree.delete(*tree.get_children())

    # Fetch and filter data based on the selected criterion
    filtered_data = [partner for partner in fetch_partners_data() if filter_criterion in partner]

    # Populate Treeview with filtered data
    for partner in filtered_data:
        tree.insert('', tk.END, values=partner)


def fetch_partners_data():
    # Fetch data and format for Treeview (excluding ID)
    partners_data = partners_col.find({})
    return [(partner['companyName'], partner['type'], partner['contactPhone']) for partner in partners_data]

def create_and_show_treeview(root, return_to_main):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    # Styling options for buttons
    button_style = {"fg_color": "black", "text_color": "white", "hover_color": "#444444", "font": ("Roboto Medium", 25)}

    # Create frames for each row
    first_row_frame = ctk.CTkFrame(root,fg_color="transparent")
    first_row_frame.pack(anchor='n', padx=10, pady=5)

    # First row: Search bar and button
    search_entry = ctk.CTkEntry(first_row_frame, width=400,height=50,placeholder_text="Search...", font=("Roboto Medium", 30))
    search_entry.pack(side="left",padx=5)
    search_button = ctk.CTkButton(first_row_frame, width=200,height=50,text="Search", command=lambda: search_treeview(search_entry.get(), tree), fg_color="black",text_color="white",hover_color="#444444",font=("Roboto Medium",30))
    search_button.pack(side="right",padx=5)

    """filter
    filter_criteria = ["For-Profit Organization", "Non-Profit Organization", "Government Affiliated", "Local Business", "Corporate Business"]
    filter_dropdown = ctk.CTkOptionMenu(first_row_frame, values=filter_criteria)
    filter_dropdown.pack(side='left', padx=5)
    filter_button = ctk.CTkButton(first_row_frame, text="Apply Filter", command=lambda: apply_filter(filter_dropdown.get(), tree), **button_style)
    filter_button.pack(side='left', padx=5)
    """
    style=ttk.Style()
    style.configure("Treeview", font=("Roboto Medium", 10))  # Adjust size as needed


    # Setting up the Treeview
    columns = ("Company Name", "Type", "Phone Number")
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading("Company Name", text="Company Name", anchor="w")
    tree.heading("Type", text="Type", anchor="w")
    tree.heading("Phone Number", text="Phone Number", anchor="w")

    # Insert data into Treeview
    partner_data = fetch_partners_data()
    for partner in partner_data:
        tree.insert('', tk.END, values=partner)

    # Positioning the Treeview
    tree.pack(expand=True, fill='both')

    # Create third row frame after the Treeview
    third_row_frame = ctk.CTkFrame(root, fg_color="transparent")
    third_row_frame.pack(anchor='nw', padx=10, pady=5)

    # Third row: Back, Delete, and More Details buttons
    back_button = ctk.CTkButton(third_row_frame, width=275,height=50,text="Back", command=return_to_main, **button_style)
    back_button.pack(side='left', padx=5)
    delete_button = ctk.CTkButton(third_row_frame, width=275,height=50, text="Delete", command=lambda: delete_selected_partner(tree, partners_col, return_to_main), **button_style)
    delete_button.pack(side='left', padx=5)
    more_details_button = ctk.CTkButton(third_row_frame, width=250,height=50, text="More Details", command=lambda: show_more_details(tree, root, return_to_main), **button_style)
    more_details_button.pack(side='left', padx=5)


# Add other functionalities as needed
def show_more_details(tree, root, return_to_main):
    selected_item = tree.selection()
    if selected_item:
        # Fetch company name from the selected item
        company_name = tree.item(selected_item, 'values')[0]
        
        # Fetch complete details of the company from MongoDB
        company_details = partners_col.find_one({"companyName": company_name})

        # Display these details
        display_details_in_current_window(company_details, root, return_to_main)

def display_details_in_current_window(details, root, return_to_main):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    # Create a frame to contain the labels, aligned to the top left
    details_frame = ctk.CTkFrame(background_frame,fg_color="white")
    details_frame.pack(fill='both', expand=True,anchor='nw', padx=10, pady=10)

    root.update_idletasks()  
    frame_width = details_frame.winfo_width()  # Get the width of the frame

    # Define common label options
    label_options = {'font': ("Roboto Medium", 20), 'wraplength': frame_width, 'anchor': 'w', 'justify': 'left'}

    # Display the details
    ctk.CTkLabel(details_frame, text=f"{details['companyName']}", justify="left",font=("Roboto Medium", 40), anchor="w").pack(pady=2, padx=5,fill='x')
    ctk.CTkLabel(details_frame, text=f"{details['type']}", justify="left",font=("Roboto Medium", 30,"underline"), anchor="w").pack(pady=2, padx=5, fill='x')
    ctk.CTkLabel(details_frame, text=f"{details['description']}", **label_options).pack(pady=2, padx=5, fill='x')
    ctk.CTkLabel(details_frame, text=f"Resources", justify="left",font=("Roboto Medium", 30,"underline"), anchor="w").pack(padx=5, fill='x')
    ctk.CTkLabel(details_frame, text=f"{details['resources']}", justify="left",font=("Roboto Medium", 20), wraplength=frame_width, anchor="w").pack(pady=2, padx=5, fill='x')
    ctk.CTkLabel(details_frame, text=f"Contact Phone: {details['contactPhone']}", font=("Roboto Medium", 30), justify="left",anchor="w").pack(pady=2, padx=5, fill='x')
    ctk.CTkLabel(details_frame, text=f"Contact Email: {details['contactEmail']}", font=("Roboto Medium", 30), justify="left",anchor="w").pack(pady=2, padx=5, fill='x')

    # Back button to return to the Treeview
    back_button = ctk.CTkButton(root, text="Back", fg_color="black", hover_color="#444444",width=250, height=40, font=("Roboto Medium", 30), command=lambda: create_and_show_treeview(root, return_to_main))
    back_button.pack(pady=5)