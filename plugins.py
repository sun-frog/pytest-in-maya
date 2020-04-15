"""pytest plugins."""


class CollectTestNames:
    """
    Collect test names

    Example

    >>> test_names = CollectTestNames()
    >>> directory = '<path_to_test_dir>/<test>.py'
    >>> pytest.main(['--collect-only', '-p', 'no:terminal', '--capture=sys', directory],
                    plugins=[test_names])
    >>>
    >>> for test_name in test_names.collected:
    >>>     print(test_name)
    """

    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item.nodeid)
