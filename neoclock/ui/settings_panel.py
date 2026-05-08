from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QSlider, QComboBox, QCheckBox, QColorDialog, QFrame
)
from PySide6.QtCore import Qt, Signal

FONTES = ["Consolas", "Arial", "Courier New", "Segoe UI", "Verdana"]

class SettingsPanel(QWidget):
    config_alterada = Signal()  # notifica a janela principal

    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager
        self.setFixedWidth(220)
        self.setStyleSheet("background-color: #2a2a3e; color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)

        layout.addWidget(self._titulo("Configurações"))
        layout.addWidget(self._separador())

        layout.addWidget(self._secao("CORES"))
        layout.addWidget(self._botao_cor("Fundo", "cor_fundo"))
        layout.addWidget(self._botao_cor("Texto", "cor_texto"))

        layout.addWidget(self._separador())
        layout.addWidget(self._secao("FONTE"))
        layout.addWidget(self._dropdown_fonte())
        layout.addWidget(self._slider_tamanho())

        layout.addWidget(self._separador())
        layout.addWidget(self._secao("FORMATO"))
        layout.addWidget(self._checkbox_segundos())
        layout.addWidget(self._combo_formato())

        layout.addStretch()

    def _titulo(self, texto):
        lbl = QLabel(texto)
        lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        return lbl

    def _secao(self, texto):
        lbl = QLabel(texto)
        lbl.setStyleSheet("font-size: 10px; color: #888; margin-top: 6px;")
        return lbl

    def _separador(self):
        linha = QFrame()
        linha.setFrameShape(QFrame.HLine)
        linha.setStyleSheet("color: #3a3a5e;")
        return linha

    def _botao_cor(self, label, chave):
        btn = QPushButton(f"● {label}: {self.sm.get(chave)}")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #3a3a5e;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 4px;
                text-align: left;
            }}
            QPushButton:hover {{ background-color: #4a4a7e; }}
        """)

        def escolher():
            cor = QColorDialog.getColor()
            if cor.isValid():
                hex_cor = cor.name()
                self.sm.set(chave, hex_cor)
                btn.setText(f"● {label}: {hex_cor}")
                self.config_alterada.emit()

        btn.clicked.connect(escolher)
        return btn

    def _dropdown_fonte(self):
        combo = QComboBox()
        combo.addItems(FONTES)
        combo.setCurrentText(self.sm.get("fonte"))
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
            lambda v: (self.sm.set("fonte", v), self.config_alterada.emit())
        )
        return combo

    def _slider_tamanho(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(f"Tamanho: {self.sm.get('tamanho_fonte')}px")
        lbl.setStyleSheet("color: white; font-size: 11px;")

        slider = QSlider(Qt.Horizontal)
        slider.setRange(24, 120)
        slider.setValue(self.sm.get("tamanho_fonte"))
        slider.setStyleSheet("accent-color: #e94560;")

        def ao_mover(v):
            lbl.setText(f"Tamanho: {v}px")
            self.sm.set("tamanho_fonte", v)
            self.config_alterada.emit()

        slider.valueChanged.connect(ao_mover)
        layout.addWidget(lbl)
        layout.addWidget(slider)
        return container

    def _checkbox_segundos(self):
        cb = QCheckBox("Mostrar segundos")
        cb.setChecked(self.sm.get("mostrar_segundos"))
        cb.setStyleSheet("color: white; font-size: 11px;")
        cb.toggled.connect(
            lambda v: (self.sm.set("mostrar_segundos", v), self.config_alterada.emit())
        )
        return cb

    def _combo_formato(self):
        combo = QComboBox()
        combo.addItems(["24h", "12h"])
        combo.setCurrentText(self.sm.get("formato"))
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
            lambda v: (self.sm.set("formato", v), self.config_alterada.emit())
        )
        return combo