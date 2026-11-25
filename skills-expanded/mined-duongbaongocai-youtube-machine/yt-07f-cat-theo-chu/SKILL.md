---
name: yt-07f-cat-theo-chu
description: Bước Cắt của quy trình YouTube Machine — cắt video quay, ghi màn hình hoặc podcast bằng cách đọc lời thay vì kéo dòng thời gian. Bóc lời có báo chi phí trước, lập bản cắt đề xuất bỏ câu hỏng, câu nói lại, khoảng lặng, từ đệm, cho người dùng duyệt bằng chữ, xem thử 60 giây, rồi xuất bản cắt cùng phụ đề theo thời gian mới. File gốc không bị đụng tới. Ghi videos/NNN-slug/4-dung/cat/ và 4-dung/NNN-slug-cat.mp4. Dùng khi người dùng nói "cắt video", "cắt khoảng lặng", "bỏ câu nói hỏng", "cắt theo lời", "bóc lời", "transcript video", "rough cut", "bản cắt", "cắt podcast", hoặc khi skill youtube-machine gọi bước Cắt của đường Quay trước, Màn hình, Tư liệu sẵn. Không dùng cho video đường Lời trước, nơi nhịp đã do giọng đọc quyết định.
---

# yt-07f-cat-theo-chu

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07f-cat-theo-chu/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
