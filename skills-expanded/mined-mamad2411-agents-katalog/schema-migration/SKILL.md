---
name: schema-migration
description: Xử lý khi Data Model trong delta spec của OpenSpec (openspec/changes/<change-name>/specs/) thay đổi so với spec đã archive (openspec/specs/) - thêm/xóa/sửa field, đổi kiểu dữ liệu - để tránh crash do local database (Hive/SQFLite/Drift) hoặc parse JSON API bị lệch schema cũ. LUÔN dùng skill này TRƯỚC KHI sinh code, ngay khi phát hiện Data Model mới khác với model hiện có trong code.
---

# Schema Migration

## Khi nào trigger

`project-orchestrator` phát hiện Data Model trong delta spec (`openspec/changes/<change-name>/specs/<domain>/spec.md`) khác với model đã archive (`openspec/specs/<domain>/spec.md`) hoặc khác với model thật trong code (thêm field, đổi tên, đổi kiểu, xóa field). Đây LUÔN LÀ bước bắt buộc trước khi `flutter-coding` sửa model, không được bỏ qua kể cả khi thay đổi có vẻ nhỏ.

## Quy trình

1. **Diff model**: so sánh field cũ (trong `openspec/specs/<domain>/spec.md` đã archive, đối chiếu code thật qua codebase-memory nếu có) với field mới (delta spec trong `changes/<change-name>/specs/`). Liệt kê rõ: field nào thêm, field nào xóa, field nào đổi kiểu.

2. **Xác định loại lưu trữ đang dùng**: local DB (Hive/SQFLite/Drift) hay chỉ gọi API/Firebase không lưu local.
   - Nếu chỉ dùng API/Firebase không cache local → thường chỉ cần cập nhật model + parse JSON, rủi ro thấp hơn, vẫn nên test qua MCP.
   - Nếu có local DB → bắt buộc viết migration script (không sửa model rồi để app tự crash lần chạy sau).

3. **Sinh migration script** tương ứng:
   - SQFLite/Drift: viết `ALTER TABLE` hoặc bump `version` + `onUpgrade`.
   - Hive: tạo `TypeAdapter` version mới, viết logic đọc dữ liệu cũ và map sang field mới (field mới thêm cần giá trị mặc định).

4. **Chạy thử migration qua MCP** trên simulator/dev trước khi cho phép `flutter-coding` sửa code chính thức dùng model mới. Nếu app dữ liệu mẫu (seed data) đang có sẵn, test load lại dữ liệu cũ qua migration để chắc không mất/lỗi data.

5. **Nếu migration fail**: rollback (dùng git checkpoint gần nhất, xem `git-checkpoint/SKILL.md`), sửa lại script, không cố sửa đè lên code đã lỗi.

6. Sau khi migration pass → mới chuyển sang `flutter-coding/SKILL.md` để cập nhật phần code dùng model mới (UI, provider...).

## Ví dụ cụ thể

> Ngày 7, delta spec trong `changes/add-product-color/specs/product/spec.md` thêm field `color` (String) vào model `Product` (vốn chỉ có `id`, `name` trong `openspec/specs/product/spec.md` đã archive).

- Diff: thêm field `color`, kiểu String, cần giá trị mặc định (ví dụ `""` hoặc `null` cho phép).
- Nếu dùng Hive: bump `Product` TypeAdapter, field mới đánh dấu optional/default để đọc được record cũ không có field này.
- Test: load lại 1 record cũ (không có `color`) qua adapter mới, xác nhận không crash, `color` trả về giá trị mặc định.
- Pass → mới cho `flutter-coding` sinh UI hiển thị `color` trong màn hình Product.

## Không làm gì nếu đây là project mới hoàn toàn

Nếu chưa có data thật (project mới init, model đầu tiên) thì không cần migration script, chỉ cần định nghĩa model đúng ngay từ đầu và bỏ qua bước này.
