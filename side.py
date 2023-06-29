import tkinter as tk
import json
from internal import wincalsave


def set_alarm(event):
    wincalsave.set_alarm(event)


def display_events():
    window = tk.Tk()
    window.title("Events")

    # Read the events from events.json
    with open("assets/events.json", "r") as file:
        events = json.load(file)

    # Create a label to display the events
    events_label = tk.Label(window, text="Upcoming Events")
    events_label.pack()

    # Display the events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event["summary"]

        event_text = f"{start}: {summary}"

        # Create a Checkbutton for each event
        event_checkbox = tk.Checkbutton(
            window, text=event_text, command=lambda ev=event_text: set_alarm(ev)
        )
        event_checkbox.pack()

    window.mainloop()
