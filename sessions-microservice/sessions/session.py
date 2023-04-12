from subprocess import Popen, PIPE, STDOUT
from random import randint
from enum import Enum

from psutil import Process

SERVER_RUN_COMMAND = "VRExpPluginExampleServer.exe -log -port"


def process_kill(proc_pid: int):
    process = Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


class SessionStatus(Enum):
    killed = -1
    pending = 0
    running = 1


class Session:
    def __init__(self):
        self.id = randint(10000, 99999)
        self.status = SessionStatus.pending
        self.__server_process: Popen = None

    def start_instance(self, cwd: str) -> Popen:
        process = Popen(
            f"{SERVER_RUN_COMMAND}{self.id}",
            shell=True,
            cwd=cwd,
            stdout=PIPE,
            stderr=STDOUT
        )

        self.__server_process = process
        self.status = SessionStatus.running
        return process

    def kill(self):
        process_kill(self.__server_process.pid)
        self.status = SessionStatus.killed
