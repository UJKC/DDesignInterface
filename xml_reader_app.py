import time
import tkinter as tk
from tkinterdnd2 import TkinterDnD
from tkinter import filedialog
import xml.etree.ElementTree as ET
from zookeeper_manager import ZookeeperManager
from utils import check_java_git, clone_repository

class XMLReaderApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("XML Reader App")
        self.geometry("1000x1000")

        # Initialize components
        self.label = tk.Label(self, text="Click the button to select an XML file", pady=20, padx=20)
        self.label.pack(fill=tk.BOTH, expand=True)

        self.text_box = tk.Text(self, wrap=tk.WORD, width=50, height=15)
        self.text_box.pack(pady=20)

        # Check Java and Git installation
        check_java_git(self.text_box)

        # XML file selection button
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
            tree = ET.parse(file_path)
            root = tree.getroot()

            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, ET.tostring(root, encoding='unicode', method='xml'))

            time.sleep(30)

            clone_repository(self.text_box, root)
                
        except Exception as e:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, f"Error reading file: {e}")
