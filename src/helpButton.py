import tkinter as tk
import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk

def show_answer(frame, answer_text, return_to_main):
    # Clear the frame content
    for widget in frame.winfo_children():
        widget.destroy()
    # Display the answer
    ctk.CTkLabel(frame, text=answer_text, font=("Roboto Medium", 18), wraplength=frame.winfo_width()).pack(pady=5, anchor='w')
    # Add a "Clear" button to clear the answer
    clear_button = ctk.CTkButton(frame, text="Clear", font=("Roboto Medium", 18), fg_color="transparent", hover_color="#444444", text_color="black", command=lambda: clear_answer(frame, add_logo_and_back_button, return_to_main))
    clear_button.pack(pady=10)

def clear_answer(frame, callback, return_to_main):
    for widget in frame.winfo_children():
        widget.destroy()
    # Re-add the logo and back button
    callback(frame, return_to_main)

def add_logo_and_back_button(frame, return_to_main):
    # Frame to contain the picture, packed to the right side
    right = frame

    # LOGO
    logo_image = Image.open("./assets/logoSlogan.png") 
    original_width, original_height = logo_image.size
    new_width = int(original_width * 0.75)
    new_height = int(original_height * 0.75)
    logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(right, text="", image=logo_photo, bg_color='white')
    logo_label.image = logo_photo  # Keep a reference to the image
    logo_label.pack(pady=40)

    # HYPERLINK
    hyperlink_label = ctk.CTkLabel(right, text="PartnerLink GitHub Page", font=("Roboto Medium", 24), text_color="blue", fg_color="transparent", cursor="hand2")
    hyperlink_label.pack()
    hyperlink_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/aidanq06/PartnerLink"))

    # Back Button
    back_button = ctk.CTkButton(right, width=175, height=35, text="Back", command=return_to_main, fg_color="black", bg_color="transparent", hover_color="#444444", text_color="white", font=("Roboto Medium", 25))
    back_button.pack(pady=10)

