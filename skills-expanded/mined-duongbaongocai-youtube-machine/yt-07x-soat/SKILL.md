---
name: yt-07x-soat
description: Bước Soát thành phẩm của quy trình YouTube Machine, cổng 4 của năm cổng — kiểm tra video sau khi dựng và trước khi đăng, cho mọi đường sản xuất. Máy đo thời lượng, độ phân giải, âm lượng, hình đứng yên, khung đen, tiếng tắt và tạo tờ khung; sau đó một người soát có ngữ cảnh sạch đối chiếu thành phẩm với lời hứa của Thẻ giá trị, báo lỗi theo mốc thời gian và mức nặng nhẹ. Ghi videos/NNN-slug/4-dung/soat/. Dùng khi người dùng nói "soát video", "kiểm tra video", "video này ổn chưa", "duyệt thành phẩm", "QC video", "xem lại trước khi đăng", "soát lỗi", hoặc khi skill youtube-machine gọi bước soát sau khi dựng. Luôn chạy trước yt-08-seo-publish với video mới.
---

# yt-07x-soat

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07x-soat/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
