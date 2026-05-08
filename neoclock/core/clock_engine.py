from PySide6.QtCore import QObject, Signal, QTimer, Qt
from datetime import datetime

class ClockEngine(QObject):
    tick = Signal(str)  # emite a string formatada do horário

    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager

        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.PreciseTimer)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._emitir_hora)

    def iniciar(self):
        self._emitir_hora()  # dispara imediatamente ao iniciar
        self._timer.start()

    def _emitir_hora(self):
        agora = datetime.now()
        fmt = self._formato()
        self.tick.emit(agora.strftime(fmt))

    def _formato(self) -> str:
        is_12h = self.sm.get("formato") == "12h"
        com_seg = self.sm.get("mostrar_segundos")

        if is_12h:
            return "%I:%M:%S %p" if com_seg else "%I:%M %p"
        else:
            return "%H:%M:%S" if com_seg else "%H:%M"