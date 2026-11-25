---
name: youtube-machine
description: Skill tổng điều phối quy trình xây kênh YouTube từ số 0 đến video đăng được và học từ số liệu, cho nhiều định dạng và thể loại (kể chuyện, giải thích, nói trước ống kính, review, hướng dẫn, vlog, podcast, gameplay, nhạc nền, dữ liệu, phim ngắn, Shorts), có cổng giá trị và chống lặp cho từng video. Dẫn dắt tuần tự các bước và luôn hỏi người dùng để làm rõ trước khi làm (dò máy chọn Blender hay CapCut → chọn ngách → đối thủ → từ khóa → thương hiệu → phong cách hình ảnh và nhân vật → tạo kênh → kế hoạch nội dung → kiểm tra chính sách → kiểm tra nhu cầu từng video → kịch bản lời đọc liền mạch → giọng ElevenLabs và SRT → chia cảnh theo SRT, tạo hình khớp giọng → kế hoạch dựng giữ chân → dựng video → SEO đăng video → sau khi đăng → học từ số liệu), lưu hồ sơ trong thư mục kênh và nhớ tiến độ để làm tiếp lần sau. Dùng skill này BẤT CỨ KHI NÀO người dùng muốn "xây kênh YouTube", "mở kênh mới", "làm kênh từ đầu", "bắt đầu kênh faceless / Shorts", "làm kênh quay thật", "làm kênh hướng dẫn, review, podcast", "video không bị lặp", "tiếp tục kênh X", "kênh của tôi đang tới bước nào", hỏi "nên làm kênh gì", hoặc nhắc tới bất kỳ bước nào trong quy trình mà chưa có hồ sơ kênh — kể cả khi không nói tên skill. Nếu người dùng chỉ cần một bước lẻ và đã có hồ sơ kênh, gọi thẳng skill yt-XX tương ứng.
---

# youtube-machine

Nội dung skill này nằm trên máy chủ YouTube Machine. Gọi công cụ `ytm_doc` với `duong_dan: "youtube-machine/SKILL.md"` và làm theo nội dung trả về.

Mọi đường dẫn `.claude/skills/...` trong đó cũng đọc bằng `ytm_doc` (bỏ phần `.claude/skills/`). Chưa đăng nhập thì gọi `ytm_trang_thai` rồi `ytm_dang_nhap`, theo luật đầu tiên trong AGENTS.md. Không làm theo trí nhớ.
