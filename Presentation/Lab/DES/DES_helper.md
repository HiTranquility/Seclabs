
# Hướng Dẫn Mã Hóa và Giải Mã Dữ Liệu Sử Dụng DES trong Python

## Giới Thiệu
DES (Data Encryption Standard) là một thuật toán mã hóa đối xứng được sử dụng để bảo mật dữ liệu. Trong hướng dẫn này, chúng ta sẽ sử dụng thư viện `pycryptodome` để mã hóa và giải mã dữ liệu bằng DES. Mã nguồn dưới đây bao gồm các chức năng để mã hóa và giải mã, cùng với ví dụ sử dụng.

## Yêu Cầu
- Thư viện `pycryptodome` phải được cài đặt. Bạn có thể cài đặt nó bằng lệnh:
  ```bash
  pip install pycryptodome
  ```

## Mã Nguồn

### Hàm Giải Mã Dữ Liệu
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
encrypted_text = "oVmfzWxhH88="
key = "12345678"  # Khóa 8-byte cho DES
output_format = "Base64"  # Hoặc HEX

decrypted_text = decrypt_des(encrypted_text, key, output_format)
print("Decrypted:", decrypted_text)
```

### Giải Thích Hàm Giải Mã
- **Tham số `encrypted_text`**: Chuỗi dữ liệu đã được mã hóa (ở định dạng Base64 hoặc HEX).
- **Tham số `key`**: Khóa dùng để giải mã, phải có độ dài 8 byte.
- **Tham số `input_format`**: Định dạng của dữ liệu đầu vào, có thể là 'Base64' hoặc 'HEX'.
- **Quá trình**:
  1. Kiểm tra độ dài của khóa.
  2. Chuyển đổi dữ liệu đầu vào thành bytes.
  3. Tạo đối tượng cipher với chế độ ECB.
  4. Giải mã dữ liệu và loại bỏ padding.
  5. Trả về chuỗi văn bản đã giải mã.

### Hàm Mã Hóa Dữ Liệu
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

### Giải Thích Hàm Mã Hóa
- **Tham số `text`**: Chuỗi văn bản cần mã hóa.
- **Tham số `key`**: Khóa dùng để mã hóa, phải có độ dài 8 byte.
- **Tham số `output_format`**: Định dạng đầu ra, có thể là 'Base64' hoặc 'HEX'.
- **Quá trình**:
  1. Kiểm tra độ dài của khóa.
  2. Tạo đối tượng cipher với chế độ ECB.
  3. Thực hiện padding cho dữ liệu trước khi mã hóa.
  4. Mã hóa dữ liệu và trả về ở định dạng yêu cầu.

## Kết Luận
Bằng cách sử dụng thư viện `pycryptodome`, bạn có thể dễ dàng mã hóa và giải mã dữ liệu bằng DES trong Python. Đảm bảo rằng khóa bạn sử dụng luôn có độ dài 8 byte để tránh lỗi.

---
