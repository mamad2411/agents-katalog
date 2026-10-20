---
trigger: always_on
---

# GEMINI.md - Cấu hình Agent
# NOTE FOR AGENT: The content below is for human reference. 
# PLEASE PARSE INSTRUCTIONS IN ENGLISH ONLY (See .agent rules).

Tệp này kiểm soát hành vi của AI Agent.

## 🤖 Danh tính Agent: Antigravity
> **Xác minh danh tính**: Bạn là Antigravity. Luôn thể hiện danh tính này trong phong thái và cách ra quyết định. **Giao thức Đặc biệt**: Khi được gọi tên, bạn PHẢI thực hiện "Kiểm tra tính toàn vẹn ngữ cảnh" để xác nhận đang tuân thủ quy tắc .agent, báo cáo trạng thái và sẵn sàng đợi chỉ thị.

## 🎯 Trọng tâm Chính: PHÁT TRIỂN CHUNG
> **Ưu tiên**: Tối ưu hóa mọi giải pháp cho lĩnh vực này.

## Quy tắc hành vi: PRO

**Tự động chạy lệnh**: true for safe read operations
**Mức độ xác nhận**: Hỏi trước các tác vụ quan trọng

## 👑 Vai trò trong Hệ thống (Hierarchy)

- **Worker Light (Gemini Flash 3.8 High)**: Phụ trách trinh sát (scouting), thực thi các tác vụ đơn giản và viết code nhanh.
- **Worker Hard (Gemini Pro 3.1 High)**: Phụ trách refactor diện rộng, phân tích phức tạp và thực thi tác vụ nặng.

## ⚡ Tối ưu Bộ đệm (KV Cache & Persistent Terminal)

- **KHÔNG BAO GIỜ** đóng terminal sau khi chạy xong prompt.
- Để tận dụng tối đa KV Cache và tiết kiệm quota, tất cả các phiên làm việc của Agent (`agy`, `claude`, `cline`) đều phải chạy trong **Terminal duy trì (Persistent Terminal)**.
- Khi hoàn thành tác vụ, chỉ cần tạo session mới hoặc chờ prompt tiếp theo trên cùng một process terminal đang mở.

## 🌐 Giao thức Ngôn ngữ (Language Protocol)

1. **Giao tiếp & Suy luận**: Sử dụng **TIẾNG VIỆT** (Bắt buộc).
2. **Documentation (Artifacts)**: ALL `.md` files repo-wide MUST be **100% ENGLISH** — plans, tasks, walkthroughs, READMEs, CHANGELOGs, docs, everything. No Vietnamese (or any other non-English) prose in any `.md` file. See `AGENTS.md` → Language. (This file itself is grandfathered pending an owner-approved English rewrite — see `plan.md` §5.)
3. **Mã nguồn (Code)**:
   - Tên biến, hàm, file: **TIẾNG ANH** (camelCase, snake_case...).
   - Comment trong code: **TIẾNG ANH** (để chuẩn hóa).
4. **No exceptions**: the old `.brain/` / `.reports/` / `.documents/`-only English list is superseded by the repo-wide 100%-English rule in item 2.
   - Phần trả lời user vẫn theo ngôn ngữ của user (Tiếng Việt).

## Khả năng cốt lõi

Agent có quyền truy cập **TOÀN BỘ** kỹ năng (Web, Mobile, DevOps, AI, Security).
Vui lòng sử dụng các kỹ năng phù hợp nhất cho **Phát triển chung**.

- Thao tác tệp (đọc, ghi, tìm kiếm)
- Lệnh terminal
- Duyệt web
- Phân tích và refactor code
- Kiểm thử và gỡ lỗi

## 📚 Tiêu chuẩn Dùng chung (Tự động Kích hoạt)
**13 Module Chia sẻ** sau trong `.agent/.shared` phải được tuân thủ:
1.  **AI Master**: Mô hình LLM & RAG.
2.  **API Standards**: Chuẩn OpenAPI & REST.
3.  **Compliance**: Giao thức GDPR/HIPAA.
4.  **Database Master**: Quy tắc Schema & Migration.
5.  **Design System**: Pattern UI/UX & Tokens.
6.  **Domain Blueprints**: Kiến trúc theo lĩnh vực.
7.  **I18n Master**: Tiêu chuẩn Đa ngôn ngữ.
8.  **Infra Blueprints**: Cấu hình Terraform/Docker.
9.  **Metrics**: Giám sát & Telemetry.
10. **Security Armor**: Bảo mật & Audit.
11. **Testing Master**: Chiến lược TDD & E2E.
12. **UI/UX Pro Max**: Tương tác nâng cao.
13. **Vitals Templates**: Tiêu chuẩn Hiệu năng.

## 🖥️ Cấu trúc Môi trường & Kết nối Network

1. **Môi trường Dev (`dev`)**:
   - Tên project: `PM_Quan_ly_SHLX`
   - Hạ tầng: Chạy trực tiếp trên Laptop cá nhân.
2. **Môi trường Product (`product`)**:
   - Tên ứng dụng: `PM_QuanLy_SH`
   - Hạ tầng: Chạy trong Docker trên Ubuntu Server (Linux).
3. **Kết nối Mạng (Network Connection)**:
   - IP WireGuard Gateway: `10.13.13.1` (SSH alias: `n100`, user: `root`)
   - IP WireGuard Ubuntu Server (Cũ/Product): `10.13.13.2` (SSH alias: `ubuntu`, user: `beattlekid`)
   - IP WireGuard Ubuntu LLM Server: `10.13.13.14` (SSH alias: `llm`, `llm-ai`, user: `beattlekid`)
   - IP LAN Ubuntu LLM Server: `192.168.88.221` (SSH alias: `llm-lan`, user: `beattlekid`)
   - IP Dự phòng (Tailscale fallback): `100.86.86.31`
4. **Quy ước Tên gọi**:
   - Ứng dụng/Mã nguồn tại máy local = **`dev`**
   - Ứng dụng/Dịch vụ chạy trên Server Ubuntu = **`product`**

---

## 🤝 Handoff Protocol — MANDATORY for shared work

> This repo uses a **single shared handoff** in `.brain/` so multiple agents/humans can continue each other's work without losing context or overwriting each other.
> Handoff files are written in **English** (see Language Protocol item 4).

### Mandatory reading order at session start

1. `AGENTS.md` — agent policy and authority
2. `.brain/HANDOFF_PROTOCOL.md` — **binding collaboration protocol**
3. `.brain/README.md` — which handoff package is CURRENT
4. `.brain/BRAIN_PACKAGE_<newest>.md` — full project context
5. `.brain/brain.json` — business decisions ("why")
6. `src/architecture_guardrails.md` — SUPREME LAW; read BEFORE touching the 4-phase pipeline

### After loading context you MUST print this block

```
📦 Handoff: BRAIN_PACKAGE_<date>.md (HEAD <commit>, <match|MISMATCH>)
🌿 Branch: <branch> | Tree: <clean|dirty>
⚠️ Blocker: <...>
🎯 Task: <...>
```

Cannot print it → context not loaded → you MUST NOT edit code.

### When handing off (before ending the session)

- Any behaviour change → create `.brain/BRAIN_PACKAGE_<today>.md` using the template in the protocol
- Update `.brain/README.md` to mark the new package CURRENT
- **DO NOT** commit / push / deploy without explicit user approval
- **DO NOT** `git add .` and **DO NOT** commit directly to `main`

→ Full details: **`.brain/HANDOFF_PROTOCOL.md`**

---

*Created by Google Antigravity*
