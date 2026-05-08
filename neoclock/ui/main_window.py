from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from ui.clock_widget import ClockWidget
from ui.settings_panel import SettingsPanel
from core.clock_engine import ClockEngine
from core.quote_engine import QuoteEngine          # novo

class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager
        self.setWindowTitle("NéoClock")
        self.resize(700, 200)
        self.setMinimumSize(400, 120)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.painel = SettingsPanel(self.sm)
        self.relogio = ClockWidget(self.sm)

        layout.addWidget(self.painel)
        layout.addWidget(self.relogio, stretch=1)

        self.engine = ClockEngine(self.sm)
        self.engine.tick.connect(self.relogio.atualizar)
        self.painel.config_alterada.connect(self.relogio.aplicar_estilo)

        self.engine.iniciar()
        self._aplicar_fundo()
        self._carregar_frase()                     # novo

    def _aplicar_fundo(self):
        self.setStyleSheet(f"background-color: {self.sm.get('cor_fundo')};")

    def _carregar_frase(self):                     # novo
        try:
            qe = QuoteEngine(self.sm)
            frase = qe.obter_frase()
            self.relogio.definir_frase(frase)
        except Exception as e:
            print("[MainWindow] Erro ao carregar frase:", e)
            self.relogio.definir_frase("Erro ao carregar frase.")