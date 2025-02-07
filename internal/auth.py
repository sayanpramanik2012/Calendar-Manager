import tkinter as tk
from tkinter import messagebox
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from google.oauth2.credentials import Credentials 

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    creds = None
    if os.path.exists("assets/token.json"):
        creds = Credentials.from_authorized_user_file("assets/token.json", SCOPES)
    return creds

def authenticate_google():
    flow = InstalledAppFlow.from_client_secrets_file(
        "assets/credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    
    with open("assets/token.json", "w") as token:
        token.write(creds.to_json())
    
    messagebox.showinfo("Success", "Authentication successful!")
    login_window.destroy()

def authorize_user():
    global login_window
    login_window = tk.Tk()
    login_window.title("Google Login")
    
    tk.Label(login_window, text="Google Authentication Required").pack(pady=10)
    tk.Button(login_window, text="Login with Google", command=authenticate_google).pack(pady=10)
    
    login_window.mainloop()
