import paramiko
import re
import logging
import time
import scp

logging.basicConfig(filename="logger2.log", level=logging.INFO)
logging.info("#" * 10 + "\n" + 'Starting test_ssh_execute.py ' + "#" * 10 + "\n")
logging.getLogger()

class SSHCMDExecute:
    """
    Class for easy command execution. Uses parmiko module to set the connection.
    After initial connection, passing command for the execution is sufficient.
    Handled initial connection establishment and closing of connection.
    """
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        logging.info("#"*10  + "ssh_cmd_executor" + "#" * 10 + "\n")
        self.current_stats = self.run_ssh_cmd("date")

    def __repr__(self):
        status_of_host = 'SSH executor: Date on host ' + self.current_stats
        logging.info("#" * 10 + status_of_host + "#" * 10 + "\n")
        return status_of_host

    def __str__(self):
        status_of_host = 'Class to interact with ssh enabled host machines... Date on host: '
        logging.info("#" * 10 + status_of_host + "#" * 10 + "\n")
        return status_of_host

    @staticmethod
    def _ascii_conversion(cmd):
        return cmd.decode('ascii')

    @staticmethod
    def _grep_for_a_word(multilines, pattern):
        logging.info("Grepping for pattern")
        for line in multilines.split("\n"):
            logging.info("Checking line:" + line)
            if re.search(pattern, line):
                logging.info("Match")
                return line
        return 0


    def run_ssh_cmd(self, command):
        """
        Executes the command provided on the machines where prameters are initialized in __init__
        :param command:
        :return: command output
        """
        #try:
        port = 22
        client_connection = paramiko.SSHClient()
        client_connection.load_system_host_keys()
        client_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logging.info("#" * 10  + "****     Creating ssh connection to Machine: " + self.host +
                    ". With Username: " + self.username + " and password: " + self.password +
                     " ****" + "#" * 10 + "\n")
        client_connection.connect(self.host, port=port, username=self.username, password=self.password)
        logging.info("#" * 10  + "****     Executing command: " + command + " ****" + "#" * 10 + "\n")
        stdin, stdout, stderr = client_connection.exec_command(command)
        """
        if stderr:
            logging.debug("#" * 10 + "Found stderr: "  + stderr + "#" * 10 + "\n")
        """
        #self.log.info(stdout.read())
        cmd_output = stdout.read()
        #logging.info("#"*10  + cmd_output.decode("ascii") + "#"*10 + "\n")
        #logging.info("****     Closing ssh connection to Machine: " + self.host + " ****")
        client_connection.close()
        #logging.info("****     Closed ssh connection to Machine successfully: " + self.host + " ****")
        return cmd_output.decode('ascii')
    """
        except:
            logging.info("#" * 10  + "***    Caught an exception closing connection      ***" + "#" * 10 + "\n")
            logging.info(stderr.read())
            client_connection.close()
            return "Error connecting to client " + self.host
    """

    def run_background_command(self, cmd, run_time_seconds, unique_identity):
        """
        Runs commands which will hold the ssh connection and then checks the process using unique identity
        :param cmd:
        :param run_time_seconds:
        :param unique_identity:
        :return:

        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, username=self.username, password=self.password)
        transport = ssh.get_transport()
        client_connection_background = transport.open_session()
        client_connection_background.get_pty()
        client_connection_background.set_combine_stderr(True)
        logging.info("#" * 10 + "****     Executing command: " + cmd + " ****" + "#" * 10 + "\n")
        client_connection_background.exec_command(cmd)  # will return instantly due to new thread being spawned.
        # do something else
        end_time = time.time() + run_time_seconds
        while time.time() < end_time:
            logging.info("#" * 10  + "****     Sleeping for 60 secs ****" + "#" * 10 + "\n")
            time.sleep(60)  # wait 60 seconds
            pgrep_identifier = "ps -ef | grep " + unique_identity
            _, stdout, _ = ssh.exec_command(pgrep_identifier)  # or explicitly pkill tcpdump
            logging.info(
                "#" * 10  + pgrep_identifier +"\n"+ stdout.read().decode('ascii') + "#" * 10 + "\n")
            # stdout.read()  # other command, differ
            # ent shell
        client_connection_background.close()  # close channel and let remote side terminate your proc.
        time.sleep(10)


    def scp_put(self, file):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, username=self.username, password=self.password)
        scp_connection = scp.SCPClient(ssh.get_transport())
        scp_connection.put(file, recursive=True,
                         remote_path="/etc/pki/ca-trust/source/anchors/")





