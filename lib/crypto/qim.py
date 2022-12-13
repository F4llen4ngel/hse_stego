import cv2
from lib.crypto.encoder import encode_bytes, decode_bytes

def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:
    """Encodes data into given cv2 image using QIM steganography method.

    Args:
        image (cv2.Mat): cv2 image to encode data in
        data (bytes): data to encode

    Returns:
        cv2.Mat: cv2 image with encoded datas
    """
    pass


def decode_data(image: cv2.Mat) -> bytes:
    """Decodes data from given cv2 image using QIM steganography method.

    Args:
        image (cv2.Mat): image to decode data from

    Returns:
        bytes: decoded data
    """
    pass