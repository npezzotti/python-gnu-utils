import os
import sys
import datetime
import grp
import pwd
import stat
import argparse

__version__ = '1.0.0'

TERSE_FMT_REG = '{n} {s} {b} {f} {u} {g} {D} {i} {h} {t} {T} {X} {Y} {Z} {W} {o}'
TERSE_FORMAT_FS = '{n} {i} {l} {t} {s} {S} {b} {f} {a} {c} {d}'
DEFAULT_FORMAT = '  File: {N!r}\n  Size: {s}\tBlocks: {b}\tIO Block: {o}\t{F}\n  Device: {D:x}h/{d:d}d\tInode: {i}\tLinks: {h}\nAccess: ({a}/{A})\tUid: ( {u}/ {U})\tGid: ( {G}/ {g})\nAccess: {x}\nModify: {y}\nChange: {z}\n Birth: {w}'
DEFAULT_FS_FORMAT = '  File: {n}\n    ID: {i} Namelen: {l} Type: {T}\nBlock size: {s} Fundamental block size: {S}\nBlocks: Total: {b} Free: {f} Available: {a}\nInodes: Total: {c} Free: {d}'

TIME_FORMAT = '%Y-%m-%d %H:%M:%S +0000'

FOLLOW_LINKS = False
PRINT_KWARGS = {'end': '\n'}
PRINT_RAW_STRING = False

FILE_TYPES = {
    stat.S_ISREG: 'regular file',
    stat.S_ISDIR: 'directory',
    stat.S_ISCHR: 'character special file',
    stat.S_ISBLK: 'block special file',
    stat.S_ISFIFO: 'fifo',
    stat.S_ISLNK: 'symbolic link',
    stat.S_ISSOCK: 'socket'
}

