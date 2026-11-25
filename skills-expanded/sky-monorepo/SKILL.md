---
name: sky-monorepo
description: >-
  Monorepo kurma ve yönetme: ne zaman monorepo, pnpm workspaces yapısı (apps/ ve packages/),
  Turborepo ile görev orkestrasyonu ve önbellek (yerel + uzak), iç paketler (just-in-time TS vs
  derlenmiş), paylaşılan tsconfig/eslint/tailwind ayarları, bağımlılık sürüm tutarlılığı
  (catalog, syncpack), CI'da yalnızca etkilenen paketler, changesets ile sürümleme, Nx
  alternatifi ve sık sorunlar. "Monorepo", "web ve mobil aynı repoda", "Turborepo" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Monorepo

## Ne zaman?

✓ Web + mobil + API + ortak paketler (tipler, Zod şemaları, UI, yapılandırmalar) birlikte gelişiyor; atomik değişiklik (API + istemci tek PR).
✗ Tek uygulama; bağımsız ekipler/yaşam döngüleri; farklı erişim yetkisi gereken kod.

## Yapı (pnpm + Turborepo)

```
apps/
  web/        # Next.js
  mobile/     # Expo
  api/        # Hono
packages/
  db/         # Drizzle şema + istemci
  schemas/    # Zod şemaları (API sözleşmesi)
  ui/         # paylaşılan React bileşenleri
  config/     # tsconfig, eslint/biome, tailwind preset
pnpm-workspace.yaml
turbo.json
```
```yaml
# pnpm-workspace.yaml
packages: ["apps/*", "packages/*"]
catalog:                       # tek yerde sürüm: paketlerde "react": "catalog:"
  react: ^19.0.0
  zod: ^4.0.0
  typescript: ^5.6.0
```

## İç paketler

```json
// packages/schemas/package.json — "just-in-time": derleme yok, tüketen uygulama TS'i derler
{ "name": "@acme/schemas", "private": true, "type": "module",
  "exports": { ".": "./src/index.ts" } }
// apps/web/package.json
{ "dependencies": { "@acme/schemas": "workspace:*" } }
```
Next.js'te `transpilePackages: ["@acme/ui", "@acme/schemas"]`. Yayınlanacak paketler derlenir (bkz. `sky-npm-library`).
Paket adlarında ortak kapsam (`@acme/`), iç paketler `private: true`.

## Turborepo

```json
{
  "$schema": "https://turborepo.com/schema.json",
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**", ".next/**", "!.next/cache/**"] },
    "typecheck": { "dependsOn": ["^build"] },
    "lint": {},
    "test": { "dependsOn": ["^build"], "outputs": ["coverage/**"] },
    "dev": { "cache": false, "persistent": true }
  }
}
```
- `turbo run build --filter=web...` (web ve bağımlılıkları), `--filter=[origin/main]` (değişenler) → CI'da yalnızca etkilenenler.
- Önbellek: aynı girdiler → aynı çıktı, tekrar çalıştırmaz; **uzak önbellek** (Vercel Remote Cache / kendi sunucun) ile ekip ve CI paylaşır — dakikalar saniyeye iner.
- Env değişkenleri önbellek anahtarına dahil olmalı (`env`/`globalEnv`) — yoksa yanlış önbellek isabeti.

## Paylaşılan yapılandırma

`packages/config/tsconfig/base.json` → uygulamalar `"extends": "@acme/config/tsconfig/nextjs.json"`; aynı şekilde lint ve Tailwind preset.
TypeScript project references büyük monorepolarda tip kontrolünü hızlandırır.

## Sürüm tutarlılığı

pnpm catalog veya `syncpack` (aynı bağımlılığın farklı sürümlerini tespit); `pnpm dedupe`; React gibi tekil olması gerekenler için tek sürüm şart.

## CI ve deploy

- Vercel/Netlify monorepo desteği: proje başına kök klasör + "yalnızca değişince build" (`turbo-ignore`).
- Docker: `turbo prune api --docker` → yalnızca gereken paketlerle hafif build bağlamı.
- Sürümleme: changesets (yalnızca yayınlanan paketler için).

## Sık sorunlar

| Sorun | Çözüm |
|---|---|
| "Module not found" iç paket | `workspace:*` bağımlılığı eklenmemiş, `exports` yolu yanlış |
| İki React kopyası (hook hatası) | tek sürüm, peerDependency, `pnpm why react` |
| Turbo önbelleği yanlış sonuç | çıktılar/env tanımları eksik |
| Yavaş tip kontrolü | project references, paket başına typecheck |
| Hayalet bağımlılık | pnpm katı izolasyon — kullandığın her paketi kendi package.json'una ekle |

Alternatif: **Nx** (daha güçlü görev grafiği, üreticiler, eklentiler; daha fazla yapı) — büyük kurumsal monorepolarda.
