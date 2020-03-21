import paramiko
import re
import logging


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
        logging.info("#"*50 + "\n")
        logging.info("ssh_cmd_executor")
        logging.info("#" * 50 + "\n")
        self.current_stats = self.run_ssh_cmd("hostname")

    def __repr__(self):
        logging.info("#" * 50 + "\n")
        status_of_host = 'SSH executor on host ' + self.current_stats
        logging.info("#" * 50 + "\n")
        return status_of_host

    def __str__(self):
        logging.info("#" * 50 + "\n")
        status_of_host = 'Class to interact with ssh enabled host machines'
        logging.info("#" * 50 + "\n")
        return status_of_host

    def run_ssh_cmd(self, command):
        """
        Executes the command provided on the machines where prameters are initialized in __init__
        :param command:
        :return: command output
        """
        try:
            port = 22
            client_connection = paramiko.SSHClient()
            client_connection.load_system_host_keys()
            client_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logging.info("#" * 50 + "\n")
            logging.info("****     Creating ssh connection to Machine: " + self.host + ". With Username: " +
                         self.username + " and password: " + self.password + " ****")
            logging.info("#" * 50 + "\n")
            client_connection.connect(self.host, port=port, username=self.username, password=self.password)
            logging.info("#" * 50 + "\n")
            logging.info("****     Executing command: " + command + " ****")
            logging.info("#" * 50 + "\n")
            stdin, stdout, stderr = client_connection.exec_command(command)
            if stderr:
                logging.debug("#" * 50 + "\n")
                logging.debug("Found stderr")
                logging.debug("#" * 50 + "\n")
                logging.debug(stderr)
                logging.debug("#" * 50 + "\n")
            # self.log.info(stdout.read())
            cmd_output = stdout.read()
            logging.info("#"*50 + "\n")
            logging.info(cmd_output)
            logging.info("#"*50 + "\n")
            client_connection.close()
            return cmd_output.decode('ascii')
        except:
            logging.info("#" * 50 + "\n")
            logging.info("****     Caught an exception closing connection      ****")
            client_connection.close()
            logging.info("#" * 50 + "\n")
            return "Error connecting to client " + self.host

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
