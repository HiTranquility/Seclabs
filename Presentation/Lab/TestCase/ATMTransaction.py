from pyDes import des, ECB
import os

# Thiết lập khóa DES cho mã hóa
KEY = b"ATMKEY01"  # Khóa 8 byte
des_cipher = des(KEY, ECB)

# Đường dẫn tới file lưu trữ dữ liệu mã hóa
FILE_PATH = "encrypted_accounts.txt"
FAILED_ATTEMPTS = {}

# Hàm mã hóa dữ liệu tài khoản với trạng thái khóa
def encrypt_data(account_number, pin, role, status="unlocked"):
    transaction_data = f"{account_number}:{pin}:{role}:{status}"
    if len(transaction_data) % 8 != 0:
        transaction_data += ' ' * (8 - len(transaction_data) % 8)
    return des_cipher.encrypt(transaction_data)

# Hàm giải mã dữ liệu
def decrypt_data(encrypted_data):
    decrypted_data = des_cipher.decrypt(encrypted_data).decode('utf-8').strip()
    return decrypted_data.split(":")

# Tạo tài khoản mẫu cho admin và user
def create_sample_accounts():
    print("Đang tạo tài khoản mẫu...") 
    admin_account_number = "admin123"
    admin_pin = "1234"
    admin_role = "admin"
    user_account_number = "user456"
    user_pin = "5678"
    user_role = "user"
    
    try:
        with open(FILE_PATH, "wb") as file:
            encrypted_admin = encrypt_data(admin_account_number, admin_pin, admin_role)
            file.write(encrypted_admin + b'\n')
            
            encrypted_user = encrypt_data(user_account_number, user_pin, user_role)
            file.write(encrypted_user + b'\n')
        
        print("File 'encrypted_accounts.txt' đã được tạo với tài khoản admin và user mẫu.")
    
    except Exception as e:
        print(f"Lỗi khi tạo tài khoản mẫu: {e}")

# Đăng ký tài khoản mới
def register_account(account_number, pin, role):
    encrypted_data = encrypt_data(account_number, pin, role)
    with open(FILE_PATH, "ab") as file:
        file.write(encrypted_data + b'\n')
    print(f"Tài khoản '{role}' đã được đăng ký thành công!")

# Hàm kiểm tra đăng nhập với giới hạn số lần thử
def check_login(input_account, input_pin):
    with open(FILE_PATH, "rb") as file:
        for line in file:
            acc_num, pin, role, status = decrypt_data(line.strip())
            
            if acc_num == input_account and status == "locked":
                print("Tài khoản của bạn đã bị khóa.")
                return None
            elif acc_num == input_account and pin == input_pin:
                if role == "admin":
                    print("Đăng nhập với quyền Admin thành công!")
                    return "admin"
                elif role == "user":
                    print("Đăng nhập với quyền User thành công!")
                    return "user"

    FAILED_ATTEMPTS[input_account] = FAILED_ATTEMPTS.get(input_account, 0) + 1
    if FAILED_ATTEMPTS[input_account] >= 3:
        lock_account(input_account)
    else:
        print("Đăng nhập thất bại!")
    return None

# Hàm xem tất cả tài khoản (dành cho admin)
def view_all_accounts():
    if os.path.exists(FILE_PATH):
        print("\nDanh sách tất cả tài khoản:")
        with open(FILE_PATH, "rb") as file:
            for line in file:
                decrypted_data = decrypt_data(line.strip())
                print(decrypted_data)
    else:
        print("File không tồn tại!")

# Hàm xem thông tin tài khoản của người dùng hiện tại (dành cho user)
def view_user_account(account_number, pin):
    with open(FILE_PATH, "rb") as file:
        for line in file:
            acc_num, pin_num, role, status = decrypt_data(line.strip())
            if acc_num == account_number and pin == pin_num:
                print(f"\nThông tin tài khoản của bạn: {line.strip().decode()}")
                return
    print("Tài khoản không tìm thấy!")

# Hàm khóa tài khoản
def lock_account(account_number):
    with open(FILE_PATH, "rb") as file:
        lines = file.readlines()
    
    with open(FILE_PATH, "wb") as file:
        for line in lines:
            acc_num, pin, role, status = decrypt_data(line.strip())
            if acc_num == account_number:
                status = "locked"
                encrypted_data = encrypt_data(acc_num, pin, role, status)
                file.write(encrypted_data + b'\n')
                print(f"Tài khoản '{account_number}' đã bị khóa.")
            else:
                file.write(line)

# Hàm mở khóa tài khoản (Admin)
def unlock_account(account_number):
    with open(FILE_PATH, "rb") as file:
        lines = file.readlines()
    
    with open(FILE_PATH, "wb") as file:
        for line in lines:
            acc_num, pin, role, status = decrypt_data(line.strip())
            if acc_num == account_number:
                status = "unlocked"
                encrypted_data = encrypt_data(acc_num, pin, role, status)
                file.write(encrypted_data + b'\n')
                print(f"Tài khoản '{account_number}' đã được mở khóa.")
            else:
                file.write(line)

# Menu chính
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
            
            # Menu cho Admin
            if role == "admin":
                while True:
                    print("\nAdmin Menu:")
                    print("1. Tạo tài khoản mới")
                    print("2. Xem tất cả tài khoản")
                    print("3. Khóa tài khoản")
                    print("4. Mở khóa tài khoản")
                    print("5. Đăng xuất")
                    admin_choice = input("Chọn chức năng (1-5): ")
                    
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
                        lock_acc = input("Nhập số tài khoản cần khóa: ")
                        lock_account(lock_acc)
                    
                    elif admin_choice == "4":
                        unlock_acc = input("Nhập số tài khoản cần mở khóa: ")
                        unlock_account(unlock_acc)
                    
                    elif admin_choice == "5":
                        print("Đăng xuất Admin thành công!")
                        break
                    else:
                        print("Lựa chọn không hợp lệ, vui lòng chọn lại.")
            
            # Menu cho User
            elif role == "user":
                while True:
                    print("\nUser Menu:")
                    print("1. Xem thông tin tài khoản")
                    print("2. Đăng xuất")
                    user_choice = input("Chọn chức năng (1-2): ")
                    
                    if user_choice == "1":
                        view_user_account(account_number, pin)
                    
                    elif user_choice == "2":
                        print("Đăng xuất User thành công!")
                        break
                    else:
                        print("Lựa chọn không hợp lệ, vui lòng chọn lại.")
        
        elif choice == "2":
            create_sample_accounts()
        
        elif choice == "3":
            print("Cảm ơn bạn đã sử dụng dịch vụ.")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

# Chạy chương trình
main()
