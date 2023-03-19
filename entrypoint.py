import argparse
import os.path
import re
import sys
from typing import List, Set, Dict

REGEX_TARGET_AND_PREREQS = re.compile(r'^(?P<target>(?:[^:\t\s])+)\s*:(?P<prerequisites>[^=].*)?$')
REGEX_SPACES = re.compile(r'\s')


def validate_inputs(makefile: str, dependencies: List[str]) -> bool:
    ok: bool = True
    if not os.path.exists(makefile):
        print(f'Argument Error: {makefile} is not found')
        ok &= False
    return ok


def parse_makefile(contents: str) -> Dict[str, List[str]]:
    d: Dict[str, List[str]] = {}
    for line in contents.split('\n'):
        if m := REGEX_TARGET_AND_PREREQS.match(line):
            t = m.group('target').strip()
            d[t] = REGEX_SPACES.split(m.group('prerequisites').strip())
    return d


def search(req: str, d: Dict[str, List[str]]) -> Set[str]:
    # 計算量が大きいのでボトルネックになりうる
    r: Set[str] = {k for k, v in d.items() if req in v}
    x: Set[str] = set()
    for i in r:
        x |= search(i, d)
    return r | x


def search_targets_from_dependencies(parse_makefile_data: Dict[str, List[str]], dependencies: List[str]) -> Set[str]:
    return set.union(*[search(dep, parse_makefile_data) for dep in dependencies])


def main(makefile: str, dependencies: List[str]):
    if not validate_inputs(makefile, dependencies):
        sys.exit(1)
    with open(makefile, 'r') as f:
        parse_makefile_data = parse_makefile(f.read())
    print(' '.join(search_targets_from_dependencies(parse_makefile_data, dependencies)))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='entrypoint script for Makefile Build Target Finder')
    argparser.add_argument('makefile', type=str, default='Makefile')
    argparser.add_argument('dependencies', nargs='+', type=str)
    args = argparser.parse_args()

    main(args.makefile, args.dependencies)
