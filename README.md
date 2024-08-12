# 6733-raspberry-pi

**Important:** Please see our [final report (PDF)](./No.100_final_report.pdf) for detailed project information.

## Project Overview

This project aims to provide a cost-effective, non-invasive, and scalable solution for building occupancy monitoring using Bluetooth Low Energy (BLE) technology. Our system is designed to benefit various applications, including public health, emergency response, energy efficiency, and space utilization.

### Key Components

- `raspi_sender.py`: Script for the Raspberry Pi to send data
- `ble_receiver.py`: Script for receiving data via Bluetooth Low Energy
- Algorithm code on the server: [algorithm side code](https://github.com/classmateada/6733-algorithm-scaffold) (private repository)
- [Server side code](https://github.com/classmateada/6733-server) including database (private repository)

**Note:** The algorithm and server-side code repositories are private due to university restrictions on publicly displaying project code.

### System Architecture

- Hardware: 4 Raspberry Pi Zero W devices for BLE scanning, connected via WiFi hotspot hosted by a Raspberry Pi 4
- Data Flow: BLE scanners detect devices, data is aggregated by the Raspberry Pi 4, and then processed on a server-side laptop
- Key Technologies: BLE, WiFi, Python, Java SpringBoot, MongoDB, gRPC

### Key Features

1. Cost-effective solution using affordable, readily available components
2. Non-invasive monitoring, preserving privacy and requiring minimal space
3. Scalable system with potential for easy expansion in larger spaces
4. Versatile applications from pandemic safety to daily space management

### Technical Approaches

- Frequent BLE scanning (20-second intervals)
- Data preprocessing and aggregation
- Triangulation for device localization using RSSI values
- DBSCAN clustering for occupancy estimation

### Challenges and Future Improvements

- Addressing MAC address randomization and signal reflection issues
- Implementing more secure data transmission protocols (e.g., MQTT)
- Exploring efficient power solutions for continuous operation

### Team Members

- Alan
- Xiang
- Ada
- Leo

### Acknowledgements

We thank our university and professors for their support and guidance throughout this project.

For full details on the project, methodology, and results, please refer to our [final report (PDF)](./No.100_final_report.pdf).
