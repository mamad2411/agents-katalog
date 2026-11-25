# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Iablee is a Next.js 15 application for managing digital assets and beneficiaries. It uses Supabase for authentication and data storage, with support for internationalization (English and Spanish).

## Reference Documents

- `ABOUT.md` — Technical business overview of the platform, architecture, data model, i18n, middleware, and flows.
- `TECHNICAL-SPECIFICATIONS.md` — Provider-agnostic subscription and payments architecture (Stripe/PayPal/Wompi/PayU) with schema, APIs, webhooks, and gating.
- `TODO.md` — Current implementation tasks including the subscription module roadmap and additional SaaS features.

## Commands

### Development
```bash
npm run dev          # Start dev server with Turbopack
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint checks
```

### Important Notes
- The pre-commit hook runs `npm run lint` and `npm run build` automatically before each commit
- Both must pass for the commit to succeed
- Dev server uses Turbopack for faster builds

## Architecture

### Routing & Middleware

**Locale-based routing**: All pages live under `src/app/[locale]/` with support for `en` and `es` locales via next-intl.

**Authentication flow in middleware** (`src/middleware.ts:9-76`):
1. next-intl middleware runs first for locale negotiation
2. Supabase session check follows
3. Unauthenticated users → redirect to `/{locale}/auth/login`
4. Authenticated users on `/auth/*` → redirect based on assets:
   - No assets → `/wizard` (onboarding)
   - Has assets → `/dashboard`

The middleware chains two concerns: internationalization and authentication. This is why you see both `intlMiddleware` and `supabase` client creation.

### Supabase Integration

**Client configuration** (`src/lib/supabase.ts`):
- Uses `@supabase/auth-helpers-nextjs` for Next.js integration
- Validates Supabase URL format before creating client
- Contains TypeScript database schema definitions for:
  - `users` table
  - `digital_assets` table
  - `beneficiaries` table

**Authentication hook** (`src/lib/auth.ts`):
- Provides `useAuth()` hook for client components
- Manages session state, user state, and auth changes
- Includes `signOut()` helper

**Required environment variables** (`.env.local`):
```bash
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Digital Assets System

**Asset types** (`src/constants/assetTypes.ts`):
- Currently active: Cartas (letters), Audios, Fotos, Videos, Documentos
- Each asset type has:
  - Custom fields with validation
  - File type restrictions (`fileAccept`)
  - Required/optional field definitions
- Many financial asset types are commented out (bank accounts, insurance, crypto, etc.)

**Asset model** (`src/models/asset.ts`):
- Assets support beneficiary assignment
- Status types: `active`, `inactive`, `pending`, `assigned`
- Flexible schema with optional fields (email, password, website, etc.)
- Support for file attachments via `files` array
- Custom fields via `custom_fields` JSON object

### Internationalization

**Configuration** (`src/i18n/routing.ts`):
- Supported locales: `['en', 'es']`
- Default locale: `en`

**Translation files**: `messages/en.json` and `messages/es.json`

**Usage patterns**:
- Use next-intl's `useTranslations()` hook in components
- Navigation utilities available in `src/i18n/navigation.ts`
- Request-based translations in `src/i18n/request.ts`

### Component Architecture

**UI components** (`src/components/ui/`):
- Based on Radix UI primitives
- Styled with Tailwind CSS and class-variance-authority
- Use `@/lib/utils.ts` for className merging via `cn()` helper

**Key components**:
- `auth/auth-form.tsx`: Unified auth form component
- `AddAssetForm.tsx` & `AddAssetModal.tsx`: Asset creation with type-specific fields
- `AssetAttachmentsModal.tsx`: File upload and preview for assets
- `ProtectedRoute.tsx`: Client-side route protection
- `LayoutWrapper.tsx` & `ClientLayout.tsx`: Layout composition
- `Navigation.tsx` & `Navbar.tsx`: Navigation components

**Theme support**:
- Dark mode via `next-themes`
- `ThemeRegistry.tsx` and `theme-provider.tsx` manage theme state

### TypeScript Configuration

**Path aliases** (`tsconfig.json:21-23`):
- `@/*` maps to `./src/*`
- Use `@/components/...`, `@/lib/...`, etc. for imports

**Strict mode**: Enabled for type safety

### Next.js Configuration

**Image domains** (`next.config.ts:9-12`):
- Configured for OAuth providers: `appleid.cdn-apple.com`, `www.gstatic.com`
- Localhost allowed for development

**Turbopack**: Enabled by default with path alias support

## Key Development Patterns

### Adding a New Asset Type

1. Add definition to `ASSET_TYPES` array in `src/constants/assetTypes.ts`
2. Define custom fields with proper types and validation
3. Add translations to `messages/en.json` and `messages/es.json`
4. Asset form (`AddAssetForm.tsx`) will automatically render custom fields

### Working with Supabase

- Use `supabase` client from `src/lib/supabase.ts` in client components
- Middleware uses `createMiddlewareClient` from `@supabase/auth-helpers-nextjs`
- Database types are defined inline in `src/lib/supabase.ts` (Database type)

### Authentication Flow

- Public pages: Root `/` and `/auth/*` routes
- Protected pages: Everything else (enforced by middleware)
- Wizard flow: First-time users with no assets are directed to `/wizard`
- OAuth callback: Handled at `/auth/callback`

### Internationalization

- All user-facing text should be in translation files
- Use descriptive keys (e.g., `"writeWhatYouWantToSay"` not `"label1"`)
- Custom field labels in asset types reference translation keys
- URLs automatically prefixed with locale (handled by next-intl)

## Database Schema

Key tables (defined in `src/lib/supabase.ts:34-141`):

**users**: Basic user profile (id, email, full_name, timestamps)

**digital_assets**: Asset storage with flexible schema
- Foreign key: `user_id` → `users.id`
- Core fields: `asset_type`, `asset_name`, `asset_value`, `access_instructions`
- Extended fields stored in UI models: `email`, `password`, `website`, `valid_until`, `description`, `files`, `custom_fields`, `beneficiary_id`, `status`

**beneficiaries**: Beneficiary management
- Foreign key: `user_id` → `users.id`
- Fields: `full_name`, `email`, `relationship`, `phone_number`, `notes`
- Status tracking: `notified`, `status`, `last_notified_at`, `email_verified`

## Project Dependencies

**UI/Styling**:
- Tailwind CSS v4 (with `@tailwindcss/postcss`)
- Radix UI components
- Framer Motion for animations
- Lucide React for icons

**Forms & Validation**:
- react-hook-form
- zod (schema validation)
- @hookform/resolvers

**State Management**:
- @tanstack/react-query for async state

**Authentication/Database**:
- @supabase/supabase-js
- @supabase/auth-helpers-nextjs
- @supabase/ssr
