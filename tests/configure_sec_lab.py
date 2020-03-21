import src.client
import logging
import scp
import threading

logging.basicConfig(filename='logger2.log', level=logging.INFO)
logging.warning("#" * 50 + 'Starting test_ssh_execute.py ' + "#" * 50 + "\n")
logging.getLogger()


def test_client_execute(client):
    logging.info("Tetsing 123\n")
    filer_connection = src.client.CLIENTops(client, "knarendr", "Babydance@1728")
    # logging.info(filer_connection.client_command_execute("uname -a"))
    cert = "-----BEGIN CERTIFICATE-----\n\
MIIDaTCCAlGgAwIBAgIJAOq/zL+84IswMA0GCSqGSIb3DQEBCwUAMFoxCzAJBgNV\n\
BAYTAlVTMQswCQYDVQQIDAJOQzEMMAoGA1UEBwwDUlRQMQ8wDQYDVQQKDAZOZXRB\n\
cHAxDTALBgNVBAsMBEVTSVMxEDAOBgNVBAMMB1NTRk1DQ0EwHhcNMTcxMTAxMjEw\n\
OTQyWhcNMjcxMDMwMjEwOTQyWjBaMQswCQYDVQQGEwJVUzELMAkGA1UECAwCTkMx\n\
DDAKBgNVBAcMA1JUUDEPMA0GA1UECgwGTmV0QXBwMQ0wCwYDVQQLDARFU0lTMRAw\n\
DgYDVQQDDAdTU0ZNQ0NBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA\n\
iaD9Ee0Yrdka0I+9GTJBIW/Fp5JU6kyjaxfOldW/R9lEubegXQFhDD2Xi1HZ+fTM\n\
f224glB9xLJXAHhipRK01C2MgC4kSH75WL1iAiYeOBloExqmK6OCX+sdyO7RXm/H\n\
Ra9tN2INWdvyO2pnmxsSnq56mCMsUZLtrRKp89FWgcxLg5r8QxH7xwfh5k54rxjE\n\
144TD9yrIiQOgRSIRHUrVJ9l/F/gnwzP8wcNABeXwN71Mzl7mliPA703kONQIAyU\n\
0E0tLpmy/U8dZdMmTBZGB7jI9f95Hl1RunfwhR371a6z38kgkvwrLzl4qflfsPjw\n\
K9n4omNk9rCH9H9tWkxxjwIDAQABozIwMDAdBgNVHQ4EFgQU/bFyCCnqdDFKlQBJ\n\
ExtV6wcMYkEwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAOQMs\n\
Pz2iBD1+3RcSOsahB36WAwPCjgPiXXXpU+Zri11+m6I0Lq+OWtf+YgaQ8ylLmCQd\n\
0p1wHlYA4qo896SycrhTQfy9GlS/aQqN192k3oBGoJcMIUnGUBGuEvyZ2aDUfkzy\n\
JUqBe+0KaT7pkvvbRL7VUz34I7ouq9fQIRZ26vUDLTY3KM1n/DXBj3e30GHGMV3K\n\
NN2twuLXPNjnryfgpliHU1rwV7r1WvrCVn4StjimP2bO5HGqD/SbiYUL2M9LOuLK\n\
6mqY4OHumYXq3k7CHrvt0FepsN0L14LYEt1LvpPDFWP3SdN4z4KqT9AGqBaJnhhl\n\
Qiq8GWnAChspdBLxCg==\n\
-----END CERTIFICATE-----"
    fp = open("NetAppRootCA.pem", "w")
    fp.write(cert)
    fp.close()
    logging.info(filer_connection.client_command_execute(
        "sudo cp NetAppRootCA.pem /etc/pki/ca-trust/source/anchors/NetAppRootCA.pem"))
    logging.info(filer_connection.client_command_execute(
        "sudo ls  /etc/pki/ca-trust/source/anchors/"))
    logging.info(filer_connection.client_command_execute(
        "sudo update-ca-trust enable"))
    logging.info(filer_connection.client_command_execute(
        "sudo update-ca-trust extract"))


def main():
    test_client_execute("10.234.165.57")


if __name__ == "__main__":
    main()


