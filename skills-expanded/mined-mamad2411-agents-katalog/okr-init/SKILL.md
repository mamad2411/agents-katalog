---
name: okr-init
description: "Dùng khi `/okr` cần tạo hoặc sửa objective, KR, KI, period, deadline, resources, capacity, skill, tool, ngân sách. Gọi trực tiếp chỉ khi người dùng gõ `/okr-init`."
---

# okr-init: Khởi tạo + cập nhật objective & resource

Skill duy nhất quản lý 2 SOT khởi tạo: `objective.md` và `resources.md`. Hỗ trợ tạo mới và cập nhật.

> **Tiên quyết**: Skill `okr` (orchestrator) PHẢI load trước khi skill này chạy. Context từ orchestrator đã có sẵn (SOT ownership, shared schemas, quality gate), KHÔNG đọc lại.

## Nguyên tắc

- Hỏi từng câu một, không hỏi hàng loạt.
- BẮT BUỘC có phase confirm bảng trước khi ghi/sửa file.
- Tận dụng context user truyền từ `/okr`. Vd: "/okr thêm Dũng vào dự án QA 80%" → vào `update-resource` ngay với context Dũng.
- Đề xuất + lý do, để user quyết. Không tự áp đặt.

## Quality Gate

Áp dụng Quality Gate (đã có trong context từ orchestrator). Áp dụng trước khi tiến hành các phase hỏi user.

Ví dụ áp dụng cho mode `new` / `update-objective`:

- "Đủ cụ thể?" → "tăng doanh thu" FAIL vì chưa nói kênh nào, sản phẩm nào, bao nhiêu %.
- "Giả định ẩn?" → "launch Q4" nhưng chưa nói capacity có đủ không.
- "Mâu thuẫn?" → muốn 12 bài/tháng nhưng capacity Solo Profile chỉ 8h/tuần.

Mode `update-resource` áp dụng câu 1 chính (tài nguyên có cụ thể đo được không: số giờ/tuần, skill rõ ràng, tool đã tồn tại).

## Flow

### Phase 0: Detect mode

| State                                                         | Mode                                                        |
| ------------------------------------------------------------- | ----------------------------------------------------------- |
| `.okr/` chưa có HOẶC `objective.md` thiếu                     | `new`                                                       |
| Có objective.md + user nhắc tới objective/KR/KI/period        | `update-objective`                                          |
| Có objective.md + user nhắc tới capacity/skill/tool/ngân sách | `update-resource`                                           |
| User chọn explicit (vd "/okr init update-objective")          | theo lựa chọn                                               |
| Mơ hồ                                                         | hỏi user: "Tạo mới (ghi đè) / Sửa mục tiêu / Sửa resource?" |

**Cảnh báo ghi đè**: Nếu mode `new` nhưng `objective.md` đã tồn tại:
1. Hiển thị: "Objective đã tồn tại: [tên]. Ghi đè sẽ mất KR/KI hiện tại + plan liên kết có thể bất khớp."
2. Hỏi: "(ghi đè / chuyển sang update-objective / huỷ)"
3. User chọn ghi đè → Phase 1 bình thường. Chuyển → đổi mode.


---

## Mode NEW: tạo `.okr/` từ đầu

### Phase 0a: Đọc inbox làm context (nếu có)

Trước khi hỏi loại mục tiêu, kiểm tra `.okr/inbox/*.md`:

- Nếu thư mục `.okr/inbox/` chưa có hoặc rỗng → skip Phase 0a, sang Phase 1.
- Nếu có items → đọc tất cả file (frontmatter + body), nhóm theo `type`:
  - `action` items: gợi ý cho user đây có thể là việc cần làm cho objective sắp tạo.
  - `resource` items: tool/tài liệu sẵn có, dùng làm input cho Phase 5 Resource.
  - `blocker` items: rủi ro/thiếu hụt, dùng làm input cho Phase 5 mục Rủi ro.
  - `thought` items: ý tưởng nền, có thể chuyển thành KR hoặc actions.

