---
name: sky-typescript
description: >-
  Web projeleri için TypeScript kalıpları: strict ayarlar, discriminated union ile durum
  modelleme, Zod'dan tip türetme, markalı (branded) ID tipleri, Result/hata tipleri, generics
  ölçüsü, satisfies/as const, enum yerine union, exhaustive switch, utility tipler, tip
  daraltma, modül sınırları ve sık tip hataları. Tip tasarlarken, "any'den kurtul", "tip
  hatası alıyorum", "bu tipi nasıl yazarım" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · TypeScript

## tsconfig temeli

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,   // arr[0] → T | undefined; gerçek hataları yakalar
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true, // { a?: string } ile a: undefined farkı
    "verbatimModuleSyntax": true,       // import type zorunluluğu
    "moduleResolution": "bundler",
    "target": "ES2022",
    "paths": { "@/*": ["./src/*"] }
  }
}
```
`skipLibCheck: true` kabul; `strict: false` veya `// @ts-ignore` yayılmasına izin yok
(`@ts-expect-error` + açıklama tercih).

## Tip nereden gelir? Tek kaynak

- **Şema → tip:** `const UserSchema = z.object({...}); type User = z.infer<typeof UserSchema>;`
  Elle aynı tipi bir daha yazma.
- **DB → tip:** Drizzle `typeof users.$inferSelect` / `$inferInsert`; Prisma üretilen tipler.
- **API → tip:** Zod şeması paylaşılır; tRPC/OpenAPI varsa oradan.
- UI prop tipleri bu kaynaklardan `Pick`/`Omit` ile türetilir; kopyalanmaz.

## Durum modelleme: discriminated union

Boolean çorbası yerine:
```ts
type FetchState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: AppError };
```
Böylece `data` yalnızca `success`ta erişilebilir; imkânsız durumlar (`loading && error`) yok olur.
Tüketimde `switch (state.status)` + exhaustive kontrol:
```ts
default: { const _exhaustive: never = state; return _exhaustive; }
```

## enum yerine

```ts
export const Role = { admin: "admin", editor: "editor", viewer: "viewer" } as const;
export type Role = (typeof Role)[keyof typeof Role];
```
veya Zod: `z.enum(["admin", "editor", "viewer"])` → `z.infer`. TS `enum`ın runtime/tree-shaking
sürprizleri yok; string literal union her yerde çalışır.

## Markalı tipler (ID karışmasın)

```ts
type Brand<T, B extends string> = T & { readonly __brand: B };
export type UserId = Brand<string, "UserId">;
export type OrderId = Brand<string, "OrderId">;
export const UserId = (s: string) => s as UserId;
```
`getOrder(userId)` artık derlenmez. Zod ile: `z.string().uuid().brand<"UserId">()`.

## Hata modeli: Result

Beklenen hatalar için exception yerine değer:
```ts
type Result<T, E = AppError> = { ok: true; value: T } | { ok: false; error: E };
type AppError =
  | { code: "NOT_FOUND"; resource: string }
  | { code: "FORBIDDEN" }
  | { code: "VALIDATION"; issues: Record<string, string[]> };
```
Servis `Result` döner, handler `code` → HTTP durumuna eşler (bkz. `sky-backend-api`).
`catch (e)` içinde `e` **`unknown`**: `e instanceof Error ? e.message : String(e)`.

## `satisfies` ve `as const`

```ts
const routes = {
  home: "/",
  post: (slug: string) => `/blog/${slug}`,
} satisfies Record<string, string | ((...a: string[]) => string)>;
// routes.home tipi "/" olarak kalır (literal korunur), ama şekil denetlenir
```
`as const` ile dizi/obje literal'ini dondur: `["tr", "en"] as const` → `"tr" | "en"` türet.

## Generics ölçüsü

- Generic'i yalnızca **iki yer arasında ilişki** kuruyorsa kullan (`function first<T>(xs: T[]): T`).
- Tek yerde geçen `<T>` gereksiz; `unknown` yeter.
- Kısıt ver: `<T extends { id: string }>`. Varsayılan ver: `<T = unknown>`.
- Çağıran yerde açık tip argümanı yazmak gerekiyorsa API'yi yeniden düşün.

## Daraltma araçları

- `typeof`, `instanceof`, `in` ("kind" in x), eşitlik (`x.status === "ok"`).
- Tip koruyucu: `function isUser(x: unknown): x is User { return UserSchema.safeParse(x).success; }`
- `asserts`: `function assertDefined<T>(x: T): asserts x is NonNullable<T>`.
- `Array.isArray`, `.filter((x): x is T => x != null)` (veya `filter(Boolean)` yerine).
- Dış veri **her zaman** `unknown` → şema ile parse. `as User` değil.

## Faydalı utility tipler

`Partial`, `Required`, `Pick`, `Omit`, `Record`, `Extract`, `Exclude`, `NonNullable`,
`ReturnType<typeof fn>`, `Awaited<ReturnType<typeof fetchUser>>`, `Parameters<typeof fn>[0]`,
`ComponentProps<typeof Button>`, `ComponentPropsWithoutRef<"button">`.
Template literal: `` type EventName = `${Entity}_${Action}` ``.
Fazla akıllı tip (derin koşullu/mapped) → okunabilirlik kaybı; iki satır fazla kod daha iyi.

## React ile

- Prop tipi: `type Props = { ... }` + `children?: React.ReactNode`. `React.FC` şart değil.
- Native öğeyi genişlet: `type ButtonProps = React.ComponentPropsWithoutRef<"button"> & { variant?: Variant }`.
- Event: `React.ChangeEvent<HTMLInputElement>`; handler'ı inline yazıp çıkarım yaptır.
- Generic bileşen: `function List<T>({ items, render }: { items: T[]; render: (t: T) => ReactNode })`.
- `useState<User | null>(null)` — başlangıç `null` ise tipi açık yaz.
- `useRef<HTMLDivElement>(null)`.

## Modül sınırları

- `import type { X }` tip-only importlarda (verbatimModuleSyntax zorlar).
- Barrel (`index.ts`) dosyalarını ölçülü kullan; döngüsel import ve bundle şişmesi yapar.
- `export default` yerine adlandırılmış export (yeniden adlandırma/refactor kolay); Next sayfa dosyaları istisna.
- Ortak tipler `types.ts` içinde özellik klasöründe; global `types/` yalnızca gerçekten paylaşılanlar için.

## Sık hatalar → çözüm

| Hata | Anlamı | Yap |
|---|---|---|
| `Object is possibly 'undefined'` | `noUncheckedIndexedAccess` veya opsiyonel | `?.`, `??`, erken return, `assertDefined` |
| `Type 'string' is not assignable to type '"a" \| "b"'` | literal genişledi | `as const`, `satisfies`, parametre tipini union yap |
| `Property 'x' does not exist on type 'never'` | daraltma hepsini eledi | union'ı/koşulu kontrol et |
| `Argument of type 'unknown'` | catch/dış veri | şema ile parse, `instanceof` |
| `Excessive stack depth` / çok yavaş TS | aşırı koşullu tip | tipi basitleştir, ara tip adlandır |
| `any` yayılıyor | tipsiz kütüphane/JSON | `unknown` + parse; `@types/` ekle; yerel `d.ts` |

## Kontrol

`tsc --noEmit` CI'da zorunlu. `eslint` kuralları: `@typescript-eslint/no-explicit-any`,
`no-unsafe-*`, `consistent-type-imports`, `switch-exhaustiveness-check`.
