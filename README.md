# Notify Anything

A Windows utility that monitors a user-defined region of the screen and sends a system notification when visual changes are detected. It utilizes low-level Windows APIs (Win32) for screen interaction and change detection.

## Features
- **Region Selection**: Custom overlay for defining the monitor area.
- **Change Detection**: Compares SHA-256 hashes of screen bit data using Win32 bit-block transfers.
- **Background Operation**: Runs in the system tray with a basic termination menu.
- **Startup Integration**: Optional registration with the Windows Registry `Run` key.
- **System Identity**: Uses an App User Model ID (AUMID) to associate notifications with the application.

## Getting Started

### Prerequisites
- Windows 10/11
- Python 3.10+

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/madhavc21/NotifyAnything.git
   cd NotifyAnything
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .notify
   .notify\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run: `python main.py`
2. **Select Region**: Use the hotkey `Ctrl + Alt + Shift + C`.
3. **Capture**: Click and drag to define the area.
4. **Monitoring**: The app hashes the pixel data at regular intervals. A notification is sent if the hash value changes.

## Building the Executable
The project includes a build script for PyInstaller:
```bash
python build.py
```

## Project Structure
- `core/`: Orchestration and Windows message loop.
- `observer/`: Win32 capture and hashing logic.
- `window/`: Selection overlay implementation.
- `services/`: Registry and notification wrappers.
- `assets/`: Image data and icons.