import tkinter as tk
from tkinter import messagebox
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from screen import launch_application, add_event, fetch_events
import os.path


def check_authorization():
    creds = None
    if os.path.exists("./assets/token.json"):
        creds = Credentials.from_authorized_user_file("./assets/token.json")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return False
    return True  # Return True if the credentials are valid


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
    launch_application()
