"""Gestão centralizada de áudio: lo-fi, chuva e toque horário (sem sobrepor players do mesmo papel)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QObject, QTimer, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

SOUNDS_DIR = Path(__file__).parent.parent / "assets" / "sounds"

LOFI_FILE = "lo-fi-01.mp3"
RING_FILE = "ring-01.mp3"
RAIN_FILES = {"rain01": "rain-01.mp3", "rain02": "rain-02.mp3"}

LOFI_TARGET_VOL = 0.22
RAIN_TARGET_VOL = 0.30
RING_TARGET_VOL = 0.16

FADE_MS = 480
FADE_STEPS = 10


@dataclass
class _FadeState:
    timer: QTimer
    output: QAudioOutput


class AudioManager(QObject):
    """Três canais independentes (lo-fi, chuva, sino), um player por canal."""

    def __init__(self, settings_manager, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.sm = settings_manager
        self._user_interacted = False
        self._last_chime_key: Optional[tuple] = None
        self._fade_lofi: Optional[_FadeState] = None
        self._fade_rain: Optional[_FadeState] = None

        raw = str(self.sm.get("audio_rain") or "off")
        self._rain_mode: str = raw if raw in ("off", "rain01", "rain02") else "off"

        self._out_lofi = QAudioOutput(self)
        self._out_lofi.setVolume(0.0)
        self._player_lofi = QMediaPlayer(self)
        self._player_lofi.setAudioOutput(self._out_lofi)
        self._player_lofi.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / LOFI_FILE)))
        self._bind_loop(self._player_lofi)

        self._out_rain = QAudioOutput(self)
        self._out_rain.setVolume(0.0)
        self._player_rain = QMediaPlayer(self)
        self._player_rain.setAudioOutput(self._out_rain)
        self._bind_loop(self._player_rain)

        self._out_ring = QAudioOutput(self)
        self._out_ring.setVolume(self._out_hourly_target())
        self._player_ring = QMediaPlayer(self)
        self._player_ring.setAudioOutput(self._out_ring)
        self._player_ring.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / RING_FILE)))

        for pl, name in (
            (self._player_lofi, "lofi"),
            (self._player_rain, "rain"),
            (self._player_ring, "ring"),
        ):

            def make_cb(n: str):
                def _cb(*_args) -> None:
                    print(f"[AudioManager] {n} playback error")

                return _cb

            pl.errorOccurred.connect(make_cb(name))

    @staticmethod
    def _bind_loop(player: QMediaPlayer) -> None:
        def on_status(status: QMediaPlayer.MediaStatus) -> None:
            if status == QMediaPlayer.MediaStatus.EndOfMedia:
                player.setPosition(0)
                player.play()

        player.mediaStatusChanged.connect(on_status)

    def notify_user_interaction(self) -> None:
        if self._user_interacted:
            return
        self._user_interacted = True
        self.apply_from_settings()

    def apply_from_settings(self) -> None:
        self._apply_lofi()
        self._apply_rain(self.sm.get("audio_rain"))
        self._sync_playing_volumes()

    def _lvl(self, key: str, default: float = 0.75) -> float:
        try:
            v = float(self.sm.get(key, default))
        except (TypeError, ValueError):
            v = default
        return max(0.0, min(1.0, v))

    def _out_lofi_target(self) -> float:
        return max(0.0, min(1.0, LOFI_TARGET_VOL * self._lvl("audio_lofi_volume")))

    def _out_rain_target(self) -> float:
        return max(0.0, min(1.0, RAIN_TARGET_VOL * self._lvl("audio_rain_volume")))

    def _out_hourly_target(self) -> float:
        return max(0.0, min(1.0, RING_TARGET_VOL * self._lvl("audio_hourly_volume")))

    def _sync_playing_volumes(self) -> None:
        if self._fade_lofi is None and (
            self._player_lofi.playbackState()
            == QMediaPlayer.PlaybackState.PlayingState
        ):
            self._out_lofi.setVolume(self._out_lofi_target())
        if self._fade_rain is None and self._rain_playing():
            self._out_rain.setVolume(self._out_rain_target())
        self._out_ring.setVolume(self._out_hourly_target())

    def on_full_hour(self) -> None:
        if not self.sm.get("audio_hourly_on"):
            return
        from datetime import datetime

        now = datetime.now()
        key = (now.year, now.month, now.day, now.hour)
        if key == self._last_chime_key:
            return
        self._last_chime_key = key
        self._out_ring.setVolume(self._out_hourly_target())
        self._player_ring.setPosition(0)
        self._player_ring.play()

    def _rain_playing(self) -> bool:
        return (
            self._player_rain.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        )

    def _cancel_fade(self, which: str) -> None:
        attr = f"_fade_{which}"
        st: Optional[_FadeState] = getattr(self, attr)
        if st is not None:
            st.timer.stop()
            st.timer.deleteLater()
            setattr(self, attr, None)

    def _linear_fade(
        self,
        which: str,
        out: QAudioOutput,
        v_start: float,
        v_end: float,
        on_complete: Optional[Callable[[], None]] = None,
    ) -> None:
        self._cancel_fade(which)
        steps = FADE_STEPS
        interval = max(20, FADE_MS // steps)
        timer = QTimer(self)
        state = {"i": 0}

        def tick() -> None:
            state["i"] += 1
            t = min(1.0, state["i"] / steps)
            out.setVolume(v_start + (v_end - v_start) * t)
            if state["i"] >= steps:
                timer.stop()
                timer.deleteLater()
                out.setVolume(v_end)
                setattr(self, f"_fade_{which}", None)
                if on_complete:
                    on_complete()

        timer.timeout.connect(tick)
        setattr(self, f"_fade_{which}", _FadeState(timer=timer, output=out))
        timer.start(interval)

    def _apply_lofi(self) -> None:
        want = bool(self.sm.get("audio_lofi_on"))
        playing = (
            self._player_lofi.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        )
        if want and self._user_interacted:
            if not playing:
                self._out_lofi.setVolume(0.0)
                self._player_lofi.setPosition(0)
                self._player_lofi.play()
                self._linear_fade("lofi", self._out_lofi, 0.0, self._out_lofi_target())
        else:
            if playing or self._out_lofi.volume() > 0.01:

                def after_fade() -> None:
                    self._player_lofi.pause()
                    self._player_lofi.setPosition(0)

                self._linear_fade(
                    "lofi",
                    self._out_lofi,
                    self._out_lofi.volume(),
                    0.0,
                    after_fade,
                )
            else:
                self._player_lofi.pause()
                self._out_lofi.setVolume(0.0)

    def _apply_rain(self, mode: object) -> None:
        m = str(mode or "off")
        if m not in ("off", "rain01", "rain02"):
            m = "off"

        if m == "off":
            if not self._rain_playing() and self._out_rain.volume() < 0.02:
                self._rain_mode = "off"
                return

            def after_rain_fade() -> None:
                self._player_rain.pause()
                self._player_rain.setPosition(0)
                self._rain_mode = "off"

            self._linear_fade(
                "rain",
                self._out_rain,
                self._out_rain.volume(),
                0.0,
                after_rain_fade,
            )
            return

        if self._rain_mode == m and self._rain_playing():
            return

        def start_rain() -> None:
            fname = RAIN_FILES[m]
            self._player_rain.setSource(QUrl.fromLocalFile(str(SOUNDS_DIR / fname)))
            self._out_rain.setVolume(0.0)
            self._player_rain.setPosition(0)
            self._player_rain.play()
            self._linear_fade("rain", self._out_rain, 0.0, self._out_rain_target())
            self._rain_mode = m

        if self._rain_playing() or self._out_rain.volume() > 0.02:

            def after_out() -> None:
                self._player_rain.pause()
                self._player_rain.setPosition(0)
                start_rain()

            self._linear_fade(
                "rain",
                self._out_rain,
                self._out_rain.volume(),
                0.0,
                after_out,
            )
        else:
            start_rain()
