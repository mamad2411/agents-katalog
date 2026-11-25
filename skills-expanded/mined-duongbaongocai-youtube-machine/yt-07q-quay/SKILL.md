---
name: yt-07q-quay
description: Bước Quay của quy trình YouTube Machine, dành cho đường Quay trước và đường Màn hình — chuẩn bị để người dùng tự quay hoặc ghi màn hình một video từ dàn ý đã duyệt. Lập kế hoạch quay, chữ nhắc theo ý, danh sách cảnh phụ, bảng phép thử cho review, quay thử 30 giây để kiểm tra tiếng và khung, dọn thông tin riêng tư trước khi ghi màn hình, rồi nhận file và kiểm tra kỹ thuật. Ghi videos/NNN-slug/1-kich-ban/NNN-slug-quay.md, NNN-slug-nhac.txt và 3-hinh/tho/. Dùng khi người dùng nói "chuẩn bị quay", "kế hoạch quay", "chữ nhắc", "teleprompter", "danh sách cảnh cần quay", "cảnh phụ", "b-roll", "quay gì", "ghi màn hình", "tôi quay xong rồi", "đã có video quay", hoặc khi skill youtube-machine gọi bước Quay hay Ghi. Không dùng cho video làm bằng hình AI.
---

# yt-07q-quay

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07q-quay/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
