from lib.steganography import Stego


stg = Stego()
stg.load_image("test.png")
stg.encode_data(b"amogus")
print(stg.decode_data())
stg.save_image(".")
stg.load_image("enc_test.png")
print(stg.decode_data())
print(stg.image.format)