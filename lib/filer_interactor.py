import lib.ssh_execute
import logging
import lib.helper
import re
import time

class Filerops:
    def __init__(self, host, username, password="netapp1!"):
        self.host = host
        self.username = username
        self.password = password
        self.filer_connection = lib.ssh_execute.SSHCMDExecute(self.host, self.username, self.password)
        self.vserver = self._get_nfs_data_vserver()

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def filer_command_execute(self, command):
        return self.filer_connection.run_ssh_cmd(command)

    def filer_command_execute_backgroud(self, command, run_time, unique_identity):
        return self.filer_connection.run_background_command(command, run_time, unique_identity)

    def stats_commands(self):
        commands = ["set admin", "rows 5000", "run local version", "run local sysconfig -av", "storage failover show",
                    "storage failover show -instance",
                    "set diag -confirmations off; storage failover show -fields local-missing-disks,partner-missing-disks" 
                    "metrocluster show", "metrocluster node show", "metrocluster node show -instance",
                    "metrocluster operation show", "run local aggr status", "aggr status -r", "run local disk show -v",
                    "run local aggr status -r",   "run local aggr status -v",
                    "storage aggregate show -nodes * -is-home false -fields owner-name,home-name,state",
                    "storage aggregate show -instance", "disk show -ownership", "storage disk show -broken",
                    "system show -instance", "date", "system node show -instance","cluster show",
                    "set diag -confirmations off; system node image show",
                    "network interface show -role data -is-home false", "volume show -state offline",
                    "network interface failover-groups show", "network port vlan show", "system license show",
                    "system node autosupport show",
                    "set diag -confirmations off;show-periodic -interval 2 -iterations 3"]
        for command in commands:
            logging.info(self.filer_command_execute(command))

    def aggr_create(self, aggr_name, disk_count, node_name):
        command = "storage aggregate create -aggregate %s -diskcount %d -node %s" %(aggr_name, disk_count, node_name)
        logging.info(self.filer_command_execute(command))

    def vol_create(self, vol_name, aggr_name, vol_size, vserver_name):
        command = "volume create -volume %s -aggregate %s -size %s -unix-permissions 777 -state online \
            -junction-path /%s -policy default -vserver %s" %(vol_name, aggr_name, vol_size, vol_name, vserver_name)
        logging.info(self.filer_command_execute(command))

    def _get_nfs_data_vserver(self):
        command = "vserver show -type data -allowed-protocols nfs"
        logging.info(self.filer_command_execute(command))
        return self.filer_command_execute(command)

    def storage_failover_show(self):
        command = "storage failover show"
        return self.filer_command_execute(command)

    def is_storage_failover_enabled(self):
        test = self.storage_failover_show()
        if lib.helper.Helper.grep_for_a_word(test, "enabled"):
            return "storage failover enabled"
        else:
            return "storage failover disabled"

    def aggr_add_disk(self, aggr_name, disk_count):
        command = "storage aggregate add-disks -agregate " + aggr_name + " -diskcount " + disk_count
        logging.info(self.filer_command_execute(command))

    def vol_move(self, vol_name, dest_aggr):
        command = "volume move -volume " + vol_name + "-destination_aggregate " + dest_aggr
        logging.info(self.filer_command_execute(command))

    def run_local_panic(self):
        command = "run local panic"
        logging.info(self.filer_command_execute(command))

    def arl(self, aggr_name, dest_node):
        command = "storage aggregate relocation start -aggregate " + aggr_name + " -destination-aggregate " + dest_node
        logging.info(self.filer_command_execute(command))

    def check_aggr_owner_name(self, aggr_name):
        command = "storage aggregate show -fields ownername -aggregate " + aggr_name
        return self.filer_command_execute(command)

    def check_vol_owner_name(self, vol_name):
        command = "volume show -fields ownername -volume " + vol_name
        return self.filer_command_execute(command)

    @staticmethod
    def grep_for_a_word(multilines, pattern):
        logging.info("Grepping for pattern")
        for line in multilines.split("\n"):
            logging.info("Checking line:" + line)
            if re.search(pattern, line):
                logging.info("Match")
                return line
        return 0

    def check_event_unsync(self, past_num_minutes):
        """
        :param past_num_minutes: checking event logs for past number of minutes
        :return: 1 if unsync log found
        """
        cmd = "event log show -event *unsynchronized* -time >" + str(past_num_minutes) + "m"
        out = self.filer_command_execute(cmd)
        logging.info(out)
        if self.grep_for_a_word(out, "unsynchronized log"):
            logging.info("unsynchronized log")
            print("unsynchronized log")
            return 1
        else:
            logging.info("No unsync log in the event logs")
            print("No unsynchronized log in the event logs")
            return 0

    def check_nvmm_mirror_abort(self, past_num_minutes):
        """
        :param past_num_minutes: checking event logs for past number of minutes
        :return: 1 if nvmm mirror aborts found
        """
        cmd = "set diag -confirmations off;event log show -event *nvmm.mirror.aborting* -time >" + str(
            past_num_minutes) + "m"
        out = self.filer_command_execute(cmd)
        logging.info(out)
        if self.grep_for_a_word(out, "nvmm.mirror.aborting"):
            logging.info("nvmm.mirror.aborting")
            print("unsynchronized log")
            return 1
        else:
            logging.info("No nvmm.mirror.aborting log in the event logs")
            print("No nvmm.mirror.aborting in the event logs")
            return 0

    def check_cp_too_long(self, past_num_minutes):
        """
        :param past_num_minutes: checking event logs for past number of minutes
        :return: 1 if unsync log found
        """
        cmd = "event log show -event wafl.cp.toolong*  -time >" + str(past_num_minutes) + "m"
        out = self.filer_command_execute(cmd)
        logging.info(out)
        if self.grep_for_a_word(out, "toolong"):
            logging.info("wafl.cp.toolong")
            print("wafl.cp.toolong")
            return 1
        else:
            logging.info("No wafl.cp.toolong event logs")
            print("No wafl.cp.toolong event logs")
            return 0

    def initiate_packet_trace(self, port_name, run_time):
        cmd = "sudo vcontext -v -5 /usr/sbin/tcpdump tcpdump -i " + port_name + " -w /mroot/pkt_trace_" + port_name + ".trc"
        return self.filer_command_execute_backgroud(cmd, run_time, port_name)

    def get_wafl_stats(self):
        cmd = "set test -confirmations off; run local wafl stats"
        wafl_stats = self.filer_command_execute(cmd)
        print(wafl_stats)
        logging.info(wafl_stats)
        file_name = "wafl_stats_" + self.host
        with open(file_name, "w") as fp:
            fp.write(wafl_stats)
        return wafl_stats

    def initiate_wafl_sync(self):
        cmd = "set test -confirmations off;run local sync"
        return self.filer_command_execute(cmd)


    def initiate_panic_for_core(self):
        cmd = "set test -confirmations off; cluster ha modify -configured false ;storage failover modify -enabled false -node *"
        self.filer_command_execute(cmd)
        time.sleep(5)
        cmd = "set test -confirmations off;run local panic"
        return self.filer_command_execute(cmd)



