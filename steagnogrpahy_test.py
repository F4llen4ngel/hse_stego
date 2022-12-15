import pytest

from lib.steganography import Stego


stg = Stego()


def test_lsb():
    stg.load_image("putin.png")
    stg.encode_data(b"Hello, world!", "lsb")
    stg.save_image("putin.png")
    stg.load_image("putin.png")
    assert stg.decode_data("lsb") == b"Hello, world!"

def test_pm1():
    stg.load_image("putin.png")
    stg.encode_data(b"Hello, world!", "pm1")
    stg.save_image("putin.png")
    stg.load_image("putin.png")
    assert stg.decode_data("pm1") == b"Hello, world!"

def test_qim():
    stg.load_image("putin.png")
    stg.encode_data(b"Hello, world!", "qim")
    stg.save_image("putin.png")
    stg.load_image("putin.png")
    assert stg.decode_data("qim") == b"Hello, world!"

def test_pvd():
    stg.load_image("putin.png")
    stg.encode_data(b"Hello, world!", "pvd")
    stg.save_image("putin.png")
    stg.load_image("putin.png")
    assert stg.decode_data("pvd") == b"Hello, world!"


