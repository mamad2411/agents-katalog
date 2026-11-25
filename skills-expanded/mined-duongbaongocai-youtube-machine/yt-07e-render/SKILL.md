---
name: yt-07e-render
description: Bước 7e của quy trình YouTube Machine — dựng video thật từ giọng đọc, SRT, ảnh và clip Flow theo kế hoạch 7d, bằng đường dựng hợp với máy người dùng. Dò cấu hình (GPU, RAM, ổ đĩa, Blender, CapCut, ffmpeg), đề xuất Blender hoặc CapCut, người dùng chốt và đổi được cho từng video. Đường Blender dùng tools/blender (ghép cảnh, parallax, nét động, HUD, nhạc, xuất MP4); đường CapCut dùng bản nháp xuất từ Flow AIC và checklist dựng tay. Có bản thử 1 phút trước khi render đầy đủ, kiểm tra âm lượng và file cuối. Ghi videos/NNN-slug/4-dung/. Dùng khi người dùng nói "dựng video", "render video", "ghép video", "xuất MP4", "edit video này", "dựng bằng Blender", "dựng bằng CapCut", "máy tôi có dựng nổi không", "nên dùng CapCut hay Blender", hoặc khi skill youtube-machine gọi bước 7e.
---

# yt-07e-render

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07e-render/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
