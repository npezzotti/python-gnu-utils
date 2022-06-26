import argparse
from errno import ENOENT
import os
import time
import sys

from dateutil import parser


def get_local(ts):
    """Return the current time as a struct_time in local time"""
    return time.localtime(ts)


def get_utc(ts):
    """Return the current time as a struct_time in UTC"""
    return time.gmtime(ts)


def get_modified_date(file):
    """Return a struct_time representing last modified time of a file"""
    try:
        stats = os.stat(file)
        return time.localtime(stats.st_mtime)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(ENOENT)


def format_time(fmt, tm):
    """Convert a struct_time to a string in the specified format"""
    return time.strftime(fmt, tm)


def parse_date_string(dt_str):
    """Parse a date string and return a datetime.datetime object"""
    try:
        return parser.parse(dt_str)
    except parser.ParserError as e:
        print(str(e))
        sys.exit(1)


def main(args):
    """Main driver code"""
    if args.FILE:
        mtime = get_modified_date(args.FILE)
        return print(format_time(args.FORMAT, mtime))

    if args.DATEFILE:
        try:
            with open(args.DATEFILE) as f:
                for line in f.read().splitlines():
                    dt = parse_date_string(line)
                    print(dt.strftime(args.FORMAT))
            return
        except Exception:
            raise

    if args.STRING:
        dt = parse_date_string(args.STRING)
        return print(dt.strftime(args.FORMAT)) 

    now = time.time()
    t = get_utc(now) if args.utc else get_local(now)

    return print(format_time(args.FORMAT, t))


if __name__ == '__main__':

    argparser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="print or set the system date and time",
    )

    argparser.add_argument('FORMAT', nargs='?', default='%a %b %d %H:%M:%S %Y', help='format')
    argparser.add_argument('-d', '--date', dest='STRING', help="display time described by STRING, not 'now'")
    argparser.add_argument('-f', '--file', dest='DATEFILE', help="like --date; once for each line of DATEFILE")
    argparser.add_argument('-r', '--reference', dest='FILE', help="display the last modification time of FILE")
    argparser.add_argument('-u', '--utc', '--universal', action='store_true', help="print or set Coordinated Universal Time (UTC)")
    argparser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = argparser.parse_args()

    main(args)
