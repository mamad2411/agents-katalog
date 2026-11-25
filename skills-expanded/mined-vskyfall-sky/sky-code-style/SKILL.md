---
name: sky-code-style
description: >-
  Kod stili ve otomatik kalite araçları: Biome vs ESLint (flat config) + Prettier seçimi,
  önerilen kural setleri (typescript-eslint, react-hooks, jsx-a11y, import sırası), EditorConfig,
  husky + lint-staged ile commit öncesi kontroller, commitlint, VS Code ayarları, Python (ruff),
  Go (gofmt, golangci-lint), Rust (rustfmt, clippy), isimlendirme ve dosya düzeni kuralları,
  mevcut projeye kademeli ekleme. "Lint kur", "Prettier", "Biome", "kod stili", "pre-commit" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Kod Stili & Araçlar

İlke: **stil tartışılmaz, araca bırakılır.** İnsanlar mantığı inceler; boşluklar, tırnaklar, import sırası otomatik.

## JS/TS: seçim

| Seçenek | Ne zaman |
|---|---|
| **Biome** | yeni proje, tek araç (lint + format), çok hızlı, sıfıra yakın yapılandırma |
| **ESLint (flat) + Prettier** | geniş eklenti ekosistemi gerekiyor (özel kurallar, framework eklentileri), mevcut proje |

### Biome

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "formatter": { "indentStyle": "space", "lineWidth": 100 },
  "linter": { "rules": { "recommended": true, "correctness": { "noUnusedImports": "error" }, "suspicious": { "noConsole": "warn" } } },
  "assist": { "actions": { "source": { "organizeImports": "on" } } }
}
```
`biome check --write .` (lint + format + import düzenleme). Şema sürümünü kurulu Biome sürümüne göre ayarla.

### ESLint flat config

```js
// eslint.config.mjs
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";
export default tseslint.config(
  { ignores: ["dist", ".next", "coverage"] },
  js.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  { languageOptions: { parserOptions: { projectService: true } } },
  reactHooks.configs["recommended-latest"],
  jsxA11y.flatConfigs.recommended,
  { rules: { "@typescript-eslint/consistent-type-imports": "error", "no-console": ["warn", { allow: ["warn", "error"] }] } },
);
```
Next.js'te `eslint-config-next` ekle. Prettier ile çakışan stil kurallarını kapat (`eslint-config-prettier`). Prettier: `{ "printWidth": 100 }` + `prettier-plugin-tailwindcss` (sınıf sıralama).

## Commit öncesi

```json
// package.json
"lint-staged": { "*.{ts,tsx,js,json,css,md}": ["biome check --write --no-errors-on-unmatched"] }
```
`npx husky init` → `.husky/pre-commit`: `npx lint-staged`. Yalnızca değişen dosyalar → hızlı.
Tip kontrolü ve testler pre-commit'te yavaş olabilir → pre-push veya CI.
Commit mesajı: `commitlint` + `@commitlint/config-conventional` (`.husky/commit-msg`) (bkz. `sky-git`).

## EditorConfig ve editör

```ini
# .editorconfig
root = true
[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
insert_final_newline = true
trim_trailing_whitespace = true
```
`.vscode/settings.json`: kaydederken format, varsayılan formatter, `"editor.codeActionsOnSave": { "source.fixAll": "explicit" }`;
`.vscode/extensions.json` önerilen eklentiler. `.gitattributes`: `* text=auto eol=lf` (Windows satır sonu karmaşasını bitirir).

## Diğer diller

- **Python**: `ruff check --fix` + `ruff format` (bkz. `sky-python`), pre-commit framework (`.pre-commit-config.yaml`).
- **Go**: `gofmt`/`goimports` + `golangci-lint run`. **Rust**: `cargo fmt` + `cargo clippy -- -D warnings`.
- **PHP**: Pint / PHP-CS-Fixer + PHPStan. **Ruby**: RuboCop. **C#**: `dotnet format` + analyzers. **Kotlin**: ktlint/detekt. **Swift**: swift-format/SwiftLint.

## İsimlendirme ve düzen (dil bağımsız ilkeler)

- İsim niyeti söyler: `upcomingBookings`, `isEligibleForRefund`; kısaltma yok (`usr`, `bkg`), tek harf yalnızca kısa döngüde.
- Boolean: `is/has/can/should` öneki. Fonksiyon: fiil (`calculateTotal`). Sabit: `MAX_RETRY`.
- Dosya adları projede tek biçim (`kebab-case.ts` veya bileşenler `PascalCase.tsx`).
- Fonksiyon ~40 satırı, dosya ~300 satırı geçiyorsa bölmeyi düşün (bkz. `sky-refactor`).
- Yorumlar **neden**'i anlatır; ne yaptığını kod anlatsın. Eskimiş yorum yanlış yorumdur.

## Mevcut projeye ekleme

Tüm kodu tek seferde biçimlendir → **ayrı commit** (`chore: format with biome`) + `.git-blame-ignore-revs` dosyasına SHA ekle (blame bozulmaz).
Kuralları kademeli sıkılaştır: önce `warn`, temizlik, sonra `error`.
