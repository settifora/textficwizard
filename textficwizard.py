from PyQt5.QtWidgets import QApplication
from gui.appmain import AppMainWindow

app = QApplication([])

window = AppMainWindow()
window.show()

app.exec()