# Hướng dẫn tra cứu EduTrack

Trước khi sửa chức năng, đọc mục liên quan trong [docs/project-guide.md](docs/project-guide.md), đặc biệt bảng tra cứu file ở mục 2 và bất biến ở mục 19.

Chạy `node scripts/project-index.cjs --check` để biết các file nguồn BE/FE đã thay đổi so với lần sinh tài liệu. Tool cần frontend sibling `../edutrack_fe`. Nếu có thay đổi, đọc diff và code đích; chỉ mục [docs/project-code-index.md](docs/project-code-index.md) giúp tìm route/schema/DTO/method/test.

Không nạp toàn bộ chỉ mục hoặc JSON snapshot vào context. Tài liệu không thay thế xác minh quyền sở hữu, transaction, snapshot hóa đơn, biểu diễn giờ và auth khi sửa.

Sau thay đổi, cập nhật guide về hành vi thực tế và kiểm thử, rồi chạy `node scripts/project-index.cjs` và `--check`. Không đọc/commit credential JSON, .env thật hoặc dữ liệu backup chỉ để cập nhật tài liệu.
