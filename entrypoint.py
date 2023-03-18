import argparse
import os.path
import sys
from typing import List


def validate_inputs(makefile: str, dependencies: List[str]) -> bool:
    ok: bool = True
    if not os.path.exists(makefile):
        print(f'Argument Error: {makefile} is not found')
        ok &= False
    return ok


def main(makefile: str, dependencies: List[str]):
    if not validate_inputs(makefile, dependencies):
        sys.exit(1)
    with open(makefile, 'r') as f:
        print(f.read())
    print(dependencies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='entrypoint script for Makefile Build Target Finder')
    parser.add_argument('makefile', type=str, default='Makefile')
    parser.add_argument('dependencies', nargs='+', type=str)
    args = parser.parse_args()

    main(args.makefile, args.dependencies)
