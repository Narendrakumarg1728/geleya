import src.client
import logging
import threading
import lib.filer_interactor

logging.basicConfig(filename='logger2.log', level=logging.INFO)
logging.warning("#" * 10 + 'Starting test_ssh_execute.py ' + "#" * 10 + "\n")
logging.getLogger()

def test_client_execute(clients):
    logging.info("Test_client_execute 123\n")
    username= "root"
    password = "netapp1!"
    mount_path = "/load/narendra/test123/"
    data_ip = "172.30.16.110"
    vol_initial_name = "vol_A4_vvvv"
    vol_count = 3
    block_size = "4k"
    run_time = 43200 #12 hours
    client_connections = []
    num_of_threads_on_each_vol = 5
    list_of_volumes = []
    mount_path_each_vol = []
    for volume_append in range(vol_count):
        vol_name = vol_initial_name + str(volume_append)
        list_of_volumes.append(vol_name) # for future to see if we need the list of all the volumes
        mount_path_each_vol.append(mount_path + vol_name)
        logging.info("mount_path_each_vol list:")
        logging.info(mount_path_each_vol)
        for client in clients:
            client_connections.append(src.client.CLIENTops(client, username, password))
            logging.info(client_connections[-1].mkdir_path(mount_path_each_vol[-1]))
            #using the last created client connection
            logging.info(client_connections[-1].mount(data_ip, vol_name,
                                            mount_path_each_vol[-1]))
    threads = []
    for mount in mount_path_each_vol:
        for client_connection in client_connections:
            for thread in range (num_of_threads_on_each_vol):
                threads.append(threading.Thread(target=client_connection.run_load,
                                            args=(mount, block_size, run_time)))
                threads[-1].start()
    for thread in threads:
        thread.join()

def filers_execute():
    logging.info("Tetsing Filer ops\n")
    filer = lib.filer_interactor.Filerops("172.30.16.118", "admin", "netapp1!")
    filer.aggr_create("A4", 1, "knarendr126202023334-rg-ha1-vm1")
    vol_initial_name = "vol_A4_vvvv"
    vol_count =2
    filer.vol_create(vol_initial_name, vol_count, "A4", "10g", "svm_knarendr126202023334-cot-deployment")
    #filer.stats_commands()

def main():
    clients = ["172.30.16.212", "172.30.16.213", "172.30.16.214", "172.30.16.215", "172.30.16.216"]
    filers_execute()
    test_client_execute(clients)
    filer = lib.filer_interactor.Filerops("172.30.16.118", "admin", "netapp1!")
    filer.stats_commands()

if __name__ == "__main__":
    main()
