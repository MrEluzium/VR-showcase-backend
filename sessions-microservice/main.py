from fastapi import FastAPI, HTTPException

from sessions.manager import SessionsManager

session_manager = SessionsManager()

app = FastAPI()


@app.get("/session/new", status_code=201)
async def create_session():
    return session_manager.start_session()


@app.delete("/session/{id}/stop")
async def stop_session(id: int):
    if not session_manager.stop_session(id):
        raise HTTPException(status_code=404, detail="Item not found")
    return

@app.get("/session/all")
async def get_sessions_list():
    return session_manager.sessions_list()