from lib.steganography import Stego


stg = Stego()
stg.load_image("putin.png")
stg.encode_data(b"some based text", "qim")
print(stg.decode_data("qim"))
stg.save_image("enc_putin.png")
stg.load_image("enc_putin.png")
print(stg.decode_data("qim"))