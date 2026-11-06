# Music Playlist

A small Windows desktop music player for livestreams. It plays a random, looping
track from a category folder when its global keyboard shortcut is pressed, and
provides a volume slider. Optionally, it can show the playing track in OBS
through OBS WebSocket.

## Requirements

- Windows
- Python 3.12.6
- [uv](https://docs.astral.sh/uv/)
- An audio output device
- OBS Studio with its WebSocket server enabled (optional; required only with
  `--obs-text`)

## Setup

1. Clone or download this project and open a terminal in its root directory.
2. Create the environment and install dependencies:

   ```powershell
   uv sync
   ```

3. Arrange audio files (`.mp3` and `.wav`) in one folder per category. By
   default, the application expects this layout under
   `~/Music/Musics`:

   ```text
   Youtube Music/
   ├── Action/
   ├── Chill/
   ├── Epic/
   ├── Ending/
   ├── Funny/
   ├── Hope/
   ├── Infiltration/
   ├── Normal/
   ├── Sad/
   ├── Starting/
   └── Thinking/
   ```

   Set `MUSIC_FOLDER` to the parent directory if your music is stored
   elsewhere. The category folders must use the names shown above.

   All the configurations are located in `src/music_playlist/config/config.py`.
   Make sure to set the different variables according to your current structure and needs.

## Running

From the project root:

```powershell
uv run python src\main.py
```

On Windows, `run.bat` provides the same launch command. Press the category
shortcut shown in the console to start a random track. Press the same shortcut
again to stop it. Adjust playback volume with the slider in the window. The
global hotkeys are:

| Shortcut | Category |
| --- | --- |
| `Ctrl+Shift+Alt+1` | Action |
| `Ctrl+Shift+Alt+2` | Chill |
| `Ctrl+Shift+Alt+3` | Epic |
| `Ctrl+Shift+Alt+4` | Sad |
| `Ctrl+Shift+Alt+5` | Normal |
| `Ctrl+Shift+Alt+6` | Thinking |
| `Ctrl+Shift+Alt+7` | Funny |
| `Ctrl+Shift+Alt+8` | Ending |
| `Ctrl+Shift+Alt+9` | Starting |
| `Ctrl+Shift+Alt+0` | Infiltration |
| `Ctrl+Shift+Alt+H` | Hope |

All the shortcut keys can be modified depending on the structure of your music folders
in `src/music_playlist/config/config.py`.

`MUSIC_FOLDER` and the OBS connection values are read from process environment
variables at startup.

## (optional) OBS

It is not required to setup OBS as long as you do not use the argument to activate
OBS websocket.

To enable the OBS track title overlay, first enable the WebSocket server in
OBS's **Tools → WebSocket Server Settings**. Then set the connection environment
variables and start with the option:

```powershell
$env:OBS_WEBSOCKET_HOST = "localhost"
$env:OBS_WEBSOCKET_PORT = "4455"
$env:OBS_WEBSOCKET_PASSWORD = "your websocket password"
uv run python src\main.py --obs-text
```

The OBS scene must have a text input named `Music Text` and filters named
`Move Music Show` and `Move Music Hide` on the active scene's source. The
overlay displays each track for five seconds. The host and port default to
`localhost` and `4455`; set the password only when OBS requires one. Keep the
password private and do not commit it to the repository.

## Project layout

```text
src/
|-- main.py
`-- music_playlist/
    |-- app.py
    |-- config/
    |   `-- config.py          # Environment variables and category settings
    |-- music_player.py        # Audio playback and looping
    |-- window.py              # Tkinter volume and status window
    `-- packages/
        |-- audio/
        |   `-- audio_player.py
        `-- obs/
            `-- obs_websockets.py
```

## Troubleshooting

- **No tracks play:** check that `MUSIC_FOLDER` points to the parent of the
  category folders and that a category contains `.mp3` or `.wav` files.
- **No global hotkeys:** ensure the app is running and that another application
  is not intercepting the same shortcuts. Windows may require elevated
  permissions for global keyboard hooks in some environments.
- **OBS connection fails:** verify OBS is running, its WebSocket server is
  enabled, and the configured host, port, and password match.
- **No sound or wrong output:** check the Windows default output device before
  launching; playback uses the default output device.
