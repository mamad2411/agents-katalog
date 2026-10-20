# Love Diary — Project Manual

## Project Overview

《恋爱日记》是一对恋人的专属 PWA 日记应用。以温暖阳光与柔和浪漫为视觉基调，记录恋爱中的每一天。纯前端单机应用，数据持久化在 LocalStorage。

## Tech Stack

```yaml
Framework:    Vue 3 (Composition API + <script setup>)
Build:        Vite 5
Styling:      Tailwind CSS 3.4
State:        Pinia (localStorage plugin)
Router:       Vue Router 4
Icons:        lucide-vue-next
Animation:    CSS @keyframes + Vue <Transition>
PWA:          vite-plugin-pwa
Testing:      Vitest + @vue/test-utils
Lint:         ESLint + Prettier
Language:     TypeScript (strict)
```

## Quick Start

```bash
# Install dependencies
npm install

# Start dev server (default: http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Generate PWA icons & service worker
npm run generate-pwa
```

## Testing

```bash
# Run unit tests (watch mode)
npm run test

# Run tests once (CI mode)
npm run test:ci

# Run tests with coverage report
npm run test:coverage
```

## Linting & Formatting

```bash
# Lint check
npm run lint

# Lint with auto-fix
npm run lint:fix

# Format check
npm run format

# Format with auto-fix
npm run format:fix

# Type check
npm run typecheck
```

## Project Conventions

### Git

- Branch naming: `feature/<desc>`, `fix/<desc>`, `chore/<desc>`
- Commit style: [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat:` new feature
  - `fix:` bug fix
  - `refactor:` code restructure
  - `style:` formatting only
  - `docs:` documentation
  - `test:` test changes
  - `chore:` build/config/tooling

### Code Style

- Vue 3 `<script setup lang="ts">` + Composition API
- Single-file components (SFC), one component per `.vue` file
- TypeScript strict mode. No `any` without explicit justification.
- All UI must use Tailwind classes mapped to `DESIGN.md` tokens.
- Pinia stores auto-sync to LocalStorage via custom plugin.
- No `console.log` in production — use a proper logger or remove.

### Directory Structure

```
love-diary/
├── public/
│   └── icons/               # PWA icons
├── src/
│   ├── components/
│   │   ├── ui/              # 设计系统基础组件 (DiaryCard, DiaryButton, DiaryInput)
│   │   ├── features/        # 功能组件 (CountdownTimer, HabitCard, StatusBar)
│   │   └── layout/          # 布局组件 (AppShell, BottomNav)
│   ├── composables/         # Vue Composables (useLocalStorage, useHaptic, useImageUpload)
│   ├── stores/              # Pinia stores (diary, fragments, grow, footprints, bucketlist, care)
│   ├── pages/               # 路由页面 (6 个核心页面)
│   ├── router/              # Vue Router 配置
│   ├── types/               # TypeScript 类型定义
│   ├── utils/               # 工具函数 (date, base64, storage)
│   ├── App.vue
│   └── main.ts
├── docs/
│   └── specs/               # SPEC-*.md & TASKS-*.md
├── DESIGN.md                # 设计系统规范
├── CLAUDE.md                # 本文件
├── .clinerules              # Superpowers 工作流
├── tailwind.config.js
├── vite.config.ts
└── tsconfig.json
```

## Data Layer

- **Storage Engine**: LocalStorage (via Pinia plugin — every mutation auto-persists)
- **Image/Video**: Base64 encoded strings stored inline in LocalStorage
- **Schema**: JSON objects matching Pinia store state shape
- **Migration**: Version field in store root; on load, run migration fns if version mismatch

```ts
// Example Pinia localStorage plugin
function localStoragePlugin({ store }) {
  const key = `love-diary:${store.$id}`
  const saved = localStorage.getItem(key)
  if (saved) store.$patch(JSON.parse(saved))
  store.$subscribe(() => {
    localStorage.setItem(key, JSON.stringify(store.$state))
  })
}
```

## Design System

See [DESIGN.md](./DESIGN.md) for the complete visual design system.
All UI development MUST adhere to the tokens defined there.

### Tailwind Config Quick Ref

```js
// All colors, spacing, borderRadius, fontFamily must match DESIGN.md
colors: { sunshine: {...}, warm: {...}, rose: {...} }
borderRadius: { sm: '8px', md: '12px', lg: '16px', xl: '24px', full: '9999px' }
fontFamily: { display: [...], body: [...], hand: [...] }
```

## PWA Checklist

- [ ] `vite-plugin-pwa` configured with `generateSW`
- [ ] manifest.json with name "恋爱日记", short_name "Love Diary"
- [ ] Icons: 192x192, 512x512 (sunshine-rose themed app icon)
- [ ] Theme color: `#FFF9E6` (sunshine-100)
- [ ] Background color: `#FFFEF7` (sunshine-50)
- [ ] `display: standalone` with `apple-mobile-web-app-capable`
