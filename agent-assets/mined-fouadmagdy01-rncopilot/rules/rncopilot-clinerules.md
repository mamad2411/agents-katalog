# Cline Rules - React Native Expo Template

This is a production-grade React Native Expo template project. Read and apply every rule here before making code changes.

## Project Context

**Stack:** React Native 0.83.2 + Expo SDK 55, expo-router, TypeScript 5.9 strict, react-native-unistyles 3.x, TanStack Query, Zustand, Supabase, Axios, react-i18next (EN+AR+RTL), react-native-mmkv, react-hook-form, zod/v4.

**Path aliases:**
- `@/*` → `src/*`
- `~/*` → `app/*`

**Key file locations:**
- 33 shared components: `src/common/components/`
- Auth store: `src/providers/auth/authStore.ts`
- API client: `src/services/api/client.ts`
- Theme: `src/theme/` (light-theme.ts, dark-theme.ts, metrics.ts)
- Storage: `src/utils/storage/`
- i18n: `src/i18n/locales/en.json` and `ar.json`
- Environment config: `src/config/env.ts`
- Root layout: `app/_layout.tsx`

---

## Mandatory Coding Rules

### Styling

The project uses react-native-unistyles 3.x. This is NOT the same as React Native's built-in StyleSheet.

```typescript
// ALWAYS import from react-native-unistyles
import { StyleSheet, useUnistyles } from 'react-native-unistyles';

// ALWAYS use theme callback - every property uses theme tokens
const styles = StyleSheet.create((theme) => ({
  screen: {
    flex: 1,
    backgroundColor: theme.colors.background.app,
  },
  card: {
    padding: theme.metrics.spacing.p16,
    paddingVertical: theme.metrics.spacingV.p20,
    backgroundColor: theme.colors.background.surface,
    borderRadius: theme.metrics.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.border.default,
  },
  title: {
    fontSize: theme.fonts.size.xl,
    color: theme.colors.text.primary,
    fontWeight: '700',
  },
  subtitle: {
    fontSize: theme.fonts.size.sm,
    color: theme.colors.text.secondary,
  },
  errorText: {
    fontSize: theme.fonts.size.xs,
    color: theme.colors.state.error,
  },
}));
```

Rules:
- NEVER `import { StyleSheet } from 'react-native'`
- NEVER inline styles: `style={{ padding: 16 }}`
- NEVER color literals: `'#6366F1'`, `'white'`, `'#fff'`
- NEVER hardcoded spacing: `padding: 16` → use `theme.metrics.spacing.p16`

Access theme in component body:
```typescript
import { useUnistyles } from 'react-native-unistyles';
const { theme } = useUnistyles();
```

Responsive helper functions (import from `@/theme/metrics`):
```typescript
import { rf, hs, vs } from '@/theme/metrics';
rf(16)  // responsive font size
hs(20)  // horizontal scale
vs(24)  // vertical scale
```

---

### Project Components

Always use project components. Never use bare React Native primitives for UI that has a project equivalent.

**Text** — use for all user-facing text:
```typescript
import { Text } from '@/common/components/Text';
// Variants: h1, h2, h3, body, bodySmall, caption, label, overline
// Weights: regular, medium, semibold, bold
<Text variant="h1">{t('screen.title')}</Text>
<Text variant="body" color={theme.colors.text.secondary}>{t('screen.body')}</Text>
```

**Button:**
```typescript
import { Button } from '@/common/components/Button';
// Variants: primary, secondary, outline, ghost | Sizes: sm, md, lg
<Button title={t('actions.save')} variant="primary" size="md" loading={isPending} onPress={fn} />
<Button title={t('actions.cancel')} variant="ghost" fullWidth onPress={fn} />
<Button title={t('actions.share')} variant="outline" leftIcon={<Icon name="share-outline" />} onPress={fn} />
```

**ScreenContainer** — root of every screen:
```typescript
import { ScreenContainer } from '@/common/components/ScreenContainer';
export default function MyScreen() {
  return (
    <ScreenContainer scrollable padded>
      {/* screen content */}
    </ScreenContainer>
  );
}
```

**Icon** — Ionicons only:
```typescript
import { Icon } from '@/common/components/Icon';
// Variants: primary, secondary, tertiary, muted, inverse, accent
<Icon name="home-outline" variant="primary" size={20} />
<Icon name="alert-circle-outline" color={theme.colors.state.error} />
```

**Card:**
```typescript
import { Card } from '@/common/components/Card';
// Variants: default, elevated, outlined
<Card variant="elevated" pressable onPress={() => router.push('/detail')}>
  <Text variant="h3">{item.title}</Text>
</Card>
```

