---
name: boot
description: Đọc doctrine + diagram + evidence gần nhất của agent-hub, báo cáo trạng thái phiên trong đúng 6 dòng. Dùng đầu mỗi phiên làm việc.
---

# /boot

> Đọc, KHÔNG sửa gì. Launchpad 60 giây cho một phiên "nguội" — không cần
> re-scan toàn bộ codebase mỗi lần.

## 7 bước, đúng thứ tự
1. Đọc `agent-hub/NORTHSTAR.md`.
2. Nhớ lại forbidden states + seal gate từ `agent-hub/CLAUDE.md` — [GUARD,
   thêm 2026-08-30] KHÔNG tự `cat`/`Read` file này: harness tự bơm lại
   toàn bộ nội dung file này qua nested-CLAUDE.md `<system-reminder>` ngay
   khi bước 1 chạm vào bất kỳ file nào dưới `agent-hub/` — đọc tay ở đây
   chỉ tạo ra 1 bản trùng thứ 2 trong context. Chỉ đọc tay nếu bản tự bơm
   đó không xuất hiện trong phiên này.
3. Đọc `agent-hub/doctrine/MEMORY.md` — lấy path, stack, lệnh chính xác.
4. Đọc `agent-hub/doctrine/domains/PROJECT.md` — invariants/traps/decisions.
5. Đọc mọi file trong `agent-hub/haven/diagrams/` **TRỪ** file có chữ
   `archive` trong tên (`dev-loop-archive.md`...) — [sửa 2026-09-05] đó là
   cold storage theo thiết kế (xem ghi chú token-discipline trong
   `dev-loop.prime-mermaid.md` + `hub-tokens.md`), đọc lại mỗi phiên phá
   vỡ đúng mục đích archive. Chỉ đếm node + PM status từ file KHÔNG phải
   archive.
6. Đọc `agent-hub/haven/workers/*/manifest.yaml` — roster worker khả dụng.
7. Đọc tối đa 5 evidence note gần nhất trong `agent-hub/evidence/`
   (implementer + verifier, mới nhất trước). Để liệt kê, dùng
   `find <dir> -maxdepth 2 -type f -name "*.md" -exec ls -t {} + | head -5`
   — [GUARD, thêm 2026-08-30] KHÔNG dùng `ls -lat <dir>` trực tiếp: đã ghi
   nhận trả về sai (listing của thư mục khác thay vì thư mục evidence thật)
   trong một sandbox thật — lỗi shell/alias, không phải lỗi riêng của
   project này. `find` là dạng đã kiểm chứng ổn định.

## Report — đúng 6 dòng, không hơn
```
🎯 Northstar: <one sentence từ NORTHSTAR.md>
✅ Forbidden: <none active | tên state nếu có tín hiệu vi phạm>
📊 Diagrams: <N nodes = X sealed, Y pending, Z in_progress>
🔧 Workers: implementer, verifier
📝 Last action: <node — verdict — date, hoặc "none yet">
🚧 Blockers: <danh sách <<FILL>> còn mở trong doctrine/MEMORY.md, hoặc "none">
```

## Rules
- Không sửa file nào trong bước này — `/boot` là read-only.
- Nếu `doctrine/MEMORY.md` còn `<<FILL>>` ở lệnh test/build, liệt kê rõ
  trong dòng Blockers — đây là tín hiệu đúng, không phải lỗi.
- Nếu chưa từng `/boot` trong phiên hiện tại và sắp dùng `/worker` hoặc
  `/todo`, chạy `/boot` trước — không bỏ qua kể cả việc nhỏ.
- Nếu bước 5 phát hiện diagram active vượt ~15KB (hoặc `/hub-tokens` báo
  vậy), đó là tín hiệu thật để chạy 1 đợt archive — xem ghi chú token-
  discipline ngay trong `dev-loop.prime-mermaid.md`. `/boot` không tự sửa
  gì — archive là hành động riêng, tường minh.
