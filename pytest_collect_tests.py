import pytest

from . import plugins

test_names = plugins.CollectTestNames()
directory = 'C:/Users/sun/Desktop/New_folder/test_qt.py'
pytest.main(['--collect-only', '-p', 'no:terminal', '--capture=sys', directory],
            plugins=[test_names])

for test_name in test_names.collected:
    print(test_name)