**Input:**
```typescript
import { Input } from '@/common/components/Input';
<Input
  label={t('fields.email')}
  value={value}
  onChangeText={onChange}
  error={errors.email ? t(errors.email.message) : undefined}
  keyboardType="email-address"
  autoCapitalize="none"
  leftIcon={<Icon name="mail-outline" variant="muted" />}
/>
```

**Loading:**
```typescript
import { Loading } from '@/common/components/Loading';
if (isLoading) return <Loading fullScreen />;
// or inline: {isLoading && <Loading size="small" />}
```

**EmptyState:**
```typescript
import { EmptyState } from '@/common/components/EmptyState';
<EmptyState
  title={t('list.noItems')}
  message={t('list.noItemsMessage')}
  icon={<Icon name="file-tray-outline" size={48} variant="muted" />}
  actionLabel={t('actions.refresh')}
  onAction={refetch}
/>
```

**ErrorBoundary** — wrap risky subtrees:
```typescript
import { ErrorBoundary } from '@/common/components/ErrorBoundary';
<ErrorBoundary><MyDataComponent /></ErrorBoundary>
```

**Dialog:**
```typescript
import { Dialog } from '@/common/components/Dialog';
<Dialog
  visible={showConfirm}
  onDismiss={() => setShowConfirm(false)}
  title={t('dialogs.deleteTitle')}
  message={t('dialogs.deleteMessage')}
  actions={[
    { label: t('actions.cancel'), onPress: () => setShowConfirm(false), variant: 'ghost' },
    { label: t('actions.delete'), onPress: handleDelete, variant: 'primary' },
  ]}
/>
```

**Snackbar:**
```typescript
import { Snackbar } from '@/common/components/Snackbar';
<Snackbar
  visible={visible}
  message={t('messages.saved')}
  variant="success"  // default, success, error
  onDismiss={() => setVisible(false)}
/>
```

Import from barrels only: `@/common/components/Button` not `@/common/components/Button/Button`.

---

### Internationalization

All user-visible text MUST go through `useTranslation`. This includes button titles, labels, placeholders, error messages, accessibility labels, dialog titles, and snackbar messages.

```typescript
const { t } = useTranslation();

// Every string
<Text variant="h1">{t('home.title')}</Text>
<Button title={t('actions.save')} />
<Input placeholder={t('fields.namePlaceholder')} />
accessibilityLabel={t('actions.close')}
```

When adding new keys, update BOTH files simultaneously:
```
src/i18n/locales/en.json  →  { "home": { "title": "Home" } }
src/i18n/locales/ar.json  →  { "home": { "title": "الرئيسية" } }
```

Zod schema messages use i18n keys (not raw text):
```typescript
z.string().min(1, 'validation.required')         // CORRECT
z.string().min(1, 'This field is required')      // WRONG
```

---

### Auth

Auth state is managed by Zustand. Never create React Context for auth.

```typescript
import { useAuthStore } from '@/providers/auth/authStore';

// In React components - always use a selector
const user = useAuthStore((s) => s.user);
const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
const clearSession = useAuthStore((s) => s.clearSession);

// Outside React (e.g., in Axios interceptors)
const session = useAuthStore.getState().session;
```

The store is initialized in `app/_layout.tsx` via `useAuthInit()`. Never call `initialize()` elsewhere.

---

### State Management

```typescript
// Zustand for client state
import { create } from 'zustand';

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  clearCart: () => set({ items: [] }),
}));

// ALWAYS use selectors
const items = useCartStore((s) => s.items);    // CORRECT - precise subscription
const store = useCartStore();                   // WRONG - subscribes to all

// React Query for server/async state
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useProducts() {
  return useQuery({
    queryKey: ['products', 'list'],
    queryFn: () => api.get<Product[]>('/products').then((r) => r.data),
  });
}
```

---

### API

```typescript
import { api } from '@/services/api';
// Configured with base URL from env.ts
// Auto-attaches Authorization: Bearer <token>
// 401 response → calls clearSession()
// Errors normalized to Error with human-readable .message

// Service function pattern (place in src/features/<feature>/services/)
export async function fetchProduct(id: string): Promise<Product> {
  const { data } = await api.get<Product>(`/products/${id}`);
  return data;
}
```

---

### Forms

```typescript
// Always zod/v4 (not zod)
import { z } from 'zod/v4';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  name: z.string().min(1, 'validation.required'),
  email: z.email('validation.emailInvalid'),
  role: z.enum(['admin', 'user']),
});

type FormData = z.infer<typeof schema>;

function MyForm() {
  const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', email: '', role: 'user' },
  });

  return (
    <Controller
      control={control}
      name="email"
      render={({ field: { onChange, onBlur, value } }) => (
        <Input
          label={t('fields.email')}
          value={value}
          onChangeText={onChange}
          onBlur={onBlur}
          error={errors.email?.message ? t(errors.email.message) : undefined}
        />
      )}
    />
  );
}
```

