import pytest


class MyPlugin:

    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item.nodeid)


my_plugin = MyPlugin()
directory = 'C:/Users/sun/Desktop/New_folder/test_qt.py'
pytest.main(['--collect-only', '-p', 'no:terminal', '--capture=sys', directory],
            plugins=[my_plugin])

for nodeid in my_plugin.collected:
    print(nodeid)
