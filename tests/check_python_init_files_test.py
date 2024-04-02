from __future__ import annotations

from pre_commit_hooks.check_python_init_files import main


def test_init_good(tmpdir):
    filename = tmpdir.mkdir('tests').join('__init__.py')
    filename.write('__cn__ = "test"')
    ret = main((str(filename),))
    assert ret == 0


def test_init_bad(tmpdir):
    filename = tmpdir.mkdir('tests').join('__init__.py')
    filename.write('__cn_ = "test"')
    ret = main((str(filename),))
    assert ret == 1


def test_init_parent_dir(tmpdir):
    filename = tmpdir.mkdir('testdir').join('__init__.py')
    filename.write('__cn__ = "test"')
    ret = main((str(filename), '--parent-dir', 'testdir'))
    assert ret == 0


def test_init_parrent_dir_bad(tmpdir):
    filename = tmpdir.mkdir('testdir1').join('__init__.py')
    filename.write('__cn_ = "test"')
    ret = main((str(filename), '--parent-dir', 'testdir'))
    assert ret == 0
