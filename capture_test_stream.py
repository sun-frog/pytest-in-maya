import io
import re
import sys
import tempfile

from PySide2.QtGui import QColor


class COLOR(object):

    SUCCESS = QColor(13, 188, 121)
    FAIL = QColor(241, 57, 41)
    ERROR = FAIL
    SKIP = QColor(229, 229, 16)
    XFAIL = SKIP
    NORMAL = QColor(200, 200, 200)

    DIFF = QColor(41, 184, 219)
    DIFF_LEFT = SUCCESS
    DIFF_RIGHT = ERROR


CONSOLE_RESET = '\x1b[0m'

CONSOLE_BRIGHT_CYAN = '\x1b[1m\x1b[36m'
CONSOLE_BRIGHT_RED = '\x1b[1m\x1b[31m'
CONSOLE_BRIGHT_GREEN = '\x1b[1m\x1b[32m'
CONSOLE_COLORS = {
    CONSOLE_BRIGHT_CYAN: COLOR.DIFF,
    CONSOLE_BRIGHT_GREEN: COLOR.DIFF_LEFT,
    CONSOLE_BRIGHT_RED: COLOR.DIFF_RIGHT,
}


def get_color_text_pattern(colors):
    colors = map(re.escape, CONSOLE_COLORS)
    colors = '|'.join(colors)

    color_text_pattern = re.compile('({})(.*)'.format(colors))
    return color_text_pattern


COLOR_TEXT_PATTERN = get_color_text_pattern(CONSOLE_COLORS)


class CaptureTestStream(io.FileIO):
    """Allows the output of the tests to be displayed in a QTextEdit."""

    def __init__(self, text_edit):
        temp_file = tempfile.mkstemp(prefix='pytest_')[1]

        super(CaptureTestStream, self).__init__(temp_file, 'w+')
        self.text_edit = text_edit
        self.log = []
        self.old_stdout = None

    def write(self, text):
        """Write text into the QTextEdit."""
        super(CaptureTestStream, self).write(text)

        if CONSOLE_RESET in text:
            self._insert_diff_text(text)
        else:
            self._insert_text(text)

        self._scroll_to_bottom()
        self.log.append(text)

    def _insert_diff_text(self, text):
        parts = text.split(CONSOLE_RESET)
        parts = [part for part in parts if part != '']

        for part in parts:
            match = COLOR_TEXT_PATTERN.match(part)

            if match:
                color = match.group(1)
                text = match.group(2)
                color = CONSOLE_COLORS[color]
                self._insert_text(text, color)
            else:
                self._insert_text(part)

    def _insert_text(self, text, color=None):

        if not color:
            self._set_text_color(text)
        else:
            self.text_edit.setTextColor(color)

        self.text_edit.insertPlainText(text)
        self._reset_text_color()

    def _set_text_color(self, text):
        if text == 'PASSED' or text == '.':
            self.text_edit.setTextColor(COLOR.SUCCESS)

        elif text == 'FAILED' or text == 'F':
            self.text_edit.setTextColor(COLOR.FAIL)

        elif text.startswith('===') and'failed' in text:
            self.text_edit.setTextColor(COLOR.FAIL)

        elif text.startswith('___') or text.endswith('.py'):
            self.text_edit.setTextColor(COLOR.FAIL)

        elif text == 'ERROR' or text == 'E' or text.startswith('E '):
            self.text_edit.setTextColor(COLOR.ERROR)

        elif text == 'SKIPPED' or text == 's':
            self.text_edit.setTextColor(COLOR.SKIP)

        elif text == 'XFAIL' or text == 'x':
            self.text_edit.setTextColor(COLOR.XFAIL)

    def _scroll_to_bottom(self):
        scroll_bar = self.text_edit.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def _reset_text_color(self):
        self.text_edit.setTextColor(COLOR.NORMAL)

    def __enter__(self):
        super(CaptureTestStream, self).__enter__()

        self.old_stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, *exec_info):
        super(CaptureTestStream, self).__exit__(*exec_info)

        sys.stdout = self.old_stdout

        if exec_info != (None, None, None):
            print exec_info

        for line, text in enumerate(self.log):
            print 'line:', line, repr(text)
