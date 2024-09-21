import tkinter as tk
from tkinter import messagebox, RIGHT, LEFT, BOTH, Y, Frame, Text, Scrollbar
import requests


class SMSView:
    def __init__(self, parent):
        self.page_index = 1
        self.total_pages = 1

        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10, fill=BOTH, expand=True)

        self.create_sms_view()

    def create_sms_view(self):
        # فریم برای نمایش پیام‌ها
        display_frame = tk.Frame(self.frame)
        display_frame.pack(pady=10, fill=BOTH, expand=True)

        scrollbar = Scrollbar(display_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.sms_display = Text(display_frame, width=100, height=20, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.sms_display.pack(side=LEFT, padx=10, fill=BOTH, expand=True)
        scrollbar.config(command=self.sms_display.yview)

        # فریم برای دکمه‌ها
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=10)

        self.prev_page_button = tk.Button(button_frame, text="Previous Page", command=self.prev_page, state=tk.DISABLED)
        self.prev_page_button.pack(side=LEFT, padx=5)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=lambda: self.refresh_sms(go_to_first_page=True))
        self.refresh_button.pack(side=LEFT, padx=5)

        self.next_page_button = tk.Button(button_frame, text="Next Page", command=self.next_page)
        self.next_page_button.pack(side=LEFT, padx=5)

        self.refresh_sms()

    def refresh_sms(self, go_to_first_page=False):
        if go_to_first_page:
            self.page_index = 1

        total_pages_val, cur_page_val = self.fetch_sms()
        self.total_pages = total_pages_val

        # تنظیم وضعیت دکمه‌های صفحه‌بندی
        self.update_pagination_buttons()

    def fetch_sms(self):
        url = f"http://192.168.0.1/PageList?pageIndex={self.page_index}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            sms_data = response.json()
            self.populate_sms_list(sms_data['data'])
            return sms_data['totalPage'], sms_data['curPage']
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch messages: {e}")
            return 1, 1

    def populate_sms_list(self, sms_list):
        self.sms_display.config(state=tk.NORMAL)  # فعال کردن ادیتور برای نوشتن متن
        self.sms_display.delete(1.0, tk.END)  # پاک کردن لیست فعلی

        # اضافه کردن پیام‌های جدید
        for sms in sms_list:
            self.sms_display.insert(tk.END, f"Sender: {sms['phoneNumber']}\n", 'header')
            self.sms_display.insert(tk.END, f"Message: {sms['smsContent']}\n", 'content')
            self.sms_display.insert(tk.END, f"Date: {sms['smsDate']}\n", 'footer')
            self.sms_display.insert(tk.END, "-" * 50 + "\n\n")  # خط جداساز

        self.sms_display.config(state=tk.DISABLED)  # غیر فعال کردن ادیتور

        # اضافه کردن استایل به متن
        self.sms_display.tag_config('header', foreground='blue', font=('Arial', 12, 'bold'))
        self.sms_display.tag_config('content', foreground='black', font=('Arial', 10))
        self.sms_display.tag_config('footer', foreground='gray', font=('Arial', 9))

    def update_pagination_buttons(self):
        if self.page_index == 1:
            self.prev_page_button.config(state=tk.DISABLED)
        else:
            self.prev_page_button.config(state=tk.NORMAL)

        if self.page_index == self.total_pages:
            self.next_page_button.config(state=tk.DISABLED)
        else:
            self.next_page_button.config(state=tk.NORMAL)

    def prev_page(self):
        if self.page_index > 1:
            self.page_index -= 1
            self.refresh_sms()

    def next_page(self):
        if self.page_index < self.total_pages:
            self.page_index += 1
            self.refresh_sms()
