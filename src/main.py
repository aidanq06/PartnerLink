import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkextrafont import Font
import re
import hashlib
from pymongo import MongoClient
import json
import random
from email.mime.text import MIMEText
import smtplib
from tkinter import messagebox

import partnerManager as partnerManager
import addPartner as addPartner
import helpButton as helpButton 
import helpLogin as helpLogin
import accountSettings as accountSettings
import newAccount as newAccount
import contact as contact
import searchPartners as searchPartners
import export as export

# retrieving mongodb connection string from json file
with open("./assets/variables.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']
    sender_email = data['sender_email']
    sender_password = data['password']
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
        self.geometry("1000x650")  # window size
        self.setup_login_screen()
        self.configure(bg_color='white', fg_color="white")

    def clear_window(self):
        # Destroy all widgets from the window
        for widget in self.winfo_children():
            widget.destroy()

    def setup_login_screen(self):
        self.clear_window()
        self.configure(bg_color='white', fg_color="white")
        # Adjusting frames for layout
        left_frame = ctk.CTkFrame(self, width=500, height=650, bg_color='white', fg_color="white")
        left_frame.pack(side="left", fill="y", expand=False)
        right_frame = ctk.CTkFrame(self, width=500, height=650, bg_color="white", fg_color="white")
        right_frame.pack(side="right", fill="y", expand=True)

        login_label = ctk.CTkLabel(right_frame, text="          Login          ", font=("Roboto Medium", 60), bg_color='white', fg_color="white")
        login_label.pack(pady=30)
        
        # Load and display logo in the left frame
        self.logo_image = Image.open("./assets/logoSlogan.png")
        self.logo_image = self.logo_image.resize((450, 350), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ctk.CTkLabel(left_frame, image=self.logo_image, bg_color='white', fg_color="white", text="")
        self.logo_label.pack(pady=130)

        # Add a thin black bar
        # Add a thin vertical black bar
        bar_frame = ctk.CTkFrame(self, width=4, height=600, bg_color='black', fg_color="black")
        bar_frame.place(relx=0.47, rely=0.5, anchor='center')


        # Increase size of entries and align them in the right frame
        # Set a fixed width for text entries
        entry_width = 300  
        entry_height = 60
        entry_font = ("Roboto Medium", 20)

        self.email_entry = ctk.CTkEntry(right_frame, placeholder_text="Email", width=entry_width, height=entry_height, font=entry_font)
        self.email_entry.pack(pady=10)

        self.email_status_label = ctk.CTkLabel(right_frame, text="", font=entry_font, bg_color='white', fg_color="white")
        self.email_status_label.pack(pady=5)

        self.email_entry.bind("<KeyRelease>", self.validate_email)

        self.password_entry = ctk.CTkEntry(right_frame, placeholder_text="Password", show="*", width=entry_width, height=entry_height, font=entry_font)
        self.password_entry.pack(pady=10)
        
        self.login_error_label = ctk.CTkLabel(right_frame, text="", bg_color='white', fg_color="white", font=entry_font)
        self.login_error_label.pack(pady=(5,20))

        self.sign_in_button = ctk.CTkButton(right_frame, text="Login", text_color="white", command=self.sign_in, width=250, height=50, font=("Roboto Medium", 20), fg_color="#000000", hover_color="#444444")
        self.sign_in_button.pack(pady=10)

        self.register_button = ctk.CTkButton(right_frame, text="Register", text_color="white", width=250, height=50, font=("Roboto Medium", 20), fg_color="#000000", hover_color="#444444", command=lambda: newAccount.create_new_account_form(self, lambda: self.show_login_screen()))
        self.register_button.pack(pady=10)
        
        help_icon = Image.open("assets/helpIcon.png")
        help_icon = help_icon.resize((50, 50), Image.Resampling.LANCZOS)
        help_photo = ImageTk.PhotoImage(help_icon)

        # Create a help button
        help_button = ctk.CTkButton(self, image=help_photo,
                                    text="",
                                    command=lambda: helpLogin.create_help_window(self, self.show_login_screen),
                                    width=40, height=40,
                                    fg_color="white",
                                    bg_color="white",
                                    hover_color="#444444")
        help_button.image = help_icon  # Keep a reference to avoid garbage collection

        # Place the button at the bottom right corner
        help_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")



    def send_verification_code(self, email):
        code = str(random.randint(100000, 999999))
        msg = MIMEText(f'Your verification code is: {code}')
        msg['Subject'] = 'Your Verification Code'
        msg['From'] = sender_email
        msg['To'] = email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())
            return code
        except Exception as e:
            print(f'Error sending email: {e}')
            return None

    def verify_code(self, correct_code, entered_code):
        return correct_code == entered_code

    def show_login_screen(self):
        self.setup_login_screen()  # Reset to the login screen

    def validate_email(self, event=None):
        email = self.email_entry.get()
        # Regular expression for validating an email
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, email):
            self.email_status_label.configure(text="Email Entered", text_color="black", fg_color="white", bg_color="white")
        else:
            self.email_status_label.configure(text="Incorrect Email Format", text_color="red", fg_color="white", bg_color="white")
    def sign_in(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if self.email_status_label.cget("text") == "Email Entered" and password:
            user = users_col.find_one({"email": email})

            if user and user['passwordHash'] == password_hash:
                print("Login successful")
                self.user_id = user['_id']
                self.user_name = user.get('name', 'User')  # Default to 'User' if name is not available
                self.school = user['school']

                # Send verification code
                self.correct_code = self.send_verification_code(email)
                if self.correct_code:
                    # Clear current content and ask for verification code
                    self.clear_window()

                    def on_verify():
                        entered_code = self.code_entry.get()
                        if self.verify_code(self.correct_code, entered_code):
                            self.clear_window()
                            self.create_new_layout()  # Create a new layout after successful login
                        else:
                            self.verification_error_label.configure(text="Invalid Verification Code", text_color="red")

                    def resend_verification_code():
                        self.correct_code = self.send_verification_code(email)
                        if self.correct_code:
                            messagebox.showinfo("Success", "Verification code resent.")
                        else:
                            messagebox.showerror("Error", "Error resending verification code.")

                    background_frame = ctk.CTkFrame(self, bg_color='white', fg_color="white")
                    background_frame.pack(fill='both', expand=True)
                    background_frame.lower(belowThis=None)

                    # Title label
                    title_label = ctk.CTkLabel(background_frame, text="Enter Verification Code", font=("Roboto Medium", 50), fg_color="white", bg_color="white")
                    title_label.pack(pady=20)

                    # Verification code entry
                    self.code_entry = ctk.CTkEntry(background_frame, placeholder_text="Verification Code", width=500, height=50, font=("Roboto Medium", 25))
                    self.code_entry.pack(pady=(25,0))

                    # Error label for verification code
                    self.verification_error_label = ctk.CTkLabel(background_frame, text="", font=("Roboto Medium", 20), fg_color="white", bg_color="white")
                    self.verification_error_label.pack(pady=(10, 0))

                    # Verify button
                    verify_button = ctk.CTkButton(background_frame, text="Verify", text_color="white", hover_color="#444444", font=("Roboto Medium", 20), fg_color="black", width=250, height=45, command=on_verify)
                    verify_button.pack(pady=15)

                    # Resend Verification Code button
                    resend_button = ctk.CTkButton(background_frame, text="Resend Verification Code", text_color="white", hover_color="#444444", font=("Roboto Medium", 20), fg_color="black", width=250, height=45, command=resend_verification_code)
                    resend_button.pack()

                    # Logo at the bottom left
                    logo_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
                    logo_frame.pack(side="bottom", anchor="w", padx=20, pady=20)

                    # Open the image
                    logo_image = Image.open("./assets/menulogo.png")
                    original_width, original_height = logo_image.size
                    new_width = int(original_width * 0.75)
                    new_height = int(original_height * 0.75)
                    logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    logo_photo = ImageTk.PhotoImage(logo_image)

                    # Create a label to hold the image, inside the logo_frame
                    logo_label = ctk.CTkLabel(logo_frame, text="", image=logo_photo, bg_color='white')
                    logo_label.image = logo_photo  # Keep a reference to the image
                    logo_label.pack(anchor="w")

                else:
                    self.login_error_label.configure(text="Error sending verification code", text_color="red", fg_color="white", bg_color="white", font=("Roboto Medium", 20))
                    self.login_error_label.pack(pady=10)
            else:
                self.login_error_label.configure(text="Invalid Credentials", text_color="red", fg_color="white", bg_color="white", font=("Roboto Medium", 20))
        else:
            self.login_error_label.configure(text="Invalid Credentials", text_color="red", fg_color="white", bg_color="white", font=("Roboto Medium", 20))

    def create_new_layout(self):
            self.geometry("1000x650")
            background_frame = ctk.CTkFrame(self, bg_color='white', fg_color="white")
            background_frame.pack(fill='both', expand=True)
            background_frame.lower(belowThis=None)

            # Greeting label with user's name
            welcome_label = ctk.CTkLabel(background_frame, text=f"Welcome, {self.user_name}!", font=("Roboto Medium", 50))
            welcome_label.pack(pady=(10, 0), padx=15, anchor="nw")
            school_label = ctk.CTkLabel(background_frame, text=f"{self.school}", font=("Roboto Medium", 25))
            school_label.pack(pady=(0, 15), padx=17, anchor="nw")

            # Frame to contain the buttons, packed to the center
            buttons_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
            buttons_frame.pack(expand=True, padx=20, pady=20)

            buttonWidth = 125
            buttonHeight = 125
            buttonFont = ("Roboto Medium", 20)

            # Load the images for the buttons
            images = ["./assets/button1.png", "./assets/button2.png", "./assets/button3.png",
                    "./assets/button4.png", "./assets/button5.png", "./assets/button7.png", "./assets/button6.png"]

            button_images = []
            for image_path in images:
                image = Image.open(image_path)
                image = image.resize((buttonWidth, buttonHeight), Image.Resampling.LANCZOS)
                button_images.append(ImageTk.PhotoImage(image))

            # Create buttons in a 4x3 grid
            button_texts = ["Current Partners", "Contact", "Add New Partners",
                            "Find New Partners", "Account Settings", "Export Data", "Logout"]
            button_commands = [
                lambda: partnerManager.create_and_show_treeview(self, self.return_to_main_menu),
                lambda: contact.switch_to_contact_window(self, self.return_to_main_menu),
                lambda: addPartner.create_add_partner_form(self, self.return_to_main_menu),
                lambda: searchPartners.create_search_form(self, self.return_to_main_menu),
                lambda: accountSettings.create_account_settings_form(self, self.user_id, self.return_to_main_menu),
                lambda: export.create_export_form(self, self.return_to_main_menu),  # New export button command
                lambda: self.show_login_screen()
            ]

            for i in range(2):
                for j in range(4):
                    index = i * 4 + j
                    if index < len(button_texts):
                        button = ctk.CTkButton(
                            buttons_frame,
                            text=button_texts[index],
                            image=button_images[index],
                            compound="top",
                            width=buttonWidth,
                            height=buttonHeight,
                            font=buttonFont,
                            fg_color="white",
                            bg_color="white",
                            text_color="black",
                            hover_color="#444444",
                            command=button_commands[index]
                        )
                        if i == 1:  # For the second row
                            button.grid(row=i, column=j, padx=40, pady=10, columnspan=2)  # Span two columns
                        else:
                            button.grid(row=i, column=j, padx=40, pady=10)

            # Frame to contain the logo, packed to the bottom left
            logo_frame = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
            logo_frame.pack(side="bottom", anchor="w", padx=20, pady=20)

            # Open the image
            logo_image = Image.open("./assets/menulogo.png")
            original_width, original_height = logo_image.size
            new_width = int(original_width * 0.75)
            new_height = int(original_height * 0.75)
            logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)

            # Create a label to hold the image, inside the logo_frame
            logo_label = ctk.CTkLabel(logo_frame, text="", image=logo_photo, bg_color='white')
            logo_label.image = logo_photo  # Keep a reference to the image
            logo_label.pack(anchor="w")

            # Load the help icon image
            help_icon = Image.open("assets/helpIcon.png")
            help_icon = help_icon.resize((75, 75), Image.Resampling.LANCZOS)
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
