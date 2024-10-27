# LAB về DES và 3DES

Trong bài lab này, bạn sẽ được biết các sử dụng website, python để đổi từ plaintext sang cipher text ra sao. Ngoài ra, bạn sẽ được demo thực tế cách mã hóa file ngân hàng như thế nào (liên hệ về chapter2, chapter4).

## Các đường link tham khảo

- Link github toàn bộ bài Lab:
- Link website: [anycript.com](https://anycript.com/crypto/)

## Làm việc trên website

Trên website, ta sẽ được làm quen với các thao tác cơ bản như nhập liệu, chọn chế độ và hiểu rõ bản chất những hành động ta làm.

### Hiểu rõ những điều đang hiển thị trên ảnh dưới đây

1. **Secret Key:**
    - This is the cryptographic key used for encryption and decryption in the DES algorithm. The secret key is a 64-bit value (56 bits of effective key length and 8 bits for parity checking).

2. **Encryption Mode:**
    - **CBC (Cipher Block Chaining):** This is a mode of operation for block ciphers, where each block of plaintext is XORed with the previous ciphertext block before encryption.
    - **ECB (Electronic Codebook):** This is a mode of operation where each block of plaintext is encrypted independently, resulting in the same ciphertext blocks for the same plaintext blocks.
        - Điều này có nghĩa là nếu hai khối plaintext giống nhau, chúng sẽ cho ra cùng một khối ciphertext (dữ liệu đã được mã hóa).

3. **IV (Initialization Vector) chỉ có trong CBC:**
    - IV chỉ được sử dụng trong chế độ mã hóa CBC (Cipher Block Chaining), không phải trong chế độ ECB (Electronic Codebook).
    - IV là một tham số tùy chọn, nhưng nếu sử dụng CBC thì việc cung cấp IV là cần thiết để đảm bảo an toàn.
    - IV phải là một giá trị 64-bit và được kết hợp với khối dữ liệu plaintext đầu tiên để cung cấp thêm tính bảo mật.
    - Khi nhập IV, cần đảm bảo nó được nhập ở dạng UTF-8, để tránh xảy ra lỗi khi giải mã.

4. **Output Format:**
    - **Base64:** This is a binary-to-text encoding scheme that represents binary data in an ASCII string format.
    - **HEX:** This is a hexadecimal representation of the encrypted data, where each byte is represented by two hexadecimal digits (0-9, A-F).

**For example**, if you have a plaintext message "Hello, World!" and a secret key of "0123456789ABCDEF", you can encrypt it using the DES algorithm in CBC mode with an IV of "FEDCBA9876543210". The resulting ciphertext in Base64 format might be something like "oBZVFTU/VitbwktaXg==", and in HEX format, it might be "A08655153535B2B5DAD24E".

## Encrypt và Decrypt với DES

### Encryption

- **Secret Key:** 0123456789ABCDEF
- **Encryption Mode:** CBC
- **IV (optional):** FEDCBA9876543210
- **Output format:** Base64
- **Ciphertext:** zCysUH9MqH5x1Rtw1K+qVA==

### Decryption

- **Encrypted Text:** zCysUH9MqH5x1Rtw1K+qVA==
- **Secret Key:** 0123456789ABCDEF
- **Encryption Mode:** CBC (Cipher Block Chaining)
- **IV (optional):** FEDCBA9876543210
- **Output format:** Base64
- **Plaintext:** Hello, World!

## Encrypt và Decrypt với 3DES

### Encryption

- **Plaintext:** "Hello, World!"
- **Secret Key:** "0123456789ABCDEF"
- **Encryption Mode:** CBC (Cipher Block Chaining)
- **Output format:** Base64
- **Ciphertext:** 3Sx0odVpCpZBzbSJVe9DuA==

### Decryption

- **Encrypted Text:** 3Sx0odVpCpbc8tmVzp46lA==
- **Secret Key:** "0123456789ABCDEF"
- **Encryption Mode:** CBC (Cipher Block Chaining)
- **IV (optional):** "12345678"
- **Output format:** Base64
- **Plaintext:** Hello, World!

## Làm việc với Python

### Thư viện cần tải

- Thư viện crypto: `pip install cryptography` hoặc `pip install pycryptodome`
  
  **LOẠI BỎ:** `pip install crypto` vì đã hết được sử dụng.

- Nếu có lỗi xuất hiện, bạn có thể dùng câu lệnh `pip install --upgrade setuptools` và sau đó cài đặt lại bình thường.

### Loại mã hóa

- **DES**
- **3DES**

### TestCase thực tế

- Thư viện cần tải: `pip install pyDes`
- **Mục tiêu hướng đến:** hiểu được tại sao trên thực tế lại cần phải làm điều này, cũng như là xem được file text thực tế khi chuyển nó sẽ như thế nào bằng cách sử dụng python và một ứng dụng đăng nhập nhỏ.
