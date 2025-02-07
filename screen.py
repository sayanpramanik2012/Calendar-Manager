import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import json
import time
import threading
import pytz
from internal.calendar_fetcher import fetch_all_events, add_event_to_calendar, delete_event
from internal.auth import get_credentials
from win10toast import ToastNotifier
from plyer import notification

class CalendarApp:
    def __init__(self, master):
        self.toaster = ToastNotifier()
        self.notified_events = set()
        self.master = master
        self.master.title("Google Calendar Manager")
        self.master.geometry("1000x700")
        self.master.minsize(800, 600)
        self.creds = get_credentials()
        self.alarm_thread = None
        self.selected_timezone = pytz.utc
        
        # Configure styles
        self.configure_styles()
        
        # Load config
        self.load_timezone_config()
        
        # Build UI
        self.create_widgets()
        self.setup_context_menu()
        self.check_alarms()
        self.fetch_events()

    def configure_styles(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.map("TButton", background=[("active", "#e0e0e0")])

    def load_timezone_config(self):
        try:
            with open("assets/config.json", "r") as f:
                config = json.load(f)
                self.selected_timezone = pytz.timezone(config.get("timezone", "UTC"))
        except (FileNotFoundError, pytz.UnknownTimeZoneError):
            self.selected_timezone = pytz.utc

    def save_timezone_config(self):
        with open("assets/config.json", "w") as f:
            json.dump({"timezone": str(self.selected_timezone)}, f)

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Top Control Panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Timezone Selection
        tz_frame = ttk.Frame(control_frame)
        tz_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(tz_frame, text="Timezone:").pack(side=tk.LEFT, padx=5)
        self.tz_combo = ttk.Combobox(tz_frame, 
                                   values=sorted(pytz.all_timezones),
                                   state="readonly",
                                   width=40)
        self.tz_combo.set(str(self.selected_timezone))
        self.tz_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(tz_frame, text="Set Timezone", 
                 command=self.update_timezone).pack(side=tk.LEFT, padx=5)

        # Control Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.fetch_events).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", command=self.delete_selected_event).pack(side=tk.LEFT, padx=2)

        # Event List Frame
        list_frame = ttk.LabelFrame(main_frame, text="Calendar Events")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Treeview with scrollbars
        self.tree = ttk.Treeview(list_frame, columns=("Title", "Date", "Time", "ID"), show="headings")
        self.tree.heading("Title", text="Title", anchor=tk.W)
        self.tree.heading("Date", text="Date", anchor=tk.W)
        self.tree.heading("Time", text="Time", anchor=tk.W)
        self.tree.column("ID", width=0, stretch=tk.NO)
        
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        # Add Event Frame
        add_frame = ttk.LabelFrame(main_frame, text="Add New Event")
        add_frame.pack(fill=tk.X, pady=(0, 10))

        # Event Title
        ttk.Label(add_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(add_frame, width=50)
        self.title_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

        # Date and Time Selection
        ttk.Label(add_frame, text="Date:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.date_picker = DateEntry(
            add_frame,
            date_pattern="yyyy-mm-dd",
            mindate=datetime.now() - timedelta(days=365),
            maxdate=datetime.now() + timedelta(days=365),
            width=12
        )
        self.date_picker.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(add_frame, text="Time:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.time_frame = ttk.Frame(add_frame)
        self.time_frame.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        self.hour_var = tk.StringVar(value=datetime.now().strftime("%H"))
        self.minute_var = tk.StringVar(value=datetime.now().strftime("%M"))
        
        ttk.Combobox(self.time_frame, width=3, textvariable=self.hour_var, 
                   values=[f"{i:02d}" for i in range(24)], state="readonly").pack(side=tk.LEFT)
        ttk.Label(self.time_frame, text=":").pack(side=tk.LEFT)
        ttk.Combobox(self.time_frame, width=3, textvariable=self.minute_var,
                   values=[f"{i:02d}" for i in range(60)], state="readonly").pack(side=tk.LEFT)

        # Add Event Button
        ttk.Button(add_frame, text="➕ Add Event", command=self.add_event).grid(
            row=1, column=4, padx=5, pady=5, sticky="e"
        )

        # Configure column weights
        add_frame.grid_columnconfigure(1, weight=1)
        add_frame.grid_columnconfigure(4, weight=0)

    def update_timezone(self):
        """Update the selected timezone and refresh events"""
        try:
            new_tz = self.tz_combo.get()
            # Validate the timezone
            pytz.timezone(new_tz)
            self.selected_timezone = pytz.timezone(new_tz)
            self.save_timezone_config()
            messagebox.showinfo("Success", f"Timezone updated to {new_tz}")
            self.fetch_events()  # Refresh events with new timezone
        except pytz.UnknownTimeZoneError:
            messagebox.showerror("Error", "Invalid timezone selected")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update timezone: {str(e)}")

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Delete Event", command=self.delete_selected_event)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def add_event(self):
        title = self.title_entry.get().strip()
        date = self.date_picker.get_date()
        time_str = f"{self.hour_var.get()}:{self.minute_var.get()}"

        if not title:
            messagebox.showerror("Error", "Please enter an event title")
            return

        try:
            # Create datetime object in local timezone
            local_tz = self.selected_timezone
            naive_time = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
            local_time = local_tz.localize(naive_time)
            
            # Convert to UTC for Google Calendar
            utc_time = local_time.astimezone(pytz.utc)
            
            event = {
                "summary": title,
                "start": {
                    "dateTime": utc_time.isoformat(),
                    "timeZone": str(local_tz)
                },
                "end": {
                    "dateTime": utc_time.isoformat(),
                    "timeZone": str(local_tz)
                }
            }

            if add_event_to_calendar(self.creds, event):
                messagebox.showinfo("Success", "Event added to Google Calendar!")
                self.title_entry.delete(0, tk.END)
                self.fetch_events()
            else:
                messagebox.showerror("Error", "Failed to add event")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date/time format: {str(e)}")

    def fetch_events(self):
        try:
            events = fetch_all_events(self.creds)
            self.tree.delete(*self.tree.get_children())
            
            for event in events:
                start = event.get("start", {})
                event_tz = pytz.timezone(start.get("timeZone", "UTC"))
                date_time = start.get("dateTime")
                
                if date_time:
                    # Convert from UTC to selected timezone
                    utc_time = datetime.fromisoformat(date_time.replace('Z', '+00:00'))
                    local_time = utc_time.astimezone(self.selected_timezone)
                    date_part = local_time.strftime("%Y-%m-%d")
                    time_part = local_time.strftime("%H:%M")
                else:
                    # All-day events
                    date_part = start.get("date", "")
                    time_part = "All Day"
                
                self.tree.insert("", "end", values=(
                    event.get("summary", "No Title"),
                    date_part,
                    time_part,
                    event.get("id", "")
                ))

            with open("assets/events.json", "w") as f:
                json.dump([e for e in events if "id" in e], f, indent=2)
            
            status = f"Loaded {len(events)} events"
            self.master.title(f"Google Calendar Manager - {status}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch events: {str(e)}")
    def delete_selected_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an event to delete")
            return
            
        event_id = self.tree.item(selected[0], "values")[3]
        event_title = self.tree.item(selected[0], "values")[0]
        
        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete event '{event_title}'?\nThis action cannot be undone!"
        ):
            if delete_event(self.creds, event_id):
                self.tree.delete(selected[0])
                messagebox.showinfo("Success", "Event deleted successfully")
                self.fetch_events()
            else:
                messagebox.showerror("Error", "Failed to delete event")

    def check_alarms(self):
        def alarm_loop():
            while True:
                try:
                    with open("assets/events.json") as f:
                        events = json.load(f)
                        now = datetime.now(self.selected_timezone)
                        
                        for event in events:
                            event_id = event.get("id")
                            if event_id in self.notified_events:
                                continue
                                
                            start = event["start"].get("dateTime")
                            if start:
                                event_time = datetime.fromisoformat(
                                    start.replace('Z', '+00:00')
                                ).astimezone(self.selected_timezone)
                                
                                # Show notification 5 minutes before and at event time
                                if now >= event_time - timedelta(minutes=5):
                                    self.show_reminder(event)
                                    self.notified_events.add(event_id)
                except Exception as e:
                    print(f"Alarm error: {e}")
                time.sleep(60)  # Check every minute

        self.alarm_thread = threading.Thread(target=alarm_loop, daemon=True)
        self.alarm_thread.start()

    def show_reminder(self, event):
        event_time = datetime.fromisoformat(
            event["start"].get("dateTime").replace('Z', '+00:00')
        ).astimezone(self.selected_timezone)
        
        # Format the notification message
        title = "📅 Event Reminder"
        message = (
            f"{event.get('summary', 'Unnamed Event')}\n"
            f"Time: {event_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"Location: {event.get('location', 'No location')}"
        )
        
        # Show notification using plyer
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=10,  # Show for 10 seconds
                app_name="Calendar Manager",
                app_icon=None  # You can add an icon path here if desired
            )
        except Exception as e:
            print(f"Notification error: {e}")
            # Fallback to messagebox if notification fails
            self.master.after(0, lambda: messagebox.showinfo(title, message))

def launch_application():
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_application()