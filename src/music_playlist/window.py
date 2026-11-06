import tkinter as tk
from collections.abc import Callable
from pathlib import Path

from .config.config import (
    MUSIC_CATEGORIES,
    MUSIC_FOLDER
)


class MusicWindow:
    """
    Class to generate and manage TKinter window.
    """

    def __init__(self, on_volume_change: Callable[[float], None], on_song_select: Callable[[str, Path], None], on_stop_button:  Callable[[], None]) -> None:
        self.win = tk.Tk()
        self.win.title("Music Player")
        self.win.geometry("640x360")
        self.win.resizable(False, False)
        self.on_volume_change = on_volume_change
        self.on_song_select = on_song_select
        self.on_stop_button = on_stop_button
        self._selected_category = ""
        self._song_paths: list[Path] = []

        controls_frame = tk.Frame(self.win)
        controls_frame.pack(pady=20, padx=10, fill=tk.BOTH)

        self._generate_volume_slider(controls_frame)
        self._generate_categories_lists(controls_frame)
        self._generate_songs_lists(controls_frame)
        self._generate_buttons()

        self.hint_label = tk.Label(self.win, text="Use hotkeys or the list to play songs from categories")
        self.hint_label.pack(pady=10)

    def _generate_categories_lists(self, frame: tk.Frame):
        categories = MUSIC_CATEGORIES.values()
        cat_list = tk.Listbox(frame, width=20, height=len(categories))

        for category in categories:
            cat_list.insert(tk.END, category)

        cat_list.pack(side=tk.LEFT, pady=(10, 0), padx=(5,0))

        cat_list.bind("<<ListboxSelect>>", self._on_categorylist_select)

        self._categories_list = cat_list

    def _generate_songs_lists(self, frame: tk.Frame):
        songs_list = tk.Listbox(frame, width=100, height=len(MUSIC_CATEGORIES))

        songs_list.pack(side=tk.LEFT, pady=(10, 0), padx=(5,0))
        songs_list.bind("<<ListboxSelect>>", self._on_songlist_select)

        self._songs_list = songs_list

    def _generate_volume_slider(self, frame: tk.Frame):
        self.volume_label = tk.Label(frame, text="Volume: 50%", width=14)
        self.volume_label.pack(pady=(0, 10))

        self.volume_slider = tk.Scale(
            frame,
            from_=0,
            to=100,
            orient="horizontal",
            length=260,
            command=self._set_volume,
            showvalue=False,
        )
        self.volume_slider.set(50)
        self.volume_slider.pack()

    def _generate_buttons(self):
        self.stop_button = tk.Button(self.win, text="Stop", command=self._on_stop_button_pressed)
        self.stop_button.pack()

    def _on_stop_button_pressed(self):
        self.on_stop_button()
        self.set_status("Use hotkeys or the list to play songs from categories")

    def _on_categorylist_select(self, event):
        widget = event.widget
        selection = widget.curselection()

        if selection:
            category = widget.get(selection[0])
            self._selected_category = category
            self._songs_list.delete(0, tk.END)
            self._song_paths = []
            song_folder_path = MUSIC_FOLDER / category

            for song in song_folder_path.iterdir():
                if song.is_file() and song.suffix.lower() in {".mp3", ".wav"}:
                    self._song_paths.append(song)
                    self._songs_list.insert(tk.END, song.stem)

    def _on_songlist_select(self, event):
        widget = event.widget
        selection = widget.curselection()

        if selection and self._selected_category:
            song_path = self._song_paths[selection[0]]
            self.on_song_select(self._selected_category, song_path)

    def _set_volume(self, value: str) -> None:
        percentage = int(float(value))
        self.volume_label.config(text=f"Volume: {percentage}%")
        self.on_volume_change(percentage / 100)

    def set_status(self, text: str) -> None:
        self.hint_label.config(text=text)

    def run(self) -> None:
        self.win.mainloop()
