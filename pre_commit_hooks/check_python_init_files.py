from __future__ import annotations

import argparse
import os
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    parser.add_argument(
        '--parent-dir',
        dest='parent_dir',
        action='store',
        default='tests',
        help='需要检查文件的父级目录',
    )
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:

        # 检查文件的目录路径
        filename_dir_path = os.path.dirname(filename)
        # 需要上级目录的路径
        parent_dir_path = os.path.abspath(
            os.path.join(filename_dir_path, os.pardir, args.parent_dir),
        )
        # 判断上级目录是否是 tests
        print('filename_dir_path:', filename_dir_path)
        print('parent_dir_path:', parent_dir_path)
        if os.path.commonpath(
                [filename_dir_path, parent_dir_path],
        ).__contains__(args.parent_dir):
            is_parent_directories_tests = True
        else:
            is_parent_directories_tests = False
        # 判断是否是 __init__.py 文件 且上级目录有 tests
        base = os.path.basename(filename)
        if base == '__init__.py' and is_parent_directories_tests:
            with open(filename, encoding='utf-8') as fp:
                if not fp.readline().startswith('__cn__'):
                    retval = 1
                    print(f'"{filename}" not found __cn__ const definition')
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
