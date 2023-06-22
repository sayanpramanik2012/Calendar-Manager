import tkinter as tk
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate_google():
    # Define the scopes required for Google Calendar API access
    scopes = ["https://www.googleapis.com/auth/calendar.events"]

    # Set up the Google OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=scopes)
    authorization_url, _ = flow.authorization_url(prompt="select_account")

    # Open the authorization URL in the user's browser
    webbrowser.open(authorization_url)

    # Close the login window
    login_window.destroy()

    # Launch the main application
    launch_application()


def launch_application():
    # Implement the code to launch the main application
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
