import os
import argparse
from distributed_nhc.nhc_runner import NHCRunner, NHCStates

def file_path(filepath):
    if os.path.isfile(filepath):
        return filepath
    raise FileNotFoundError(filepath)



def invoke_on_host(hostname):
    runner = NHCRunner(hostname)

    while runner.execute_next() != NHCStates.FINISHED:
        pass
    print("Finished")

    # prepare contents
    # deploy to host
    # install-nhc
    # start-nhc as background process
    # check periodically

parser = argparse.ArgumentParser("Run NHC distributed to multiple nodes, aggregating the results together")
parser.add_argument("--hostsfile", type=file_path, help="Host names to run distributed-nhc on.", required=True)

args = parser.parse_args()

with open(args.hostsfile, encoding="utf-8") as f:
    hostnames = f.readlines()
    for hostname in hostnames:
        invoke_on_host(hostname)