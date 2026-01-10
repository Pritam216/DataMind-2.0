SESSION_STORE = {}

def set_session(session_id: str, run_id: str):
    SESSION_STORE[session_id] = run_id

def get_run_id(session_id: str):
    return SESSION_STORE.get(session_id)
