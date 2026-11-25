---
name: yt-09-post-publish
description: Bước 9 của quy trình YouTube Machine — kế hoạch sau khi đăng video, lịch 48 giờ đầu (ghim bình luận, trả lời bình luận trong 1-2 giờ đầu), theo dõi CTR, thời gian xem, điểm khán giả rời đi, ngưỡng đổi tiêu đề hoặc thumbnail dự phòng (thử A/B), chiến lược Shorts dẫn về video dài (một Short cùng ngày, một Short sau 24 giờ), chia sẻ chính đáng vào cộng đồng đúng ngách, thăm dò hoặc teaser trước khi đăng, cân nhắc quảng cáo nhỏ có trần ngân sách, và quy trình khi video gãy đề xuất. Ghi videos/NNN-slug/6-dang/NNN-slug-hau-dang.md. Dùng khi người dùng nói "video vừa đăng làm gì tiếp", "video không có view", "gãy đề xuất", "đổi thumbnail", "làm Shorts từ video dài", "trả lời bình luận", "chia sẻ video ở đâu", hoặc khi skill youtube-machine gọi bước 9. Không tạo tài khoản phụ, proxy hay tăng tương tác giả.
---

# yt-09-post-publish

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-09-post-publish/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
