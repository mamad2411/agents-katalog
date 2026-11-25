---
name: flow-review
description: Dùng khi cần một cặp mắt không dính vào lúc viết để soát thay đổi — sau một đợt task, trong bước đóng việc, trước khi mở PR, hoặc khi nghi có lặp mã. Người dùng hay nói "soát giúp", "xem lại code", "đọc diff này", "có lặp code không", "review", "đủ chuẩn để merge chưa".
---

# flow-review — soát độc lập

Người viết thấy điều mình định viết, không thấy điều mình đã viết. Vì vậy review do một subagent mới làm, không phải chính phiên đang viết.

## Gói giao cho subagent

Chỉ gồm:

- Diff: `git diff <nhánh gốc>...HEAD`, hoặc diff của đợt task
- Mục tiêu: mục tiêu plan và danh sách task, hoặc một câu nếu không có plan
- Luật khớp: `flow rules find --changed`
- Kết quả công cụ: `flow check --base <nhánh gốc>`, `flow dup check --base <nhánh gốc>`, verify

Không đưa kết luận hay lập luận của người viết, vì chúng neo người soát vào cùng một cách nhìn. Không nói "phần này đã ổn".

## Hai kết luận riêng

Một thay đổi có thể đúng plan mà mã kém, hoặc mã đẹp mà lệch plan, nên không gộp.

### Đúng plan

- Mọi task đã làm đủ, không làm thừa ngoài phạm vi
- Test chứng minh đúng hành vi plan nói
- Thứ tự triển khai, hợp đồng, rollback còn khớp với plan

### Chất lượng

- DRY: có hàm mới trùng ý đồ với hàm có sẵn. Dùng `flow dup find` chứ không chỉ đọc diff, vì bản gốc thường nằm ngoài diff.
- Ranh giới: logic nằm đúng tầng, không xuyên module
- Lỗi im lặng: `catch` rỗng, mặc định che lỗi, kết quả bỏ qua
- Đồng thời: tranh chấp ghi, thiếu transaction, thao tác không idempotent
- Tên: nói đúng việc, theo quy ước repo
- Bảo mật cơ bản: kiểm quyền, nối chuỗi vào SQL, in bí mật, log thông tin cá nhân

## Định dạng kết quả

```
Đúng plan: đạt | không đạt
Chất lượng: đạt | không đạt

- [chặn] `loan/renew.ts:42` — thiếu transaction khi gia hạn `Loan` — hai yêu cầu đồng thời cùng qua — bọc trong transaction, thêm test đồng thời
- [nên sửa] `loan/format.ts:10` — trùng ý đồ với `formatDueDate` — dùng lại bản có sẵn
- [gợi ý] `loan/renew.ts:7` — tên `data` chưa nói gì
```

Mỗi mục có `tệp:dòng`, vấn đề, hệ quả, cách sửa.

| Mức | Nghĩa | Xử lý |
|---|---|---|
| `chặn` | Sai hành vi, mất dữ liệu, vi phạm luật | Phải sửa trước khi đi tiếp |
| `nên sửa` | Làm việc được nhưng để lại nợ | Sửa, hoặc ghi lý do không sửa |
| `gợi ý` | Tuỳ ý | Người viết tự quyết |

## Vòng lặp

Tối đa hai vòng. Sửa xong gửi diff mới cho subagent mới. Sau hai vòng vẫn còn mục chặn thì hỏi người dùng trên chat, vì lúc đó thường là bất đồng về thiết kế, không phải lỗi mã.

Người viết không tự bác mục chặn. Không đồng ý thì nêu lý do cho người dùng.

## Khi nào

- Sau mỗi task rủi ro hoặc mỗi đợt task trong skill `flow-execute`: soát phần vừa làm.
- Ở skill `flow-post`: review cuối soát cả nhánh, vì lỗi hay nằm ở chỗ các task ghép với nhau.
