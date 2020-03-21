import time
import re
import logging
timestr = time.strftime("%Y%m%d-%H%M%S") # Time stamp for the file name
log_name = "./logs/" +  "check_sfo_stats_" + timestr + ".log"
logging.basicConfig(filename=log_name, level=logging.INFO)
logging.getLogger()
import lib.filer_interactor
import threading

class CheckStatus:
    def __init__(self, filer_name, filer_username, filer_password):
        self.filer_name = filer_name
        self.filer_username = filer_username
        self.filer_password = filer_password
        # self.command = commands
        self.filer_connection = lib.filer_interactor.Filerops(self.filer_name, self.filer_username, self.filer_password)

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

    def check_nvmm_mirror_abort(self, past_event_log_duration):
        return self.filer_connection.check_nvmm_mirror_abort(past_event_log_duration)

    def initiate_packet_trace(self, port_name, run_time):
        return self.filer_connection.initiate_packet_trace(port_name, run_time)

def main():
    filer_vm1 = "172.30.16.127"
    filer_vm2 = "172.30.16.54"
    past_event_log_duration = 10
    sfo_stat_connection = CheckStatus(filer_vm1, "admin", "netapp1!")
    while True:
        try:
            if not (sfo_stat_connection.check_nvmm_mirror_abort(past_event_log_duration)):
                #
                t = time.localtime()
                print(t)
                logging.info(t)
            else:
                break
        except TimeoutError:
            print("TimeoutError detected")
            logging.info("TimeoutError detected")
            continue
    message = "Unsync detected...."
    print(message)
    logging.info(message)
    systemshell_connections = []
    systemshell_connection1 = CheckStatus(filer_vm2, "diag", "netapp1!")
    systemshell_connections.append(systemshell_connection1)
    systemshell_connection2 = CheckStatus(filer_vm1, "diag", "netapp1!")
    systemshell_connections.append(systemshell_connection2)
    threads = []
    for systemshell_connection in systemshell_connections:
        message = "Starting packet trace on filer"
        logging.info(message)
        print(message)
        print(time.localtime())
        threads.append(threading.Thread(target=systemshell_connection.initiate_packet_trace, args=("e0c", 100)))
        threads[-1].start()
    for thread in threads:
        print(time.localtime())
        print("Joining threads")
        thread.join()

if  __name__ =='__main__':main()