Hiển thị block context:

```
Inbox sẵn có (5 items, captured trước khi tạo objective)
- 2 action: "Viết blog post về X", "Setup analytics tracking"
- 1 resource: "Library Y hỗ trợ chart"
- 1 blocker: "Server staging không stable"
- 1 thought: "Có thể test pricing model 2 tier?"

Mình sẽ dùng các items này làm context khi đề xuất KR (Phase 3),
actions (qua /okr plan sau), và resources (Phase 5). Sau khi
objective tạo xong, mình sẽ hỏi map từng item vào KR phù hợp.
Tiếp tục Phase 1? (y/sửa context/skip context)
```

User trả lời:

- `y` → đi tiếp Phase 1, agent giữ items làm context nội bộ.
- `sửa context` → user bổ sung/loại trừ items nào.
- `skip context` → đi tiếp Phase 1 nhưng không dùng items (vẫn giữ inbox cho Phase 8).

### Phase 1: Loại mục tiêu

Hỏi: **Project** (có deadline, đạt target rồi kết thúc) hay **Ongoing** (duy trì liên tục, không có điểm kết thúc, giống lĩnh vực cần chăm sóc).

Ví dụ giúp user phân biệt:

- Project: "Ra mắt MVP trước 30/7", "Viết xong sách trước Q4"
- Ongoing: "Duy trì sức khoẻ thể chất", "Chất lượng code", "Tài chính cá nhân"

### Phase 2: Thu thập Objective (hỏi từng câu + đào sâu)

Hỏi từng câu. Sau mỗi câu trả lời, chạy Quality Gate. Nếu fail, dùng kỹ thuật đào sâu tương ứng.

| Câu hỏi                                             | Tiêu chí "đạt"                                                                                       | Kỹ thuật đào sâu khi chưa đạt                                                                                                                   |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **WHY**: Tại sao mục tiêu này quan trọng?           | Chạm được động lực gốc (không còn hỏi "tại sao?" tiếp được)                                          | Dùng "5 Whys": hỏi "tại sao?" lặp lại cho đến khi chạm lý do thật. Vd: "Tăng doanh thu" → "Tại sao?" → "Để có lãi" → "Đang lỗ à? Lỗ bao nhiêu?" |
| **WHAT**: Kết quả cụ thể mong đợi?                  | User mô tả được "done trông thế nào" (Project) hoặc "khoẻ trông thế nào" (Ongoing) bằng 1 câu cụ thể | Hỏi: "Khi xong, chuyện gì khác đi so với bây giờ?" (Project) hoặc "Lĩnh vực này đang khoẻ khi nào? Tiêu chí nào cho biết?" (Ongoing)            |
| **HOW**: Cách tiếp cận tổng quan?                   | User chọn được hướng đi, không nói chung chung                                                       | Đưa 2-3 hướng kèm tradeoff. Vd: "Có 3 cách: A (nhanh, rủi ro cao), B (chắc, tốn resource), C (thử nghiệm nhỏ trước). Nghiêng hướng nào?"        |
| **Khung thời gian** (Project): start_date, end_date | Có mốc cụ thể, không "càng sớm càng tốt"                                                             | Hỏi: "Có event nào buộc phải xong trước không?" (deadline cứng) hoặc "Nếu không có deadline, bao lâu là hợp lý?"                                |
| **Chu kỳ review** (Ongoing): review_cycle           | User chọn weekly/biweekly/monthly                                                                    | Hỏi: "Bạn muốn review lĩnh vực này bao lâu 1 lần? Tuần / 2 tuần / tháng?"                                                                       |


### Phase 3: Đề xuất Key Results (Project) hoặc Key Indicators (Ongoing)

Đọc `references/okr-guide.md` để check tiêu chí.

**Với Project (Key Results)**:

- Đo được (số liệu, không mơ hồ)
- Có baseline + target
- Khả thi nhưng thách thức

