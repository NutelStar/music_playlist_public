import threading
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf

class MusicPlayer:
    """
    Play and loop an audio file through the selected output device.
    """

    def __init__(self, output_device_index: int | None) -> None:
        self.output_device_index = output_device_index
        self._volume = 0.5
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def play(self, file_path: Path) -> None:
        self.stop()

        if self._thread is not None and self._thread.is_alive():
            raise TimeoutError("The previous audio stream did not stop in time.")
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._play_loop, args=(file_path,), daemon=True
        )

        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=5)

    def _play_loop(self, file_path: Path) -> None:
        data, sample_rate = sf.read(file_path, dtype="float32")
        if data.size == 0:
            raise ValueError(f"Audio file is empty: {file_path}")
        data = np.clip(data, -1.0, 1.0)
        if data.ndim == 1:
            data = data[:, np.newaxis]
        channels = data.shape[1]
        position = 0

        def callback(outdata, frames, _time, status):
            nonlocal position

            indices = (np.arange(frames) + position) % len(data)
            outdata[:] = data[indices] * self._volume
            position = (position + frames) % len(data)

            if self._stop_event.is_set():
                raise sd.CallbackStop()

        with sd.OutputStream(
            callback=callback,
            samplerate=sample_rate,
            channels=channels,
            device=self.output_device_index,
        ):
            while not self._stop_event.is_set():
                time.sleep(0.1)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, vol: int):
        self._volume = vol
