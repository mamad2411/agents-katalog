---
name: tpl-frontend-react-native-expo
description: Template do pack (frontend/07-react-native-expo.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/07-react-native-expo.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App Mobile]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/07-react-native-expo.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — React Native + Expo SDK 52 + TypeScript
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Mobile | React Native + Expo | SDK 52 |
| Linguagem | TypeScript | 5.x (strict) |
| Routing | Expo Router | v4 (file-based) |
| Server State | TanStack Query | v5 |
| Client State | Zustand | v5 |
| Styling | NativeWind (Tailwind for RN) | v4 |
| Forms | React Hook Form + Zod | latest |
| Storage | Expo SecureStore + AsyncStorage | latest |
| Tests | Jest + React Native Testing Library | latest |

---

## FILE STRUCTURE

```
app/                       # Expo Router file-based routing
├── (auth)/                # Auth route group (login, register)
│   ├── _layout.tsx        # Stack navigator for auth screens
│   ├── login.tsx
│   └── register.tsx
├── (tabs)/                # Main app with bottom tabs
│   ├── _layout.tsx        # Tab navigator config
│   ├── index.tsx          # Home tab
│   ├── search.tsx         # Search tab
│   └── profile.tsx        # Profile tab
├── [id].tsx               # Dynamic route: /123
├── _layout.tsx            # Root layout (providers, auth redirect)
└── +not-found.tsx         # 404 screen

components/
├── ui/                    # Base: Button, Input, Card, Avatar
└── features/              # Feature-specific components

hooks/                     # Custom hooks (useAuth, usePermissions)
stores/                    # Zustand stores
lib/
├── api.ts                 # Axios instance with auth interceptor
├── storage.ts             # SecureStore wrapper
└── query-client.ts        # TanStack Query config
```

---

## MENTAL MODEL — Expo Router Navigation

```typescript
// app/_layout.tsx — Root layout (providers + auth redirect)
import { Stack, useRouter, useSegments } from 'expo-router';
import { useEffect } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from '@/stores/auth.store';
import { queryClient } from '@/lib/query-client';

export default function RootLayout() {
  const { isAuthenticated } = useAuthStore();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    const inAuthGroup = segments[0] === '(auth)';

    if (!isAuthenticated && !inAuthGroup) {
      router.replace('/(auth)/login');
    } else if (isAuthenticated && inAuthGroup) {
      router.replace('/(tabs)');
    }
  }, [isAuthenticated, segments]);

  return (
    <QueryClientProvider client={queryClient}>
      <Stack screenOptions={{ headerShown: false }} />
    </QueryClientProvider>
  );
}
```

---

## NATIVE vs WEB DIFFERENCES

| Web | React Native | Solution |
|-----|-------------|----------|
| `<div>` | `<View>` | Always use RN primitives |
| `<p>`, `<span>` | `<Text>` | ALL text MUST be inside `<Text>` |
| `onClick` | `onPress` | Use `<Pressable>` (not TouchableOpacity) |
| CSS `gap` | `gap` (RN 0.71+) | Works in modern Expo |
| `overflow: scroll` | `<ScrollView>` / `<FlashList>` | Use FlashList for >50 items |
| localStorage | SecureStore / AsyncStorage | SecureStore for tokens, AsyncStorage for prefs |
| CSS animations | `react-native-reanimated` | For performant 60fps animations |

---

## SECURE STORAGE PATTERN

```typescript
// lib/storage.ts
import * as SecureStore from 'expo-secure-store';

export const secureStorage = {
  async get(key: string): Promise<string | null> {
    return await SecureStore.getItemAsync(key);
  },
  async set(key: string, value: string): Promise<void> {
    await SecureStore.setItemAsync(key, value);
  },
  async delete(key: string): Promise<void> {
    await SecureStore.deleteItemAsync(key);
  },
};

// SECURITY: NEVER use AsyncStorage for tokens, API keys, or credentials
// AsyncStorage is NOT encrypted — use SecureStore for anything sensitive
```

---

## LIST PERFORMANCE — FlashList

