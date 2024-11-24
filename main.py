import sys
import os
import ctypes
import subprocess
import tkinter as tk
from tkinterdnd2 import TkinterDnD
from tkinter import filedialog
import xml.etree.ElementTree as ET

def is_admin():
    """ Check if the script is running with administrator privileges """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    """ Rerun the script with administrator privileges """
    script = sys.argv[0]
    params = " ".join(sys.argv[1:])
    subprocess.run(f"powershell -Command Start-Process python -ArgumentList '{script} {params}' -Verb RunAs", shell=True)

def set_java_home():
    """ Set the JAVA_HOME environment variable permanently """
    java_home = r"C:\Program Files\Java\jdk-23"
    
    # Set JAVA_HOME in system environment variables for the current user
    try:
        # Access the current user's environment variables (this will persist across sessions)
        current_user_env = os.environ.get('USERPROFILE')
        java_home_key = r"Environment\JAVA_HOME"
        
        # Check if the JAVA_HOME environment variable already exists and update it
        if java_home:
            os.environ["JAVA_HOME"] = java_home
            subprocess.run(f"setx JAVA_HOME \"{java_home}\"", shell=True)  # Set for future sessions
            print(f"JAVA_HOME has been set to {java_home}")
    except Exception as e:
        print(f"Error setting JAVA_HOME: {e}")

if not is_admin():
    run_as_admin()
    sys.exit(0)

# Your existing XMLReaderApp code
class XMLReaderApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # Initialize the GUI components
        self.title("XML Reader App")
        self.geometry("500x400")

        # Label to display instructions or the content of the XML file
        self.label = tk.Label(self, text="Click the button to select an XML file", pady=20, padx=20)
        self.label.pack(fill=tk.BOTH, expand=True)

        # Text box to display the XML content and status messages
        self.text_box = tk.Text(self, wrap=tk.WORD, width=50, height=15)
        self.text_box.pack(pady=20)

        # Check if Java and Git are installed, and display the results in the text box
        self.check_java_git()

        # Button to select XML file
        self.select_button = tk.Button(self, text="Select XML File", command=self.select_file)
        self.select_button.pack(pady=10)

    def select_file(self):
        """ Open a file dialog to select an XML file """
        file_path = filedialog.askopenfilename(
            title="Select an XML file",
            filetypes=[("XML files", "*.xml")]
        )
        if file_path:
            self.display_xml_content(file_path)

    def display_xml_content(self, file_path):
        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Clear the text box before displaying new content
            self.text_box.delete(1.0, tk.END)

            # Display the XML content in a readable format in the text box
            self.text_box.insert(tk.END, ET.tostring(root, encoding='unicode', method='xml'))

            # Extract values from XML
            language = root.find('language').text if root.find('language') is not None else ""
            cluster_management = root.find('clusterManagement').text if root.find('clusterManagement') is not None else ""
            tick_time = root.find('tickTime').text if root.find('tickTime') is not None else ""
            init_limit = root.find('initLimit').text if root.find('initLimit') is not None else ""
            sync_limit = root.find('syncLimit').text if root.find('syncLimit') is not None else ""
            client_port = root.find('clientPort').text if root.find('clientPort') is not None else ""

            # Check if language is 'Java' and clusterManagement is 'Zookeeper'
            if language == 'Java' and cluster_management == 'Zookeeper':
                self.clone_repository(tick_time, init_limit, sync_limit, client_port)

        except Exception as e:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, f"Error reading file: {e}")

    def clone_repository(self, tick_time, init_limit, sync_limit, client_port):
        """ Clone the repository if the conditions are met in the current working directory """
        repo_url = "https://github.com/UJKC/DDResouces.git"
        
        # Get the current working directory (where the script is being executed)
        current_dir = os.getcwd()
        
        # Run git clone in that directory
        try:
            subprocess.run(["git", "clone", repo_url], cwd=current_dir, check=True)
            self.text_box.insert(tk.END, f"\nRepository cloned to: {current_dir}")
            
            # After cloning the repository, update the zoo.cfg file
            self.update_zoo_cfg(tick_time, init_limit, sync_limit, client_port)
        except subprocess.CalledProcessError as e:
            self.text_box.insert(tk.END, f"\nError cloning repository: {e}")

    def update_zoo_cfg(self, tick_time, init_limit, sync_limit, client_port):
        """ Update the zoo.cfg file with the provided values """
        try:
            # Define the path to the zoo.cfg file
            zoo_cfg_path = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "conf", "zoo.cfg")
            
            # Define the dataDir path inside the cloned repository
            data_dir = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "log")
            
            # Read the existing zoo.cfg content and append the new configuration
            with open(zoo_cfg_path, 'a') as zoo_cfg_file:
                zoo_cfg_file.write(f"\ntickTime={tick_time}\n")
                zoo_cfg_file.write(f"initLimit={init_limit}\n")
                zoo_cfg_file.write(f"syncLimit={sync_limit}\n")
                zoo_cfg_file.write(f"clientPort={client_port}\n")
                zoo_cfg_file.write(f"dataDir={data_dir}\n")  # Add dataDir configuration
            
            self.text_box.insert(tk.END, f"\nzoo.cfg updated at: {zoo_cfg_path}")
        except Exception as e:
            self.text_box.insert(tk.END, f"\nError updating zoo.cfg: {e}")

    def check_java_git(self):
        """ Check if Java and Git are installed and show the results in the text box. """
        status = []

        # Check Java
        try:
            subprocess.run(['java', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status.append("Java is installed.")
            
            # Set JAVA_HOME environment variable if Java is installed
            java_home = r"C:\Program Files\Java\jdk-23"
            os.environ["JAVA_HOME"] = java_home
            status.append(f"JAVA_HOME is set to {java_home}.")
            # Also set it permanently by calling set_java_home()
            set_java_home()
        except subprocess.CalledProcessError:
            status.append("Java is not installed.")

        # Check Git
        try:
            subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            status.append("Git is installed.")
        except subprocess.CalledProcessError:
            status.append("Git is not installed.")

        # Show the status messages in the text box
        self.text_box.delete(1.0, tk.END)  # Clear the text box
        self.text_box.insert(tk.END, "\n".join(status))

        # If either Java or Git is missing, prompt the user to install them
        if "not installed" in status[0] or "not installed" in status[1]:
            self.text_box.insert(tk.END, "\n\nPlease install the missing software to proceed.")
            self.label.config(text="Java or Git is missing, please install them.")
        else:
            self.label.config(text="Click the button to select an XML file")

# Create and run the application
if __name__ == "__main__":
    app = XMLReaderApp()
    app.mainloop()
