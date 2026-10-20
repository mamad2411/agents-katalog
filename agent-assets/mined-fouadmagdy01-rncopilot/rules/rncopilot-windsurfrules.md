# Windsurf Rules - React Native Expo Template

You are working in a production-grade React Native Expo template. These rules are absolute. Violating any of them will break the app.

## Technology Stack

- React Native 0.83.2 + Expo SDK 55
- expo-router (file-based, typed routes)
- TypeScript 5.9 (strict mode enabled)
- react-native-unistyles 3.x (theming and styles)
- @tanstack/react-query (server/async state)
- Zustand (client/UI state)
- Supabase (auth + database, graceful degradation)
- Axios API client with interceptors (`@/services/api`)
- react-i18next with EN + AR locales + RTL
- react-native-mmkv (persistent storage)
- react-hook-form + zod/v4 (forms and validation)

**Path aliases:** `@/*` → `src/*` | `~/*` → `app/*`

---

## Rule 1: Styling

### Import StyleSheet from react-native-unistyles

```typescript
// CORRECT
import { StyleSheet, useUnistyles } from 'react-native-unistyles';

// WRONG - never import StyleSheet from react-native
import { StyleSheet } from 'react-native';
```

### Always use the theme callback

```typescript
// CORRECT
const styles = StyleSheet.create((theme) => ({
  container: {
    padding: theme.metrics.spacing.p16,
    paddingVertical: theme.metrics.spacingV.p24,
    backgroundColor: theme.colors.background.surface,
    borderRadius: theme.metrics.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.border.default,
    gap: theme.metrics.spacingV.p12,
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
}));

// WRONG - no theme callback
const styles = StyleSheet.create({
  container: { padding: 16, backgroundColor: '#fff' },
});
```

### No inline styles. No color literals. No hardcoded numbers.

```typescript
// ALL WRONG
<View style={{ padding: 16 }}>
<View style={{ backgroundColor: '#FFFFFF' }}>
<View style={{ backgroundColor: 'white' }}>
<Text style={{ color: '#6366F1' }}>

// ALL CORRECT
<View style={styles.container}>   {/* defined in StyleSheet.create((theme) => ...) */}
```

### Responsive helpers

```typescript
import { rf, hs, vs } from '@/theme/metrics';
// rf(n) - responsive font, hs(n) - horizontal scale, vs(n) - vertical scale
// Use these for dynamic values not available as theme tokens
```

---

## Rule 2: Components

Use project components. Full list in `src/common/components/`.

```typescript
// Text - always the project component, never React Native Text for UI
import { Text } from '@/common/components/Text';
// Variants: h1, h2, h3, body, bodySmall, caption, label, overline
<Text variant="h2">{t('section.title')}</Text>
<Text variant="body" color={theme.colors.text.secondary}>{t('section.body')}</Text>

// Button
import { Button } from '@/common/components/Button';
// Variants: primary, secondary, outline, ghost | Sizes: sm, md, lg
<Button title={t('actions.submit')} variant="primary" loading={isPending} onPress={fn} />
<Button title={t('actions.cancel')} variant="ghost" fullWidth onPress={fn} />

// Icon - Ionicons names only
import { Icon } from '@/common/components/Icon';
// Variants: primary, secondary, tertiary, muted, inverse, accent
<Icon name="settings-outline" variant="primary" size={20} />

// ScreenContainer - root of every screen
import { ScreenContainer } from '@/common/components/ScreenContainer';
<ScreenContainer scrollable padded edges={['top', 'bottom']}>

// Card
import { Card } from '@/common/components/Card';
<Card variant="elevated">  {/* default, elevated, outlined */}

// Input with validation
import { Input } from '@/common/components/Input';
<Input label={t('fields.email')} error={err ? t(err) : undefined} leftIcon={<Icon name="mail-outline" />} />

// EmptyState - for empty lists
import { EmptyState } from '@/common/components/EmptyState';
<EmptyState title={t('list.empty')} actionLabel={t('actions.refresh')} onAction={refetch} />

// Loading
import { Loading } from '@/common/components/Loading';
<Loading fullScreen message={t('common.loading')} />

// ErrorBoundary - wrap risky subtrees
import { ErrorBoundary } from '@/common/components/ErrorBoundary';
<ErrorBoundary><MyComponent /></ErrorBoundary>

// Dialog - confirmations
import { Dialog } from '@/common/components/Dialog';
<Dialog visible={show} onDismiss={close} title={t('dialog.title')}
  actions={[{ label: t('actions.cancel'), onPress: close }, { label: t('actions.confirm'), onPress: confirm }]} />

// Snackbar - toast messages
import { Snackbar } from '@/common/components/Snackbar';
<Snackbar visible={show} message={t('messages.saved')} variant="success" onDismiss={close} />
```

Import ALWAYS from barrels: `@/common/components/Button` not `@/common/components/Button/Button`.

---

## Rule 3: i18n

All user-visible text goes through `useTranslation`. No exceptions.

```typescript
const { t } = useTranslation();

// CORRECT
<Text variant="h1">{t('home.title')}</Text>
<Button title={t('actions.save')} />
placeholder={t('fields.emailPlaceholder')}

// WRONG
<Text variant="h1">Home</Text>
<Button title="Save" />
```

When adding translation keys, always update BOTH:
- `src/i18n/locales/en.json`
- `src/i18n/locales/ar.json`

