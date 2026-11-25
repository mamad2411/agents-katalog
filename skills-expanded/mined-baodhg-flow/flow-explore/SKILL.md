---
name: flow-explore
description: Dùng khi việc sắp làm có thể lan qua nhiều module hoặc nhiều repo, hoặc đụng tiền, xác thực, schema, sự kiện, luật critical, và cần biết phạm vi trước khi viết plan hay sửa mã. Người dùng hay nói "tìm hiểu trước", "xem ảnh hưởng tới đâu", "đọc xem luồng này chạy sao", "có sẵn chưa", "explore".
---

# flow-explore — điều tra

Không sửa mã trong bước này. Kết quả là một khối thông tin đủ để viết plan.

## Các bước

1. Nạp ngữ cảnh theo thứ tự ở skill `flow`. Luật và gate: `flow rules find --path <tệp>`, `flow gates --path <tệp> --print explore`.
2. Truy vết ba hướng: upstream (ai gọi vào, dữ liệu từ đâu), luồng chính, downstream (ai nhận kết quả, ai đọc bảng).
3. Grep có mục tiêu, ghi mọi phát hiện dạng `tệp:dòng`. Không đọc tràn cả thư mục.
4. Trả lời "đã có sẵn chưa".
5. Điền khối output.

## Đã có sẵn chưa

Bước bắt buộc, vì viết lại thứ đã có tạo ra hai bản sẽ lệch nhau.

1. `flow dup find "<ý đồ>"` — tìm theo ý đồ, ví dụ `dup find "định dạng ngày hẹn trả"`, không chỉ theo tên.
2. Grep API cốt lõi mà việc đó phải gọi. Ví dụ: hàm định dạng ngày gần như chắc chắn gọi thư viện ngày của dự án.
3. Grep kiểu vào và kiểu ra. Ví dụ: hàm nhận `Loan` và trả chuỗi có thể chính là `formatDueDate`.

Ghi cả khi không thấy, kèm lệnh đã chạy, để người sau không phải tìm lại và biết phạm vi đã tìm.

## Impact score

```
score = số thành phần chịu ảnh hưởng × mức rủi ro
```

Mức rủi ro: thấp 1, vừa 2, cao 3, critical 4. Nhân đôi nếu chạm hợp đồng có bên tiêu thụ khác repo, vì bên đó không chạy chung test với bạn.

## Khối output

```
Repo & module:   <…>
Luật khớp:       <id, mức, một dòng mỗi luật>
Hợp đồng:        <API, sự kiện, schema dùng chung, bên tiêu thụ>
Schema:          <bảng, additive hay phá vỡ>
Vùng rủi ro:     <tệp:dòng — hậu quả nếu hỏng>
Gate khớp:       <tên>
Tái dùng:        <tệp:dòng, hoặc "không thấy" kèm lệnh đã chạy>
Quy ước:         <theo profile và theo mã xung quanh>
Nơi kiến thức sẽ ở: <CONTEXT.md nào, luật nào, tên test nào>
Impact score:    <số thành phần> × <mức> [× 2] = <điểm>
Cỡ task:         S | M | L
```

## Sau khi có output

- Điều cần người dùng quyết: hỏi ngay trên chat theo mục "Hỏi người dùng" ở skill `flow`.
- Điểm vượt `impact.humanReviewAt` hoặc rủi ro cao: plan cần người dùng duyệt.
- Cỡ S: sửa rồi sang skill `flow-post`. Cỡ M, L: sang skill `flow-plan`.
- Ngữ cảnh sai so với mã: sửa ngay, không đợi tới post.
