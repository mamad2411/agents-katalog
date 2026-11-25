---
name: flow-context
description: Dùng khi sắp sửa một module mà `flow context missing` báo thiếu tài liệu, khi `.flow/coverage.md` báo nghi cũ, khi tài liệu module nói khác mã, khi cần ghi lại cách repo dùng một dịch vụ ngoài hoặc một chuẩn chung. Người dùng hay nói "viết tài liệu module", "ghi lại cách module này chạy", "cập nhật context", "tóm tắt module cho agent".
---

# flow-context — ngữ cảnh module

## Các ngăn

| Ngăn | Chứa | Không chứa |
|---|---|---|
| `.flow/PROJECT.md` | Toàn cảnh, nhánh, quy ước | Chi tiết module |
| `.flow/services.md` | Bản đồ service | Cách một service chạy bên trong |
| `CONTEXT.md` cạnh mã | Điều riêng của module | Kiến thức xuyên repo |
| `.flow/contracts.md` | API, sự kiện, schema dùng chung | Chi tiết cài đặt |
| `.flow/consumed/` | Cách repo dùng một service ngoài | Tài liệu gốc của họ |
| `.flow/reference/` | Chuẩn dùng chung, bảng tên, sổ phân loại | Dữ liệu thật |
| `.flow/rules/` | Luật có cách kiểm | Ghi chú chung chung |
| `.flow/memory/` | Điều về cách làm việc | Điều về hệ thống |
| `.flow/assets/` | Sơ đồ, ảnh tham khảo | Giá trị bí mật |
| `.flow/coverage.md` | Tự sinh, không sửa tay | |

## Sinh `CONTEXT.md`

1. `flow exclude` trước, để tệp không vào git. Tiếp: `flow context new <dir>`.
2. Đọc theo stack của module, mỗi stack một danh sách đọc và một danh sách trích:
   - [references/nestjs.md](references/nestjs.md)
   - [references/go.md](references/go.md)
   - [references/react.md](references/react.md)
   - [references/dotnet.md](references/dotnet.md)
   - [references/python.md](references/python.md)
3. Điền các mục. Mục không có gì thì ghi `không có`, không để khung.
4. Đọc lại từ đầu, xoá mọi dòng không chắc.
5. `flow context coverage`, `flow doctor`.

## Luật viết

- Chỉ ghi điều kiểm được, kèm `tệp:dòng`. Thứ không kiểm được sẽ thành lời đồn.
- Thang risk: `thấp` tự phục hồi hoặc chỉ ảnh hưởng hiển thị · `vừa` một tính năng hỏng, sửa được · `cao` nhiều người dùng bị ảnh hưởng hoặc dữ liệu sai cần sửa tay · `critical` mất dữ liệu, sai tiền, lộ thông tin.
- Invariant khác validation. Validation kiểm đầu vào của một yêu cầu: `dueDate` phải là ngày hợp lệ. Invariant đúng ở mọi thời điểm dù dữ liệu đến từ đâu: một `Book` không có hai `Loan` đang mở.
- Luật xuyên repo dẫn id, ví dụ `R-0007`, không chép nội dung, để luật chỉ có một nơi phải sửa.
- Chuyển kiến thức từ chú thích sắp xoá vào mục riêng trước khi xoá, kèm `tệp:dòng`.
- Giữ dưới `context.maxLines`. Dài hơn thì tách theo module con hoặc đẩy phần chung sang `.flow/reference/`.
- Không ghi giá trị bí mật, chỉ ghi tên biến.

## `consumed/`

Mỗi service ngoài một tệp, từ `<gói>/templates/consumed.md`: dùng để làm gì, điểm gọi, điều phía ta giả định, hành vi khi bên kia lỗi, tên biến cấu hình. Ghi phía tiêu thụ, không chép tài liệu của họ, vì bản chép sẽ cũ mà không ai biết. Ví dụ: `consumed/identity.md` ghi `Member` đăng nhập qua đâu và claim nào được dùng.

## `reference/`

Mỗi chuẩn dùng chung một tệp, từ `<gói>/templates/reference.md`: tên biến môi trường, sổ phân loại `Book`, bảng mã lỗi. Có mục cách kiểm, để phát hiện được chỗ lệch.

## Chốt

```
flow context coverage
flow doctor
```

Module nghi cũ xử lý bằng skill `flow-sync`. Điều về hệ thống đáng thành luật thì dùng skill `flow-learn`.
