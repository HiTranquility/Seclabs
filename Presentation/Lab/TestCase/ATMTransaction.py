from pyDes import des, ECB
import os

# Thiết lập khóa DES cho mã hóa
KEY = b"ATMKEY01"  # Khóa 8 byte
des_cipher = des(KEY, ECB)

# Đường dẫn tới file lưu trữ dữ liệu mã hóa
FILE_PATH = "encrypted_accounts.txt"

# Hàm mã hóa dữ liệu tài khoản
def encrypt_data(account_number, pin, role):
    transaction_data = f"{account_number}:{pin}:{role}"
    if len(transaction_data) % 8 != 0:
        transaction_data += ' ' * (8 - len(transaction_data) % 8)
    return des_cipher.encrypt(transaction_data)

# Tạo tài khoản mẫu cho admin và user
def create_sample_accounts():
    print("Đang tạo tài khoản mẫu...")  # Thông báo kiểm tra
    admin_account_number = "admin123"
    admin_pin = "1234"
    admin_role = "admin"
    
    user_account_number = "user456"
    user_pin = "5678"
    user_role = "user"
    
    try:
        # Mã hóa dữ liệu và ghi vào file
        with open(FILE_PATH, "wb") as file:
            print(f"Đang ghi tài khoản admin vào {FILE_PATH}...")  # Kiểm tra khi ghi admin
            encrypted_admin = encrypt_data(admin_account_number, admin_pin, admin_role)
            file.write(encrypted_admin + b'\n')
            
            print(f"Đang ghi tài khoản user vào {FILE_PATH}...")  # Kiểm tra khi ghi user
            encrypted_user = encrypt_data(user_account_number, user_pin, user_role)
            file.write(encrypted_user + b'\n')
        
        print("File 'encrypted_accounts.txt' đã được tạo với tài khoản admin và user mẫu.")
    
    except Exception as e:
        print(f"Lỗi khi tạo tài khoản mẫu: {e}")

# Hàm đăng ký tài khoản mới (chỉ dành cho admin)
def register_account(account_number, pin, role):
    encrypted_data = encrypt_data(account_number, pin, role)
    # Ghi dữ liệu đã mã hóa vào file
    with open(FILE_PATH, "ab") as file:
        file.write(encrypted_data + b'\n')
    print(f"Tài khoản '{role}' đã được đăng ký thành công!")

# Hàm kiểm tra đăng nhập
def check_login(input_account, input_pin):
    encrypted_input_user = encrypt_data(input_account, input_pin, "user")
    encrypted_input_admin = encrypt_data(input_account, input_pin, "admin")
    
    # Đọc dữ liệu mã hóa từ file và kiểm tra trùng khớp
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as file:
            for line in file:
                # So sánh với mã hóa của tài khoản admin và user
                if line.strip() == encrypted_input_admin:
                    print("Đăng nhập với quyền Admin thành công!")
                    return "admin"
                elif line.strip() == encrypted_input_user:
                    print("Đăng nhập với quyền User thành công!")
                    return "user"
    print("Đăng nhập thất bại!")
    return None

# Hàm xem tất cả tài khoản (dành cho admin)
def view_all_accounts():
    if os.path.exists(FILE_PATH):
        print("\nDanh sách tất cả tài khoản:")
        with open(FILE_PATH, "rb") as file:
            for line in file:
                decrypted_data = des_cipher.decrypt(line.strip()).decode('utf-8').strip()
                print(decrypted_data)
    else:
        print("File không tồn tại!")

# Hàm xem thông tin tài khoản của người dùng hiện tại (dành cho user)
def view_user_account(account_number, pin):
    encrypted_input_user = encrypt_data(account_number, pin, "user")
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as file:
            for line in file:
                if line.strip() == encrypted_input_user:
                    decrypted_data = des_cipher.decrypt(line.strip()).decode('utf-8').strip()
                    print(f"\nThông tin tài khoản của bạn: {decrypted_data}")
                    return
    print("Tài khoản không tìm thấy!")

# Giao diện chính
def main():
    while True:
        print("\nChọn chức năng:")
        print("1. Đăng nhập")
        print("2. Tạo tài khoản mẫu (admin & user)")
        print("3. Thoát")
        
        choice = input("Chọn chức năng (1-3): ")
        
        if choice == "1":
            account_number = input("Nhập số tài khoản: ")
            pin = input("Nhập mã PIN: ")
            role = check_login(account_number, pin)
            
            # Nếu đăng nhập với tài khoản admin, có thể tạo tài khoản mới và xem tất cả tài khoản
            if role == "admin":
                while True:
                    print("\nAdmin Menu:")
                    print("1. Tạo tài khoản mới")
                    print("2. Xem tất cả tài khoản")
                    print("3. Đăng xuất")
                    admin_choice = input("Chọn chức năng (1-3): ")
                    
                    if admin_choice == "1":
                        new_account_number = input("Nhập số tài khoản mới: ")
                        new_pin = input("Nhập mã PIN cho tài khoản mới: ")
                        new_role = input("Chọn loại tài khoản (admin/user): ").strip().lower()
                        if new_role in ["admin", "user"]:
                            register_account(new_account_number, new_pin, new_role)
                        else:
                            print("Loại tài khoản không hợp lệ!")
                    
                    elif admin_choice == "2":
                        view_all_accounts()
                    
                    elif admin_choice == "3":
                        print("Đăng xuất Admin thành công!")
                        break
                    else:
                        print("Lựa chọn không hợp lệ, vui lòng chọn lại.")
            
            # Nếu đăng nhập với tài khoản user, chỉ có quyền xem thông tin tài khoản của chính họ
            elif role == "user":
                view_user_account(account_number, pin)
        
        elif choice == "2":
            create_sample_accounts()
        
        elif choice == "3":
            print("Cảm ơn bạn đã sử dụng dịch vụ.")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

# Chạy ứng dụng
if __name__ == "__main__":
    main()
