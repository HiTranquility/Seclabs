from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from base64 import b64encode
import binascii

def encrypt_des(text, key, output_format='Base64'):
    # Đảm bảo key có độ dài 8 byte cho DES
    if len(key) != 8:
        raise ValueError("Key must be 8 bytes long.")

    # Khởi tạo đối tượng cipher
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)

    # Pad dữ liệu trước khi mã hóa
    padded_text = pad(text.encode('utf-8'), DES.block_size)

    # Mã hóa
    encrypted_bytes = cipher.encrypt(padded_text)

    # Chọn định dạng đầu ra
    if output_format == 'Base64':
        return b64encode(encrypted_bytes).decode('utf-8')
    elif output_format == 'HEX':
        return binascii.hexlify(encrypted_bytes).decode('utf-8')
    else:
        raise ValueError("Unsupported output format! Use 'Base64' or 'HEX'.")

# Ví dụ sử dụng
plaintext = "Hello"
key = "12345678"  # Khóa 8-byte cho DES
output_format = "Base64"  # Hoặc HEX

encrypted_text = encrypt_des(plaintext, key, output_format)
print("Encrypted:", encrypted_text)