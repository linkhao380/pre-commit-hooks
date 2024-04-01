from __future__ import annotations

import argparse
import os
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    # reg = re.compile(args.pattern)
    retval = 0
    for filename in args.filenames:
        print('--------------------------------------------------------------')
        print(f'checking "{filename}" ---------------------------------------')
        # 判断上级目录是否是 tests
        current_path = filename
        is_parent_directories_tests = False
        while True:
            # path = Path(filename)
            current_path, current_folder = os.path.split(current_path)
            if not current_folder:
                # 如果当前文件夹为空，表示已经到达根目录
                break
            if current_folder == 'tests':
                is_parent_directories_tests = True
                break
            else:
                continue
        if is_parent_directories_tests is False:
            print('not start with tests, pass')
        # 判断是否是 __init__.py 文件 且上级目录有 tests
        base = os.path.basename(filename)
        if base == '__init__.py' and is_parent_directories_tests:
            with open(filename) as fp:
                if not fp.readline().startswith('__cn__'):
                    retval = 1
                    print(f'"{filename}" not add __cn__ comment')
        print('--------------------------------------------------------------')
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
