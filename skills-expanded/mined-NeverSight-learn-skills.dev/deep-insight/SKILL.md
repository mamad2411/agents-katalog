---
name: deep-insight
description: "Hiểu sâu vấn đề bằng Quan sát, Phân tích, Đúc kết lõi."
---

# Deep Insight — Quan sát · Phân tích · Đúc kết

Skill giúp hiểu sâu bất kỳ vấn đề nào thông qua chu trình **ba bước tư duy**:

| Bước          | Bản chất                   | Mục tiêu                  |
| ------------- | -------------------------- | ------------------------- |
| **Quan sát**  | Thu thập đa chiều          | Thấy đủ — không bỏ sót    |
| **Phân tích** | Tách lớp, tìm liên kết     | Thấy rõ — cơ chế vận hành |
| **Đúc kết**   | Rút cốt lõi, nguyên lý hóa | Thấy sâu — nắm bản chất   |

Ba bước này là **chu trình lặp**, không tuyến tính. Mỗi vòng lặp đi sâu hơn vòng trước.

> **Nguyên tắc vàng**: Đúc kết không phải tóm tắt. Tóm tắt là rút gọn thông tin. Đúc kết là tìm ra **cái lõi chi phối tất cả những cái khác** — thứ mà khi nắm được, mọi thứ còn lại tự sáng tỏ.

### Nguyên tắc giải thích sâu

Phân tích giỏi mà giải thích dở thì user không được lợi gì. Mọi output phải tuân theo 4 nguyên tắc:

1. **Từ quen → lạ** — Mỗi khái niệm mới phải neo vào thứ user đã biết. Bắt đầu bằng ví dụ đời thường, rồi mới dẫn đến khái niệm trừu tượng. Lý do: não xử lý thông tin mới bằng cách gắn vào schema có sẵn.
2. **Ẩn dụ bắt buộc** — Mỗi insight trừu tượng cần ít nhất 1 ẩn dụ hoặc phép so sánh cụ thể. Ẩn dụ tốt = user "thấy" được cơ chế vận hành thay vì chỉ "đọc" mô tả.
3. **Giải thích "tại sao" trước "là gì"** — Không liệt kê kết luận. Dẫn dắt user qua quá trình suy luận: vấn đề → manh mối → kết nối → insight. User hiểu logic dẫn đến kết luận sẽ nhớ lâu hơn.
4. **Nhiều chiều = nhiều góc nhìn user** — Không chỉ phân tích đa chiều cho mình, mà trình bày đa chiều cho user: "Nếu bạn là X, bạn sẽ thấy... Nếu nhìn từ góc Y, lại thấy..." — giúp user tự xây dựng mental model đa diện.

**Failure modes cần tránh:**
- **Tóm tắt giả đúc kết** — Liệt kê ý chính rồi gọi là "cốt lõi". Nếu bỏ 1 ý mà hệ thống không sụp → chưa tìm được lõi.
- **Phân tích thiếu dữ liệu** — Vào phân tích khi chưa quan sát đủ rộng → kết luận phiến diện.
- **Sơ đồ mục lục** — Mind map chỉ liệt kê, không thể hiện nhân quả hay tương tác → không giúp hiểu vận hành.
- **Đúc kết bị động** — Đọc nhiều rồi chờ "ngộ" thay vì chủ động hỏi "cái gì chi phối tất cả?"
- **Thiếu hành động** — Hiểu sâu mà không biết phải làm gì tiếp = chưa đúc kết xong.

## References — đọc khi cần

| Khi cần | Đọc |
|---------|-----|
| Nền tảng triết học (ba gốc, nhân-duyên-quả) | `references/framework-foundation.md` |
| Kỹ thuật quan sát chi tiết | `references/observation-guide.md` |
| Patterns phân tích (tách lớp, nhân quả, tương tác) | `references/analysis-patterns.md` |
| Phương pháp đúc kết & sơ đồ hóa | `references/synthesis-methods.md` |
| Template output | `references/output-template.md` |

## Quy trình thực hiện

### Bước 0: Xác định đầu vào

Cần 3 thông tin. **Chỉ hỏi những gì user chưa cung cấp**, gộp 1 lần hỏi:

