# Skill: /kltn-implement (FE)

## Kích hoạt
`/kltn-implement [issue-number]` — làm việc trên GitHub Issue phía Frontend (Web hoặc Mobile).

---

## Quy trình

### Bước 0 — Kiểm tra CLAUDE.local.md
```bash
cat .claude/CLAUDE.local.md 2>/dev/null || { echo "❌ CLAUDE.local.md chưa tồn tại — tạo file này trước (xem /kltn-setup)"; exit 1; }
```
Xác nhận file có đủ 4 trường: **Tên**, **MSSV**, **Role chính**, **Role phụ**.
Nếu thiếu → dừng lại và yêu cầu tạo/bổ sung trước khi tiếp tục.

### Bước 1 — Đọc GitHub Issue
```bash
gh issue view $ISSUE_NUMBER --json number,title,body,labels,milestone,assignees

# Đọc sub-issues (nếu có)
gh api repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/issues/$ISSUE_NUMBER/sub_issues \
  --jq '.[] | {number: .number, title: .title, body: .body, state: .state}'
```
Từ output ghi nhớ:
- `$ISSUE_NUMBER` — số issue (ví dụ: `12`)
- `$ISSUE_TITLE` — title của issue
- `$SPRINT` — milestone name
- **Web** (ReactJS) hay **Mobile** (React Native / Expo)?
- Output mong đợi là gì? (màn hình, component, API call nào?)
- Có dependency với issue BE nào không?
- Tổng hợp thêm context từ sub-issues nếu có.

### Bước 2 — Kiểm tra plan hiện tại

```bash
cat logs/GH-$ISSUE_NUMBER/plan.md 2>/dev/null
```

- **Nếu tồn tại** → Hiện nội dung, hỏi:
  ```
  Plan đã tồn tại (Status: [status]).
  [1] Dùng plan này → tiếp tục Bước 2.5
  [2] Ghi đè plan mới → tiếp tục viết plan bên dưới
  ```
  Chờ user chọn. Nếu chọn 1 → chuyển thẳng sang Bước 2.5.

- **Nếu chưa tồn tại** → Lập plan và viết file tại `logs/GH-$ISSUE_NUMBER/plan.md`:

```markdown
# Plan — GH-[number]: [Tên issue]

## Metadata
- **Status:** PLANNING
- **Role:** FE | **Ngày:** YYYY-MM-DD
- **Issue:** #[number] — [GitHub URL]
- **Sprint:** [milestone]

## Mục tiêu
[Issue yêu cầu làm gì, output là gì]

## Scope
- Trong scope: ...
- Ngoài scope: ...

## Files
| File | Action | Ghi chú |
|------|--------|---------|
| path/to/file.tsx | create/modify | ... |

## Approach
[Cấu trúc component, state management, API calls]

## Edge Cases
- Input không hợp lệ: ...
- Error handling: ...

## Success Criteria
| Tiêu chí | Cách verify |
|----------|------------|
| [Mô tả outcome cụ thể] | [Lệnh / bước kiểm tra] |

## Steps
- [ ] Bước 1: [...]
- [ ] Bước 2: [...]
- [ ] Bước 3: [...]

## Câu hỏi đã giải đáp
[Tóm tắt những điểm đã hỏi và câu trả lời — để reviewer hiểu context]
```

> **DỪNG LẠI — chờ user xác nhận ("ok", "approve", "yes", "y", "tiến hành") trước khi làm bất cứ bước nào tiếp theo.**
> **TUYỆT ĐỐI KHÔNG CODE khi chưa có xác nhận. Không có ngoại lệ, dù issue nhỏ đến đâu.**

### Bước 2.5 — Chọn executor

Sau khi plan được approve, hỏi user:

> **"Ai sẽ thực thi plan này?"**
> 1. **Claude** — Claude Code tự implement (tiếp tục Bước 3 bên dưới)
> 2. **Codex** — Trigger Codex CLI thực thi plan (Claude dừng lại sau bước này)

**Nếu user chọn Option 2 — Codex:**

Claude đọc toàn bộ `logs/GH-$ISSUE_NUMBER/plan.md`, tính slug từ title issue, rồi in ra description kèm hướng dẫn rõ ràng:

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CODEX DESCRIPTION — GH-$ISSUE_NUMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 Thực hiện theo thứ tự:
   1. Mở terminal (hoặc cửa sổ Codex CLI bạn đang dùng)
   2. cd vào đúng thư mục repo:
        cd ~/Documents/GSU26SE55/frontend
   3. Copy TOÀN BỘ đoạn bên dưới (từ dòng "You are..." đến hết "...clearly.")
   4. Paste vào Codex CLI và nhấn Enter
   5. Codex tự chạy — không cần làm gì thêm

