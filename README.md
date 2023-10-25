# ZKTeco-Biometric-Attendance-Sync-Streamline-Your-Attendance-Process
Simplify attendance management with the 'ZKTeco Biometric Attendance Sync' Python script. Tested with ZKTeco F18 and K40 models, effortlessly sync data from your biometric devices to your HR system.

# Overview
ZKTeco Biometric Attendance Sync is a Python script designed for synchronizing attendance data from ZK biometric attendance devices to an external API. It connects to a ZK device over the network, fetches attendance logs, stores them in a local SQLite database, and then uploads the attendance data to a specified API endpoint.This project is an extended version of [zkconnect](https://github.com/sowrensen/zkconnect) by [@sowrensen](https://github.com/sowrensen).

# Features
  * Fetches attendance data from ZK biometric devices.
  * Stores attendance records in a SQLite database.
  * Posts attendance data to a specified API endpoint.
  * Supports customization of device host, port, and API endpoint.
  * Configurable logging for easy monitoring.
    
# Requirements
 * python >= 3.5
 * pyzk == 0.9
 * requests == 2.25.1
 * pyyaml == 5.4.1

# Configuration
 * **HOST:** The IP address or hostname of your ZKTeco device.
 * **PORT:** The port number of your ZKTeco device.
 * **ENDPOINT:** The API endpoint where attendance data will be sent.
 * **Database:** The SQLite database file is named "**_zk_teco_data.db_**".

# How to Use
  1. Clone this repository to your local machine using:
     ```bash
     git clone
     ```
  3. Navigate to the project directory:
     ```bash
     cd ZKTeco-Biometric-Attendance-Sync-Streamline-Your-Attendance-Process  
  5. Install virtual enviroment using:  "_**pipenv --python 3.9.12**_"(or any version)
  6. Start virtual environment using: "_**pipenv shell**_"
  7. Install the required Python packages using pip: "_**pip install -r requirements.txt**_"
  8. Open the zk_attendance_sync.py script and configure the following parameters in the script:
     >> **HOST**: The IP address or hostname of your ZK biometric attendance device. Ex: "**_HOST = '192.168.10.121'_**"
     
     >> **PORT**: The port number for your ZK device. Ex: "**_PORT = 4370_**"
     
     >> **ENDPOINT**: The URL of the remote API where attendance data will be sent. Ex: "**_https://hr.example.com/api/attendance/update_**"
  9. Run the script: "_**python zk_attendance_sync.py**_"
     
**Note**: The script will connect to your ZKTeco device, fetch attendance logs, store them in the local SQLite database, and then upload the data to the specified API. The script will run continuously to monitor and synchronize attendance data.

**Additional information:** You can convert the Python script into an executable file, such as '**zkteco-attendance-sync.exe**,' using the following command: '**pyinstaller --onefile zkteco-attendance-sync.py**.


# Contributing
Contributions to this project are welcome. You can fork the repository, make improvements, and create a pull request.
  
