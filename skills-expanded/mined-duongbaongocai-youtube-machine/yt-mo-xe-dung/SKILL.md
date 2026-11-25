---
name: yt-mo-xe-dung
description: Skill tùy chọn của quy trình YouTube Machine — mổ xẻ cách dựng video đối thủ (video reverse engineering) bằng số đo thật thay vì chỉ chụp màn hình. Nhận link YouTube hoặc file video, tải tạm rồi tự xóa, dò điểm cắt, nhịp cắt theo đoạn, tờ khung có số cảnh và mốc giờ, lời gắn theo cảnh, cú dội âm thanh trùng điểm cắt, khoảng lặng; trợ lý xem hết tờ khung rồi viết bản phân tích cấu trúc câu chuyện, ngữ pháp hình, chữ trên màn hình, âm thanh, và cơ chế học được cho kênh mình mà không chép. Ghi kenh/nghien-cuu/dung/<ma-video>/. Dùng khi người dùng nói "video này dựng thế nào", "học cách edit của kênh X", "mổ xẻ video", "phân tích cách dựng", "nhịp cắt của đối thủ", "video reverse engineering", "reverse engineer video", hoặc khi bước 2 và 7d đề xuất và người dùng đồng ý. KHÔNG dùng để tải lại, cắt đoạn hay đăng lại video của người khác.
---

# yt-mo-xe-dung

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-mo-xe-dung/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
