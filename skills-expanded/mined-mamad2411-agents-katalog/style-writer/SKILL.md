---
name: style-writer
description: "Viết theo voice/structure hoặc phân tích DNA văn phong. Trigger: viết lại, clone giọng, stylometry, tạo voice."
---

# Style Writer

Skill quản lý văn phong viết lách, gồm 2 workflow:

| Workflow                | Mục đích                                         | Khi nào dùng                                       |
| ----------------------- | ------------------------------------------------ | -------------------------------------------------- |
| **Writer** *(mặc định)* | Viết nội dung dựa trên input + voice + structure | User muốn viết bài, viết lại nội dung, tạo content |
| **Analyze**             | Bóc tách DNA văn phong từ corpus → tạo voice mới | User muốn phân tích cách viết, tạo voice mới       |


**Mặc định: Workflow Writer.** Khi user gọi skill mà không chỉ định rõ workflow, dùng ngay **Writer** (đi thẳng đến mục `## Workflow 2: Writer` bên dưới).

Chỉ dùng **Analyze** khi user nói rõ ý định phân tích/bóc tách văn phong, ví dụ: "phân tích văn phong", "clone giọng văn", "tạo voice mới", "stylometry", "fingerprint viết lách", "phân tích cách viết của X".

Nếu thực sự mơ hồ (ví dụ user vừa nhắc tới phân tích vừa nhắc tới viết bài) → hỏi user chọn workflow nào.

---

## Workflow 1: Analyze

Bóc tách DNA văn phong từ tập bài viết của MỘT tác giả, trả về **voice file** markdown theo template cố định. File output lưu vào `references/voices/` để Workflow Writer dùng lại.

### Vai trò

Chuyên gia phân tích văn phong (stylometry & literary analysis) 15 năm kinh nghiệm. Mỗi đặc điểm phát biểu phải có trích dẫn nguyên văn từ corpus. Không bằng chứng → không ghi nhận.

**Bạn KHÔNG generate bài mới, KHÔNG so sánh tác giả, KHÔNG đánh giá hay/dở. Chỉ mô tả khách quan hình thức cách viết, có bằng chứng.**

### Bước 1. Thu thập corpus (Văn)

User có thể cung cấp corpus theo 3 cách. Detect và xử lý tương ứng:

**a. File/folder local** — user cho path `.txt`/`.md` hoặc folder.

- File đơn: `Read` file.
- Folder: `Glob` pattern `**/*.{md,txt}`, `Read` từng file, nối lại phân tách bởi `---`.

**b. Paste trực tiếp** — user dán nội dung vào chat, bài phân tách bởi `---`.

- Không cần load file, dùng luôn nội dung trong tin nhắn.

**c. URL (Substack/blog)** — user cho URL newsletter hoặc bài riêng lẻ.

- Nếu là Substack: ưu tiên dùng skill `substack-tools` (có `substack_crawl.py`).
- Nếu là blog khác: dùng `WebFetch` từng URL, extract nội dung main article.
- Nếu là URL mục lục (archive page): fetch trước để lấy danh sách URL bài, rồi fetch từng bài.

**Kiểm tra cỡ corpus**: tối thiểu 3 bài để có pattern đáng tin. Dưới 3 bài → báo user biết giới hạn, vẫn làm nhưng ghi rõ "dữ liệu hạn chế" trong output.

**Hỏi tên tác giả** nếu user chưa cung cấp — dùng cho tên file output và heading.

### Bước 2. Phân tích 8 chiều (Tư)

Đọc `references/analysis-dimensions.md` để có guide chi tiết từng chiều với ví dụ cụ thể cần tìm gì.

Tóm tắt 8 chiều:

1. **Giọng điệu & vai người kể** — Formal level (1-5), tone, ngôi xưng, distance với reader, thái độ.
2. **Cấu trúc bài** — Pattern mở bài, xương sống triển khai, pattern kết bài.
3. **Nhịp & độ dài câu** — Độ dài TB, câu cụt, tỷ lệ đơn/phức/ghép, thủ pháp nhịp.
4. **Từ vựng đặc trưng (fingerprint)** — 10-20 từ/cụm tác giả hay dùng, slang, thuật ngữ, filler.
5. **Kỹ thuật tu từ** — Metaphor domain, nguồn ví dụ, cách chuyển đoạn, cách dùng hài.
6. **Format & typography** — Heading, list, bold, đoạn dài, emoji, em-dash, whitespace.
7. **Tư duy & logic** — Pattern lập luận, xử lý counter-argument, tuyệt đối vs. nuance.
8. **Quirks cá nhân** — Thói quen riêng, tagline, cách đặt câu hỏi, pattern lặp ≥3 lần.

