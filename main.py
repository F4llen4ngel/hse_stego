from lib.steganography import Stego
import sys
from os.path import exists

def print_usage():
    usage_msg = """
    usage: python3 main.py --file=$filename$ --method=$method$ --decode
           python3 main.py --file=$filename$ --method=$method$ --encode $data$
    $filename$: [filename of PNG picture]
    $method$: [lsb, pm1, qmi]
    $data$: [bytes]
    """
    print(usage_msg)


def parse_args():
    """Checks kwargs and returns parsed data to main.

    Returns:
        _type_: tuple
    """
    args = []
    for arg in sys.argv[1:]:
        args += arg.split('=')
    methods = ("lsb", "pm1", "qmi")

    # decode request 
    if len(args) == 5 and args[4] == "--decode" and args[0] == "--file" and exists(args[1]) and args[2] == "--method" and args[3] in methods:
        return "decode", args[1], args[3]

    # encode request
    if len(args) == 6 and args[4] == "--encode" and args[0] == "--file" and exists(args[1]) and args[2] == "--method" and args[3] in methods:
        return "encode", args[1], args[3], args[5].encode("utf-8")

    # bad request
    print_usage()
    exit(0)


def main():
    stg = Stego()
    args = parse_args()
    
    if args[0] == "decode":
        stg.load_image(args[1])
        print(stg.decode_data(args[2]))
    elif args[0] == "encode":
        stg.load_image(args[1])
        stg.encode_data(args[3], args[2])
        stg.save_image(args[1])
        print(f"Encoded data into {args[1]}.")


if __name__ == "__main__":
    main()
