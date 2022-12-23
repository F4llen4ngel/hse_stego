import cv2
from numpy import array
from math import log2

from lib.crypto.encoder import encode_bytes, decode_bytes

def encode_data(image: cv2.Mat, data: bytes) -> cv2.Mat:

    #Encodes given data into cv2 image using mni steganography method.

    #Args:
    #   image (cv2.Mat): cv2 image to encode data in.
    #   data (bytes): data to encode into image.

    #Returns:
    #   cv2.Mat: cv2 image with encoded data inside.


    height, width, _ = image.shape
    data = encode_bytes(data) + "1"
    max_data = 0
    exit_flag = 0

    new_image = array([[[0] * 3] * (width * 2 - 1)] * (height * 2 - 1))

    for i in range(height):
        for j in range(width):
            new_image[i * 2, j * 2] = image[i, j]

    height = height * 2 - 2
    width = width * 2 - 1


    for i in range(0, height, 2):
        for j in range(1, width, 2):
            for c in range(3):
                max_data += pix("bpp10", i, j, c)
                new_image[i, j, c] = pix("p10", i, j, c)
            for c in range(3):
                max_data += pix("bpp01", i, j, c)
                new_image[i + 1, j - 1, c] = pix("p01", i, j, c)
            for c in range(3):
                max_data += pix("bpp11", i, j, c)
                new_image[i + 1, j, c] = pix("p11", i, j, c)
            
    for i in range(0, height, 2):
        for c in range(3):
            max_data += pix("bpp01", i, width, c)
            new_image[i + 1, width - 1, c] = pix("p01", i, width, c)

    for j in range(1, width, 2):
        for c in range(3):
            max_data += pix("bpp10", height, j, c)
            new_image[height, j, c] = pix("p10", height, j, c)


    assert max_data - 1 >= len(data), "[ERROR]: Can't encode data: image is too small."


    for i in range(0, height, 2):
        for j in range(1, width, 2):
            for c in range(3):
                if 0 < pix("bpp10", i, j, c) < len(data):
                    new_image[i, j, c] = pix("p10", i, j, c) + int(data[:pix("bpp10", i, j, c)], 2)
                    data = data[pix("bpp10", i, j, c):]
                elif pix("bpp10", i, j, c) == 0:
                    new_image[i, j, c] = pix("p10", i, j, c)
                else:
                    new_image[i, j, c] = pix("p10", i, j, c) + int(data, 2)
                    exit_flag = 1
                    data = "0"
                    break
            for c in range(3):
                if 0 < pix("bpp01", i, j, c) < len(data):
                    new_image[i + 1, j - 1, c] = pix("p01", i, j, c) + int(data[:pix("bpp01", i, j, c)], 2)
                    data = data[pix("bpp01", i, j, c):]
                elif pix("bpp01", i, j, c) == 0:
                    new_image[i + 1, j - 1, c] = pix("p01", i, j, c)
                else:
                    new_image[i + 1, j - 1, c] = pix("p01", i, j, c) + int(data, 2)
                    exit_flag = 1
                    data = "0"
                    break
            for c in range(3):
                if 0 < pix("bpp11", i, j, c) < len(data):
                    new_image[i + 1, j, c] = pix("p11", i, j, c) + int(data[:pix("bpp11", i, j, c)], 2)
                    data = data[pix("bpp11", i, j, c):]
                elif pix("bpp11", i, j, c) == 0:
                    new_image[i + 1, j, c] = pix("p11", i, j, c)
                else:
                    new_image[i + 1, j, c] = pix("p11", i, j, c) + int(data, 2)
                    exit_flag = 1
                    data = "0"
                    break
            if exit_flag == 1:
                break
        if exit_flag == 1:
            break

    for i in range(0, height, 2):
        for c in range(3):
            if 0 < pix("bpp01", i, width, c) < len(data):
                new_image[i + 1, width - 1, c] = pix("p01", i, width, c) + int(data[:pix("bpp01", i, width, c)], 2)
                data = data[pix("bpp01", i, width, c):]
            elif pix("bpp01", i, width, c) == 0:
                new_image[i + 1, width - 1, c] = pix("p01", i, width, c)
            else:
                new_image[i + 1, width - 1, c] = pix("p01", i, width, c) + int(data, 2)
                exit_flag = 1
                data = "0"
                break
        if exit_flag == 1:
            break

    for j in range(1, width, 2):
        for c in range(3):
            if 0 < pix("bpp10", height, j, c) < len(data):
                new_image[height, j, c] = pix("p10", height, j, c) + int(data[:pix("bpp10", height, j, c)], 2)
                data = data[pix("bpp10", height, j, c):]
            elif pix("bpp10", height, j, c) == 0:
                new_image[height, j, c] = pix("p10", height, j, c)
            else:
                new_image[height, j, c] = pix("p10", height, j, c) + int(data, 2)
                exit_flag = 1
                data = "0"
                break
        if exit_flag == 1:
            break

    return new_image


