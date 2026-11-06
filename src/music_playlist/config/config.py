import os
from pathlib import Path

MUSIC_FOLDER = Path(
    os.getenv("MUSIC_FOLDER", str(Path.home() / "Music" / "Musics"))
).expanduser()

OBS_WEBSOCKET_HOST = os.getenv("OBS_WEBSOCKET_HOST", "localhost")
OBS_WEBSOCKET_PORT = int(os.getenv("OBS_WEBSOCKET_PORT", "4455"))
OBS_WEBSOCKET_PASSWORD = os.getenv("OBS_WEBSOCKET_PASSWORD")

MUSIC_CATEGORIES = {
    "ctrl+shift+alt+1": "Action",
    "ctrl+shift+alt+2": "Chill",
    "ctrl+shift+alt+3": "Epic",
    "ctrl+shift+alt+4": "Sad",
    "ctrl+shift+alt+5": "Normal",
    "ctrl+shift+alt+6": "Thinking",
    "ctrl+shift+alt+7": "Funny",
    "ctrl+shift+alt+8": "Ending",
    "ctrl+shift+alt+9": "Starting",
    "ctrl+shift+alt+0": "Infiltration",
    "ctrl+shift+alt+h": "Hope",
}

OBS_SCENES = [
    "Starting Screen",
    "Live",
    "Just Chatting Screen",
    "Be Right Back Screen",
    "Live Block View",
]
MUSIC_TEXT_WAIT = 5