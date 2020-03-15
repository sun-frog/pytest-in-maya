import io
import sys
import tempfile

import pytest

from PySide2.QtWidgets import (QApplication,
                               QHBoxLayout,
                               QDialog, QTextEdit, QPushButton, )
from PySide2.QtGui import QColor
from PySide2.QtCore import Qt


import pymel.core as pm

from rollback_importer import RollbackImporter


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


class COLOR(object):
    FAIL_LIGHT = QColor(241, 57, 41)
    ERROR = FAIL_LIGHT

    SUCCESS = QColor(13, 188, 121)
    FAIL = QColor(205, 49, 49)
    ERROR = FAIL
    SKIP = QColor(229, 229, 16)
    NORMAL = QColor(200, 200, 200)


def preserve_huds(func):

    def wrapper(*args, **kwargs):
        # store current huds' names, visibility and positions
        old_huds = pm.headsUpDisplay(listHeadsUpDisplays=True) or []
        old_visibility = [get_hud_visibility(hud) for hud in old_huds]
        old_positions = [get_hud_position(hud) for hud in old_huds]

        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            # delete new huds
            all_huds = pm.headsUpDisplay(listHeadsUpDisplays=True) or []
            for hud in all_huds:
                if hud not in old_huds:
                    pm.headsUpDisplay(hud, remove=True)

            # restore huds' visibility
            for hud, visible in zip(old_huds, old_visibility):
                pm.headsUpDisplay(hud, e=True, visible=visible)

            # restore hud positions
            for hud, (section, block) in zip(old_huds, old_positions):
                pm.headsUpDisplay(hud, e=True, section=section, block=block)

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def get_hud_visibility(hud):
    return pm.headsUpDisplay(hud, q=True, visible=True)


def get_hud_position(hud):
    section = pm.headsUpDisplay(hud, q=True, section=True)
    block = pm.headsUpDisplay(hud, q=True, block=True)
    return section, block


class TestCaptureStream(io.FileIO):
    """Allows the output of the tests to be displayed in a QTextEdit."""

    def __init__(self, text_edit):
        temp_file = tempfile.mkstemp(prefix='pytest_')[1]

        super(self.__class__, self).__init__(temp_file, 'w+')
        self.text_edit = text_edit
        self.log = []

    def write(self, text):
        """Write text into the QTextEdit."""
        super(self.__class__, self).write(text)

        self._set_text_color(text)
        self.text_edit.insertPlainText(text)
        self._reset_text_color()

        self._scroll_to_bottom()
        self.log.append(text)

    def _set_text_color(self, text):
        if 'PASSED' == text or text == '.':
            self.text_edit.setTextColor(COLOR.SUCCESS)

        elif 'FAILED' == text or text == 'F':
            self.text_edit.setTextColor(COLOR.FAIL)

        elif 'failed' in text:
            self.text_edit.setTextColor(COLOR.FAIL_LIGHT)

        elif text == 'ERROR' or text == 'E' or text.startswith('E '):
            self.text_edit.setTextColor(COLOR.ERROR)

        elif text == 'SKIPPED' or text == 's' or text == 'XFAIL' or text == 'x':
            self.text_edit.setTextColor(COLOR.SKIP)

    def _scroll_to_bottom(self):
        scroll_bar = self.text_edit.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def _reset_text_color(self):
        self.text_edit.setTextColor(COLOR.NORMAL)

    def __enter__(self):
        super(self.__class__, self).__enter__()

        self.old_stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, *exec_info):
        super(self.__class__, self).__exit__(*exec_info)

        sys.stdout = self.old_stdout

        if exec_info != (None, None, None):
            print exec_info

        for line, text in enumerate(self.log):
            print 'line:', line, repr(text)

# line: 63 u'E     \x1b[0m\x1b[1m\x1b[36mleft:  \x1b[0m\x1b[1m\x1b[32m3\x1b[0m'
# line: 63 u'E     {reset}{bright}{cyan}left:  {reset}{bright}{geeen}3{reset}'

# line: 65 u'E     \x1b[0m\x1b[1m\x1b[36mright: \x1b[0m\x1b[1m\x1b[31m4\x1b[0m'
# line: 65 u'E     {reset}{bright}{cyan}right: {reset}{bright}{red}4{reset}'

# reset = "\x1b[0m"
# bright = "\x1b[1m"
# dim = "\x1b[2m"
# underscore = "\x1b[4m"
# blink = "\x1b[5m"
# reverse = "\x1b[7m"
# hidden = "\x1b[8m"

# black = "\x1b[30m"
# red = "\x1b[31m"
# green = "\x1b[32m"
# yellow = "\x1b[33m"
# blue = "\x1b[34m"
# magenta = "\x1b[35m"
# cyan = "\x1b[36m"
# white = "\x1b[37m"

# BGblack = "\x1b[40m"
# BGred = "\x1b[41m"
# BGgreen = "\x1b[42m"
# BGyellow = "\x1b[43m"
# BGblue = "\x1b[44m"
# BGmagenta = "\x1b[45m"
# BGcyan = "\x1b[46m"
# BGwhite = "\x1b[47m"


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
        self.setStyleSheet('font-size: 12pt')

        screen = QApplication.primaryScreen()
        size = screen.size() * 0.66
        self.resize(size)

        self.text_edit.setStyleSheet('QTextEdit:focus{ border: none; }')

    @preserve_huds
    def _run_tests(self):
        self._reset()

        with TestCaptureStream(self.text_edit):
            pytest.main(ARGS + TARGETS)

        self.rollback_importer.uninstall()
        pm.newFile(force=True)

    def _reset(self):
        self.rollback_importer.uninstall()
        self.text_edit.clear()
        self.text_edit.setTextColor(COLOR.NORMAL)

    def closeEvent(self, event):
        self.rollback_importer.uninstall()


WINDOW = Window()
WINDOW.showMaximized()
