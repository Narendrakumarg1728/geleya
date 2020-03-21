import src.client
import logging
import threading

logging.basicConfig(filename='logger2.log', level=logging.INFO)
logging.warning("#" * 50 + 'Starting test_ssh_execute.py ' + "#" * 50 + "\n")
logging.getLogger()

def test_client_execute():
    logging.info("Tetsing 123\n")
    filer_connection = src.client.CLIENTops("172.30.16.212", "root", "netapp1!")
    #logging.info(filer_connection.client_command_execute("uname -a"))
    logging.info(filer_connection.mkdir_path("/load/narendra/test123/vol_knarendr126202023334_B2_5"))
    logging.info(filer_connection.mount("172.30.16.110", "vol_knarendr126202023334_B2_5", "/load/narendra/test123/vol_knarendr126202023334_B2_5"))
    """
    for i in range(10):
        logging.info("Iteration: " + str(i))
        logging.info(filer_connection.run_load("/load/narendra/test123/vol_knarendr126202023334_B2_5", "4k", 120))
        
    """
    t1 = threading.Thread(target = filer_connection.run_load,
                          args=("/load/narendra/test123/vol_knarendr126202023334_B2_5", "4k", 120))
    t2 = threading.Thread(target=filer_connection.run_load,
                          args=("/load/narendra/test123/vol_knarendr126202023334_B2_5", "4k", 120))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def main():
    test_client_execute()


if __name__ == "__main__":
    main()


