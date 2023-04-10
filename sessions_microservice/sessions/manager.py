from pathlib import Path
import shutil

from sessions.session import Session

SERVER_DIRECTORY = "../server"
INSTANCES_DIRECTORY = "../instances"
SERVER_RUN_COMMAND = "java -Xmx1024M -Xms1024M -jar server/server.jar nogui"  # temporary testing on mc server


class SessionsManager:
    def __init__(self):
        self.__instances = dict()

        server_path = Path(SERVER_DIRECTORY)
        if not server_path.exists():
            raise FileNotFoundError("No server directory found")

    def start_session(self) -> int:
        while True:
            session = Session()
            if session.id not in self.__instances.keys():
                break
            del session

        self.__instances[session.id] = session

        instance_path = Path(f"{INSTANCES_DIRECTORY}/{session.id}")
        shutil.copytree(SERVER_DIRECTORY, instance_path)

        session.start_instance(instance_path)

        return session.id

    def stop_session(self, id: int) -> bool:
        if id in self.__instances.keys():
            session = self.__instances.pop(id)
            session.kill()

            shutil.rmtree(f"{INSTANCES_DIRECTORY}/{session.id}")

            return True
        return False
