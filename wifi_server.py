# Raspberry Pi 4 acts as a central spot for all the data to flow into.
# Also does some preprocessing and hosts the hotspot for all devices to connect to.

import time
import pandas as pd
import threading
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

LAPTOP_IP = '10.42.0.72'  # laptop's IP address
LAPTOP_PORT = 9080  # port that server is listening to 

def check_laptop_connection():
    url = f"http://{LAPTOP_IP}:{LAPTOP_PORT}/health"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def send_to_laptop(data):
    url = f"http://{LAPTOP_IP}:{LAPTOP_PORT}/add/batch"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully to laptop")
        else:
            print(f"Failed to send data to laptop. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending data to laptop: {e}")

def process_data(data_queue):
    while True:
        if data_queue and check_laptop_connection():
            # Process data every 60 seconds
            time.sleep(60)
            df = pd.DataFrame([d.split(',') for d in data_queue], columns=['device_id', 'mac_address', 'rssi', 'timestamp'])
            df['device_id'] = df['device_id'].str.split(':').str[1].astype(int)
            df['rssi'] = df['rssi'].str.split(':').str[1].astype(int)
            df['timestamp'] = df['timestamp'].str.split(':').str[1].astype(int)
            df['mac_address'] = df['mac_address'].str.replace('MAC:', '', regex=False)
            
            # Clear the queue
            data_queue.clear()
            
            # Process the data
            summary = df.groupby(['device_id', 'mac_address']).agg(
                avg_rssi=('rssi', lambda x: round(x.mean())),
                count=('rssi', 'count'),
                first_seen=('timestamp', 'min'),
                last_seen=('timestamp', 'max')
            ).reset_index()
            summary['duration'] = summary['last_seen'] - summary['first_seen']

            summary = summary[summary['duration'] > 0]

            data_to_send = {
                "timestamp": int(time.time() * 1000),
                "data": summary.to_dict(orient='records')
            }
            print(data_to_send)
            send_to_laptop(data_to_send)
        else:
            # If no connection or no data, wait for a short time before checking again
            time.sleep(1)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    data_queue.extend(data)
    return jsonify({"status": "success"}), 200

def main():
    global data_queue
    data_queue = []
    
    process_thread = threading.Thread(target=process_data, args=(data_queue,))
    process_thread.daemon = True
    process_thread.start()
    
    # Start the Flask app
    app.run(host='10.42.0.1', port=5432)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped.")
