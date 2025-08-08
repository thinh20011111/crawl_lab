import requests
import time
import os
import json
import random
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.base_page import BasePage
from utils.config import Config
from selenium.webdriver.chrome.options import Options
from requests.exceptions import RequestException

# Thông tin API
API_URL = "https://dashboard-crawl.wuaze.com/api/update_status.php"
PROGRAM_NAME = "Post_Page_crawl"

# Hàm gửi trạng thái đến dashboard
def send_status(status="running", retries=3, delay=5, verify_ssl=True):
    payload = {
        "program_name": PROGRAM_NAME,
        "status": status,
        "timestamp": int(time.time())
    }
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, json=payload, timeout=30, verify=verify_ssl)
            print(f"Trạng thái đã gửi: {response.status_code}")
            print(f"Nội dung phản hồi: {response.text}")
            return
        except RequestException as e:
            print(f"Thử lần {attempt + 1} thất bại: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    print("Gửi trạng thái thất bại sau tất cả các lần thử")

# Hàm gửi trạng thái định kỳ
def periodic_status():
    while True:
        send_status()
        time.sleep(300)  # Gửi mỗi 5 phút

def main():
    # Load cấu hình
    config = Config()

    # Khởi tạo Service với đường dẫn ChromeDriver
    service = Service(config.CHROME_DRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Mở trang web
    base_page = BasePage(driver)
    accounts_filename = "data/account_lab.json"
    output_file = "data/facebook_posts.json"
    data_filename = "data/data.json"

    # Đọc dữ liệu tài khoản từ data.json
    with open(data_filename, 'r') as data_file:
        data = json.load(data_file)

    driver.maximize_window()

    try:
        # Đăng nhập vào Facebook một lần
        facebook_account = data.get("account_facebook", {})
        email_facebook = facebook_account["email"]
        password_facebook = facebook_account["password"]

        driver.get(config.FACEBOOK_URL)
        base_page.login_facebook(email_facebook, password_facebook)
        time.sleep(30)
        print("Đăng nhập thành công vào Facebook.")

        # Gửi trạng thái ban đầu
        send_status()

        # Khởi động thread gửi trạng thái định kỳ
        status_thread = threading.Thread(target=periodic_status, daemon=True)
        status_thread.start()

        # Hỏi người dùng về chế độ chạy
        use_post_limit = input("Bạn có muốn chạy theo số lượng bài post quy định không? (y/n): ").lower()
        total_posts_crawled = 0
        target_posts = None

        if use_post_limit == 'y':
            while True:
                try:
                    target_posts = int(input("Nhập số lượng bài post cần crawl: "))
                    if target_posts > 0:
                        break
                    print("Vui lòng nhập một số lớn hơn 0.")
                except ValueError:
                    print("Vui lòng nhập một số hợp lệ.")
            print(f"Chương trình sẽ dừng sau khi crawl {target_posts} bài post.")

        # Vòng lặp chính
        while True:
            # Đọc dữ liệu tài khoản từ account.json
            with open(accounts_filename, 'r') as file:
                accounts_data = json.load(file)

            # Xáo trộn danh sách tài khoản
            account_items = list(accounts_data.items())
            random.shuffle(account_items)  # Ngẫu nhiên thứ tự, không trùng lặp

            print("Bắt đầu chu kỳ crawl mới với danh sách tài khoản đã xáo trộn.")

            # Lặp qua danh sách tài khoản đã được shuffle
            for account_key, account_data in account_items:
                try:
                    print(f"\nĐang xử lý tài khoản: {account_key}")

                    group_url = account_data["url2"]
                    emso_username = account_data["username"]
                    emso_password = account_data["password"]
                    post_url = account_data["url1"]

                    num_posts = 1  # Mặc định crawl 1 bài mỗi lần
                    success = base_page.scroll_to_element_and_crawl(
                        username=emso_username,
                        password=emso_password,
                        nums_post=num_posts,
                        crawl_page=group_url,
                        post_page=post_url,
                        page=True
                    )

                    if success:
                        print(f"Hoàn tất xử lý tài khoản: {account_key}")
                        total_posts_crawled += num_posts
                        base_page.clear_media_folder()
                        
                        # Kiểm tra nếu đã đạt số lượng bài post mục tiêu
                        if use_post_limit == 'y' and total_posts_crawled >= target_posts:
                            print(f"Đã crawl đủ {target_posts} bài post. Dừng chương trình.")
                            return  # Thoát khỏi hàm main
                        else:        
                            print(f"TẠM DỪNG 3P")
                            time.sleep(180)                
                            
                    else:
                        print(f"Không có bài đăng thành công, tiếp tục với tài khoản tiếp theo.")
                except Exception as e:
                    print(f"Đã gặp lỗi khi xử lý tài khoản {account_key}: {e}")
                    continue

            print("Đã hoàn tất xử lý tất cả các tài khoản trong chu kỳ này. Bắt đầu chu kỳ mới.")
            # Gửi trạng thái sau mỗi chu kỳ
            send_status()

    except Exception as e:
        print(f"Lỗi nghiêm trọng trong quá trình chạy: {e}")
        send_status(status="stopped")  # Gửi trạng thái stopped nếu có lỗi nghiêm trọng
    finally:
        send_status(status="stopped")  # Gửi trạng thái stopped khi chương trình kết thúc
        driver.quit()

if __name__ == "__main__":
    main()