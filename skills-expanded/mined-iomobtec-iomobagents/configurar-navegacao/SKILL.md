---
name: configurar-navegacao
description: "Implementa a estrutura de rotas com Expo Router — tabs, stack, modais, autenticação com redirect e deep linking. Use quando o dev-mobile vai estruturar a navegação do app."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: configurar-navegacao

Implementa a **estrutura de rotas Expo Router** de um projeto mobile: layouts de tabs, stack, modais, autenticação com redirect e deep linking.

**Agente:** dev-mobile  
**Guardrails aplicáveis:** `mobile.md §3`, `mobile.md §9`  
**Referências rápidas:** `Guidelines/mobile/navegacao.md`

---

## Quando usar

- Para implementar a estrutura de navegação de um app novo (após `configurar-expo`)
- Para adicionar um novo grupo de rotas (novo tab, nova stack aninhada)
- Para implementar fluxo de autenticação com redirect automático
- Para configurar deep linking e rotas dinâmicas

---

## Pré-requisitos

- Projeto inicializado com `configurar-expo`
- Definição das telas e fluxos validados com o arquiteto
- Design system e especificações do dev-ui-ux disponíveis

---

## Processo de execução

### Passo 1 — Mapear a estrutura de rotas

Antes de criar arquivos, mapear o fluxo completo de navegação:

```
app/
├── _layout.tsx              ← RootLayout (providers + Stack raiz)
├── +not-found.tsx           ← 404
├── (auth)/                  ← Fluxo de autenticação (sem tabs)
│   ├── _layout.tsx
│   ├── login.tsx
│   └── register.tsx
└── (tabs)/                  ← Área autenticada com tabs
    ├── _layout.tsx
    ├── index.tsx            ← Tab principal
    ├── <tab-2>.tsx
    └── <feature>/           ← Stack aninhada dentro de um tab
        ├── _layout.tsx
        ├── index.tsx
        └── [id].tsx         ← Detalhe dinâmico
```

Confirmar com o usuário:
- Quais são os tabs principais e seus ícones?
- Há fluxo de autenticação?
- Há rotas dinâmicas (listas com detalhe)?
- Há modais?

### Passo 2 — Criar RootLayout com providers

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import { QueryClientProvider } from '@tanstack/react-query';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { queryClient } from '@/services/queryClient';
import { useAuthRedirect } from '@/hooks/useAuthRedirect';

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <QueryClientProvider client={queryClient}>
          <RootNavigator />
        </QueryClientProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

function RootNavigator() {
  useAuthRedirect();
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="(auth)" />
      <Stack.Screen name="(tabs)" />
      <Stack.Screen
        name="modal/[type]"
        options={{ presentation: 'modal', headerShown: true }}
      />
    </Stack>
  );
}
```

### Passo 3 — Implementar hook de autenticação com redirect

```typescript
// src/hooks/useAuthRedirect.ts
import { useEffect } from 'react';
import { useRouter, useSegments } from 'expo-router';
import { useAuthStore } from '@/stores/authStore';

export function useAuthRedirect() {
  const router = useRouter();
  const segments = useSegments();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const isLoading = useAuthStore((s) => s.isLoading);

  useEffect(() => {
    if (isLoading) return; // aguardar carregamento inicial

    const inAuthGroup = segments[0] === '(auth)';

    if (!isAuthenticated && !inAuthGroup) {
      router.replace('/(auth)/login');
    } else if (isAuthenticated && inAuthGroup) {
      router.replace('/(tabs)');
    }
  }, [isAuthenticated, isLoading, segments]);
}
```

### Passo 4 — Criar layout do grupo (auth)

```tsx
// app/(auth)/_layout.tsx
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function AuthLayout() {
  return (
    <>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }} />
    </>
  );
}
```

### Passo 5 — Criar layout de tabs

Substituir os nomes das tabs, ícones e labels pela definição real da feature:

```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Platform } from 'react-native';

