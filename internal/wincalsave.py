import json
from win10toast import ToastNotifier
from datetime import datetime


def set_alarm(event):
    # Extract the date and time from the event
    datetime_str, event_name = event.split(": ", 1)
    date_str, time_with_offset = datetime_str.split("T")

    # Remove the timezone offset from the time string
    time_str = time_with_offset.split("+")[0]

    # Convert the date and time strings to datetime objects
    date = datetime.strptime(date_str, "%Y-%m-%d")
    time = datetime.strptime(time_str, "%H:%M:%S")

    # Combine the date and time objects
    event_datetime = datetime.combine(date.date(), time.time())

    # Create a Windows toast notifier
    toaster = ToastNotifier()

    # Set the alarm
    toaster.show_toast(event_name, event_datetime.strftime("%Y-%m-%d %H:%M:%S"))
