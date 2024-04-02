from __future__ import annotations

from pre_commit_hooks.check_test_meta import main


def test_func(tmpdir):
    filename = tmpdir.join('__init__.py')
    filename.write("""
def test_A():
    pass

@pytest.mark.meta(author="Raigor Deng")
def test_B():
    pass

@pytest.mark.meta(author="Raigor Deng")
def a_test():
    pass

""")
    ret = main((str(filename),))
    assert ret == 1


def test_class(tmpdir):
    filename = tmpdir.join('__init__.py')
    filename.write("""
class TestA():
    pass

@pytest.mark.meta(author="Raigor Deng")
class TestB():
    pass

class ATest():
    pass

""")
    ret = main((str(filename),))
    assert ret == 1
