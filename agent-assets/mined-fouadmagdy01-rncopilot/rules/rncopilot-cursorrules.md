# Cursor Rules - React Native Expo Template

You are an expert React Native developer working in a production-grade Expo template. Follow every rule below exactly. When in doubt, look at an existing file and match its patterns.

## Stack
- React Native 0.83.2 + Expo SDK 55
- expo-router (file-based routing, typed)
- TypeScript 5.9 strict mode
- react-native-unistyles 3.x (styling)
- @tanstack/react-query (server state)
- Zustand (client state)
- Supabase (auth + database, graceful degradation)
- Axios with auth interceptors
- react-i18next (EN/AR, RTL support)
- react-native-mmkv (storage)
- react-hook-form + Zod (forms)
- ESLint 9 flat config

## Path Aliases
- `@/*` → `src/*`
- `~/*` → `app/*`

Always use these aliases. Never use relative paths that climb more than one level.

---

## Styling - THE MOST IMPORTANT RULES

1. ALWAYS import StyleSheet from react-native-unistyles, NOT from react-native:
   ```typescript
   import { StyleSheet } from 'react-native-unistyles';  // CORRECT
   import { StyleSheet } from 'react-native';             // WRONG
   ```

2. ALWAYS use the theme callback form:
   ```typescript
   const styles = StyleSheet.create((theme) => ({  // CORRECT
     container: { padding: theme.metrics.spacing.p16 }
   }));

   const styles = StyleSheet.create({  // WRONG - no theme access
     container: { padding: 16 }
   });
   ```

3. NEVER use inline styles:
   ```typescript
   <View style={{ padding: 16 }}>           // WRONG
   <View style={styles.container}>          // CORRECT
   ```

4. NEVER use color literals:
   ```typescript
   color: '#6366F1'                          // WRONG
   color: theme.colors.brand.primary         // CORRECT
   backgroundColor: 'white'                 // WRONG
   backgroundColor: theme.colors.background.surface  // CORRECT
   ```

5. NEVER hardcode spacing numbers:
   ```typescript
   padding: 16                              // WRONG
   padding: theme.metrics.spacing.p16       // CORRECT
   ```

## Theme Token Reference

```
theme.colors.brand.primary          - #6366F1 indigo (main brand)
theme.colors.brand.secondary        - #1E293B dark slate
theme.colors.brand.tertiary         - #14B8A6 teal accent
theme.colors.background.app         - page/screen background
theme.colors.background.surface     - cards, sheets
theme.colors.background.input       - text input background
theme.colors.background.modal       - modal background
theme.colors.text.primary           - main text
theme.colors.text.secondary         - supporting text
theme.colors.text.muted             - placeholder, hints
theme.colors.text.inverse           - text on dark/primary bg
theme.colors.text.accent            - teal accent text
theme.colors.border.default         - standard border
theme.colors.border.focus           - input focus ring
theme.colors.icon.primary           - icon color (primary)
theme.colors.icon.muted             - subtle icon
theme.colors.state.success          - #10B981 green
theme.colors.state.error            - #EF4444 red
theme.colors.state.warning          - #F59E0B amber
theme.colors.state.info             - #3B82F6 blue
theme.colors.overlay.modal          - rgba black 0.5
theme.colors.overlay.pressed        - rgba indigo 0.12
theme.colors.mode                   - 'light' | 'dark'

theme.metrics.spacing.p4/p8/p12/p16/p20/p24/p32/p48/p64  (horizontal)
theme.metrics.spacingV.p4/.p8/...                          (vertical)
theme.metrics.borderRadius.xs/sm/md/lg/xl/full
theme.metrics.iconSize.xs/sm/md/lg/xl
theme.fonts.size.xxs/xs/sm/md/lg/xl/2xl/3xl/4xl/5xl/6xl
```

Responsive helpers (import from @/theme/metrics):
```typescript
rf(16)  // responsive font size
hs(20)  // horizontal scale
vs(24)  // vertical scale
```

---

## Components

