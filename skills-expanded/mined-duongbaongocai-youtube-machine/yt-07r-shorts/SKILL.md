---
name: yt-07r-shorts
description: Bước Shorts của quy trình YouTube Machine — chọn đoạn đứng độc lập từ video dài và làm thành Shorts dọc 1080x1920. Chọn đoạn theo ý chứ không theo độ dài, đặt tâm khung sau khi nhìn hình, cắt dọc hoặc giữ khung ngang trên nền mờ, in phụ đề, chuẩn âm lượng, soát từng Shorts, ghi tiêu đề và mô tả riêng, chống lặp mẫu giữa các lô. Ghi videos/NNN-slug/5-xuat/shorts/ và 6-dang/NNN-shorts.md. Dùng khi người dùng nói "cắt Shorts", "làm Shorts từ video này", "video dọc", "9:16", "reframe", "cắt clip ngắn", "Shorts từ podcast", hoặc khi video đã có đầu ra dọc. Shorts gốc viết riêng thì làm theo đường chính và công thức shorts.md; video đường Blender có thể dùng tools/blender/cat_shorts.py.
---

# yt-07r-shorts

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07r-shorts/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
