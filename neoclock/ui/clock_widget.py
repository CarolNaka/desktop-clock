from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class ClockWidget(QLabel):
    def __init__(self, settings_manager):
        super().__init__()
        self.sm = settings_manager
        self.setAlignment(Qt.AlignCenter)
        self.aplicar_estilo()

    def aplicar_estilo(self):
        fonte = self.sm.get("fonte")
        tamanho = self.sm.get("tamanho_fonte")
        cor_texto = self.sm.get("cor_texto")
        cor_fundo = self.sm.get("cor_fundo")

        self.setStyleSheet(f"""
            QLabel {{
                font-family: {fonte};
                font-size: {tamanho}px;
                font-weight: bold;
                color: {cor_texto};
                background-color: {cor_fundo};
                padding: 20px;
            }}
        """)

    def atualizar_hora(self, hora: str):
        self.setText(hora)