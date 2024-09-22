import tkinter as tk
from tkinter import ttk, messagebox

import requests

from modem_status import ModemStatus
from new_sms import SendSMS
from sms_view import SMSView


class ModemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D-LINK Modem DWR-930M")

        self.root.geometry("400x420")

        if self.check_modem_connection():
            self.create_notebook()
        else:
            self.root.destroy()

    def check_modem_connection(self):
        url = "http://192.168.0.1"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            messagebox.showerror("Connection Error", "Not connected to the modem. Please connect to the modem first.")
            return False

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=5)

        self.modem_status = ModemStatus(self.notebook)
        self.notebook.add(self.modem_status.frame, text="Modem Status")

        self.sms_view = SMSView(self.notebook)
        self.notebook.add(self.sms_view.frame, text="SMS List")

        self.send_sms_view = SendSMS(self.notebook)
        self.notebook.add(self.send_sms_view.frame, text="Send SMS")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModemApp(root)
    root.mainloop()
