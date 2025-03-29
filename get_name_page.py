from utils.base_page import BasePage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import Config
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.common.by import By
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

    # Đường dẫn file dữ liệu
    accounts_filename = "data/account.json"  # Đọc dữ liệu tài khoản từ file account.json
    output_filename = "name.txt"  # File để lưu dữ liệu lấy được
    base_page = BasePage(driver)
    # Đọc dữ liệu tài khoản từ account.json
    with open(accounts_filename, 'r') as file:
        accounts_data = json.load(file)
    HOME_PAGE_TAB = "//button[contains(text(),'Trang chủ')]"


    driver.maximize_window()
    try:
        base_page.login_emso("testeremso3@gmail.com", "khongnhomatkhaucu")
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for account_key, account_info in accounts_data.items():
                url = account_info.get("url1")
                if not url:
                    continue

                # Truy cập URL
                driver.get(url)
                base_page.wait_for_element_present(HOME_PAGE_TAB)
                try:
                    # Lấy text từ element chỉ định
                    base_page.wait_for_element_present("/html/body/div/div/div/main/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/p")
                    text = base_page.get_text_from_element("/html/body/div/div/div/main/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/p")

                    # Ghi dữ liệu vào file ngay sau khi lấy dữ liệu thành công
                    output_file.write(f"{text}\n")
                    output_file.flush()
                except Exception as e:
                    print(f"Không thể lấy dữ liệu từ {url}: {e}")


    finally:
        driver.quit()

if __name__ == "__main__":
    main()
