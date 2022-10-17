import os
import sys


def main(args):
    path = os.getenv('PATH')
    dirs = path.split(';') if sys.platform.startswith('win32') else path.split(':')

    results = { prog: [] for prog in args.program }
    for dir in dirs:
        with os.scandir(dir) as files:
            for file in files:
                if file.name in results and file.is_file():
                    results[file.name].append(file.path)

    exit_status = 0
    for _, files in results.items():
        if not files:
            exit_status = 1
            continue

        if args.a and not args.s:
            for f in files:
                print(f)
        elif not args.s:
            print(files[0])

    sys.exit(exit_status)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Locate a program file in the user's path",
    )

    parser.add_argument(
        'program',
        nargs='+',
        type=str,
        help='List of command names'
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