Đề xuất 2-4 KR, hỏi feedback từng cái.

**Với Ongoing (Key Indicators)**:

- Đo được (số hoặc tần suất)
- Có ngưỡng tối thiểu rõ ràng
- Phản ánh trực tiếp sức khoẻ lĩnh vực

Đề xuất 2-4 KI, hỏi feedback từng cái.

**Challenge KR/KI (bắt buộc với mỗi cái):**

Sau khi user đồng ý, agent phải challenge:

Với KR (Project):

1. **Đo bằng gì?** Data source ở đâu? Ai đo? Bao lâu đo 1 lần?
2. **Kiểm soát được không?** KR phụ thuộc hoàn toàn vào team hay cần bên ngoài? Nếu phụ thuộc ngoài → cảnh báo rủi ro + hỏi có backup plan.
3. **Baseline chính xác chưa?** Số hiện tại là bao nhiêu? Lấy từ đâu? Đã verify chưa?
4. **Target có stretch đủ?** So sánh với tốc độ tăng trưởng hiện tại. Vd: "Hiện 1k DAU, target 5k trong 3 tháng = tăng 5x. Growth rate hiện tại bao nhiêu?"

Với KI (Ongoing):

1. **Đo bằng gì?** Data thu thập thế nào? Tự ghi hay tự động?
2. **Ngưỡng có thực tế?** So với thực tế hiện tại. Vd: "Hiện tập 1 lần/tuần, đặt ngưỡng 5 lần/tuần có khả thi không?"
3. **Warning/Critical phân biệt rõ?** Khi nào chỉ cần lưu ý, khi nào cần hành động gấp?

Không cần hỏi tất cả nếu đã rõ (Quality Gate pass). Chỉ hỏi câu nào agent chưa tự trả lời được.

### Phase 4: CONFIRM Objective (BẮT BUỘC, kèm đánh giá)

Bảng confirm PHẢI kèm phần "Đánh giá nhanh" do agent tự phân tích. Không chỉ echo data.

**Với Project:**

```
Tóm tắt Objective
| Field        | Value                                |
|--------------|--------------------------------------|
| Type         | project                              |
| Objective    | Tăng doanh thu sản phẩm A 30% Q4-2026|
| Period       | 2026-10-01 > 2026-12-31              |
| WHY          | [tóm tắt 1 câu]                      |
| KR1          | DAU: 1k > 5k (target)                |
| KR2          | MRR: 100M > 200M VND                 |

Đánh giá nhanh
  Điểm mạnh:
  - [vd: KR1 đo được rõ, data source có sẵn (GA4)]
  - [vd: Timeline 3 tháng khớp với chu kỳ kinh doanh]
  Cần lưu ý:
  - [vd: KR2 phụ thuộc đội sales, ngoài kiểm soát trực tiếp]
  - [vd: ⚠️ WHY chưa rõ động lực gốc (đánh dấu TBD)]

Xác nhận? (y / sửa <field>: <giá trị mới> / huỷ)
```

**Với Ongoing:**

```
Tóm tắt Objective
| Field         | Value                                |
|---------------|--------------------------------------|
| Type          | ongoing                              |
| Objective     | Duy trì sức khoẻ thể chất            |
| Review cycle  | weekly                               |
| WHY           | [tóm tắt 1 câu]                      |
| KI1           | Tập thể dục ≥3 lần/tuần (current: 1) |
| KI2           | Ngủ ≥7 giờ/đêm (current: 5.5)        |

Đánh giá nhanh
  Điểm mạnh:
  - [vd: KI đo được rõ, dễ tự track hàng ngày]
  Cần lưu ý:
  - [vd: KI1 ngưỡng 3 nhưng current chỉ 1, gap lớn → nên bắt đầu từ 2?]
  - [vd: KI2 phụ thuộc nhiều yếu tố ngoài kiểm soát (công việc, con nhỏ)]

Xác nhận? (y / sửa <field>: <giá trị mới> / huỷ)
```

