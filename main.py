import pytest

from PySide2.QtWidgets import (QApplication,
                               QHBoxLayout,
                               QDialog, QTextEdit, QPushButton, )
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont


import pymel.core as pm


from rollback_importer import RollbackImporter

from maya_pytest.capture_test_stream import CaptureTestStream, COLOR
from maya_pytest.utils import preserve_huds

ARGS = [
    '-s',
    # '--verbose',
    # '--tb=line',
    '-vv',
]

TARGETS = [
    'C:/Users/sun/Desktop/New_folder/test_qt.py',
    'C:/Users/sun/Desktop/New_folder/test_script.py',
    # 'E:/Projects/python/maya/advanced_rigging/tests/test_rig/test_base/test_control',
    # 'E:/Projects/python/maya/advanced_rigging/tests/test_rig/test_modules/test_stretchy_limb',
]


class Window(QDialog):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.rollback_importer = RollbackImporter()

        self._create_widgets()
        self._create_layout()
        self._create_connections()
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

    def _create_connections(self):
        self.test_button.clicked.connect(self._run_tests)

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

    @preserve_huds
    def _run_tests(self):
        self._reset()

        with CaptureTestStream(self.text_edit):
            pytest.main(ARGS + TARGETS)

        self.rollback_importer.uninstall()
        pm.newFile(force=True)

    def _reset(self):
        self.rollback_importer.uninstall()
        self.text_edit.clear()
        self.text_edit.setTextColor(COLOR.NORMAL)

    def closeEvent(self, event):  # pylint: disable=arguments-differ
        super(self.__class__, self).closeEvent(event)

        self.rollback_importer.uninstall()


WINDOW = Window()
WINDOW.showMaximized()
