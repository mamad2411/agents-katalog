---
name: yt-04b-visual-style
description: Bước 4b của quy trình YouTube Machine — xây bộ phong cách hình ảnh (visual style bible) cố định cho kênh YouTube faceless, khóa phong cách (style lock) gắn vào mọi prompt, bảng màu, ánh sáng, ngôn ngữ máy quay, danh mục loại cảnh kèm mẫu prompt, quy tắc chọn ảnh tĩnh hay clip, chuyển động mặc định, yếu tố hình lặp lại của kênh, bối cảnh và vật thể cố định (@TÊN), quy tắc thiết kế nhân vật riêng từng video. Tạo ảnh thử miễn phí bằng Flow AIC để người dùng chọn, lưu khóa phong cách vào kênh Flow AIC. Ghi kenh/04b-visual-style.md và thư mục nhan-dien/phong-cach/. Dùng khi người dùng nói "phong cách hình ảnh", "style kênh", "cố định nhân vật", "giữ hình đồng nhất", "khóa phong cách", "style bible", "ảnh mẫu cho kênh", "nhân vật bị đổi mặt giữa các cảnh", hoặc khi skill youtube-machine gọi bước 4b.
---

# yt-04b-visual-style

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-04b-visual-style/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
