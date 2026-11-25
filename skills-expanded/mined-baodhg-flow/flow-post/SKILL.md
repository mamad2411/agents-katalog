---
name: flow-post
description: Dùng khi vừa thay đổi mã trong repo có `.flow/` và sắp tuyên bố hoàn thành, sắp mở PR, hoặc vừa hết danh sách task, kể cả với sửa nhỏ một dòng. Người dùng hay nói "xong chưa", "chốt lại", "đóng việc", "mở PR đi", "kiểm lại trước khi giao", "post".
---

# flow-post — đóng việc

Đi đủ các bước theo thứ tự. Việc cần người dùng cho phép thì hỏi trên chat. `flow plan status <slug> VERIFYING` ở đầu nếu có plan.

## 1. Verify

`flow verify --full`. Bước bị bỏ qua không phải là xanh; ghi rõ bước nào và vì sao. Đỏ thì phân biệt đỏ sẵn so với mốc và đỏ do mình.

## 2. Vệ sinh

`flow check --base <nhánh gốc>` gồm bí mật, chú thích, lộ harness, tên, DRY. Sửa mã cho qua, không nới công cụ.

## 3. Nghiệm thu thật

Lấy danh sách: `flow gates --changed --print post`.

| Loại thay đổi | Cách nghiệm thu |
|---|---|
| UI | Tự nhìn kết quả thật và viết runbook nghiệm thu; cần trình duyệt trên môi trường thật thì xin phép |
| Bất đồng bộ | Đo ở đầu nhận, không coi gửi thành công là xong |
| Dữ liệu, hạ tầng, phát hành | Runbook, dùng skill `flow-runbook` |
| Logic thuần | Test ở bước 1 là đủ, ghi rõ test nào |

## 4. Review cả nhánh

Dùng skill `flow-review` trên toàn bộ diff so với nhánh gốc, vì lỗi hay nằm ở chỗ các task ghép với nhau.

## 5. Cập nhật ngữ cảnh

- `CONTEXT.md` của module đã chạm: sửa phần lệch, sinh nếu thiếu (`flow context missing --changed`), xem skill `flow-context`
- `.flow/coverage.md`: `flow context coverage`
- `.flow/contracts.md` khi hợp đồng đổi
- Luật và memory qua skill `flow-learn`

## 6. Xử lý ma sát

Đọc ledger, mục `friction`. Mỗi mục chọn một:

- Vá ở dạng rẻ nhất có tác dụng: sửa `CONTEXT.md`, thêm luật, thêm memory, thêm test.
- Thứ thuộc về bộ skill: đề xuất cho người dùng trên chat, theo mục ranh giới ở skill `flow-learn`. Không tự sửa bộ skill.
- Không đáng làm: ghi một dòng vì sao.

## 7. Sức khoẻ

`flow doctor`.

## 8. Giao theo `autonomy.level`

- `local`: để commit trên nhánh, báo tên nhánh.
- `pr`: `flow prmsg <tệp mô tả>` rồi push và mở PR.
- `merge`: như `pr`, merge khi cổng xanh, trừ phần thuộc `branches.ownerOnly`.

Viết mô tả từ `<gói>/templates/pr-description.md` hoặc template của repo. Không nhắc harness.

## 9. Đóng plan

`flow plan status <slug> DONE`. Còn nợ thì `PARKED`, ghi vào mục 8 của plan.

## Báo cáo

Giữ đúng khuôn, ô nào không làm thì ghi lý do, không xoá dòng.

```
Verify:      <lệnh> — <xanh hay đỏ>, <đỏ sẵn nào>
Test:        <thêm ca nào, đã thấy đỏ trước chưa>
Vệ sinh:     <kết quả check --base>
Nghiệm thu:  <đã đo gì, ở đâu, thấy gì>
Review:      <đúng plan? chất lượng? số mục chặn đã xử lý>
Ngữ cảnh:    <tệp đã cập nhật>
Ma sát:      <đã vá gì, đề xuất gì>
Giao:        <nhánh hoặc PR>
Đã bỏ qua:   <việc gì, vì sao, ai cần làm>
```
