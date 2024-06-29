import tkinter as tk
import customtkinter as ctk
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
import json
import imaplib
import email
from email.header import decode_header

# Database connection
with open("./assets/variables.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']
    password = data["password"]
    sender_email = data["sender_email"]

client = MongoClient(conn_str)
db = client['partnerlink']
partners_col = db['partners']

def fetch_email_content(sender_email, password, email_id):
    with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
        mail.login(sender_email, password)
        mail.select('inbox')
        status, data = mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            return None
        
        email_msg = email.message_from_bytes(data[0][1])
        subject = decode_header(email_msg['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        from_ = email_msg['From']
        # Extracting the body of the email
        if email_msg.is_multipart():
            for part in email_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_msg.get_payload(decode=True).decode()
            
        return {"from": from_, "subject": subject, "body": body}

def fetch_replies(sender_email, password):
    replies = []
    with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
        mail.login(sender_email, password)
        mail.select('inbox')
        status, messages = mail.search(None, '(SUBJECT "Re:")')
        if status != 'OK':
            return replies
        
        for num in messages[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            if status != 'OK':
                continue
            email_msg = email.message_from_bytes(data[0][1])
            subject = decode_header(email_msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            from_ = email_msg['From']
            replies.append({"id": num.decode(), "from": from_, "subject": subject})
    return replies

def send_email(sender_email, receiver_email, password, subject, body, return_to_main):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        messagebox.showinfo("Success", "Email sent successfully.")
        return_to_main()  # Return to the main menu
    except Exception as e:
        print(f"Error: {e}")

def fetch_company_details():
    # Fetch company names and emails from the MongoDB database
    return {company['companyName']: company['contactEmail'] for company in partners_col.find({}, {'companyName': 1, 'contactEmail': 1})}

def update_email_input(selected_company, company_details, email_input):
    # Update the email input box with the selected company's email
    email_input.delete(0, tk.END)
    email_input.insert(0, company_details.get(selected_company, ""))
def switch_to_contact_window(root, return_to_main):
    root.geometry("1000x650")
    # Clear existing content in the root widget
    for widget in root.winfo_children():
        widget.destroy()

    background_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
    background_frame.pack(fill='both', expand=True)
    background_frame.lower(belowThis=None)

    # Split the window into two frames
    left_frame = ctk.CTkFrame(background_frame, fg_color="white", bg_color="white")
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = ctk.CTkFrame(background_frame, fg_color="white", bg_color="white")
    right_frame.pack(side="right", fill="both", expand=True)

    # Title for the right frame
    title_label = ctk.CTkLabel(right_frame, text="Contact Companies", font=("Roboto Medium", 40), fg_color="white", bg_color="white")
    title_label.pack(pady=20)

    # Input boxes for email, subject, and content
    email_input = ctk.CTkEntry(right_frame, placeholder_text="Company Email", width=400, height=35, font=("Roboto Medium", 18))
    email_input.pack(pady=5)

    subject_input = ctk.CTkEntry(right_frame, placeholder_text="Subject", width=400, height=35, font=("Roboto Medium", 18))
    subject_input.pack(pady=5)

    content_input = ctk.CTkTextbox(right_frame, width=400, height=150, font=("Roboto Medium", 15))
    content_input.pack(pady=(5, 10))

    # Fetch companies and create checkboxes in the scrollable frame
    company_details = fetch_company_details()
    selected_company = tk.StringVar(value="")

    # Scrollable frame in the left frame for company selection
    scrollable_frame = ctk.CTkFrame(left_frame, bg_color='white', fg_color='white')
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

    canvas_widget = tk.Canvas(scrollable_frame, bg='white', highlightthickness=0)
    scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas_widget.yview)
    inner_frame = ctk.CTkFrame(canvas_widget, bg_color='white', fg_color='white')

    inner_frame.bind(
        "<Configure>",
        lambda e: canvas_widget.configure(
            scrollregion=canvas_widget.bbox("all")
        )
    )

    canvas_widget.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas_widget.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas_widget.pack(side="left", fill="both", expand=True)

    for company, email in company_details.items():
        check_btn = ctk.CTkCheckBox(inner_frame, text=company, variable=selected_company, onvalue=company, 
                                    command=lambda c=company: update_email_input(c, company_details, email_input),
                                    font=("Roboto Medium", 18), bg_color='white', fg_color="white", hover_color="#444444", corner_radius=0)
        check_btn.pack(pady=5, fill='x')


    # Button to confirm the selection and send an email
    def on_send_email():
        receiver_email = email_input.get()
        subject = subject_input.get()
        body = content_input.get("1.0", tk.END)
        
        # Validate the email and subject before sending
        if receiver_email and subject and body.strip():
            send_email(sender_email, receiver_email, password, subject, body, return_to_main)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    confirm_button = ctk.CTkButton(right_frame, text="Send Email", text_color="white", hover_color="#444444", font=("Roboto Medium", 20), fg_color="black", command=on_send_email, width=250, height=45)
    confirm_button.pack(pady=10)

    def on_view_replies():
        # Clear existing content in the root widget
        for widget in root.winfo_children():
            widget.destroy()

        replies_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
        replies_frame.pack(fill='both', expand=True, pady=20)

        # Fetch replies
        replies = fetch_replies(sender_email, password)

        # Scrollable frame for replies
        scrollable_frame = ctk.CTkFrame(replies_frame, bg_color='white', fg_color='white')
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        canvas_widget = tk.Canvas(scrollable_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas_widget.yview)
        inner_frame = ctk.CTkFrame(canvas_widget, bg_color='white', fg_color='white')

        inner_frame.bind(
            "<Configure>",
            lambda e: canvas_widget.configure(
                scrollregion=canvas_widget.bbox("all")
            )
        )

        canvas_widget.create_window((0, 0), window=inner_frame, anchor="nw")
        canvas_widget.configure(yscrollcommand=scrollbar.set)

        canvas_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        selected_reply = tk.StringVar(value="")
        
        if replies:
            for reply in replies:
                option_text = f"{reply['from']} - {reply['subject']}"
                radio_btn = ctk.CTkRadioButton(inner_frame, font=("Roboto Medium", 18), text=option_text, variable=selected_reply, value=reply['id'],
                                            command=lambda: print(selected_reply.get()))
                radio_btn.pack(pady=5, fill='x')
        else:
            no_reply_label = ctk.CTkLabel(inner_frame, text="No replies found", font=("Roboto Medium", 20), fg_color="#dbdbdb", bg_color="white")
            no_reply_label.pack()

        def view_full_email():
            email_id = selected_reply.get()
            if email_id:
                email_content = fetch_email_content(sender_email, password, email_id)
                if email_content:
                    # Clear existing content
                    for widget in root.winfo_children():
                        widget.destroy()

                    email_frame = ctk.CTkFrame(root, bg_color='white', fg_color="white")
                    email_frame.pack(fill='both', expand=True, pady=20)

                    from_label = ctk.CTkLabel(email_frame, text=f"{email_content['from']}", font=("Roboto Medium", 20), fg_color="white", bg_color="white")
                    from_label.pack(pady=5)

                    subject_label = ctk.CTkLabel(email_frame, text=f"{email_content['subject']}", font=("Roboto Medium", 20), fg_color="white", bg_color="white")
                    subject_label.pack(pady=5)

                    def remove_quoted_text(email_body):
                        lines = email_body.splitlines()
                        # Assuming the quoted text starts after the line containing "wrote:"
                        unquoted_lines = []
                        for line in lines:
                            if line.strip().endswith("wrote:"):
                                break
                            unquoted_lines.append(line)
                        return '\n'.join(unquoted_lines).strip()

                    # Use this function in the 'fetch_email_content' function after extracting the body
                    email_content['body'] = remove_quoted_text(email_content['body'])

                    body_label = ctk.CTkLabel(email_frame, text=f"{email_content['body']}", font=("Roboto Medium", 20), fg_color="white", bg_color="white")
                    body_label.pack(pady=5)

                    # Button to go back to replies
                    back_to_replies_button = ctk.CTkButton(email_frame, text="Back", command=on_view_replies, hover_color="#444444", fg_color='black', width=300, height=50, font=("Roboto Medium", 25))
                    back_to_replies_button.pack(side=tk.BOTTOM, pady=10)
                else:
                    messagebox.showerror("Error", "Failed to fetch the email content.")
            else:
                messagebox.showinfo("Select an Email", "Please select an email to view.")

        # Frame for holding the buttons
        buttons_frame = ctk.CTkFrame(replies_frame, fg_color='white', bg_color='white')
        buttons_frame.pack(fill='x', pady=10)

        # Button to view full email
        view_button = ctk.CTkButton(buttons_frame, text="View Email", command=view_full_email, hover_color="#444444", fg_color='black', width=300, height=50, font=("Roboto Medium", 25))
        view_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        # Button to return to the contact window
        back_button = ctk.CTkButton(buttons_frame, text="Back", hover_color="#444444", command=lambda: switch_to_contact_window(root, return_to_main), fg_color='black', width=300, height=50, font=("Roboto Medium", 25))
        back_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

    replies = ctk.CTkButton(right_frame, text="View Replies", text_color="white", font=("Roboto Medium", 20), hover_color="#444444", fg_color="black", command=on_view_replies, width=250, height=45)
    replies.pack(pady=10)

    # Back button to return to the main menu
    back_button = ctk.CTkButton(right_frame, text="Back", text_color="white", font=("Roboto Medium", 20), hover_color="#444444", fg_color="black", command=return_to_main, width=250, height=45)
    back_button.pack(pady=10)
