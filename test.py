import lib.crypto.lsb
from PIL import Image

from lib.crypto.encoder import encode_bytes, decode_bytes

img = Image.open("test.png")
encoded_image = lib.crypto.lsb.encode_data(Image.open("test.png"), b"huesos")
decoded_data = lib.crypto.lsb.decode_data(encoded_image)
encoded_image.save("enc.png")
print(decoded_data)