from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
from base64 import b64decode
import binascii

def decrypt_3des(encrypted_text, key, mode='CBC', iv=None, input_format='Base64'):
    # Ensure the key is 16 or 24 bytes for 3DES
    if len(key) not in [16, 24]:
        raise ValueError("Key must be 16 or 24 bytes long.")

    # Convert input data to bytes
    if input_format == 'Base64':
        # Ensure proper padding for Base64
        missing_padding = len(encrypted_text) % 4
        if missing_padding:
            encrypted_text += '=' * (4 - missing_padding)
        encrypted_bytes = b64decode(encrypted_text)
    elif input_format == 'HEX':
        encrypted_bytes = binascii.unhexlify(encrypted_text)
    else:
        raise ValueError("Unsupported input format! Use 'Base64' or 'HEX'.")

    # Initialize cipher object
    if mode == 'CBC':
        if iv is None:
            raise ValueError("IV is required for CBC mode.")
        cipher = DES3.new(key.encode('utf-8'), DES3.MODE_CBC, iv.encode('utf-8'))
    elif mode == 'ECB':
        cipher = DES3.new(key.encode('utf-8'), DES3.MODE_ECB)
    else:
        raise ValueError("Unsupported mode! Use 'CBC' or 'ECB'.")

    # Decrypt and remove padding
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted_text = unpad(decrypted_padded, DES3.block_size)

    return decrypted_text.decode('utf-8')

# Example usage for decryption
encrypted_text = "l+Ftfdzl3LLqibrqyyL5dE5SL6mq0Tug"  # Replace with actual encrypted Base64 or HEX text
key = "0123456789ABCDEF01234567"  # 24-byte key
iv = "12345678"  # 8-byte IV (for CBC mode)
mode = 'CBC'  # Choose 'CBC' or 'ECB'
input_format = 'Base64'  # Choose 'Base64' or 'HEX'

try:
    decrypted_text = decrypt_3des(encrypted_text, key, mode, iv, input_format)
    print("Decrypted:", decrypted_text)
except Exception as e:
    print("Error:", e)
