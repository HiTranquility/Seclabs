
# Hướng Dẫn Mã Hóa và Giải Mã Dữ Liệu Sử Dụng Triple DES trong Python

## Giới Thiệu
Triple DES (3DES) là một thuật toán mã hóa đối xứng, sử dụng ba lần mã hóa DES để bảo mật dữ liệu. Trong hướng dẫn này, chúng ta sẽ sử dụng thư viện `pycryptodome` để mã hóa và giải mã dữ liệu bằng 3DES. Mã nguồn dưới đây bao gồm các chức năng để mã hóa và giải mã, cùng với ví dụ sử dụng.

## Yêu Cầu
- Thư viện `pycryptodome` phải được cài đặt. Bạn có thể cài đặt nó bằng lệnh:
  ```bash
  pip install pycryptodome
  ```

## Mã Nguồn

### Hàm Giải Mã Dữ Liệu
```python
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
decrypted_text = "l+Ftfdzl3LLqibrqyyL5dE5SL6mq0Tug"  # Replace with actual encrypted Base64 or HEX text
key = "0123456789ABCDEF01234567"  # 24-byte key
iv = "12345678"  # 8-byte IV (for CBC mode)
mode = 'CBC'  # Choose 'CBC' or 'ECB'
input_format = 'Base64'  # Choose 'Base64' or 'HEX'

try:
    decrypted_text = decrypt_3des(decrypted_text, key, mode, iv, input_format)
    print("Decrypted:", decrypted_text)
except Exception as e:
    print("Error:", e)
```

### Giải Thích Hàm Mã Hóa
- **Tham số `plaintext`**: Chuỗi văn bản cần mã hóa.
- **Tham số `key`**: Khóa dùng để mã hóa, phải có độ dài 16 hoặc 24 byte.
- **Tham số `mode`**: Chế độ mã hóa, có thể là 'CBC' hoặc 'ECB'.
- **Tham số `iv`**: (Chỉ áp dụng cho chế độ CBC) giá trị khởi tạo cần thiết cho mã hóa.
- **Tham số `output_format`**: Định dạng đầu ra, có thể là 'Base64' hoặc 'HEX'.
- **Quá trình**:
  1. Kiểm tra độ dài của khóa.
  2. Chuyển đổi dữ liệu đầu vào thành bytes.
  3. Tạo đối tượng cipher với chế độ đã chọn.
  4. Thực hiện padding cho dữ liệu trước khi mã hóa.
  5. Mã hóa dữ liệu và trả về ở định dạng yêu cầu.

## Kết Luận
Bằng cách sử dụng thư viện `pycryptodome`, bạn có thể dễ dàng mã hóa và giải mã dữ liệu bằng Triple DES trong Python. Đảm bảo rằng khóa bạn sử dụng luôn có độ dài 16 hoặc 24 byte và IV được cung cấp cho chế độ CBC.

---
