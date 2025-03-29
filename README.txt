1, crawl post page: python crawl_post_page.py

điều kiện: 
- trong file account.json 
+ dùng lệnh python convert_file.py
+ để chuyển dạng csv sang json
ví dụ
{
    "account_1": {
        "url1": "https://lab-fe.emso.vn/page/TrenDuongPitch/",
        "url2": "https://www.facebook.com/TrenDuongPitch",
        "username": "s1456a2@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_2": {
        "url1": "https://lab-fe.emso.vn/page/vkrnews/",
        "url2": "https://www.facebook.com/vkrnews",
        "username": "s1456a2@gmail.com",
        "password": "khongnhomatkhaucu"
    }
}
- Dữ liệu sau khi crawl sẽ lưu vào file post, file này cần giữ nguyên cho lần crawl sau đê tránh việc crawl post trùng 
- Chuyển môi tường cần crawl trong file config.py
- Chuẩn bị account fb trong file  data.json

2, crawl post page: python crawl_post_user.py

tương tự khi crawl post page
nhưng lấy data từ file: data_crawl_post_user.json

3, crawl moment - reels: python crawl_moment.py
điều kiện:
- chuẩn bị account trong file: account_create_moment
- Dữ liệu crawl sẽ được lưu vào moment.json
ví dụ: 
{
    "account_1": {
        "username": "emsomanagerhd@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_2": {
        "username": "s1456a2@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_3": {
        "username": "pnnh1311@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_4": {
        "username": "hungnguyen10121311@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_5": {
        "username": "testeremso12@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_6": {
        "username": "hungnguyen610a2@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_7": {
        "username": "testeremso@gmail.com",
        "password": "khongnhomatkhaucu"
    },
    "account_8": {
        "username": "testeremso2@gmail.com",
        "password": "khongnhomatkhaucu"
    }
}


3, crawl moment - tiktok: python crawl_titkok.py
sau khi chrome được mở cần đăng nhập nhanh vào tiktok 
- dữ liệu được lưu vào file: tiktok.json
- Các tài khoản dùng đề đăng trong file "account_create_moment.json"


4, crawl watch: python crawl_watch.py
điều kiện: sử dụng file account.json tương tự như crawl post
- dữ liệu được lưu vào file: watch.json



