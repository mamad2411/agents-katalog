---
name: ui-checkpoint
description: Chụp screenshot màn hình vừa build qua MCP và hỏi user xác nhận ngắn gọn trước khi commit, thay vì tự động chấm điểm UI bằng vision model (tốn token không cần thiết cho quy mô solo dev). Dùng skill này ngay sau khi mcp-loop báo build sạch lỗi, trước khi git-checkpoint.
---

# UI Checkpoint (Human-in-the-loop nhẹ)

## Vì sao dùng cách này thay vì auto vision QA

Việc dùng thêm một model vision để tự chấm "UI đạt >90% chuẩn design" mỗi lần build tốn thêm lệnh gọi model không cần thiết cho một solo dev đang tự review. Cách rẻ và đủ tốt hơn: chụp ảnh, hỏi 1 câu, để user (chính là bạn) quyết định trực tiếp.

## Quy trình

1. Qua MCP, chụp screenshot màn hình/tính năng vừa build xong (không cần chụp toàn bộ app, chỉ màn hình liên quan đến thay đổi vừa rồi).
2. Hiển thị ảnh trong chat kèm đúng 1 câu hỏi dạng:
   > "Giao diện [tên màn hình] đã ổn chưa? (Gõ 'ok' để commit, hoặc mô tả ngắn cần chỉnh)"
3. Dừng lại, chờ phản hồi user - đây là điểm dừng chủ đích duy nhất trong luồng chính, không tự ý bỏ qua.

## Xử lý phản hồi

- User gõ "ok"/"được"/tương đương → chuyển sang `git-checkpoint/SKILL.md`.
- User mô tả điều chỉnh ngắn (ví dụ "to chữ lên", "xanh hơn", "cách xa nhau hơn") → map sang token cụ thể trong `design-system/SKILL.md`, sửa, quay lại `mcp-loop/SKILL.md` để build lại, rồi lặp lại bước UI-checkpoint này.
- User nói bug logic (không phải UI, ví dụ "bấm không lưu được") → không xử lý ở đây, quay lại `mcp-loop` để debug logic, không nhầm với chỉnh UI thẩm mỹ.

## Tắt bước này khi cần

Nếu user đã dặn trước (ví dụ trong `openspec/config.yaml` mục `rules` có ghi "auto-approve UI, không cần hỏi"), bỏ qua bước này và tự động chuyển sang `git-checkpoint`. Mặc định (chưa dặn gì) LUÔN hỏi.

## Giới hạn phạm vi

Không dùng skill này để duyệt logic nghiệp vụ hay dữ liệu - chỉ để duyệt phần nhìn (UI/UX). Logic sai thuộc về `mcp-loop`, dữ liệu sai thuộc về `schema-migration`.