Quy tắc đánh giá:

- Liệt kê 1-3 điểm mạnh (để user yên tâm phần đã tốt).
- Liệt kê mọi điểm cần lưu ý: field TBD, KI/KR phụ thuộc ngoài, mâu thuẫn tiềm ẩn.
- Nếu có field TBD → liệt kê rõ, hỏi user muốn bổ sung ngay hay ghi nhận rủi ro.

Lặp đến khi user `y`.

### Phase 5: Thu thập Resource (hỏi tuần tự + cross-check)

Skill phục vụ persona **solo only** (1 user, 1 objective). KHÔNG còn nhánh team. Hỏi tuần tự:

1. **Solo Profile**:
  - **Capacity**: Bạn dành bao nhiêu giờ/tuần cho mục tiêu này? (vd: 10 giờ/tuần, mỗi tối 1 tiếng)
  - **Skills liên quan**: Bạn đã có sẵn kỹ năng nào phục vụ mục tiêu này? (vd: Python, viết content, design Figma). Mục đích: agent biết tự tin đề xuất action loại nào, và cảnh báo khi action cần skill chưa có.
2. **Công cụ**: Danh sách công cụ (6 cột: Tên, Mục đích, Khi nào dùng, Cách dùng, Resource, Ghi chú). Hỏi thêm: "Cách dùng" (có skill/MCP integration? hay quy trình thủ công?), "Ghi chú" (license, giới hạn, lưu ý). Xem schema `references/data-format.md` section "Schema 6 cột thống nhất".
3. **Tài liệu / Knowledge Base**: Tài liệu và KB (6 cột: Tên, Mục đích, Khi nào dùng, Cách dùng, Resource, Ghi chú). Status cũ gộp vào Ghi chú. Hỏi thêm: "Khi nào dùng" (trigger cụ thể), "Cách dùng" (mở link, dùng skill, search). Xem schema `references/data-format.md` section "Schema 6 cột thống nhất".
4. **Ngân sách** (nếu Project hoặc cần đầu tư): Có ngân sách không? Bao nhiêu?
5. **Thiếu hụt**: Có rủi ro/thiếu hụt nào nhận biết được không? (vd: skill còn thiếu, tool chưa mua, deadline ngoài tầm kiểm soát)

User skip được (`không có` / `để sau`), nhưng field skip đánh dấu `⚠️ TBD`.

**Cross-check capacity vs. scope (bắt buộc sau khi thu thập xong):**

Agent tự tính toán sơ bộ trước khi sang Phase 6:

- Tổng available capacity = `capacity h/tuần × số tuần đến end_date` (Project) hoặc `capacity h/tuần × 4` (Ongoing, dùng 1 tháng làm horizon đánh giá)
- Ước tính scope từ KR/KI đã define (Phase 3): mỗi KR cần khoảng bao nhiêu giờ?
- So sánh: capacity có đủ cho scope không?

Nếu lệch rõ rệt → cảnh báo user ngay, hỏi:

- "Scope cần khoảng X giờ, capacity hiện có Y giờ. Cần thu hẹp scope, extend deadline, hay tăng capacity?"

Không cần chính xác tuyệt đối. Mục tiêu là phát hiện bất hợp lý lớn (vd: 10 giờ/tuần làm việc của 40 giờ/tuần).

### Phase 6: CONFIRM Resource (BẮT BUỘC, kèm đánh giá)

```
Tóm tắt Resource
| Mục            | Giá trị                                  |
|----------------|------------------------------------------|
| Solo Profile   | Tuấn, 10h/tuần, skills: Python, viết     |
| Công cụ        | Notion (Task), GitHub, Figma             |
| Tài liệu/KB    | brief.pdf, thư mục Drive                 |
| Ngân sách      | 5M VND                                   |
| Rủi ro         | Skill design Figma còn yếu               |

Đánh giá nhanh
  Capacity: 10h/tuần × 12 tuần = 120 giờ
  Scope ước tính: [dựa trên KR/KI] ≈ 150 giờ
  Fit: ⚠️ hơi thiếu, cần buffer hoặc thu hẹp scope
  Rủi ro chính:
  - Skill Figma còn yếu, cân nhắc dùng template/outsource phần design
  - ⚠️ Ngân sách chưa rõ (TBD)

Xác nhận? (y / sửa / huỷ)
```

