from PIL import Image
from math import ceil

from lib.crypto.encoder import encode_bytes, decode_bytes


def encode_data_zero(image: Image.Image, data: bytes) -> Image.Image:
    """
    Encodes given data into PIL image using lsb steganography method. Fills unused pixels with 0.

    Args:
        image (Image): PIL image to encode data in.
        data (bytes): data to encode into image.

    Returns:
        Image: PIL image with encoded data inside.
    """
    height, width = image.size
    data = "0" + encode_bytes(data)

    assert height * width >= len(data), "[ERROR]: Can't encode data: image is too small."

    for i in range(height):
        for j in range(width):
            cur_pixel = image.getpixel((i, j))
            if i * width + j < len(data):
                encoded_pixel = (cur_pixel[0], cur_pixel[1],
                                 (cur_pixel[2] | 1) & int("1" * 8 + data[i * width + j], 2))
            elif i * width + j == len(data):
                encoded_pixel = (cur_pixel[0], cur_pixel[1],
                                 cur_pixel[2] | 1)
            else:
                encoded_pixel = (cur_pixel[0], cur_pixel[1],
                                 cur_pixel[2] & int("1" * 8 + "0", 2))
            image.putpixel((i, j), encoded_pixel)

    return image


def encode_data_double(image: Image.Image, data: bytes) -> Image.Image:
    """
    Encodes given data into PIL image using lsb steganography method. Marks used pixels using additional bit.

    Args:
        image (Image): PIL image to encode data in.
        data (bytes): data to encode into image.

    Returns:
        Image: PIL image with encoded data inside.
    """
    height, width = image.size
    data = "1" + encode_bytes(data)

    assert height * width + 1 >= len(data), "[ERROR]: Can't encode data: image is too small."

    for i in range(ceil(len(data) / width)):
        for j in range(min(width, len(data) - width * i)):
            cur_pixel = image.getpixel((i, j))
            encoded_pixel = (cur_pixel[0], cur_pixel[1],
                         (cur_pixel[2] | int('11', 2)) & int("1" * 8 + data[i * width + j], 2))
            image.putpixel((i, j), encoded_pixel)

    ending_pixel = image.getpixel(((len(data) + 1) // width, (len(data) + 1) % width))
    encoded_pixel = (ending_pixel[0], ending_pixel[1],
                     ending_pixel[2] & int("1" * 7 + "01", 2))

    image.putpixel(((len(data) + 1) // width, (len(data) + 1) % width), encoded_pixel)

    return image


def encode_data(image: Image.Image, data: bytes) -> Image.Image:
    """
    Encodes given data into PIL image using lsb steganography method.

    Args:
        image (Image): PIL image to encode data in.
        data (bytes): data to encode into image.

    Returns:
        Image: PIL image with encoded data inside.
    """
    if len(encode_bytes(data)) * 2 < image.size[0] * image.size[1]:
        return encode_data_double(image, data)
    return encode_data_zero(image, data)


def decode_data_double(image: Image.Image) -> bytes:
    """
    Decodes data from PIL image using lsb steganography method. Decodes method with bit marking.

    Args:
        image (Image): PIL image to decode data from.

    Returns:
        bytes: decoded data.
    """
    height, width = image.size

    data = ""

    for i in range(height):
        for j in range(width):
            cur_pixel = image.getpixel((i, j))
            if (cur_pixel[2] // 2) % 2 == 0:
                return decode_bytes(data[1:])
            data += str(cur_pixel[2] % 2)


def decode_data_zero(image: Image.Image) -> bytes:
    """
    Decodes data from PIL image using lsb steganography method. Decodes method with zero filling.

    Args:
        image (Image): PIL image to decode data from.

    Returns:
        bytes: decoded data.
    """
    height, width = image.size

    data = ""

    for i in range(height):
        for j in range(width):
            cur_bit = image.getpixel((i, j))[2] % 2
            data += str(cur_bit)

    data = data[1:data.rfind("1")]

    return decode_bytes(data)


def decode_data(image: Image.Image) -> bytes:
    """
    Decodes data from PIL image using lsb steganography method.

    Args:
        image (Image): PIL image to decode data from.

    Returns:
        bytes: decoded data.
    """

    method = image.getpixel((0, 0))[2] % 2

    if method == 0:
        return decode_data_zero(image)
    return decode_data_double(image)
