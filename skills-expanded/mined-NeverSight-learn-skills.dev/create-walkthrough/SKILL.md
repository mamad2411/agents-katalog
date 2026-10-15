---
name: create-walkthrough
description: >
  Sử dụng khi kết thúc một session (hoặc nhiều session) để viết walkthrough
  ghi lại quá trình làm việc (incremental), các prompt đã dùng, git history
  và bài học rút ra.
license: "MIT"
metadata:
  author: "thiennq"
  version: "1.0.0"
---

# Skill: /create-walkthrough — Viết nhật ký kỹ thuật cho session

Bạn là một **Tech Writer** đang ghi lại quá trình làm việc giữa user và AI.
Walkthrough không phải tài liệu kiến trúc — nó là **nhật ký có cấu trúc** để cả team:

- Học cách prompt AI hiệu quả (prompt nào dẫn tới kết quả tốt, prompt nào không)
- Re-do lại một tính năng nếu cần (biết chính xác thứ tự bước)
- Hiểu quyết định thiết kế đã được đưa ra tại thời điểm nào, vì sao

---

## Quy trình BẮT BUỘC

```
Bước 1: Xác định phạm vi thời gian (Incremental — No Overlap)

Bước 2: Thu thập dữ liệu từ 2 nguồn (Chat History + Git Log)

Bước 3: Nhóm thành Phase, viết cặp Prompt → Việc đã làm

Bước 4: Viết Lessons Learned + Thống kê

Bước 5: Tạo file vào walkthroughs/
```

---

## Bước 1: Xác định phạm vi thời gian

- Liệt kê các file trong `walkthroughs/`, tìm file có **số thứ tự cao nhất**.
- Đọc YAML frontmatter trường `date` của file đó → đây là **mốc thời gian cutoff**.
- Walkthrough mới **chỉ ghi lại những gì xảy ra SAU mốc cutoff**. Không ghi lại nội dung đã có ở walkthrough trước.
- Nếu chưa có file walkthrough nào → ghi từ đầu dự án.

---

## Bước 2: Thu thập dữ liệu

Hai nguồn dữ liệu **đều quan trọng ngang nhau**, phục vụ mục đích khác nhau:
- **Git History** → cho biết **đã làm gì** (file nào, commit nào, thứ tự nào)
- **Chat History** → cho biết **tại sao làm** (prompt nào, quyết định nào, lỗi nào)

Cả hai đều cần thiết để walkthrough vừa chính xác về mặt kỹ thuật, vừa giữ lại giá trị học hỏi cách prompt AI.

### 2a. Git History — "Đã làm gì"

Chạy lệnh:
```bash
git log --since="YYYY-MM-DD" --format="%h %ai %s" --name-status
```

Từ output, trích xuất:
- **Commit hash + message** — dùng làm anchor cho mỗi Action
- **Danh sách file thay đổi** — biết chính xác những gì đã sửa
- **Thứ tự thời gian** — sắp xếp đúng trình tự

### 2b. Chat History — "Tại sao làm"

Xem conversation summaries gần đây. **LƯU Ý QUAN TRỌNG:**
- **CHỈ** đọc conversation có workspace path trùng với thư mục hiện tại
- KHÔNG lấy nhầm conversation từ dự án khác
- Nếu cần chi tiết, có thể đọc `overview.txt` của conversation cụ thể

Từ chat history, trích xuất:
- **Prompt gốc của user** — nguyên văn hoặc tóm tắt sát nhất
- **Quyết định thiết kế** — user chọn phương án nào, reject phương án nào
- **Lỗi / debug** — AI gặp vấn đề gì, mất bao lâu

### 2c. Uncommitted changes

Chạy `git status -s` và `git diff --stat` để phát hiện các thay đổi chưa commit.
Ghi chú rõ trong walkthrough: `[Uncommitted]`.

---

## Bước 3: Viết file Walkthrough

### Quy tắc file

- **Thư mục:** `walkthroughs/`
- **Tên file:** `XX.md` — XX là số thứ tự tăng dần, bắt đầu từ `01`
- **Encoding:** UTF-8

### Template bắt buộc

