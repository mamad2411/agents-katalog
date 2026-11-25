---
name: flow-runbook
description: Dùng khi người hoặc agent phải chạy tay một quy trình và đọc được kết quả — nghiệm thu trên môi trường thật, thao tác hạ tầng, chỉnh dữ liệu bằng SQL, đưa bản mới lên, chuyển việc cho người kiểm thử. Người dùng hay nói "viết kịch bản kiểm", "các bước cho QC", "chạy tay", "script sửa dữ liệu", "các bước lên bản", "chuyển cho người khác test".
---

# flow-runbook — quy trình chạy tay

## Lệnh

```
flow runbook new <loại> <slug> --plan <plan>
flow runbook lint <slug>
flow runbook lint <slug> --after
flow runbook list
```

`lint` chạy trước khi thực hiện. `lint --after` chạy sau khi đã điền kết quả. Tệp nằm ở `.flow/handoff/`.

## Luật chung

- Viết bảng diễn giải kết quả trước khi chạy, gồm hàng "không khớp" nghĩa là giả thuyết sai. Viết sau khi thấy kết quả thì sẽ giải thích cho hợp với điều vừa thấy.
- Tiêu chí pass phải đo được: con số, chuỗi, trạng thái đọc lại. Không dùng "hoạt động bình thường".
- Có đối chứng âm, chạy trước. Ca âm không đỏ thì phép đo không phân biệt được gì.
- Một thao tác không đổi trạng thái vẫn có thể báo thành công, nên phải thử cả hai chiều: `Loan` đang mở thì trả được, trả rồi thì lần hai phải khác đi.
- Dữ liệu tiền đề có ký hiệu (`M1`, `B1`), các bước chỉ dùng ký hiệu, để đổi dữ liệu không phải sửa cả tệp.
- Bỏ qua ghi `N/A` kèm lý do, không để ô trống, vì ô trống không nói được là chưa chạy hay quên ghi.
- Đo trên hệ đang chạy. Không đọc lại cấu hình để xác nhận, vì cấu hình nói điều mong muốn chứ không nói điều đang xảy ra.
- Nhìn nội dung phản hồi, không chỉ mã trạng thái, vì `200` vẫn có thể mang thông báo lỗi.
- Ai chạy trên môi trường thật thì hỏi trước trên chat.

## Năm loại

### acceptance

Nghiệm thu một thay đổi hoặc tính năng. Mục 0 phân biệt rõ đã đo, suy ra và chưa làm, để người đọc biết mức tin cậy. Mỗi ca là `#### TC-01 · <tên> [âm]` hoặc `[dương]`, có dòng `**Kỳ vọng:**` và nhánh khi khác kỳ vọng ghi rõ giả thuyết sai. Mục 3 điền kết quả, mục 4 là bảng diễn giải.

### ops

Dựng hoặc vận hành hạ tầng. Mục 0 đo trước khi đụng, lệch thì hành động là `DỪNG`, vì chạy tiếp trên tiền đề sai làm việc khôi phục khó hơn. Mỗi bước có phép đo riêng. Có rollback và nhật ký.

### data-op

Sửa dữ liệu bằng SQL. Script trong transaction, khẳng định trạng thái trước, sao lưu vào bảng `bak_…`, cập nhật, khẳng định trạng thái sau, kết thúc `ROLLBACK`. Chỉ đổi thành `COMMIT` khi đã chạy thử và có người được giao phê duyệt. Có mục đọc lại, đảo ngược và ngoài phạm vi. Không viết chú thích trong khối SQL.

### release

Phát hành một bản. Mục `Cửa một chiều` liệt kê điều không lùi được sau khi đi qua, để người duyệt biết mình quyết gì. Có thay đổi, cổng trước phát hành, thứ tự kèm lý do, nghiệm thu sau, sự cố và ký duyệt.

### handoff

Bàn giao cho QC hoặc người khác. Mục 0 là điều kiện gửi dạng checkbox, gồm bằng chứng bản mới đã lên, vì kiểm trên bản cũ là tốn công hai bên. Có tiêu đề và nội dung văn bản thuần, dán thẳng vào kênh trao đổi được, không nhắc harness.

## Trình tự

1. Tạo runbook, điền mọi chỗ `<…>`.
2. `flow runbook lint <slug>`.
3. Hỏi ai chạy nếu là môi trường thật. Việc chỉ người chạy được thì giao và chờ, không tự đánh dấu.
4. Chạy, điền kết quả đúng như đã thấy.
5. `flow runbook lint <slug> --after`.
6. Đối chiếu bảng diễn giải. Khớp hàng "không khớp" thì dừng và báo, không sửa bảng cho hợp.
