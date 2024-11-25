import os
import subprocess
import tkinter as tk

def set_java_home():
    """ Set the JAVA_HOME environment variable permanently """
    java_home = r"C:\Program Files\Java\jdk-23"
    
    try:
        os.environ["JAVA_HOME"] = java_home
        subprocess.run(f"setx JAVA_HOME \"{java_home}\"", shell=True)  # Set for future sessions
        print(f"JAVA_HOME has been set to {java_home}")
    except Exception as e:
        print(f"Error setting JAVA_HOME: {e}")
