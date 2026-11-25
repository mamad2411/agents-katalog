---
name: yt-06b-policy-check
description: Bước 6b của quy trình YouTube Machine — kiểm tra chính sách và rủi ro trước khi sản xuất video, nội dung dùng lại, nội dung lặp lại hoặc sản xuất hàng loạt, bản quyền hình, nhạc và đoạn phim (Content ID, gậy bản quyền), thương hiệu, fair use, nội dung AI gây hiểu lầm và khai báo giọng AI, an toàn trẻ em và bạo lực. Rà từng ý tưởng trong kế hoạch nội dung, chấm mức rủi ro thấp / trung bình / cao, ghi nguồn giấy phép nhạc và hình, đề xuất cách sửa. Ghi kenh/06b-policy-check.md. Dùng khi người dùng nói "kiểm tra bản quyền", "có vi phạm chính sách không", "nhạc này dùng được không", "khai báo nội dung AI", "kênh có bị gỡ kiếm tiền không", "rà chính sách trước khi làm video", hoặc khi skill youtube-machine gọi bước 6b. Không tư vấn pháp lý và không đảm bảo kết quả kiếm tiền.
---

# yt-06b-policy-check

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-06b-policy-check/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
