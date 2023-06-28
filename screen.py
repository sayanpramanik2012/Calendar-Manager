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
    if not event_title or not event_date or not event_time:
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
