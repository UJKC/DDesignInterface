import subprocess
import tkinter as tk

def check_java_git(text_box):
    """ Check if Java and Git are installed """
    try:
        java_version = subprocess.check_output("java -version", stderr=subprocess.STDOUT, shell=True)
        text_box.insert(tk.END, f"Java is installed: {java_version.decode()}\n")
    except subprocess.CalledProcessError:
        text_box.insert(tk.END, "Java is not installed.\n")

    try:
        git_version = subprocess.check_output("git --version", stderr=subprocess.STDOUT, shell=True)
        text_box.insert(tk.END, f"Git is installed: {git_version.decode()}\n")
    except subprocess.CalledProcessError:
        text_box.insert(tk.END, "Git is not installed.\n")
