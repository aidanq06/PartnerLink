import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkextrafont import Font
import re
import hashlib
from pymongo import MongoClient
import json

import partner_manager as partner_manager
import add_partner as add_partner
import helpButton as helpButton 
import account_settings as account_settings
import newAccount as newAccount

# retrieving mongodb connection string from json file
with open("./assets/mongodb.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']

# connect to mongodb
client = MongoClient(conn_str)
db = client['partnerlink']  # database name
users_col = db['users']  # users table

class SignInWindow(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("light")
        super().__init__()
        self.custom_font = Font(file="./assets/Roboto-Medium.ttf", family="Roboto Medium")
        self.title("PartnerLink")
        self.geometry("900x500")  # window size
        self.setup_login_screen()

    def clear_window(self):
        # Destroy all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()

    def setup_login_screen(self):
        self.clear_window()

        # Adjusting frames for layout
        left_frame = ctk.CTkFrame(self, width=400, height=500, bg_color='white', fg_color="white")
        left_frame.pack(side="left", fill="y", expand=False)
        right_frame = ctk.CTkFrame(self, width=400, height=500)
        right_frame.pack(side="right", fill="y", expand=True)

        login_label = ctk.CTkLabel(right_frame, text="          Login          ", font=("Roboto Medium", 50), bg_color='white', fg_color="#dbdbdb")
        login_label.pack(pady=20)
        
        # Load and display logo in the left frame
        self.logo_image = Image.open("./assets/logoSlogan.png")
        self.logo_image = self.logo_image.resize((450, 350), Image.ANTIALIAS)  # Resize logo
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ctk.CTkLabel(left_frame, image=self.logo_image, bg_color='white', fg_color="white", text="")
        self.logo_label.pack(pady=75)

        # Increase size of entries and align them in the right frame
        # Set a fixed width for text entries
        entry_width = 300  
        entry_height = 60
        entry_font = ("Roboto Medium", 20)

        self.email_entry = ctk.CTkEntry(right_frame, placeholder_text="Email", width=entry_width, height=entry_height, font=entry_font)
        self.email_entry.pack(pady=10)

        self.email_status_label = ctk.CTkLabel(right_frame, text="", font=entry_font,bg_color='#dbdbdb', fg_color="#dbdbdb")
        self.email_status_label.pack(pady=5)

        self.email_entry.bind("<KeyRelease>", self.validate_email)


        self.password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", show="*", width=entry_width, height=entry_height, font=entry_font)
        self.password_entry.pack(pady=10)
        
        self.password_status_label = ctk.CTkLabel(right_frame, text="", bg_color='#dbdbdb', fg_color="#dbdbdb", font=entry_font)
        self.password_status_label.pack(pady=5)

        self.password_entry.bind("<KeyRelease>", self.validate_password)

        # Sign In Button in the right frame
        self.sign_in_button = ctk.CTkButton(right_frame, text="login", text_color="#dbdbdb",command=self.sign_in, width=250, height=50, font=entry_font, fg_color="#000000", hover_color="#444444")
        self.sign_in_button.pack(pady=10)

        self.login_error_label = ctk.CTkLabel(right_frame, text="", bg_color='white', fg_color="#dbdbdb", font=entry_font)
        self.login_error_label.pack(pady=2)
    

    def show_login_screen(self):
        self.setup_login_screen()  # Reset to the login screen

    def validate_email(self, event=None):
        email = self.email_entry.get()
        # Regular expression for validating an email
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, email):
            self.email_status_label.configure(text="Email Entered", text_color="black", fg_color="#dbdbdb", bg_color="#dbdbdb")
        else:
            self.email_status_label.configure(text="Incorrect email format", text_color="red", fg_color="#dbdbdb", bg_color="#dbdbdb")

    def validate_password(self, event=None):
        password = self.password_entry.get()
        if password:
            self.password_status_label.configure(text="Password Entered", text_color="black", fg_color="#dbdbdb", bg_color="#dbdbdb")
        else:
            self.password_status_label.configure(text="Invalid password", text_color="red", fg_color="#dbdbdb", bg_color="#dbdbdb")

    def sign_in(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if self.email_status_label.cget("text") == "Email Entered" and password:
            user = users_col.find_one({"email": email})

            if user and user['passwordHash'] == password_hash:
                print("Login successful")
                self.user_id = user['_id']
                # Store the user's name
                self.user_name = user.get('name', 'User')  # Default to 'User' if name is not available
                self.clear_window()
                self.create_new_layout()  # Create a new layout after successful login
            else:
                self.login_error_label.configure(text="credentials did not match\nour systems", text_color="red", fg_color="#dbdbdb", bg_color="#dbdbdb", font=("Roboto Medium", 20))
        else:
            self.login_error_label.configure(text="invalid credentials", text_color="red", fg_color="#dbdbdb", bg_color="#dbdbdb")

    def create_new_layout(self):
        self.geometry("900x500")
        background_frame = ctk.CTkFrame(self, bg_color='white', fg_color="white")
        background_frame.pack(fill='both', expand=True)
        background_frame.lower(belowThis=None)

        # Greeting label with user's name
        welcome_label = ctk.CTkLabel(background_frame, text=f"Welcome, {self.user_name}!", font=("Roboto Medium", 50))
        welcome_label.pack(pady=10, padx=20, anchor="nw")

        # Frame to contain the buttons, packed to the left side
        buttons_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
        buttons_frame.pack(side="left", fill='y', expand=True, padx=20)

        # Frame to contain the picture, packed to the right side
        picture_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
        picture_frame.pack(side="right", fill='y', expand=True, padx=20, pady=25)

         # Open the image
        logo_image = Image.open("./assets/loginLogo.png") 
    
        # Get current size and calculate new size (75% of the current size)
        original_width, original_height = logo_image.size
        new_width = int(original_width * 0.75)
        new_height = int(original_height * 0.75)
        
        # Resize the image
        logo_image = logo_image.resize((new_width, new_height), Image.ANTIALIAS)
        
        # Convert the image to a format that tkinter recognizes
        logo_photo = ImageTk.PhotoImage(logo_image)
        
        # Create a label to hold the image, inside the picture_frame
        logo_label = ctk.CTkLabel(picture_frame, text="", image=logo_photo, bg_color='white')
        logo_label.image = logo_photo  # Keep a reference to the image
        logo_label.pack()


        buttonWidth = 350 
        buttonHeight = 60
        buttonFont = ("Roboto Medium", 25)

        # Button for the first plugin
        plugin_button1 = ctk.CTkButton(
            buttons_frame,
            text="Current Partners",
            width=buttonWidth,
            height=buttonHeight,
            font=buttonFont,
            fg_color="black",
            bg_color="white",
            text_color="white",
            hover_color="#444444",
            command=lambda: partner_manager.create_and_show_treeview(self, self.return_to_main_menu)
        )
        plugin_button1.pack(pady=10)

        # Button for the second plugin
        plugin_button2 = ctk.CTkButton(
            buttons_frame,
            text="Add New Partners",
            width=buttonWidth,
            height=buttonHeight,
            font=buttonFont,
            fg_color="black",
            bg_color="white",
            text_color="white",
            hover_color="#444444",
            command=lambda: add_partner.create_add_partner_form(self, self.return_to_main_menu)
        )
        plugin_button2.pack(pady=10)

        plugin_button3 = ctk.CTkButton(
            buttons_frame,
            text="Add New Login",
            width=buttonWidth,
            height=buttonHeight,
            font=buttonFont,
            fg_color="black",
            bg_color="white",
            text_color="white",
            hover_color="#444444",
            command=lambda: newAccount.create_new_account_form(self, self.return_to_main_menu)
        )
        plugin_button3.pack(pady=10)

        plugin_button4 = ctk.CTkButton(
            buttons_frame,
            text="Account Settings",
            width=buttonWidth,
            height=buttonHeight,
            font=buttonFont,
            fg_color="black",
            bg_color="white",
            text_color="white",
            hover_color="#444444",
            command=lambda: account_settings.create_account_settings_form(self, self.user_id, self.return_to_main_menu)

        )
        plugin_button4.pack(pady=10)

        # Button for the third plugin
        logoutButton = ctk.CTkButton(
            buttons_frame,
            command=lambda: self.show_login_screen(),
            text="Logout",
            width=buttonWidth,
            height=buttonHeight,
            font=buttonFont,
            fg_color="black",
            bg_color="white",
            text_color="white",
            hover_color="#444444",
        )
        logoutButton.pack(pady=10)

        # Load the help icon image
        help_icon = Image.open("assets/helpIcon.png")
        help_icon = help_icon.resize((50,50), Image.ANTIALIAS)

        help_photo = ImageTk.PhotoImage(help_icon)


        # Create a help button
        help_button = ctk.CTkButton(self, image=help_photo,
                                    text="",
                                    command=lambda: helpButton.create_help_window(self, self.return_to_main_menu), 
                                    width=40, height=40, 
                                    fg_color="white", 
                                    bg_color="white",
                                    hover_color="#444444")
        help_button.image = help_icon  # Keep a reference to avoid garbage collection

        # Place the button at the bottom right corner
        help_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

    def return_to_main_menu(self):
        # Clear the current window contents
        for widget in self.winfo_children():
            widget.destroy()

        # Recreate the initial layout
        self.create_new_layout()

if __name__ == "__main__":
    app = SignInWindow()
    app.mainloop()
