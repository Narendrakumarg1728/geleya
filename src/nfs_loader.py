import lib.client
import lib.filer_interactor
import threading
import logging
import sys
import time
import json


class NFS:
    def __init__(self, filer, filer_user, filer_password, node_name, aggr_name, disk_count, vol_name, vol_count,
                 vol_size, use_existing_vol, vserver_name, data_ip, clients, client_user, client_password, mount_path, block_size,
                 run_time):
        self.filer = filer
        self.filer_user = filer_user
        self.filer_password = filer_password
        self.node_name = node_name
        self.aggr_name = aggr_name
        self.disk_count = disk_count
        self.vol_name = vol_name
        self.vol_size = vol_size
        self.vol_count = vol_count
        self.use_existing_vol = use_existing_vol
        self.vserver_name = vserver_name
        self. data_ip = data_ip
        self.clients = clients
        self.client_user = client_user
        self.client_password = client_password
        self.mount_path = mount_path
        self.block_size = block_size
        self.run_time = run_time

    def create_aggr(self):
        filer_connection = lib.filer_interactor.Filerops(self.filer, self.filer_user)
        filer_connection.aggr_create(self.aggr_name, self.disk_count, self.node_name)

    def vol_create(self, vol_name):
        filer_connection = lib.filer_interactor.Filerops(self.filer, self.filer_user)
        filer_connection.vol_create(vol_name, self.aggr_name, self.vol_size, self.vserver_name)

    def _run_load(self, vol, client, mount_path):
        client_connection = lib.client.CLIENTops(client, self.client_user, self.client_password)
        print(client_connection.mkdir_path(mount_path))
        client_connection.mount(self.data_ip, vol, mount_path)
        client_connection.run_load(mount_path, self.block_size, self.run_time)

    def start_stress(self):
        logging.info(self.create_aggr())
        time.sleep(5)
        vol_list = []
        for i in range(self.vol_count):
            if self.use_existing_vol:
                vol_list.append(self.vol_name + str(i))
            else:
                timestr = time.strftime("%Y%m%d_%H%M%S")
                vol_list.append(self.vol_name + timestr + "_" + str(i))
            logging.info(self.vol_create(vol_list[-1]))
            time.sleep(5)
        threads = []
        for client in self.clients:
            for vol in vol_list:
                m_path = self.mount_path + vol
                threads.append(threading.Thread(target=self._run_load, args=(vol, client, m_path)))
                threads[-1].start()
                time.sleep(5)
        for thread in threads:
            thread.join()

def main():
    file_name = sys.argv[1]  # Param file
    timestr = time.strftime("%Y%m%d_%H%M%S")  # Time stamp for the file name
    log_name = "./logs/loader_" + file_name + "_" + timestr + ".log"
    logging.basicConfig(filename=log_name, level=logging.INFO)
    logging.getLogger()
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
        load = NFS(filer, filer_user, filer_password, node_name, aggr_name, disk_count, vol_name, vol_count,
                              vol_size, use_existing_vol, vserver_name, data_ip, clients, client_user, client_password, mount_path,
                              block_size, run_time)
        threads.append(threading.Thread(target=load.start_stress))
        threads[-1].start()

    for thread in threads:
        thread.join()


if  __name__ =='__main__':main()
