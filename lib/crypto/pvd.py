import cv2
from math import log2

from lib.crypto.encoder import encode_bytes, decode_bytes


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
            w.append(8)
        elif 8 <= i <= 15:
            w.append(8)
        elif 16 <= i <= 31:
            w.append(16)
        elif 32 <= i <= 63:
            w.append(32)
        elif 64 <= i <= 127:
            w.append(64)
        elif 128 <= i <= 255:
            w.append(128)
        else:
            raise ValueError("Invalid pixel value")
    return w


def get_n(w: list) -> list:
    """Calculates n_i array for following calculations.

    Args:
        w (list): w_i array

    Returns:
        list: n_i array
    """
    n = []
    for i in w:
        n.append(int(log2(i)))
    return n


def calculate_new_pixels(pixel_i: int, pixel_i_1: int, new_d: int, d: int) -> tuple:
    """Calculates new pixel values.

    Args:
        pixel_i (int): pixel value
        pixel_i_1 (int): pixel value
        new_d (int): new pixel values difference
        d (int): old pixel values difference

    Returns:
        tuple: new pixel values
    """
    if d % 2 == 1:
        new_pixel_i = pixel_i - (new_d - d + 1) // 2
        new_pixel_i_1 = pixel_i_1 + (new_d - d) // 2
    else:
        new_pixel_i = pixel_i - (new_d - d) // 2
        new_pixel_i_1 = pixel_i_1 + (new_d - d + 1) // 2
    return new_pixel_i, new_pixel_i_1


def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:
    """Encodes data into given image using PVD steganography method.

    Args:
        image (cv2.Mat): image to encode data in
        data (bytes): data to encode

    Returns:
        cv2.Mat: image with encoded data
    """
    height, width, _ = image.shape
    data = encode_bytes(data) + '1'
    print(data)
    d = get_values_diff(image)
    w = get_w(d)
    n = get_n(w)
    
    assert sum(n) >= len(data) + 1, "[ERROR]: Can't encode data: image is too small."
    
    for i in range(len(n)):
        if len(data) == 0:
            break

        chunk = data[:n[i]]
        data = data[n[i]:]
        b = int(chunk, 2)
        new_d = w[i] + b if d[i] >= 0 else w[i] - b

        # old pixel values
        pixel_i = image[i // width, i %  width][2]
        pixel_i_1 = image[(i + 1) // width, (i + 1) %  width][2]
        # new pixel values
        new_pixels = calculate_new_pixels(pixel_i, pixel_i_1, new_d, d[i])
        # write new pixel values
        image[i // width, i %  width][2] = new_pixels[0]
        image[(i + 1) // width, (i + 1) %  width][2] = new_pixels[1]

    return image


def decode_data(image: cv2.Mat) -> bytes:
    """Decodes data from given image using PVD steganography method.

    Args:
        image (cv2.Mat): image to decode data from

    Returns:
        bytes: decoded data
    """
    d = get_values_diff(image)
    w = get_w(d)
    n = get_n(w)
    data = ''
    
    for i in range(len(n)):
        b = abs(d[i]) - w[i]
        if b < 0: # тут не должно быть < 0, это ломает декодирование
            print(data)
            raise ValueError("Invalid image")
        chunk = bin(b)[2:]
        data += chunk
    print(data)
    return decode_bytes(data[:data.rfind('1')])