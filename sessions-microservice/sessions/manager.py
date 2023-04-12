from pathlib import Path
import shutil

from sessions.session import Session

SERVER_DIRECTORY = "server"


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
        session.start_instance(SERVER_DIRECTORY)

        return session.id

    def stop_session(self, id: int) -> bool:
        if id in self.__instances.keys():
            session = self.__instances.pop(id)
            session.kill()
            return True
        return False

    def get_session_by_id(self, id: int) -> Session | None:
        return self.__instances.get(id)

    def sessions_list(self):
        return list(self.__instances.keys())
