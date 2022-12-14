import cv2

from lib.crypto.encoder import encode_bytes, decode_bytese


def get_values_diff(image: cv2.Mat) -> list:
    """Calculates pixel values differense array for following calculations.

    Args:
        image (cv2.Mat): image to encode data in

    Returns:
        list: pixels values diff array 
    """
    height, width, _ = image.shape
    w = []
    for p in range(1, height * width, 2):
        p0 = image[(p - 1) // width, (p - 1) % width][2]
        p1 = image[p // width, p % width][2]
        w.append(p0 - p1)
    return w


def get_w(diffs: list) -> list:
    """Calculates w_i array for following calculations.

    Args:
        diffs (list): pixel values differense array

    Returns:
        list: w_i array
    """
    w = []
    for i in diffs:
        if 0 <= i <= 7:
            w.append(3)
        elif 8 <= i <= 15:
            w.append(3)
        elif


def max_data_length(image: cv2.Mat) -> int:
    """Calculates max data length that can be encoded into given image.

    Args:
        image (cv2.Mat): image to encode data in

    Returns:
        int: max encoded data length
    """
    pass


def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:
    """Encodes data into given image using PVD steganography method.

    Args:
        image (cv2.Mat): image to encode data in
        data (bytes): data to encode

    Returns:
        cv2.Mat: image with encoded data
    """
    height, width, _ = image.shape
    data = encode_bytes(data)

    assert max_data_length(image) >= len(data) + 1
    

    pass


def decode_data(image: cv2.Mat) -> bytes:
    """Decodes data from given image using PVD steganography method.

    Args:
        image (cv2.Mat): image to decode data from

    Returns:
        bytes: decoded data
    """
    pass