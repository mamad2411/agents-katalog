---
name: flow-plan
description: Dùng khi việc cần chia thành nhiều bước, chạm nhiều tệp hay nhiều repo, hoặc cần được duyệt trước khi động tay, thường là sau khi đã điều tra xong. Người dùng hay nói "lên kế hoạch", "chia việc", "viết plan", "tách task", "cho tôi xem hướng làm trước".
---

# flow-plan — kế hoạch

## Tạo

```
flow plan new <slug> --title "…" --branch <nhánh> --repos a,b
```

Tệp nằm ở `.flow/plans/active/`, dựa trên `<gói>/templates/plan.md`. Tài liệu khác của việc này để trong `.flow/handoff/`.

## Các mục

| Mục | Viết gì |
|---|---|
| 0. Quyết định | Biên bản câu hỏi đã hỏi trên chat, dòng `- [ ] **D1** …` |
| 1. Pre-flight | Điều kế hoạch giả định đúng, kèm lệnh đo và kết quả thật |
| 2. Tasks | Danh sách việc, xem dưới |
| 3. Schema | Mặc định additive. Thay đổi phá vỡ dùng expand-contract: thêm mới, ghi cả hai, chuyển bên đọc, gỡ cũ |
| 4. Hợp đồng và ngữ cảnh | Hợp đồng đổi, bên tiêu thụ, `CONTEXT.md` và luật cần sửa |
| 5. Thứ tự triển khai | Thứ tự kèm lý do, ví dụ consumer trước producer |
| 6. Kiểm chứng | Lệnh verify, gate khớp, cách nghiệm thu thật |
| 7. Rollback | Cách lùi từng bước, điểm không lùi được |
| 8. Nhánh và việc còn lại | Tên nhánh, phần để sau, nợ khi `PARKED` |
| 9. Ledger | `flow task note` tự ghi vào đây |

## Task

```
- [ ] **T1** Cho phép gia hạn `Loan` một lần — tệp: `loan/renew.ts` — test đỏ trước: gia hạn lần hai bị từ chối — tái dùng: `formatDueDate`
```

- Một task một kết quả kiểm được và một commit.
- Test đỏ phải nói được hành vi nào, không phải "viết test".
- Tái dùng ghi đúng thứ tìm thấy ở explore. Không có thì ghi `không`.
- Thêm task sau này: `flow task add <slug> "…"`.

## Quyết định

Không để câu hỏi nằm im trong tệp. Hỏi trên chat theo mục "Hỏi người dùng" ở skill `flow`, rồi ghi:

```
flow plan decisions <slug>
flow plan decide <slug> D1 "<lựa chọn>"
```

Không có gì để hỏi thì xoá dòng mẫu D1.

## Vòng đời

```
DRAFT → APPROVED → EXECUTING → VERIFYING → DONE
Rẽ nhánh: PARKED (tạm dừng, còn nợ) · ABANDONED (bỏ)
```

Đổi bằng `flow plan status <slug> <STATUS>`.

- `APPROVED` bị từ chối khi còn quyết định mở, vì thi hành trên điều chưa chốt là làm lại.
- `DONE` bị từ chối khi còn task mở. Còn nợ thì dùng `PARKED` và ghi vào mục 8.

## Duyệt

Xin duyệt trên chat, tóm tắt tối đa 10 dòng: mục tiêu, các task, rủi ro, thứ tự, điều đã tự quyết. Plan vượt `impact.humanReviewAt` hoặc chạm vùng rủi ro cao phải có người dùng duyệt. Plan còn lại tự chuyển `APPROVED` khi pre-flight đã có bằng chứng.

Duyệt xong sang skill `flow-execute`.
