import os
import sys


def _find_files(name, start='.'):
    for relpath, _, files in os.walk(start):
        if name in files:
            path = os.path.join(relpath, name)
            yield os.path.normpath(os.path.abspath(path))

def main(args):
    dirs = os.getenv('PATH').split(':')

    results = []
    for dir in dirs:
        files = _find_files(args.program, dir)
        for file in files:
            results.append(file)

    if not results:
        sys.exit(1)
    
    if args.s:
        pass
    elif args.a:
        for file in results:
            print(file)
    else:
        print(results[0])

    sys.exit(0)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='locate a program file in the user\'s path')

    parser.add_argument(
        'program',
        help='Program to search for'
    )
    parser.add_argument(
        '-a', 
        help="List all instances of executables found (instead of just the first one of each).", 
        action="store_true"
    )
    parser.add_argument(
        '-s', 
        help="No output, just return 0 if all of the executables are found, or 1 if some were not found.", 
        action="store_true"
    )

    args = parser.parse_args()

    main(args)
