# Lotus

This project is a bottle deposit system implemented in Python using the PySide6 library for the GUI. The system allows users to deposit bottles, generate QR codes for the deposited bottles, and donate bottles.

### Running the Project

To run the project, simply double-click on the executable file.

## Built With

* [Python](https://www.python.org/) - The programming language used
* [PySide6](https://www.qt.io/qt-for-python) - The Python binding for Qt libraries
* [PyInstaller](https://www.pyinstaller.org/) - Used to package Python applications

## Project Structure

The project is structured into several Python scripts and modules:

- `LotusSystem.py`: This is the main script that runs the application. It handles the system's state and the transitions between different pages.

- `MachineEvent.py`: This script handles the communication with the physical machine via a serial connection.

- `QRGenerator.py`: This script generates QR codes for the deposited bottles.

- `UI/`: This directory contains the scripts for the different pages of the GUI:
  - `StartPage.py`: The start page of the application.
  - `DepositPage.py`: The page where users can deposit their bottles.
  - `DonePage.py`: The page that shows the QR code for the deposited bottles.
  - `DonatePage.py`: The page where users can donate their bottles.
  - `Component.py`: To load fonts if not exist and Find the path for image

## Packaging the Application

To package the application into a standalone executable, you can use PyInstaller. Run the following command in your terminal:

```bash
pyinstaller --onefile \
--hidden-import=qrcode --hidden-import=PyJWT --hidden-import=pyserial --hidden-import=PySide6 --hidden-import=psutil \
--add-data 'resources/LotusBackground.jpg:resources' \
--add-data 'resources/Lotus.png:resources' \
--add-data 'resources/EggLogo.png:resources' \
--add-data 'resources/bottle.png:resources' \
--add-data 'Font/LotussSmartHL-Bold.ttf:Font' \
--add-data 'Font/LotussSmartHL-ExtraBold.ttf:Font' \
--add-data 'Font/LotussSmartHL-Light.ttf:Font' \
--add-data 'Font/LotussSmartHL-Medium.ttf:Font' \
--add-data 'Font/LotussSmartHL-Regular.ttf:Font' \
main.py
