from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QComboBox, QColorDialog, QFrame, QPushButton
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QConicalGradient

FONTS = ["Consolas", "Arial", "Courier New", "Segoe UI", "Verdana"]
PANEL_WIDTH = 200


class ColorDot(QWidget):
    clicked = Signal()

    def __init__(self, color: str = None, rainbow: bool = False, size: int = 22):
        super().__init__()
        self._color = color
        self._rainbow = rainbow
        self._active = False
        self._size = size
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)

    def set_active(self, active: bool):
        self._active = active
        self.update()

    def set_color(self, color: str):
        self._color = color
        self.update()

    def mousePressEvent(self, event):
        self.clicked.emit()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(2, 2, -2, -2)

        if self._rainbow:
            grad = QConicalGradient(r.center(), 0)
            colors = ["#e94560","#f5a623","#2ecc71","#3498db","#9b59b6","#e94560"]
            for i, c in enumerate(colors):
                grad.setColorAt(i / (len(colors) - 1), QColor(c))
            p.setBrush(QBrush(grad))
        else:
            p.setBrush(QBrush(QColor(self._color or "#000")))

        if self._active:
            text_color = QColor(self.parent().sm.get("text_color") if self.parent() and hasattr(self.parent(), "sm") else "#ffffff")
            pen = QPen(text_color, 2)
            p.setPen(pen)
            r = r.adjusted(1, 1, -1, -1)
        else:
            p.setPen(Qt.NoPen)

        p.drawEllipse(r)


