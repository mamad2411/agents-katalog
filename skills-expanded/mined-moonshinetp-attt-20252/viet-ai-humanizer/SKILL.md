---
name: viet-ai-humanizer
description: "Phát hiện và tự động sửa dấu hiệu AI trong văn bản tiếng Việt — không đánh giá, chỉ fix thẳng. Dùng khi: bài cần humanize, bớt mùi AI, viết lại tự nhiên hơn. Trigger bất cứ khi nào người dùng paste văn bản tiếng Việt và hỏi có vẻ AI không, hoặc dùng từ: 'kiểm tra AI', 'chỉnh bài AI', 'humanize', 'bớt mùi AI', 'viết lại tự nhiên hơn'."
---

# Viet AI Humanizer

Phát hiện và loại bỏ dấu hiệu AI trong văn bản tiếng Việt. Giữ nguyên ý nghĩa và giọng văn gốc — chỉ can thiệp chỗ "lộ AI".

Một dấu hiệu đơn lẻ không đủ kết luận là AI. Tìm **cụm** dấu hiệu.

---

## Bước 1: Phân tích dấu hiệu

### Nhóm 1 — Ngôn ngữ máy móc

- **Câu khuôn:** "Trong bối cảnh X đang phát triển…", "Trong thời đại số hiện nay…", kết bằng "Tóm lại / Kết luận là"
- **Từ nối sáo:** Hơn nữa, Thêm vào đó, Bên cạnh đó, Không những vậy (liên tục)
- **Ngôn ngữ quảng cáo:** độc đáo, ấn tượng, vượt trội; "đóng vai trò then chốt / là minh chứng cho / đánh dấu bước ngoặt"
- **Signposting:** "Hãy cùng tìm hiểu…", "Dưới đây chúng ta sẽ khám phá…"
- **Mệnh đề phụ rỗng:** "…, qua đó thể hiện cam kết…", "…, từ đó cho thấy sự chuyển dịch…"
- **Copula avoidance:** "đóng vai trò là" → "là"
- **Bộ ba ép buộc:** ép ý thành nhóm 3 dù chỉ có 2 hoặc 4 ý thật
- **Persuasive tropes:** "Điều thực sự quan trọng là / Bản chất của vấn đề là" → câu sau chỉ nhắc lại điều đã nói
- **Lặp luận điểm:** cùng ý xuất hiện nhiều đoạn, chỉ đổi cách diễn đạt

### Nhóm 2 — Format rối

- **Bullet nông:** "Dưới đây là một số…", các ý chung chung/trùng, dùng list thay vì đoạn văn
- **Inline-header list / Header + câu lặp:** câu ngay sau header chỉ nhắc lại header
- **Bold / emoji trang trí:** in đậm hoặc emoji không nhấn mạnh nội dung thật

### Nhóm 3 — Em-dash thừa

Dấu `—` từ 2 lần trở lên trong đoạn ngắn, đặc biệt dạng kẹp: "chiến dịch này — triển khai quý 3 — đạt…"

### Nhóm 4 — Giọng chatbot

"Bạn đã hỏi tôi về…", "Chắc chắn rồi!", "Đây là câu hỏi rất hay!", "Hy vọng bài viết hữu ích!"

### Nhóm 5 — Cấu trúc yếu

- **Synonym cycling:** cùng một thứ nhưng gọi nhiều tên — chiến dịch/kế hoạch/chương trình
- **False ranges:** "từ chiến lược đến thực thi" — nghe toàn diện nhưng vô nghĩa
- **Excessive hedging:** "có thể có lẽ dường như" chồng nhau
- **Passive voice thừa:** "Kết quả được ghi nhận là…", "Điều này được xem là…"
- **Filler phrases:** "Trong bối cảnh đó / Nhìn vào thực tế / Điều quan trọng cần lưu ý là"
- **Mục "Thách thức và Triển vọng" khuôn:** "Mặc dù… vẫn thách thức… nhưng tương lai sáng"

**False positives — không gắn cờ:** một từ nối đơn lẻ, một dấu `—`, thuật ngữ chuyên ngành, số liệu có nguồn, chi tiết cụ thể — đây là tín hiệu người thật.

---

## Bước 2: Liệt kê + sửa

Liệt kê từng dấu hiệu: `[Loại]: "[trích dẫn]" → [cách sửa]`

**Dịch EN→VN tự động** với từ tiếng Anh có từ tương đương thông dụng trong tiếng Việt. Giữ tiếng Anh khi là tên riêng, thuật ngữ không có từ tương đương, hoặc văn bản dùng Anh-Việt có chủ đích.

**Bảng sửa — áp dụng cứng:**

| Dấu hiệu | Cách sửa |
|----------|----------|
| Câu mở đầu khuôn | Xóa, viết thẳng vào ý chính |
| Từ nối sáo / filler / signposting | Xóa nếu câu vẫn đủ nghĩa; thay từ cụ thể nếu cần nối ý |
| Ngôn ngữ quảng cáo | Thay bằng mô tả cụ thể |
| Mệnh đề phụ rỗng | Xóa |
| Copula avoidance | Đổi thành "là" |
| Bộ ba ép buộc | Xóa ý thừa/giả tạo, giữ số ý thật |
| Persuasive tropes | Xóa câu intro, giữ nội dung phía sau |
| Lặp luận điểm | Xóa đoạn lặp, giữ đoạn diễn đạt tốt nhất |
| Bullet list nông | Gộp thành đoạn văn |
| Header + câu lặp | Xóa câu nhắc lại header |
| Bold / emoji thừa | Xóa hết |
| Em-dash (`—` `–`) | Thay bằng dấu phẩy hoặc tách câu. Không để lại `—` nào. |
| Giọng chatbot / xu nịnh | Xóa toàn bộ |
| Kết bài sáo | Viết lại có luận điểm riêng |
| Synonym cycling | Chọn từ đầu tiên, dùng nhất quán |
| False ranges | Xóa |
| Excessive hedging | Giữ tối đa một từ phòng thủ/câu |
| Passive voice thừa | Chuyển chủ động khi rõ chủ thể |
| Mục "Thách thức & Triển vọng" khuôn | Xóa nếu không có thông tin cụ thể |

---

## Bước 3: Xuất

```
## Bản đã chỉnh sửa
[Toàn bộ văn bản]

---
Thay đổi:
- [mỗi dòng một thay đổi chính]
```

Bài >1.500 từ: hỏi người dùng muốn bắt đầu từ phần nào.
