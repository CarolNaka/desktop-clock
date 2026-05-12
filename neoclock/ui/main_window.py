from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

from ui.clock_widget import ClockWidget
from ui.settings_panel import SettingsPanel, PANEL_WIDTH
from core.clock_engine import ClockEngine
from core.quote_engine import QuoteEngine


class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager

        self.setWindowTitle("MyClock")
        self.resize(700, 220)
        self.setMinimumSize(400, 160)

        # Container central — fundo alinhado ao tema (o relógio expande e cobre tudo)
        self.central = QWidget()
        self.central.setObjectName("centralArea")
        self.central.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(self.central)

        self.clock = ClockWidget(self.sm)
        layout = QHBoxLayout(self.central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.clock, 1)

        # Painel flutua sobre o central como filho direto
        self.panel = SettingsPanel(self.sm, parent=self.central)
        self.panel.setGeometry(-PANEL_WIDTH, 0, PANEL_WIDTH, self.height())
        self.panel.raise_()  # garante que fica na frente

        # Conexões
        self.engine = ClockEngine(self.sm)
        self.engine.tick.connect(self.clock.update_clock)
        self.panel.config_changed.connect(self.clock.apply_style)
        self.panel.config_changed.connect(self._sync_chrome_background)

        self.engine.start()
        self._sync_chrome_background()
        self._load_quote()

        # Mouse tracking
        self.setMouseTracking(True)
        self.central.setMouseTracking(True)
        self.clock.setMouseTracking(True)

    def _sync_chrome_background(self):
        bg = self.sm.get("background_color")
        self.central.setStyleSheet(f"#centralArea {{ background-color: {bg}; }}")
        self.setStyleSheet(f"QMainWindow {{ background-color: {bg}; }}")

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
        if x < 76:
            self.panel.slide_in()
        elif x > PANEL_WIDTH + 36:
            self.panel.slide_out()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.panel.slide_out()
        super().leaveEvent(event)