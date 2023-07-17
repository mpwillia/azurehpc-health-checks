import logging
import os
import subprocess
from subprocess import CalledProcessError
from shutil import which
from typing import Tuple
from distributed_nhc import APP_ROOT_DIR

class SSHClient():
    @staticmethod
    def is_ssh_available():
        return which("ssh") is not None

    @staticmethod
    def require_ssh():
        if not SSHClient.is_ssh_available():
            logging.error("SSH is not available on this device, cannot execute an ssh command")
            raise FileNotFoundError("No SSH client found on device, cannot execute an ssh command")
    
    @staticmethod
    def is_scp_available():
        return which("scp") is not None
    
    @staticmethod
    def require_scp():
        if not SSHClient.is_ssh_available():
            logging.error("SSH is not available on this device, cannot execute an ssh command")
            raise FileNotFoundError("No SSH client found on device, cannot execute an ssh command")

    def __init__(self, hostname):
        self._ssh_base_args = [
            "ssh",
            "-T",
            "-o", "StrictHostKeyChecking=no",
            hostname]

    def execute(self, command : str, *args) -> Tuple[str, str]:
        """
        Executes a given command. The command will be passed verbatim to ssh and can support newlines.

        :param command: The command to run on the remote machine. It is passed verbatim to ssh. It can support newlines which allows for full scripts to run as well
        :param args: Arguments to pass to the command. *args will be expanded as a list. The first argument will be assigned to $1, the second to $2, and so on. 
        This allows commands or scripts to support handling typical positional parameters. This is done by using the 'set' builtin prior to executing the given command.
        All arguments will be ran through str(arg) to convert them to strings.
        :returns: A tuple (stdout, stderr) containing the raw standard out and standard error produced by executing the given script
        """
        SSHClient.require_ssh()

        if len(args) > 0:
            args_def = f"set {' '.join((str(arg) for arg in args))};"
            command = args_def + command

        try:
            ssh_proc = subprocess.run(
                self._ssh_base_args + [command],
                capture_output=True,
                check=True,
                universal_newlines=True
            )
            return ssh_proc.stdout, ssh_proc.stderr
        except CalledProcessError as ex:
            logging.exception("SSH command failed due to an exception")
            logging.error(f"Dumping failed command's stdout:\n{ex.stdout}")
            logging.error(f"Dumping failed command's stderr:\n{ex.stderr}")
            raise

    def execute_script(self, script_rel_file_path : str, *args) -> Tuple[str, str]:
        script_abs_file_path = os.path.join(APP_ROOT_DIR, script_rel_file_path)
        with open(script_abs_file_path, 'r') as f:
            script_content = ''.join(f.readlines())
            return self.execute(script_content, *args)

_ssh_clients = {} # { hostname : sshclient instance}
def get_client(hostname) -> SSHClient:
    if hostname not in _ssh_clients:
        _ssh_clients[hostname] = SSHClient(hostname)
    return _ssh_clients[hostname]
