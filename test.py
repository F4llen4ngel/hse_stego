from lib.steganography import Stego


stg = Stego()
stg.load_image("putin.png")
stg.encode_data(b"my preZident", "pm1")
print(stg.decode_data("pm1"))
stg.save_image("enc_putin.png")
stg.load_image("enc_putin.png")
print(stg.decode_data("pm1"))