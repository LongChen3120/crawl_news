## MÔ TẢ
- Dự án thu thập, cập nhật, xử lý, lưu trữ thông tin các bài tin tức trên các Website Online.
- Dự án dễ dàng mở rộng, không giới hạn nguồn các Website thu thập vì cách thức thu thập đa dạng: qua Request, qua Selenium, qua API

## CÔNG NGHỆ SỬ DỤNG
- Python: Request, Selenium, ThreadPool, Logging
- Apache Airflow
- Mongodb
- Docker

## NỘI DUNG
### Sơ đồ tổng quát
![ETL news](https://github.com/user-attachments/assets/17ddf6ba-b3a5-4142-90fc-8a7fdf1fc553)

### Nhiệm vụ
1. Xây dựng File Config
- File Config là File Json thiết lập cách mà chương trình thu thập dữ liệu, nằm ở trong thư mục ./src/extract.
- Nếu có Website mới cần thu thập dữ liệu, thêm Website đó vào trong File Config theo mẫu, ý nghĩa của các Key trong file Config Json được định nghĩa ở trong File ./src/extract/keys.md.

2. Thu thập URL bài viết
- Truy cập vào Website, thu thập tất cả URL rồi lưu vào Datalake.
- Lập lịch Airflow chạy thu thập URL của tất cả các Website trong File Config mỗi 30 phút.

3. Thu thập dữ liệu chi tiết bài viết lần 1
- Select những URL mới (chưa được thu thập dữ liệu chi tiết lần nào) trong Data Warehouse.
- Truy cập vào URL bài viết, thu thập Tiêu đề, sapo, nội dung, ảnh, tác giả, thời gian rồi lưu vào Datalake.
- Những URL đã được thu thậP dữ liệu chi tiết sẽ được cập nhật số lần thu thập dữ liệu chi tiết += 1.
- Lập lịch Airflow chạy thu thập dữ liệu chi tiết mỗi 30 phut.

4. Cập nhật lại bài viết
- Select lấy những URL có số lần thu thập dữ liệu chi tiết từ 1 đến 5 và có thời gian cập nhật dữ liệu chi tiết nhỏ hơn 10 giờ trong Data Warehouse.
- Truy cập vào URL bài viết, thu thập Tiêu đề, sapo, nội dung, ảnh, tác giả, thời gian rồi cập nhật trong Data Warehouse.
- Những URL đã được thu thậP dữ liệu chi tiết sẽ được cập nhật số lần thu thập dữ liệu chi tiết += 1.
- Lập lịch Airflow chạy thu thập dữ liệu chi tiết mỗi 1 tiếng.

3. Xử lý dữ liệu
- Dọn dẹp dữ liệu URL, dữ liệu chi tiết cũ (dữ liệu cũ là dữ liệu có time_crawl > 48h) trong Datalake vào 23h45p chủ nhật hàng tuần.
- Format lại dữ liệu URL trong Datalake, bổ sung thêm thông tin cho những URL khuyết thiếu, lọc URL trùng lặp, lưu vào trong Data Warehouse mỗi 30 phút (sau khi thu thập dữ liệu URL).
- Format lại dữ liệu chi tiết trong Datalake, xử lý text, xử lý dữ liệu ngày tháng, lọc dữ liệu trùng lặp, lưu vào trong Data Warehouse
