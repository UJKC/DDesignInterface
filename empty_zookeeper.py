from zookeeper_manager import ZookeeperManager
import tkinter as tk

class Empty_Zookeeper(ZookeeperManager):
    def __init__(self, text_box):
        super().__init__(text_box)


    def empty_zookeeper(self, root):
        self.root = root
        """Handle Empty_Zookeeper project type."""
        self.text_box.insert(tk.END, "Empty_Zookeeper detected...\n")
        self.update_zoo_cfg(root)
        self.show_zookeeper_buttons()
