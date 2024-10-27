from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
from base64 import b64encode
import binascii

def encrypt_3des(plaintext, key, mode='CBC', iv=None, output_format='Base64'):
    # Ensure the key is 16 or 24 bytes for 3DES
    if len(key) not in [16, 24]:
        raise ValueError("Key must be 16 or 24 bytes long.")

    # Convert input data to bytes
    plaintext_bytes = plaintext.encode('utf-8')
    
    # Initialize cipher object
    if mode == 'CBC':
        if iv is None:
            raise ValueError("IV is required for CBC mode.")
        cipher = DES3.new(key.encode('utf-8'), DES3.MODE_CBC, iv.encode('utf-8'))
    elif mode == 'ECB':
        cipher = DES3.new(key.encode('utf-8'), DES3.MODE_ECB)
    else:
        raise ValueError("Unsupported mode! Use 'CBC' or 'ECB'.")

    # Add padding to plaintext to match block size
    padded_text = pad(plaintext_bytes, DES3.block_size)

    # Encrypt
    encrypted_bytes = cipher.encrypt(padded_text)

    # Convert result to desired format
    if output_format == 'Base64':
        encrypted_text = b64encode(encrypted_bytes).decode('utf-8')
    elif output_format == 'HEX':
        encrypted_text = binascii.hexlify(encrypted_bytes).decode('utf-8')
    else:
        raise ValueError("Unsupported output format! Use 'Base64' or 'HEX'.")

    return encrypted_text

# Example usage for encryption
plaintext = "Hello, Triple DES!"
key = "0123456789ABCDEF01234567"  # 24-byte key
iv = "12345678"  # 8-byte IV (for CBC mode)
mode = 'CBC'  # Choose 'CBC' or 'ECB'
output_format = 'Base64'  # Choose 'Base64' or 'HEX'

encrypted_text = encrypt_3des(plaintext, key, mode, iv, output_format)
print("Encrypted:", encrypted_text)