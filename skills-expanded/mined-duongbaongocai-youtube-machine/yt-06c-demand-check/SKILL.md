---
name: yt-06c-demand-check
description: Bước 6c của quy trình YouTube Machine — kiểm tra nhu cầu và chốt tiêu đề cùng ý thumbnail của một video TRƯỚC khi viết kịch bản. Đối chiếu ý tưởng với video vượt trội của đối thủ, video cùng chủ đề trong 3 tháng gần đây, độ tràn của định dạng (nhất là kênh AI làm hàng loạt), kết quả các video trước của kênh; viết Thẻ giá trị và đối chiếu sổ khác biệt; viết 5-10 cặp tiêu đề và thumbnail, chấm điểm, người dùng chốt một cặp hoặc đổi chủ đề. Ghi videos/NNN-slug/1-kich-ban/NNN-slug-nhu-cau.md. Dùng khi người dùng nói "video này có ai xem không", "chủ đề này còn nhu cầu không", "chọn chủ đề video tiếp theo", "kiểm tra ý tưởng trước khi viết", "tiêu đề trước kịch bản", "video làm xong không có view nên làm gì khác", hoặc khi skill youtube-machine gọi bước 6c, luôn chạy trước yt-07-script.
---

# yt-06c-demand-check

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-06c-demand-check/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
