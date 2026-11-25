---
name: okr-plan
description: "Dùng khi `/okr` cần tạo hoặc sửa plan, milestones, actions, dependencies, deadline, PIC, external_ids, hoặc plan lệch objective/resources. Gọi trực tiếp chỉ khi người dùng gõ `/okr-plan`."
---

# okr-plan: Tạo + cập nhật plan & actions

Skill quản lý 2 SOT: `plan.md` và `actions/`. Hỗ trợ tạo mới và điều chỉnh sau (khi `okr-track` deep phát hiện cần thay đổi cấu trúc).

> **Tiên quyết**: Skill `okr` (orchestrator) PHẢI load trước khi skill này chạy. Context từ orchestrator đã có sẵn (SOT ownership, shared schemas, quality gate), KHÔNG đọc lại.

## Điều kiện tiên quyết

- `.okr/objective.md` tồn tại. Thiếu → quay lại `/okr` để init.
- `.okr/resources.md` tồn tại. Thiếu → hỏi user có bổ sung trước (`/okr` → `okr-init` mode `update-resource`) hay tiếp tục với Solo Profile mặc định (capacity 0h/tuần, skills rỗng — sẽ cảnh báo cross-check fit ở Phase 3 confirm).

## Quality Gate

Áp dụng Quality Gate (đã có trong context từ orchestrator). Áp dụng trước khi tiến hành các phase hỏi user.

Ví dụ áp dụng cho mode `new` / `update`:

- "Đủ cụ thể?" → action "Nghiên cứu thêm" FAIL (output là gì? đo bằng gì?).
- "Giả định ẩn?" → thêm 5 actions mới nhưng không nói effort tổng bao nhiêu giờ.
- "Mâu thuẫn?" → capacity 10h/tuần nhưng gán 6 actions effort `m` (1-2 ngày mỗi cái) cùng deadline tuần sau.

## Phase 0: Detect mode

| State                                            | Mode          |
| ------------------------------------------------ | ------------- |
| `plan.md` chưa có                                | `new`         |
| Có `plan.md` + user/track nhắc thay đổi cấu trúc | `update`      |
| User chọn explicit (vd `/okr plan update`)       | theo lựa chọn |

**Cảnh báo ghi đè**: Nếu mode `new` nhưng `plan.md` đã tồn tại:
1. Hiển thị: "Plan đã tồn tại (X milestones, Y actions active, Z done/archive). Mode `new` sẽ ghi đè plan + xoá action files active. Actions archived không bị ảnh hưởng."
2. Hỏi: "(ghi đè / chuyển sang update / huỷ)"
3. User chọn ghi đè → Phase 1 bình thường. Chuyển update → đổi mode.


---

## Mode NEW: tạo plan từ đầu

### Phase 1: Đọc context

- `.okr/objective.md`: Objective + Key Results.
- `.okr/resources.md`: Solo Profile (capacity h/tuần, skills) + công cụ + ngân sách.

### Phase 2: Đề xuất phân rã (KHÔNG ghi file, có đào sâu)

Với mỗi KR:

1. Đề xuất 1-3 **Initiatives** (sáng kiến lớn).
2. Mỗi Initiative → 2-5 **Actions** cụ thể.
3. Nhóm actions thành **Milestones** theo thời gian.
4. Đề xuất dependencies (action B chờ A).
5. Mặc định mỗi action `pic: self`. Có thể gán tên người khác khi delegate việc. Cảnh báo nếu action cần skill chưa có trong Solo Profile (đề xuất thêm action học/outsource trước).
6. Nếu action có ghi chú ngắn (dependency, blocker, context quan trọng), ghi vào field `notes` (≤50 ký tự). Không có thì để trống.
7. Nếu action liên kết tool trong resources.md có `Cách dùng` là `skill:` hoặc `mcp:`, hỏi user có external ID để sync không. Nếu có → ghi `external_ids` frontmatter. Nếu không → bỏ qua.

**Deepening Techniques (agent tự challenge trước khi trình user):**

| Khía cạnh        | Kỹ thuật                                          | Ví dụ                                                                                                       |
| ---------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Initiative**   | Hỏi "nếu chỉ được làm 1, chọn cái nào?"           | Buộc user ưu tiên, tránh plan phình to                                                                      |
| **Action**       | Yêu cầu mô tả output cụ thể (file, event, metric) | "Action 'Nghiên cứu thị trường': output là gì? Report? Slide? Data raw?"                                    |
| **Skill match**  | Challenge action có skill chưa có                 | "Action 'Design Figma' nhưng Solo Profile chưa có skill design. Có học trước, outsource, hay đổi approach?" |
| **Dependencies** | Vẽ critical path, hỏi user confirm                | "A003 chờ A001 + A002. Nếu A002 trễ 1 tuần, plan có chịu được không?"                                       |
| **Timeline**     | So sánh tổng effort vs. capacity                  | "12 actions, 12 tuần, capacity 10h/tuần = 120h. Mỗi action ước 8h = 96h. Buffer 24h. OK?"                   |


