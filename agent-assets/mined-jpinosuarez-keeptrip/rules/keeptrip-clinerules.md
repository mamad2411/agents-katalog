# Keeptrip Master Agent Rules (.clinerules)

## 1. Role & Architectural Boundaries (FSD)
- You are a Senior Product Engineer under the supervision of the Staff Frontend Architect.
- Strictly adhere to Feature-Sliced Design (FSD): `app` > `pages` > `widgets` > `features` > `entities` > `shared`.
- Upward imports and illegal cross-feature imports are strictly forbidden. Features only communicate with `entities` or `shared`.
- Use the Repository Pattern (`src/shared/api/services/`) for data access; direct Firestore calls inside UI components are prohibited.

## 2. Styling, Tokens & Zero-JS Layouts
- Use Tailwind CSS with Design Tokens from `tailwind.config.js`. Arbitrary utility values (e.g., `w-[123px]`, `text-[#ff0000]`) are strictly forbidden unless required for iOS dynamic safe-area calculation (`env(safe-area-...)`) or visualViewport offsets.
- Always combine classes using the `cn()` helper (`clsx` + `tailwind-merge`).
- Zero-JS Layouts: Responsive layouts must rely exclusively on Tailwind CSS media queries (`md:`, `lg:`). Never use `window.innerWidth`, `isMobile`, or JS event listeners for structural DOM layout branching.

## 3. Linguistic Hygiene & Strict i18n
- Source code (variables, functions, components, filenames, internal comments) must be 100% in English.
- User-facing text must be 100% localized using `useTranslation()` (`t('namespace:key')`) via `react-i18next`. Hardcoded Spanish/English UI strings in JSX are considered severe regressions.

## 4. Visual Excellence & Mobile Ergonomics
- Touch Targets: Every interactive element must have a minimum bounding box of 44x44px (primary actions: 48–56px).
- Animations & Micro-interactions: Managed strictly via non-blocking `framer-motion` spring physics (`stiffness: 100, damping: 20`).
- Prevent horizontal scrollbars on mobile viewports under all circumstances.

## 5. Cost-Aware Architecture & Performance Defense
- Firestore: Zero N+1 writes. Always use diffing and `writeBatch` for multi-document operations. Snapshot listeners (`onSnapshot`) must depend strictly on stable primitive identifiers (`user.uid`).
- Mapbox GL: Interactive map views (`MapaView`, `HomeMap`) must apply memoization and stable coordinate hash keys to prevent parent state churn from triggering WebGL canvas redraws. Defer WebGL loading via interaction-based listeners (`{ once: true }`).

## 6. Git Protocol & Release-Please Versioning
- NEVER modify or bump the `version` field in `package.json`. Automated Semantic Versioning is managed exclusively by Google's `release-please` bot via Conventional Commits.
- Never work directly on `main`. Always work on dedicated branches (`fix/*`, `feature/*`).
- Commit messages must follow Conventional Commits specification strictly (`feat:`, `fix:`, `chore:`, `refactor:`, `test:`).
- Always verify quality gates before requesting approval (`npm run lint`, unit tests passing).