import argparse
from typing import List


def main(makefile: str, dependencies: List[str]):
    print(makefile)
    print(dependencies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='entrypoint script for Makefile Build Target Finder')
    parser.add_argument('makefile', type=str, default='Makefile')
    parser.add_argument('dependencies', nargs='+', type=str)
    args = parser.parse_args()

    main(args.makefile, args.dependencies)
