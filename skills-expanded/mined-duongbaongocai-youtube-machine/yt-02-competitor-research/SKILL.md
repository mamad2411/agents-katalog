---
name: yt-02-competitor-research
description: Bước 2 của quy trình YouTube Machine — nghiên cứu kênh đối thủ trong ngách đã chọn bằng trình duyệt tích hợp và tìm kiếm web (không cần API key). Tìm 5-10 kênh cùng ngách (ưu tiên kênh nhỏ đang tăng nhanh), ghi lại sub, số video, tần suất đăng, video top, tiêu đề, thumbnail, độ dài, cấu trúc mở đầu, tag và mô tả họ dùng; rút ra công thức đang ăn khách, khoảng trống nội dung và cách kênh mình khác đi. Ghi kenh/02-competitors.md và dữ liệu thô vào kenh/nghien-cuu/. Dùng khi người dùng nói "nghiên cứu đối thủ", "phân tích kênh X", "kênh nào đang làm ngách này", "xem kênh đối thủ đăng gì", "học theo kênh nào", hoặc khi skill youtube-machine gọi bước 2.
---

# yt-02-competitor-research

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-02-competitor-research/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
