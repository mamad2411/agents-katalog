---
name: okr-capture
description: "Dùng khi `/okr` cần ghi nhanh ý tưởng, ghi chú, action, blocker, resource, meeting note, inbox/capture trước khi xử lý sau. Gọi trực tiếp chỉ khi người dùng gõ `/okr-capture`."
---

# okr-capture: Thu thập nhanh → Inbox

Skill giúp user ghi lại bất kỳ nội dung gì nhanh nhất có thể, không cần biết nó thuộc skill nào hay mode nào. Agent phân tích, tinh chỉnh, phân loại, rồi lưu vào inbox. Việc xử lý inbox (chuyển thành action, update resource, ghi log...) là trách nhiệm của `okr-track`.

> **Tiên quyết**: Skill `okr` (orchestrator) PHẢI load trước khi skill này chạy. Context từ orchestrator đã có sẵn (SOT ownership, shared schemas), KHÔNG đọc lại.

## Tại sao cần skill này?

Giữa lúc làm việc, user thường nảy ra ý tưởng hoặc phát hiện vấn đề. Nếu phải vào đúng mode (`okr-plan update`, `okr-init update-resource`) mới thêm được, ma sát quá lớn → user bỏ qua → mất thông tin. Capture giải quyết vấn đề này: ghi trước, xử lý sau.

## Nguyên tắc

- Nhanh: tối thiểu bước xác nhận. Mục tiêu là ghi xong trong 1-2 turn.
- Không sửa SOT: chỉ tạo file trong `inbox/`. Mọi thay đổi SOT do skill khác xử lý khi inbox được process.
- Giữ nguyên văn gốc: dù agent tinh chỉnh title/description, phần context gốc (nguyên văn user nhập) luôn được giữ lại.
- **Không validate `related_kr`/`related_action` ID (M5a):** capture chỉ **gợi ý** best-effort dựa trên context user nhập + đọc nhanh `.okr/objective.md`/`actions/`. Nếu gợi ý sai (ID không tồn tại, KR đã missed, action đã archive), không phải lỗi capture. Track Phase 5 Bước 3 sẽ validate lại từng ID lúc xử lý inbox + đề xuất sửa hoặc set `null`.
- Cho phép capture khi chưa có `.okr/objective.md`: tạo `.okr/inbox/` ngay, cảnh báo user nên chạy `/okr init` khi sẵn sàng.

## Flow

### Phase 1: Nhận input

User cung cấp input bằng 1 trong các cách:
- Câu nói ngắn: "thêm nhanh: viết unit test cho API auth"
- Đoạn text dài (paste từ meeting notes, chat, doc)
- Nhiều ý cùng lúc cách bởi bullet hoặc xuống dòng

### Phase 2: Phân tích + phân loại

Agent phân tích input và phân loại mỗi ý thành 1 item với type:

| Type | Khi nào | Ví dụ |
|------|---------|-------|
| `action` | Việc cần làm cụ thể, có output rõ | "Viết unit test cho API auth" |
| `blocker` | Vấn đề đang chặn tiến độ | "Server staging bị down, không deploy được" |
| `resource` | Tài nguyên mới phát hiện (tool, doc) | "Tìm được thư viện Y hỗ trợ chart, miễn phí" |
| `thought` | Ý tưởng, ghi chú, context bổ sung (chưa thành action rõ) | "Có thể dùng framework X cho frontend?", "Khách hàng muốn demo trước 15/6" |

> **Lưu ý dữ liệu cũ**: Schema trước đây có 5 type với `idea` + `note` riêng biệt. Đã gộp thành `thought` để giảm friction phân loại. Nếu gặp inbox file cũ với `type: idea` hoặc `type: note`, coi như `type: thought` khi xử lý.

**Tinh chỉnh cho mỗi item:**
- Title: viết lại ngắn gọn, rõ ràng (≤15 từ)
- Description: 1-2 câu mô tả (agent viết dựa trên context)
- Related KR/KI: gợi ý KR/KI liên quan (nếu `.okr/objective.md` tồn tại)
- Related action: gợi ý action liên quan (nếu `.okr/actions/` tồn tại)

Nếu không chắc chắn type → hỏi user. Nếu không map được KR/action → để `null`.

### Phase 3: Confirm (nhanh)

**Single item skip confirm**: Khi input chỉ 1 item đơn giản + type rõ ràng (action hoặc blocker), skip Phase 3 confirm. Ghi luôn + thông báo:

```
✓ Đã lưu "Viết unit test API auth" vào inbox (type: action, gợi ý KR2).
```

Giữ confirm cho:
- Batch (≥2 items)
- Type mơ hồ (không chắc action hay thought)
- User muốn review (nói "xem lại trước khi lưu")

**Single item (cần confirm):**

```
Inbox item
| Field    | Value                                     |
|----------|-------------------------------------------|
| Type     | action                                    |
| Title    | Viết unit test cho API auth               |
| Related  | KR2 (code coverage), A005 (implement API) |

Lưu vào inbox? (y / sửa / huỷ)
```

**Batch (nhiều items):**

```
Inbox: 3 items từ input của bạn
| # | Type     | Title                         | Related |
|---|----------|-------------------------------|---------|
| 1 | action   | Viết unit test cho API auth   | KR2     |
| 2 | blocker  | Server staging down           | A007    |
| 3 | thought  | Thử framework X cho frontend  | -       |

Lưu tất cả? (y / sửa N / bỏ N / huỷ)
```

### Phase 4: Ghi file + nhắc xử lý

1. Tạo `.okr/inbox/` nếu chưa có.
2. Ghi mỗi item thành 1 file: `YYYY-MM-DD-HHmm-slug.md`
3. Hiển thị: "Đã lưu N items vào inbox. Chạy `/okr track` để xử lý inbox."
4. **Reminder (nếu áp dụng):** đếm tổng items pending trong `.okr/inbox/` (kể cả vừa thêm). Nếu ≥5 → in thêm 1 dòng: `⚠️ Inbox có N items pending. Xử lý sớm bằng /okr track để tránh tích luỹ.`

## Schema

Đọc `references/data-format.md` cho schema inbox item.

## Quy tắc

- KHÔNG sửa SOT (objective.md, plan.md, resources.md, actions/).
- KHÔNG tự phân loại nếu mơ hồ. Hỏi user.
- KHÔNG validate `related_kr`/`related_action` ID. Gợi ý best-effort là đủ. Track xử lý inbox sẽ validate.
- Giữ nguyên văn gốc trong body (section "## Context gốc").
- Batch: tách rõ từng item, confirm tất cả 1 lần.
- File name: `YYYY-MM-DD-HHmm-slug.md`. Slug dùng tiếng Việt không dấu hoặc tiếng Anh, dấu gạch ngang.
- Nếu `.okr/` chưa có → vẫn tạo `.okr/inbox/` + cảnh báo chạy init.
- KHÔNG ghi `staleness_days` vào frontmatter. Capture chỉ lưu `captured_at`. Staleness được compute on-the-fly bởi `okr-track` Phase 5 (xem `references/data-format.md` section "Inbox Aging").
