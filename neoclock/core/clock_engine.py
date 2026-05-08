from PySide6.QtCore import QObject, Signal, QTimer, Qt
from datetime import datetime

DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

class ClockEngine(QObject):
    tick = Signal(str, str)  # (hora_formatada, data_formatada)

    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager

        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.PreciseTimer)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._emitir)

    def iniciar(self):
        self._emitir()
        self._timer.start()

    def _emitir(self):
        agora = datetime.now()
        hora = agora.strftime(self._formato_hora())
        data = self._formatar_data(agora)
        self.tick.emit(hora, data)

    def _formato_hora(self) -> str:
        is_12h = self.sm.get("formato") == "12h"
        com_seg = self.sm.get("mostrar_segundos")
        if is_12h:
            return "%I:%M:%S %p" if com_seg else "%I:%M %p"
        return "%H:%M:%S" if com_seg else "%H:%M"

    def _formatar_data(self, agora: datetime) -> str:
        dia_semana = DIAS_SEMANA[agora.weekday()]
        mes = MESES[agora.month - 1]
        return f"{dia_semana}, {agora.day} de {mes}"