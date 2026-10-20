# GitHub Copilot Instructions

React Native Expo template. Follow these rules for every suggestion.

## Stack

React Native 0.83.2, Expo SDK 55, expo-router, TypeScript 5.9 strict, react-native-unistyles 3.x, TanStack Query, Zustand, Supabase, Axios, react-i18next (EN+AR), react-native-mmkv, react-hook-form, zod/v4.

Path aliases: `@/*` = `src/*`, `~/*` = `app/*`

---

## Styling Rules

- Import `StyleSheet` from `react-native-unistyles`, never from `react-native`
- Always use the theme callback: `StyleSheet.create((theme) => ({ ... }))`
- Never inline styles: no `style={{ padding: 16 }}`
- Never color literals: no `color: '#6366F1'` or `backgroundColor: 'white'`
- Never hardcoded spacing: use `theme.metrics.spacing.p16` not `padding: 16`

```typescript
import { StyleSheet } from 'react-native-unistyles';

const styles = StyleSheet.create((theme) => ({
  container: {
    padding: theme.metrics.spacing.p16,
    backgroundColor: theme.colors.background.surface,
    borderRadius: theme.metrics.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.border.default,
  },
  title: {
    fontSize: theme.fonts.size.lg,
    color: theme.colors.text.primary,
  },
}));
```

---

## Components

Use project components, not React Native primitives where a project component exists.

```typescript
// Text - use project Text, not RN Text
import { Text } from '@/common/components/Text';
<Text variant="h1">{t('home.title')}</Text>
<Text variant="body" color={theme.colors.text.secondary}>{t('home.body')}</Text>
// Variants: h1, h2, h3, body, bodySmall, caption, label, overline

// Button
import { Button } from '@/common/components/Button';
<Button title={t('actions.submit')} variant="primary" size="md" onPress={fn} loading={isPending} />
// Variants: primary, secondary, outline, ghost | Sizes: sm, md, lg

// Icon (Ionicons names)
import { Icon } from '@/common/components/Icon';
<Icon name="home-outline" variant="primary" size={20} />
// Variants: primary, secondary, tertiary, muted, inverse, accent

// Screen root
import { ScreenContainer } from '@/common/components/ScreenContainer';
<ScreenContainer scrollable padded>{/* content */}</ScreenContainer>

// Card
import { Card } from '@/common/components/Card';
<Card variant="elevated" pressable onPress={fn}>{/* content */}</Card>
// Variants: default, elevated, outlined

// Input
import { Input } from '@/common/components/Input';
<Input label={t('fields.email')} value={val} onChangeText={fn} error={err ? t(err) : undefined} />
```

Import from barrels: `@/common/components/Button` not `@/common/components/Button/Button`.

---

## i18n - Required for Every String

```typescript
const { t } = useTranslation();

// CORRECT
<Text>{t('home.welcome')}</Text>
<Button title={t('actions.save')} />

// WRONG
<Text>Welcome</Text>
<Button title="Save" />
```

When adding keys, update both:

- `src/i18n/locales/en.json`
- `src/i18n/locales/ar.json`

Zod validation messages use i18n keys:

```typescript
z.string().min(1, 'validation.required'); // key, not raw text
```

---

## Auth

```typescript
import { useAuthStore } from '@/providers/auth/authStore';

// Always use selectors in components
const user = useAuthStore((s) => s.user);
const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

// Outside React (interceptors, utilities)
const session = useAuthStore.getState().session;
```

Never create a React Context for auth.

---

## State Management

```typescript
// Zustand for client state - always use selectors
const items = useMyStore((s) => s.items); // CORRECT
const { items } = useMyStore(); // WRONG

// Store pattern
export const useMyStore = create<MyState>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
}));

// React Query for server state
export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => api.get<Product[]>('/products').then((r) => r.data),
  });
}
```

---

## API

```typescript
import { api } from '@/services/api';
// Auto-attaches Bearer token, handles 401, normalizes errors

const products = await api.get<Product[]>('/products').then((r) => r.data);
const product = await api.post<Product>('/products', data).then((r) => r.data);
```

---

## Forms

```typescript
import { z } from 'zod/v4';    // zod/v4, not zod
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { FormField } from '@/common/components/FormField';
import { Input } from '@/common/components/Input';

const schema = z.object({
  email: z.email('validation.emailInvalid'),
  password: z.string().min(8, 'validation.passwordMin'),
});

const { control, handleSubmit } = useForm({
  resolver: zodResolver(schema),
  defaultValues: { email: '', password: '' },
});

// Use FormField instead of raw Controller
<FormField name="email" control={control} label={t('fields.email')} required>
  <Input keyboardType="email-address" autoCapitalize="none" />
</FormField>
```

---

## Exports

```typescript
// Named exports in src/ always
export function MyComponent() {} // CORRECT
export default function MyComponent() {} // WRONG (except app/ screens)

// app/ screens require default (Expo Router)
export default function HomeScreen() {} // CORRECT
```

---

## Never Do

- `import { StyleSheet } from 'react-native'`
- Inline styles: `style={{ padding: 16 }}`
- Color literals: `color: '#fff'`
- Hardcoded UI text: `<Text>Hello</Text>`
- `any` types
- `import { z } from 'zod'` (must be `zod/v4`)
- `useMyStore()` without selector
- React Context for auth
- `fetch()` directly (use `api` from `@/services/api`)
- Relative paths climbing 2+ levels
- `export default` in `src/` component files
- `console.log` in production code

---

## Template Migration

Follow `docs/MIGRATION.md` for the step-by-step migration guide.
