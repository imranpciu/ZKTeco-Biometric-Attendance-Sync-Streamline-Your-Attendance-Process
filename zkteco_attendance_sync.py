#!/usr/bin/python3
import logging
import os
import sys
from datetime import date
import requests
from zk import ZK
from zk.exception import ZKError, ZKErrorConnection, ZKNetworkError
import sqlite3
import time

# Define the SQLite database filename
DB_FILENAME = 'zk_teco_data.db'

# Hardcoded host, port, and endpoint
HOST = '192.168.0.1' # Add Your device IP
PORT = 4370
ENDPOINT = 'https://hr.example.com/api/attendance/' # Add your external API endpoint 

# Function to create a date-wise log file name
def getLogFileName():
    """
    Generate a log file name based on the current date.

    Returns:
        str: The generated log file name.
    """
    today = date.today().strftime("%Y-%m-%d")
    return f"transactions_{today}.log"

class ZkConnect:
    def __init__(self, host, port, endpoint, transmission=True):
        """
        Initialize a connection to the ZK device and database for attendance data.

        Args:
            host (str): The IP address of the ZK device.
            port (int): The port number for the ZK device.
            endpoint (str): The API endpoint for data transmission.
            transmission (bool): Flag indicating whether data should be transmitted immediately.

        Attributes:
            host (str): The IP address of the ZK device.
            port (int): The port number for the ZK device.
            endpoint (str): The API endpoint for data transmission.
            transmission (bool): Flag indicating whether data should be transmitted immediately.
            connection: The ZK device connection.
        """
        try:
            self.host = host
            self.port = port
            self.endpoint = endpoint
            self.transmission = transmission
            self.connection = None
            self._connect()
            self._create_database_table()
        except (ZKNetworkError, ZKErrorConnection, ZKError) as error:
            logging.error(error)
        except Exception as error:
            logging.error(error)

    def _connect(self, reconnect=False):
        """
        Establish a connection to the ZK device.

        Args:
            reconnect (bool): Flag indicating whether this is a reconnection attempt.
        """
        zk = ZK(ip=self.host, port=self.port, verbose=True)
        self.connection = zk.connect()
        if reconnect:
            logging.debug('initiating reconnection...')
        logging.info(
            'connection established: host: {}, port: {}'.format(self.host, self.port))

    def _transmit(self, data):
        """
        Transmit data to the specified API endpoint via HTTP.

        Args:
            data (dict): Data to be transmitted.

        Returns:
            requests.Response: The HTTP response object.
        """
        try:
            logging.debug('Initiating transmission for ' + str(data))
            response = requests.post(self.endpoint, data)
            response.raise_for_status()

            if 'application/json' in response.headers.get('Content-Type', ''):
                jsonResponse = response.json()
                logging.debug("HTTP Response: {}, data: {}".format(jsonResponse.get('message'), jsonResponse.get('log')))
            else:
                logging.debug("HTTP Response content (non-JSON): {}".format(response.text))

            return response
        except requests.exceptions.HTTPError as error:
            logging.error("HTTP Error: {}, message: {}, data: {}".format(error, error.response.text, str(data)))
        except Exception as error:
            logging.error("Error: {}, data: {}".format(error, str(data)))

    def _create_database_table(self):
        """
        Create an SQLite database table for attendance records if it doesn't exist.
        """
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                device_user_id TEXT,
                timestamp DATETIME UNIQUE,
                api_status INTEGER DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()

    def _fetch_and_store_data(self):
        """
        Fetch and store attendance data from the ZK device into the SQLite database.
        """
        if not self.connection:
            raise ZKErrorConnection('Connection is not established!')

        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()

        for log in self.connection.get_attendance():
            if log is not None:
                cursor.execute('''
                    INSERT OR IGNORE INTO attendance (device_user_id, timestamp, api_status)
                    VALUES (?, ?, ?)
                ''', (log.user_id, log.timestamp, 0))

        conn.commit()
        conn.close()

    def _post_data_from_database(self):
        """
        Post attendance data from the SQLite database to the specified endpoint.
        """
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()

        data_to_post = cursor.execute('SELECT device_user_id, timestamp FROM attendance WHERE api_status = 0').fetchall()

        for row in data_to_post:
            device_user_id, timestamp = row
            response = self._transmit({
                'device_user_id': device_user_id,
                'timestamp': timestamp
            })

            if response.status_code == 200:
                cursor.execute('UPDATE attendance SET api_status = 1 WHERE device_user_id = ? AND timestamp = ?', (device_user_id, timestamp))

        conn.commit()
        conn.close()

    def monitor(self):
        """
        Monitor and manage the data transmission and storage process.
        """
        while True:
            self._post_data_from_database()
            self._fetch_and_store_data()
            time.sleep(1)

    def disconnect(self):
        """
        Disconnect from the ZK device.
        """
        self.connection.disconnect()

def configLogger():
    """
    Configure the logger with a date-wise log file.
    """
    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s %(lineno)d: %(message)s',
        filename=getLogFileName(),
        level=logging.DEBUG
    )

def init():
    try:
        configLogger() 
        # Configure the logger with the date-wise log file
        zk = ZkConnect(
            host=HOST,
            port=PORT,
            endpoint=ENDPOINT
        )
        zk.monitor()
    except Exception as error:
        # Handle exceptions and log errors
        logging.error(error)
        sys.exit(1)

if __name__ == "__main__":
    init()