VALID_FILE_SPECIFIERS = {'N', 'a', 'A', 'b', 'B', 'C', 'd', 'D', 'f', 'F', 'g', 'G', 'h', 'i', 'n', 'N', 'o', 's', 't', 'T', 'u', 'U', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z'}
VALID_FS_SPECIFIERS = {'a', 'b', 'c', 'd', 'f', 'C', 'i', 'l', 'n', 's', 'S', 't','T'}

def _mk_format(fs, terse, device):
    if fs:
        return DEFAULT_FS_FORMAT if not terse else TERSE_FORMAT_FS
    if device:
        pass

    return DEFAULT_FORMAT if not terse else TERSE_FMT_REG

def get_major_dev_num(dev):
    return os.major(dev)

def get_minor_dev_num(dev):
    return os.minor(dev)

def get_file_type(mode):
    for file_type in FILE_TYPES.keys():
        if file_type(mode) == True: return FILE_TYPES[file_type]
    return '?'

def get_permission_bits(mode):
    return oct(mode)[-4:]

def mk_permission_string(mode):
    return stat.filemode(mode)

def is_device(mode):
    return stat.S_ISBLK(mode) or stat.S_ISCHR(mode)

def get_usr_name(uid):
    return pwd.getpwuid(uid).pw_name

def get_grp_name(gid):
    return grp.getgrgid(gid).gr_name

def format_time(ts):
    return datetime.datetime.fromtimestamp(ts).strftime(TIME_FORMAT)

def _get_stats(file, fs):
    try:
        stats = os.statvfs(file) if fs else os.stat(file, follow_symlinks=FOLLOW_LINKS) 
    except FileNotFoundError as e:
        print("{} {!r}".format(e.strerror, e.filename))
        sys.exit(e.errno)
    return stats

def print_stats(file, print_fmt, fs=False, terse=False):
    stats = _get_stats(file, fs)
    if not print_fmt:
        print_fmt = _mk_format(fs, terse, False) if fs else  _mk_format(fs, terse, is_device(stats.st_mode))

    format_args = {}
    if fs:
        for index, char in enumerate(print_fmt):
            if char == '{' and print_fmt[index + 1] in VALID_FS_SPECIFIERS:
                fmt_spec = print_fmt[index + 1]
                if fmt_spec == 'a':
                    format_args['a'] = stats.f_bavail
                if fmt_spec == 'b':
                    format_args['b'] = stats.f_blocks
                if fmt_spec == 'c':
                    format_args['c'] = stats.f_files
                if fmt_spec == 'd':
                    format_args['d'] = stats.f_ffree
                if fmt_spec == 'f':
                    format_args['f'] = stats.f_bfree
                if fmt_spec == 'C':
                    pass 
                if fmt_spec == 'i':
                    format_args['i'] = stats.f_fsid
                if fmt_spec == 'l':
                    format_args['l'] = stats.f_namemax
                if fmt_spec == 'n':
                    format_args['n'] = file
                if fmt_spec == 's':
                    format_args['s'] = stats.f_bsize
                if fmt_spec == 'S':
                    format_args['S'] = stats.f_frsize
                if fmt_spec == 't':
                    format_args['t'] = 'TODO'
                if fmt_spec == 'T':
                    format_args['T'] = 'TODO'
    else:
        for index, char in enumerate(print_fmt):
            if char == '{' and print_fmt[index + 1] in VALID_FILE_SPECIFIERS:
                fmt_spec = print_fmt[index + 1]

                if fmt_spec == 'a':
                    format_args['a'] = get_permission_bits(stats.st_mode)
                elif fmt_spec == 'A':
                    format_args['A'] = mk_permission_string(stats.st_mode)
                elif fmt_spec == 'b':
                    format_args['b'] = stats.st_blocks
                elif fmt_spec == 'B':
                    format_args['B'] = int(stats.st_blksize / stats.st_blocks)
                elif fmt_spec == 'C':
                    format_args['C'] = None
                elif fmt_spec == 'd':
                    format_args['d'] = stats.st_rdev if is_device(stats.st_mode) else stats.st_dev
                elif fmt_spec == 'D':
                    format_args['D'] = stats.st_rdev if is_device(stats.st_mode) else stats.st_dev
                elif fmt_spec == 'f':
                    format_args['f'] = hex(stats.st_mode)
                elif fmt_spec == 'F':
                    format_args['F'] = get_file_type(stats.st_mode)
                elif fmt_spec == 'g':
                    format_args['g'] = get_grp_name(stats.st_gid)
                elif fmt_spec == 'G':
                    format_args['G'] = stats.st_gid
                elif fmt_spec == 'h':
                    format_args['h'] = stats.st_nlink
                elif fmt_spec == 'i':
                    format_args['i'] = stats.st_ino
                elif fmt_spec == 'n':
                    format_args['n'] = file
                elif fmt_spec == 'N':
                    format_args['N'] = file
                elif fmt_spec == 'o':
                    format_args['o'] = stats.st_blksize
                elif fmt_spec == 's':
                    format_args['s'] = stats.st_size
                elif fmt_spec == 't':
                    format_args['t'] = get_major_dev_num(stats.st_rdev) if is_device(stats.st_mode) else get_major_dev_num(stats.st_dev)
                elif fmt_spec == 'T':
                    format_args['T'] = get_minor_dev_num(stats.st_rdev) if is_device(stats.st_mode) else get_minor_dev_num(stats.st_dev)
                elif fmt_spec == 'u':
                    format_args['u'] = stats.st_uid
                elif fmt_spec == 'U':
                    format_args['U'] = get_usr_name(stats.st_uid)
                elif fmt_spec == 'x':
                    format_args['x'] = format_time(stats.st_atime)
                elif fmt_spec == 'X':
                    format_args['X'] = int(stats.st_atime)
                elif fmt_spec == 'y':
                    format_args['y'] = format_time(stats.st_mtime)
                elif fmt_spec == 'Y':
                    format_args['Y'] = int(stats.st_mtime)
                elif fmt_spec == 'w':
                    format_args['w'] = format_time(stats.st_birthtime)
                elif fmt_spec == 'W':
                    try:
                        birth_time = int(stats.st_birthtime)
                    except AttributeError:
                        birth_time = 0
                    
                    format_args['W'] = birth_time
                elif fmt_spec == 'z':
                    format_args['z'] = format_time(stats.st_ctime)
                elif fmt_spec == 'Z':
                    format_args['Z'] = int(stats.st_ctime)

    print(print_fmt.format(**format_args), **PRINT_KWARGS)

def main(args):
    global FOLLOW_LINKS
    global PRINT_KWARGS
    global PRINT_RAW_STRING

    print_fmt = args.format or args.printf

    if args.dereference: 
        FOLLOW_LINKS = True
    
    if args.printf: 
        PRINT_KWARGS['end'] = ''
        PRINT_RAW_STRING = True

    for file in args.file:
        print_stats(file, print_fmt, args.file_system, args.terse)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description='Print the stats of a file')

    parser.add_argument('file', nargs='*', help='File to stat')
    parser.add_argument('--version', '-v', action='version', version=__version__)
    parser.add_argument('-L', '--dereference', help="follow links",
                        action="store_true")
    parser.add_argument('-f', '--file-system', help="display file system status instead of file status",
                        action="store_true")
    parser.add_argument('-c', '--format', help="use the specified FORMAT instead of the default; output a newline after each use of FORMAT")
    parser.add_argument('--printf', help="like --format, but interpret backslash escapes, and do not output a mandatory trailing newline; if you want a newline, include \n in FORMAT")
    parser.add_argument('-t', '--terse', help="print the information in terse form", 
                        action="store_true")
    args = parser.parse_args()

    main(args)
