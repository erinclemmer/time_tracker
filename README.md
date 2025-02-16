Time Tracker Application
========================

Overview
--------

The **Time Tracker Application** is a GUI-based activity tracker built using Python's Tkinter framework. It allows users to log and monitor time spent on different activities, store activity data locally, and sync data with a remote server.

Features
--------

*   **Activity Management**: Add, remove, and view activities.
    
*   **Time Tracking**: Start and stop timers to log activity durations.
    
*   **Manual Entry**: Add activity instances manually.
    
*   **Data Storage**: Save data locally in CSV format.
    
*   **Remote Syncing**: Retrieve and sync data with a remote server.
    
*   **Reports**: View activity logs and time spent over the last seven days.
    

Installation
------------

### Prerequisites

*   Python 3.x
    
*   Required dependencies:
    
    pip install requests pandas
    

### Configuration

Create a `config.json` file in the root directory with the following structure:
```json
{
  "server": "your_server_ip",
  "server_port": "your_server_port",
  "password": "your_password"
}
```

This file is required to enable syncing with a remote server.

Usage
-----

### Running the Application

python time\_tracker.py

### Interface

*   **Add Activity**: Click the "Add Activity" button to create a new activity.
    
*   **Remove Activity**: Select an activity and click "Remove Activity".
    
*   **Start Timer**: Select an activity and click "Start Timer".
    
*   **Stop Timer**: Click "Stop Timer" to log the elapsed time.
    
*   **Add Manual Instance**: Click "Add Instance" to input custom start and stop times.
    
*   **View Reports**: The table displays activities with total time spent and last 7-day data.
    
*   **Save Data**: Click "Save Data" to export data to `activities.csv`.
    
*   **Sync Data**: The app automatically syncs with the server if configured.
    

File Structure
--------------
```
.
├── time_tracker.py # Main application script
├── objects.py # Contains the ActivityTracker class
├── util.py # Utility functions for time formatting
├── config.json # Configuration file (required for server sync)
├── activities.csv # Local storage for activity logs
```
API Integration
---------------

The application communicates with a remote server using the following API endpoints:

*   **Retrieve Data**: `POST /retrieve`
    
    *   Request Payload:
        
        ```{ "password": "your_password" }```
        
    *   Response: Returns activity data in CSV format.
        
*   **Sync Data**: `POST /sync`
    
    *   Request Payload:
```json
{
  "password": "your_password",
  "data": "CSV formatted activity data"        
}
```        

Future Improvements
-------------------

*   Add visualization for activity reports.
    
*   Improve UI with better styling.
    
*   Implement user authentication for enhanced security.
    
*   Add mobile support.
    

License
-------

MIT License
