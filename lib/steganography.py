from PIL import Image
from os.path import exists
from lib.crypto import lsb


class Stego:
    """
    Provides multiple steganograpy information encoding/decoding methods.
    """

    def __init__(self):
        self.image = None

    def load_image(self, path: str):
        """
        Loads image from given file.

        Args:
            path (str): absolute/relative path to the image.
        """
        assert exists(path), "[ERROR]: can't open image. File does not exist."

        self.image = Image.open(path)

    def save_image(self, path: str):
        """
        Writes image to given file.

        Args:
            path (str): absolute/relative path to the image.
        """
        assert self.image is not None, "[ERROR]: No image was loaded."

        self.image.save(path)

    def encode_data(self, data: bytes, method: str = 'lsb'):
        """
        Encodes given data into image using specified steganography method (default lsb).

        Args:
            data (bytes): data to encode.
            method (str, optional): steganography method. Defaults to 'lsb'.
        """
        assert self.image is not None, "[ERROR]: image was not specified."
        assert data != b"", "[ERROR]: data can't be empty."
        assert method in ('lsb'), f"[ERROR]: incorrect method. '{method}'"

        if method == 'lsb':
            self.image = lsb.encode_data(self.image, data)

    def decode_data(self, method: str = 'lsb') -> bytes:
        """
        Decodes data from image using specified steganography method (default lsb).

        Args:
            method (str, optional): steganography method. Defaults to 'lsb'.
        """
        assert method in ('lsb'), f"[ERROR]: incorrect method. '{method}'"

        data = b''

        if method == 'lsb':
            data = lsb.decode_data(self.image)

        return data