### Text Component

ALWAYS use the project's Text component for user-facing text, NOT React Native's Text:
```typescript
import { Text } from '@/common/components/Text';  // CORRECT
import { Text } from 'react-native';               // WRONG for UI text

<Text variant="h1">Title</Text>
<Text variant="body" color={theme.colors.text.secondary}>Body</Text>
```

Variants: h1, h2, h3, body, bodySmall, caption, label, overline

### Button Component
```typescript
import { Button } from '@/common/components/Button';

<Button title={t('actions.submit')} variant="primary" size="md" onPress={fn} />
<Button title={t('actions.cancel')} variant="ghost" loading={isPending} />
<Button title={t('actions.share')} variant="outline" leftIcon={<Icon name="share-outline" />} />
```
Variants: primary, secondary, outline, ghost
Sizes: sm, md, lg

### Icon Component
```typescript
import { Icon } from '@/common/components/Icon';
// Name is from Ionicons - always use "-outline" suffix for line icons
<Icon name="home-outline" variant="primary" size={20} />
<Icon name="alert-circle-outline" variant="accent" />
```
Variants: primary, secondary, tertiary, muted, inverse, accent

### ScreenContainer - Use for every screen root
```typescript
import { ScreenContainer } from '@/common/components/ScreenContainer';
<ScreenContainer scrollable padded>
  {/* screen content */}
</ScreenContainer>
```

### All 33 Components (import from @/common/components/*)
Action: Button, IconButton
Data Display: Avatar, Badge, Card, Chip, ListItem, Text
Disclosure: Accordion
Feedback: EmptyState, ErrorBoundary, Loading, ProgressBar, Skeleton, Snackbar
Form: Checkbox, FormField, Input, RadioGroup, SearchBar, SegmentedControl, Select, Switch, TextArea
Layout: Divider, ScreenContainer
Overlay: Dialog, Menu
Typography: Icon

---

## Internationalization - HARD RULES

1. EVERY user-facing string MUST use useTranslation:
   ```typescript
   const { t } = useTranslation();
   <Text>{t('home.welcome')}</Text>         // CORRECT
   <Text>Welcome</Text>                     // WRONG
   ```

2. When adding new text, update BOTH files:
   - src/i18n/locales/en.json
   - src/i18n/locales/ar.json

3. Translation keys use dot notation: 'feature.subKey'

4. Validation messages in Zod schemas are i18n keys:
   ```typescript
   z.string().min(1, 'validation.required')  // CORRECT - key, not text
   z.string().min(1, 'Required')             // WRONG - raw text
   ```

---

## State Management

### Auth State - Zustand ONLY
```typescript
import { useAuthStore } from '@/providers/auth/authStore';

// In React components - use selectors
const user = useAuthStore((s) => s.user);
const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

// Outside React (Axios interceptors, etc.)
const session = useAuthStore.getState().session;
```

NEVER create a React Context for auth. The Zustand store IS the auth layer.

### Zustand Store Pattern
```typescript
import { create } from 'zustand';

interface MyState {
  items: MyItem[];
  addItem: (item: MyItem) => void;
  reset: () => void;
}

export const useMyStore = create<MyState>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  reset: () => set({ items: [] }),
}));

// Usage - always use selectors
const items = useMyStore((s) => s.items);      // CORRECT
const store = useMyStore();                     // WRONG - subscribes to everything
```

### React Query Pattern
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

// Query key factories
export const MY_KEYS = {
  all: ['myItems'] as const,
  list: () => [...MY_KEYS.all, 'list'] as const,
  detail: (id: string) => [...MY_KEYS.all, 'detail', id] as const,
};

export function useMyItems() {
  return useQuery({
    queryKey: MY_KEYS.list(),
    queryFn: () => api.get<MyItem[]>('/items').then((r) => r.data),
  });
}
```

---

## Forms

```typescript
import { z } from 'zod/v4';  // NOTE: zod/v4 not zod

