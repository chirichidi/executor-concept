# set path
import os
import sys

src_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir))
sys.path.append(src_path)

dir_list = os.listdir(src_path)
for item in dir_list:
    path = src_path + "/" + item
    if not os.path.isdir(path):
        continue
    if item.startswith("."):
        continue
    if path in sys.path:
        continue
    sys.path.append(item)


from executor.task.interface import Task

import subprocess


class PullRepoTask(Task):
    start_date: int = 0
    end_date: int = 0
    # TODO variables..

    def __init__(self) -> None:
        import paramiko
        import select

        key_file = "/home/root/.ssh/123.pem"

        k = paramiko.RSAKey.from_private_key_file(key_file)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="", username="ec2-user", pkey=k)

        start_date = "2023-03-06"
        end_date = "2023-03-07"

        command = f"/usr/local/bin/python3.10 /tmp/main.py ---start_date={start_date} --end_date={end_date}"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)

        exit_code = ssh_stdout.channel.recv_exit_status()  # handles async exit error
        for line in ssh_stdout:
            print(line.strip())

        ssh.close()

        pass

    def execute(self):
        pass

    def deserialize(self, data):
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]


if __name__ == "__main__":
    a = PullRepoTask()
    a.execute()
