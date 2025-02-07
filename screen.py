import tkinter as tk
from tkinter import messagebox
import json
from internal import calendar_fetcher


def add_event():
    # Get the values from the entry fields
    event_title = title_entry.get()
    event_date = date_entry.get()
    event_time = time_entry.get()

    # Validate the input
    if not event_title or not event_date or not event_time:aimport tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import time
import threading
from internal.calendar_fetcher import fetch_all_events, add_event_to_calendar
from internal.auth import get_credentials

class CalendarApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calendar Event Manager")
        self.creds = get_credentials()
        self.alarm_thread = None
        self.create_widgets()
        self.check_alarms()

    def create_widgets(self):
        # Event Input Frame
        input_frame = ttk.LabelFrame(self.master, text="Add New Event")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Event Title
        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        # Event Date
        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="w")
        self.date_entry = ttk.Entry(input_frame, width=30)
        self.date_entry.grid(row=1, column=1, padx=5, pady=2)

        # Event Time
        ttk.Label(input_frame, text="Time (HH:MM):").grid(row=2, column=0, sticky="w")
        self.time_entry = ttk.Entry(input_frame, width=30)
        self.time_entry.grid(row=2, column=1, padx=5, pady=2)

        # Buttons
        ttk.Button(input_frame, text="Add Event", command=self.add_event).grid(row=3, column=1, pady=5)
        ttk.Button(self.master, text="Fetch Events", command=self.fetch_events).grid(row=1, column=0, pady=5)

        # Event List
        self.tree = ttk.Treeview(self.master, columns=("Title", "Date", "Time"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

    def add_event(self):
        title = self.title_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        if not all([title, date, time]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format!")
            return

        event = {
            "summary": title,
            "start": {"dateTime": f"{date}T{time}:00", "timeZone": "UTC"},
            "end": {"dateTime": f"{date}T{time}:00", "timeZone": "UTC"}
        }

        if add_event_to_calendar(self.creds, event):
            messagebox.showinfo("Success", "Event added to Google Calendar!")
            self.title_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.fetch_events()
        else:
            messagebox.showerror("Error", "Failed to add event")

    def fetch_events(self):
        events = fetch_all_events(self.creds)
        self.tree.delete(*self.tree.get_children())
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            date, time = start.split("T") if "T" in start else (start, "00:00")
            self.tree.insert("", "end", values=(event["summary"], date, time.split("-")[0][:5]))
        
        with open("assets/events.json", "w") as f:
            json.dump(events, f, indent=2)
        
        messagebox.showinfo("Success", f"Fetched {len(events)} events!")

    def check_alarms(self):
        def alarm_loop():
            while True:
                try:
                    with open("assets/events.json") as f:
                        events = json.load(f)
                        now = datetime.utcnow().isoformat() + "Z"
                        for event in events:
                            start = event["start"].get("dateTime", event["start"].get("date"))
                            if start <= now:
                                messagebox.showinfo("Event Reminder", 
                                    f"Event '{event['summary']}' is starting!")
                except Exception as e:
                    print(f"Alarm error: {e}")
                time.sleep(60)

        self.alarm_thread = threading.Thread(target=alarm_loop, daemon=True)
        self.alarm_thread.start()

def launch_application():
    root = tk.Tk()
    CalendarApp(root)
    root.mainloop()
        messagebox.showerror("Error", "Please enter all the event details.")
        return

    # Implement the code to add the event to the calendar
    # You can use the Google Calendar API or any other calendar API of your choice
    # Here, we'll just print the event details
    event_details = f"Title: {event_title}\nDate: {event_date}\nTime: {event_time}"
    print(event_details)

    # Clear the entry fields
    title_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)


def launch_application():
    # Create the main application window
    window = tk.Tk()
    window.title("Calendar Event Manager")

    # Create a label
    label = tk.Label(window, text="Add Event to Calendar")
    label.pack()

    # Create a button to fetch events
    fetch_button = tk.Button(window, text="Fetch Events", command=fetch_events)
    fetch_button.pack()

    # Create an entry field for the event title
    global title_entry
    title_label = tk.Label(window, text="Event Title:")
    title_label.pack()
    title_entry = tk.Entry(window)
    title_entry.pack()

    # Create an entry field for the event date
    global date_entry
    date_label = tk.Label(window, text="Event Date:")
    date_label.pack()
    date_entry = tk.Entry(window)
    date_entry.pack()

    # Create an entry field for the event time
    global time_entry
    time_label = tk.Label(window, text="Event Time:")
    time_label.pack()
    time_entry = tk.Entry(window)
    time_entry.pack()

    # Create a button to add the event
    add_button = tk.Button(window, text="Add Event", command=add_event)
    add_button.pack()

    # Start the main event loop
    window.mainloop()


def fetch_events():
    # Fetch all current events from the calendar
    events = calendar_fetcher.fetch_all_events()

    # Save the events in a JSON file
    with open("assets/events.json", "w") as file:
        json.dump(events, file, indent=4)

    messagebox.showinfo(
        "Events Fetched", "All current events fetched and saved in events.json."
    )
