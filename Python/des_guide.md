
# Hướng dẫn sử dụng DES trong Python

## Giới thiệu
DES (Data Encryption Standard) là một thuật toán mã hóa cổ điển sử dụng khóa 56-bit để mã hóa dữ liệu. Bài viết này hướng dẫn bạn cách mã hóa và giải mã văn bản bằng DES trong Python.

## Cài đặt thư viện cần thiết
Để sử dụng mã hóa DES, bạn cần cài đặt thư viện `pycryptodome`. Bạn có thể cài đặt bằng lệnh sau:
```bash
pip install pycryptodome
```

## Mã hóa văn bản bằng DES
Dưới đây là hàm để mã hóa văn bản bằng DES với chế độ CBC hoặc ECB.

```python
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
```

## Các tham số hàm `encrypt_des`
- **text**: Văn bản bạn muốn mã hóa.
- **key**: Khóa bí mật có độ dài 8 bytes.
- **output_format**: Định dạng đầu ra của văn bản đã mã hóa (`Base64` hoặc `HEX`).

## Giải mã văn bản bằng DES
Bạn có thể tạo một hàm giải mã tương tự để phục hồi văn bản gốc từ văn bản đã mã hóa.

```python
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
decrypted_text = decrypt_des(encrypted_text, key, output_format)
print("Decrypted:", decrypted_text)
```

## Kết luận
Bài viết này đã hướng dẫn bạn cách mã hóa văn bản bằng DES trong Python. Hãy thực hành và áp dụng cho các dự án của bạn!

Nếu bạn cần thêm thông tin về bất kỳ phần nào khác, hãy cho tôi biết!
