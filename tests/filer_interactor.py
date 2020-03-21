import lib.ssh_execute
import logging
import uuid

class Filerops:
    def __init__(self, host, username, password="netapp1!"):
        self.host = host
        self.username = username
        self.password = password
        self.filer_connection = lib.ssh_execute.SSHCMDExecute(self.host, self.username, self.password)


    def __repr__(self):
        pass


    def __str__(self):
        pass


    def client_command_execute(self, command):
        return self.filer_connection.run_ssh_cmd(command)


    def client_command_execute_backgroud(self, command, run_time, unique_identity):
        return self.filer_connection.run_background_command(command, run_time, unique_identity)


    def stats_commands(self):
        commands = ["set admin", "rows 5000", "run local version"]
        for command in commands:
            logging.info(self.filer_command_execute(command))




