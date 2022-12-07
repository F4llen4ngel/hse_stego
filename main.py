from lib.steganography import Stego
import sys
from os.path import exists


def print_usage():
    usage_msg = """
    usage: python3 main.py --file=$filename$ --method=$method$
    --file [filename of picture]
    --method: [lsb]
    """
    print(usage_msg)


def parse_args():
    args = []
    for arg in sys.argv[1:]:
        args += arg.split('=')
    methods = ["lsb"]
    if len(args) != 4 or args[0] != '--file' or args[2] != "--method" or not exists(args[1]) or args[3] not in methods:
        print_usage()
        exit(0)
    return args[1]


def main():
    s = Stego()
    method = parse_args()
    s.load_image("test.png")
    s.encode_data(b"amongus")
    t = s.decode_data()
    print(t)


if __name__ == "__main__":
    main()