const schema = z.object({
  email: z.email('validation.emailInvalid'),
  password: z.string().min(8, 'validation.passwordMin'),
});

type FormData = z.infer<typeof schema>;

const { control, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { email: '', password: '' },
});
```

---

## File and Component Conventions

### Named exports for everything in src/
```typescript
export function MyComponent() { }  // CORRECT
export default function MyComponent() { }  // WRONG (except app/ screens)
```

### Default exports only in app/ (Expo Router requires it)
```typescript
// app/(main)/(tabs)/home.tsx
export default function HomeScreen() { }  // CORRECT - Expo Router needs default
```

### Component directory structure
```
ComponentName/
├── ComponentName.tsx
├── ComponentName.types.ts   (optional)
├── ComponentName.styles.ts  (optional)
└── index.ts                 (required - barrel export)
```

### Import from barrels
```typescript
import { Button } from '@/common/components/Button';  // CORRECT
import { Button } from '@/common/components/Button/Button';  // WRONG
```

### Type imports
```typescript
import type { ButtonProps } from '@/common/components/Button';  // CORRECT
import { ButtonProps } from '@/common/components/Button';       // WRONG for type-only
```

---

## API Client

```typescript
import { api } from '@/services/api';

// The client auto-attaches Bearer token and handles 401
const data = await api.get<Product[]>('/products');
const product = await api.post<Product>('/products', payload);
```

Never call fetch() directly. Never use a different HTTP client.

---

## Expo Router

```typescript
import { router } from 'expo-router';
import { useLocalSearchParams } from 'expo-router';

router.push('/products');
router.push({ pathname: '/products/[id]', params: { id: '123' } });
router.replace('/(auth)/login');
router.back();

// In a screen
const { id } = useLocalSearchParams<{ id: string }>();
```

---

## Storage

```typescript
import { useStorage, useStorageBoolean } from '@/utils/storage';
import { STORAGE_KEYS } from '@/utils/storage/constants';

const { value, setValue } = useStorage<string>(STORAGE_KEYS.preferences.language);
const { value: isDark, toggle } = useStorageBoolean(STORAGE_KEYS.preferences.theme);

// Non-React context
import { getItem, setItem } from '@/utils/storage';
const result = getItem<string>(STORAGE_KEYS.preferences.language);
if (result.success && result.data) { /* use result.data */ }
```

---

## Feature Module Structure

```
src/features/<feature>/
├── components/    # Feature UI components
├── services/      # Pure async API functions (no React)
├── hooks/         # React Query hooks + custom hooks
├── stores/        # Zustand stores (if needed)
├── types/         # TypeScript types
├── schemas/       # Zod schemas
└── constants/     # Constants
```

---

## Accessibility Requirements

Every interactive element MUST have:
```typescript
<Pressable
  accessibilityRole="button"
  accessibilityLabel={t('actions.submit')}
  accessibilityState={{ disabled, busy: loading }}
>
```

---

## Git Commits

Format: `<type>(<scope>): <subject>`

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

Examples:
```
feat(auth): add forgot password screen
fix(button): correct disabled state in dark mode
test(input): add error state tests
```

---

## NEVER DO

- `import { StyleSheet } from 'react-native'` (use react-native-unistyles)
- Inline styles: `style={{ padding: 16 }}`
- Color literals: `color: '#6366F1'`
- Hardcoded UI strings: `<Text>Hello</Text>`
- `any` types
- React Context for auth
- `useMyStore()` without a selector function
- `import { Button } from '@/common/components/Button/Button'` (use barrel)
- `import { z } from 'zod'` (use `zod/v4`)
- `export default` from component files in `src/`
- Direct `fetch()` calls (use `api` from `@/services/api`)
- Relative paths that climb multiple levels: `../../../components`
- Hardcoded spacing: `padding: 16` (use `theme.metrics.spacing.p16`)
- `console.log` in production (use `if (__DEV__) { console.log(...) }`)

---

## Template Migration

When adapting this template for a specific app, follow `docs/MIGRATION.md` for the complete step-by-step guide.
