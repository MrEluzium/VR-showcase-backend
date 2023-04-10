from subprocess import Popen, PIPE, STDOUT
from random import randint
from enum import Enum

SERVER_RUN_COMMAND = "java -Xmx1024M -Xms1024M -jar /Users/elzzz/Documents/server/server.jar nogui"


class SessionStatus(Enum):
    killed = -1
    pending = 0
    running = 1


class Session:
    def __init__(self):
        self.id = randint(100000, 999999)
        self.status = SessionStatus.pending
        self.__server_process: Popen = None

    def start_instance(self, cwd: str) -> Popen:
        process = Popen(
            SERVER_RUN_COMMAND,
            shell=True,
            cwd=cwd,
            stdout=PIPE,
            stderr=STDOUT
        )

        self.__server_process = process
        self.status = SessionStatus.running
        return process

    def kill(self):
        self.__server_process.kill()
        self.status = SessionStatus.killed
