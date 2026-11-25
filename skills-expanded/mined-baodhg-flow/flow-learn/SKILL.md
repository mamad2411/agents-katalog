---
name: flow-learn
description: Dùng khi người dùng chỉnh cách bạn làm việc, khi bạn nhận ra mình vừa làm sai, khi vừa tìm ra nguyên nhân gốc của một lỗi, khi ledger có mục ma sát, và ở bước cập nhật ngữ cảnh lúc đóng việc. Người dùng hay nói "nhớ nhé", "từ giờ", "lần sau đừng", "luôn phải", "ghi vào luật", "thêm rule".
---

# flow-learn — ghi điều học được

## Hai kho cục bộ

| Kho | Chứa | Ví dụ |
|---|---|---|
| `.flow/rules/` | Điều về hệ thống | Một `Book` không có hai `Loan` đang mở |
| `.flow/memory/` | Điều về cách làm việc | Người dùng muốn thấy diff trước khi commit |

## Có đáng ghi không

Ghi khi trả lời có cả ba:

1. Đọc mã không suy ra được?
2. Lần sau một agent mới có khả năng sai lại?
3. Có cách kiểm, hoặc là sở thích rõ ràng của người dùng?

Không ghi tóm tắt việc vừa làm, không ghi điều đã có trong mã hay trong git.

## Dạng bền nhất có thể

Chọn dạng cao nhất làm được, vì thứ chạy tự động không phụ thuộc vào việc có ai đọc:

```
test > check máy > gate > luật > memory
```

- Test: khi hành vi kiểm được bằng mã. Dùng skill `flow-test`.
- Check máy: mẫu cấm grep được, khai ở `hygiene.customChecks`.
- Gate: danh sách cần nhìn khi chạm một loại tệp, ở `.flow/gates/`.
- Luật: điều đúng về hệ thống mà máy chưa kiểm được.
- Memory: cách làm việc, sở thích.

## Ghi

Tìm trùng trước, vì hai luật nói cùng một điều sẽ dần mâu thuẫn. Có rồi thì sửa bản cũ.

```
flow rules find --text "<từ khoá>"
flow memory --text "<từ khoá>"
```

Luật:

```
flow rules new --title "Một Book không có hai Loan đang mở" --type invariant --severity critical --scope "src/loan/**" --tags loan --enforced "test: loan.concurrency"
```

Mỗi luật có bốn mục, điền đủ, không chép định dạng từ nơi khác:

- `Luật`: một câu, kiểm được
- `Vì sao`: hậu quả khi vi phạm
- `Cách kiểm`: lệnh, test hoặc truy vấn
- `Sự cố gốc`: điều dẫn tới luật này trong dự án

Memory:

```
flow memory new --type feedback --name "xem-diff-truoc-commit" --desc "Cho người dùng xem diff trước khi commit"
```

Xong chạy `flow reindex`, `flow doctor`.

## Ranh giới dự án ↔ bộ skill

Dự án là nơi học. Bộ skill chỉ giữ nguyên lý chung. Hai bên không được lẫn vào nhau, vì bộ skill đi theo người dùng sang mọi dự án khác.

**Ở lại trong `.flow/` của dự án, không bao giờ đi vào bộ skill:** tên, mã, số liệu, sự cố, từ nghiệp vụ, dữ liệu, cùng mọi kiến thức cụ thể khác của dự án.

**Chỉ được đưa vào bộ skill** một nguyên lý đã khái quát thành thực hành chung, thoả đủ:

- Viết lại hoàn toàn bằng lời mới
- Không có định danh
- Không có số liệu
- Không kể chuyện cụ thể
- Ví dụ dùng miền hư cấu, như thư viện cho mượn sách
- Áp dụng được cho một dự án xa lạ

Không chép mã. Không chép câu từ của dự án.

**Quy trình:**

1. Agent không tự sửa bộ skill giữa task, kể cả khi thấy rõ chỗ sai.
2. Ở bước post, đề xuất cho người dùng trên chat, kèm bản nháp đã khái quát.
3. Được đồng ý mới sửa.
4. Chạy, cả hai phải sạch:

```
flow selftest
flow provenance --against <dự án>
```

**Từ riêng của một dự án** (ví dụ thuật ngữ để nhận diện tên định danh) khai trong `.flow/profile.json`, ở `hygiene.namingTerms`, không đưa vào bộ skill.

## Khi nào

- Người dùng sửa cách làm: ghi ngay, không đợi cuối task.
- Vừa phát hiện mình sai: ghi trước khi làm tiếp.
- Một lỗi tìm ra nguyên nhân gốc: thêm test, rồi luật nếu còn cần.
- Ở skill `flow-post`: đọc mục `friction` trong ledger, chọn dạng bền nhất.
