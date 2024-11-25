import os
import subprocess
import time
import platform
import tkinter as tk

class ZookeeperManager:
    def __init__(self, text_box):
        self.text_box = text_box
        self.zk_pid = None

        # Initialize start/stop buttons
        self.start_button = None
        self.stop_button = None

    def show_zookeeper_buttons(self):
        """ Show the start and stop buttons for Zookeeper """
        self.start_button = tk.Button(self.text_box.master, text="Start Zookeeper", command=self.start_zookeeper, bg="green", fg="white")
        self.stop_button = tk.Button(self.text_box.master, text="Stop Zookeeper", command=self.stop_zookeeper, bg="red", fg="white")
        
        self.start_button.pack(pady=10)
        if platform.system() == "Windows":
            self.stop_button.pack(pady=10)
            self.stop_button.config(state=tk.DISABLED)

    def update_zoo_cfg(self, root):
        """ Update the zoo.cfg file with the provided values """
        try:
            zoo_cfg_path = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "conf", "zoo.cfg")
            data_dir = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "log")

            tick_time = root.find('tickTime').text
            init_limit = root.find('initLimit').text
            sync_limit = root.find('syncLimit').text
            client_port = root.find('clientPort').text

            with open(zoo_cfg_path, 'a') as zoo_cfg_file:
                zoo_cfg_file.write(f"\ntickTime={tick_time}\n")
                zoo_cfg_file.write(f"initLimit={init_limit}\n")
                zoo_cfg_file.write(f"syncLimit={sync_limit}\n")
                zoo_cfg_file.write(f"clientPort={client_port}\n")
                zoo_cfg_file.write(f"dataDir={data_dir}\n")

            self.text_box.insert(tk.END, f"\nzoo.cfg updated at: {zoo_cfg_path}")

        except Exception as e:
            self.text_box.insert(tk.END, f"Error updating zoo.cfg: {e}")

    def start_zookeeper(self):
        """ Start the Zookeeper server """
        self.text_box.insert(tk.END, "Starting Zookeeper...\n")
        if platform.system() == 'Windows':
            zk_server_cmd = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "bin", "zkServer.cmd")
            subprocess.Popen([zk_server_cmd])
        elif platform.system() == 'Linux':
            zk_server_sh = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "bin", "zkServer.sh")
            subprocess.Popen([zk_server_sh, "start"])

        time.sleep(5)
        self.start_zookeeper_cli()

    def start_zookeeper_cli(self):
        """ Start Zookeeper CLI """
        if platform.system() == 'Windows':
            zk_cli_cmd = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "bin", "zkCli.cmd")
            subprocess.Popen(['start', 'cmd', '/K', zk_cli_cmd], shell=True)
        elif platform.system() == 'Linux':
            zk_cli_sh = os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "bin", "zkCli.sh")
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', zk_cli_sh])

    def stop_zookeeper(self):
        """ Stop the Zookeeper server """
        self.text_box.insert(tk.END, "Stopping Zookeeper...\n")
        if self.zk_pid is not None:
            try:
                subprocess.run([os.path.join(os.getcwd(), "DDResouces", "apache-zookeeper-3.9.3-bin", "bin", "zkServer.sh"), "stop"])
                self.text_box.insert(tk.END, "Zookeeper stopped successfully.")
                self.zk_pid = None
                self.stop_button.config(state=tk.DISABLED)
            except Exception as e:
                self.text_box.insert(tk.END, f"Error stopping Zookeeper: {e}")
