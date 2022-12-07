from bitstring import BitArray


def encode_bytes(data: bytes) -> str:
    """
    Encodes bytes to binary string.

    Args:
        data (bytes): data to encode.

    Returns:
        str: encoded data.
    """
    return BitArray(data).bin


def decode_bytes(data: str) -> bytes:
    """
    Decodes binary string to bytes.

    Args:
        data (str): binary string to decode.

    Returns:
        bytes: decoded data.
    """
    return bytes([int(data[i:i+8], 2) for i in range(0, len(data), 8)])
