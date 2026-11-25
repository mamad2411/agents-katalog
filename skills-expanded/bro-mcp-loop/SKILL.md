---
name: bro-mcp-loop
description: Điều phối vòng lặp khép kín (Autonomous Multi-Agent Loop) giữa Lead Planner (Codex/Cursor), Executor (Antigravity) và Hội đồng Review Triad (Code, UI, QA) qua chuẩn bro-mcp. Kích hoạt khi cần lập plan, giao việc, code, test và review tự động sửa lỗi cho đến khi hoàn thành.
---

# 🔁 bro-mcp: Autonomous Multi-Agent Loop Skill

Skill này đóng gói toàn bộ quy trình phối hợp khép kín giữa các AI Agent mà người dùng không cần phải nhớ hay gọi thủ công từng MCP tool.

---

## 🎯 Khi Nào Kích Hoạt Skill Này?
- Khi người dùng yêu cầu: *"Chạy loop làm tính năng X"*, *"Dùng bro-mcp"*, *"Giao cho Antigravity code rồi Codex review"*, hoặc gõ `/bro-mcp-loop`.
- Khi cần phát triển tính năng mới với yêu cầu nghiêm ngặt: Có kiểm thử tự động, có review độc lập và tự động sửa bug khi có phản hồi.

---

## 🚦 Quy Trình Vận Hành 4 Bước Tự Động (Auto-Orchestration)

### Bước 1: Kiểm Tra Kết Nối (Pre-flight Check)
- Xác nhận server `bro-mcp` đang hoạt động tại `http://localhost:3088/health`.
- Nếu server chưa chạy, nhắc người dùng bật container: `docker compose up -d` tại `f:\wedabro\bro-mcp`.

---

### Bước 2: Vai Trò Lead Planner (Codex / Cursor) — Lập Kế Hoạch & Giao Task
1. Phân tích yêu cầu của người dùng, phân rã WBS và xác định kiến trúc.
2. Thiết lập 2 - 4 tiêu chí **Acceptance Criteria (AC)** rõ ràng dạng Given-When-Then.
3. **Tự động gọi tool MCP**:
   ```json
   bro_dispatch_task({
     "title": "<Tên tính năng ngắn gọn>",
     "description": "<Mô tả kiến trúc và các ràng buộc kỹ thuật>",
     "acceptanceCriteria": [
       "AC1: <Tiêu chí bắt buộc 1>",
       "AC2: <Tiêu chí bắt buộc 2>"
     ],
     "assignedTo": "antigravity",
     "maxIterations": 3
   })
   ```
4. Báo cáo cho người dùng mã `taskId` đã được giao thành công ở trạng thái `DISPATCHED`.

---

### Bước 3: Vai Trò Executor (Antigravity) — Nhận Việc & Thi Công
1. **Tự động gọi tool MCP**:
   ```json
   bro_fetch_task({ "taskId": "<taskId>" })
   ```
2. Đọc toàn bộ specs, tiêu chí AC và hướng dẫn sửa lỗi (nếu đang ở vòng lặp revision).
3. Trực tiếp thực thi:
   - Sửa/tạo file mã nguồn, không để lại placeholder hoặc `TODO`.
   - Chạy kiểm thử tự động trong Docker hoặc terminal.
   - Chụp ảnh giao diện UI / Generative UI render (nếu có frontend).
4. **Tự động gọi tool MCP nộp sản phẩm**:
   ```json
   bro_submit_for_review({
     "taskId": "<taskId>",
     "gitDiff": "<toàn bộ mã thay đổi>",
     "testResults": "<log kết quả chạy test tự động>",
     "uiArtifacts": ["<đường dẫn ảnh giao diện nếu có>"],
     "notes": "<tóm tắt các tiêu chí AC đã hoàn thành>"
   })
   ```
5. Trạng thái task chuyển sang `UNDER_REVIEW`.

---

### Bước 4: Thẩm Định Review Triad & Vòng Lặp Sửa Lỗi (Quality Gate)
Server `bro-mcp` tự động tổng hợp kết quả thẩm định từ 3 chuyên gia:
1. **Code & Security Review** (Codex/Claude): Kiểm tra syntax, Clean Code, bảo mật.
2. **Visual & UI Review** (Claude Vision/Cursor): Kiểm tra responsive, CSS, alignment.
3. **Feature & QA Review** (Claude QA): Đối soát từng mục trong Acceptance Criteria.

#### 🔴 Nếu Bị Từ Chối (Score < 80 hoặc có BLOCKER):
- Task chuyển sang `NEEDS_REVISION`.
- Loop Controller tự động xuất vé lỗi chi tiết (**Actionable Revision Ticket**).
- **Hành động**: Antigravity tự động đọc vé lỗi bằng `bro_fetch_task`, tiến hành sửa triệt để các lỗi được chỉ ra, và gọi lại `bro_submit_for_review` (Vòng lặp tiếp diễn).

#### 🟢 Nếu Được Phê Duyệt (Tất cả PASS & Score >= 80):
- Task chuyển sang `APPROVED`.
- Lead Agent tự động gọi:
   ```json
   bro_complete_task({ "taskId": "<taskId>" })
   ```
- Báo cáo người dùng: Tính năng đã hoàn thành xuất sắc và sẵn sàng merge/commit!
