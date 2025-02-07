# Calendar Manager Documentation

![Application Screenshot](screenshot.png) <!-- Add actual screenshot later -->

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [API Reference](#api-reference)
8. [Error Handling](#error-handling)
9. [License](#license)

## Project Overview <a name="project-overview"></a>

A desktop application for managing Google Calendar events with local reminder functionality. Features secure OAuth2 authentication and real-time synchronization with Google services.

## Features <a name="features"></a>

- 🔐 Secure Google OAuth2 authentication
- 📅 Event creation with validation
- 🔄 Real-time calendar synchronization
- ⏰ Local reminder system
- 📁 JSON data storage
- 🖥️ Tkinter GUI interface

## Installation <a name="installation"></a>

### Requirements

- Python 3.8+
- Google account with Calendar API enabled

```bash
# Install dependencies
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib tkinter
```

### Google Cloud Setup

- Enable Google Calendar API at Google Cloud Console
- Create OAuth2 credentials (Desktop App type)
- Download `credentials.json`

## Configuration <a name="configuration"></a>

### Create project structure:

```
Calendar-Manager/
├── assets/
│   ├── credentials.json
│   └── token.json (auto-generated)
└── internal/
```

### File permissions:

```bash
chmod 600 assets/credentials.json
```

## Usage <a name="usage"></a>

```bash
python main.py
```

### Workflow

#### Authentication Flow:

- First launch → Google login
- Automatic token refresh
- Local token storage

#### Event Management:

- Add events with datetime validation
- Fetch latest events from Google
- Automatic reminders for upcoming events

#### Reminder System:

- Background thread checks events every 60s
- Desktop notifications for due events

## Project Structure <a name="project-structure"></a>

### Core Modules

| File                           | Purpose                 |
| ------------------------------ | ----------------------- |
| `main.py`                      | Application entry point |
| `screen.py`                    | Main GUI interface      |
| `internal/auth.py`             | Authentication handlers |
| `internal/calendar_fetcher.py` | Google API integration  |

### Key Components

#### `screen.py`

```python
class CalendarApp:
    def __init__(self)  # UI initialization
    def add_event()     # Validate and create events
    def fetch_events()  # Sync with Google Calendar
    def check_alarms()  # Background reminder system
```

#### `auth.py`

```python
def authenticate_google()  # OAuth2 flow handler
def get_credentials()      # Token management
```

#### `calendar_fetcher.py`

```python
def fetch_all_events()     # Retrieve calendar items
def add_event_to_calendar()# Create new events
```

## API Reference <a name="api-reference"></a>

### Google Calendar API Endpoints

```python
# calendar_fetcher.py
service.events().list()    # Returns events
service.events().insert()  # Creates new event
```

### OAuth2 Scopes

```python
SCOPES = ["https://www.googleapis.com/auth/calendar"]
```

## Error Handling <a name="error-handling"></a>

### Common Errors

| Error                      | Solution                        |
| -------------------------- | ------------------------------- |
| Missing `credentials.json` | Verify file location            |
| Invalid `token.json`       | Delete token and reauthenticate |
| API quota exceeded         | Wait 24h or increase quota      |

### Debugging Tips

```bash
# Enable verbose logging
export GOOGLE_API_LOG=1
```

## License <a name="license"></a>

MIT License - See LICENSE file

---

This documentation provides:

1. Technical specifications for developers
2. Setup guide for new users
3. Architectural overview
4. API integration details
5. Troubleshooting resources