### Phase 7: Ghi file

1. Tạo `.okr/`.
2. Ghi `.okr/objective.md` theo schema.
3. Ghi `.okr/resources.md` theo schema (giữ section header dù rỗng).
4. Hiển thị: "Đã tạo objective + resources. Tiếp tục Phase 8 nếu có inbox sẵn, hoặc chạy `/okr` để lập plan."

### Phase 8: Post-init — gợi ý map inbox vào KR (chỉ chạy nếu Phase 0a đã đọc inbox)

Skip nếu Phase 0 trả về rỗng. Nếu có items:

Với mỗi inbox item có `related_kr: null`, agent đề xuất KR phù hợp dựa trên KR vừa tạo + nội dung item:

```
Map inbox items vào KR (5 items pending)
| # | Type     | Title                          | Đề xuất related_kr | Lý do                          |
|---|----------|--------------------------------|--------------------|--------------------------------|
| 1 | action   | Viết blog post về X            | KR1                | KR1 về content marketing       |
| 2 | action   | Setup analytics tracking       | KR2                | KR2 cần đo conversion          |
| 3 | resource | Library Y hỗ trợ chart         | (không cần map)    | Resource, không link KR        |
| 4 | blocker  | Server staging không stable    | KR2                | Blocker A007 thuộc KR2         |
| 5 | thought  | Có thể test pricing 2 tier?    | KR2                | Liên quan revenue              |

Apply gợi ý? (vd: "1,2,4,5 apply / 3 skip" / all / sửa N: KR<X> / huỷ)
```

User trả lời:

- `<N> apply`: ghi `related_kr: KR<X>` vào frontmatter inbox item.
- `<N> skip`: giữ `related_kr: null`.
- `all`: apply hết.
- `sửa N: KR<X>`: override gợi ý.
- `huỷ`: bỏ hết, không apply.

Sau khi apply: hiển thị "Đã map N items. Chạy `/okr` để lập plan và xử lý inbox khi track."

---

## Mode UPDATE-OBJECTIVE: sửa objective/KR/KI

Chi tiết flow (7 phases: hiển thị state → hỏi thay đổi → re-validate SMART → Impact Check → CONFIRM diff → ghi file): xem [flow-update-objective.md](references/flow-update-objective.md). Đọc khi orchestrator kích hoạt mode `update-objective`.

---

## Mode UPDATE-RESOURCE: sửa resource

Chi tiết flow (5 phases: hiển thị state → hỏi update → thu thập → CONFIRM diff → áp dụng + cảnh báo cross-check): xem [flow-update-resource.md](references/flow-update-resource.md). Đọc khi orchestrator kích hoạt mode `update-resource`.

---

## Schema

Đọc `references/data-format.md` cho schema `objective.md` + `resources.md` + rule phát hiện xung đột.
Đọc `references/okr-guide.md` cho check SMART KR và KI guidelines.

## Quy tắc chung

- Hỏi 1 câu/lần.
- KHÔNG ghi file trước phase confirm.
- Mode `new`: ghi cả 2 file (objective + resources). Resource trống vẫn ghi `resources.md` rỗng có header.
- Mode `update-*`: ghi đè SOT. `pic` mặc định `self`, có thể gán tên người khác khi delegate.
- KR không SMART → chỉ rõ thiếu tiêu chí nào + gợi ý sửa.
- KI không đo được hoặc thiếu ngưỡng → chỉ rõ + gợi ý sửa.
- Không tạo `plan.md` hay action files. Plan thuộc `okr-plan`.
- Không sửa action status. Đó là việc của `okr-track`.
