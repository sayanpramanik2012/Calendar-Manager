import tkinter as tk
from tkinter import messagebox
import json
from screen import launch_application, add_event
from screen import fetch_events


def check_authorization():
    try:
        with open("assets/check.json", "r") as file:
            data = json.load(file)
            return data.get("authorization_status", 0) == 1
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def authorize_user():
    # Open the login window for user authorization
    from internal import auth


# Check if the user is authorized
if check_authorization():
    # If authorized, launch the application
    launch_application()
else:
    # If not authorized, display a messagebox and open the authorization window
    messagebox.showinfo(
        "Authorization Required", "Please log in to verify your account."
    )
    authorize_user()
    if check_authorization():
        # If authorized, launch the application
        launch_application()
