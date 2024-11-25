import os
import subprocess
import tkinter as tk
from empty_zookeeper import Empty_Zookeeper
import shutil

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

def clone_repository(text_box, root):
    """ Clone the repository if the conditions are met in the current working directory """
    repo_url = "https://github.com/UJKC/DDResouces.git"
    current_dir = os.getcwd()

    try:
        # Clone the repository into the current working directory
        subprocess.run(["git", "clone", repo_url], cwd=current_dir, check=True)
        text_box.insert(tk.END, f"Repository cloned to: {current_dir}")
        
        # Check if project is 'Empty_Zookeeper', then call the function empty_zookeeper
        project_name = root.find('project').text if root.find('project') is not None else ""
        if project_name == "Empty_Zookeeper":
            resourceoptimizer("Empty_Zookeeper")
            empty_zookeeper = Empty_Zookeeper(text_box)
            empty_zookeeper.empty_zookeeper(root)

    except subprocess.CalledProcessError as e:
        text_box.insert(tk.END, f"Error cloning repository: {e}")


def resourceoptimizer(projectname):
    # Path to the DDResources directory (inside current working directory)
    base_path = os.path.join(os.getcwd(), 'DDResouces')
    
    # Define the folder configuration for each project
    # For each project, we define a list of folder names that should be kept
    folders_to_keep = {
        'Empty_Zookeeper': ['apache-zookeeper-3.9.3-bin'],  # For 'ujwal' project, keep folder1 and folder3
    }

    # Check if the project name exists in the folders_to_keep dictionary
    if projectname not in folders_to_keep:
        print(f"No configuration found for project '{projectname}'.")
        return

    # Get the list of folders that should be kept for the current project
    folders_to_keep_for_project = folders_to_keep[projectname]
    
    # Get the list of all folders inside the DDResources directory
    all_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

    # Iterate through all folders in the DDResources directory
    for folder in all_folders:
        folder_path = os.path.join(base_path, folder)
        if folder not in folders_to_keep_for_project:
            try:
                # Delete the folder and its contents
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder}")
            except Exception as e:
                print(f"Error deleting folder {folder}: {e}")
        else:
            print(f"Kept folder: {folder}")

    print(f"Resource optimization for project '{projectname}' is complete.")