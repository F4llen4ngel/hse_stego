import cv2

from lib.crypto.encoder import encode_bytes, decode_bytes


def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:
    """
    Encodes given data into cv2 image using pm1 steganography method.

    Args:
        image (cv2.Mat): cv2 image to encode data in.
        data (bytes): data to encode into image.

    Returns:
        cv2.Mat: cv2 image with encoded data inside.
    """
    height, width, _ = image.shape
    data = encode_bytes(data)

    assert height * width >= len(data), "[ERROR]: Can't encode data: image is too small."

    for i in range(height):
        for j in range(width):
            if i * width + j < len(data):
                image[i, j][2] = image[i, j][2] // 2 * 2 + int(data[i * width + j])
            elif i * width + j == len(data):
                image[i, j][2] = image[i, j][2] // 2 * 2 + 1
            else:
                image[i, j][2] = image[i, j][2] // 2 * 2
    return image



def decode_data(image: cv2.Mat) -> bytes:
    """
    Decodes data from cv2 image using pm1 steganography method.

    Args:
        image (cv2.Mat): cv2 image to decode data from.

    Returns:
        bytes: decoded data.
    """
    height, width, _ = image.shape

    data = ""

    for i in range(height):
        for j in range(width):
            data += str(image[i, j][2] % 2)

    data = data[:data.rfind("1")]
    
    return decode_bytes(data)