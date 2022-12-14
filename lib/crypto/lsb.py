import cv2

from lib.crypto.encoder import encode_bytes, decode_bytes



def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:
    """
    Encodes given data into cv2 image using lsb steganography method. Marks used pixels using additional bit.

    Args:
        image (cv2.Mat): cv2 image to encode data in.
        data (bytes): data to encode into image.

    Returns:
        cv2.Mat: cv2 image with encoded data inside.
    """
    height, width, _ = image.shape
    data = encode_bytes(data)
    
    assert height * width >= len(data) + 1, "[ERROR]: Can't encode data: image is too small."


    for i in range((len(data) + width - 1) // width):
        for j in range(min(width, len(data) - width * i)):
            image[i, j][2] = (image[i, j][2] | int('11', 2)) & int("1" * 8 + data[i * width + j], 2)

    # ending pixel
    image[len(data) // width, len(data) % width][2] &= int("1" * 7 + "01", 2)

    return image


def decode_data(image: cv2.Mat) -> bytes:
    """
    Decodes data from cv2 image using lsb steganography method. Decodes method with bit marking.

    Args:
        image (cv2.Mat): cv2 image to decode data from.

    Returns:
        bytes: decoded data.
    """

    height, width, _ = image.shape
    data = ""

    for i in range(height):
        for j in range(width):
            if (image[i, j][2] // 2) % 2 == 0:
                return decode_bytes(data)
            data += str(image[i, j][2] % 2)

    return b""