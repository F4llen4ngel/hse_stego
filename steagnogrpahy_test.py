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
    
 def test_qim():
    stg.load_image("putin.png")
    stg.encode_data(b"Hello, world!", "nmi")
    stg.save_image("putin.png")
    stg.load_image("putin.png")
    assert stg.decode_data("nmi") == b"Hello, world!"


def test_lsb_long_input():
    with pytest.raises(Exception) as e:
        stg.load_image("putin.png")
        stg.encode_data(b"Hello, world!" * 100000, "lsb")
    assert str(e.value) == "[ERROR]: Can't encode data: image is too small."


def test_pm1_long_input():
    with pytest.raises(Exception) as e:
        stg.load_image("putin.png")
        stg.encode_data(b"Hello, world!" * 100000, "pm1")
    assert str(e.value) == "[ERROR]: Can't encode data: image is too small."

def test_qim_long_input():
    with pytest.raises(Exception) as e:
        stg.load_image("putin.png")
        stg.encode_data(b"Hello, world!" * 100000, "qim")
    assert str(e.value) == "[ERROR]: Can't encode data: image is too small."

def test_qim_long_input():
    with pytest.raises(Exception) as e:
        stg.load_image("putin.png")
        stg.encode_data(b"Hello, world!" * 100000, "nmi")
    assert str(e.value) == "[ERROR]: Can't encode data: image is too small."    
