# Tổng Quan Dự Án aix — AI Engineering Platform

> [!NOTE]
> Tài liệu này cung cấp cái nhìn toàn diện về kiến trúc monorepo của dự án `aix`, các package cấu thành, quy trình phát triển phần mềm tự động (SDLC Spine) và thư viện gồm 159 kỹ năng (skills).

## 1. Giới thiệu chung

**aix** là một nền tảng kỹ thuật AI (AI Engineering Platform) và là một plugin dành cho AI Agents. Nó định hình phương pháp luận SDLC theo luồng thảo luận → lên kế hoạch → thực thi (discuss → plan → execute) kết hợp với thư viện 159 kỹ năng (skills). 

Trong mô hình này:
- **Host Agent chính là Runtime**: `aix` đóng vai trò là sách hướng dẫn (playbook) và thư viện tài nguyên, chứ không phải là một công cụ độc lập chạy ngoài.
- Dự án được cấu trúc dưới dạng **TypeScript Monorepo** sử dụng `pnpm`.

---

## 2. Sơ đồ Kiến trúc và Dòng hoạt động

Dưới đây là sơ đồ minh họa cách plugin `aix` được tải và hoạt động thông qua Host Agent:

```mermaid
graph TD
    A[Bắt đầu Session] --> B[Hook: SessionStart]
    B -->|Inject| C[using-aix SKILL]
    C -->|Hướng dẫn sử dụng| D[Skill Tool / router-pro]
    D -->|Kích hoạt| E[159 Skills Thư viện]
    
    subgraph "Các gói hỗ trợ (Monorepo)"
        F[@x/core]
        G[@x/registry]
        H[@x/engine]
        I[services/kb-server]
    end
    
    E -->|Thực thi spine| F
    E -->|Đọc Schema| G
    E -->|Chạy Headless/CI| H
    E -->|Lưu trữ tri thức| I
```

---

## 3. Cấu trúc Monorepo & Các Package Cốt lõi

Dự án sử dụng cấu trúc Monorepo quản lý bởi `pnpm` (tham khảo [package.json](file:///C:/Users/truongdq/Documents/projects/aix/package.json)). Dưới đây là vai trò của các thư mục và package chính:

### Cấu trúc Thư mục chính:
- [.claude-plugin/](file:///C:/Users/truongdq/Documents/projects/aix/.claude-plugin): Chứa Manifest plugin (`plugin.json`, `marketplace.json`).
- [hooks/](file:///C:/Users/truongdq/Documents/projects/aix/hooks): Chứa hook `SessionStart` để inject skill nhập môn `using-aix`.
- [content/](file:///C:/Users/truongdq/Documents/projects/aix/content): Chứa toàn bộ nội dung của 159 skills, rules và workflows.
- [packages/](file:///C:/Users/truongdq/Documents/projects/aix/packages): Các package Node.js phục vụ quá trình biên dịch và thực thi.
- [services/](file:///C:/Users/truongdq/Documents/projects/aix/services): NestJS backend cho Graph Knowledge Base sử dụng Neo4j.

### Danh sách các gói hỗ trợ (`packages/*`):

| Tên Gói | Vai trò & Chức năng |
| :--- | :--- |
| `@x/core` | Định nghĩa các type dùng chung, Phase Machine, bộ giám sát ngân sách (USD + Context window). |
| `@x/registry` | Quản lý schema của `SKILL.md` (sử dụng Zod), hỗ trợ load, phân loại và migrate skill. |
| `@x/policy` | Bảo mật ở biên, lọc thông tin nhạy cảm/bí mật (PII/Secret) và danh sách đen lệnh shell. |
| `@x/providers` | Bộ adapter chuyển đổi lúc build/runtime giữa Claude, Cursor, Codex, Gemini. |
| `@x/compiler` | Trình biên dịch sinh file đảm bảo tính toàn vẹn (hash + generated-marker). |
| `@x/context` | Phân tích code dựa trên Regex, lập chỉ mục và truy vấn RAG, tạo wiki. |
| `@x/memory` | Lưu trữ markdown-first và adapter cho Knowledge Base. |
| `@x/engine` | Công cụ thực thi CI/headless không tương tác (sử dụng LangGraph.js). |
| `@x/cli` | Giao diện dòng lệnh (`aix`) phục vụ biên dịch, chạy tác vụ, kiểm tra hệ thống (`aix doctor`). |

---

## 4. Quy trình Phát triển (The Engineering Spine)

Mỗi tác vụ được thực thi thông qua một chuỗi các kỹ năng quy trình (Process Skills):

1. **`discussing-pro`**: Trao đổi làm rõ yêu cầu, thảo luận các phương án thiết kế trước khi code.
2. **`planning-pro`**: Lập kế hoạch chi tiết, chia nhỏ tác vụ và xác định rõ các file thay đổi cùng cách thức xác minh.
3. **`git-worktree-pro`**: Kiểm tra trạng thái Git, hiển thị tóm tắt thay đổi và yêu cầu người dùng xác nhận, sau đó tạo nhánh làm việc độc lập trên Git để giữ sạch môi trường phát triển gốc.
4. **`ttd-pro`**: Viết kiểm thử trước để phát hiện & định nghĩa hành vi (Phase A - RED), sau đó viết code logic tối thiểu và chạy lại kiểm thử để đảm bảo hoàn thành (Phase B - GREEN).
5. **`executing-pro`**: Tiến hành code thực thi theo kế hoạch và thực hiện tạo các checkpoint thường xuyên.
6. **`code-review-pro`**: Đánh giá chất lượng và kiểm tra bảo mật cho mã nguồn.
7. **`verify-pro`**: Xác minh kỹ lưỡng và chạy lại tất cả các kịch bản test trước khi đóng tác vụ.
8. **`remember-pro`**: Lưu lại các bài học kinh nghiệm và kiến thức mới phát hiện được.

---

## 5. Thư viện 159 Skills (`content/skills/`)

Thư viện skill nằm dưới thư mục [content/skills/](file:///C:/Users/truongdq/Documents/projects/aix/content/skills). Nó được chia làm hai loại chính:

### A. Kỹ năng Quy trình (Process Skills)
Giúp định hình cách làm việc và điều phối của agent:
- [using-aix](file:///C:/Users/truongdq/Documents/projects/aix/content/skills/using-aix/SKILL.md): Skill nhập môn điều hướng toàn bộ hệ thống.
- `router-pro`: Phân tích yêu cầu và định tuyến đến các skill phù hợp.
- `tool-discovery-skill`: Tìm kiếm nhanh công cụ/skill tương ứng với tính năng cần triển khai.
- `debugging-investigation`: Quy trình chẩn đoán lỗi có hệ thống.

### B. Kỹ năng Chuyên môn (Domain Skills)
Bao gồm kiến thức chuyên sâu về công nghệ và framework:
- **Frontend**: `react-pro`, `nextjs-pro`, `nextjs-15-pro`, `vue-pro`, `angular-pro`, `shadcn-mastery-pro`.
- **Backend & Database**: `nestjs-pro`, `fastapi-pro`, `postgres-patterns`, `postgresql-pro`, `redis-pro`, `mongodb-pro`.
- **Ngôn ngữ**: `typescript-pro`, `python-pro`, `go-pro`, `rust-pro`, `cpp-pro`, `java-pro`.
- **Cloud & DevOps**: `docker-pro`, `kubernetes-pro`, `aws-pro`, `cloudflare-pro`, `vercel-deployment-pro`, `ci-cd-pro`.
- **Bảo mật & AI**: `security-pro`, `ai-agents-pro`, `gemini-api-dev`, `prompt-engineering-pro`.
