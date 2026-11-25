---
name: mcp-loop
description: Chạy vòng lặp build/run/fix tự động qua MCP Flutter (mcp_flutter) - chạy app, đọc log, chụp screenshot, tự sửa lỗi compile/overflow, hot reload lại. Dùng skill này ngay sau khi flutter-coding sinh xong code, trước khi đưa cho user duyệt UI.
---

# MCP Loop (Auto-Fix)

## Điều kiện tiên quyết

- MCP server của Dart/Flutter (`mcp_flutter`) đã được cấu hình và cấp quyền chạy `flutter run`, đọc devtools, widget tree, log, chụp screenshot. Nếu không có quyền này, báo cho user cấu hình trước — không đoán kết quả build mà không chạy thật.

## Vòng lặp (tối đa 5 lần)

```
Lần 1..5:
  1. flutter run / hot reload qua MCP
  2. Đọc log build + runtime log
  3. Nếu compile error → đọc message lỗi cụ thể → sửa file liên quan → quay lại bước 1
  4. Nếu build pass → chụp screenshot qua MCP
  5. Đọc widget tree, kiểm tra: text overflow, widget lỗi layout, exception runtime
  6. Nếu phát hiện lỗi → sửa → quay lại bước 1
  7. Nếu sạch lỗi → DỪNG vòng lặp, chuyển sang ui-checkpoint
```

## Khi nào dừng và báo user (không lặp vô hạn)

- Sau 5 lần vẫn còn lỗi compile → thử `rag-fallback/SKILL.md` (fetch doc mới nếu nghi lỗi do API/package deprecated), tối đa 2 lần thử thêm.
- Sau khi thử cả rag-fallback vẫn lỗi → DỪNG hẳn, xuất toàn bộ log lỗi gần nhất cho user, không tiếp tục đoán mò (tránh đốt token vô ích).
- Nếu lỗi thuộc dạng thiếu API key/credential → dừng ngay lập tức (không thuộc phạm vi tự sửa), báo user cần cấu hình `.env`.

## Phân loại lỗi để quyết định hướng sửa

| Loại lỗi | Cách xử lý |
|---|---|
| Compile error do sai cú pháp/import | Tự sửa trực tiếp |
| Compile error do API deprecated | → `rag-fallback` |
| Runtime exception (null check, type error) | Đọc stack trace, sửa logic liên quan |
| UI overflow / layout lỗi | Sửa widget, đối chiếu lại `design-system` |
| Lỗi do thiếu package đã duyệt nhưng chưa `pub get` | Chạy `flutter pub get`, thử lại |
| Lỗi do thiếu package CHƯA duyệt | Dừng, hỏi user (không tự thêm) |

## Ghi chú tiết kiệm token

- Chỉ gửi phần log/error liên quan vào context, không dán toàn bộ log verbose của `flutter run` nếu không cần thiết.
- Dùng widget tree/screenshot only khi nghi ngờ lỗi UI, không cần chụp ảnh nếu chỉ đang sửa lỗi compile thuần logic.
