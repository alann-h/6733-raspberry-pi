# For the Raspberry Pi Zeros (scanners). For BLE scanning and sends data through WiFi.

from bluepy.btle import Scanner, DefaultDelegate
import time
import requests

class ScanDelegate(DefaultDelegate):
    def __init__(self, device_id):
        DefaultDelegate.__init__(self)
        self.start_time = time.time()
        self.device_id = device_id

    def handleDiscovery(self, dev, isNewDev, isNewData):
        elapsed_ms = int((time.time() - self.start_time) * 1000)        
        return f"ID:{self.device_id},MAC:{dev.addr},RSSI:{dev.rssi},Timestamp:{elapsed_ms}"

def send_data(data, url):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending data: {e}")

def main():
    device_id = 3  # Set the device ID
    scanner = Scanner().withDelegate(ScanDelegate(device_id))
    receiver_url = 'http://10.42.0.1:5432/receive_data'

    try:
        while True:
            devices = scanner.scan(20.0)  # Scan for 20 seconds
            data = [scanner.delegate.handleDiscovery(dev, None, None) for dev in devices]
            if data:
                send_data(data, receiver_url)
    except KeyboardInterrupt:
        print("\nScan stopped by user.")

if __name__ == "__main__":
    main()