---
name: flow-test
description: Dùng khi viết, chỉnh, chuyển chỗ hoặc đánh giá test trong repo có `.flow/`, gồm test cho task trong plan, test giữ lỗi không quay lại, test hợp đồng, test cho script kiểm hoặc hook, test đồng thời; hoặc khi xanh mà chưa tin. Người dùng hay nói "thêm test", "test trước", "sao test vẫn xanh", "test này chạy thật không", "đủ test chưa".
---

# flow-test — thiết kế test

Test phải có khả năng thất bại. Test không thể đỏ thì không chứng minh gì.

## Vòng đỏ-xanh

1. Viết test, chạy, thấy đỏ.
2. Đọc thông báo đỏ: phải đỏ đúng lý do. Đỏ vì lỗi import hay sai fixture thì chưa tính.
3. Viết mã, chạy, thấy xanh.
4. Kiểm test thật sự được chạy: đếm số test trước và sau, số phải tăng đúng phần đã thêm, vì mẫu lọc sai có thể cho xanh với không test nào.
5. Lỗi khó: tạm tháo bản sửa, xác nhận test đỏ lại, rồi trả bản sửa về.

Lệnh chạy một test và đếm test theo stack: [references/stacks.md](references/stacks.md).

## Thiết kế ca

- Đối chứng âm và dương: `Member` đủ điều kiện được mượn, `Member` đang nợ quá hạn bị từ chối. Thiếu một chiều thì test có thể xanh nhờ hàm luôn trả cùng một kết quả.
- Biên: rỗng, một phần tử, đúng ngày hẹn trả, trước và sau một ngày.
- Idempotency: gọi hai lần trả `Loan` thì trạng thái và phí không đổi ở lần hai.
- Đồng thời: hai `Member` cùng mượn cuốn cuối cùng thì chỉ một người được. Dùng tiến trình hoặc kết nối thật, không dùng mock.
- Fixture đủ lớn: phân trang, chỉ mục, bộ đệm chỉ lộ lỗi khi vượt ngưỡng.
- Mock quá nhiều thì không chứng minh hiệu ứng: nếu test chỉ xác nhận mock được gọi, hãy đọc lại trạng thái thật trong CSDL.
- Tên ca mô tả hành vi: `từ chối gia hạn khi đã gia hạn một lần`, không phải `test renew 2`. Ngôn ngữ theo `language.team`.

## Công cụ kiểm và hook

Công cụ kiểm cũng là mã và cần test.

- Logic thuần, phụ thuộc tiêm vào: hệ tệp, git, đồng hồ đều truyền vào để test được.
- Chạy offline, không cần mạng hay dịch vụ ngoài.
- Đổi từng yếu tố một giữa các ca, để biết yếu tố nào quyết định kết quả.
- Có ca tự đối chứng: một đầu vào biết chắc phải bị bắt, chạy cùng mỗi lần. Ca này không đỏ nghĩa là công cụ hỏng.
- Neo theo ngữ nghĩa, không theo số dòng hay thứ tự in, để công cụ không gãy khi đổi định dạng.
- Công cụ đỏ thường trực phải sửa hoặc gỡ, vì đỏ quen mắt thì không ai đọc nữa.

## Đặt test

Theo quy ước đo được của repo: `flow fingerprint` và các test xung quanh. Không mang cấu trúc từ repo khác. Dời test thì đếm trước và sau để chắc không mất ca.

## Mẫu báo cáo

```
Ca đã thêm:     <tên ca>
Đỏ trước:       <thông báo đỏ, đúng lý do không>
Xanh sau:       <lệnh>
Đếm:            <trước> → <sau>
Đối chứng:      <âm, dương, hoặc tháo bản sửa>
Chưa kiểm được: <gì, vì sao>
```
