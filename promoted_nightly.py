import time
import re
import logging
timestr = time.strftime("%Y%m%d-%H%M%S") # Time stamp for the file name
log_name = "./logs/" +  "BuilUpgradeHelper_" + timestr + ".log"
logging.basicConfig(filename=log_name, level=logging.INFO)
logging.getLogger()
import lib.filer_interactor
import threading

class BuildUpgrade:
    def __init__(self, filer_name, filer_username, filer_password):
        self.filer_name = filer_name
        self.filer_username = filer_username
        self.filer_password = filer_password
        # self.command = commands
        self.filer_connection = lib.filer_interactor.Filerops(self.filer_name, self.filer_username, self.filer_password)
        self.node_name = self.find_node_name_from_ip()

    def run_command(self, command):
        return self.filer_connection.filer_command_execute(command)

    @staticmethod
    def grep_for_a_word(multilines, pattern):
        logging.info("Grepping for pattern")
        for line in multilines.split("\n"):
            logging.info("Checking line:" + line)
            if re.search(pattern, line):
                logging.info("Match")
                return line
        return 0

    def promoted_to_nightly(self):
        # commands = ["clus image show", "storage failover show", "date", "cluster show"]
        commands = ["ls -l /var/etc/*pem", "sudo mkdir /var/etc/tmp", "sudo cp /var/etc/*pem /var/etc/tmp/",
                    "ls /var/etc/*devel*pem",
                    "sudo mv /var/etc/csc-development-chain.pem /var/etc/csc-production-chain.pem",
                    "sudo mv /var/etc/csc-development.pem /var/etc/csc-production.pem",
                    "sudo mv /var/etc/tsa-development-chain.pem /var/etc/tsa-production-chain.pem",
                    "sudo mv /var/etc/tsa-development.pem /var/etc/tsa-production.pem",
                    "ls /var/etc/*devel*pem"]
        for command in commands:
            systemshell_cmd = "set diag -confirmations off ;systemshell -node " + self.node_name + " -command " + command
            print(systemshell_cmd)
            logging.info(systemshell_cmd)
            logging.info(self.filer_connection.filer_command_execute(systemshell_cmd))

    def find_node_name_from_ip(self):
        out = self.run_command("network interface show -address " + self.filer_name + " -fields curr-node")
        out_list = out.split()
        print(out_list)
        logging.info(out_list)
        return out_list[13]

def main():
    filer_vm1 = "172.30.16.196"
    filer_vm2 = "172.30.16.188"
    systemshell_connections = []
    systemshell_connection1 = BuildUpgrade(filer_vm2, "admin", "netapp1!")
    systemshell_connections.append(systemshell_connection1)
    systemshell_connection2 = BuildUpgrade(filer_vm1, "admin", "netapp1!")
    systemshell_connections.append(systemshell_connection2)
    threads = []
    for systemshell_connection in systemshell_connections:
        message = "Starting promoted to nightly build upgrade changes."
        logging.info(message)
        print(message)
        print(time.localtime())
        threads.append(threading.Thread(target=systemshell_connection.promoted_to_nightly))
        threads[-1].start()
    for thread in threads:
        print(time.localtime())
        print("Joining threads")
        thread.join()

if  __name__ =='__main__':main()



