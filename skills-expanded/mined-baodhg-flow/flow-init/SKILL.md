---
name: flow-init
description: Dùng khi người dùng muốn đưa một dự án vào quy trình lần đầu — dự án trắng, repo đang có đội làm chung, hệ thống đang chạy production, hoặc repo đã có sẵn tài liệu cho agent cần nhận về. Người dùng hay nói "khởi tạo", "cài quy trình cho repo này", "mới vào dự án", "tôi vừa nhận repo này", "init".
---

# flow-init — vào dự án

Bộ skill trung tính: không giả định stack, ngôn ngữ hay kiểu commit. Đo trước, cấu hình sau, hỏi phần lệch.

## Ai thắng ở đâu

- Thứ đội nhìn thấy (commit, PR, tên test, định dạng mã, ngôn ngữ tài liệu): theo đội.
- Thứ chỉ người dùng thấy (ngôn ngữ chat, ghi chú trong `.flow/`): theo người dùng.

Sở thích cá nhân xem bằng `flow user`, đặt bằng `flow user set <khoá> <giá trị>`. Lớp này luôn nằm dưới quy ước dự án.

## Các bước chung

1. `flow fingerprint` — đo quy ước, không ghi gì. Đọc kết quả trước khi quyết định.
2. `flow init` — tạo `.flow/` và ghi `.git/info/exclude`. Thêm `--stack`, `--gates`, `--comments`, `--commit-body`, `--context`, `--name` khi kết quả đo chưa đúng.
3. `flow onboard` — xem điều còn lệch. Hỏi người dùng trên chat, ghi bằng `flow onboard decide <Dn> <số>`.
4. Soát `modules`, `verify`, `canonical` trong `.flow/profile.json`. Điền `.flow/PROJECT.md` và `.flow/services.md`.
5. Rà bí mật ngay, dùng skill `flow-secrets`, vì nên biết trước khi có thêm công cụ đọc repo.
6. Làm theo loại dự án dưới.
7. Chốt.

## Bốn loại dự án

### Dự án mới

- Sở thích người dùng trở thành quy ước.
- Điền bản đồ service và module từ thiết kế, kể cả khi chưa có mã.
- Gieo vài luật đầu tiên bằng `flow rules new`, mỗi luật có cách kiểm.
- Chọn gate theo rủi ro: `flow init --gates ui-change,schema-migration`.

### Repo có đội

- Đọc tệp chỉ dẫn của dự án trước mọi thứ khác, vì chúng thắng bộ skill.
- `verify` ưu tiên đúng lệnh CI đang chạy, để kết quả cục bộ và CI khớp nhau.
- Không sinh ngữ cảnh hàng loạt. Module nào chạm tới thì sinh khi đó bằng skill `flow-context`.
- Không đổi quy ước của đội, không thêm tệp lên repo.

### Hệ đang chạy production

- Bắt đầu chỉ đọc, đặt `autonomy.level` là `local`.
- Đo baseline: `flow verify` để biết cái gì đỏ sẵn, nếu không sẽ không phân biệt được lỗi cũ với lỗi do mình gây ra.
- Rút luật từ lịch sử sửa lỗi (`git log --grep`) và hỏi người dùng những điều cấm kỵ, vì chúng hiếm khi nằm trong mã.
- Xác nhận `branches.protected` và `branches.ownerOnly` với người dùng.
- Viết characterization test trước khi sửa, để giữ hành vi đang có.
- Chỉ chặn trùng lặp mới: `flow dup baseline`.
- Mọi thao tác production đi qua runbook, dùng skill `flow-runbook`.

### Có sẵn hệ ngữ cảnh

- Trỏ vào qua `layout.legacy`, `layout.moduleContext`, `layout.contracts`. Không di chuyển, không đổi tên, vì người khác và công cụ khác đang dùng chúng.
- Tên tệp ngữ cảnh module khác mặc định thì dùng `flow init --context <tên>`.
- Dự án có chủ trương track tài liệu harness thì dùng `--track-harness`, không tự quyết.

## Chốt

```
flow reindex
flow context coverage
flow doctor
flow sync --mark
```

`flow onboard refresh` để đo lại khi quy ước của dự án đổi. `sync --mark` chỉ chạy khi đã đọc ngữ cảnh hiện có và kiểm với mã.

## Báo cáo

Ngắn, gồm:

- Loại dự án và lý do xếp vào loại đó
- Quy ước đo được, phần người dùng đã chốt
- Lệnh verify và cái gì đang đỏ sẵn
- Kết quả rà bí mật
- Điều còn thiếu và bước kế tiếp
