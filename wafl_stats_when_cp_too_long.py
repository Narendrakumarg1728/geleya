import time
import re
import logging
timestr = time.strftime("%Y%m%d-%H%M%S") # Time stamp for the file name
log_name = "./logs/" +  "check_wafl_cp_too_long_" + timestr + ".log"
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

    def check_cp_too_long(self, past_event_log_duration):
        return self.filer_connection.check_cp_too_long(past_event_log_duration)

    def get_wafl_stats(self):
        return self.filer_connection.get_wafl_stats()

    def initiate_wafl_sync(self):
        return self.filer_connection.initiate_wafl_sync()

    def initiate_panic_for_core(self):
        return self.filer_connection.initiate_panic_for_core()

def main():
    filer_vm1 = "172.30.16.146"
    filer_vm2 = "172.30.16.159"
    past_event_log_duration = 17
    while True:
        try:
            wafl_cp_stat_connection = CheckStatus(filer_vm1, "admin", "netapp1!")
            if not (wafl_cp_stat_connection.check_cp_too_long(past_event_log_duration)):
                t = time.localtime()
                print(t)
                logging.info(t)
            else:
                break
        except TimeoutError:
            continue
    message = "cp too long detected"
    print(message)
    logging.info(message)
    wafl_stats_connection1 = CheckStatus(filer_vm1, "admin", "netapp1!")
    wafl_stats_connection2 = CheckStatus(filer_vm2, "admin", "netapp1!")
    wafl_stats_connection1.get_wafl_stats()
    wafl_stats_connection2.get_wafl_stats()
    wafl_stats_connection1.initiate_wafl_sync()
    wafl_stats_connection2.initiate_wafl_sync()
    wafl_stats_connections = []
    wafl_stats_connections.append(wafl_stats_connection1)
    wafl_stats_connections.append(wafl_stats_connection2)
    threads = []
    for wafl_connection in wafl_stats_connections:
        message = "Starting to get core"
        logging.info(message)
        print(message)
        print(time.localtime())
        threads.append(threading.Thread(target=wafl_connection.initiate_panic_for_core))
        threads[-1].start()
    for thread in threads:
        print(time.localtime())
        print("Joining threads")
        thread.join()


if  __name__ =='__main__':main()
