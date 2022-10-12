import os
import sys


def find_files(name, start='.'):
    for relpath, _, files in os.walk(start):
        if name in files:
            path = os.path.join(relpath, name)
            yield os.path.normpath(os.path.abspath(path))

def get_path_dirs():
    path = os.getenv('PATH')
    
    return path.split(';') if sys.platform.startswith('win32') else path.split(':')

def main(args):
    dirs = get_path_dirs()

    result = ''
    for dir in dirs:
        for file in find_files(args.program, dir):
            if args.a and not args.s:
                print(file)
            else:
                result = file
                break
        if result:
            break

    if not result:
        sys.exit(1)
    
    if not args.s:
        print(result)
    
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
