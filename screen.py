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


def update_checkbox_state(data, checkbox_vars, index):
    # Update the alert value based on checkbox state
    if checkbox_vars[index].get() == 1:
        data["dates"][index]["alert"] = "1"
    else:
        data["dates"][index]["alert"] = "0"


def update_all_states(data, checkbox_vars):
    for index in range(len(checkbox_vars)):
        update_checkbox_state(data, checkbox_vars, index)


def create_checkbox(data, checkbox_vars, index):
    checkbox = tk.Checkbutton(
        window,
        variable=checkbox_vars[index],
        command=lambda index=index: update_checkbox_state(data, checkbox_vars, index),
    )
    checkbox.select() if data["dates"][index]["alert"] == "1" else checkbox.deselect()
    checkbox.grid(row=index + 1, column=2)


def create_label(date, index):
    label = tk.Label(window, text=date)
    label.grid(row=index + 1, column=1)


def done(data, checkbox_vars):
    # Update all checkbox states in data before writing to the file
    update_all_states(data, checkbox_vars)
    # Update the JSON file with the modified data
    with open("assets/upcoming.json", "w") as file:
        json.dump(data, file, indent=2)


def create_event_window():
    # Read the JSON file
    with open("assets/upcoming.json") as file:
        data = json.load(file)

    checkbox_vars = []

    # Create checkboxes and labels dynamically
    for index, date_entry in enumerate(data["dates"]):
        date = date_entry["date"]
        alert = date_entry["alert"]

        checkbox_var = tk.IntVar(value=int(alert))
        checkbox_vars.append(checkbox_var)

        create_label(date, index)
        create_checkbox(data, checkbox_vars, index)

    done_button = tk.Button(
        window,
        text="Done",
        command=lambda: done(data, checkbox_vars),
    )
    done_button.grid(row=len(data["dates"]) + 1, column=1, columnspan=2)


def fetch_events():
    # Fetch all current events from the calendar
    events = calendar_fetcher.fetch_all_events()

    # Save the events in a JSON file
    with open("assets/events.json", "w") as file:
        json.dump(events, file, indent=4)

    messagebox.showinfo(
        "Events Fetched", "All current events fetched and saved in events.json."
    )


def launch_application():
    global window
    window = tk.Tk()
    window.title("Calendar Event Manager")

    # Create a label
    label = tk.Label(window, text="Add Event to Calendar")
    label.grid(row=0, column=0, columnspan=2)

    # Create a button to fetch events
    fetch_button = tk.Button(window, text="Fetch Events", command=fetch_events)
    fetch_button.grid(row=1, column=0, columnspan=2)

    # Create an entry field for the event title
    global title_entry
    title_label = tk.Label(window, text="Event Title:")
    title_label.grid(row=2, column=0, sticky="e")
    title_entry = tk.Entry(window)
    title_entry.grid(row=2, column=1, sticky="w")

    # Create an entry field for the event date
    global date_entry
    date_label = tk.Label(window, text="Event Date:")
    date_label.grid(row=3, column=0, sticky="e")
    date_entry = tk.Entry(window)
    date_entry.grid(row=3, column=1, sticky="w")

    # Create an entry field for the event time
    global time_entry
    time_label = tk.Label(window, text="Event Time:")
    time_label.grid(row=4, column=0, sticky="e")
    time_entry = tk.Entry(window)
    time_entry.grid(row=4, column=1, sticky="w")

    # Create a button to add the event
    add_button = tk.Button(window, text="Add Event", command=add_event)
    add_button.grid(row=5, column=0, columnspan=2)

    event_button = tk.Button(window, text="Show all Event", command=create_event_window)
    event_button.grid(column=1, columnspan=1, pady=(10, 200), padx=(70, 210))

    # Start the main event loop
    window.mainloop()