---

### TypeScript

```typescript
// No any types - ever
const data: Product[] = response.data;    // CORRECT
const data: any = response.data;          // WRONG

// Type-only imports
import type { Product } from '../types';
import type { ButtonProps } from '@/common/components/Button';

// Named exports in src/
export function MyComponent() {}            // CORRECT
export default function MyComponent() {}    // WRONG (in src/)

// Default exports in app/ (Expo Router)
export default function HomeScreen() {}    // CORRECT
```

---

### Feature Module Structure

```
src/features/<feature>/
├── components/      Feature-specific UI components
├── services/        Pure async API functions (no React, no hooks)
├── hooks/           useQuery, useMutation, custom hooks
├── stores/          Zustand stores (only if needed)
├── types/           TypeScript types and interfaces
├── schemas/         Zod validation schemas
└── constants/       Constants (not magic numbers)
```

---

### Routing

```typescript
import { router, useLocalSearchParams } from 'expo-router';

// Navigation
router.push('/products');
router.push({ pathname: '/products/[id]', params: { id: product.id } });
router.replace('/(auth)/login');
router.back();

// Params in a screen
const { id } = useLocalSearchParams<{ id: string }>();
```

---

### Storage

```typescript
import { useStorage, useStorageBoolean } from '@/utils/storage';
import { getItem, setItem } from '@/utils/storage';
import { STORAGE_KEYS } from '@/utils/storage/constants';

// React hook
const { value, setValue, removeValue } = useStorage<string>(STORAGE_KEYS.preferences.language);
const { value: isDark, toggle } = useStorageBoolean(STORAGE_KEYS.preferences.theme);

// Non-React context
const result = getItem<string>(STORAGE_KEYS.preferences.language);
if (result.success && result.data) {
  // safe to use result.data
}
```

---

### Accessibility

Every interactive element must have:
```typescript
<Pressable
  accessibilityRole="button"
  accessibilityLabel={t('actions.submit')}
  accessibilityState={{ disabled: isDisabled, busy: isLoading }}
>
```

---

### Git Commit Format

```
<type>(<scope>): <subject>

Valid types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
```

---

## Quick Reference: Theme Tokens

```
Background:    theme.colors.background.app / .surface / .surfaceAlt / .input / .modal / .elevated
Text:          theme.colors.text.primary / .secondary / .tertiary / .muted / .inverse / .accent / .link
Brand:         theme.colors.brand.primary(#6366F1) / .secondary(#1E293B) / .tertiary(#14B8A6)
Border:        theme.colors.border.default / .subtle / .strong / .focus / .disabled
Icon:          theme.colors.icon.primary / .secondary / .muted / .inverse / .accent
State:         theme.colors.state.success / .successBg / .error / .errorBg / .warning / .info
Overlay:       theme.colors.overlay.modal / .pressed / .hover / .focus
Mode:          theme.colors.mode ('light' | 'dark')

Spacing H:     theme.metrics.spacing.p4/.p8/.p12/.p16/.p20/.p24/.p32/.p48/.p64/.p120
Spacing V:     theme.metrics.spacingV.p4/.p8/... (same keys)
Border Radius: theme.metrics.borderRadius.xs(4)/sm(6)/md(8)/lg(12)/xl(16)/full(999)
Icon Size:     theme.metrics.iconSize.xs(14)/sm(16)/md(18)/lg(20)/xl(24)
Font Size:     theme.fonts.size.xxs/xs/sm/md/lg/xl/2xl/3xl/4xl/5xl/6xl
```

---

## Things That Will Break the App

1. `import { StyleSheet } from 'react-native'` - breaks theming
2. Inline styles - bypasses theme, breaks dark mode
3. Color literals - breaks dark mode
4. Hardcoded UI strings - breaks AR translation
5. `any` types - TypeScript strict mode will fail type-check
6. `import { z } from 'zod'` - wrong version, must be `zod/v4`
7. `useMyStore()` without selector - performance issue and lint error
8. Creating React Context for auth - duplicates state, creates inconsistency
9. `export default` in `src/` component files - inconsistency
10. Not updating `ar.json` when adding to `en.json` - broken Arabic UI

---

## Template Migration

When adapting this template for a specific app:

1. Follow `docs/MIGRATION.md` for the complete step-by-step migration guide covering app identity, theme, i18n, backend, auth, navigation, and deployment
