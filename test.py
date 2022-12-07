from lib.steganography import Stego


stg = Stego()
stg.load_image("test.png")
stg.encode_data(b"amogus")
print(stg.decode_data())
stg.save_image("enc.png")
stg.load_image("enc.png")
print(stg.decode_data())