**Nguyên tắc cốt lõi**: không bằng chứng → không ghi nhận. Pattern phải lặp ≥2 lần ở ≥2 bài. Thiếu data → ghi "Không đủ dữ liệu", không bịa. Chi tiết evidence rules (trích dẫn nguyên văn ≤30 từ, tham chiếu bài, v.v.) xem `references/anti-patterns.md` mục A.

### Bước 3. Xuất voice file (Tu)

Đọc `references/output-template.md` để lấy template chính xác.

**Tên file output**: `references/voices/<ten-tac-gia-kebab-case>.md`

- VD tác giả "Nguyễn Văn A" → `references/voices/nguyen-van-a.md`.
- Nếu file đã tồn tại, hỏi user: ghi đè, đổi tên (thêm date suffix), hay skip.

**Sau khi ghi file**, cập nhật bảng **Voices có sẵn** trong SKILL.md này (thêm dòng mới), rồi báo user:

```
Đã tạo: [path file]
- Bản chất: [1 câu ≤25 từ mô tả văn phong]
- Signature phrases: "[cụm 1]", "[cụm 2]", "[cụm 3]"
- Độ tin cậy: [Rất thấp / Trung bình / Khá / Cao] — [N bài]
```

### Ràng buộc và self-check (Analyze)

Mọi ràng buộc (must NOT) và checklist verify cuối nằm trong `references/anti-patterns.md`:

- **Mục A-F**: anti-patterns phân nhóm (bằng chứng, form vs content, đánh giá, so sánh, cỡ mẫu, template). Đọc khi cần hiểu lỗi cụ thể.
- **Mục H**: checklist 12 ô cuối cùng trước khi ghi file. Đi qua từng ô, fail bất kỳ ô nào → sửa trước khi `Write`. Không ghi draft cẩu thả rồi hứa "sẽ sửa sau".

### Cỡ corpus và độ tin cậy

| Số bài | Độ tin cậy | Ghi chú khi xuất                             |
| ------ | ---------- | -------------------------------------------- |
| 1-2    | Rất thấp   | Ghi rõ "style guide sơ bộ, cần thêm corpus"  |
| 3-5    | Trung bình | Đủ pattern cơ bản, một số chiều có thể thiếu |
| 6-10   | Khá        | Đủ cho hầu hết chiều                         |
| 10+    | Cao        | Đáng tin, có thể dùng để training            |


Luôn ghi số bài đã phân tích vào phần metadata đầu style guide.

---

## Style Catalog

Danh mục style guide có sẵn, chia 2 category:

- **Voices** — giọng điệu (gồm cả giọng generic như teacher/storyteller và giọng cá nhân do Workflow Analyze tạo ra). Voice chứa **da thịt** (giọng, nhịp, kỹ thuật, verbal tics, exemplars).
- **Structures** — khung cấu trúc bài viết (story arc, BLUF, building blocks...). Structure chứa **xương** (phases, opening palette, arc patterns, content-type adaptation). Mỗi structure có recommended voice.

### Voices có sẵn

| Voice        | Slug           | Tóm tắt 1 dòng                                                           | Khác biệt chính                                                         | File                                                        |
| ------------ | -------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| Teacher      | `teacher`      | Dạy bài bản, giải thích khái niệm từng bước, scaffolding cho người mới.  | vs Guide: thuần giáo dục, không triết học Đông-Tây                      | [voices/teacher.md](references/voices/teacher.md)           |
| Storyteller  | `storyteller`  | Kể chuyện chánh niệm, hành trình ngôi "tôi", trải nghiệm > lý thuyết.    | vs Personal: có Thầy (embedded dialogue), metaphor không gian/thời tiết | [voices/storyteller.md](references/voices/storyteller.md)   |
| Objective    | `objective`    | Trung lập, dữ liệu, phân tích, giọng báo chí nghiêm túc.                 | vs Investigator: trình bày trung lập + khuyến nghị, không phản biện sâu | [voices/objective.md](references/voices/objective.md)       |
| Investigator | `investigator` | Điều tra, đặt câu hỏi, dẫn dắt người đọc tự khám phá qua manh mối.       | vs Objective: đặt câu hỏi thật, phản biện sâu, không kết luận cứng      | [voices/investigator.md](references/voices/investigator.md) |
| Guide        | `guide`        | Hướng dẫn cụ thể, actionable, đi kèm người đọc như một mentor đồng hành. | vs Teacher: thêm lớp triết học + thực nghiệm, câu flowing dài hơn       | [voices/guide.md](references/voices/guide.md)               |
| Personal     | `personal`     | Cá nhân, tự sự, reflective; kể chuyện mình để reader chiếu vào.          | vs Storyteller: không có Thầy, tự vấn trực tiếp, metaphor cơ thể/đồ vật | [voices/personal.md](references/voices/personal.md)         |
| Dialogue     | `dialogue`     | Đối thoại thầy-trò (format C:/T:), triết lý qua hỏi-đáp.                 | Format riêng biệt, không trùng voice nào                                | [voices/dialogue.md](references/voices/dialogue.md)         |


