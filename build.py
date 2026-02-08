import PyInstaller.__main__
import os

# Get the path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',                      # The entry point
    '--onefile',                    # Bundle into a single EXE
    '--noconsole',                  # No black terminal window
    '--name=NotifyAnything',        # The name of the EXE
    f'--add-data={os.path.join(current_dir, "assets")};assets', # Include assets
    '--clean',                      # Clean cache before building
    f'--icon={os.path.join(current_dir, "assets/icon.ico")}',
    # Source - https://stackoverflow.com/a/57538181
    # Posted by mucomoc
    # Retrieved 2026-02-08, License - CC BY-SA 4.0
    # Fix NotImplementedError with plyer library
    '--hidden-import=plyer.platforms.win.notification',
])