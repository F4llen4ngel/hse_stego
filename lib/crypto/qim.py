import cv2
from lib.crypto.encoder import encode_bytes, decode_bytes

def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:
    """Encodes data into given cv2 image using QIM steganography method.

    Args:
        image (cv2.Mat): cv2 image to encode data in
        data (bytes): data to encode

    Returns:
        cv2.Mat: cv2 image with encoded data
    """
    height, width, _ = image.shape
    assert height * width >= len(data), "[ERROR]: Can't encode data: image is too small."

    data = encode_bytes(data)
    for i in range((len(data) + width - 1) // width):
        for j in range(10):
            pass


def decode_data(image: cv2.Mat) -> bytes:
    """Decodes data from given cv2 image using QIM steganography method.

    Args:
        image (cv2.Mat): image to decode data from

    Returns:
        bytes: decoded data
    """
    pass