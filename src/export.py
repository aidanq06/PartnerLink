import tkinter as tk
import customtkinter as ctk
from pymongo import MongoClient
from tkinter import messagebox
import json
import webbrowser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from collections import Counter
import matplotlib.pyplot as plt

# MongoDB connection string
with open("./assets/variables.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']

# Connect to MongoDB
client = MongoClient(conn_str)
db = client['partnerlink']
partners_col = db['partners']

def export_to_pdf(selected_partners, include_phone, include_email, chart_type=None):
    # Create PDF
    pdf_filename = "exported_partners.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Exported Partners")

    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 100
    for partner in selected_partners:
        text = f"{partner['companyName']}\n"
        if include_phone:
            text += f"{partner['contactPhone']}\n"
        if include_email:
            text += f"{partner['contactEmail']}\n"
        text += "\n"
        for line in text.split('\n'):
            c.drawString(50, y_position, line)
            y_position -= 20
        y_position -= 10  # Adjust this value to change the spacing between companies
        if y_position < 50:
            c.showPage()
            y_position = height - 50

    # Add chart if selected
    if chart_type and chart_type != "None":
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"{chart_type} Chart")

        # Generate and add chart
        types = [partner['type'] for partner in selected_partners]
        type_counts = Counter(types)
        labels, values = zip(*type_counts.items())

        plt.figure(figsize=(8, 6))
        if chart_type == "Bar Chart":
            plt.bar(labels, values, color='blue')
        elif chart_type == "Pie Chart":
            plt.pie(values, labels=labels, autopct='%1.1f%%')
        elif chart_type == "Line Chart":
            plt.plot(labels, values, marker='o')

        plt.title(f"{chart_type} of Partner Types")
        plt.savefig("chart.png")
        plt.close()

        # Insert chart into PDF
        c.drawImage("chart.png", 50, height - 400, width=500, height=300)

    c.save()
    webbrowser.open(pdf_filename)

def create_export_form(root, return_to_main):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    # Styling options for buttons
    button_style = {"fg_color": "black", "text_color": "white", "hover_color": "#444444", "font": ("Roboto Medium", 20)}

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    # Title
    ctk.CTkLabel(background_frame, text="Export Partners", font=("Roboto Medium", 30)).pack(pady=10)

    # Frame for the checklist and additional options
    options_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    options_frame.pack(fill='both', expand=True, padx=20, pady=20)

    checklist_frame = ctk.CTkFrame(options_frame, bg_color='white', fg_color="white")
    checklist_frame.pack(side="left", fill='both', expand=True)

    # Scrollbar
    canvas_widget = tk.Canvas(checklist_frame, bg='white', highlightthickness=0)
    scrollbar = tk.Scrollbar(checklist_frame, orient="vertical", command=canvas_widget.yview)
    scrollable_frame = ctk.CTkFrame(canvas_widget, bg_color='white', fg_color="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas_widget.configure(
            scrollregion=canvas_widget.bbox("all")
        )
    )

    canvas_widget.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas_widget.configure(yscrollcommand=scrollbar.set)

    canvas_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fetching partners data
    partners_data = list(partners_col.find({}))
    checkboxes = []
    select_all_var = tk.BooleanVar()

    def toggle_select_all():
        select_all = select_all_var.get()
        for cb, var, _ in checkboxes:
            var.set(select_all)

    select_all_cb = ctk.CTkCheckBox(scrollable_frame, text="Select All", variable=select_all_var, font=("Roboto Medium", 18), bg_color='white', fg_color="white", command=toggle_select_all)
    select_all_cb.pack(anchor="w", pady=2)

    for partner in partners_data:
        var = tk.BooleanVar()
        cb = ctk.CTkCheckBox(scrollable_frame, text=partner['companyName'], variable=var, font=("Roboto Medium", 18), bg_color='white', fg_color="white", hover_color="#444444")
        cb.pack(anchor="w", pady=2)
        checkboxes.append((cb, var, partner))

    # Frame for additional options
    additional_options_frame = ctk.CTkFrame(options_frame, bg_color='white', fg_color="white")
    additional_options_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Dropdown for chart type selection
    chart_frame = ctk.CTkFrame(additional_options_frame, bg_color='white', fg_color="white")
    chart_frame.pack(pady=5, anchor="w")
    ctk.CTkLabel(chart_frame, text="Select Chart Type", font=("Roboto Medium", 18)).pack(side="left", padx=5)
    chart_options = ["None", "Bar Chart", "Pie Chart", "Line Chart"]
    chart_type_var = tk.StringVar(value="None")
    chart_dropdown = ctk.CTkOptionMenu(chart_frame, variable=chart_type_var, values=chart_options, font=("Roboto Medium", 18), fg_color="#cfcfcf", text_color="black", button_color="#444444", button_hover_color="#444444")
    chart_dropdown.pack(side="left", padx=5)

    # Filter by Type dropdown
    filter_frame = ctk.CTkFrame(additional_options_frame, bg_color='white', fg_color="white")
    filter_frame.pack(pady=5, anchor="w")
    ctk.CTkLabel(filter_frame, text="Filter by Type", font=("Roboto Medium", 18)).pack(side="left", padx=5)
    filter_options = ["All", "For-Profit Organization", "Non-Profit Organization", "Government Affiliated", "Local Business", "Corporate Business"]
    filter_type_var = tk.StringVar(value="All")
    filter_dropdown = ctk.CTkOptionMenu(filter_frame, variable=filter_type_var, values=filter_options, font=("Roboto Medium", 18), fg_color="#cfcfcf", text_color="black", button_color="#444444", button_hover_color="#444444", command=lambda e: apply_filter())
    filter_dropdown.pack(side="left", padx=5)

    def apply_filter():
        filter_type = filter_type_var.get()
        for cb, var, partner in checkboxes:
            if filter_type == "All" or filter_type == partner['type']:
                cb.pack(anchor="w", pady=2)
            else:
                cb.pack_forget()

    # Checkboxes for including phone numbers and emails
    include_phone_var = tk.BooleanVar(value=True)
    include_phone_cb = ctk.CTkCheckBox(additional_options_frame, hover_color="#444444", text="Include Phone Numbers", variable=include_phone_var, font=("Roboto Medium", 18), bg_color='white', fg_color="white")
    include_phone_cb.pack(pady=5, anchor="w")

    include_email_var = tk.BooleanVar(value=True)
    include_email_cb = ctk.CTkCheckBox(additional_options_frame, hover_color="#444444", text="Include Emails", variable=include_email_var, font=("Roboto Medium", 18), bg_color='white', fg_color="white")
    include_email_cb.pack(pady=5, anchor="w")

    def export_selected_partners():
        selected_partners = [partner for cb, var, partner in checkboxes if var.get()]
        if selected_partners:
            export_to_pdf(selected_partners, include_phone_var.get(), include_email_var.get(), chart_type_var.get())
        else:
            messagebox.showwarning("No Selection", "Please select at least one partner to export.")

    # Export and Back buttons
    buttons_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    buttons_frame.pack(pady=10)

    export_button = ctk.CTkButton(buttons_frame, text="Export", command=export_selected_partners, width=250, height=60, **button_style)
    export_button.pack(side="left", padx=10)

    back_button = ctk.CTkButton(buttons_frame, text="Back", command=return_to_main, width=250, height=60, **button_style)
    back_button.pack(side="left", padx=10)