```typescript
// components/features/UserList.tsx
import { FlashList } from '@shopify/flash-list';

export function UserList({ users }: { users: User[] }) {
  return (
    <FlashList
      data={users}
      estimatedItemSize={72}
      renderItem={({ item }) => <UserRow user={item} />}
      keyExtractor={(item) => item.id}
      ItemSeparatorComponent={() => <View style={{ height: 1, backgroundColor: '#e5e7eb' }} />}
      ListEmptyComponent={<EmptyState message="Nenhum usuário encontrado" />}
    />
  );
}

// RULES:
// - FlashList for >50 items (FlatList is OK for <50)
// - ALWAYS set estimatedItemSize
// - NEVER use ScrollView for dynamic lists
```

---

## PERMISSIONS PATTERN

```typescript
// hooks/useCamera.ts
import * as ImagePicker from 'expo-image-picker';
import { Alert, Linking } from 'react-native';

export function useCamera() {
  async function pickImage() {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();

    if (status !== 'granted') {
      Alert.alert(
        'Permissão necessária',
        'Precisamos de acesso à câmera para esta funcionalidade.',
        [
          { text: 'Cancelar', style: 'cancel' },
          { text: 'Configurações', onPress: () => Linking.openSettings() },
        ]
      );
      return null;
    }

    return await ImagePicker.launchCameraAsync({
      quality: 0.8,
      allowsEditing: true,
      aspect: [1, 1],
    });
  }

  return { pickImage };
}
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New screen | `app/(group)/screen.tsx` → add to `_layout.tsx` if in tabs |
| Auth flow | Root `_layout.tsx` redirect based on `useAuthStore` state |
| API call | TanStack Query hook in `hooks/use{Resource}.ts` |
| Native feature | Check Expo SDK FIRST → Expo plugin for native modules |
| Performance | FlashList, `useMemo`, avoid inline functions in render item |
| Deep link | Configure `app.json` → `scheme` + `expo-linking` |
| Push notifications | `expo-notifications` + register token → send to API |

---

## TESTING PATTERNS

```typescript
// __tests__/LoginScreen.test.tsx
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import LoginScreen from '../app/(auth)/login';

jest.mock('@/stores/auth.store', () => ({
  useAuthStore: () => ({
    login: jest.fn().mockResolvedValue(undefined),
    isAuthenticated: false,
  }),
}));

test('shows validation error for empty email', async () => {
  const { getByText, getByPlaceholderText } = render(<LoginScreen />);
  fireEvent.press(getByText('Entrar'));
  await waitFor(() => {
    expect(getByText('Email inválido')).toBeTruthy();
  });
});
```

---

## ENV VARS (app.json + eas.json)

```json
// app.json extra
{
  "expo": {
    "extra": {
      "apiUrl": "https://api.myapp.com",
      "eas": { "projectId": "..." }
    }
  }
}
```

## BUILD COMMANDS

```bash
npx expo start              # Dev server
npx expo start --clear      # Dev with cache clear
eas build --platform ios --profile preview     # iOS preview
eas build --platform android --profile preview # Android preview
eas build --platform all --profile production  # Production build
eas submit --platform all                      # Submit to stores
npx expo install --check     # Check dependency compatibility
```

---

## QUALITY GATES

□ `npx tsc --noEmit` — 0 errors
□ `npm test` — all pass
□ No tokens in AsyncStorage (use SecureStore)
□ All lists >50 items use FlashList
□ Tested on iOS simulator AND Android emulator
□ Offline state handled gracefully
□ All permissions checked before use with graceful denial
□ App runs in Expo Go for rapid iteration

---

## FORBIDDEN

- NEVER store tokens in AsyncStorage (use SecureStore)
- NEVER use `<TouchableOpacity>` (use `<Pressable>` — more customizable)
- NEVER use `<FlatList>` for >50 items (use FlashList)
- NEVER put text outside `<Text>` component
- NEVER use CSS `vh`/`vw` units (use `Dimensions` or `useWindowDimensions`)
- NEVER hardcode API URL (use `Constants.expoConfig.extra`)
- NEVER skip permission checks before accessing camera/location/photos