class SettingsPanel(QWidget):
    config_changed = Signal()

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.sm = settings_manager
        self.setFixedWidth(PANEL_WIDTH)
        self._visible = False
        self._preset_dots = {}
        self._custom_dot = None

        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(250)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(0)

        layout.addWidget(self._section("THEME"))
        layout.addSpacing(8)
        layout.addWidget(self._preset_row())
        layout.addSpacing(14)
        layout.addWidget(self._divider())
        layout.addSpacing(14)

        layout.addWidget(self._section("FONT"))
        layout.addSpacing(8)
        layout.addWidget(self._font_dropdown())
        layout.addSpacing(8)
        layout.addWidget(self._size_slider())
        layout.addSpacing(14)
        layout.addWidget(self._divider())
        layout.addSpacing(14)

        layout.addWidget(self._section("FORMAT"))
        layout.addSpacing(8)
        layout.addWidget(self._seconds_toggle())
        layout.addSpacing(8)
        layout.addWidget(self._format_buttons())

        layout.addStretch()

    def _apply_style(self):
        bg = self.sm.get("background_color")
        c = QColor(bg)
        h, s, v, _ = c.getHsvF()
        v2 = max(0.0, v - 0.1) if v > 0.5 else min(1.0, v + 0.12)
        panel_bg = QColor.fromHsvF(h, min(s + 0.03, 1.0), v2).name()
        text = self.sm.get("text_color")
        font = self.sm.get("font")

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {panel_bg};
                color: {text};
                font-family: '{font}';
                font-size: 11px;
                border: none;
            }}
            QComboBox {{
                background-color: rgba(128,128,128,0.08);
                color: {text};
                border: 0.5px solid rgba(128,128,128,0.2);
                border-radius: 7px;
                padding: 6px 10px;
                font-size: 11px;
                font-family: '{font}';
            }}
            QComboBox:hover {{
                border: 0.5px solid rgba(128,128,128,0.35);
            }}
            QComboBox::drop-down {{ border: none; width: 16px; }}
            QComboBox QAbstractItemView {{
                background-color: {panel_bg};
                color: {text};
                selection-background-color: rgba(128,128,128,0.15);
                border: 0.5px solid rgba(128,128,128,0.2);
                padding: 4px;
            }}
            QSlider::groove:horizontal {{
                height: 3px;
                background: rgba(128,128,128,0.15);
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                width: 14px; height: 14px;
                margin: -6px 0;
                border-radius: 7px;
                background: {text};
            }}
            QSlider::sub-page:horizontal {{
                background: {text};
                border-radius: 2px;
                opacity: 0.7;
            }}
            QPushButton {{
                background-color: rgba(128,128,128,0.08);
                color: {text};
                border: 0.5px solid rgba(128,128,128,0.2);
                border-radius: 7px;
                padding: 6px 0;
                font-size: 11px;
                font-family: '{font}';
            }}
            QPushButton:hover {{
                background-color: rgba(128,128,128,0.18);
            }}
            QPushButton[active="true"] {{
                background-color: rgba(128,128,128,0.2);
                border: 0.5px solid rgba(128,128,128,0.45);
            }}
        """)

        self._update_preset_dots()

    # ── Seções ─────────────────────────────────────────────────

    def _section(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "font-size: 9px; letter-spacing: 1.8px;"
            "color: rgba(128,128,128,0.5); background: transparent;"
        )
        return lbl

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background: rgba(128,128,128,0.12); max-height: 1px;")
        return line

    def _preset_row(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)

        all_presets = self.sm.all_presets()
        active_id = self.sm.get("active_preset")

        for preset in all_presets:
            dot = ColorDot(color=preset["background_color"])
            dot.set_active(preset["id"] == active_id)
            dot.setToolTip(preset["label"])

            def make_handler(pid):
                def handler():
                    self.sm.apply_preset(pid)
                    self._update_preset_dots()
                    self._apply_style()
                    self.config_changed.emit()
                return handler

            dot.clicked.connect(make_handler(preset["id"]))
            self._preset_dots[preset["id"]] = dot
            row.addWidget(dot)

        # Bolinha arco-íris — color picker customizado
        self._custom_dot = ColorDot(rainbow=True)
        self._custom_dot.setToolTip("Custom")
        self._custom_dot.set_active(active_id == "custom")
        self._custom_dot.clicked.connect(self._open_custom_picker)
        row.addWidget(self._custom_dot)

        row.addStretch()
        return container

    def _update_preset_dots(self):
        active_id = self.sm.get("active_preset")
        for pid, dot in self._preset_dots.items():
            dot.set_active(pid == active_id)
        if self._custom_dot:
            self._custom_dot.set_active(active_id == "custom")

    def _open_custom_picker(self):
        color = QColorDialog.getColor(
            QColor(self.sm.get("background_color")), self,
            "Background color"
        )
        if color.isValid():
            self.sm.set("background_color", color.name())
            self.sm.set("active_preset", "custom")
            self._update_preset_dots()
            self._apply_style()
            self.config_changed.emit()

    def _font_dropdown(self):
        combo = QComboBox()
        combo.addItems(FONTS)
        combo.setCurrentText(self.sm.get("font"))
        combo.currentTextChanged.connect(
            lambda v: (self.sm.set("font", v), self._apply_style(), self.config_changed.emit())
        )
        return combo

    def _size_slider(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        header = QHBoxLayout()
        lbl = QLabel("Size")
        lbl.setStyleSheet("font-size: 11px; color: rgba(128,128,128,0.6); background: transparent;")
        self._size_val = QLabel(f"{self.sm.get('font_size')}px")
        self._size_val.setStyleSheet(f"font-size: 11px; color: {self.sm.get('text_color')}; background: transparent;")
        header.addWidget(lbl)
        header.addStretch()
        header.addWidget(self._size_val)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(24, 120)
        slider.setValue(self.sm.get("font_size"))

        def on_change(v):
            self._size_val.setText(f"{v}px")
            self.sm.set("font_size", v)
            self.config_changed.emit()

        slider.valueChanged.connect(on_change)
        layout.addLayout(header)
        layout.addWidget(slider)
        return container

    def _seconds_toggle(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)

        lbl = QLabel("Seconds")
        lbl.setStyleSheet("font-size: 11px; background: transparent;")

        # Toggle pill customizado
        toggle = QPushButton()
        toggle.setFixedSize(36, 20)
        toggle.setCheckable(True)
        toggle.setChecked(self.sm.get("show_seconds"))
        toggle.setStyleSheet(self._toggle_style(self.sm.get("show_seconds")))

        def on_toggle(checked):
            toggle.setStyleSheet(self._toggle_style(checked))
            self.sm.set("show_seconds", checked)
            self.config_changed.emit()

        toggle.toggled.connect(on_toggle)
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(toggle)
        return container

    def _toggle_style(self, checked: bool) -> str:
        text = self.sm.get("text_color")
        bg = f"rgba(128,128,128,0.4)" if checked else "rgba(128,128,128,0.15)"
        return f"""
            QPushButton {{
                background-color: {bg};
                border: none;
                border-radius: 10px;
            }}
        """

    def _format_buttons(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)

        current = self.sm.get("format")
        self._fmt_btns = {}

        for fmt in ["24h", "12h"]:
            btn = QPushButton(fmt)
            btn.setProperty("active", fmt == current)
            btn.setStyle(btn.style())

            def make_handler(f, b):
                def handler():
                    self.sm.set("format", f)
                    for ff, bb in self._fmt_btns.items():
                        bb.setProperty("active", ff == f)
                        bb.setStyle(bb.style())
                    self.config_changed.emit()
                return handler

            btn.clicked.connect(make_handler(fmt, btn))
            self._fmt_btns[fmt] = btn
            row.addWidget(btn)

        return container

    # ── Animação ───────────────────────────────────────────────

    def slide_in(self):
        if self._visible:
            return
        self._visible = True
        h = self.parent().height() if self.parent() else self.height()
        self._anim.stop()
        self._anim.setStartValue(QRect(-PANEL_WIDTH, 0, PANEL_WIDTH, h))
        self._anim.setEndValue(QRect(0, 0, PANEL_WIDTH, h))
        self.raise_()
        self._anim.start()

    def slide_out(self):
        if not self._visible:
            return
        self._visible = False
        h = self.parent().height() if self.parent() else self.height()
        self._anim.stop()
        self._anim.setStartValue(QRect(0, 0, PANEL_WIDTH, h))
        self._anim.setEndValue(QRect(-PANEL_WIDTH, 0, PANEL_WIDTH, h))
        self._anim.start()