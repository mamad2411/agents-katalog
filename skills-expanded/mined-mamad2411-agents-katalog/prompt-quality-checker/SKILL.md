---
name: prompt-quality-checker
description: Kiểm tra và đánh giá chất lượng prompt/conversation theo 5 kỹ thuật Conversational Prompting (Few-Shot, Context Engineering, Decomposition, Extended Thinking, Self-Criticism). Sử dụng skill này bất cứ khi nào người dùng yêu cầu "kiểm tra prompt", "review prompt", "prompt này đã đủ rõ ràng chưa", "đánh giá prompt", "cải thiện prompt", "prompt này có ổn không", "check prompt", hoặc dán một prompt/đoạn hội thoại kèm theo bất kỳ câu hỏi nào về độ rõ ràng, độ đầy đủ, tính actionable, hay chất lượng tổng thể. Cũng kích hoạt khi người dùng hỏi "prompt này thiếu gì", "làm sao để prompt tốt hơn", hoặc muốn so sánh nhiều phiên bản prompt. Mục tiêu — giúp người dùng viết prompt rõ ràng hơn, đủ bước hơn, và actionable hơn trước khi gửi cho AI.
---

# Prompt Quality Checker

Skill này giúp đánh giá xem một prompt hoặc conversation đã áp dụng đầy đủ **5 kỹ thuật Conversational Prompting** hay chưa, và đưa ra gợi ý cải thiện cụ thể.

## Triết lý cốt lõi

Một prompt tốt không chỉ là "câu hỏi rõ ràng" — nó phải giúp AI hiểu **bối cảnh**, **định dạng mong muốn**, **các bước cần làm**, và **tiêu chí đánh giá kết quả**. 5 kỹ thuật dưới đây là khung kiểm tra để đảm bảo prompt đủ mạnh trước khi gửi.

Ghi nhớ nhanh: **VÍ DỤ** cho hay — **CONTEXT** đủ đầy — **CHIA NHỎ** ra đây — **NGHĨ SÂU** cho chín — **TỰ KIỂM** xong xài.

## 5 kỹ thuật kiểm tra

### 1. Few-Shot — Cho AI ví dụ mẫu
**Mục đích:** Giúp AI hiểu chính xác phong cách, định dạng, hoặc mức độ chi tiết mong muốn bằng cách đưa ra ví dụ cụ thể.

**Dấu hiệu prompt đã có Few-Shot:**
- Có ít nhất một ví dụ mẫu (input → output, hoặc "đây là mẫu tôi thích")
- Có reference tới tài liệu/email/format đã tồn tại
- Cụm từ thường thấy: "ví dụ như...", "theo phong cách này...", "giống như cái này..."

**Dấu hiệu prompt CHƯA có Few-Shot (khi cần):**
- Yêu cầu output có format/style cụ thể nhưng không có ví dụ
- Mô tả style bằng tính từ trừu tượng ("chuyên nghiệp", "thân thiện") mà không minh họa
- Tác vụ lặp lại nhưng không có mẫu tham chiếu

**Khi nào BẮT BUỘC cần Few-Shot:** Viết email/content theo tone riêng, format dữ liệu đặc thù, phân loại theo tiêu chí chủ quan.

**Khi nào KHÔNG cần:** Câu hỏi kiến thức chung, tác vụ đơn giản một bước, khi AI đã được dạy chuẩn rõ ràng.

---

### 2. Context Engineering — Nói rõ bạn là ai, cần gì, kết quả mong muốn
**Mục đích:** Cung cấp đủ bối cảnh để AI không phải đoán — ai đang hỏi, tại sao hỏi, kết quả dùng để làm gì.

**Dấu hiệu prompt đã có Context:**
- Nêu rõ vai trò/nghề nghiệp người hỏi ("Tôi là kế toán...", "Tôi là sinh viên năm 3...")
- Nêu rõ mục đích cuối ("để gửi sếp", "để học ôn thi", "để đăng LinkedIn")
- Nêu rõ đối tượng người đọc/người dùng kết quả
- Nêu ràng buộc (độ dài, ngôn ngữ, mức độ formal)

**Dấu hiệu prompt THIẾU Context:**
- Câu lệnh trống ("Viết email cho khách hàng") — không rõ khách hàng nào, về việc gì
- Không nói mục đích dùng output
- Không nói background/level của người hỏi (ảnh hưởng độ khó giải thích)