Zod error messages use i18n keys:
```typescript
z.string().min(1, 'validation.required')  // key, not 'This field is required'
```

---

## Rule 4: Auth

Auth state lives exclusively in Zustand. Never create React Context for auth.

```typescript
import { useAuthStore } from '@/providers/auth/authStore';

// In React components - selector only
const user = useAuthStore((s) => s.user);
const session = useAuthStore((s) => s.session);
const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
const isLoading = useAuthStore((s) => s.isLoading);

// Outside React (Axios interceptors, service functions)
const session = useAuthStore.getState().session;
const clearSession = useAuthStore.getState().clearSession;
```

For protected screens:
```typescript
import { useProtectedRoute } from '@/hooks/useProtectedRoute';
export default function DashboardScreen() {
  useProtectedRoute(); // redirects to /(auth)/login if not authenticated
  return <ScreenContainer>{/* ... */}</ScreenContainer>;
}
```

---

## Rule 5: State Management

```typescript
// Zustand - always use selectors
const items = useMyStore((s) => s.items);           // CORRECT
const addItem = useMyStore((s) => s.addItem);
const { items, addItem } = useMyStore();             // WRONG - whole store subscription

// Zustand store pattern
import { create } from 'zustand';
export const useMyStore = create<MyState>((set, get) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({ items: state.items.filter((i) => i.id !== id) })),
  reset: () => set({ items: [] }),
}));

// React Query for server state
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

export function useItems() {
  return useQuery({
    queryKey: ['items'],
    queryFn: () => api.get<Item[]>('/items').then((r) => r.data),
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateItemData) => api.post<Item>('/items', data).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['items'] }),
  });
}
```

---

## Rule 6: API

```typescript
import { api } from '@/services/api';
// Bearer token auto-attached. 401 auto-clears session. Errors normalized.

// Place all service functions in src/features/<feature>/services/
export async function fetchItems(): Promise<Item[]> {
  const { data } = await api.get<Item[]>('/items');
  return data;
}
```

---

## Rule 7: Forms

```typescript
import { z } from 'zod/v4';  // zod/v4 NOT zod
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.email('validation.emailInvalid'),
  name: z.string().min(1, 'validation.required'),
  age: z.number().min(18, 'validation.ageMin'),
});

type FormData = z.infer<typeof schema>;

const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { email: '', name: '' },
});
```

---

## Rule 8: TypeScript

```typescript
// No any types
const data: Product = response.data;   // CORRECT
const data: any = response.data;       // WRONG

// Type-only imports
import type { Product } from '../types';

// Exports in src/ - named, not default
export function MyComponent() {}        // CORRECT
export default function MyComponent() {} // WRONG

// app/ screens - default only (Expo Router requirement)
export default function HomeScreen() {} // CORRECT
```

---

## Rule 9: Storage

```typescript
import { useStorage, useStorageBoolean } from '@/utils/storage';
import { STORAGE_KEYS } from '@/utils/storage/constants';

const { value, setValue } = useStorage<string>(STORAGE_KEYS.preferences.language);
const { value: isDark, toggle } = useStorageBoolean(STORAGE_KEYS.preferences.theme);

// Non-React: check result.success
import { getItem, setItem } from '@/utils/storage';
const result = getItem<string>(STORAGE_KEYS.preferences.language);
if (result.success && result.data) { /* safe to use result.data */ }
```

---

## Feature Module Pattern

```
src/features/<feature>/
├── components/     Feature UI (e.g., ProductCard.tsx)
├── services/       Pure async functions (e.g., productService.ts)
├── hooks/          Query + custom hooks (e.g., useProducts.ts)
├── stores/         Zustand stores (only if needed)
├── types/          TypeScript interfaces
├── schemas/        Zod schemas
└── constants/      Constants
```

---

## Routing

```typescript
import { router } from 'expo-router';
import { useLocalSearchParams, useRouter, Link } from 'expo-router';

router.push('/products');
router.push({ pathname: '/products/[id]', params: { id: item.id } });
router.replace('/(auth)/login');
router.back();

const { id } = useLocalSearchParams<{ id: string }>();
```

---

## Commit Format

```
<type>(<scope>): <subject>
feat | fix | docs | style | refactor | perf | test | build | ci | chore | revert
```

---

## Absolute Prohibitions

| Never Do | Do Instead |
|----------|-----------|
| `import { StyleSheet } from 'react-native'` | `import { StyleSheet } from 'react-native-unistyles'` |
| `style={{ padding: 16 }}` | `style={styles.container}` |
| `color: '#6366F1'` | `color: theme.colors.brand.primary` |
| `<Text>Hello</Text>` | `<Text>{t('key.here')}</Text>` |
| `any` types | Proper TypeScript types |
| React Context for auth | `useAuthStore` from Zustand |
| `useStore()` | `useStore((s) => s.field)` |
| `import { z } from 'zod'` | `import { z } from 'zod/v4'` |
| `export default function MyComponent()` in `src/` | `export function MyComponent()` |
| `fetch('/api/...')` | `api.get('/...')` from `@/services/api` |
| `../../common/components` | `@/common/components` |
| `console.log(...)` in prod | `if (__DEV__) { console.log(...) }` |

---

## Template Migration

When adapting this template for a specific app (e-commerce, games, social, etc.):

1. Follow `docs/MIGRATION.md` for the complete step-by-step guide
