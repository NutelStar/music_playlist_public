import random
import threading
import time
from pathlib import Path

import keyboard
import pygame
import sounddevice as sd

from .config.config import (
    MUSIC_CATEGORIES,
    MUSIC_FOLDER,
    MUSIC_TEXT_WAIT,
)
from .music_player import MusicPlayer
from .packages.obs.obs_websockets import OBSWebsocketsManager
from .window import MusicWindow


class MusicPlaylistApp:
    """
    Class to manage the application.
    """

    def __init__(self, show_obs_text: bool = False) -> None:
        self.show_obs_text = show_obs_text
        self.player: MusicPlayer | None = None
        self.window: MusicWindow | None = None
        self.obs_manager: OBSWebsocketsManager | None = None
        self.current_category: str | None = None
        self.loading = False
        self.last_trigger_time = 0.0
        self._lock = threading.Lock()
        self._obs_generation = 0

    def run(self) -> None:
        pygame.mixer.init()
        self.player = MusicPlayer(sd.default.device[1])
        if self.show_obs_text:
            self.obs_manager = OBSWebsocketsManager()

        self.window = MusicWindow(self._set_volume, self.play_category, self._stop_playback)
        for shortcut, category in MUSIC_CATEGORIES.items():
            keyboard.add_hotkey(shortcut, self.play_category, args=(category,))
            print(f"Press {shortcut} to play a song from '{category}'")

        try:
            self.window.run()
        finally:
            keyboard.unhook_all_hotkeys()
            self.player.stop()
            if self.obs_manager is not None:
                self.obs_manager.disconnect()

    def _set_volume(self, volume: float) -> None:
        self.player.volume = max(0.0, min(1.0, volume))

    def _prevent_spam_crash(self):
        """
        Prevent crashes due to spam
        """
        now = time.time()
        if now - self.last_trigger_time < 0.5 or self.loading:
            return False
        self.last_trigger_time = now
        return True

    def play_category(self, category: str, song_path: Path | None = None) -> None:
        with self._lock:
            if not self._prevent_spam_crash():
                return

            if song_path is None:
                if self.current_category == category:
                    self._stop_playback()
                    print(f"Stopped: {category}")
                    return

                songs_folder = MUSIC_FOLDER / category
                if not songs_folder.is_dir():
                    self.window.set_status(f"Folder not found: {songs_folder}")
                    print(f"Music folder not found: {songs_folder}")
                    return

                songs = [
                    path
                    for path in songs_folder.iterdir()
                    if path.is_file() and path.suffix.lower() in {".mp3", ".wav"}
                ]
                if not songs:
                    print(f"No songs found in {songs_folder}")
                    return

                song = random.choice(songs)
            else:
                song = song_path

            self.loading = True
            self._obs_generation += 1
            obs_generation = self._obs_generation
            try:
                self.player.play(song)
                self.current_category = category
            finally:
                self.loading = False

        self.window.set_status(f"Playing: {song.stem}")
        print(f"Now playing: {song.stem} from {category}")
        if self.show_obs_text:
            threading.Thread(
                target=self._show_obs_song,
                args=(song, obs_generation),
                daemon=True,
            ).start()

    def _stop_playback(self) -> None:
        self.player.stop()
        self.current_category = None
        self._obs_generation += 1

    def _show_obs_song(self, song: Path, generation: int) -> None:
        manager = self.obs_manager
        if manager is None:
            return
        
        time.sleep(0.5)
        if generation != self._obs_generation:
            return
        
        manager.set_text("Music Text", f"Music: {song.stem}")
        scene = manager.get_scene()
        manager.set_filter_visibility(scene, "Move Music Show", True)
        started_at = time.time()
        while (
            time.time() - started_at <= MUSIC_TEXT_WAIT
            and generation == self._obs_generation
        ):
            time.sleep(0.1)

        scene = manager.get_scene()
        manager.set_filter_visibility(scene, "Move Music Hide", True)