---
name: flow-secrets
description: Dùng khi cần soát khoá, mật khẩu, thông tin cá nhân trong repo có `.flow/` — lúc mới nhận repo, trước khi mở công khai, khi `flow check` có cảnh báo, khi nghi bị lộ, khi cần đọc `.env` hay nối CSDL mà không để lộ giá trị. Người dùng hay nói "có lộ key không", "quét secret", "lỡ commit mật khẩu", "đổi khoá", "dữ liệu cá nhân", "PII".
---

# flow-secrets — bí mật và thông tin cá nhân

In ra là một lần lộ, vì giá trị nằm lại trong lịch sử phiên và có thể được gửi đi. Mọi thao tác dưới đây đều nhằm biết được điều cần biết mà không thấy giá trị.

## Ba lớp dò và điểm mù

| Lớp | Bắt được | Điểm mù |
|---|---|---|
| Hình dạng và gitleaks | Khoá có định dạng nhận ra được | Mật khẩu thường, chuỗi không có khuôn |
| Giá trị thật từ `.env` | Đúng giá trị đang dùng, kể cả khi không có khuôn | Giá trị đã xoay, giá trị không nằm trong `.env`, bản đã mã hoá |
| Danh sách hash | Giá trị hoặc tên riêng đã khai | Điều chưa khai, biến thể khác một ký tự |

Cần cả ba, vì mỗi lớp mù ở chỗ lớp khác thấy. Dòng tóm tắt của lệnh cho biết lớp nào đã chạy: số giá trị từ tệp env, gitleaks có hay không. Lớp không chạy thì kết quả sạch không nói gì về lớp đó.

## Đối chứng

Kết quả rỗng cần chứng minh công cụ bắt được.

- Đọc số dòng đã quét. Quét 0 dòng nghĩa là phép đo hỏng hoặc repo trống, không phải sạch.
- Tự chạy đối chứng: trong một repo git tạm, commit một tệp có khoá giả đúng hình dạng rồi chạy `flow secrets scan --path <repo tạm>`. Không báo gì thì lớp dò đang hỏng, chưa thể kết luận repo thật sạch.

## Lệnh

```
flow secrets scan
flow secrets scan --staged
flow secrets scan --base <ref>
flow secrets scan --history
flow secrets scan --local
flow secrets scan --path <thư mục> --env <tệp>
flow secrets env <tệp>
flow secrets watch --label <nhãn> < <tệp>
flow secrets allow <#mã> --reason "…" --debt
```

- Mặc định quét cây hiện tại, không nói gì về lịch sử. `--history` quét toàn bộ commit.
- `--local` quét bộ não cục bộ `.flow/` và `CONTEXT.md`.
- `secrets env`: xem tên khoá, độ dài, host, không có giá trị.
- `secrets watch`: chỉ lưu hash.
- `secrets allow`: chỉ dùng sau khi đã xem; `--debt` khi còn nợ phải xử lý.

## Phán xử

- Xem theo dạng ký tự, không in: độ dài, tiền tố, loại ký tự. Nhiều nhất là che phần lớn.
- Dương tính giả: `secrets allow` kèm lý do cụ thể.
- Thật: xoay khoá trước, xoá sau, vì xoá khỏi mã không làm khoá hết hiệu lực.
- Đã lên remote: coi như đã lộ, kể cả repo riêng tư, kể cả đã force-push.
- Viết lại lịch sử phải hỏi người dùng, vì nó ảnh hưởng mọi người đang giữ bản sao.
- Không tự xoay khoá dùng chung. Báo người dùng khoá nào, ở đâu, tạo khi nào, không kèm giá trị.

## Thông tin cá nhân

- Loại cần để ý: tên, email, số điện thoại, số giấy tờ, địa chỉ, ngày sinh, số thẻ.
- Mặc định là cảnh báo. Mức thật theo `hygiene.pii`.
- Dữ liệu mẫu và test dùng giá trị giả rõ ràng: `member@example.com`, không dùng dữ liệu thật đã che.
- Không log định danh theo từng request. Cần truy vết thì dùng mã nội bộ của `Member`.

## Thói quen an toàn

| Việc | Tránh | Làm |
|---|---|---|
| Đọc `.env` | `cat .env` | `flow secrets env .env` |
| Kiểm một biến có chưa | `echo $API_KEY` | `test -n "$API_KEY" && echo có` |
| Xem độ dài | In giá trị | `echo ${#API_KEY}` |
| Nối CSDL | Dán URI vào dòng lệnh | Client nhận URI qua biến, vì khi lỗi client có thể in lại đối số |
| Xem cấu hình dạng JSON | In cả tệp | Che theo tên khoá thay vì regex, vì regex bỏ sót dạng lạ |
| Lưu nhật ký chạy | Dán nguyên output | Lọc trước khi ghi |

Bộ não cục bộ cũng không chứa giá trị. `.flow/` chỉ ghi tên biến và nơi lấy, vì nó được agent đọc liên tục.

## Khi nào chạy

- Khi vào dự án: `secrets scan`, `--history`.
- Trước commit: đã có trong `flow check --staged`.
- Trước khi đóng việc: `flow check --base <ref>`.
- Trước khi công khai hoặc chia sẻ repo: `--history`, `--local`.
- Khi nghi lộ: `--history`, rồi xử lý theo mục Phán xử.
