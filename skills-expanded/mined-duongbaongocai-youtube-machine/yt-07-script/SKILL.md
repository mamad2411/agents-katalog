---
name: yt-07-script
description: Bước 7 của quy trình YouTube Machine — viết kịch bản video YouTube hoàn chỉnh theo đúng giọng điệu kênh trong 04-brand.md, nghiên cứu tư liệu, dàn ý giữ chân người xem (hook 15 giây, mở nút, cao trào, kết có CTA), lời đọc theo chương, gợi ý hình cho từng đoạn theo danh mục loại cảnh của kênh, danh sách nhân vật riêng của video với mô tả cố định, và một file lời đọc liền mạch (voice.txt) viết theo lối nói của người Mỹ bản xứ (rút gọn, nối âm, dạng nói theo mức nói của kênh, thẻ cảm xúc Eleven v3), có công cụ soát độ tự nhiên, sạch để dán thẳng vào ElevenLabs tạo giọng. Hỗ trợ video dài và Shorts. Ghi videos/NNN-slug/1-kich-ban/NNN-slug.md và NNN-slug-voice.txt. Dùng khi người dùng nói "viết kịch bản", "script cho video", "lời đọc voice", "viết video số 3 trong kế hoạch", "kịch bản Shorts", "lời đọc liền mạch để tạo giọng", hoặc khi skill youtube-machine gọi bước 7. Không dùng để tạo giọng, chia cảnh theo SRT hay dựng video (đó là yt-07b, yt-07c, yt-07e).
---

# yt-07-script

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07-script/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
