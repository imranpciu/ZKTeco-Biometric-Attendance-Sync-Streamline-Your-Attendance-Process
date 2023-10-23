# ZKTeco-Biometric-Attendance-Sync-Streamline-Your-Attendance-Process
Simplify attendance management with the 'ZKTeco Biometric Attendance Sync' Python script. Tested with ZKTeco F18 and K40 models, effortlessly sync data from your biometric devices to your HR system.

An Extended Version of zkconnect by sowrensen

# Overview
ZKTeco Biometric Attendance Sync is a Python script designed for synchronizing attendance data from ZK biometric attendance devices to an external API. It connects to a ZK device over the network, fetches attendance logs, stores them in a local SQLite database, and then uploads the attendance data to a specified API endpoint.This project is an extended version of zkconnect by sowrensen.

# Features
  * Fetches attendance data from ZK biometric devices.
  * Stores attendance records in a SQLite database.
  * Posts attendance data to a specified API endpoint.
  * Supports customization of device host, port, and API endpoint.
  * Configurable logging for easy monitoring.

# How to Use
  1. Clone this repository to your local machine using **git clone**.
  2. Navigate to the project directory:**cd zk-attendance-sync**
  3. Install the required Python packages using pip: **pip install -r requirements.txt**
  4. Open the zk_attendance_sync.py script and configure the following parameters in the script:
     >> **HOST**: The IP address or hostname of your ZK biometric attendance device. Ex: "**_HOST = '192.168.10.121'_**"
     
     >> **PORT**: The port number for your ZK device. Ex: "**_PORT = 4370_**"
     
     >> **ENDPOINT**: The URL of the remote API where attendance data will be sent. Ex: "**_https://hr.example.com/api/attendance/update_**"