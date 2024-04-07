# Lotus

This project is a bottle deposit system implemented in Python using the PySide6 library for the GUI. The system allows users to deposit bottles, generate QR codes for the deposited bottles, and donate bottles.

## Project Structure

The project is structured into several Python scripts and modules:

- `LotusSystem.py`: This is the main script that runs the application. It handles the system's state and the transitions between different pages.

- `MachineEvent.py`: This script handles the communication with the physical machine via a serial connection.

- `QRGenerator.py`: This script generates QR codes for the deposited bottles.

- `models.py`: This script contains the response models for the HTTP requests.

- `UI/`: This directory contains the scripts for the different pages of the GUI:
  - `StartPage.py`: The start page of the application.
  - `DepositPage.py`: The page where users can deposit their bottles.
  - `DonePage.py`: The page that shows the QR code for the deposited bottles.
  - `DonatePage.py`: The page where users can donate their bottles.