⚠️  Lưu ý:
   - Copy đúng toàn bộ, không bỏ sót dòng nào
   - Codex sẽ KHÔNG commit / push — chỉ implement code
   - Sau khi Codex xong → quay lại chạy /kltn-reviewcode $ISSUE_NUMBER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✂️  COPY TỪ ĐÂY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are implementing GitHub Issue #$ISSUE_NUMBER for a Frontend (ReactJS/React Native) project.

Follow ALL coding conventions in .codex/skills/fe/ (feature folder structure,
TanStack Query hooks, service layer, Zod schemas, shadcn/ui, shared/lib/axios.ts only).

Branch to create: feat/GH-$ISSUE_NUMBER-$SLUG

== IMPLEMENTATION PLAN ==
[toàn bộ nội dung logs/GH-$ISSUE_NUMBER/plan.md được paste ở đây]
== END OF PLAN ==

Rules:
- Follow the Steps section in order, check off each step as done.
- Do NOT commit or push — stop after implementation.
- If a step fails, stop and report the error clearly.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✂️  COPY ĐẾN ĐÂY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> Claude dừng lại sau khi in description. Chờ user thực hiện xong với Codex rồi tiếp tục `/kltn-reviewcode $ISSUE_NUMBER`.

**Nếu user chọn Option 1 — Claude:** tiếp tục Bước 3 bên dưới.

---

### Bước 3 — Tạo branch
```bash
# Slug: viết thường, chỉ a-z/0-9/gạch ngang, tối đa 5 từ
# Ví dụ: "Add Battery CRUD API" → feat/GH-42-add-battery-crud-api
SLUG=$(gh issue view $ISSUE_NUMBER --json title -q '.title' \
  | tr '[:upper:]' '[:lower:]' \
  | tr -cs 'a-z0-9' '-' \
  | tr -s '-' \
  | cut -d'-' -f1-5 \
  | sed 's/-$//')

git checkout -b feat/GH-$ISSUE_NUMBER-$SLUG
```

### Bước 4 — Implement theo đúng cấu trúc

**Web (ReactJS) — Feature-based + Shared:**
```
src/
├── config/
│   └── env.ts                   ← Zod-validate import.meta.env khi boot
├── router/
│   ├── index.tsx                ← createBrowserRouter — toàn bộ route tree
│   ├── ProtectedRoute.tsx       ← redirect /login nếu chưa auth
│   └── RoleRoute.tsx            ← redirect /unauthorized nếu sai role
├── features/<tên-feature>/
│   ├── pages/                   ← route entry: layout + gọi hook, không có logic
│   ├── components/              ← UI components của feature này
│   ├── hooks/                   ← useQuery / useMutation (TanStack Query)
│   ├── services/                ← Axios API calls qua axiosInstance
│   ├── schemas/                 ← Zod schema cho form validation
│   └── types/                   ← TypeScript types của feature
└── shared/
    ├── components/
    │   ├── layout/              ← AppLayout, AuthLayout, Sidebar, Header
    │   ├── common/              ← LoadingSpinner, ErrorBoundary, EmptyState
    │   └── ui/                  ← shadcn generated components (thực tế: src/components/ui/)
    ├── context/
    │   └── authContext.tsx      ← AuthProvider: hydrate sessionStore từ cookie khi boot
    ├── lib/
    │   ├── axios.ts             ← Axios instance + interceptors (không tạo instance mới)
    │   ├── authz.ts             ← RBAC: P constants, checkPermission(), checkRole()
    │   └── errors.ts            ← HttpError, EntityError, handleErrorApi
    ├── utils/
    │   ├── queryKeys.ts         ← KEY (root) + QUERY_KEY (factories)
    │   └── endpoints.ts         ← ENDPOINTS — single source of truth cho API paths
    ├── stores/
    │   └── sessionStore.ts      ← Zustand: token, user, setToken, logout
    ├── enums/                   ← `as const` + type alias — dùng cross-feature
    │   ├── session.enum.ts      ← UserRole
    │   ├── account.enum.ts      ← AccountStatusEnum, AvatarSourceEnum, RefreshTokenStatus
    │   ├── ticket.enum.ts       ← TicketStatusEnum, TicketPriorityEnum, ImpactScopeEnum, ...
    │   ├── battery.enum.ts      ← BatteryStatusEnum
    │   ├── site.enum.ts         ← SiteStatusEnum
    │   └── common.enum.ts       ← TrendDir
    └── types/
        ├── api.types.ts         ← ResponseData<T>, PaginationResponse<T>, ErrorEntity
        ├── ticket.types.ts      ← TicketDTO, TicketDetailDTO, payloads (re-export từ ticket.enum)
        ├── session.types.ts     ← SessionUser, decodeToken, redirectByRole
        └── common.types.ts      ← BaseFilterPagination, shared query types
```