def create_help_window(root, return_to_main):
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

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
    ctk.CTkLabel(left, text="PartnerLink Help Guide", font=("Roboto Medium", 36)).pack(pady=5, anchor='w')

    qna_frame = ctk.CTkFrame(left, bg_color='white', fg_color="white")
    qna_frame.pack(fill='both', expand=True)

    questions_answers = [
        ("Current Partners", 
        "Click here to view a list of all the partners associated with the program. This is where you can browse through existing partnerships and view detailed information.\n\n"
        "Q: How do I view the details of a specific partner?\n"
        "A: Click on the partner's name in the list to view detailed information about the partner, including contact details and partnership history.\n\n"
        "Q: Can I search for a specific partner?\n"
        "A: Yes, use the search bar at the top to type in the name or other relevant details of the partner you are looking for.\n\n"
        "Q: How do I edit a partner's information?\n"
        "A: Click on the partner's name to open their details and then click on the 'Edit' button to modify their information.\n\n"
        "Q: Can I delete a partner from the list?\n"
        "A: Yes, you can select the partner and click on the 'Delete' button to remove them from the list.\n\n"
        "Q: Is there a way to filter partners by type?\n"
        "A: Yes, use the filter options to narrow down the list of partners by type, such as for-profit, non-profit, etc.\n\n"
        "Q: Is there a way to contact a partner directly from the list?\n"
        "A: Yes, click on the partner's email address to open your default email client and send a message directly."),

        ("Add New Partners", 
        "Use this button to input new business and community partners into PartnerLink. It's a simple form that lets you expand your network.\n\n"
        "Q: What information do I need to add a new partner?\n"
        "A: You need the company name, type of business, contact email, contact phone number, resources, and a description of the partner.\n\n"
        "Q: Can I edit the details of a new partner after adding them?\n"
        "A: Yes, once the partner is added, you can go to the 'Current Partners' section to edit their details.\n\n"
        "Q: How do I ensure the email format is correct when adding a partner?\n"
        "A: The system will validate the email format automatically. If the format is incorrect, you will receive an error message.\n\n"
        "Q: Can I add multiple partners at once?\n"
        "A: No, you need to add each partner individually by filling out the form for each one.\n\n"
        "Q: What should I do if I make a mistake while filling out the form?\n"
        "A: Simply correct the mistake before submitting the form. If you realize a mistake after submission, you can edit the partner's details in the 'Current Partners' section.\n\n"
        "Q: How do I save the information entered if I am not ready to submit?\n"
        "A: Use the 'Save as Draft' option to save the information without submitting it."),

        ("Add New Login", 
        "This feature allows you to create additional login credentials. Ideal for granting access to new users who need to work with your school.\n\n"
        "Q: What information is required to create a new login?\n"
        "A: You need to provide a username, email address, and password for the new user.\n\n"
        "Q: Can I assign different roles to new users?\n"
        "A: Yes, you can specify the role of the new user during the login creation process.\n\n"
        "Q: How do I manage the logins created?\n"
        "A: You can manage all user logins in the 'Account Settings' section, where you can edit or delete user accounts.\n\n"
        "Q: Can I deactivate a user account without deleting it?\n"
        "A: Yes, you can deactivate a user account in the account management settings.\n\n"
        "Q: Is there a limit to the number of logins I can create?\n"
        "A: There is no specified limit; however, it is recommended to manage the number of active users efficiently.\n\n"
        "Q: How do I update a user's role?\n"
        "A: You can update a user's role in the 'Account Settings' section by selecting the user and changing their role."),

        ("Account Settings", 
        "Customize your PartnerLink experience by managing your personal settings. Update your profile, change your password, and more.\n\n"
        "Q: How do I update my profile information?\n"
        "A: Click on the 'Account Settings' button and edit your profile information in the provided fields.\n\n"
        "Q: Can I change my password in this section?\n"
        "A: Yes, you can change your password by entering your current password and the new password.\n\n"
        "Q: What should I do if I forget my password?\n"
        "A: Use the 'Forgot Password' feature on the login screen to reset your password.\n\n"
        "Q: Can I update my email address in the account settings?\n"
        "A: Yes, you can update your email address in the account settings.\n\n"
        "Q: Are there any security measures in place for changing sensitive information?\n"
        "A: Yes, you may be required to enter your current password to verify your identity before changing sensitive information.\n\n"
        "Q: How do I deactivate my account?\n"
        "A: You can deactivate your account by going to 'Account Settings' and selecting the 'Deactivate Account' option."),

        ("Export Data", 
        "The 'Export Data' feature allows you to export information about your partners into a PDF format. You can select which partners to export and customize the export format.\n\n"
        "Q: How do I select partners to export?\n"
        "A: Use the checklist to select the partners you want to include in the export.\n\n"
        "Q: Can I customize the information included in the export?\n"
        "A: Yes, you can choose to include phone numbers, emails, and select the type of chart to be included in the PDF.\n\n"
        "Q: What formats are available for export?\n"
        "A: Currently, the information is exported in PDF format.\n\n"
        "Q: How do I include a chart in the export?\n"
        "A: Select the chart type from the dropdown menu to include it in the exported PDF.\n\n"
        "Q: Can I export data for all partners at once?\n"
        "A: Yes, you can use the 'Select All' checkbox to include all partners in the export.\n\n"
        "Q: Is there a limit to the number of partners I can export?\n"
        "A: No, you can export as many partners as needed, depending on your selection."),

        ("Contact", 
        "The 'Contact' section enables you to send emails to the partners directly from the application. You can select partners, compose an email, and send it, as well as view replies.\n\n"
        "Q: How do I select a partner to contact?\n"
        "A: Use the scrollable list on the left to select a partner by clicking on their name.\n\n"
        "Q: Can I send emails to multiple partners at once?\n"
        "A: No, you can only send emails to one partner at a time using the 'Contact' section.\n\n"
        "Q: How do I view replies to my emails?\n"
        "A: Click on the 'View Replies' button to see a list of replies from partners.\n\n"
        "Q: Can I save a draft of my email to send later?\n"
        "A: No, the current version does not support saving drafts. You need to send the email immediately after composing it.\n\n"
        "Q: What happens if I enter an incorrect email address?\n"
        "A: The system will show an error message if the email format is incorrect. If the email is not deliverable, you will receive a failure notice.\n\n"
        "Q: How do I confirm that the email was sent successfully?\n"
        "A: After sending, you will receive a confirmation message indicating the email was sent successfully."),

        ("Logout", 
        "Safely exit your session with this button. It ensures that your information remains secure when you're done using the application.\n\n"
        "Q: How do I logout of my account?\n"
        "A: Click the 'Logout' button on the main menu to safely exit your session.\n\n"
        "Q: Will I be logged out automatically after a period of inactivity?\n"
        "A: Yes, for security reasons, you may be logged out automatically after a period of inactivity.\n\n"
        "Q: Can I log back in immediately after logging out?\n"
        "A: Yes, you can log back in using your credentials immediately after logging out.\n\n"
        "Q: What happens to my unsaved work if I log out?\n"
        "A: Ensure you save any changes or work before logging out, as unsaved work will be lost.\n\n"
        "Q: Is there a confirmation prompt before logging out?\n"
        "A: Yes, you may receive a confirmation prompt to ensure you intend to log out.\n\n"
        "Q: Can I log out from multiple devices at once?\n"
        "A: No, you need to log out from each device individually."),

        ("Find New Partners", 
        "The 'Find New Partners' feature allows you to search for potential new partners to expand your network. You can use various filters and search criteria to find the best matches.\n\n"
        "Q: How do I search for new partners?\n"
        "A: Use the search bar to enter keywords or use the filters to narrow down your search based on specific criteria.\n\n"
        "Q: What filters are available for finding new partners?\n"
        "A: You can filter by industry, location, type of business, and more.\n\n"
        "Q: Can I save my search criteria for future use?\n"
        "A: Yes, you can save your search criteria to quickly find new partners in the future.\n\n"
        "Q: How do I contact a new partner found through the search?\n"
        "A: Click on the partner's name to view their details and use the 'Contact' button to send them an email.\n\n"
        "Q: Can I add a new partner directly from the search results?\n"
        "A: Yes, you can add a new partner directly from the search results by clicking the 'Add Partner' button.\n\n"
        "Q: Can I provide feedback on the search results?\n"
        "A: Yes, you can provide feedback to improve the search feature by using the 'Feedback' option."),

        ("Help", 
        "The 'Help' section provides you with guidance and answers to common questions about using PartnerLink. You can find detailed instructions and troubleshooting tips for all features.\n\n"
        "Q: How do I access the help guide?\n"
        "A: Click on the 'Help' button in the main menu to open the help guide.\n\n"
        "Q: What topics are covered in the help guide?\n"
        "A: The help guide covers all features of PartnerLink, including Current Partners, Add New Partners, Add New Login, Account Settings, Export Data, Contact, Find New Partners, and Logout.\n\n"
        "Q: Can I search for specific help topics?\n"
        "A: Yes, use the search bar in the help section to find specific topics or questions.\n\n"
        "Q: How do I contact support if I need further assistance?\n"
        "A: Use the 'Contact Support' button in the help section to get in touch with our support team.\n\n"
        "Q: Is there a user manual available for download?\n"
        "A: Yes, you can download the user manual from the help section.\n\n"
        "Q: Is the help guide available in multiple languages?\n"
        "A: Currently, the help guide is available only in English.")
    ]

    for question, answer in questions_answers:
        btn = ctk.CTkButton(qna_frame, text=question, font=("Roboto Medium", 24), fg_color="transparent", hover_color="#444444", text_color="black", anchor='w', command=lambda a=answer: show_answer(right, a, return_to_main))
        btn.pack(fill='x', pady=5, anchor='w')

    # Add logo and back button initially
    add_logo_and_back_button(right, return_to_main)

# Additional functionality as needed
