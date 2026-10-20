<!-- GSD:project-start source:PROJECT.md -->
## Project

**C.H.E.C.K.-I.N. App**

A mobile-first wellness companion app for the C.H.E.C.K.-I.N. method — a private, local-first self-tracking habit app. It teaches a seven-step daily reset practice, reminds the user to do it, lets them log completions with minimal friction, tracks contentment over time, and features a teaching video from Simone (the method creator). Built as a SvelteKit web app with Capacitor native wrappers for iOS and Android. Deployed to GitHub Pages for web demos, targeting Apple App Store and Google Play Store for native distribution.

**Core Value:** A user can learn the seven-step C.H.E.C.K.-I.N. method and build a daily reset habit with zero friction, zero guilt, and complete privacy.

### Constraints

- **Tech stack**: SvelteKit 2 + Svelte 5 + TypeScript + Tailwind CSS 4 + Capacitor 8
- **No backend**: Entirely client-side with IndexedDB via Dexie.js
- **Mobile-first**: Must look good on phone screens; desktop is secondary
- **Privacy**: Zero PII collection — no accounts, no tracking, no external data transmission
- **Style spec**: Visual design follows locked style specification (prompts/style_spec.md) — Cormorant Garamond + Inter typography, Harbor Blue (#3E6178) palette, calm sanctuary aesthetic
- **Native distribution**: iOS via Capacitor + App Store, Android via Capacitor + Play Store
- **Tone**: Warm, elegant, non-judgmental — no "you failed" language, no streak guilt
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

### Actual Stack (as implemented)
| Technology | Version | Purpose |
|------------|---------|---------|
| SvelteKit | ^2.16.0 | Full-stack framework (used in static/SPA mode) |
| Svelte | ^5.19.0 | UI framework (runes mode) |
| TypeScript | ^5.7.3 | Type safety |
| Vite | ^6.4.1 | Build tool / dev server |
| Tailwind CSS | ^4.2.2 | Styling via `@tailwindcss/vite` plugin, CSS-first config in `app.css` |
| Dexie.js | ^4.3.0 | IndexedDB wrapper for structured data (check-ins, contentment logs, preferences) |
| Chart.js | ^4.4.7 | Trend charts (contentment and check-in frequency) |
| date-fns | ^4.1.0 | Date formatting and manipulation |
| lucide-svelte | ^0.469.0 | Tree-shakable SVG icon library |
| canvas-confetti | ^1.9.4 | Celebration animations |
| Capacitor | ^8.3.0 | Native iOS/Android wrapper |
| @capacitor/local-notifications | ^8.0.2 | Scheduled daily reminders |
| @capacitor/splash-screen | ^8.0.1 | Native splash screen |
| @capacitor/status-bar | ^8.0.2 | Native status bar styling |
| @capacitor/app | ^8.1.0 | App lifecycle and back button handling |
| @sveltejs/adapter-static | ^3.0.8 | Static site generation for GitHub Pages and Capacitor |

### Key Patterns
- **Routing**: SvelteKit file-based routing (`src/routes/`)
- **State management**: Svelte writable stores (`src/lib/stores/`) for session state, Dexie for persistent data
- **Reactive DB queries**: Custom `useLiveQuery()` hook in `src/lib/hooks/dexie.svelte.ts` wrapping Dexie's `liveQuery`
- **Animations**: Svelte built-in transitions (`fly`, `fade`, `scale`, `slide`)
- **Notifications**: Capacitor LocalNotifications for native, browser Notification API for web
- **Data export**: Native Blob API for JSON/CSV export

### Deployment
| Target | Method |
|--------|--------|
| Web (demo) | GitHub Pages via GitHub Actions (`deploy.yml`), base path `/checkin_app` |
| Android | Capacitor 8 native build (`npx cap open android`) |
| iOS | Capacitor 8 native build (`npx cap open ios`) |
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
