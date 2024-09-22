import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import LEFT, messagebox

import requests
import threading
from dataclasses import dataclass


@dataclass
class ModemData:
    battery: str
    signal: int
    network_type: str
    uptime: str
    hotcount: str


class ModemStatus:
    UPDATE_INTERVAL = 5000
    MODEM_URL = "http://192.168.0.1/jsonp_dashboard"

    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.create_widgets()
        self.update_modem_info()

    def create_widgets(self):
        tk.Label(self.frame, text="").pack(pady=10)

        self.signal_canvas = tk.Canvas(self.frame, width=100, height=50)
        self.signal_bars = self.prepare_signal_bars()
        self.signal_canvas.pack(pady=10)

        self.battery_label = self.create_label("Battery: ")
        self.network_label = self.create_label("Network Type: ")
        self.uptime_label = self.create_label("Uptime: ")
        self.hotcount_label = self.create_label("Connected Devices: ")

        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=10)
        self.power_off_button = tk.Button(button_frame, text="Power Off Modem", command=self.confirm_power_off)
        self.power_off_button.pack(side=LEFT, padx=5)

    def confirm_power_off(self):
        result = messagebox.askyesno("Confirm Power Off", "Are you sure you want to power off the modem?")
        if result:
            self.power_off_modem()

    def power_off_modem(self):
        url = "http://192.168.0.1/jsonp_power_off"
        try:
            response = requests.get(url)
            response.raise_for_status()
            messagebox.showinfo("Success", "The modem is shutting down.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to power off modem: {e}")

    def create_label(self, text):
        label = tk.Label(self.frame, text=text, font=("Arial", 12))
        label.pack(pady=5)
        return label

    def prepare_signal_bars(self):
        bars = []
        bar_width = 15
        for i in range(5):
            x1 = 10 + i * (bar_width + 3)
            bar = self.signal_canvas.create_rectangle(x1, 40, x1 + bar_width, 40 - (i + 1) * 7, fill="white")
            bars.append(bar)
        return bars

    def update_modem_info(self):
        threading.Thread(target=self._fetch_and_display_modem_info, daemon=True).start()

    def _fetch_and_display_modem_info(self):
        try:
            modem_data = self.fetch_modem_data()
            if modem_data:
                self.display_modem_info(modem_data)
        except Exception as e:
            self.battery_label.config(text="Error fetching modem info")
            print(f"Failed to fetch modem info: {e}")

        self.frame.after(self.UPDATE_INTERVAL, self.update_modem_info)

    def fetch_modem_data(self) -> ModemData:
        response = requests.get(self.MODEM_URL)
        response.raise_for_status()

        raw_data = self._clean_modem_data(response.content.decode('utf-8', errors='ignore'))
        root = ET.fromstring(raw_data)

        return ModemData(
            battery=root.find("batteryPercent").text or "Unknown",
            signal=int(root.find("strengthLevel").text or 0),
            network_type=root.find("networkType").text or "Unknown",
            uptime=root.find("functionTimes").text or "Unknown",
            hotcount=root.find("hotcount").text or "0"
        )

    @staticmethod
    def _clean_modem_data(raw_data: str) -> str:
        return raw_data.replace('Lms("', '').replace('")', '').strip()

    def display_modem_info(self, data: ModemData):
        self.update_signal_strength(data.signal)

        self.battery_label.config(text=f"Battery: {data.battery}")
        self.network_label.config(text=f"Network Type: {data.network_type}")
        self.uptime_label.config(text=f"Uptime: {data.uptime}")
        self.hotcount_label.config(text=f"Connected Devices: {data.hotcount}")

    def update_signal_strength(self, level):
        for i, bar in enumerate(self.signal_bars):
            color = "green" if i < level else "white"
            self.signal_canvas.itemconfig(bar, fill=color)