### Structures có sẵn

Mỗi structure định nghĩa khung cấu trúc bài viết: phases, opening palette, arc pattern (nếu có), content-type adaptation, quality checklist.

| Structure       | Slug              | Recommended Voice | Arc Pattern       | Best for                               | File                                                                      |
| --------------- | ----------------- | ----------------- | ----------------- | -------------------------------------- | ------------------------------------------------------------------------- |
| Story Arc       | `story-arc`       | storyteller       | Growth Journey    | Bài có hành trình thời gian            | [structures/story-arc.md](references/structures/story-arc.md)             |
| BLUF-Evidence   | `bluf-evidence`   | objective         |                   | Bài cần kết luận trước, chứng minh sau | [structures/bluf-evidence.md](references/structures/bluf-evidence.md)     |
| Building Blocks | `building-blocks` | teacher           |                   | Bài xây kiến thức từng bước            | [structures/building-blocks.md](references/structures/building-blocks.md) |
| Spiral Return   | `spiral-return`   | personal          | Quiet Devastation | Bài quay lại chủ đề, mỗi lần sâu hơn   | [structures/spiral-return.md](references/structures/spiral-return.md)     |
| Five Layers     | `five-layers`     | investigator      |                   | Bài đào sâu 5 tầng                     | [structures/five-layers.md](references/structures/five-layers.md)         |
| Master-Student  | `master-student`  | dialogue          |                   | Bài đối thoại thầy-trò                 | [structures/master-student.md](references/structures/master-student.md)   |
| Depth-Practice  | `depth-practice`  | guide             | Transformation    | Bài chiều sâu + thực hành              | [structures/depth-practice.md](references/structures/depth-practice.md)   |
| Adaptive        | `adaptive`        | (any)             |                   | Nội dung hỗn hợp                       | [structures/adaptive.md](references/structures/adaptive.md)               |


### Thêm voice mới

Có 2 cách:

**a. Bóc tách từ corpus có sẵn** (giọng cá nhân, fingerprint mạnh):

- Dùng **Workflow 1: Analyze** để phân tích DNA từ tập bài viết. Output tự động lưu vào `references/voices/` và cập nhật bảng.

**b. Soạn voice generic mới** (không có corpus, design từ đầu):