**Checklist Context tối thiểu:**
- [ ] **Ai** đang hỏi? (vai trò, nghề, level)
- [ ] **Cần gì** cụ thể? (output kiểu gì)
- [ ] **Để làm gì**? (mục đích dùng kết quả)
- [ ] **Ràng buộc** nào? (độ dài, format, tone, deadline)

---

### 3. Decomposition — Chia nhỏ vấn đề, hỏi từng phần
**Mục đích:** Tác vụ phức tạp nên được chẻ thành các bước nhỏ — giúp AI (và người hỏi) kiểm soát từng giai đoạn thay vì nhận một cục output khó sửa.

**Dấu hiệu prompt đã Decompose:**
- Liệt kê các bước/phần cần có ("1. Phân tích... 2. So sánh... 3. Kết luận...")
- Yêu cầu AI outline trước khi viết chi tiết
- Cụm từ: "Trước khi làm X, hãy...", "Đầu tiên..., sau đó..."
- Tách thành nhiều turn trong conversation thay vì nhồi hết vào 1 prompt

**Dấu hiệu prompt CHƯA Decompose (khi cần):**
- Yêu cầu output phức tạp (báo cáo, phân tích đa chiều, code lớn) trong 1 câu lệnh duy nhất
- Không nói thứ tự ưu tiên khi có nhiều yêu cầu cùng lúc
- Không yêu cầu kiểm tra/xác nhận ở giữa quá trình

**Gợi ý Decompose hiệu quả:**
- Bước 1: yêu cầu outline/kế hoạch
- Bước 2: review outline, điều chỉnh
- Bước 3: thực thi từng phần của outline
- Bước 4: ráp lại và tinh chỉnh

---

### 4. Extended Thinking — Cho AI suy nghĩ sâu trước khi trả lời
**Mục đích:** Với tác vụ đòi hỏi lập luận (logic, toán, phân tích chiến lược, debug code phức tạp), cho AI thời gian "suy nghĩ" trước khi trả lời sẽ cho kết quả chính xác hơn đáng kể.

**Dấu hiệu prompt đã kích hoạt Extended Thinking:**
- Bật chế độ "thinking"/"extended thinking" trong UI (nếu có)
- Yêu cầu AI suy luận từng bước ("think step by step", "hãy suy luận kỹ...")
- Yêu cầu AI xem xét nhiều góc độ trước khi kết luận
- Yêu cầu AI liệt kê giả định và kiểm tra từng giả định

**Dấu hiệu prompt CHƯA dùng Extended Thinking (khi cần):**
- Câu hỏi phức tạp (logic puzzle, chiến lược kinh doanh, debug sâu) nhưng kỳ vọng trả lời ngay
- Không yêu cầu AI giải thích lý do
- Tác vụ có nhiều ràng buộc/điều kiện nhưng không bảo AI cân nhắc từng cái

**Khi nào BẮT BUỘC cần Extended Thinking:** Toán, logic, phân tích chiến lược, debug code, ra quyết định có đánh đổi, review pháp lý/hợp đồng.

**Khi nào KHÔNG cần:** Trò chuyện, sáng tạo đơn giản, tra cứu thông tin.

---

### 5. Self-Criticism — Yêu cầu AI tự rà soát kết quả
**Mục đích:** AI đôi khi tự tin về câu trả lời sai. Yêu cầu nó tự phản biện/rà soát trước khi chốt giúp bắt lỗi logic, thiếu sót, hoặc điểm chưa thuyết phục.

**Dấu hiệu prompt đã có Self-Criticism:**
- Yêu cầu AI review/critique chính câu trả lời của nó
- Cụm từ: "Có chỗ nào thiếu logic không?", "Rà soát lại xem còn sai sót gì", "Tìm điểm yếu trong lập luận trên"
- Yêu cầu đưa ra counter-argument
- Hỏi "Điều gì có thể sai với câu trả lời này?"

**Dấu hiệu prompt CHƯA có Self-Criticism (khi cần):**
- Chỉ yêu cầu output, không yêu cầu kiểm tra
- Tin tưởng câu trả lời đầu tiên cho tác vụ quan trọng

**Khi nào BẮT BUỘC cần Self-Criticism:** Ra quyết định quan trọng, phân tích có rủi ro, nội dung công bố công khai, code sản xuất, tư vấn ảnh hưởng tài chính/sức khỏe.

---

## Quy trình đánh giá prompt

Khi người dùng đưa một prompt/conversation để review, hãy làm theo các bước:

