---
name: yt-osint
description: Skill tùy chọn của quy trình YouTube Machine — tra cứu nguồn mở (OSINT) cho video YouTube bằng danh mục công cụ chọn lọc từ OSINT4ALL. Tìm tài liệu gốc, kiểm chứng tuyên bố, tìm nguồn gốc ảnh và video, lấy số liệu, bản đồ, tư liệu địa lý, thời tiết trong quá khứ, dữ liệu tàu và máy bay cho video sự kiện, khảo sát video đối thủ, bình luận, xu hướng và cộng đồng, ghi danh sách nguồn có link và ngày truy cập. Có ranh giới rõ, không tìm thông tin người riêng tư, không dùng dữ liệu rò rỉ, giấy tờ giả, tìm mặt người, camera không bảo mật. Ghi videos/NNN-slug/1-kich-ban/NNN-slug-nguon.md hoặc kenh/nghien-cuu/. Dùng khi người dùng nói "OSINT", "OSINT4ALL", "tìm nguồn", "kiểm chứng", "fact check", "ảnh này từ đâu", "tìm tài liệu gốc", "số liệu cho video", "bản đồ cho video", "công cụ tra cứu". Trong quy trình, các bước 2, 3, 6b, 6c, 7, 7c, 7m, 8 chỉ đề xuất một dòng khi có việc phù hợp, người dùng đồng ý mới chạy. KHÔNG dùng để tìm hồ sơ của một người, kể cả khi được yêu cầu.
---

# yt-osint

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-osint/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
