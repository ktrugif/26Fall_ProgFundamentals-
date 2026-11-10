
import sqlite3
import time
import serial                     
from datetime import datetime
PORT = "@ /dev/cu.usbmodem101"       
BAUD = 115200


def ask_board(ser, command):
    """
    Send a one-letter command ('T' or 'H') to the MicroPython board over serial 
    and return the numeric float reading returned by the board.[cite: 4]
    """
    ser.reset_input_buffer()                 
    ser.write((command + "\n").encode())      
   
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line == "":
            raise TimeoutError("No reply from board")
        if line.startswith("DATA,"):
            return float(line.split(",")[2])



class DatabaseManager:
    """
    Custom class to manage SQLite database connections, table creation,
    logging sensor readings, and retrieving logged history.
    """
    def __init__(self, db_name="sensor_data.db"):
        """Initialize the database manager and create table if it does not exist."""
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        """Helper method to return a new SQLite database connection object."""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """
        Creates the 'sensor_readings' table in sensor_data.db if it does not exist.
        Columns:
          - id: INTEGER PRIMARY KEY AUTOINCREMENT
          - timestamp: TEXT (Date and time of reading)
          - sensor_type: TEXT ('Temperature' or 'Humidity')
          - reading_value: REAL (Numeric float value)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensor_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    sensor_type TEXT NOT NULL,
                    reading_value REAL NOT NULL
                )
            """)
            conn.commit()

    def insert_reading(self, sensor_type: str, reading_value: float):
        """
        Method to insert and log a single sensor reading into the SQLite database.
        
        Parameters:
            sensor_type (str): Type of sensor data logged ('Temperature' or 'Humidity')
            reading_value (float): Measurement float value returned by board
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sensor_readings (timestamp, sensor_type, reading_value)
                VALUES (?, ?, ?)
            """, (timestamp, sensor_type, reading_value))
            conn.commit()
            print(f"[DATABASE LOGGED] {timestamp} | {sensor_type}: {reading_value}")

    def view_history(self):
        """
        Method to query and display all historical records stored in the SQLite database.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, sensor_type, reading_value FROM sensor_readings")
            rows = cursor.fetchall()

            print("\n" + "=" * 62)
            print("                 HISTORICAL SENSOR LOG HISTORY                ")
            print("=" * 62)
            if not rows:
                print("No historical records found in database.")
            else:
                print(f"{'ID':<6} | {'Timestamp':<20} | {'Sensor Type':<13} | {'Value':<10}")
                print("-" * 62)
                for rec_id, ts, s_type, val in rows:
                    unit = "°C" if s_type.lower() == "temperature" else "%"
                    print(f"{rec_id:<6} | {ts:<20} | {s_type:<13} | {val:.2f} {unit}")
            print("=" * 62 + "\n")



def handle_temperature(ser, db: DatabaseManager):
    """
    Requests temperature data from board via ask_board('T'), displays result,
    and logs reading into SQLite database.[cite: 4]
    """
    try:
        temp_val = ask_board(ser, "T")
        print(f"\n--> Temperature Reading: {temp_val:.2f} °C")
        db.insert_reading("Temperature", temp_val)
    except TimeoutError as te:
        print(f"\n[ERROR] {te}")
    except Exception as e:
        print(f"\n[ERROR] Failed to read temperature: {e}")


def handle_humidity(ser, db: DatabaseManager):
    """
    Requests humidity data from board via ask_board('H'), displays result,
    and logs reading into SQLite database.[cite: 4]
    """
    try:
        hum_val = ask_board(ser, "H")
        print(f"\n--> Humidity Reading: {hum_val:.2f} %")
        db.insert_reading("Humidity", hum_val)
    except TimeoutError as te:
        print(f"\n[ERROR] {te}")
    except Exception as e:
        print(f"\n[ERROR] Failed to read humidity: {e}")



def display_menu():
    """Prints terminal options required by Part 3 Task 1."""
    print("Please choose from the following options:")
    print("  T - Temperature")
    print("  H - Humidity")
    print("  0 - Both")
    print("  V - View Log History")


def main():
   
    db = DatabaseManager("sensor_data.db")

    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=3)
        time.sleep(2)  
        ser.reset_input_buffer()
    except serial.SerialException as e:
        print(f"[ERROR] Could not open serial port '{PORT}'.")
        print("Ensure Thonny IDE is completely closed before running.")
        return

    
    try:
        while True:
            display_menu()
            choice = input("Enter option: ").strip().upper()

            if choice == "T":
                handle_temperature(ser, db)
            elif choice == "H":
                handle_humidity(ser, db)
            elif choice == "0":
                handle_temperature(ser, db)
                handle_humidity(ser, db)
            elif choice == "V":
                db.view_history()
            else:
                print("\nInvalid choice! Please try again.\n")
    finally:
       
        ser.close()


if __name__ == "__main__":
    main()