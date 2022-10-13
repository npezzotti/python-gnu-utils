import os
import sys


def find_files(name, dir='.'):
    with os.scandir(dir) as files:
        for file in files:
            if file.name == name:
                path = os.path.join(dir, name)
                yield os.path.normpath(os.path.abspath(path))

def get_path_dirs():
    path = os.getenv('PATH')
    
    return path.split(';') if sys.platform.startswith('win32') else path.split(':')

def main(args):
    dirs = get_path_dirs()

    results = []
    for dir in dirs:
        for file in find_files(args.program, dir):
            results.append(file)

    if not results:
        sys.exit(1)
    
    if args.a and not args.s:
        for res in results:
            print(res)
    elif not args.s:
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
