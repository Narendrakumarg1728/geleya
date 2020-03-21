import re
import logging
import json
import lib.client
import lib.filer_interactor


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def grep_for_a_word(multilines, pattern):
        logging.info("Grepping for pattern")
        for line in multilines.split("\n"):
            logging.info("Checking line:" + line)
            if re.search(pattern, line):
                logging.info("Match")
                return line
        return 0

class POPULATEparams:
    def __init__(self, param_file):
        with open(param_file) as json_file:
            sets = json.load(json_file)
        filer_details = sets["parameters"]["filer_details"]
        self.filer_name = filer_details["filer"]
        self.filer_user = filer_details["filer_user"]
        self.filer_password = filer_details["filer_password"]
        client_details = sets["parameters"]["client_details"]
        self.clients = client_details["clients"]
        self.client_user = client_details["client_user"]
        self.client_password = client_details["client_password"]
        self.filer_connection = lib.filer_interactor.Filerops(self.filer_name, self.filer_user, self.filer_password)
        self.node1, self.node2 = self.get_node_names()
        print(self.node1, self.node2)
        self.node1_aggr1, self.node1_aggr2 = self.get_aggr_names(self.node1)
        print(self.node1_aggr1, self.node1_aggr2)
        self.node2_aggr1, self.node2_aggr2 = self.get_aggr_names(self.node2)
        print(self.node2_aggr1, self.node2_aggr2)
        # print(self.filer_name, self.filer_user, self.filer_password, self.clients, self.client_user, self.client_password)

    def get_node_names(self):
        out = self.filer_connection.filer_command_execute("system node show")
        out_list = out.split()
        print(out_list)
        return out_list[19], out_list[24]

    def get_aggr_names(self, node_name):
        command = "storage  aggregate show -has-mroot false -node " + node_name
        out = self.filer_connection.filer_command_execute(command)
        out_list = out.split()
        try:
            aggr1 = out_list[22]
        except IndexError:
            aggr1 = 0
        try:
            aggr2 = out_list[32]
        except IndexError:
            aggr2 = 0
        return aggr1, aggr2


def main():
    test = POPULATEparams("basic_param.json")
    # test.get_basic_info("basic_param.json")


if __name__ == '__main__':main()