1. Soạn file `<slug>.md` (kèm exemplars).
2. File tối thiểu cần: Philosophy, Voice, Language (DO/DON'T), Core Techniques, Verbal Tics, Metaphor Bank, Pacing Rules, Quality Checklist (Voice), Exemplars.
3. Arc pattern (nếu có) → thêm vào structure tương ứng, không vào voice file.
4. Lưu vào `references/voices/`.
5. Thêm dòng mới vào bảng **Voices có sẵn**.

### Thêm structure mới

1. Soạn file `<slug>.md` với frontmatter (name, recommended_voice, best_for, version).
2. File tối thiểu cần: Overview, Phases (từng giai đoạn + Opening Palette), Content-Type Adaptation, Quality Checklist.
3. Lưu vào `references/structures/`.
4. Thêm dòng mới vào bảng **Structures có sẵn**.

---

## Workflow 2: Writer

Viết nội dung dựa trên input của user, áp dụng voice + structure đã chọn.

**Tài liệu hỗ trợ** (đọc khi cần):

- `references/value-framework.md` — framework đảm bảo giá trị nội dung
- `references/shared-rules.md` — quy tắc chung (nhịp thở, dấu câu, checklist hình thức, opening palette)

### Bước 1. Nhận input

User cung cấp nội dung đầu vào theo 1 trong các dạng:

- **Outline / ý tưởng**: gạch đầu dòng, bullet points, notes thô.
- **Bài viết cần viết lại**: bài gốc cần rewrite theo style khác.
- **Chủ đề**: mô tả chủ đề, user muốn viết bài mới.
- **Transcript / raw notes**: nội dung thô cần chuyển thành bài viết.

### Bước 2. Đào insight

Đọc `references/value-framework.md` phần "Đào Insight" và "Reader Empathy". Trả lời 4 câu hỏi bắt buộc:

1. **Điều mới**: Input nói gì mà người đọc phổ thông CHƯA biết?
2. **Góc nhìn**: Góc nào chưa ai khai thác?
3. **"À, hóa ra"**: Người đọc sẽ bất ngờ ở chỗ nào?
4. **Một câu cốt lõi**: Nếu người đọc chỉ nhớ 1 câu, câu đó là gì?

Xác định reader profile: người đọc là ai, họ đã biết gì, đang đau ở đâu, sau khi đọc họ làm gì.

**Nếu không trả lời được** → chưa viết. Hỏi user thêm thông tin, hoặc đề xuất góc nhìn mới.

### Bước 3. Xác định voice

Nếu user đã chỉ định → dùng ngay. Nếu chưa → hỏi user chọn voice từ bảng **Voices có sẵn** (có cả giọng generic như teacher/storyteller và giọng cá nhân do Analyze tạo). Load file voice tương ứng.

### Bước 4. Xác định structure (optional)

Nếu user đã chỉ định → dùng ngay. Nếu chưa:

1. Đề xuất structure dựa trên `recommended_voice` mapping trong bảng Structures.
2. User confirm hoặc chọn structure khác.
3. Nếu user không muốn structure cụ thể → dùng `adaptive`.

Load file structure tương ứng.

### Bước 5. Viết bài

1. **Read** toàn bộ file voice + structure + `references/shared-rules.md`.
2. **Phân tích input**: xác định content type (narrative/conceptual/tutorial/analysis/mixed) để apply Content-Type Adaptation trong structure.
3. **Viết** theo:
  - **Insight cốt lõi** (từ Bước 2): mọi đoạn phục vụ insight này.
  - **Voice**: giọng, nhịp, kỹ thuật, anti-patterns, verbal tics.
  - **Structure**: phases, opening palette (chọn 1 technique), transitions.
  - **Value**: mỗi đoạn pass "Vậy thì sao?" test (xem `references/value-framework.md`).
4. **Self-critique**: chạy qua Quality Checklist của cả voice VÀ structure VÀ Base Checklist (`references/shared-rules.md`).
5. Fix bất kỳ lỗi nào trước khi sang bước tiếp.

### Bước 6. Revision

Đọc `references/value-framework.md` phần "Revision Protocol" và "Reader Impact Checklist".

1. **Đọc lại như người đọc**: chỗ nào phải đọc 2 lần thì viết lại.
2. **"Vậy thì sao?" sweep**: đoạn nào không pass → cắt hoặc nối.
3. **Đoạn yếu nhất**: mạnh lên hoặc cắt đi.
4. **Share test**: "Tôi có share bài này không?" Không → sửa.
5. **Reader Impact Checklist**: chạy 8 ô kiểm tra giá trị. Fail bất kỳ ô nào → sửa trước khi output.

### Bước 7. Output

Trả bài viết hoàn chỉnh, sẵn sàng publish. Không heading meta, không label structure/voice, không commentary. Chỉ bài viết thuần túy.

Sau bài viết, ghi ngắn:

- Voice, structure, content type detected
- Insight cốt lõi (1 câu)
- Quality level tự đánh giá: Đạt / Tốt / Xuất sắc (xem rubric trong `references/value-framework.md`)

### Ràng buộc Writer

- KHÔNG tự chọn style. User phải chọn hoặc confirm đề xuất.
- KHÔNG viết nếu chưa load voice. Hỏi user trước.
- KHÔNG viết nếu chưa xác định insight cốt lõi (Bước 2). Chất lượng nội dung quan trọng hơn tốc độ.
- Output phải pass CẢ form checklist (`references/shared-rules.md` + voice + structure) VÀ value checklist (`references/value-framework.md`).
- Bài viết phải đọc như người viết, không như AI. Tuân thủ mọi anti-pattern trong voice.
- Kết bài theo phân loại voice category (xem `references/shared-rules.md` phần "Kết Bài").

---

## Quy ước file style guide

- **Voice (designed)**: philosophy + voice + language + core techniques + verbal tics + metaphor bank + pacing rules + quality checklist (voice) + exemplars. KHÔNG chứa phases/arc pattern (đó thuộc structure). Quy tắc chung (nhịp thở, dấu câu) nằm trong `references/shared-rules.md`.
- **Voice (analyzed từ Workflow Analyze)**: theo output chuẩn 8 chiều + signature phrases + công thức + anti-patterns + AI anti-patterns. Lưu chung folder `references/voices/`.
- **Structure**: frontmatter (name, recommended_voice, best_for) + phases + opening palette + arc pattern (nếu có) + content-type adaptation + quality checklist (structure). Opening Palette master list nằm trong `references/shared-rules.md`.

## Nguyên tắc

- **Single source of truth**: mỗi voice một file duy nhất trong skill này. Skill/AI khác reference bằng path, không copy nội dung đi nơi khác. Quy tắc chung nằm trong `references/shared-rules.md`, không copy vào từng voice.
- **Giá trị > Hình thức**: bài viết đẹp mà rỗng thì vô giá trị. Luôn đào insight trước khi viết. Xem `references/value-framework.md`.
- **Fingerprint > generic**: voice tốt phải có nét nhận dạng mạnh (signature phrase, quirks, pattern rõ ràng), đủ để phân biệt qua 3 câu đầu.
- **Viết như người, không như AI**: tuân thủ mọi anti-pattern trong voice. Output phải pass quality checklist.
