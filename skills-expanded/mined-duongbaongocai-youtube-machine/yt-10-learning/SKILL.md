---
name: yt-10-learning
description: Bước 10 của quy trình YouTube Machine — vòng học từ số liệu thật của kênh. Thu CTR, thời lượng xem, điểm rời đi, nguồn hiển thị từ YouTube Studio (người dùng đọc hoặc xuất lại) và ý kiến của người dùng, so giữa các video, rút ra mẫu tiêu đề, thumbnail, hook, chủ đề, nhịp dựng đang thắng và đang thua, ghi learnings.md để mọi bước sau tự áp dụng, rồi đề xuất thay đổi cụ thể cho video kế tiếp và kế hoạch nội dung. Dùng khi người dùng nói "phân tích kênh", "video nào tốt nhất", "vì sao video này ít view", "rút kinh nghiệm", "số liệu tuần này", "CTR", "retention", "kênh không lên", "nên đổi gì", "tối ưu kênh theo số liệu", hoặc khi skill youtube-machine gọi bước 10 sau mỗi video đủ 48 giờ và sau mỗi 5 video.
---

# yt-10-learning

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "yt-10-learning/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