1. **Chủ đề / vấn đề cần hiểu sâu là gì?**
2. **Tài liệu đầu vào?** — files, URLs, hoặc kiến thức user đã có
3. **Mục đích hiểu sâu để làm gì?** — ra quyết định, dạy người khác, viết bài, giải quyết vấn đề...

Nếu user đã cung cấp đủ → vào thẳng Bước 1. Khi user không có tài liệu → dùng research (WebSearch, deep-research) làm nguồn chính.

### Bước 1: QUAN SÁT — Thu thập đa chiều

Mục tiêu: **Thấy đủ** — nhìn vấn đề từ nhiều góc, không bỏ sót chiều quan trọng.

**1.1. Đọc & tiêu hóa tài liệu đầu vào**

- Đọc toàn bộ tài liệu user cung cấp
- Ghi nhận: ý chính, thuật ngữ, mâu thuẫn, khoảng trống thông tin

**1.2. Quan sát đa chiều** — Nhìn vấn đề từ ≥5 góc:

| Chiều quan sát          | Câu hỏi bề mặt                                     | Câu hỏi đào sâu                                                            |
| ----------------------- | --------------------------------------------------- | --------------------------------------------------------------------------- |
| **Từ trên** (tổng quan) | Vấn đề này nằm trong hệ thống lớn nào?              | Nếu bỏ vấn đề này ra, hệ thống lớn hơn bị ảnh hưởng gì? Mức nào?           |
| **Từ dưới** (nền tảng)  | Cái gì làm nền, làm gốc cho vấn đề này?             | Nền tảng đó hình thành từ đâu? Có thể thay nền khác không?                  |
| **Từ trong** (cơ chế)   | Bên trong nó vận hành như thế nào?                   | Thành phần nào bỏ đi thì hệ thống sụp? Thành phần nào chỉ là phụ trợ?      |
| **Từ ngoài** (bối cảnh) | Môi trường xung quanh ảnh hưởng ra sao?             | Thay đổi 1 yếu tố bên ngoài → bên trong phản ứng thế nào? Có ngưỡng đột biến không? |
| **Theo thời gian**      | Nó thay đổi thế nào theo thời gian?                 | Nhân quả gần (tức thì) vs. xa (tích lũy) là gì? Xu hướng đang tăng tốc hay chậm lại? |
| **Liên đới**            | Vấn đề tương tự ở lĩnh vực khác vận hành ra sao?    | Cùng nguyên lý gốc hay chỉ giống bề ngoài? Pattern chung là gì?             |

**1.3. Research bổ sung** (nếu cần)

- Khi phát hiện khoảng trống thông tin → research thêm từ nguồn uy tín
- Có thể sử dụng skill `deep-research` nếu cần nghiên cứu chuyên sâu
- Có thể dùng `WebSearch` / `WebFetch` cho tra cứu nhanh
- Ưu tiên: sách, nghiên cứu học thuật, chuyên gia uy tín trong lĩnh vực

Output: Bản ghi quan sát theo từng chiều, đánh dấu mâu thuẫn và khoảng trống.

### Bước 2: PHÂN TÍCH — Tách lớp, tìm liên kết

Mục tiêu: **Thấy rõ** — hiểu cơ chế vận hành, mối quan hệ nhân quả.

**2.1. Tách lớp & giải thích lớp** — 4 tầng: Hiện tượng → Cơ chế → Nguyên nhân → Gốc rễ. Chi tiết & ví dụ: đọc `references/analysis-patterns.md` mục "Tách lớp".

Khi trình bày mỗi lớp cho user:
- **Bắt đầu từ lớp user đang thấy** (hiện tượng) → dẫn dắt xuống sâu hơn. Không nhảy thẳng vào gốc rễ.
- **Mỗi lớp cần câu cầu nối**: "Hiện tượng này xảy ra vì bên dưới có cơ chế X..." → "Cơ chế X tồn tại bởi nguyên nhân Y..." — user phải thấy logic nối lớp này sang lớp kia.
- **Mỗi lớp trừu tượng cần 1 ví dụ cụ thể** — nếu nói "feedback loop tự tăng cường", phải chỉ ra loop đó hoạt động như thế nào trong bối cảnh cụ thể đang phân tích.

