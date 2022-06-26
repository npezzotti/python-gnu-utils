import os


class Tree:
    def __init__(self, include_all=False):
        self.include_all = include_all
        self.dir_count = 0
        self.file_count = 0

    def increment_stats(self, absolute):
        if os.path.isdir(absolute):
            self.dir_count += 1
        else:
            self.file_count += 1

    def summary(self):
        return str(self.dir_count) + " directories, " + str(self.file_count) + " files"

    def walk(self, directory, prefix=""):
        filepaths = sorted([filepath for filepath in os.listdir(directory)])

        for index in range(len(filepaths)):
            absolute = os.path.join(directory, filepaths[index])
            self.increment_stats(absolute)

            if not self.include_all and filepaths[index][0] == ".":
                continue

            if index == len(filepaths) - 1:
                print(prefix + "└── " + filepaths[index])

                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + "    ")
            else:
                print(prefix + "├── " + filepaths[index])
                if os.path.isdir(absolute):
                    self.walk(absolute, prefix + "│   ")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='List the contents of a directory in a tree-like format')

    parser.add_argument('directory', nargs='?', default='.',
                        help='Starting directory')
    parser.add_argument('-a', help="All files are listed.",
                        action="store_true")
    parser.add_argument('-d', help="List directories only.",
                        action="store_true")

    args = parser.parse_args()

    tree = Tree(include_all=args.a)
    tree.walk(args.directory)
    print("\n" + tree.summary())