def decode_data(image: cv2.Mat) -> bytes:

    #Decodes data from cv2 image using mni steganography method.

    #Args:
    #   image (cv2.Mat): cv2 image to decode data from.

    #Returns:
    #   bytes: decoded data.

    data = ""
    end_cnt = 0
    last_pix = [0, 0, 0, 0]
    exit_flag = 0


    for i in range(0, height, 2):
        for j in range(1, width, 2):
            for c in range(3):
                if 0 < pix("bpp10", i, j, c):
                    data += ("0" * (pix("bpp10", i, j, c) - len(pix("dp10", i, j, c))) + pix("dp10", i, j, c))
                    if new_image[i, j, c] - pix("p10", i, j, c) == 0:
                        end_cnt += pix("bpp10", i, j, c)
                        if end_cnt > 7:
                            exit_flag = 1
                            break
                    else:
                        last_pix = [i, j, c, "10"]
                        end_cnt = 0
            for c in range(3):
                if 0 < pix("bpp01", i, j, c):
                    data += ("0" * (pix("bpp01", i, j, c) - len(pix("dp01", i, j, c))) + pix("dp01", i, j, c))
                    if new_image[i + 1, j - 1, c] - pix("p01", i, j, c) == 0:
                        end_cnt += pix("bpp01", i, j, c)
                        if end_cnt > 7:
                            exit_flag = 1
                            break
                    else:
                        last_pix = [i, j, c, "01"]
                        end_cnt = 0
            for c in range(3):
                if 0 < pix("bpp11", i, j, c):
                    data += ("0" * (pix("bpp11", i, j, c) - len(pix("dp11", i, j, c))) + pix("dp11", i, j, c))
                    if new_image[i + 1, j, c] - pix("p11", i, j, c) == 0:
                        end_cnt += pix("bpp11", i, j, c)
                        if end_cnt > 7:
                            exit_flag = 1
                            break
                    else:
                        last_pix = [i, j, c, "11"]
                        end_cnt = 0
            if exit_flag == 1:
                break
        if exit_flag == 1:
            break

    for i in range(0, height, 2):
        for c in range(3):
            if 0 < pix("bpp01", i, width, c):
                data += ("0" * (pix("bpp01", i, width, c) - len(pix("dp01", i, width, c))) + pix("dp01", i, width, c))
                if new_image[i + 1, width - 1, c] - pix("p01", i, width, c) == 0:
                    end_cnt += pix("bpp01", i, width, c)
                    if end_cnt > 7:
                        exit_flag = 1
                        break
                else:
                    last_pix = [i, j, c, "01"]
                    end_cnt = 0
        if exit_flag == 1:
            break

    for j in range(1, width, 2):
        for c in range(3):
            if 0 < pix("bpp10", height, j, c):
                data += ("0" * (pix("bpp10", height, j, c) - len(pix("dp10", height, j, c))) + pix("dp10", height, j, c))
                if new_image[height, j, c] - pix("p10", height, j, c) == 0:
                    end_cnt += pix("bpp10", height, j, c)
                    if end_cnt > 7:
                        exit_flag = 1
                        break
                else:
                    last_pix = [i, j, c, "10"]
                    end_cnt = 0
        if exit_flag == 1:
            break


    last_pix_bpp = pix("bpp" + last_pix[3], last_pix[0], last_pix[1], last_pix[2])
    last_pix_dp = pix("dp" + last_pix[3], last_pix[0], last_pix[1], last_pix[2])[:-1]

    data = data[:len(data) - end_cnt - last_pix_bpp]
    if len(data) % 8 != 0:
        data = data + ("0" * (8 - len(data) % 8 - len(last_pix_dp))) + last_pix_dp


    return decode_bytes(data)

def pix(arg, i, j, c):
    if arg == "p10":
        return (new_image[i, j - 1, c] + new_image[i, j + 1, c]) // 2
    if arg == "p01":
        return (new_image[i, j - 1, c] + new_image[i + 2, j - 1, c]) // 2
    if arg == "p11":
        return (pix("p10", i, j, c) + pix("p01", i, j, c) + int(new_image[i, j - 1, c])) // 3
    if arg == "bpp10":
        return int(log2(abs(pix("p10", i, j, c) - new_image[i, j - 1, c]) + 0.9))
    if arg == "bpp01":
        return int(log2(abs(pix("p01", i, j, c) - new_image[i, j - 1, c]) + 0.9))
    if arg == "bpp11":
        return int(log2(abs(pix("p11", i, j, c) - new_image[i, j - 1, c]) + 0.9))
    if arg == "dp10":
        return format(new_image[i, j, c] - pix("p10", i, j, c), 'b')
    if arg == "dp01":
        return format(new_image[i + 1, j - 1, c] - pix("p01", i, j, c), 'b')
    if arg == "dp11":
        return format(new_image[i + 1, j, c] - pix("p11", i, j, c), 'b')