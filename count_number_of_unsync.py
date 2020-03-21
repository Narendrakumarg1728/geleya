import time
import re
import logging
import sys

timestr = time.strftime("%Y%m%d-%H%M%S") # Time stamp for the file name
log_name = "./logs/" +  "check_sfo_stats_" + timestr + ".log"
logging.basicConfig(filename=log_name, level=logging.INFO)
logging.getLogger()
import lib.filer_interactor

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

    def check_event_unsync(self, past_event_log_duration):
        return self.filer_connection.check_event_unsync(past_event_log_duration)

    def initiate_packet_trace(self, port_name, run_time):
        return self.filer_connection.initiate_packet_trace(port_name, run_time)

def main():
    filer_vm1 =  sys.argv[1] # "172.30.16.146"
    # filer_vm2 = "172.30.16.205"
    past_event_log_duration = 5
    sfo_stat_connection =  CheckStatus(filer_vm1, "admin", "netapp1!" )
    number_of_unsync = 0
    while True:
        try:
            if not (sfo_stat_connection.check_event_unsync(past_event_log_duration)):
                t = time.localtime()
                print(t)
                logging.info(t)
                time.sleep(30)
                message = f"Number of unsync so far: {number_of_unsync}\n"
                print(message)
                logging.info(message)
            else:
                number_of_unsync = number_of_unsync + 1
                message = f"Unsync detected: Number of unsync so far: {number_of_unsync}\n Sleeping for 8 minutes"
                print(message)
                logging.info(message)
                time.sleep(480) #Sleep for 8 mins
        except TimeoutError:
            continue

if  __name__ =='__main__':main()



