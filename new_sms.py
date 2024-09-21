import tkinter as tk
from tkinter import messagebox
import requests


class SendSMS:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.create_send_sms_view()

    def create_send_sms_view(self):
        tk.Label(self.frame, text="Phone Number:", font=("Arial", 12)).pack(pady=5)
        self.phone_entry = tk.Entry(self.frame, width=30, font=("Arial", 12))
        self.phone_entry.pack(pady=5)

        tk.Label(self.frame, text="Message Content:", font=("Arial", 12)).pack(pady=5)
        self.message_text = tk.Text(self.frame, height=6, width=50, font=("Arial", 12))
        self.message_text.pack(pady=5)

        self.send_button = tk.Button(self.frame, text="Send Message", command=self.send_sms, font=("Arial", 12))
        self.send_button.pack(pady=10)

    def send_sms(self):
        phone_number = self.phone_entry.get()
        message_content = self.message_text.get("1.0", tk.END).strip()

        if not phone_number or not message_content:
            messagebox.showerror("Error", "Please enter both phone number and message content.")
            return

        url = f"http://192.168.0.1/PostMessageList?MessageList=%7B%22pnumber%22%3A%22{phone_number}%22%2C%22content%22%3A%22{message_content}%22%7D"
        try:
            response = requests.get(url)
            response.raise_for_status()
            messagebox.showinfo("Success", "Message sent successfully!")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")