// Importar ícones do design system aprovado
import { HomeIcon, UserIcon } from 'lucide-react-native';

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#6366f1',      // usar token do design system
        tabBarInactiveTintColor: '#94a3b8',
        tabBarStyle: {
          paddingBottom: Platform.OS === 'ios' ? 0 : 8,
        },
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Início',
          tabBarAccessibilityLabel: 'Ir para tela inicial',
          tabBarIcon: ({ color, size }) => (
            <HomeIcon color={color} size={size} aria-hidden />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Perfil',
          tabBarAccessibilityLabel: 'Ir para meu perfil',
          tabBarIcon: ({ color, size }) => (
            <UserIcon color={color} size={size} aria-hidden />
          ),
        }}
      />
    </Tabs>
  );
}
```

### Passo 6 — Criar tela 404

```tsx
// app/+not-found.tsx
import { Link, Stack } from 'expo-router';
import { View, Text, StyleSheet } from 'react-native';

export default function NotFoundScreen() {
  return (
    <>
      <Stack.Screen options={{ title: 'Página não encontrada' }} />
      <View style={styles.container} accessibilityRole="main">
        <Text style={styles.title}>Esta tela não existe.</Text>
        <Link href="/(tabs)" style={styles.link}>
          Voltar para o início
        </Link>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 20 },
  title: { fontSize: 20, fontWeight: 'bold' },
  link: { marginTop: 15, paddingVertical: 15, color: '#6366f1' },
});
```

### Passo 7 — Implementar rotas dinâmicas (quando houver)

```tsx
// app/(tabs)/orders/[id].tsx
import { useLocalSearchParams, Stack } from 'expo-router';
import { View } from 'react-native';
import { useOrder } from '@/hooks/useOrder';
import { LoadingScreen } from '@/components/LoadingScreen';
import { ErrorScreen } from '@/components/ErrorScreen';

export default function OrderDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data: order, isLoading, error, refetch } = useOrder(id);

  return (
    <>
      <Stack.Screen options={{ title: order?.number ?? 'Pedido' }} />
      {isLoading && <LoadingScreen />}
      {error && <ErrorScreen onRetry={refetch} />}
      {order && <OrderDetail order={order} />}
    </>
  );
}
```

### Passo 8 — Configurar deep linking (scheme no app.config.ts)

Confirmar que o `scheme` está definido no `app.config.ts`:

```typescript
// app.config.ts
scheme: '<slug-do-app>',   // habilita meuapp://...
```

Testar deep link manualmente:

```bash
# iOS Simulator
xcrun simctl openurl booted "<slug>://orders/123"

# Android Emulator
adb shell am start -a android.intent.action.VIEW -d "<slug>://orders/123"
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Vou usar `useNavigate` do React Navigation" | Em Expo Router, a navegação é feita via `router.push` ou `<Link>` — `useNavigate` não existe nesse contexto |
| "Posso pular o `useAuthRedirect` e fazer o redirect dentro das telas" | Redirect distribuído nas telas cria inconsistência — o hook centralizado garante comportamento uniforme |
| "O grupo `(auth)/` não é necessário, posso usar um stack direto" | O agrupamento semântico facilita manutenção e garante que o layout correto seja aplicado por contexto de autenticação |

---

## Checklist de conclusão

- [ ] `app/_layout.tsx` com todos os providers globais (QueryClient, SafeAreaProvider, GestureHandler)
- [ ] `useAuthRedirect` implementado e conectado ao AuthStore
- [ ] Grupo `(auth)/` com layout sem tabs
- [ ] Grupo `(tabs)/` com layout de tabs e ícones acessíveis
- [ ] `app/+not-found.tsx` implementado
- [ ] Rotas dinâmicas com `useLocalSearchParams` tipado
- [ ] Scheme de deep linking configurado no `app.config.ts`
- [ ] `npx expo start` navega entre telas sem erros
- [ ] `npx tsc --noEmit` passa sem erros
