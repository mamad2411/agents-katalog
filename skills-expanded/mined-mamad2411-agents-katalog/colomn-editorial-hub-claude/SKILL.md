# Column Editorial Hub

## Project Overview
복수 칼럼니스트 Generator를 지원하는 3패널 편집 플랫폼.
Road(길진홍) Generator + 범용 Generator를 플러그인 방식으로 제공.

## Tech Stack
- Next.js 15 (App Router)
- TypeScript (strict mode)
- CSS Modules
- React Context (state management)
- Server Actions (API key protection)

## Coding Conventions

### Types
- `type` only (no `interface`)
- PascalCase for types: `GeneratorConfig`, `DraftData`

### Naming
- Components: PascalCase (`TutorPanel.tsx`)
- Functions: camelCase (`extractFacts`)
- Constants: UPPER_SNAKE_CASE (`ROAD_TUTOR_PROMPT`)
- Folders: kebab-case, generators 내부는 id 이름 (`road/`, `generic/`)

### Import Order
1. React / Next.js
2. External libraries
3. Internal absolute (`@/...`)
4. Relative (`./...`)
5. Type-only imports (`import type`)
6. Styles

### Error Handling
- Server Actions: `{ data: T } | { error: string }` pattern
- try-catch wrapping in all Server Actions

### Key Rules
- No `any` type
- No `interface` (use `type` only)
- No honorific speech (경어체) in AI prompts
- API keys: server-side only (never NEXT_PUBLIC_)
