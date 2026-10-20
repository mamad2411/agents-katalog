# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

A production-grade React Native Expo base template designed as a reusable foundation for all future mobile applications. It includes authentication, theming, internationalization, API integration, error handling, and testing infrastructure.

## Tech Stack

- **Framework**: React Native 0.83.2 + Expo SDK 55
- **Routing**: expo-router (file-based, typed routes)
- **Language**: TypeScript 5.9
- **Styling**: react-native-unistyles 3.x
- **State Management**: @tanstack/react-query (server) + Zustand (client)
- **Backend**: Supabase (graceful degradation if unconfigured)
- **API Client**: Axios with auth/error interceptors
- **i18n**: react-i18next (EN/AR, RTL support)
- **Storage**: react-native-mmkv
- **Forms**: react-hook-form + Zod
- **Linting**: ESLint 9 flat config

## Commands

```bash
npm start                  # Start Expo dev server
npm run ios                # Run on iOS
npm run android            # Run on Android
npm run type-check         # TypeScript type checking
npm run lint               # ESLint
npm run lint:fix           # Auto-fix ESLint errors
npm run format             # Prettier format
npm run format:check       # Check formatting
npm run validate           # All checks (type-check + lint + format)
npm test                   # Run tests
npm run test:coverage      # Coverage report
```

## Project Structure

```
src/
├── common/components/     # 33 shared UI components (see docs/COMPONENTS.md for full API reference)
├── config/                # Centralized env config with validation
├── features/              # Feature modules (auth, settings)
├── hooks/                 # useBottomPadding, useNetworkStatus, useScreenDimensions, useProtectedRoute
├── i18n/                  # Translation files (en.json, ar.json) and config
├── integrations/          # Supabase client (graceful init)
├── providers/             # QueryProvider, auth store
├── services/api/          # Axios client with interceptors
├── theme/                 # Semantic tokens, metrics, fonts
├── types/                 # Global TypeScript types
└── utils/storage/         # MMKV with typed keys

app/                       # Expo Router
├── _layout.tsx            # Root layout with ErrorBoundary, providers
├── +not-found.tsx
└── (main)/(tabs)/         # Home + Settings tabs
```

## Path Aliases

- `@/*` → `src/*`
- `~/*` → `app/*`

## Theme System

Indigo-based color palette with Teal accent. Light and dark modes with semantic tokens.

- Use `theme.colors.brand.primary`, `theme.colors.text.secondary`, etc.
- Use `theme.colors.mode` to check light/dark
- Responsive metrics: `rf(16)` for fonts, `hs(20)` for horizontal, `vs(24)` for vertical
- Style pattern: `StyleSheet.create((theme) => ({...}))` from react-native-unistyles

## Component Pattern

```
Component/
├── Component.tsx
├── Component.styles.ts    # Optional
├── Component.types.ts     # Optional
└── index.ts
```

## Feature Module Pattern

```
feature/
├── components/
├── services/
├── hooks/
├── stores/
├── types/
├── schemas/
└── constants/
```

## Key Rules

- All user-facing text via `useTranslation()` hook
- No `any` types
- No inline styles - use `StyleSheet.create`
- No hardcoded strings for UI text
- No color literals - use theme tokens
- Consistent type imports: `import type { Foo } from './types'`

## Claude Code Hooks

Three shell-script hooks in `.claude/hooks/` enforce project rules deterministically:

| Hook                            | Trigger                   | Purpose                                                                                     |
| ------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------- |
| `block-suppression-comments.sh` | PreToolUse (Write\|Edit)  | Blocks `eslint-disable`, `@ts-ignore`, `@ts-nocheck`, bare `@ts-expect-error` in code files |
| `block-no-verify.sh`            | PreToolUse (Bash)         | Blocks `git commit --no-verify` and `git push --no-verify`                                  |
| `lint-after-edit.sh`            | PostToolUse (Write\|Edit) | Runs `eslint --fix` on edited ts/tsx/js/jsx files (informational)                           |

Hook configuration lives in `.claude/settings.json`.

## Strict Rules (Hook-Enforced)

These rules are enforced by hooks and will block tool calls that violate them:

- **NEVER** add `eslint-disable`, `eslint-disable-next-line`, or `eslint-disable-line` comments
- **NEVER** use `@ts-ignore` or `@ts-nocheck`
- **NEVER** use bare `@ts-expect-error` (must include a description if absolutely necessary)
- **NEVER** use `any` type (`as any`, `: any`, `<any>`)
- **NEVER** use `--no-verify` with git commit or push

When you encounter a type error, use type narrowing, `unknown` with type guards, proper interfaces, or generics. When you encounter a lint error, fix the code — don't suppress the warning.

## Auth Pattern

Auth is managed by Zustand store (`useAuthStore`), not a React context provider. `useAuthInit()` hook is called in the root layout to initialize auth and set up Supabase listener.

## Supabase

Gracefully handles missing env vars - app boots and works without Supabase configured. Just add credentials to `.env` when ready.

## Component Library (33 Components)

- **Action**: Button, IconButton
- **Data Display**: Text, Avatar, Badge, Card, Chip, ListItem
- **Disclosure**: Accordion
- **Feedback**: EmptyState, ErrorBoundary, Loading, ProgressBar, Skeleton, Snackbar
- **Form**: Checkbox, FormField, Input, RadioGroup, SearchBar, SegmentedControl, Select, Switch, TextArea
- **Layout**: Divider, ScreenContainer
- **Overlay**: Dialog, Menu
- **Typography**: Icon, Text

See `docs/COMPONENTS.md` for full API reference with props tables and usage examples.

## Migration

When adapting this template for a specific app (e-commerce, social, games, etc.):

- **Non-technical users / no AI:** Run `npm run migrate` for the interactive wizard
- **AI agents:** Follow `docs/MIGRATION.md` for the complete step-by-step guide

## Extended Documentation

- `CONVENTIONS.md` - Comprehensive coding conventions (source of truth)
- `docs/COMPONENTS.md` - Full component API reference
- `docs/AI-GUIDE.md` - Pattern cookbook, file templates, anti-patterns
- `docs/MIGRATION.md` - Step-by-step template migration guide
- `docs/ARCHITECTURE.md` - Architecture overview
- `docs/SETUP.md` - Setup guide
- `AGENTS.md` - Universal AI agent instructions

## Commit Message Format

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
```
