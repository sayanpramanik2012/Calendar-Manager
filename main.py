import tkinter as tk
from tkinter import messagebox
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from screen import launch_application
from internal.auth import authorize_user

def check_authorization():
    creds = None
    if os.path.exists("./assets/token.json"):
        try:
            creds = Credentials.from_authorized_user_file("./assets/token.json")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open("./assets/token.json", "w") as token:
                    token.write(creds.to_json())
            return True
        except Exception as e:
            print(f"Authorization error: {e}")
            return False
    return False

if __name__ == "__main__":
    if check_authorization():
        launch_application()
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Authorization Required", "Please log in to Google.")
        root.destroy()
        authorize_user()
        if check_authorization():
            launch_application()