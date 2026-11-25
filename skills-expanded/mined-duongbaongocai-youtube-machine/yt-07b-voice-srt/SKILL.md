---
name: yt-07b-voice-srt
description: Bước 7b của quy trình YouTube Machine — biến lời đọc liền mạch (1-kich-ban/NNN-slug-voice.txt) thành giọng đọc AI bằng ElevenLabs và file phụ đề SRT khớp thời gian. Hỏi người dùng có muốn tạo giọng luôn qua API không (ElevenLabs gốc hoặc aicong.pro): nhận khóa API dán vào chat, quét thư viện giọng, đề xuất giọng hợp kênh kèm mẫu nghe, lưu giọng đã chọn vào hồ sơ kênh để video sau dùng lại, tạo MP3 và SRT sau khi báo số ký tự. Không dùng API thì hướng dẫn người dùng cài giọng, từ điển phát âm, tạo một file giọng liền cho cả video, lấy SRT bằng Speech to Text (Scribe) của ElevenLabs; sau đó tự kiểm tra SRT, sửa chữ sai theo lời gốc mà giữ mốc thời gian, chuẩn hóa mỗi dòng thành một cảnh 1,5-8 giây, tìm mốc chương YouTube. Ghi videos/NNN-slug/2-giong/. Dùng khi người dùng nói "tạo giọng", "giọng AI", "ElevenLabs", "xuất SRT", "phụ đề", "file srt bị sai chữ", "căn phụ đề", "đã có file giọng và srt", "gửi file mp3 / srt", hoặc khi skill youtube-machine gọi bước 7b.
---

# yt-07b-voice-srt

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07b-voice-srt/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
