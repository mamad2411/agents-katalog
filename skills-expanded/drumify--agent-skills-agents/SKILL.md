# 🤖 Drumify AI Agents & Skills

Hệ thống AI Skills được thiết kế để hỗ trợ phát triển dự án Drumify một cách chuyên nghiệp, nhất quán và hiện đại.

## 🛠️ Danh sách Skills

| Skill Name | Responsibility | Triggers |
|------------|----------------|----------|
| **`system-planner`** | Lập kế hoạch, thiết kế kiến trúc, quản lý quy chuẩn (conventions) và scaffolding. | `plan feature`, `kiến trúc`, `breakdown`, `naming`, `folder structure`, `scaffold` |
| **`code-db`** | Thiết kế Database, JPA Entity, Repository. | `tạo entity`, `thiết kế db`, `jpa repository` |
| **`code-api`** | Backend Logic, DTO, Mapper, Service, Controller, Error Handling. | `viết api`, `tạo service`, `mapstruct`, `xử lý lỗi` |
| **`code-ui`** | React 19, MUI 7, Hooks, Frontend Services, Styling. | `viết frontend`, `tạo component`, `mui styling`, `viết hook` |
| **`integrate-api`** | Tích hợp bên thứ ba (GHN, Stripe, Cloudinary, Mailchimp). | `tích hợp api`, `kết nối ghn`, `stripe payment`, `cloudinary` |
| **`archive-memory`** | Lưu trữ quyết định kiến trúc, bài học kinh nghiệm và project memory. | `lưu ghi chú`, `archive memory`, `ghi lại quyết định` |
| **`save-context`** | Lưu trạng thái session, bàn giao công việc và quản lý tiến độ. | `save context`, `handoff`, `save progress` |

## 📐 Nguyên tắc chung (AI Principles)
1.  **Reuse-first**: Luôn tìm kiếm code có sẵn trước khi viết mới để tránh trùng lặp.
2.  **Security-first**: Mọi feature phải có RBAC/GBAC thông qua Keycloak (@PreAuthorize).
3.  **Consistency**: Tuân thủ tuyệt đối quy tắc đặt tên và cấu trúc thư mục 6-layer.
4.  **SRP (Single Responsibility)**: Mỗi class/component chỉ làm một việc duy nhất và làm tốt việc đó.
5.  **Auto-update Docs**: LUÔN cập nhật các file tài liệu (`.docs/*.md`) sau khi thay đổi mã nguồn để đảm bảo tính đồng bộ.

---
*Tài liệu này được cập nhật tự động bởi Antigravity.*
