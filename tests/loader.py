
import logging
import threading
import sys
import time
import json
import src.nfs_loader as nfs_loader

file_name = sys.argv[1] # Param file
timestr = time.strftime("%Y%m%d-%H%M%S") # Time stamp for the file name
log_name = "./logs/loader_" + file_name + "_" + timestr + ".log"
logging.basicConfig(filename=log_name, level=logging.INFO)
logging.getLogger()

with open(file_name) as json_file:
    data = json.load(json_file)

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
vserver_name = filer_details["vserver_name"]
data_ip = filer_details["data_ip"]

client_details = data["parameters"]["client_details"]
clients = client_details["clients"]
client_user = client_details["client_user"]
client_password = client_details["client_password"]
mount_path = client_details["mount_path"]
block_size = client_details["block_size"]
run_time = client_details["run_time"]

vol_list = []
if vol_count > 1:
    for i in range(vol_count):
        vol_list.append(vol_name + str(i))
threads = []
for client in clients:
    for vol in vol_list:
        m_path = mount_path + vol
        load = nfs_loader.NFS(filer, filer_user, filer_password, node_name, aggr_name, disk_count, vol, vol_size,
               vserver_name, data_ip, client, client_user, client_password, m_path, block_size, run_time)
        logging.info(load.create_aggr())
        logging.info(load.vol_create())
        threads.append(threading.Thread(target=load.run_load))
        threads[-1].start()
        #logging.info(load.run_load())

for thread in threads:
    thread.join()
