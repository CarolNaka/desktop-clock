from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QRect

from ui.clock_widget import ClockWidget
from ui.settings_panel import SettingsPanel
from core.clock_engine import ClockEngine
from core.quote_engine import QuoteEngine

PANEL_WIDTH = 200


class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager

        self.setWindowTitle("MyClock")
        self.resize(700, 220)
        self.setMinimumSize(400, 160)

        # Container central
        self.central = QWidget()
        self.setCentralWidget(self.central)

        # Relógio ocupa tudo
        self.clock = ClockWidget(self.sm)
        layout = QHBoxLayout(self.central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.clock)

        # Painel flutua sobre o central como filho direto
        self.panel = SettingsPanel(self.sm, parent=self.central)
        self.panel.setGeometry(-PANEL_WIDTH, 0, PANEL_WIDTH, self.height())
        self.panel.raise_()  # garante que fica na frente

        # Conexões
        self.engine = ClockEngine(self.sm)
        self.engine.tick.connect(self.clock.update_clock)
        self.panel.config_changed.connect(self.clock.apply_style)
        self.panel.config_changed.connect(self._apply_background)

        self.engine.start()
        self._apply_background()
        self._load_quote()

        # Mouse tracking
        self.setMouseTracking(True)
        self.central.setMouseTracking(True)
        self.clock.setMouseTracking(True)

    def _apply_background(self):
        self.setStyleSheet(
            f"background-color: {self.sm.get('background_color')};"
        )

    def _load_quote(self):
        try:
            qe = QuoteEngine(self.sm)
            quote = qe.get_quote()
            self.clock.set_quote(quote)
        except Exception as e:
            print("[MainWindow] Error loading quote:", e)
            self.clock.set_quote("")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        h = self.central.height()
        # Atualiza altura do painel ao redimensionar
        geo = self.panel.geometry()
        self.panel.setGeometry(geo.x(), 0, PANEL_WIDTH, h)

    def mouseMoveEvent(self, event):
        x = event.position().x()
        if x < 60:
            self.panel.slide_in()
        elif x > PANEL_WIDTH + 20:
            self.panel.slide_out()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.panel.slide_out()
        super().leaveEvent(event)