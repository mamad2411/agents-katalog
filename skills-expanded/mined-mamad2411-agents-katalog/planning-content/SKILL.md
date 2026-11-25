---
name: planning-content
description: "Phân tích nội dung và lên kế hoạch outline chi tiết cho bài viết. Kích hoạt khi user muốn lên dàn ý, tạo outline, lập plan content, bóc ý từ tài liệu. CHỈ tập trung phân tích + outline ý chính, KHÔNG hướng dẫn cách viết, tone, style, hay cấu trúc trình bày."
disable-model-invocation: true
---

# Planning Content

Workflow: Phân tích Input → Research → Lên outline ý chính cho từng bài.

**Nguyên tắc cốt lõi:**

- Skill CHỈ làm 2 việc: (1) phân tích nội dung input, (2) xác định các ý chính cần cover trong từng bài.
- KHÔNG can thiệp cách viết, tone, style, cách sắp xếp section, mở bài, kết bài. Đó là việc của skill viết bài.
- Outline = bản đồ ý tưởng, KHÔNG phải bản nháp.

## Phase 1: Detect Input

Xác định loại input từ user:

- **Topic thuần** — chỉ có chủ đề, cần research từ đầu.
- **Notes/ý tưởng rời** — có sẵn ý, cần phân loại + mở rộng.
- **URL** — bài viết/tài liệu online, cần phân tích + bóc ý.
- **File/document** — tài liệu đã có, cần extract concepts.
- **Sách/tài liệu dài** — nhiều chương/concept, cần content map trước.

## Phase 2: Interview

Hỏi tất cả câu hỏi trong 1 lượt:

1. **Audience**: Người đọc chính là ai? (founder, marketer, developer, sinh viên...)
2. **Goal**: Mục tiêu chính? (educate / engage / convert / thought leadership)
3. *(Optional)* **Constraints**: Yêu cầu đặc biệt (deadline, topic cần tránh, kênh đăng).

*Fast-track: Nếu input đã đủ context hoặc user yêu cầu "làm luôn", giả định sensible defaults và sang Phase 3.*

### Edge Cases

- **Input quá ngắn (1-2 câu):** Hỏi user bổ sung context hoặc dùng web research mở rộng trước khi tạo outline.
- **Thiếu data cho 1 ý:** Note rõ "data gap" trong outline (field `Open questions`) để writer biết cần tìm thêm gì, hoặc đề xuất loại bỏ ý nếu không có cách tìm.
- **Topic quá rộng:** Narrow down qua Interview, yêu cầu user chọn góc cụ thể trước khi plan.

## Phase 3: Research

- WebSearch 3-5 queries liên quan topic + audience + trends.
- Nếu input là URL → WebFetch phân tích nội dung.
- Nếu input là file → đọc và bóc ý chính.
- Thu thập: data, số liệu, góc nhìn mới, content gaps, ví dụ thực tế, case study.
- **Bắt buộc cite nguồn** cho mọi data point.

## Phase 4: Map Content & Generate Outlines

### 4.1. Content Map (cho input dài)

Trước khi tạo outline cụ thể, lập **content map** tổng quan:

- Liệt kê toàn bộ concept/chương/ý lớn từ input.
- Group các ý liên quan thành cluster theo chủ đề.
- Đánh dấu ưu tiên (must-have / nice-to-have).

### 4.2. Generate Outlines

Đề xuất số lượng bài bao phủ toàn bộ nội dung input:

- **Topic thuần** → 3-10 bài (tùy scope).
- **Notes/ý tưởng rời** → theo số ý tưởng có sẵn.
- **URL/article** → 5-15 bài (tùy độ dài + density).
- **Sách/tài liệu dài** → bao phủ toàn bộ giá trị cốt lõi. Chia thành **batches** (mỗi batch ~10 bài).

**Nguyên tắc lên outline:**

