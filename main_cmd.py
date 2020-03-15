import pytest

from rollback_importer import RollbackImporter


ARGS = [
    '-s',
    # '--verbose',
    # '--tb=line',
    '-vv',
]

TARGETS = [
    # 'C:/Users/sun/Desktop/New_folder/test_qt.py',
    'C:/Users/sun/Desktop/New_folder/test_script.py',
]

RBI = RollbackImporter()

pytest.main(ARGS + TARGETS); RBI.uninstall()
