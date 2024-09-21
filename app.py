import tkinter as tk
from tkinter import ttk

from modem_status import ModemStatus
from new_sms import SendSMS
from sms_view import SMSView


class ModemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D-LINK Modem DWR-930M")

        self.root.geometry("400x420")

        self.create_notebook()

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
