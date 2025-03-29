from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
import time
import os
import json

def main():
    # Load cấu hình
    config = Config()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Chặn thông báo
    # chrome_options.add_argument("--headless")  # Chế độ không giao diện
    chrome_options.add_argument("--disable-gpu")  # Vô hiệu hóa GPU khi chạy headless
    chrome_options.add_argument("--window-size=1920x1080")  # Thiết lập kích thước cửa sổ để tránh một số vấn đề hiển thị
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Mở trang web
    base_page = BasePage(driver)
    accounts_filename = "data/account_avt_test.json"  # Đọc dữ liệu tài khoản từ file account.json
    report_filename = "report.txt"  # File lưu kết quả

    driver.maximize_window()

    try:
        # Đọc danh sách tài khoản từ file JSON
        with open(accounts_filename, "r") as file:
            accounts = json.load(file)

        with open(report_filename, "w") as report_file:
            # Lặp qua từng tài khoản và thực hiện đăng nhập + upload ảnh
            for account_key, account_info in accounts.items():
                username = account_info["username"]
                password = account_info["password"]

                print(f"Đang xử lý tài khoản: {username}")

                # Đăng nhập tài khoản
                base_page.login_emso(username, password)

                # Thực hiện upload avatar và kiểm tra kết quả
                if base_page.update_avatar_user():
                    result = f"{username}: pass"
                    base_page.logout()
                else:
                    result = f"{username}: false"
                    base_page.logout()
                # Ghi kết quả vào file report
                report_file.write(result + "\n")
                
            
        print("Đã hoàn tất xử lý tất cả các tài khoản.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
