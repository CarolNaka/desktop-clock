from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class ClockWidget(QWidget):
    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(4)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label_hora = QLabel()
        self.label_hora.setAlignment(Qt.AlignCenter)

        self.label_data = QLabel()
        self.label_data.setAlignment(Qt.AlignCenter)

        self.label_frase = QLabel()
        self.label_frase.setAlignment(Qt.AlignCenter)
        self.label_frase.setWordWrap(True)

        layout.addWidget(self.label_hora)
        layout.addWidget(self.label_data)
        layout.addWidget(self.label_frase)

        self.aplicar_estilo()

    def aplicar_estilo(self):
        cor_texto = self.sm.get("cor_texto")
        cor_fundo = self.sm.get("cor_fundo")
        fonte = self.sm.get("fonte")
        tamanho = self.sm.get("tamanho_fonte")
        tamanho_data = max(12, tamanho // 4)
        tamanho_frase = max(11, tamanho // 5)

        self.setStyleSheet(f"background-color: {cor_fundo};")

        self.label_hora.setStyleSheet(f"""
            QLabel {{
                font-family: {fonte};
                font-size: {tamanho}px;
                font-weight: bold;
                color: {cor_texto};
                background-color: transparent;
            }}
        """)

        self.label_data.setStyleSheet(f"""
            QLabel {{
                font-family: {fonte};
                font-size: {tamanho_data}px;
                color: {cor_texto};
                background-color: transparent;
            }}
        """)

        self.label_frase.setStyleSheet(f"""
            QLabel {{
                font-family: {fonte};
                font-size: {tamanho_frase}px;
                color: {cor_texto};
                background-color: transparent;
                padding-top: 8px;
            }}
        """)

    def atualizar(self, hora: str, data: str):
        self.label_hora.setText(hora)
        self.label_data.setText(data)

    def definir_frase(self, frase: str):
        self.label_frase.setText(frase)