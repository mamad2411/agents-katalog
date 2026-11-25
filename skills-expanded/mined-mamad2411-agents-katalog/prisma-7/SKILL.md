---
name: Prisma 7 + Next.js 16 Anti-Regression Guard
description: Tự động bảo vệ 4 lỗi nghiêm trọng khi project dùng Prisma 7 + Next.js 16 + i18n. Kích hoạt ngầm khi phát hiện stack này.
---

# Prisma 7 + Next.js 16 Anti-Regression Guard

> [!CAUTION]
> Skill này là **Anti-Regression Guard** — tự động kích hoạt khi phát hiện project sử dụng **Prisma 7 + Next.js 16 + i18n**. Mọi vi phạm Guard dưới đây đều dẫn đến crash hoặc bug nghiêm trọng đã được phát hiện thực tế.

---

## GUARD 1 — Prisma 7 Adapter Mandate

Prisma 7 đã loại bỏ hoàn toàn Rust engine. `PrismaClient` **BẮT BUỘC** phải có `adapter` trong constructor.

### ❌ CẤM

```typescript
// CRASH: PrismaClientInitializationError
const prisma = new PrismaClient();
```

### ✅ BẮT BUỘC

```typescript
import Database from 'better-sqlite3';
import { PrismaBetterSqlite3 } from '@prisma/adapter-better-sqlite3';
import { PrismaClient } from '@prisma/client';

const database = new Database('prisma/dev.db');
const adapter = new PrismaBetterSqlite3(database);
const prisma = new PrismaClient({ adapter });
```

### Checklist bắt buộc

| # | Quy tắc | Chi tiết |
|---|---------|----------|
| 1 | Class name chính xác | `PrismaBetterSqlite3` (camelCase) — **KHÔNG** phải `PrismaBetterSQLite3` |
| 2 | Native dependency | `better-sqlite3` phải thêm vào `pnpm.onlyBuiltDependencies` trong `package.json` |
| 3 | Schema datasource | `schema.prisma` → `datasource` **KHÔNG** có `url` field. URL nằm trong `prisma.config.ts` |
| 4 | Seed script | Seed script **PHẢI** dùng adapter pattern giống app code (không dùng `new PrismaClient()` trần) |

---

## GUARD 2 — Auth.js v5 Build Safety

### ❌ CẤM

```typescript
// CRASH khi `next build`: Prisma instantiate lúc SSG
import { PrismaAdapter } from '@auth/prisma-adapter';

export const { handlers, auth } = NextAuth({
  adapter: PrismaAdapter(prisma), // ← top-level import = crash
});
```

### ✅ BẮT BUỘC

```typescript
// auth.config.ts — JWT strategy, KHÔNG cần DB sessions
export const authConfig = {
  session: { strategy: 'jwt' },
  providers: [
    CredentialsProvider({
      async authorize(credentials) {
        // Lazy import Prisma — chỉ chạy runtime, không chạy lúc build
        const { prisma } = await import('@/lib/prisma');
        const user = await prisma.user.findUnique({
          where: { email: credentials.email },
        });
        // ... verify password, return user
      },
    }),
  ],
};
```

```typescript
// app/api/auth/[...nextauth]/route.ts
export const dynamic = 'force-dynamic'; // ← BẮT BUỘC

export { handlers as GET, handlers as POST } from '@/auth';
```

### Quy tắc cốt lõi

1. **KHÔNG** dùng `PrismaAdapter` ở top-level import trong auth config.
2. **Dùng JWT strategy** — không cần DB sessions.
3. Prisma chỉ import lazy bằng `await import('@/lib/prisma')` **bên trong** hàm `authorize()`.
4. API route `[...nextauth]` phải có `export const dynamic = 'force-dynamic'`.

---

## GUARD 3 — i18n Error Keys

### ❌ CẤM

```typescript
// Server Action trả chuỗi tiếng Anh cứng
return { error: 'Invalid credentials' };
return { error: 'Something went wrong' };
```

### ✅ BẮT BUỘC

```typescript
// Server Action trả error KEY
return { errorKey: 'auth.invalid_credentials' };
return { errorKey: 'auth.error_generic' };
```

```tsx
// Client component dùng t() để hiển thị đúng ngôn ngữ
const result = await loginAction(formData);
if (result?.errorKey) {
  setError(t(result.errorKey));
}
```

### Quy tắc cốt lõi

1. Server Action **KHÔNG BAO GIỜ** trả về chuỗi hiển thị trực tiếp.
2. Trả về `errorKey` → client component dùng `t(result.errorKey)` để render đúng locale.
3. Mọi error key **PHẢI** có mặt trong **TẤT CẢ** locale files (`en`, `vi`, `ja`, `zh`).

---

## GUARD 4 — Static Locale Imports

### ❌ CẤM

```typescript
// Turbopack KHÔNG resolve được path alias trong dynamic import
const messages = await import(`@/locales/${locale}.json`);
// → t() trả raw key thay vì bản dịch
```

### ✅ BẮT BUỘC

```typescript
import en from '@/locales/en.json';
import vi from '@/locales/vi.json';
import ja from '@/locales/ja.json';
import zh from '@/locales/zh.json';

const allMessages: Record<string, typeof en> = { en, vi, ja, zh };

export function getMessages(locale: string) {
  return allMessages[locale] ?? allMessages.en;
}
```

### Quy tắc cốt lõi

1. **KHÔNG** dùng dynamic `import()` với template literal cho locale files.
2. Import static tất cả locale files rồi dùng **lookup map**.
3. Fallback về `en` nếu locale không hợp lệ.

---

## Khi nào Guard này kích hoạt?

Guard tự động kích hoạt khi phát hiện **BẤT KỲ** dấu hiệu nào sau đây trong project:

- `@prisma/client` ≥ 7.x trong `package.json`
- `prisma.config.ts` tồn tại
- `@auth/prisma-adapter` hoặc `next-auth` trong dependencies
- Thư mục `locales/` hoặc cấu hình i18n

Khi kích hoạt, **MỌI** code sinh ra phải tuân thủ 4 Guard trên. Vi phạm bất kỳ Guard nào đều bị coi là **regression bug**.
