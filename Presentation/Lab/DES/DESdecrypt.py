from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import binascii
from base64 import b64decode

def decrypt_des(encrypted_text, key, input_format='Base64'):
    # Đảm bảo key có độ dài 8 byte cho DES
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long.")

    # Chuyển đổi dữ liệu đầu vào về dạng bytes
    if input_format == 'Base64':
        encrypted_bytes = b64decode(encrypted_text)
    elif input_format == 'HEX':
        encrypted_bytes = binascii.unhexlify(encrypted_text)
    else:
        raise ValueError("Unsupported input format! Use 'Base64' or 'HEX'.")

    # Khởi tạo đối tượng cipher
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)

    # Giải mã
    decrypted_padded = cipher.decrypt(encrypted_bytes)

    # Bỏ padding
    decrypted_text = unpad(decrypted_padded, DES.block_size)

    return decrypted_text.decode('utf-8')

# Ví dụ sử dụng
encrypted_text = "Bw�;r��+��Q~��7�q��&��"
key = "12345678"  # Khóa 8-byte cho DES
output_format = "Base64"  # Hoặc HEX

decrypted_text = decrypt_des(encrypted_text, key, output_format)
print("Decrypted:", decrypted_text)