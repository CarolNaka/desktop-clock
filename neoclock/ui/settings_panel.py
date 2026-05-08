from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSlider, QComboBox, QCheckBox, QColorDialog, QFrame
)
from PySide6.QtCore import Qt, Signal

FONTS = ["Consolas", "Arial", "Courier New", "Segoe UI", "Verdana"]


class SettingsPanel(QWidget):
    config_changed = Signal()  # Notifies the main window

    def __init__(self, settings_manager):
        super().__init__()

        self.sm = settings_manager

        self.setFixedWidth(220)
        self.setStyleSheet(
            "background-color: #2a2a3e; color: white;"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)

        layout.addWidget(self._title("Settings"))
        layout.addWidget(self._separator())

        layout.addWidget(self._section("COLORS"))
        layout.addWidget(self._color_button("Background", "background_color"))
        layout.addWidget(self._color_button("Text", "text_color"))

        layout.addWidget(self._separator())
        layout.addWidget(self._section("FONT"))
        layout.addWidget(self._font_dropdown())
        layout.addWidget(self._size_slider())

        layout.addWidget(self._separator())
        layout.addWidget(self._section("FORMAT"))
        layout.addWidget(self._seconds_checkbox())
        layout.addWidget(self._format_combo())

        layout.addStretch()

    def _title(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: white;"
        )
        return lbl

    def _section(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "font-size: 10px; color: #888; margin-top: 6px;"
        )
        return lbl

    def _separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #3a3a5e;")
        return line

    def _color_button(self, label, key):
        btn = QPushButton(f"● {label}: {self.sm.get(key)}")

        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #3a3a5e;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 4px;
                text-align: left;
            }}

            QPushButton:hover {{
                background-color: #4a4a7e;
            }}
        """)

        def choose():
            color = QColorDialog.getColor()

            if color.isValid():
                hex_color = color.name()

                self.sm.set(key, hex_color)

                btn.setText(f"● {label}: {hex_color}")

                self.config_changed.emit()

        btn.clicked.connect(choose)

        return btn

    def _font_dropdown(self):
        combo = QComboBox()

        combo.addItems(FONTS)
        combo.setCurrentText(self.sm.get("font"))

        combo.setStyleSheet("""
            QComboBox {
                background-color: #3a3a5e;
                color: white;
                border: none;
                padding: 4px;
                border-radius: 4px;
            }
        """)

        combo.currentTextChanged.connect(
            lambda v: (
                self.sm.set("font", v),
                self.config_changed.emit()
            )
        )

        return combo

    def _size_slider(self):
        container = QWidget()

        container.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(f"Size: {self.sm.get('font_size')}px")

        lbl.setStyleSheet(
            "color: white; font-size: 11px;"
        )

        slider = QSlider(Qt.Horizontal)

        slider.setRange(24, 120)
        slider.setValue(self.sm.get("font_size"))

        slider.setStyleSheet("accent-color: #e94560;")

        def on_move(v):
            lbl.setText(f"Size: {v}px")

            self.sm.set("font_size", v)

            self.config_changed.emit()

        slider.valueChanged.connect(on_move)

        layout.addWidget(lbl)
        layout.addWidget(slider)

        return container

    def _seconds_checkbox(self):
        cb = QCheckBox("Show seconds")

        cb.setChecked(self.sm.get("show_seconds"))

        cb.setStyleSheet(
            "color: white; font-size: 11px;"
        )

        cb.toggled.connect(
            lambda v: (
                self.sm.set("show_seconds", v),
                self.config_changed.emit()
            )
        )

        return cb

    def _format_combo(self):
        combo = QComboBox()

        combo.addItems(["24h", "12h"])

        combo.setCurrentText(self.sm.get("format"))

        combo.setStyleSheet("""
            QComboBox {
                background-color: #3a3a5e;
                color: white;
                border: none;
                padding: 4px;
                border-radius: 4px;
            }
        """)

        combo.currentTextChanged.connect(
            lambda v: (
                self.sm.set("format", v),
                self.config_changed.emit()
            )
        )

        return combo