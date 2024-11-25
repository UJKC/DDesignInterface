import ctypes
import tkinter as tk

def is_admin():
    """ Check if the script is running with administrator privileges """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    """ Rerun the script with administrator privileges """
    import sys
    import subprocess
    script = sys.argv[0]
    params = " ".join(sys.argv[1:])
    subprocess.run(f"powershell -Command Start-Process python -ArgumentList '{script} {params}' -Verb RunAs", shell=True)
