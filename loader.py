import logging
import sys
import time
import json
file_name = sys.argv[1] # Param file
timestr = time.strftime("%Y%m%d-%H%M%S") # Time stamp for the file name
log_name = "./logs/loader_" + file_name + "_" + timestr + ".log"
logging.basicConfig(filename=log_name, level=logging.INFO)
logging.getLogger()
import threading
import src.nfs_loader as nfs_loader
import lib.filer_interactor


with open(file_name) as json_file:
    sets = json.load(json_file)

threads = []
for i in sets:
    data = sets[i]
    print(data)
    filer_details = data["parameters"]["filer_details"]
    filer = filer_details["filer"]
    filer_user = filer_details["filer_user"]
    filer_password = filer_details["filer_password"]
    node_name = filer_details["node_name"]
    aggr_name = filer_details["aggr_name"]
    disk_count = filer_details["disk_count"]
    vol_name = filer_details["vol_name"]
    vol_count = filer_details["vol_count"]
    vol_size = filer_details["vol_size"]
    use_existing_vol = filer_details["use_existing_vol"]
    vserver_name = filer_details["vserver_name"]
    data_ip = filer_details["data_ip"]
    client_details = data["parameters"]["client_details"]
    clients = client_details["clients"]
    client_user = client_details["client_user"]
    client_password = client_details["client_password"]
    mount_path = client_details["mount_path"]
    block_size = client_details["block_size"]
    run_time = client_details["run_time"]
    load = nfs_loader.NFS(filer, filer_user, filer_password, node_name, aggr_name, disk_count, vol_name, vol_count,
                          vol_size, use_existing_vol, vserver_name, data_ip, clients, client_user, client_password, mount_path,
                          block_size,
                          run_time)
    threads.append(threading.Thread(target=load.start_stress))
    threads[-1].start()

for thread in threads:
    thread.join()
