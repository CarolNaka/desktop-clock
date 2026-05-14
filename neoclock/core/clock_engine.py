from PySide6.QtCore import QObject, Signal, QTimer, Qt
from datetime import datetime

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

class ClockEngine(QObject):
    tick = Signal(str, str)  # (formatted_time, formatted_date)
    full_hour = Signal()

    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager

        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.PreciseTimer)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._emit)

    def start(self):
        self._emit()
        self._timer.start()

    def _emit(self):
        now = datetime.now()
        time = now.strftime(self._time_format())
        date = self._format_date(now)
        self.tick.emit(time, date)
        if now.minute == 0 and now.second == 0:
            self.full_hour.emit()

    def _time_format(self) -> str:
        is_12h = self.sm.get("format") == "12h"
        show_seconds = self.sm.get("show_seconds")

        if is_12h:
            return "%I:%M:%S %p" if show_seconds else "%I:%M %p"

        return "%H:%M:%S" if show_seconds else "%H:%M"

    def _format_date(self, now: datetime) -> str:
        weekday = WEEKDAYS[now.weekday()]
        month = MONTHS[now.month - 1]
        return f"{weekday}, {now.day} of {month}"