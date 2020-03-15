import io
import sys
import tempfile

from PySide2.QtGui import QColor


class COLOR(object):
    FAIL_LIGHT = QColor(241, 57, 41)
    ERROR = FAIL_LIGHT

    SUCCESS = QColor(13, 188, 121)
    FAIL = QColor(205, 49, 49)
    ERROR = FAIL
    SKIP = QColor(229, 229, 16)
    NORMAL = QColor(200, 200, 200)


class CaptureTestStream(io.FileIO):
    """Allows the output of the tests to be displayed in a QTextEdit."""

    def __init__(self, text_edit):
        temp_file = tempfile.mkstemp(prefix='pytest_')[1]

        super(CaptureTestStream, self).__init__(temp_file, 'w+')
        self.text_edit = text_edit
        self.log = []

    def write(self, text):
        """Write text into the QTextEdit."""
        super(CaptureTestStream, self).write(text)

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
