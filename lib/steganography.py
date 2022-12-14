import cv2
from os.path import exists
from lib.crypto import lsb, pm1, qim


class Stego:
    """
    Provides multiple steganography information encoding/decoding methods.
    """

    def __init__(self):
        self.image = None

    def load_image(self, path: str):
        """
        Loads image from given file.

        Args:
            path (str): absolute/relative path to the image
        """
        assert exists(path), "[ERROR]: can't open image. File does not exist."
        self.image = cv2.imread(path)

    def save_image(self, path: str):
        """
        Writes image to given file.

        Args:
            path (str): absolute/relative path to the file
        """
        assert self.image is not None, "[ERROR]: No image was loaded."
        cv2.imwrite(path, self.image)

    def check_method(self, method: str):
        return method in ('lsb', 'pm1', 'qim')

    def encode_data(self, data: bytes, method: str):
        """
        Encodes given data into image using specified steganography method.

        Args:
            data (bytes): data to encode
            method (str): steganography method
        """
        assert self.image is not None, "[ERROR]: image was not specified."
        assert data != b"", "[ERROR]: data can't be empty."
        assert self.check_method(method), f"[ERROR]: incorrect method. '{method}'"

        if method == 'lsb':
            self.image = lsb.encode_data(self.image, data)
        elif method == 'pm1':
            self.image = pm1.encode_data(self.image, data)
        elif method == 'qim':
            self.image = qim.encode_data(self.image, data)

    def decode_data(self, method: str) -> bytes:
        """
        Decodes data from image using specified steganography method.

        Args:
            method (str): steganography method
        """
        assert self.check_method(method), f"[ERROR]: incorrect method. '{method}'"

        data = b''

        if method == 'lsb':
            data = lsb.decode_data(self.image)
        elif method == 'pm1':
            data = pm1.decode_data(self.image)
        elif method == 'qim':
            data = qim.decode_data(self.image)

        return data
