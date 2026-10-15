---
name: flutter-coding
description: Sinh mã Flutter thật (widget, provider, model, route) dựa trên best-practice của flutter/agent-plugins, tuân theo architecture và design-system đã khóa. Dùng skill này ở bước viết code cụ thể, sau khi đã xác định xong kiến trúc và (nếu cần) migration.
---

# Flutter Coding

## Điều kiện tiên quyết

- `flutter/agent-plugins` phải đã được cài trong project (`npx skills add flutter/agent-plugins --skill '*'`). Nếu chưa thấy skill này available, báo cho user cài trước khi tiếp tục — không tự viết code theo "kinh nghiệm chung chung" thay thế.
- Đã đọc `architecture/SKILL.md` và `design-system/SKILL.md` trong lượt hiện tại.

## Thứ tự ưu tiên khi viết code

1. Instruction từ `flutter/agent-plugins` (Material 3, Riverpod, GoRouter, JSON serialization...) là chuẩn cao nhất.
2. Rule cứng từ `architecture/SKILL.md` (vị trí file, naming) không được vi phạm.
3. Token từ `design-system/SKILL.md` cho mọi giá trị UI.
4. Model/field phải khớp đúng với delta spec trong `openspec/changes/<change-name>/specs/` (đặc biệt sau khi qua `schema-migration`).

## Quy trình viết 1 tính năng

1. Đọc `openspec/changes/<change-name>/{proposal.md, tasks.md, specs/}` liên quan đến tính năng đang làm (dùng `/opsx:continue` nếu change đã tồn tại từ trước).
2. Tạo/sửa file theo đúng cấu trúc `feature/<ten_feature>/{data,domain,application,presentation}`.
3. Model dùng `freezed` + `json_serializable` nếu project đã dùng codegen, giữ nhất quán với các model khác trong project.
4. Provider Riverpod dùng codegen (`@riverpod`), đặt trong `application/`.
5. Route mới đăng ký trong `app/router/` (GoRouter), không hard-code Navigator.push rời rạc.
6. UI trong `presentation/screens|widgets`, ưu tiên tái sử dụng từ `shared/widgets/`.

## Sau khi viết xong

- KHÔNG dừng lại ở "code xong là done". Luôn chuyển sang `mcp-loop/SKILL.md` để build/chạy thử thật.
- Nếu trong lúc code phát hiện cần package chưa có trong danh sách duyệt của `architecture.md` → dừng, hỏi xác nhận, không tự thêm.

## Lỗi thường gặp cần tránh

- Không tạo `setState` tùy tiện trong widget đã có provider quản lý state tương ứng.
- Không tự đổi tên field model đã tồn tại nếu không đi qua `schema-migration` (sẽ vỡ data cũ).
- Không copy nguyên văn code mẫu từ agent-plugins mà không áp token của design-system (dễ bị lệch theme).
