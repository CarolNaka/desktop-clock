from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QComboBox, QFrame, QPushButton, QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QColor, QPainter, QBrush, QPen

FONTS = [
    "Consolas",
    "Cascadia Mono",
    "Cascadia Code",
    "Segoe UI Mono",
    "Lucida Console",
    "Courier New",
    "Arial",
    "Segoe UI",
    "Calibri",
    "Verdana",
    "Tahoma",
    "Georgia",
    "Times New Roman",
    "Impact",
]

PANEL_WIDTH = 268


class ColorDot(QWidget):
    clicked = Signal()

    def __init__(self, settings_manager, color: str, size: int = 26):
        super().__init__()
        self.sm = settings_manager
        self._color = color
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

        p.setBrush(QBrush(QColor(self._color or "#000")))

        if self._active:
            ring = QColor(self.sm.get("text_color"))
            p.setPen(QPen(ring, 2))
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

        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(280)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        self.setObjectName("settingsPanelRoot")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(36)
        self._shadow.setOffset(12, 0)
        self._shadow.setColor(QColor(0, 0, 0, 88))
        self.setGraphicsEffect(self._shadow)

        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 28, 22, 28)
        layout.setSpacing(0)

        layout.addWidget(self._section("THEME"))
        layout.addSpacing(12)
        layout.addWidget(self._preset_block())
        layout.addSpacing(22)
        layout.addWidget(self._divider())
        layout.addSpacing(22)

        layout.addWidget(self._section("FONT"))
        layout.addSpacing(12)
        layout.addWidget(self._font_dropdown())
        layout.addSpacing(14)
        layout.addWidget(self._size_slider())
        layout.addSpacing(22)
        layout.addWidget(self._divider())
        layout.addSpacing(22)

        layout.addWidget(self._section("FORMAT"))
        layout.addSpacing(12)
        layout.addWidget(self._seconds_toggle())
        layout.addSpacing(12)
        layout.addWidget(self._format_buttons())

        layout.addStretch()

    def _apply_style(self):
        bg = self.sm.get("background_color")
        c = QColor(bg)
        h, s, v, _ = c.getHsvF()
        # Superfície mais clara/escura que o relógio para parecer um cartão sobreposto
        if v > 0.52:
            v_panel = max(0.03, v - 0.15)
        else:
            v_panel = min(0.96, v + 0.17)
        panel_bg = QColor.fromHsvF(h, min(s + 0.04, 1.0), v_panel).name()
        text = self.sm.get("text_color")
        font = self.sm.get("font")

        if c.lightness() < 135:
            edge = "rgba(255,255,255,0.2)"
            edge_soft = "rgba(255,255,255,0.09)"
            edge_left = "rgba(0,0,0,0.45)"
            sh = QColor(0, 0, 0, 105)
        else:
            edge = "rgba(0,0,0,0.13)"
            edge_soft = "rgba(0,0,0,0.06)"
            edge_left = "rgba(0,0,0,0.07)"
            sh = QColor(0, 0, 0, 38)

        self._shadow.setColor(sh)

        self.setStyleSheet(f"""
            #settingsPanelRoot {{
                background-color: {panel_bg};
                color: {text};
                font-family: '{font}';
                font-size: 12px;
                border: none;
                border-left: 1px solid {edge_left};
                border-top: 1px solid {edge_soft};
                border-bottom: 1px solid {edge_soft};
                border-right: 2px solid {edge};
                border-top-right-radius: 16px;
                border-bottom-right-radius: 16px;
            }}
            QComboBox {{
                background-color: rgba(128,128,128,0.12);
                color: {text};
                border: 1px solid rgba(128,128,128,0.28);
                border-radius: 10px;
                padding: 10px 12px;
                min-height: 22px;
                font-size: 12px;
                font-family: '{font}';
            }}
            QComboBox:hover {{
                border: 1px solid rgba(128,128,128,0.42);
                background-color: rgba(128,128,128,0.16);
            }}
            QComboBox::drop-down {{ border: none; width: 22px; }}
            QComboBox QAbstractItemView {{
                background-color: {panel_bg};
                color: {text};
                selection-background-color: rgba(128,128,128,0.22);
                border: 1px solid rgba(128,128,128,0.28);
                padding: 6px;
                outline: none;
            }}
            QSlider::groove:horizontal {{
                height: 4px;
                background: rgba(128,128,128,0.2);
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                width: 16px; height: 16px;
                margin: -7px 0;
                border-radius: 8px;
                background: {text};
            }}
            QSlider::sub-page:horizontal {{
                background: {text};
                border-radius: 2px;
                opacity: 0.65;
            }}
            QPushButton {{
                background-color: rgba(128,128,128,0.12);
                color: {text};
                border: 1px solid rgba(128,128,128,0.28);
                border-radius: 10px;
                padding: 9px 0;
                font-size: 12px;
                font-family: '{font}';
            }}
            QPushButton:hover {{
                background-color: rgba(128,128,128,0.2);
            }}
            QPushButton[active="true"] {{
                background-color: rgba(128,128,128,0.24);
                border: 1px solid rgba(128,128,128,0.5);
            }}
        """)

        self._update_preset_dots()

    def _section(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "font-size: 10px; letter-spacing: 2.2px; font-weight: 600;"
            "color: rgba(128,128,128,0.55); background: transparent;"
        )
        return lbl

    def _subsection(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "font-size: 11px; color: rgba(128,128,128,0.45);"
            "background: transparent; padding-top: 2px;"
        )
        return lbl

    def _divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background: rgba(128,128,128,0.14); max-height: 1px;")
        return line

    def _preset_block(self):
        outer = QWidget()
        outer.setStyleSheet("background: transparent;")
        v = QVBoxLayout(outer)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(10)

        dark_presets = self.sm.presets_by_group().get("dark", [])
        light_presets = self.sm.presets_by_group().get("light", [])

        v.addWidget(self._subsection("Dark"))
        v.addWidget(self._dot_row(dark_presets))

        v.addSpacing(4)
        v.addWidget(self._subsection("Light"))
        v.addWidget(self._dot_row(light_presets))

        return outer

    def _dot_row(self, presets):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(12)

        active_id = self.sm.get("active_preset")

        for preset in presets:
            dot = ColorDot(self.sm, color=preset["background_color"])
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

        row.addStretch()
        return container

    def _update_preset_dots(self):
        active_id = self.sm.get("active_preset")
        for pid, dot in self._preset_dots.items():
            dot.set_active(pid == active_id)

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
        layout.setSpacing(8)

        header = QHBoxLayout()
        lbl = QLabel("Size")
        lbl.setStyleSheet("font-size: 12px; color: rgba(128,128,128,0.58); background: transparent;")
        self._size_val = QLabel(f"{self.sm.get('font_size')}px")
        self._size_val.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {self.sm.get('text_color')}; background: transparent;"
        )
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
        row.setSpacing(12)

        lbl = QLabel("Show seconds")
        lbl.setStyleSheet("font-size: 12px; background: transparent;")

        toggle = QPushButton()
        toggle.setFixedSize(40, 22)
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
        bg = "rgba(128,128,128,0.42)" if checked else "rgba(128,128,128,0.16)"
        return f"""
            QPushButton {{
                background-color: {bg};
                border: none;
                border-radius: 11px;
            }}
        """

    def _format_buttons(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)

        current = self.sm.get("format")
        self._fmt_btns = {}

        for fmt in ["24h", "12h"]:
            btn = QPushButton(fmt)
            btn.setProperty("active", fmt == current)
            btn.setStyle(btn.style())

            def make_handler(f):
                def handler():
                    self.sm.set("format", f)
                    for ff, bb in self._fmt_btns.items():
                        bb.setProperty("active", ff == f)
                        bb.setStyle(bb.style())
                    self.config_changed.emit()

                return handler

            btn.clicked.connect(make_handler(fmt))
            self._fmt_btns[fmt] = btn
            row.addWidget(btn)

        return container

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
