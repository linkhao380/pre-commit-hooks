from __future__ import annotations

import argparse
import ast
import re
from typing import Any
from typing import Sequence


def check_has_author_decorator_by_ast(node: Any) -> bool:
    """判断 httprunner 类是否有 @pytest.mark.meta(author = ‘’) 装饰器"""
    has_author_decorator = False
    for decorator in node.decorator_list:
        keywords = [key.arg for key in decorator.keywords]
        try:
            if decorator.func.attr == 'meta':
                ast_name = decorator.func.value
                if ast_name.attr == 'mark':
                    if ast_name.value.id == 'pytest':
                        if 'author' in keywords:
                            has_author_decorator = True
        except AttributeError:
            continue
    return has_author_decorator


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    retval = 0
    for filename in args.filenames:
        with open(file=filename, encoding='utf-8') as source:
            content = source.read()
            tree = ast.parse(content)
            # 获取所有类和函数节点
            test_nodes = [
                node for node in ast.walk(tree)
                if isinstance(node, (ast.ClassDef, ast.FunctionDef))
            ]
            # 正则匹配所有测试类或测试函数
            test_funcs = re.findall(
                r'def\s+(test_[a-zA-Z0-9]+)\(?', content,
            )
            test_classes = re.findall(
                r'class\s+(Test[a-zA-Z0-9]+)\(?', content,
            )
            for node in test_nodes:
                if node.name in test_funcs or node.name in test_classes:
                    if not check_has_author_decorator_by_ast(node):
                        print(
                            f'{filename}:: {node.name} '
                            '没有 @pytest.mark.meta 装饰器',
                        )
                        retval = 1

    return retval


if __name__ == '__main__':
    raise SystemExit(main())
