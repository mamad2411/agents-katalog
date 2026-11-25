---
name: sky-npm-library
description: >-
  npm paketi / TypeScript kütüphanesi yayınlama: paket yapısı, package.json exports alanı (ESM/
  CJS, alt yollar, types), tsup/tsdown ile build, tip bildirimleri, peerDependencies, ağaç
  sallama dostu tasarım (sideEffects), semver ve changesets ile sürümleme, provenance ile
  güvenli yayın (GitHub Actions + OIDC), README ve örnekler, publint/arethetypeswrong ile
  doğrulama, monorepoda paket ve kırıcı değişiklik yönetimi. "npm paketi yap", "kütüphane yayınla" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · npm Kütüphanesi

## package.json çekirdeği

```json
{
  "name": "@sky/slots",
  "version": "0.1.0",
  "description": "Randevu slot hesaplama — saat dilimi ve tampon destekli",
  "type": "module",
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "require": "./dist/index.cjs" },
    "./tz": { "types": "./dist/tz.d.ts", "import": "./dist/tz.js", "require": "./dist/tz.cjs" },
    "./package.json": "./package.json"
  },
  "files": ["dist"],
  "sideEffects": false,
  "engines": { "node": ">=20" },
  "peerDependencies": { "react": ">=18" },
  "peerDependenciesMeta": { "react": { "optional": true } },
  "license": "MIT",
  "repository": { "type": "git", "url": "git+https://github.com/acme/slots.git" },
  "keywords": ["booking", "slots", "scheduling"],
  "scripts": { "build": "tsup", "test": "vitest run", "lint:pkg": "publint && attw --pack ." }
}
```
- `exports` tek kaynak: tüketici yalnızca açıkça dışa aktardığın yollara erişir (iç dosyalar gizli).
- `types` koşulu her girişte **ilk** sırada.
- `files` ile yalnızca `dist` yayınlanır (testler, kaynaklar, `.env` sızmaz) — `npm pack --dry-run` ile kontrol.
- React gibi çerçeveler **peerDependency** (çift React kopyası olmasın).
- `sideEffects: false` → kullanılmayan kod ağaç sallanır (CSS import eden paketlerde `["*.css"]`).

## Build (tsup)

```ts
// tsup.config.ts
export default defineConfig({
  entry: ["src/index.ts", "src/tz.ts"],
  format: ["esm", "cjs"],          // yalnızca ESM yeterliyse cjs'yi çıkar (Node 20+ require(esm) desteği gelişiyor)
  dts: true,
  sourcemap: true,
  clean: true,
  treeshake: true,
});
```
Alternatifler: tsdown (Rolldown tabanlı), unbuild, `tsc` (yalnızca ESM, basit).

## Doğrulama

- **publint**: package.json/exports hataları. **arethetypeswrong** (`attw`): tiplerin ESM/CJS çözümlemesinde doğru çalıştığı.
- Yerel deneme: `npm pack` → başka projede `npm i ../acme-slots-0.1.0.tgz`.
- Testler her desteklenen Node sürümünde (CI matrisi).

## API tasarımı

- Küçük yüzey, iyi varsayılanlar, net isimler; seçenekler nesnesi (`generateSlots({ … })`), konumsal parametre yığını değil.
- Hatalar tipli ve belgelenmiş; girdi doğrulaması anlaşılır mesajla.
- Tüketicinin ortamını zorlama: global yan etki yok, `console.log` yok, polyfill yok.
- Bağımlılık az — her bağımlılık tüketicinin yükü ve güvenlik riski.
- JSDoc ile tip ipuçlarında örnek (`@example`) — editörde görünür.

## Sürümleme ve yayın

- semver: kırıcı = MAJOR (0.x'te MINOR kırıcı sayılır — erken dönemde kullanıcıya belirt).
- **changesets**: her PR'da değişiklik notu (`pnpm changeset`) → sürüm PR'ı → birleşince yayın + CHANGELOG.
- GitHub Actions'tan yayın, **provenance** ile (npm'de "built and signed on GitHub Actions" rozeti):
```yaml
permissions: { contents: write, id-token: write }
- run: pnpm publish --provenance --access public --no-git-checks
```
  npm trusted publishing (OIDC) ile token saklamaya gerek kalmaz; yoksa granüler, yalnızca yayın yetkili token.
- npm hesabında 2FA zorunlu.

## README (paketin vitrini)

Tek cümle ne yaptığı → kurulum → 10 satırlık hızlı örnek → API referansı (veya doküman sitesi, bkz. `sky-docs-site`) → SSS → katkı → lisans.
Rozetler: npm sürümü, bundle boyutu (bundlephobia/pkg-size), CI durumu. Canlı demo (StackBlitz) insanların çok sevdiği bir şey.

## Kullanımdan kaldırma

`npm deprecate @sky/slots@"<1.0.0" "1.x'e geçin, bkz. MIGRATION.md"`; kırıcı değişikliklerde göç rehberi ve mümkünse codemod.