- **1 bài = 1 chủ đề duy nhất.** Mỗi outline tập trung đúng 1 ý chính (concept, bài học, góc nhìn, câu chuyện).
- Outline = liệt kê **ý chính** bài cần cover. KHÔNG quy định cấu trúc trình bày, KHÔNG đề xuất framework viết.
- Mỗi ý chính phải có data/ví dụ hỗ trợ rõ ràng. Ý không có data → đánh dấu "cần tìm thêm" hoặc loại.
- Outline phải đủ rõ để writer hiểu **bài nói về cái gì** mà không cần đoán thêm ý chính. Cách trình bày là việc của writer.
- KHÔNG viết câu mở bài, câu kết, hay bất kỳ phần draft nào của bài hoàn chỉnh.

**Format mỗi outline:**

```
### Bài [N]: [Tiêu đề đề xuất]

- **Audience:** [Người đọc cụ thể của bài này]
- **Goal:** [Sau khi đọc, reader hiểu hoặc làm được gì]
- **Angle:** [Góc tiếp cận, bài này nhìn vấn đề từ hướng nào]
- **Thesis (ý cốt lõi):** [1 câu, ý duy nhất bài muốn truyền tải]
- **Key points cần cover:**
  - [Ý chính 1] | data/ví dụ: [...] | nguồn: [...]
  - [Ý chính 2] | data/ví dụ: [...] | nguồn: [...]
  - [Ý chính 3] | data/ví dụ: [...] | nguồn: [...]
- **Takeaway / insight chính:** [Reader rút ra điều gì]
- **Open questions:** [Data hoặc câu hỏi còn thiếu, writer cần tìm thêm. Nếu không có, ghi "Không"]
```

## Phase 5: Save Output

Lưu thành nhiều file để dễ quản lý:

- `{CWD}/{output-dir}/index.md` — overview + danh sách link tới các outline.
- `{CWD}/{output-dir}/outline-[NN]-[slug].md` — mỗi bài 1 file.
- `{CWD}/{output-dir}/research.md` — toàn bộ data đã research kèm sources.
- *(Input dài)* `{CWD}/{output-dir}/content-map.md` — content map + checklist coverage.

**Xử lý input dài theo batch:**

- Tạo content map trước, lưu vào `content-map.md`.
- Chia thành batches ~10 bài/batch, làm batch đầu tiên trước.
- **Checklist tiến độ** dạng markdown trong `index.md`:
  ```
  - [x] Batch 1 (Chương 1-3): 10/10 outlines
  - [ ] Batch 2 (Chương 4-6): 0/10
  ```
- **Coverage check (BẮT BUỘC):** Sau mỗi batch, đối chiếu content map. Liệt kê concept ĐÃ cover vs CHƯA cover. Lặp đến khi 100% content map có outline.
- Cập nhật `index.md` sau mỗi batch.
- Hỏi user confirm trước khi làm batch tiếp.

Cuối cùng hỏi: "Đã hoàn thành outline cho [N] bài. Bạn muốn điều chỉnh outline nào trước khi chuyển cho skill viết bài không?"

## Constraints

- Output tiếng Việt (trừ khi user yêu cầu khác).
- Mọi data point phải cite nguồn.
- KHÔNG đề xuất tone, style, cách trình bày, cấu trúc section, framework viết, độ dài bài.
- KHÔNG viết draft câu mở bài, câu kết, hay bất kỳ phần nào của bài hoàn chỉnh.
- Outline phải đủ rõ ý để writer không cần tự suy luận thêm ý chính.
- Default output dir: `{CWD}/planning-content/[topic-slug]/` nếu user không chỉ định.

## Output Format

**1. `index.md`:**

```
# Content Plan: [Topic]

## Overview
- Audience: [...]
- Goal: [...]
- Tổng số bài: [N]
- Nguồn input: [URL/file/topic]

## Danh sách Outlines
1. [Bài 1: Tiêu đề](outline-01-slug.md)
2. [Bài 2: Tiêu đề](outline-02-slug.md)
...

## Coverage Checklist (nếu input dài)
- [x] Batch 1 — 10/10
- [ ] Batch 2 — 0/10
```

**2. `outline-[NN]-[slug].md`:** chi tiết từng bài theo format ở Phase 4.2.

**3. `research.md`:** data + sources thu thập được.

**4. `content-map.md`** (input dài): toàn bộ concept map + cluster + ưu tiên.
