import lib.ssh_execute
import logging
import uuid


class CLIENTops:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client_connection = lib.ssh_execute.SSHCMDExecute(self.host, self.username, self.password)

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def client_command_execute(self, command):
        return self.client_connection.run_ssh_cmd(command)

    def client_command_execute_backgroud(self, command, run_time, file_name):
        return self.client_connection.run_background_command(command, run_time, file_name)

    def mkdir_path(self, mount_path):
        mount_path_list = mount_path.split("/")
        logging.info(mount_path_list)
        mount_start = ""
        slash = "/"
        for mount_dir in mount_path_list:
            mount_start = mount_start + slash + mount_dir
            self.client_command_execute("mkdir " + mount_start)

    def mount(self, filer_ip, vol_name , mount_path):
        self.mkdir_path(mount_path)
        cmd = "mount " + filer_ip + ":/" + vol_name + " " + mount_path
        self.client_command_execute(cmd)

    def run_load(self, mount_path, block_size, run_time):
        file_name = str(uuid.uuid4())
        cmd = "/usr/software/test/bin/dt.18.31 of=" + mount_path + "/" + file_name + " keepalive=300 keepalivet=300 " +  \
        "bufmodes=unbuffered dispose=keep incr=var iotype=random history=3 hdsize=128 min=2k max=4k bs=" + block_size \
                + " limit=90G flags=direct oflags=trunc oncerr=abort noprogt=10s noprogtt=120s pattern=iot procs=10 " \
                  + "runtime=" + str(run_time) + " stopon=/tmp/" + file_name +".dt"
        self.client_command_execute_backgroud(cmd, run_time, file_name)