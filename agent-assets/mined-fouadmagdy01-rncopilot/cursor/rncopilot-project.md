---
description: React Native Expo Template - Project Rules
alwaysApply: true
---

# Project Rules

This is a production-grade React Native Expo template. All rules below are mandatory.

See `CONVENTIONS.md` for detailed conventions and `docs/AI-GUIDE.md` for patterns and recipes.

## Stack Summary

- React Native 0.83.2 + Expo SDK 55, expo-router (file-based)
- TypeScript 5.9 strict, path aliases: `@/*` = `src/*`, `~/*` = `app/*`
- **Styling:** react-native-unistyles 3.x (NOT react-native StyleSheet)
- **Server state:** @tanstack/react-query
- **Client state:** Zustand (auth via `useAuthStore`)
- **Forms:** react-hook-form + `zod/v4`
- **Storage:** react-native-mmkv via `@/utils/storage`
- **i18n:** react-i18next, EN + AR (RTL)
- **HTTP:** Axios via `@/services/api` (auto-attaches Bearer token)

## Non-Negotiable Rules

### Styling

```typescript
// Import ALWAYS from react-native-unistyles
import { StyleSheet } from 'react-native-unistyles';

// ALWAYS use theme callback
const styles = StyleSheet.create((theme) => ({
  container: {
    padding: theme.metrics.spacing.p16,          // NOT padding: 16
    backgroundColor: theme.colors.background.surface,  // NOT '#FFFFFF'
    borderRadius: theme.metrics.borderRadius.md,
  },
}));

// NEVER inline styles
// WRONG: <View style={{ padding: 16, backgroundColor: '#fff' }}>
// RIGHT: <View style={styles.container}>
```

### Components

```typescript
// Always use project Text, not React Native Text
import { Text } from '@/common/components/Text';
<Text variant="h1">{t('home.title')}</Text>

// Always use ScreenContainer as screen root
import { ScreenContainer } from '@/common/components/ScreenContainer';
export default function MyScreen() {
  return <ScreenContainer scrollable>{/* content */}</ScreenContainer>;
}

// Import from barrel, not implementation
import { Button } from '@/common/components/Button';           // CORRECT
import { Button } from '@/common/components/Button/Button';    // WRONG
```

### i18n - Every String Must Be Translated

```typescript
const { t } = useTranslation();
<Text>{t('home.welcome')}</Text>      // CORRECT
<Text>Welcome</Text>                  // WRONG - hardcoded

// Update BOTH files when adding text:
// src/i18n/locales/en.json
// src/i18n/locales/ar.json
```

### Auth - Zustand Only

```typescript
// In components
import { useAuthStore } from '@/providers/auth/authStore';
const user = useAuthStore((s) => s.user);                // CORRECT - selector
const store = useAuthStore();                             // WRONG - whole store

// Outside React
const session = useAuthStore.getState().session;

// NEVER create React Context for auth
```

### TypeScript

```typescript
// No any types
const data: Product[] = response.data;   // CORRECT
const data: any = response.data;         // WRONG

// Type-only imports
import type { ButtonProps } from '@/common/components/Button';

// Named exports in src/ (not default)
export function MyComponent() {}         // CORRECT
export default function MyComponent() {} // WRONG (except app/ screens)

// Zod - use v4
import { z } from 'zod/v4';             // CORRECT
import { z } from 'zod';               // WRONG
```

### Forms

```typescript
import { z } from 'zod/v4';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.email('validation.emailInvalid'),      // i18n key, not raw text
  password: z.string().min(8, 'validation.passwordMin'),
});

const { control, handleSubmit } = useForm({
  resolver: zodResolver(schema),
  defaultValues: { email: '', password: '' },
});
```

### API Calls

```typescript
import { api } from '@/services/api';
// Auto-attaches Bearer token, normalizes errors, handles 401

const data = await api.get<Product[]>('/products').then((r) => r.data);

// All API calls go in src/features/<feature>/services/<feature>Service.ts
// Wrap in React Query hooks in src/features/<feature>/hooks/
```

## Directory Structure

```
src/
  common/components/    33 shared UI components
  config/               env.ts (centralized, validated)
  features/<feature>/   components/, services/, hooks/, stores/, types/, schemas/, constants/
  hooks/                useBottomPadding, useNetworkStatus, useScreenDimensions, useProtectedRoute
  i18n/locales/         en.json, ar.json
  providers/auth/       authStore.ts (useAuthStore, useAuthInit)
  services/api/         client.ts (Axios instance: api)
  theme/                metrics.ts (rf, hs, vs), light-theme.ts, dark-theme.ts
  utils/storage/        useStorage, useStorageBoolean, STORAGE_KEYS

app/
  _layout.tsx           GestureHandler > ErrorBoundary > QueryProvider > BottomSheet > AppContent
  (main)/(tabs)/        Tab screens
```

## Routing

```typescript
// Expo Router - all navigation via router
import { router } from 'expo-router';
router.push('/products');
router.replace('/(auth)/login');

// Route params
import { useLocalSearchParams } from 'expo-router';
const { id } = useLocalSearchParams<{ id: string }>();

// All app/ files use default export (Expo Router requirement)
export default function ProductsScreen() {}
```

## Theme Tokens Quick Reference

```
theme.colors.brand.primary          - #6366F1 (indigo)
theme.colors.brand.tertiary         - #14B8A6 (teal accent)
theme.colors.background.app         - screen background
theme.colors.background.surface     - cards
theme.colors.background.input       - text inputs
theme.colors.text.primary           - main text
theme.colors.text.secondary         - supporting
theme.colors.text.muted             - placeholder
theme.colors.text.inverse           - on dark backgrounds
theme.colors.border.default         - standard borders
theme.colors.border.focus           - input focus
theme.colors.state.success/error/warning/info
theme.colors.overlay.modal          - rgba(0,0,0,0.5)
theme.metrics.spacing.p{4-120}      - horizontal (hs scaled)
theme.metrics.spacingV.p{4-120}     - vertical (vs scaled)
theme.metrics.borderRadius.xs/sm/md/lg/xl/full
theme.metrics.iconSize.xs/sm/md/lg/xl
theme.fonts.size.xxs through 6xl
```

## Commit Format

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
```

## Template Migration

Follow `docs/MIGRATION.md` for the step-by-step migration guide.
