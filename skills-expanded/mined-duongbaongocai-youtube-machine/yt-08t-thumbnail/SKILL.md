---
name: yt-08t-thumbnail
description: Bước thumbnail của quy trình YouTube Machine — biến ý thumbnail đã chốt ở bước 6c thành 2-3 ảnh 1280x720 thật. Lấy nền từ khung video, ảnh Flow AIC hoặc ảnh chụp, ghép chữ bằng máy nên đúng chính tả và đủ dấu tiếng Việt, tự dừng nếu font thiếu chữ, tạo tờ so sánh ở cỡ trang chủ và cỡ nhỏ trên nền tối, nền sáng để chọn bản đọc được, đối chiếu đối thủ và các video trước của kênh. Ghi videos/NNN-slug/5-xuat/thumbnail/. Dùng khi người dùng nói "làm thumbnail", "ảnh bìa video", "thiết kế thumbnail", "ghép chữ lên thumbnail", "so sánh thumbnail", "thumbnail nhỏ quá khó đọc", "bản thumbnail thứ hai để thử A/B", hoặc khi yt-08-seo-publish cần ảnh thumbnail.
---

# yt-08t-thumbnail

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-08t-thumbnail/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
