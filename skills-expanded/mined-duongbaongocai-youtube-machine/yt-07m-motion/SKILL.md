---
name: yt-07m-motion
description: Bước 7m của quy trình YouTube Machine — dựng motion graphics cho video khi người dùng yêu cầu, bằng HyperFrames (HTML render thành video), bám mốc từng từ của giọng đọc. Có hai chế độ, chèn đoạn motion hoặc lớp chữ trong suốt lên hình đã có, làm cả video bằng motion, và xen đồ họa vào video quay hoặc podcast. Các nhóm motion, chữ động (từ khóa theo giọng, chữ đóng vai vật thể, thẻ thoại, thẻ chương), lịch sử và số liệu (bản đồ, tuyến đường, dòng thời gian, đếm số, bảng thuộc tính, thẻ nhân vật), sơ đồ giải thích (sơ đồ lớn dần, ví dụ đi xuyên suốt), chuyển cảnh có nguyên cớ (vật thành cảnh sau, tràn màu, mở lỗ tròn, tua băng), mô phỏng và dữ liệu thật. Có duyệt khung trắng và tờ duyệt khung trước khi render, ghép vào MP4 mà không dựng lại Blender hay CapCut, tiếng hiệu ứng tự tạo, chuẩn hóa âm lượng. Ghi videos/NNN-slug/4-dung/motion/. Dùng khi người dùng nói "làm motion", "motion graphics", "chữ động", "kinetic type", "bản đồ động", "dòng thời gian động", "đếm số", "sơ đồ động", "chuyển cảnh đẹp hơn", "thêm motion vào video", "làm video toàn motion", "đồ họa cho podcast", "mô phỏng", "khung trắng", "edit motion đoạn này". KHÔNG tự chạy trong quy trình nếu người dùng chưa yêu cầu; dựng và xuất thường vẫn là yt-07e-render.
---

# yt-07m-motion

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-07m-motion/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
