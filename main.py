import tkinter as tk
import os
from typing import List
from tkinter import ttk, filedialog
import time
from datetime import datetime, timedelta
from dateutil import rrule
from objects import Activity, ActivityInstance, ActivityTracker
import pandas as pd

class TimeTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Time Tracker")
        self.geometry("1280x720")

        self.data = ActivityTracker()
        self.time_data = pd.DataFrame(columns=["Activity", "Start", "End", "Duration"])

        self.add_activity_frame = ttk.Frame(self)
        self.add_activity_frame.pack(side=tk.TOP, fill=tk.X)

        self.activities_frame = ttk.Frame(self)
        self.activities_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.report_frame = ttk.Frame(self)
        self.report_frame.pack(side=tk.TOP, fill=tk.X)

        self.create_widgets()

    def create_widgets(self):
        # Add activity widgets
        self.activity_entry = ttk.Entry(self.add_activity_frame)
        self.activity_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        self.add_activity_button = ttk.Button(self.add_activity_frame, text="Add Activity", command=self.add_activity)
        self.add_activity_button.pack(side=tk.LEFT, padx=(0, 10))

        self.remove_activity_button = ttk.Button(self.add_activity_frame, text="Remove Activity", command=self.remove_activity)
        self.remove_activity_button.pack(side=tk.LEFT)

        # Current activity stats
        self.current_activity_time_label = ttk.Label(self.add_activity_frame, text="0:00:00")
        self.current_activity_time_label.pack(side=tk.RIGHT)

        self.current_activity_colon = ttk.Label(self.add_activity_frame, text=": ")
        self.current_activity_colon.pack(side=tk.RIGHT)

        self.current_activity_label = ttk.Label(self.add_activity_frame, text="None selected")
        self.current_activity_label.pack(side=tk.RIGHT)


        # Create a style object and configure the row height
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        # Activities list
        self.activities_list = ttk.Treeview(self.activities_frame, style="Treeview")
        self.activities_list["columns"] = ("Activity", "Time")
        self.activities_list.column("#0", width=0, stretch=tk.NO)
        self.activities_list.column("Activity", anchor=tk.W, width=200)
        self.activities_list.column("Time", anchor=tk.W, width=150)
        self.activities_list.heading("Activity", text="Activity", anchor=tk.W)
        self.activities_list.heading("Time", text="Time", anchor=tk.W)
        self.activities_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.activities_list_scrollbar = ttk.Scrollbar(self.activities_frame, orient="vertical", command=self.activities_list.yview)
        self.activities_list.configure(yscrollcommand=self.activities_list_scrollbar.set)
        self.activities_list_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Timer control buttons
        self.start_timer_button = ttk.Button(self.activities_frame, text="Start Timer", command=self.start_timer)
        self.start_timer_button.pack(side=tk.TOP, pady=(10, 5))

        self.stop_timer_button = ttk.Button(self.activities_frame, text="Stop Timer", command=self.stop_timer)
        self.stop_timer_button.pack(side=tk.TOP, pady=(5, 10))

        # Report widgets
        self.report_button = ttk.Button(self.report_frame, text="Show Report", command=self.generate_report)
        self.report_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        # Save and Load buttons
        self.save_data_button = ttk.Button(self.report_frame, text="Save Data", command=self.save_data)
        self.save_data_button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

        self.load_data_button = ttk.Button(self.report_frame, text="Load Data", command=self.load_data)
        self.load_data_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

        self.load_data()

        # Initialize the live timer update
        self.update_live_timer()

    def save_data(self):
        self.data.to_dataframe().to_csv("activities.csv", index=False)
        print("Data Saved!")

    def load_data(self):
        file_name = "activities.csv"
        if not os.path.exists(file_name):
            return

        df = pd.read_csv("activities.csv")
        self.data = ActivityTracker.from_dataframe(df)

    def add_activity(self):
        activity_name = self.activity_entry.get()
        if activity_name and self.data.name_available(activity_name):
            self.data.add_activity(activity_name)
            self.activities_list.insert("", tk.END, activity_name, values=(activity_name, "0:00:00"))

            # Clear the text box after adding an activity
            self.activity_entry.delete(0, tk.END)

    def remove_activity(self):
        selected_item = self.activities_list.selection()
        if selected_item:
            activity_name = selected_item[0]
            self.data.remove_activity(activity_name)
            self.activities_list.delete(activity_name)

    def start_timer(self):
        if self.data.timer_running():
            print(f"Stopping timer")
            self.stop_timer()
        
        selected_item = self.activities_list.selection()
        if not selected_item:
            print("No currently selected item")
            return
        
        print("Starting timer")
        activity_name = selected_item[0]
        self.data.start_timer(activity_name)
        self.current_activity_label.config(text=activity_name)
        self.current_activity_time_label.config(text="0:00:00")
        self.current_activity_colon.config(text=": ")

    def reset_current_activity_label(self):
        self.current_activity_label.config(text="")
        self.current_activity_time_label.config(text="")
        self.current_activity_colon.config(text="")

    def stop_timer(self):
        current_activity = self.data.get_current_activity()
        if self.data.stop_timer() is None:
            return
        self.activities_list.set(current_activity.name, "Time", current_activity.get_total_time())
        self.reset_current_activity_label()

    def update_live_timer(self):
        current_time = self.data.get_current_time()
        if current_time is not None:
            self.current_activity_time_label.config(text=current_time)

        self.after(1000, self.update_live_timer)

    def generate_report(self):
        report_window = tk.Toplevel(self)
        report_window.title("Report")
        report_window.geometry("800x600")

        report_text = tk.Text(report_window, wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        now = datetime.now()
        current_week_start = now - timedelta(days=now.weekday())
        current_week_end = current_week_start + timedelta(days=6)
        current_month_start = now.replace(day=1)
        current_month_end = (now.replace(month=now.month % 12 + 1, day=1) - timedelta(days=1)).replace(day=1)

        for activity_name, activity in self.activities.items():
            report_text.insert(tk.END, f"Activity: {activity_name}\n")
            for instance in activity["instances"]:
                start_time = instance["start_time"]
                end_time = instance["end_time"]
                duration = instance["duration"]

                if start_time is None or end_time is None or duration is None:
                    continue

                in_current_week = current_week_start <= start_time <= current_week_end
                in_current_month = current_month_start <= start_time <= current_month_end
                in_current_year = now.year == start_time.year

                if in_current_week:
                    report_text.insert(tk.END, f"  This week:\n")

                if in_current_month:
                    report_text.insert(tk.END, f"  This month:\n")

                if in_current_year:
                    report_text.insert(tk.END, f"  This year:\n")

                report_text.insert(tk.END, f"    Start time: {start_time}\n")
                report_text.insert(tk.END, f"    End time: {end_time}\n")
                report_text.insert(tk.END, f"    Duration: {duration}\n")
            report_text.insert(tk.END, "\n")

    def display_report(self, container, timeframe):
        now = datetime.now()

        if timeframe == "W":
            start_date = now - timedelta(days=now.weekday())
            end_date = start_date + timedelta(days=6)
        elif timeframe == "M":
            start_date = now.replace(day=1)
            end_date = now.replace(month=now.month+1, day=1) - timedelta(days=1)
        elif timeframe == "Y":
            start_date = now.replace(month=1, day=1)
            end_date = now.replace(year=now.year+1, month=1, day=1) - timedelta(days=1)

        filtered_data = self.time_data[(self.time_data["Start"] >= start_date) & (self.time_data["End"] <= end_date)]
        report_data = filtered_data.groupby("Activity")["Duration"].sum().reset_index()
        report_data["Duration"] = report_data["Duration"].apply(lambda x: str(x).split(".")[0])

        report_list = ttk.Treeview(container)
        report_list["columns"] = ("Activity", "Time")
        report_list.column("#0", width=0, stretch=tk.NO)
        report_list.column("Activity", anchor=tk.W, width=200)
        report_list.column("Time", anchor=tk.W, width=150)
        report_list.heading("Activity", text="Activity", anchor=tk.W)
        report_list.heading("Time", text="Time", anchor=tk.W)

        for index, row in report_data.iterrows():
            report_list.insert("", tk.END, row["Activity"], values=(row["Activity"], row["Duration"]))

        report_list.pack(expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    app = TimeTrackerApp()
    app.mainloop()