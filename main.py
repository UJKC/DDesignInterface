import sys
import os
from admin import is_admin, run_as_admin
from environment import set_java_home
from xml_reader_app import XMLReaderApp
import tkinter as tk

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        set_java_home()  # Set JAVA_HOME environment variable
        app = XMLReaderApp()  # Initialize and run the application
        app.mainloop()
