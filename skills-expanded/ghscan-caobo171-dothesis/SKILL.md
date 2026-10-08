---
name: dothesis-humanizer
description: Làm cho một chương/đoạn học thuật tiếng Việt (đã viết) đọc tự nhiên hơn, bớt "mùi AI", trong khi giữ NGUYÊN 100% số liệu, bảng, thuật ngữ và trích dẫn. Dùng khi người dùng nói "viết lại cho tự nhiên", "bị chê giống ChatGPT/AI", "humanize", "giảm mùi AI", "mượt lại chương này". Chạy qua DoThesis (kết nối bằng MCP connector "DoThesis" trong Claude).
---

# DoThesis Humanizer — mượt lại văn học thuật, giữ nguyên số liệu

Skill này gọi công cụ **`humanize`** của DoThesis (qua MCP connector). Nó *đổi cách văn được viết*, không đổi *nội dung*: mọi con số, p-value, β, tên bảng ("Bảng 4.3"), thuật ngữ (vd "KOLs", "phi xác suất") và trích dẫn được **đóng băng và kiểm tra lại** sau khi viết lại — bản nào làm sai một token là bị bỏ, giữ nguyên bản gốc.

## Nói thật với người dùng những điều này (một lần, trước khi chạy)

Đây là phần **bắt buộc** — nói sai làm hại người dùng:

- **Đây KHÔNG phải công cụ chống đạo văn.** "Đạo văn / similarity" (Turnitin similarity) là so trùng nguồn — humanize **không** kéo điểm đó xuống. Skill này chỉ giảm **mùi AI (AI-detection)**, hai thứ khác nhau.
- **Không đảm bảo qua máy quét của trường.** Công cụ tối ưu theo tín hiệu nội bộ, không phải máy dò cụ thể của hội đồng. Nó *giảm* mùi AI, không *bảo chứng* vượt Originality/GPTZero/Turnitin.
- **Số liệu và nghiên cứu giữ nguyên** — chỉ câu chữ đổi.
- **Đòn mạnh nhất vẫn là bạn tự đọc và sửa vài câu.** Chỗ bạn viết tay là tín hiệu "người thật" mạnh nhất. Skill lo phần thô; bạn chốt phần tinh.

Nếu người dùng đòi "đảm bảo pass đạo văn / pass Turnitin" → đính chính thẳng theo 2 gạch đầu dòng đầu, đừng hứa.

## Cách chạy

1. Lấy **chương/đoạn đã viết** (không phải đề bài — đây là công cụ mượt lại, không phải viết mới).
2. Gọi tool `humanize` của DoThesis với văn bản đó. Làm **theo từng phần/chương**, đừng ném cả luận văn một lần — đoạn ngắn giữ số liệu tốt hơn và mỗi chương có giọng khác nhau.
3. Nếu tool trả `error: "no_anchor"` → cần ~150 chữ **do chính người dùng viết** (bài cũ, báo cáo, bất cứ gì viết trước khi dùng AI) làm "neo giọng". Hỏi xin, rồi gọi lại với `user_anchor`. **Đừng tự bịa neo** — neo bịa làm kết quả tệ hơn (đây là phát hiện cốt lõi của công cụ).
4. Nếu trả `error: "frozen_violation"` → bản viết lại đã đụng số/trích dẫn nên bị giữ gốc. **Nói thẳng**, đừng báo là "đã humanize".

## Sau khi chạy

- Trả bản đã mượt + nêu rõ đoạn nào bị giữ nguyên (nếu có).
- Nhắc lại: đọc lướt, sửa tay vài câu còn gượng. Nếu người dùng chỉ ra câu cấn, giúp họ sửa 1-2 phương án.

## Không bao giờ

- Không quảng cáo/hứa "qua đạo văn" hay "đảm bảo qua detector".
- Không chạy khi chưa có neo giọng; không tự viết neo.
- Không báo "đã humanize" khi tool trả `ok: false`.
- Không đụng bảng số liệu — chỉ mượt phần văn xung quanh.
