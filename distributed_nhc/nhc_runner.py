
from enum import Enum
from distributed_nhc.ssh_client import SSHClient


class NHCStates(Enum):
    FAILED = -1
    NEW = 0
    RETRIEVING = 10
    RETRIEVED = 11
    INSTALLING = 20
    INSTALLED = 21
    RUNNING = 30
    FINISHED = 100


class NHCRunner():
    def __init__(self, hostname):
        self.version = "main"
        self._working_dir = "~/distributed_nhc"
        self._fetch_az_nhc_script = "./scripts/fetch_az_nhc.sh"
        self._install_nhc_script = "./scripts/install_nhc.sh"
        self._run_nhc_script = "./scripts/run_health_checks.sh"

        self.ssh_client = SSHClient(hostname)
        self.state = NHCStates.NEW

    def execute_next(self):
        if self.state == NHCStates.NEW:
            self._download_az_nhc()
        if self.state == NHCStates.RETRIEVED:
            self._setup_nhc()
        if self.state == NHCStates.INSTALLED:
            self._run_nhc()
        else:
            return NHCStates.FINISHED

    def _download_az_nhc(self):
        self.state = NHCStates.RETRIEVING
        print("Downloading AZ NHC")
        (stdout, stderr) = self.ssh_client.execute_script(self._fetch_az_nhc_script, self.version, self._working_dir)
        print(stdout)
        print("Finished downloading AZ NHC")
        self.state = NHCStates.RETRIEVED
    
    def _setup_nhc(self):
        self.state = NHCStates.INSTALLING
        print("Installing NHC")
        (stdout, stderr) = self.ssh_client.execute_script(self._install_nhc_script, self.version, self._working_dir)
        print(stdout)
        print("Finished installing NHC")
        self.state = NHCStates.INSTALLED
    
    def _run_nhc(self):
        self.state = NHCStates.RUNNING
        print("Running NHC")
        (stdout, stderr) = self.ssh_client.execute_script(self._run_nhc_script, self.version, self._working_dir)
        print(stdout)
        print("Finished installing NHC")
        self.state = NHCStates.FINISHED
