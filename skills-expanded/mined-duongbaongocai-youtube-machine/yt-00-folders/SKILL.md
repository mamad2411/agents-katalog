---
name: yt-00-folders
description: Quản lý thư mục của quy trình YouTube Machine — tạo thư mục kênh và video theo cấu trúc chuẩn (mỗi video một thư mục, chia công đoạn đánh số), giữ tài nguyên riêng từng kênh (nhạc, SFX, font, lớp phủ), kiểm tra file nằm sai chỗ, báo dung lượng, dọn file trung gian sau khi đăng, chuyển kênh kiểu cũ sang cấu trúc mới có hoàn tác. Dùng khi người dùng nói "sắp xếp thư mục", "file để lộn xộn", "file video nằm ở đâu", "tạo thư mục video", "kênh chiếm bao nhiêu ổ đĩa", "dọn file", "hết ổ đĩa", "nạp nhạc, SFX, lớp phủ cho kênh", "chuyển kênh sang cấu trúc mới", hoặc khi skill youtube-machine và các bước yt-* cần tạo thư mục, dọn sau khi đăng. KHÔNG dùng cho việc chọn nội dung file (đó là các bước yt-01 đến yt-10).
---

# yt-00-folders

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-00-folders/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