### Bước 1: Đọc kỹ prompt và xác định mục tiêu
- Prompt này đang cố làm gì? (tác vụ sáng tạo, phân tích, tra cứu, code...?)
- Độ phức tạp/rủi ro ra sao? (quyết định ngành nghề nào cần kỹ thuật nào)

### Bước 2: Chạy checklist 5 kỹ thuật

Với mỗi kỹ thuật, đánh giá theo 3 mức:
- ✅ **Đã có** — prompt đã áp dụng tốt
- ⚠️ **Thiếu/chưa đủ** — nên bổ sung
- ➖ **Không cần** — kỹ thuật này không phù hợp với tác vụ này (giải thích tại sao)

### Bước 3: Trả lời theo format chuẩn

```
## Đánh giá prompt

**Mục tiêu prompt:** [tóm tắt 1 câu]

**Điểm checklist:**
- Few-Shot: [✅/⚠️/➖] — [nhận xét ngắn]
- Context Engineering: [✅/⚠️/➖] — [nhận xét ngắn]
- Decomposition: [✅/⚠️/➖] — [nhận xét ngắn]
- Extended Thinking: [✅/⚠️/➖] — [nhận xét ngắn]
- Self-Criticism: [✅/⚠️/➖] — [nhận xét ngắn]

**Điểm mạnh:** [1-2 điểm chính]

**Thiếu sót quan trọng nhất:** [tối đa 2-3 điểm ưu tiên sửa]

**Đề xuất prompt cải tiến:**
[Viết lại prompt đã bổ sung các kỹ thuật còn thiếu, giữ nguyên ý định gốc]
```

### Bước 4: Đưa ra prompt phiên bản cải tiến

Luôn luôn cho người dùng thấy **phiên bản prompt đã sửa** — đừng chỉ nói lý thuyết. Người dùng có thể copy-paste ngay để dùng.

## Nguyên tắc đánh giá

1. **Không áp dụng máy móc cả 5 kỹ thuật cho mọi prompt.** Một câu hỏi đơn giản như "Thủ đô Pháp là gì?" không cần Few-Shot hay Self-Criticism. Hãy đánh dấu ➖ cho những kỹ thuật không phù hợp và giải thích tại sao.

2. **Ưu tiên actionable feedback.** Thay vì nói "prompt chưa đủ context", hãy chỉ rõ *thiếu context gì* và *nên thêm gì*.

3. **Tôn trọng ý định gốc.** Khi đề xuất phiên bản cải tiến, không đổi mục tiêu của người dùng — chỉ làm cho prompt đủ rõ ràng hơn.

4. **Cảnh báo over-engineering.** Nếu prompt đã quá dài hoặc dùng nhiều kỹ thuật không cần thiết, hãy nói thẳng. Prompt tốt là vừa đủ, không phải nhiều nhất.

5. **Ngắn gọn, trực tiếp.** Đánh giá nên gọn — tránh dài dòng. Người dùng muốn biết ngay cái gì thiếu và cách sửa.

## Ví dụ áp dụng

**Prompt đầu vào của người dùng:**
> "Viết email xin nghỉ phép"

**Đánh giá:**

## Đánh giá prompt

**Mục tiêu prompt:** Soạn email xin nghỉ phép.

**Điểm checklist:**
- Few-Shot: ⚠️ — Không có ví dụ về phong cách email công ty bạn dùng.
- Context Engineering: ⚠️ — Thiếu: bạn là ai, gửi cho ai, nghỉ bao lâu, lý do, ngôn ngữ.
- Decomposition: ➖ — Tác vụ đủ đơn giản, không cần chia nhỏ.
- Extended Thinking: ➖ — Không phải tác vụ cần suy luận sâu.
- Self-Criticism: ➖ — Có thể bỏ qua với email đơn giản, trừ khi email rất nhạy cảm.

**Thiếu sót quan trọng nhất:** Context quá mỏng — AI sẽ phải đoán gần như mọi thứ.

**Đề xuất prompt cải tiến:**
> "Tôi là nhân viên marketing, cần viết email xin nghỉ phép 3 ngày (15-17/5) gửi sếp trực tiếp tên là anh Minh, lý do việc gia đình. Tone lịch sự nhưng không quá trang trọng, tiếng Việt, dưới 150 từ. Đây là mẫu email tôi từng gửi cho dễ tham khảo phong cách: [dán email cũ nếu có]."