Không cần challenge tất cả. Chỉ challenge khía cạnh nào Quality Gate chưa pass.

### Phase 3: CONFIRM Plan (BẮT BUỘC, kèm đánh giá)

Bảng confirm PHẢI kèm phần "Đánh giá nhanh" do agent tự phân tích. Không chỉ echo data.

```
Tóm tắt Plan
| Milestone     | Deadline    | # Actions | KR liên quan |
|---------------|-------------|-----------|--------------|
| M1: Research  | 2026-10-15  | 3         | KR1          |
| M2: Build MVP | 2026-11-15  | 5         | KR1, KR2     |
| M3: Launch    | 2026-12-15  | 4         | KR2, KR3     |

Actions (12 total, pic mặc định self)
| ID    | Title              | Milestone | Effort | Deps      | Output            | Notes         | Ext IDs      |
|-------|--------------------|-----------|--------|-----------|-------------------|---------------|--------------|
| A001  | Khảo sát user      | M1        | m      | -         | survey-report.md  |               |              |
| A002  | Phân tích đối thủ  | M1        | l      | -         | competitor.xlsx   | Cần data từ X | things3: T01 |
| A003  | Spec MVP           | M2        | l      | A001,A002 | spec.md           |               |              |

Đánh giá nhanh
  Capacity fit:
  - Tổng effort ước tính: [X] giờ. Capacity: [10h/tuần × N tuần] = [Y] giờ. Fit: [✅/⚠️]
  - Tuần dồn việc nhất: [tuần W], [N] actions cùng deadline.
  Timeline:
  - Critical path: [A001 → A003 → A007]. Độ dài: [X tuần]. Buffer: [Y tuần]
  Rủi ro:
  - [vd: A005 dependency ngoài (chờ stakeholder), chưa có backup plan]
  - [vd: ⚠️ 2 actions cần skill chưa có trong Solo Profile (Figma, SQL)]

Xác nhận? (y / sửa <ID>: <field>=<value> / xoá <ID> / thêm)
```

Quy tắc đánh giá:

- **Capacity fit**: tính tổng effort ước tính (giờ) vs. capacity còn lại. Tuần nào dồn việc nhất?
- **Timeline**: xác định critical path dài nhất, còn buffer không?
- **Rủi ro**: liệt kê field TBD, dependency ngoài, skill chưa có trong Solo Profile.
- Nếu có rủi ro nghiêm trọng → đề xuất giải pháp cụ thể (cắt scope, dời deadline, học skill trước, outsource).

### Phase 4: Ghi file

1. Tạo `.okr/plan.md`.
2. Tạo thư mục `.okr/actions/`.
3. Ghi mỗi action thành `AXXX-slug.md`. Mặc định `pic: self` (có thể gán tên khác).
4. Cập nhật counters trong `plan.md`.
5. **Render bảng Roadmap** trong `plan.md` body `## Roadmap`: sinh bảng per-milestone từ action files vừa tạo. Format xem `references/data-format.md` section "Roadmap format". Sắp xếp: Priority (critical > high > medium > low), rồi Deadline (sớm trước). Ongoing không có milestone → heading `### Chưa phân milestone`.

### Phase 5: Hậu xử lý

Hiển thị: "Đã tạo plan với X actions. Chạy `/okr` để bắt đầu thực thi."

---

## Mode UPDATE: điều chỉnh plan/actions

Trigger phổ biến: `okr-track` mode `deep` phát hiện KR at-risk hoặc blocker dài → đề xuất điều chỉnh cấu trúc → kích hoạt `okr-plan` mode `update` với context đề xuất.

### Phase 1: Hiển thị state hiện tại

**Bypass detect (M7):** Nếu mode `update` được kích hoạt qua delegate từ `okr-track` Phase 5 (inbox processing) **kèm `context.items[]` đã pre-processed** (mỗi item có `title`, `description`, `related_kr`/`related_action` đã validate, `effort` ước, `milestone` gợi ý), SKIP Phase 1 state display + Phase 2 menu, đi thẳng Phase 3 (gom item thành changes) → Phase 4 confirm với data sẵn. State display chỉ chạy khi user vào trực tiếp `/okr plan update`.

Mode bình thường (state display): đọc `plan.md` + frontmatter `actions/*.md` (**không đệ quy**, bỏ qua `actions/archive/`) + `objective.md` + `resources.md`. Hiển thị:

