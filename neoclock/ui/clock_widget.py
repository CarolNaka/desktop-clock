from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt


class ClockWidget(QWidget):
    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager
        self.setObjectName("clockRoot")
        # Garante que o fundo do stylesheet é realmente pintado (evita “buracos” cinzentos).
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
        layout.setContentsMargins(24, 24, 24, 24)

        self.label_time = QLabel()
        self.label_time.setAlignment(Qt.AlignCenter)

        self.label_date = QLabel()
        self.label_date.setAlignment(Qt.AlignCenter)

        self.label_quote = QLabel()
        self.label_quote.setAlignment(Qt.AlignCenter)
        self.label_quote.setWordWrap(True)

        layout.addWidget(self.label_time)
        layout.addWidget(self.label_date)
        layout.addWidget(self.label_quote)

        self.apply_style()

    def apply_style(self):
        text_color = self.sm.get("text_color")
        background_color = self.sm.get("background_color")
        font = self.sm.get("font")
        size = self.sm.get("font_size")

        date_size = max(12, size // 4)
        quote_size = max(11, size // 5)

        self.setStyleSheet(f"#clockRoot {{ background-color: {background_color}; }}")

        self.label_time.setStyleSheet(f"""
            QLabel {{
                font-family: {font};
                font-size: {size}px;
                font-weight: bold;
                color: {text_color};
                background-color: transparent;
            }}
        """)

        self.label_date.setStyleSheet(f"""
            QLabel {{
                font-family: {font};
                font-size: {date_size}px;
                color: {text_color};
                background-color: transparent;
            }}
        """)

        self.label_quote.setStyleSheet(f"""
            QLabel {{
                font-family: {font};
                font-size: {quote_size}px;
                color: {text_color};
                background-color: transparent;
                padding-top: 10px;
                opacity: 0.92;
            }}
        """)

    def update_clock(self, time: str, date: str):
        self.label_time.setText(time)
        self.label_date.setText(date)

    def set_quote(self, quote: str):
        self.label_quote.setText(quote)
