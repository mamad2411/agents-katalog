---
description: Sinh ma trận truy vết (RTM) Requirements ↔ Test Cases ↔ Automation Scripts — chỉ ra requirement chưa cover, TC chưa automate, và orphan tests.
skills:
  - skills-coverage-traceability
  - skills-requirements-analyzer
  - skills-rbt-manual-testing
---

# Workflow: Sinh Ma Trận Truy Vết (RTM)

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`skills-coverage-traceability`** (tại `.claude/skills/skills-coverage-traceability/SKILL.md`) trước khi bắt đầu.

## ⚠️ Nguyên tắc thực thi

- **Tất cả output bằng Tiếng Việt**
- **KHÔNG bịa mapping** — không chắc thì để trống và đưa vào mục "cần xác nhận"
- Mapping suy luận (theo tên/mô tả, không có ID) phải đánh dấu ⚠️ và tách riêng khỏi mapping có ID
- KHÔNG tự ý sửa file TC/test gốc để thêm ID — chỉ đề xuất

## Input cần thu thập

| Nguồn | Bắt buộc? | Ghi chú |
|---|---|---|
| Requirements (markdown/Jira export/user stories) | Cần ≥2 nguồn | Có thể lấy từ `/fetch-jira-requirements` |
| Manual test cases (markdown/Excel/CSV) | Cần ≥2 nguồn | |
| Automation scripts (path thư mục test) | Cần ≥2 nguồn | Agent tự scan `.spec.ts`, `*Test.java`, `.py` |

> Có đủ 3 nguồn → RTM 3 tầng đầy đủ. Chỉ có 2 nguồn → RTM 2 chiều, ghi chú rõ phần thiếu. Chỉ có 1 nguồn → dừng, hỏi user bổ sung.

## Các bước thực hiện

### Bước 1: Thu thập & Trích xuất
1. Đọc từng nguồn, xác định format ID (`REQ-xxx`, `TC_xxx`, tên test method)
2. Liệt kê đầy đủ: REQ IDs, TC IDs, test methods (kèm file path)
3. Nếu TC/test không có ID chuẩn → ghi nhận để đề xuất bổ sung ID ở output

### Bước 2: Mapping
1. Map bằng ID trước (chuẩn nhất)
2. Map bằng nội dung cho phần không có ID → đánh dấu ⚠️
3. Ghi nhận quan hệ n-n đầy đủ

### Bước 3: Tính Metrics & Phát Hiện Gap
1. Requirement Coverage / Automation Coverage / Orphan Tests
2. Phân loại: 🔴 REQ chưa cover → 🟡 TC chưa automate → ⚪ orphan tests
3. **⬛ Module chưa có tài liệu — điểm mù của RTM, BẮT BUỘC kiểm:**
   Đọc `docs/requirements/README.md`, liệt kê module có `Trạng thái recon` = ⬜ / 🟨 / ⏸️.
   Những module này **không có REQ nào**, nên RTM tính đúng theo công thức vẫn ra coverage cao — trong khi cả một module chưa ai chạm tới. Không nêu ra thì con số RTM **gây hiểu nhầm nghiêm trọng**.
   Chưa có file danh mục (chưa chạy `/discover-system`) → ghi rõ: *"Chưa khảo sát cấp hệ thống — không kết luận được RTM đã phủ hết hệ thống hay chưa"*.

### Bước 4: Xuất RTM (CHECKPOINT)
1. Sinh `traceability_matrix.md` theo template trong skill
2. Nếu user cần import Excel → sinh thêm `traceability_matrix.csv`
3. **⏸️ Trình bày kết quả** — nhấn mạnh mục 🔴 và mục ⚠️ cần user xác nhận
4. Đề xuất bước tiếp theo: khảo sát module còn ⬜ (`/generate-requirements-from-website`), sinh TC lấp gap (`/generate-testcases-from-requirements`), automate TC ưu tiên cao (`/generate-automation-from-testcases`)

## Output

- File `traceability_matrix.md`:
  - Bảng tổng quan 3 metrics
  - Ma trận chi tiết REQ ↔ TC ↔ Automation
  - Danh sách ⬛ **module chưa có tài liệu** (nằm ngoài phạm vi RTM) — đặt **trên** mọi metric khác, kèm cảnh báo coverage % chỉ tính trên module đã có tài liệu
  - Danh sách 🔴 REQ chưa cover (kèm đề xuất)
  - Danh sách 🟡 TC chưa automate (xếp theo priority)
  - Danh sách ⚪ orphan tests
  - Mục ⚠️ mapping suy luận cần xác nhận
- File `traceability_matrix.csv` (nếu user yêu cầu)

> 📊 **Xem trực quan:** mở `scripts/execution-viewer/bundle.html` rồi kéo thả `traceability_matrix.md` vào → tab **Độ phủ automation**. Trang này tự tính lại chỉ số từ bảng "Ma trận chi tiết" (không đọc bảng Tổng quan), tách riêng trạng thái **automate một phần**, và xuất Excel nhiều sheet. Nhắc user điều này ở bước bàn giao.
