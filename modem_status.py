import tkinter as tk
import xml.etree.ElementTree as ET

import requests


class ModemStatus:
    def __init__(self, parent):
        # ساختن قاب اصلی برای این بخش
        self.frame = tk.Frame(parent)
        self.space_line = tk.Label(self.frame, text="")
        self.space_line.pack(pady=10)
        self.signal_canvas = tk.Canvas(self.frame, width=100, height=50)
        self.signal_bars = []
        self.prepare_signal_bar()
        self.create_modem_info_view()

        # بروزرسانی خودکار اطلاعات مودم
        self.update_modem_info()

    def prepare_signal_bar(self):
        for i in range(5):
            bar = self.signal_canvas.create_rectangle(10 + i * 18, 40, 25 + i * 18, 40 - (i + 1) * 7, fill="white")
            self.signal_bars.append(bar)
        self.signal_canvas.pack(pady=10)

    def create_modem_info_view(self):
        self.battery_label = tk.Label(self.frame, text="Battery: ", font=("Arial", 12))
        self.battery_label.pack(pady=5)

        self.network_label = tk.Label(self.frame, text="Network Type: ", font=("Arial", 12))
        self.network_label.pack(pady=5)

        self.uptime_label = tk.Label(self.frame, text="Uptime: ", font=("Arial", 12))
        self.uptime_label.pack(pady=5)

        self.hotcount_label = tk.Label(self.frame, text="Connected Devices: ", font=("Arial", 12))
        self.hotcount_label.pack(pady=5)

    def update_modem_info(self):
        url = "http://192.168.0.1/jsonp_dashboard"
        try:
            response = requests.get(url)
            response.raise_for_status()

            raw_data = response.content.decode('utf-8', errors='ignore')
            # پاک کردن داده‌های اضافی
            cleaned_data = raw_data.replace('Lms("', '').replace('")', '').strip()
            root = ET.fromstring(cleaned_data)

            # خواندن اطلاعات از XML
            battery = root.find("batteryPercent").text
            signal = int(root.find("strengthLevel").text)
            network_type = root.find("networkType").text
            uptime = root.find("functionTimes").text
            hotcount = root.find("hotcount").text

            self.update_signal_strength(signal)

            # نمایش اطلاعات در لیبل‌ها
            self.battery_label.config(text=f"Battery: {battery}")
            self.network_label.config(text=f"Network Type: {network_type}")
            self.uptime_label.config(text=f"Uptime: {uptime}")
            self.hotcount_label.config(text=f"Connected Devices: {hotcount}")

        except requests.exceptions.RequestException as e:
            self.battery_label.config(text="Error fetching modem info")
            print(f"Failed to fetch modem info: {e}")

        self.frame.after(5000, self.update_modem_info)

    def update_signal_strength(self, level):
        for rect in self.signal_bars:
            self.signal_canvas.itemconfig(rect, fill="white")
        for i in range(level):
            self.signal_canvas.itemconfig(self.signal_bars[i], fill="green")