```
Plan hiện tại
Milestones (3)
| Milestone     | Deadline    | Actions  | Status                |
|---------------|-------------|----------|-----------------------|
| M1: Research  | 2026-10-15  | 3/3      | done                  |
| M2: Build MVP | 2026-11-15  | 2/5      | in-progress, trễ 5 ngày|
| M3: Launch    | 2026-12-15  | 0/4      | pending               |

Cảnh báo
- KR2 at-risk → cần thêm action marketing
- A005 blocked 5 ngày, dependency A002 đã done nhưng quality không đạt
```

### Phase 2: Hỏi user/nhận đề xuất từ track

3 nguồn trigger:

1. **Từ track deep delegate** (`context.changes` + `context.reason` ở payload): hiển thị đề xuất track đã đưa, user chọn áp dụng cái nào (nếu `pre_confirmed: false` hoặc không có), hoặc đi thẳng Phase 4 confirm (nếu `pre_confirmed: true`).
2. **Từ track inbox delegate** (`context.items[]` pre-processed): gom items thành Phase 3 changes, đi thẳng Phase 4 confirm. Mỗi `action` item → 1 "Thêm action mới" với data có sẵn (title, description, related_kr, effort gợi ý, milestone gợi ý). Mỗi `blocker` đụng action → 1 "Sửa action" status=blocked + lý do. Mỗi `resource` → delegate tiếp sang `okr-init update-resource` (không xử lý ở đây).
3. **User vào trực tiếp** (`/okr plan update`): hiển thị menu:
  1. Thêm action mới
  2. Sửa action (title, due_date, status, deps, deliverable, effort, priority)
  3. Xoá action
  4. Dời deadline milestone
  5. Thêm/xoá milestone

### Phase 3: Thu thập thay đổi

Hỏi chi tiết từng cái user chọn.

### Phase 4: CONFIRM diff

Delegate protocol (pre-confirmed flow + reason display): xem skill `okr/references/delegate-protocol.md`.

Luôn hiển thị bảng diff:

```
Thay đổi sắp áp dụng (plan.md + actions/)
| Loại        | Trước              | Sau                       |
|-------------|--------------------|---------------------------|
| Thêm action | -                  | A013 "Marketing campaign" |
| Sửa A005    | due_date 2026-11-10| due_date 2026-11-20       |
| Sửa M2      | deadline 2026-11-15| deadline 2026-11-25       |

Tác động
- A013 mới → 1 action mới gắn KR2
- Dời M2 → 2 actions con tự dời theo? (y/giữ nguyên)

Xác nhận? (y / sửa / huỷ)
```

### Phase 5: Áp dụng

1. Ghi đè `plan.md` (counters, milestones).
2. Ghi/sửa file `actions/AXXX-*.md` tương ứng. **Không** tạo hoặc sửa file trong `actions/archive/`. Action mới mặc định `pic: self` (có thể gán tên khác).
3. **Re-render bảng Roadmap** trong `plan.md` body `## Roadmap`: đọc lại tất cả `actions/*.md` (không archive), sinh lại bảng per-milestone. Format xem `references/data-format.md` section "Roadmap format".
4. Đề xuất chạy `okr-track` mode `light` để confirm state mới.

---

## Schema

- `references/data-format.md`: schema `plan.md` + frontmatter `actions/*.md`.
- `references/task-format.md`: template body action file.
- `references/action-guide.md`: hướng dẫn viết action chất lượng (5 tiêu chí bắt buộc, effort, priority, DoD-based verify, anti-patterns). Đọc trước khi tạo/review actions.

## Quy tắc

- KHÔNG ghi file trước phase confirm.
- Mỗi action BẮT BUỘC có:
  - Definition of Done rõ ràng (mỗi item đo được, user tự check được)
  - Output/Deliverable cụ thể (file, số liệu, sự kiện)
  - `pic`: mặc định `self`, có thể gán tên người khác khi delegate
  - **Tiêu chí chất lượng** (output đạt khi nào? đo bằng gì?)
- Action mơ hồ kiểu "Nghiên cứu thêm" không có output đo được → CẤM. Agent phải follow-up: "Output cụ thể là gì?"
- Nếu user không trả lời được "output đo bằng gì" → action chưa đủ rõ, cần refine trước khi ghi.
- Dependencies hợp lệ: ID tồn tại, không vòng tròn.
- Mode `update` không sửa KR target. Đó là việc của `okr-init` mode `update-objective`.
- Mode `update` không sửa KR.current. Đó là việc của `okr-track` mode `light`. Action.status được phép sửa bởi cả `okr-plan update` lẫn `okr-track` để linh hoạt khi điều chỉnh plan.
- Ongoing type: plan.md body chứa `## Practices` + có thể tạo action files. Chi tiết xem `references/action-guide.md` section "Ongoing type: khi nào tạo action?".