**Enum placement rule (bắt buộc):**
- Dùng ≥ 2 feature → `src/shared/enums/{domain}.enum.ts`
- Chỉ 1 feature dùng → `src/features/{feature}/enums/{domain}.enum.ts`
- `types/*.ts` KHÔNG định nghĩa enum inline — import từ `enums/` rồi re-export
- Dùng `z.nativeEnum(SomeEnum)` trong Zod schema — không dùng `z.enum([...])`

**Enum pattern chuẩn:**
```ts
export const TicketStatusEnum = {
  New: "New",
  Open: "Open",
} as const;
export type TicketStatusEnum = (typeof TicketStatusEnum)[keyof typeof TicketStatusEnum];
```

**Không đặt file mới vào `shared/` trừ khi dùng ở ≥ 2 feature khác nhau.**

**shadcn/ui (Web):**
- UI primitive dùng từ `shared/components/ui`.
- Nếu cần primitive mới: chạy `npx shadcn@latest add <component>`.
- Không tự viết lại Button/Input/Form/Dialog/Table/Badge/Skeleton nếu shadcn đã có.

**Mobile (React Native / Expo):**
```
app/            ← Expo Router screens
components/     ← UI components
stores/         ← Zustand global state
services/       ← Axios API calls
```

### Bước 5 — Tự kiểm tra trước commit
- Không còn `console.log`
- Loading + error state đã xử lý
- UI primitive import từ `shared/components/ui`, không tự custom lại component shadcn đã có
- Không hardcode URL / token
- Route mới đã khai báo trong `router/index.tsx`
- Page cần auth đã wrap `ProtectedRoute`
- Page có role restriction đã wrap `RoleRoute` (Admin / Manager / Staff)
- Responsive đúng (Web)
- Zod schema validate đúng shape — không dùng `.any()` hay bỏ qua field bắt buộc
- Query key lấy từ `shared/utils/queryKeys.ts`, không tự tạo string mới inline
- Không tạo Axios instance mới — chỉ import từ `shared/lib/axios.ts`

Sau khi tất cả checklist pass → cập nhật `plan.md`: `Status: IN_PROGRESS → REVIEWING`.

> ⛔ **KHÔNG commit, KHÔNG push** trong bước này.
> Commit + push + tạo PR chỉ được thực hiện khi chạy `/kltn-ship $ISSUE_NUMBER`.

---

## Sau khi implement xong — chạy theo thứ tự

```
/kltn-reviewcode  →  /kltn-test  →  /kltn-ship $ISSUE_NUMBER
```

`/kltn-test` với FE sẽ chạy:
```bash
# Web
npx tsc --noEmit                  # type check
npx eslint . --max-warnings=0     # lint (0 warning)
npm run build                     # production build

# Mobile
npx tsc --noEmit
npx expo lint
```

> Cả 3 bước phải PASS trước khi `/kltn-ship`. Không bỏ qua TypeScript error hay ESLint warning.

---

## Không được
- Gọi API trực tiếp trong component (phải qua `services/`)
- Đặt state global vào `useState` local nếu nhiều component dùng
- Hardcode URL API (dùng env variable)
- Thêm npm package chưa có trong tech-defaults
- Tạo Axios instance mới ngoài `shared/lib/axios.ts`
- Tự tạo query key string inline thay vì dùng `queryKeys.ts`

---

## Stack FE
**Web:** React 19 · React Router DOM v7 · TanStack Query v5 · Zustand · Axios · React Hook Form + Zod · shadcn/ui · Tailwind v4 · Recharts · Sonner · js-cookie · jwt-decode · next-themes · date-fns
**Mobile:** React Native · Expo · Expo Router · Axios
