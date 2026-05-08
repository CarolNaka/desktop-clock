from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from ui.clock_widget import ClockWidget
from ui.settings_panel import SettingsPanel
from core.clock_engine import ClockEngine

class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager
        self.setWindowTitle("NéoClock")
        self.resize(700, 200)
        self.setMinimumSize(400, 120)

        # Layout principal
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Painel e relógio
        self.painel = SettingsPanel(self.sm)
        self.relogio = ClockWidget(self.sm)

        layout.addWidget(self.painel)
        layout.addWidget(self.relogio, stretch=1)

        # Engine conectada ao widget via signal
        self.engine = ClockEngine(self.sm)
        self.engine.tick.connect(self.relogio.atualizar_hora)
        self.painel.config_alterada.connect(self.relogio.aplicar_estilo)

        self.engine.iniciar()
        self._aplicar_fundo()

    def _aplicar_fundo(self):
        self.setStyleSheet(f"background-color: {self.sm.get('cor_fundo')};")