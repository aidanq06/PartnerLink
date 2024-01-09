import tkinter as tk
import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk

def create_help_window(root, return_to_main):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    # Add your text labels here
        
    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    left = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    left.pack(side="left", fill='both', expand=True, padx=15)

    # Frame to contain the picture, packed to the right side
    right = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    right.pack(side="right", fill='both', expand=True, padx=10, anchor="e")

    label_width = root.winfo_width() // 2  # for example, half of the root window's width


    # LEFT LABELS
    ctk.CTkLabel(left, text="PartnerLink Help Guide", font=("Roboto Medium", 30)).pack(pady=5, anchor='w')

    ctk.CTkLabel(left, text="Current Partners", font=("Roboto Medium", 18)).pack(pady=5, anchor='w')
    ctk.CTkLabel(left, justify="left",text="Click here to view a list of all the partners associated with the program.This is where you can browse through existing partnerships and view detailed information.", font=("Roboto Medium", 14), wraplength=label_width).pack(pady=5, anchor='w')

    ctk.CTkLabel(left, text="Add New Partners", font=("Roboto Medium", 18)).pack(pady=5, anchor='w')
    ctk.CTkLabel(left, justify="left",text="Use this button to input new business and community partners into PartnerLink. It's a simple form that lets you expand your network", font=("Roboto Medium", 14), wraplength=label_width).pack(pady=5, anchor='w')

    ctk.CTkLabel(left, text="Add New Login", font=("Roboto Medium", 18)).pack(pady=5, anchor='w')
    ctk.CTkLabel(left, justify="left",text="This feature allows you to create additional login credentials. Ideal for granting access to new users who need to work with your school.", font=("Roboto Medium", 14), wraplength=label_width).pack(pady=5, anchor='w')

    ctk.CTkLabel(left, text="Account Settings", font=("Roboto Medium", 18)).pack(pady=5, anchor='w')
    ctk.CTkLabel(left, justify="left",text="Customize your PartnerLink experience by managing your personal settings. Update your profile, change your password, and more.", font=("Roboto Medium", 14), wraplength=label_width).pack(pady=5, anchor='w')

    ctk.CTkLabel(left, text="Logout", font=("Roboto Medium", 18)).pack(pady=5, anchor='w')
    ctk.CTkLabel(left, justify="left",text="Safely exit your session with this button. It ensures that your information remains secure when you're done using the application.", font=("Roboto Medium", 14), wraplength=label_width).pack(pady=5, anchor='w')
   
    # LOGO

    logo_image = Image.open("./assets/logoSlogan.png") 

    # Get current size and calculate new size (75% of the current size)
    original_width, original_height = logo_image.size
    new_width = int(original_width * 0.75)
    new_height = int(original_height * 0.75)
    
    # Resize the image
    logo_image = logo_image.resize((new_width, new_height), Image.ANTIALIAS)
    
    # Convert the image to a format that tkinter recognizes
    logo_photo = ImageTk.PhotoImage(logo_image)
    
    # Create a label to hold the image, inside the picture_frame
    logo_label = ctk.CTkLabel(right, text="", image=logo_photo, bg_color='white')
    logo_label.image = logo_photo  # Keep a reference to the image
    logo_label.pack(pady=40)

    # HYPERLINK

    hyperlink_label = ctk.CTkLabel(right, text="PartnerLink GitHub Page", font=("Roboto Medium", 20), text_color="blue",fg_color="transparent", cursor="hand2")
    hyperlink_label.pack()
    hyperlink_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/aidanq06/PartnerLink"))

    # Logo


    # Back Button
    back_button = ctk.CTkButton(right, width=175, height=35, text="Back", command=return_to_main, fg_color="black", bg_color="transparent", hover_color="#444444", text_color="white", font=("Roboto Medium", 25))


    back_button.pack(pady=10)

# Additional functionality as needed
