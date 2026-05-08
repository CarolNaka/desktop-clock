import sys
from PySide6.QtWidgets import QApplication
from core.settings_manager import SettingsManager
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MyClock")

    sm = SettingsManager()
    window = MainWindow(sm)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()