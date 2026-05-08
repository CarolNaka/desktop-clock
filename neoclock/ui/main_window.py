from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtCore import Qt

from ui.clock_widget import ClockWidget
from ui.settings_panel import SettingsPanel
from core.clock_engine import ClockEngine
from core.quote_engine import QuoteEngine


class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()

        self.sm = settings_manager

        self.setWindowTitle("MyClock")
        self.resize(700, 200)
        self.setMinimumSize(400, 120)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.panel = SettingsPanel(self.sm)
        self.clock = ClockWidget(self.sm)

        layout.addWidget(self.panel)
        layout.addWidget(self.clock, stretch=1)

        self.engine = ClockEngine(self.sm)

        self.engine.tick.connect(self.clock.update_clock)
        
        self.panel.config_changed.connect(self.clock.apply_style)
        self.panel.config_changed.connect(self._apply_background)

        self.engine.start()

        self._apply_background()
        self._load_quote()

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

            self.clock.set_quote("Error loading quote.")