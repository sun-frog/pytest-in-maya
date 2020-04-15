import pytest

# imports that bug out with RollbackImporter.uninstall()
# must be imported before creating Window
# because of Window.rollback_importer
import pymel.core as pm
import maya.utils  # pylint: disable=unused-import


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
        super(Window, self).__init__()

        self.rollback_importer = RollbackImporter()

        self._create_connections()

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
        super(Window, self).closeEvent(event)

        self.rollback_importer.uninstall()


WINDOW = Window()
WINDOW.showMaximized()
