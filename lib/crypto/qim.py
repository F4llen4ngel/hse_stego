import cv2
from lib.crypto.encoder import encode_bytes, decode_bytes

Q = 8

def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:
    """Encodes data into given cv2 image using QIM steganography method.

    Args:
        image (cv2.Mat): cv2 image to encode data in
        data (bytes): data to encode

    Returns:
        cv2.Mat: cv2 image with encoded data
    """
    height, width, _ = image.shape
    data = encode_bytes(data)

    assert height * width >= len(data) + 1, "[ERROR]: Can't encode data: image is too small."

    for i in range(height):
        for j in range(width):
            if i * width + j < len(data):
                image[i, j][2] = (image[i, j][2] // Q) * Q + Q//2 * int(data[i * width + j])
            elif i * width + j == len(data):
                image[i, j][2] = (image[i, j][2] // Q) * Q + Q//2
            else:
                image[i, j][2] = (image[i, j][2] // Q) * Q
    
    return image


def decode_data(image: cv2.Mat) -> bytes:
    """Decodes data from given cv2 image using QIM steganography method.

    Args:
        image (cv2.Mat): image to decode data from

    Returns:
        bytes: decoded data
    """
    height, width, _ = image.shape
    data = ""

    for i in range(height):
        for j in range(width):
            pxl0 = (image[i, j][2] // Q) * Q
            pxl1 = (image[i, j][2] // Q) * Q + Q//2
            if abs(pxl0 - image[i, j][2]) < abs(pxl1 - image[i, j][2]):
                data += "0"
            else:
                data += "1"

    return decode_bytes(data[:data.rfind("1")])