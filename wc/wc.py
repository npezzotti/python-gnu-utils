import argparse
import os
import sys

__version__ = '1.0.0'

def wc(txt, file=''):
    num_words = num_lines = num_chars = num_bytes = line_length = 0

    for line in txt:        
        num_lines += 1
        num_words += len(line.split())
        num_chars += len(line)
        num_bytes += len(bytes(line, 'utf-8'))
        if len(line) > line_length:
            line_length = len(line)

    if not any([args.bytes, args.chars, args.lines, args.words, args.max_line_length]):
        return print(num_lines, num_words, num_bytes, line_length, file)

def read_files_from(files_from):
    try:
        with open(files_from) as file_from:
            files = file_from.read().split('\0')
            for file in files:
                with open(file) as f:
                    wc(f, file)
    except FileNotFoundError as e:
        print('{}: {}'.format(e.filename, e.strerror))
        sys.exit()

def main(args):

    if args.files0_from:
        if args.FILE:
            print(
                "extra operand {}\nfile operands cannot be combined"
                "with --files0-from\nTry 'wc --help' for more information."
                .format(args.FILE[0])
            )
            sys.exit()
        
        if args.files0_from == '-':
            files_from = sys.stdin.read().split()
            for file in files_from:
                read_files_from(file)
            return
        else:
            return read_files_from(args.files0_from)

    if not args.FILE:
        return wc(sys.stdin)

    for file in args.FILE:
        try:
            with open(file, 'r') as f:
                wc(f, file)
        except FileNotFoundError as e:
            print('{}: {}'.format(e.filename, e.strerror))
            sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Print newline, word, and byte counts for each FILE, "
                    "and a total line if more than one FILE is specified. "
                    "A word is a non-zero-length sequence of characters delimited by white space. "
                    "With no FILE, or when FILE is -, read standard input."
    )

    parser.add_argument('FILE', nargs=argparse.REMAINDER, default=argparse.SUPPRESS)
    parser.add_argument('-c', '--bytes', action='store_true', help="print the byte counts")
    parser.add_argument('-m', '--chars', action='store_true', help="print the character counts")
    parser.add_argument('-l', '--lines', action='store_true', help="print the newline counts")
    parser.add_argument(
        '--files0-from',
        metavar='', 
        help="read input from the files specified by NUL-terminated names in file; If value is - then read names from standard input"
    )
    parser.add_argument('-L', '--max-line-length', action='store_true', help="print the maximum display width")
    parser.add_argument('-w', '--words', action='store_true', help="print the word counts")
    parser.add_argument('--version', action='version', version='%(prog)s: {}'.format(__version__))
    
    args = parser.parse_args()
    print(args)

    main(args)
