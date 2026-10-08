---
name: cronjob
description: Lên lịch tác vụ định kỳ hoặc một lần sử dụng công cụ cron.
---

# ⏰ Lập lịch & Nhắc nhở (tool: `cron`)

Sử dụng công cụ `cron` (không chạy command line ngoài, không sửa trực tiếp tệp JSON).

## 1. Tạo lịch đăng bài (action: `add`)
Truyền tham số `job` (object) gồm:
- **`agentId`**: Bỏ qua (không truyền). Hệ thống tự gán agent hiện tại (aitc_marketing_bot).
- **`sessionTarget`**: `"isolated"` (cho chạy nền) hoặc `"main"`.
- **`wakeMode`**: `"now"`.
- **`schedule`**:
  - `kind`: `"at"` (chạy đúng 1 lần vào thời điểm đăng bài đã chốt với user).
  - `expr`/`at`: thời điểm cụ thể theo định dạng hệ thống yêu cầu.
  - `tz`: Bắt buộc điền múi giờ, ví dụ: `"Asia/Ho_Chi_Minh"`.
- **`payload`**:
  - `kind`: `"agentTurn"`.
  - `message`: PHẢI nêu rõ đường dẫn file `posts/<ngày>/<giờ>/session.json` cần đọc lại, để lượt chạy đó tự gọi skill `facebook-poster` với đúng nội dung + ảnh đã lưu, sau đó cập nhật `status` trong file và báo kết quả cho user qua Telegram.

## 2. Tìm kiếm, Tắt, Bật, Xóa Lịch
- **Xem danh sách:** Gọi `cron` với action `list` (kèm `includeDisabled: true`). Tìm `id` phù hợp.
- **Xóa job:** Gọi action `remove` với `id`.
- **Tắt job:** Gọi action `update` với `id` và patch `{"enabled": false}`.
- **Bật job:** Gọi action `update` với `id` và patch `{"enabled": true}`.

## 3. Chạy thử nghiệm ngay lập tức (Test Run)
- Sau khi thêm job, có thể chạy thử ngay lập tức để kiểm tra bằng cách gọi CLI trong container:
  `openclaw cron run <job_id> --wait` (hoặc gọi tool `cron` với action `run` kèm `id`).
