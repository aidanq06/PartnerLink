import tkinter as tk
import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk

def show_answer(frame, answer_text, return_to_main):
    for widget in frame.winfo_children():
        widget.destroy()
    ctk.CTkLabel(frame, text=answer_text, font=("Roboto Medium", 18), wraplength=frame.winfo_width()).pack(pady=5, anchor='w')
    clear_button = ctk.CTkButton(frame, text="Clear", font=("Roboto Medium", 18), fg_color="transparent", hover_color="#444444", text_color="black", command=lambda: clear_answer(frame, add_logo_and_back_button, return_to_main))
    clear_button.pack(pady=10)

def clear_answer(frame, callback, return_to_main):
    for widget in frame.winfo_children():
        widget.destroy()
    callback(frame, return_to_main)

def add_logo_and_back_button(frame, return_to_main):
    right = frame

    logo_image = Image.open("./assets/logoSlogan.png")
    original_width, original_height = logo_image.size
    new_width = int(original_width * 0.75)
    new_height = int(original_height * 0.75)
    logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(right, text="", image=logo_photo, bg_color='white')
    logo_label.image = logo_photo
    logo_label.pack(pady=40)

    hyperlink_label = ctk.CTkLabel(right, text="PartnerLink GitHub Page", font=("Roboto Medium", 24), text_color="blue", fg_color="transparent", cursor="hand2")
    hyperlink_label.pack()
    hyperlink_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/aidanq06/PartnerLink"))

    back_button = ctk.CTkButton(right, width=175, height=35, text="Back", command=return_to_main, fg_color="black", bg_color="transparent", hover_color="#444444", text_color="white", font=("Roboto Medium", 25))
    back_button.pack(pady=10)

def create_help_window(root, return_to_main):
    for widget in root.winfo_children():
        widget.destroy()

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    left = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    left.pack(side="left", fill='both', expand=True, padx=15)

    right = ctk.CTkFrame(background_frame, bg_color='white', fg_color="white")
    right.pack(side="right", fill='both', expand=True, padx=10, anchor="e")

    label_width = root.winfo_width() // 2

    ctk.CTkLabel(left, text="PartnerLink Help Guide", font=("Roboto Medium", 36)).pack(pady=5, anchor='w')

    qna_frame = ctk.CTkFrame(left, bg_color='white', fg_color="white")
    qna_frame.pack(fill='both', expand=True)

    questions_answers = [
    ("How to Login", 
     "Learn how to login to your PartnerLink account. Follow these steps to access your account securely.\n\n"
     "Q: What credentials do I need to login?\n"
     "A: You need your registered email address and password to login.\n\n"
     "Q: What should I do if I forget my password?\n"
     "A: Use the 'Forgot Password' link on the login screen to reset your password via email.\n\n"
     "Q: How do I validate my email format?\n"
     "A: The system will automatically check the format of your email when you enter it. Ensure it follows the standard email format (e.g., example@domain.com).\n\n"
     "Q: What happens if I enter incorrect login credentials?\n"
     "A: You will see an error message indicating 'Invalid Credentials'. Please re-enter your correct email and password."),

    ("How to Register", 
     "Follow these steps to create a new PartnerLink account. Ensure you provide accurate information to register successfully.\n\n"
     "Q: What information is required to register?\n"
     "A: You need to provide your full name, email address, and create a password.\n\n"
     "Q: Can I use any email address to register?\n"
     "A: Yes, but it must be a valid and active email address to receive the verification code.\n\n"
     "Q: How do I verify my email address?\n"
     "A: After registering, you will receive a verification code via email. Enter this code on the verification screen to complete your registration.\n\n"
     "Q: What should I do if I don't receive the verification email?\n"
     "A: Check your spam/junk folder. If you still don't receive it, use the 'Resend Verification Code' option."),

    ("How Data is Stored", 
     "Understand how PartnerLink stores your data securely. Learn about the measures taken to protect your information.\n\n"
     "Q: Where is my data stored?\n"
     "A: Your data is stored in a secure MongoDB database hosted on a cloud server.\n\n"
     "Q: Is my data encrypted?\n"
     "A: Yes, sensitive data, including passwords, are encrypted to ensure security.\n\n"
     "Q: Who has access to my data?\n"
     "A: Only authorized personnel have access to your data. We follow strict access control measures.\n\n"
     "Q: How often is my data backed up?\n"
     "A: Data is backed up regularly to prevent loss and ensure availability."),

    ("How Password is Encrypted (SHA-256)", 
     "Learn about the security measures PartnerLink uses to encrypt your password.\n\n"
     "Q: What encryption algorithm is used for passwords?\n"
     "A: PartnerLink uses the SHA-256 encryption algorithm to hash your password.\n\n"
     "Q: How does SHA-256 work?\n"
     "A: SHA-256 converts your password into a fixed-length string of characters, which is irreversible and unique.\n\n"
     "Q: Why is encryption important?\n"
     "A: Encryption protects your password from being easily read or accessed by unauthorized individuals.\n\n"
     "Q: Can the encrypted password be decrypted?\n"
     "A: No, SHA-256 is a one-way hashing algorithm, meaning the original password cannot be retrieved from the hash."),

    ("Email Requirements", 
     "Ensure your email meets the necessary requirements for registration and communication within PartnerLink.\n\n"
     "Q: What is a valid email format?\n"
     "A: A valid email format includes a local part, an '@' symbol, and a domain (e.g., user@example.com).\n\n"
     "Q: Why do I need a valid email address?\n"
     "A: A valid email address is required for account verification, password recovery, and communication.\n\n"
     "Q: What should I do if my email is not accepted?\n"
     "A: Double-check the format and ensure there are no typos. If the issue persists, contact support.\n\n"
     "Q: Can I change my email address after registration?\n"
     "A: Yes, you can update your email address in the 'Account Settings' section."),

    ("About PartnerLink", 
     "Learn more about PartnerLink and how it can help manage your partnerships efficiently.\n\n"
     "Q: What is PartnerLink?\n"
     "A: PartnerLink is a comprehensive platform designed to help manage business and community partnerships effectively.\n\n"
     "Q: Who can use PartnerLink?\n"
     "A: PartnerLink is intended for educational institutions, non-profits, and businesses looking to manage their partnerships.\n\n"
     "Q: What features does PartnerLink offer?\n"
     "A: PartnerLink offers features such as partner management, contact capabilities, data export, and customizable settings.\n\n"
     "Q: How can I get support for using PartnerLink?\n"
     "A: Use the 'Help' section within the application or contact our support team for assistance.")
]


    for question, answer in questions_answers:
        btn = ctk.CTkButton(qna_frame, text=question, font=("Roboto Medium", 24), fg_color="transparent", hover_color="#444444", text_color="black", anchor='w', command=lambda a=answer: show_answer(right, a, return_to_main))
        btn.pack(fill='x', pady=5, anchor='w')

    add_logo_and_back_button(right, return_to_main)

# Additional functionality as needed
