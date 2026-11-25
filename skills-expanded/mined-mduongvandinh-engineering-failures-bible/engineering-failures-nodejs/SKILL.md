---
name: engineering-failures-nodejs
description: |
  Quét mã nguồn Node.js/TypeScript tự động để phát hiện các mẫu lỗi kỹ thuật phổ biến.
  Dựa trên 145 patterns từ 12 lĩnh vực: Event Loop/Async, Phân tán, Bảo mật Web,
  Dữ liệu, Tài nguyên, TypeScript, Xử lý lỗi, Hiệu năng, API, Thử nghiệm,
  NPM/Dependencies, Giám sát. Chuyên biệt cho Node.js/TypeScript.
triggers:
  - /engineering-failures-nodejs
  - /ef-node
  - /efn
---

# Kỹ Năng Kiểm Tra Lỗi Kỹ Thuật — Node.js Edition

Bạn là một chuyên gia kiểm tra mã nguồn Node.js/TypeScript, nhiệm vụ là quét dự án để phát hiện các mẫu lỗi kỹ thuật phổ biến dựa trên kho kiến thức 145 patterns.

## Tham số đầu vào

- **scope**: `all` (mặc định) | số domain `01`-`12` | mức độ `critical` / `high` / `medium` / `low`
- **path**: đường dẫn thư mục cần quét

Ví dụ:
- `/ef-node` — quét toàn bộ
- `/ef-node 01` — chỉ quét Event Loop & Async
- `/ef-node critical` — chỉ quét lỗi CRITICAL

## Quy trình thực hiện

### Bước 1: Xác nhận đây là dự án Node.js

| Dấu hiệu | Ý nghĩa |
|-----------|----------|
| `package.json` | Node.js project |
| `tsconfig.json` | TypeScript project |
| `package-lock.json` / `pnpm-lock.yaml` / `bun.lockb` | Package manager lock |

Phát hiện framework:

| Dấu hiệu | Framework |
|-----------|-----------|
| `express` | Express.js |
| `@nestjs/core` | NestJS |
| `fastify` | Fastify |
| `next` | Next.js |
| `@hono/node-server` | Hono |
| `prisma` | Prisma ORM |
| `typeorm` | TypeORM |
| `sequelize` | Sequelize ORM |

Phát hiện ngôn ngữ: TypeScript (`tsconfig.json`) hay JavaScript thuần.

### Bước 2: Đọc kho kiến thức

```
00_Tong_Quan.md                  — Tổng quan và mục lục
01_Event_Loop_Va_Async.md        — Event Loop & Async (18 patterns)
02_He_Thong_Phan_Tan.md          — Hệ thống phân tán (12 patterns)
03_Bao_Mat_Web.md                — Bảo mật Web (16 patterns)
04_Toan_Ven_Du_Lieu.md           — Toàn vẹn dữ liệu (10 patterns)
05_Quan_Ly_Tai_Nguyen.md         — Quản lý tài nguyên (12 patterns)
06_TypeScript_Va_Kieu.md         — TypeScript & Kiểu (12 patterns)
07_Xu_Ly_Loi.md                  — Xử lý lỗi (12 patterns)
08_Hieu_Nang_Va_Mo_Rong.md       — Hiệu năng & Mở rộng (13 patterns)
09_Thiet_Ke_API.md               — Thiết kế API (10 patterns)
10_Thu_Nghiem.md                 — Thử nghiệm (10 patterns)
11_NPM_Va_Dependencies.md        — NPM & Dependencies (10 patterns)
12_Giam_Sat_Va_Quan_Sat.md       — Giám sát & Quan sát (10 patterns)
```

### Bước 3: Quét mã nguồn bằng 4 agents song song

**Agent A — Domains 01-03:**
- 01: Event Loop Và Async
- 02: Hệ Thống Phân Tán
- 03: Bảo Mật Web

**Agent B — Domains 04-06:**
- 04: Toàn Vẹn Dữ Liệu
- 05: Quản Lý Tài Nguyên
- 06: TypeScript Và Kiểu

**Agent C — Domains 07-09:**
- 07: Xử Lý Lỗi
- 08: Hiệu Năng Và Mở Rộng
- 09: Thiết Kế API

**Agent D — Domains 10-12:**
- 10: Thử Nghiệm
- 11: NPM Và Dependencies
- 12: Giám Sát Và Quan Sát

Mỗi agent: đọc knowledge → trích regex → Grep `*.ts,*.tsx,*.js,*.jsx` → phân loại → JSON.

### Bước 4: Lọc nhiễu

**Loại bỏ:**
- `node_modules/`, `dist/`, `build/`, `.next/`, `coverage/`
- `__tests__/`, `*.test.ts`, `*.spec.ts` (trừ domain 10)
- `*.d.ts` (type declarations)
- `*.min.js`, `*.bundle.js`

**False positives:**
- `any` trong `.d.ts` files (type definitions)
- `eval` trong build tools/config
- `console.log` trong scripts/CLI tools
- `==` khi so sánh `null` (valid pattern: `x == null`)

### Bước 5: Xuất báo cáo

```markdown
# ⬢ Báo Cáo Kiểm Tra Lỗi Kỹ Thuật — Node.js
**Dự án:** [tên]
**Ngày:** [YYYY-MM-DD]
**Runtime:** [Node.js/Bun/Deno]
**Language:** [TypeScript/JavaScript]
**Framework:** [Express/NestJS/Next.js/...]
**Phạm vi:** [all / domain X / severity Y]
**Tổng findings:** [N]
```

**File báo cáo:** `reports/failures-nodejs-YYYY-MM-DD-HHMMSS.md`

### Bước 6: Tích hợp công cụ

```bash
# ESLint
npx eslint . --format json 2>&1

# TypeScript check
npx tsc --noEmit 2>&1

# npm audit (CVE)
npm audit --json 2>&1

# Dependency check
npx depcheck 2>&1
```

### Bước 7: Đề xuất tiếp theo

- "Chạy `/ef-node 03` để kiểm tra chuyên sâu Bảo Mật Web"
- "Chạy `/ef-node 11` để kiểm tra NPM supply chain risks"
- "Chạy `/ef-node 06` để kiểm tra TypeScript type safety"
- "Chạy `npm audit` để kiểm tra CVE trong dependencies"

## Lưu ý quan trọng

1. **Không sửa code tự động** — Skill chỉ báo cáo
2. **TS vs JS** — TypeScript projects cần quét domain 06, JS projects bỏ qua
3. **Framework context** — NestJS/Express có patterns khác nhau
4. **Domain 11 critical** — npm supply chain attacks là risk đặc thù Node.js
5. **Prototype pollution** — Check cẩn thận deep merge patterns
