import pytest

import pymel.core as pm


from rollback_importer import RollbackImporter

from .capture_test_stream import CaptureTestStream, COLOR
from . import decorators
from . import ui

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


class Window(ui.Window):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.rollback_importer = RollbackImporter()

    def _create_connections(self):
        self.test_button.clicked.connect(self._run_tests)

    @decorators.preserve_huds
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

    def closeEvent(self, event):
        super(self.__class__, self).closeEvent(event)

        self.rollback_importer.uninstall()


WINDOW = Window()
WINDOW.showMaximized()