```markdown
---
title: "Walkthrough XX — [Tiêu đề ngắn gọn]"
date: "YYYY-MM-DD"
previous: "XX.md"
goal: "[1-2 câu mô tả mục tiêu chính của session]"
---

## Mục lục

1. [Phase 1: ...]
2. [Phase 2: ...]
3. [Lessons Learned]
4. [Kết quả & Thống kê]

---

## Phase 1: [Tên giai đoạn]

### Prompt
> [Trích dẫn prompt gốc của user — nguyên văn hoặc tóm tắt sát nhất]

### Việc đã làm
- Tạo file `src/services/foo.ts` — implement hàm X
- Sửa `index.ts` — register route mới
- Chạy `npm test` — 5/5 pass
- **Commit:** `abc1234` — "feat: add foo service"

*(Nếu Phase có nhiều prompt liên tiếp, lặp lại block Prompt → Việc đã làm)*

---

## Phase 2: [Tên giai đoạn tiếp theo]
...

---

## 💡 Lessons Learned

### ✅ [Bài học tích cực]
[Mô tả cách tiếp cận hiệu quả. Prompt nào dẫn tới kết quả tốt? Pattern nào nên lặp lại?]

### ❌ [Bài học tiêu cực]
[Mô tả sai lầm, thời gian lãng phí. AI hallucinate ở đâu? Prompt nào gây hiểu nhầm?]

---

## 📊 Kết quả & Thống kê

### Tasks hoàn thành
- [Liệt kê task đã done, nếu dùng hệ thống tasks/]

### Breaking changes
- [Nếu có]

### Thống kê
| Metric | Giá trị |
|--------|---------|
| Files changed | ... |
| Tests viết mới | ... |
| Commits | ... |
```

### Frontmatter Schema

| Field | Type | Bắt buộc | Mô tả |
|-------|------|----------|-------|
| `title` | string | ✅ | Tiêu đề walkthrough |
| `date` | `YYYY-MM-DD` | ✅ | Ngày viết — dùng làm mốc cutoff cho walkthrough tiếp theo |
| `previous` | string | ✅ | Tên file walkthrough trước, `null` nếu là file đầu tiên |
| `goal` | string | ✅ | Mục tiêu chính 1-2 câu |

---

## Nguyên tắc viết

1. **Prompt-Centric** — Luôn ghi prompt gốc của user. Đây là giá trị cốt lõi để team học cách làm việc với AI. Nếu prompt dài, tóm tắt ý chính nhưng giữ nguyên intent.

2. **Granular Actions** — Liệt kê từng bước cụ thể AI đã làm:
   - ❌ "Đã implement authentication"
   - ✅ "1. Tạo `auth.middleware.ts` | 2. Thêm `verifyJwt()` | 3. Wrap 7 tools | 4. Test thủ công"

3. **Git-Anchored** — Mỗi nhóm action nên gắn với commit hash khi có. Nếu chưa commit, ghi rõ `[Uncommitted]`.

4. **Phase Grouping** — Nhóm các prompt + action liên quan thành Phase (theo feature hoặc theo giai đoạn). Mỗi Phase có heading riêng trong Mục lục.

5. **Thành thật về lỗi** — Nếu AI gặp lỗi, debug mất thời gian, hoặc user phải sửa lại, GHI VÀO. Đưa vào Lessons Learned với ❌.

6. **Không lố** — Viết ngắn gọn, rõ ràng, đúng sự thật. Không dùng từ ngữ hoa mỹ quá mức. Ưu tiên danh sách bullet hơn đoạn văn dài.

---

## Quy tắc quan trọng

1. **LUÔN thu thập cả Git lẫn Chat** — Git cho biết "đã làm gì", Chat cho biết "tại sao làm". Thiếu một trong hai thì walkthrough mất giá trị.
2. **CHỈ lấy chat từ đúng project** — Check workspace path trong conversation metadata
3. **Incremental only** — Đọc mốc `date` từ walkthrough trước, không ghi đè nội dung cũ
4. **Khi mâu thuẫn, ưu tiên Git** — Nếu chat nói sửa file A nhưng git không thấy → kiểm tra lại, có thể chưa commit
5. **1 session lớn = 1 file** — Dù có nhiều feature, vẫn gom vào 1 walkthrough, tách Phase
