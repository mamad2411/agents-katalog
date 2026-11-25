---
description: 
globs: 
alwaysApply: true
---
# 📜 RULES_SUPABASE_MVP.md

## 🧠 Purpose

This project is an MVP built using:

- **Next.js** (Frontend)
- **Supabase** (Backend-as-a-Service: PostgreSQL, Auth, Storage, Functions)

The goal is to **ship fast** and **validate the business idea**, without blocking future scale-up or refactor work.

---

## 📁 Project Architecture Rules

### 1. 🔗 Supabase SDK Access

- All Supabase client calls must be **abstracted** through:
  - `/lib/supabaseClient.ts`
  - `/lib/db.ts` ← (for all DB access)
- ❌ Never call Supabase directly from components or hooks.

---

### 2. 🧠 Business Logic

- Do **not** put business logic in the frontend.
- Instead, use:
  - `lib/services/` for logic abstraction
  - Supabase Edge Functions (when needed)

---

### 3. 🧱 Data Models & DB Access

- Design DB schema in Supabase UI or with SQL migrations.
- Keep schema **simple and normalized**.
- **Use RLS (Row-Level Security)** for all tables — required for frontend safety.
- Set `NOT NULL`, `UNIQUE`, `CHECK`, and foreign key constraints early.

---

## 🔐 Authentication

### 4. 🔐 User Auth

- Use Supabase Auth for user sign-up/login.
- Use **email/password** or **OTP** login (magic link optional).
- Fetch session like this:

```ts
const { data: { user } } = await supabase.auth.getUser()
```

- Create a `profiles` table for extended user metadata.
-------

Be careful when protecting pages. The server gets the user session from the cookies, which can be spoofed by anyone.

Always use supabase.auth.getUser() to protect pages and user data.

Never trust supabase.auth.getSession() inside server code such as middleware. It isn't guaranteed to revalidate the Auth token.

It's safe to trust getUser() because it sends a request to the Supabase Auth server every time to revalidate the Auth token.

---

## 🌐 Backend Logic & API Design

### 5. 💡 Server-Side Logic

- For now, logic lives in:
  - Supabase Edge Functions
  - Or `lib/services/` in Next.js
- Future option: add real backend (e.g., Django, Express, NestJS)

---

## 🧪 Data Validation & Security

### 6. 🧪 Validation

- All input validation must be **duplicated**:
  - In frontend (for UX)
  - In DB (via constraints) or edge functions

### 7. 🔒 RLS & Security

- Apply **strict Row-Level Security** to every table.
- No public access to tables without RLS rules.
- Use JWT claims (`auth.uid()`) to restrict access.

---

## 🗃️ Storage

### 8. 🗃️ File & Image Uploads

- Use Supabase Storage.
- Store files in buckets grouped by user or resource ID.
- Use **signed URLs** to protect access.

---
🎨 UI Architecture
9. 🧩 Page-Level Component Structure
Every page directory (e.g., /app/products/) should include a:

page.tsx for layout/logic

components/ folder for all page-specific UI components

bash
Copy
Edit
/app/products/
├── page.tsx
└── components/
    ├── ProductCard.tsx
    ├── ProductList.tsx
    └── AddProductForm.tsx
✅ This keeps your components modular and your page files clean and readable.

Shared or global components still go in /components/ at the root level.
---
10. 🧾 Types
Each page should include a types.ts file to define local, page-specific types.

Shared/global types should go in /types/ at the project root.

bash
Copy
Edit
/app/products/
├── types.ts ← Local types only used by this page
/types/
├── global.ts ← App-wide shared interfaces
---
## 🚀 Scaling Plan

### 11. 🛣️ Growth Strategy

- Structure code to support future backend refactor:
  - Keep logic in `lib/services/`
  - Avoid tightly binding Supabase into UI components


---

## 🚫 Anti-Patterns

- ❌ Supabase client in pages or components
- ❌ Relying only on frontend validation
- ❌ No RLS on sensitive tables
- ❌ Business logic scattered across components
- ❌ Hardcoded table or bucket names

---

## ✅ Core Philosophy

**Move fast, but not sloppy.**


Keep things simple, abstracted, and swappable. You'll thank yourself when you scale.