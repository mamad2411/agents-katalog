---
name: react-i18n-localization
description: Add i18n localization to a React + Vite + TypeScript SPA using i18next and react-i18next with structured JSON translation files
source: auto-skill
extracted_at: '2026-06-24T07:32:01.167Z'
---

## Adding i18n Localization to a React SPA

### When to use
When you need to add multi-language support to a React (Vite/TypeScript) frontend that has hardcoded English strings.

### Approach

#### 1. Install dependencies
```bash
bun add i18next react-i18next
```
(or `npm install` / `yarn add` depending on the package manager)

#### 2. Create translation infrastructure (`src/i18n/`)

**`src/i18n/index.ts`** — Config file:
- Import `i18next` and `initReactI18next`
- Import JSON translation files
- Read saved language from `localStorage` (fallback to `'en'`)
- Call `i18n.use(initReactI18next).init(...)` with `resources`, `lng`, `fallbackLng`, `interpolation: { escapeValue: false }`
- Listen to `languageChanged` event to persist to `localStorage`

**`src/i18n/{locale}.json`** — One JSON file per language:
- Structure keys by domain/feature: `common`, `nav`, `footer`, `home`, `login`, `register`, `search`, `dashboard`, `notFound`, `loginForm`, `registerForm`, `houseForm`, `filters`, `booking`, etc.
- Use `{{variable}}` for interpolation (e.g., `"welcome": "Welcome, {{name}}"`)
- Use `_other` suffix for plurals (e.g., `"room"` / `"room_other"`)
- Keep placeholders in a sub-key like `emailPlaceholder`, `passwordPlaceholder`

#### 3. Initialize in entry point
Add `import './i18n';` to `src/main.tsx` (before App import). No provider wrapper needed — `initReactI18next` handles it via React context internally.

#### 4. Update components systematically

For each component file:
1. Add `import { useTranslation } from 'react-i18next';`
2. Destructure `const { t } = useTranslation();` (add `i18n` if language switching is needed)
3. Replace every hardcoded string with `t('namespace.key')` or `t('namespace.key', { var: value })`
4. For plurals: `t('common.room', { count: house.rooms })`

**Priority order for updating files:**
1. Pages (most user-facing text)
2. Layout components (Navbar, Footer) — also add language switcher here
3. Form components
4. Feature/domain components

#### 5. Add language switcher
Add a toggle button in the Navbar:
```tsx
const { t, i18n } = useTranslation();

function toggleLanguage() {
  i18n.changeLanguage(i18n.language === 'en' ? 'my' : 'en');
}
```
Display the *other* language name so users know what they'll switch to.

#### 6. Inventory all strings before starting
Before writing translation files, read every component to build a complete inventory of hardcoded strings. This prevents missing strings and multiple passes. Group them by feature/domain for the JSON structure.

### Key gotchas
- `escapeValue: false` is needed for React since React already escapes output
- Error messages from API responses should remain as-is (dynamic from server); only fallback error strings need translation
- Placeholders in `<Input>` and `<textarea>` elements need translation too — easy to miss
- Date formatting via `toLocaleDateString()` automatically respects the browser locale but won't change with i18n language switch unless you pass the locale explicitly
- Brand name ("Rent4U") can be a translation key but typically stays the same across languages
