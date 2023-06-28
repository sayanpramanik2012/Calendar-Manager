import tkinter as tk
from tkinter import messagebox
import json
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate_google():
    # Define the scopes required for Google Calendar API access
    scopes = ["https://www.googleapis.com/auth/calendar"]

    # Set up the Google OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(
        "./assets/credentials.json", scopes=scopes
    )
    authorization_url, _ = flow.authorization_url(prompt="select_account")
    flow.run_local_server()

    # Create the success window
    success_window = tk.Tk()
    success_window.title("Successful Login")
    update_authorization_status(1)

    # Create a label for successful login message
    success_label = tk.Label(success_window, text="Authentication successful!")
    success_label.pack()

    def close_windows():
        success_window.destroy()
        login_window.destroy()

    # Create a button to close both windows
    close_button = tk.Button(success_window, text="Close", command=close_windows)
    close_button.pack()

    # Start the success window's event loop
    success_window.mainloop()


def update_authorization_status(status):
    try:
        with open("./assets/check.json", "r+") as file:
            data = json.load(file)
            data["authorization_status"] = status
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except (FileNotFoundError, json.JSONDecodeError):
        pass


# Create the login window
login_window = tk.Tk()
login_window.title("Google Login")

# Create a label
label = tk.Label(
    login_window, text="Click the button to login with your Google account"
)
label.pack()

# Create a button to initiate the login process
login_button = tk.Button(
    login_window, text="Login with Google", command=authenticate_google
)
login_button.pack()

# Start the login window's event loop
login_window.mainloop()
