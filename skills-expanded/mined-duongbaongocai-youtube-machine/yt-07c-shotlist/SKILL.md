---
name: yt-07c-shotlist
description: Bước 7c của quy trình YouTube Machine — chia cảnh hình theo SRT của giọng đọc, mỗi dòng SRT (2-giong/NNN-slug.scenes.srt) là một cảnh, thời lượng cảnh lấy đúng theo giọng thật. Gán loại cảnh theo bộ phong cách 04b, viết prompt ảnh và chuyển động tiếng Anh, chọn cảnh nào làm clip video và cảnh nào giữ ảnh tĩnh, giữ nhân vật riêng của video đồng nhất bằng @TÊN, tính tín dụng Flow AIC theo các phương án, xuất danh sách cảnh và plan.json rồi đưa vào Flow AIC (nhập SRT, gắn giọng và phụ đề) để tạo hình khớp giọng. Dùng khi người dùng nói "chia cảnh theo srt", "tạo hình khớp giọng đọc", "prompt cho từng câu", "đưa srt vào flow", "danh sách cảnh", "shot list", "làm hình cho video", hoặc khi skill youtube-machine gọi bước 7c.
---

# yt-07c-shotlist

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07c-shotlist/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
