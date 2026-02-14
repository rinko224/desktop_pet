import sys
from PySide2.QtWidgets import QApplication
from ui.PetWindow import PetWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PetWindow()
    window.show()
    sys.exit(app.exec_())

