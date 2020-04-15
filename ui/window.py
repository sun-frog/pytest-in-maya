from PySide2.QtWidgets import (QApplication,
                               QHBoxLayout,
                               QDialog, QTextEdit, QPushButton,
                               )
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont


class Window(QDialog):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self._create_widgets()
        self._create_layout()
        self._create_style()

    def _create_widgets(self):
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.test_button = QPushButton('run tests')

    def _create_layout(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.text_edit)
        layout.addWidget(self.test_button)

    def _create_style(self):
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('Test in Maya')
        self.setStyleSheet('font-size: 12pt')

        screen = QApplication.primaryScreen()
        size = screen.size() * 0.66
        self.resize(size)

        self.text_edit.setStyleSheet('QTextEdit:focus{ border: none; }')
        font = QFont("Consolas, 'Courier New', monospace")
        font.setFixedPitch(True)
        self.text_edit.setFont(font)