**2.2. Phân tích nhân quả** — Theo chuỗi Nhân + Duyên = Quả. Luôn phân biệt **nhân quả gần** vs. **nhân quả xa**. Chi tiết: đọc `references/analysis-patterns.md` mục "Phân tích Nhân quả" và `references/framework-foundation.md` mục "Nhân - Duyên - Quả".

**2.3. Phân tích tương tác** — Các thành phần ảnh hưởng lẫn nhau thế nào:

- Vẽ sơ đồ tương tác (dùng Mermaid nếu phù hợp)
- Tìm feedback loops (vòng lặp tự tăng cường hoặc tự triệt tiêu)
- Nhận diện điểm leverage (can thiệp ít nhưng ảnh hưởng lớn)

**2.4. Quan sát liên đới** — So sánh với vấn đề tương tự:

- Lĩnh vực khác có vấn đề tương tự không?
- Cùng nguyên lý hay khác?
- Rút ra pattern chung

Output: Sơ đồ tách lớp, chuỗi nhân quả, sơ đồ tương tác.

### Bước 3: ĐÚC KẾT — Rút cốt lõi, nguyên lý hóa

Mục tiêu: **Thấy sâu** — nắm bản chất, biến thành nguyên lý có thể truyền đạt.

Đây là bước **khó nhất** — đòi hỏi **tác ý** (chủ động đặt câu hỏi), không thể làm bị động.

**3.1. Tìm LÕI** — Trả lời câu hỏi trung tâm:

> "Trong tất cả những gì đã quan sát và phân tích, **cái gì chi phối những cái khác**?"

Chi tiết 3 phương pháp tìm lõi ("Bỏ đi thử", "Giao nhau", "Câu hỏi đệ quy"): đọc `references/synthesis-methods.md`.

**3.2. Nguyên lý hóa & truyền đạt** — Biến insight thành dạng user thực sự tiêu hóa được:

- **Câu cốt lõi** (1 dòng) — Diễn đạt đơn giản nhất có thể, người không chuyên cũng hiểu.
- **Ẩn dụ minh họa** — So sánh với thứ quen thuộc trong đời thường để user "thấy" cơ chế vận hành.
- **"Điều này có nghĩa là..."** — Chuyển từ nguyên lý trừu tượng → hệ quả cụ thể mà user quan tâm. Trả lời: nếu hiểu được điều này, user sẽ làm khác đi như thế nào?
- **Kiểm chứng** — Test bằng 3 câu hỏi kiểm tra nhân quả (đọc `references/framework-foundation.md` mục "Ba câu hỏi kiểm tra nhân quả").

**3.3. Sơ đồ hóa** — Sơ đồ phải thể hiện **sự vận hành** (cái gì dẫn đến cái gì), không chỉ liệt kê. Dùng Mermaid flowchart/mindmap. Chi tiết: đọc `references/synthesis-methods.md` mục "Sơ đồ hóa".

**3.4. Kiểm tra chất lượng đúc kết** — 5 tiêu chí (chi tiết: `references/synthesis-methods.md` mục "Kiểm tra chất lượng"):

- **Cốt lõi**: Đã tìm được cái chi phối tất cả?
- **Giải thích lực**: Nguyên lý giải thích được bao nhiêu hiện tượng? (1-5)
- **Dự đoán lực**: Dự đoán được điều mới? (1-5)
- **Truyền đạt**: Người khác hiểu trong 2 phút? (1-5)
- **Hành động**: Biết phải làm gì tiếp?

**Tiêu chí dừng**: Nếu Cốt lõi = Có, Hành động = Có, và trung bình Giải thích + Dự đoán + Truyền đạt ≥ 3/5 → đúc kết đạt. Nếu chưa → quay lại Bước 1 hoặc 2 bổ sung, tối đa 2 vòng lặp.

## Format output

Dùng template mặc định từ `references/output-template.md`. Tuỳ mục đích user có thể điều chỉnh cấu trúc, nhưng giữ nguyên 3 phần chính: Quan sát → Phân tích → Đúc kết.

## Lưu report

Sau khi hoàn thành, lưu output vào:

```
{CWD}/deep-insight/{topic-slug}-{YYMMDD}.md
```

Tạo thư mục `{CWD}/deep-insight/` nếu chưa tồn tại. Thông báo đường dẫn file cho user.
