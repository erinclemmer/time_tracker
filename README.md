# Time Tracker Application

## Overview

The **Time Tracker Application** is a GUI-based activity tracker built using Python's Tkinter framework. It allows users to log and monitor time spent on different activities, store activity data locally, and optionally synchronize data with a custom server.

## Features

- **Activity Management**: Add, remove, and view activities.
- **Time Tracking**: Start and stop timers to log activity durations.
- **Manual Entry**: Add activity instances manually.
- **Data Storage**: Save data locally in CSV format.
- **Remote Syncing**: Retrieve and sync data with a remote server.
- **Reports**: View activity logs and time spent over the last seven days.

## Installation

### Prerequisites

- Python 3.x
- Required dependencies:
  ```sh
  pip install requests pandas
  ```

### Configuration

Create a `config.json` file in the root directory with the following structure:

```json
{
  "server": "your_server_ip",
  "server_port": "your_server_port",
  "password": "your_password"
}
```

This file is required to enable syncing with a remote server, and also used by the server script if you choose to host your own.

## Usage

### Running the Client Application

1. **Launch the GUI**
   ```sh
   python time_tracker.py
   ```
2. **Interface Actions**:
   - **Add Activity**: Click the "Add Activity" button to create a new activity.
   - **Remove Activity**: Select an activity and click "Remove Activity".
   - **Start Timer**: Select an activity and click "Start Timer".
   - **Stop Timer**: Click "Stop Timer" to finalize the logged time.
   - **Add Manual Instance**: Click "Add Instance" to input custom start and stop times.
   - **View Reports**: The table displays activities with total time spent and 7-day data.
   - **Save Data**: Click "Save Data" to export data to `activities.csv`.
   - **Sync Data**: Automatically runs when saving, if configured.

### Running the Server

If you want to host your own remote server, there is a **time\_tracker\_server.py** script that:

- Reads `config.json` for server port and password.
- Hosts an HTTP server to receive and respond to requests.
- Stores and retrieves data in a local `activities.csv` file.

1. **Start the server**

   ```sh
   python time_tracker_server.py
   ```

   The server will start listening on the port specified in `config.json` (`server_port`).

2. **Endpoints**:

   - `GET /` : Returns a simple success message (useful for health checks).
   - `POST /retrieve` : Validates the password and returns the full contents of the `activities.csv` file if it exists.
   - `POST /sync` : Validates the password and writes the received data to `activities.csv`.

3. **Security**:

   - The server checks the `password` field from the request body and compares it to `config.json`. Unauthorized requests return a 401 response.
   - Ensure you keep your server and client credentials secure.

## File Structure

```
.
├── time_tracker.py         # Main client application script
├── time_tracker_server.py  # Server script to host time tracking data
├── objects.py              # Contains the ActivityTracker class
├── util.py                 # Utility functions for time formatting
├── config.json             # Configuration file (used by client & server)
├── activities.csv          # Local storage for activity logs
```

## API Integration

The application and server communicate using:

- **Retrieve Data**: `POST /retrieve`
  - Request Payload:
    ```json
    {
      "password": "your_password"
    }
    ```
  - Response: CSV formatted activity data.
- **Sync Data**: `POST /sync`
  - Request Payload:
    ```json
    {
      "password": "your_password",
      "data": "CSV formatted activity data"
    }
    ```
  - Response: `"synced"` on success.

## Future Improvements

- Add visualization for activity reports.
- Improve UI with enhanced styling.
- Implement user authentication for added security.
- Add mobile support.

## License

MIT License

