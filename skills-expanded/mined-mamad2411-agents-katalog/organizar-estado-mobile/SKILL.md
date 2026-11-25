---
name: organizar-estado-mobile
description: "Decide e implementa a estratégia de estado mobile, escalando de local para Zustand e TanStack Query. Use quando o dev-mobile precisa definir onde guardar estado."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: organizar-estado-mobile

Decide e implementa a **estratégia de gerenciamento de estado** para um app React Native: estado local, Zustand (global de cliente) e TanStack Query (server state). Inclui configuração de stores, persistência e integração com o BFF.

**Agente:** dev-mobile  
**Guardrails aplicáveis:** `mobile.md §4`, `mobile.md §7`, `mobile.md §9`  
**Referências rápidas:** `Guidelines/mobile/estado.md`

---

## Quando usar

- Ao iniciar a implementação de uma feature que envolve estado compartilhado entre telas
- Ao perceber que `useState` local não é mais suficiente para a complexidade atual
- Para configurar o estado de autenticação do app
- Para decidir entre Zustand e TanStack Query para um dado específico
- Para auditar e reorganizar estado existente que cresceu sem critério

---

## Processo de execução

### Passo 1 — Mapear os dados que precisam de estado

Listar todos os dados que a feature precisa e classificar cada um:

| Dado | Origem | Classificação |
|---|---|---|
| Lista de pedidos | BFF `/orders` | Server state → TanStack Query |
| Status de autenticação | Derivado do token | Global client state → Zustand |
| Token JWT | SecureStore | Persistência segura → SecureStore |
| Preferência de tema | Local do usuário | Global persistido → Zustand + AsyncStorage |
| Modal de confirmação aberto | UI | Local → useState |
| Texto do input de busca | UI | Local → useState |

### Passo 2 — Decidir a camada correta

Fluxograma de decisão:

```
O dado vem do servidor (BFF)?
  └─ Sim → TanStack Query (useQuery / useMutation)
  └─ Não → O dado é compartilhado entre ≥2 telas sem relação pai-filho?
               └─ Sim → É sensível (token, credencial)?
                          └─ Sim → SecureStore + Zustand (apenas estado derivado em memória)
                          └─ Não → Precisa persistir entre sessões?
                                     └─ Sim → Zustand + AsyncStorage persist
                                     └─ Não → Zustand (sem persist)
               └─ Não → useState local (no componente ou tela)
```

### Passo 3 — Configurar QueryClient (se ainda não configurado)

```typescript
// src/services/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,       // 5 min — não refetch sem necessidade
      gcTime: 1000 * 60 * 10,          // 10 min em cache após desmontagem
      retry: 2,
      refetchOnWindowFocus: false,      // mobile não tem foco de janela
      refetchOnReconnect: true,
    },
    mutations: { retry: 0 },
  },
});
```

### Passo 4 — Criar store de autenticação

```typescript
// src/stores/authStore.ts
import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  initialize: () => Promise<void>;
  login: (token: string, user: User) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  initialize: async () => {
    const token = await SecureStore.getItemAsync('auth_token');
    set({ isLoading: false, isAuthenticated: !!token });
  },

  login: async (token, user) => {
    await SecureStore.setItemAsync('auth_token', token);
    set({ user, isAuthenticated: true });
  },

  logout: async () => {
    await SecureStore.deleteItemAsync('auth_token');
    set({ user: null, isAuthenticated: false });
  },
}));
```

### Passo 5 — Criar store de preferências (com persistência)

```typescript
// src/stores/preferencesStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface PreferencesState {
  theme: 'light' | 'dark' | 'system';
  language: 'pt-BR' | 'en-US';
  hasSeenOnboarding: boolean;
  notificationsEnabled: boolean;
  setTheme: (theme: PreferencesState['theme']) => void;
  markOnboardingComplete: () => void;
  setNotificationsEnabled: (enabled: boolean) => void;
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set) => ({
      theme: 'system',
      language: 'pt-BR',
      hasSeenOnboarding: false,
      notificationsEnabled: false,

      setTheme: (theme) => set({ theme }),
      markOnboardingComplete: () => set({ hasSeenOnboarding: true }),
      setNotificationsEnabled: (enabled) => set({ notificationsEnabled: enabled }),
    }),
    {
      name: 'preferences-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### Passo 6 — Store de UI compartilhada (sem persistência)

```typescript
// src/stores/uiStore.ts — para estado de UI global (toasts, modais globais)
import { create } from 'zustand';

interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
}

interface UIState {
  toasts: Toast[];
  showToast: (message: string, type: Toast['type']) => void;
  dismissToast: (id: string) => void;
}

export const useUIStore = create<UIState>()((set) => ({
  toasts: [],

  showToast: (message, type) =>
    set((state) => ({
      toasts: [
        ...state.toasts,
        { id: Date.now().toString(), message, type },
      ],
    })),

  dismissToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),
}));
```

### Passo 7 — Inicializar AuthStore no RootLayout

```tsx
// app/_layout.tsx — inicializar estado de auth ao montar
import { useEffect } from 'react';
import { useAuthStore } from '@/stores/authStore';

function RootNavigator() {
  const initialize = useAuthStore((s) => s.initialize);
  const isLoading = useAuthStore((s) => s.isLoading);

  useEffect(() => {
    initialize();
  }, []);

  useAuthRedirect();

  if (isLoading) return <SplashScreen />;

  return <Stack screenOptions={{ headerShown: false }} />;
}
```

### Passo 8 — Evitar seletores desnecessários no Zustand

```typescript
// ⛔ selecionar o store inteiro — rerenderiza a cada mudança em qualquer campo
const store = useAuthStore();

// ✅ selecionar apenas o que o componente usa
const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
const user = useAuthStore((s) => s.user);

// ✅ seletor composto com igualdade rasa para objetos
import { shallow } from 'zustand/shallow';
const { user, isAuthenticated } = useAuthStore(
  (s) => ({ user: s.user, isAuthenticated: s.isAuthenticated }),
  shallow
);
```

---

## Anti-padrões bloqueados

```typescript
// ⛔ dados do servidor em Zustand (duplica cache, cria inconsistência)
const useOrderStore = create(() => ({ orders: [] as Order[], fetchOrders: async () => {} }));

// ⛔ fetch manual em useEffect
useEffect(() => {
  fetch('/orders').then(r => r.json()).then(setOrders);
}, []);

// ⛔ token em AsyncStorage ou estado React
await AsyncStorage.setItem('token', jwtToken);
const [token, setToken] = useState('');

// ⛔ store inteiro como prop
function MyComponent({ store }: { store: ReturnType<typeof useAuthStore> }) {}

// ✅ passar apenas dados necessários
function MyComponent({ user }: { user: User }) {}
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Vou usar Context API em vez de Zustand, é mais simples" | Context API sem `useMemo`/`useCallback` cuidadoso causa re-renders em cascata — Zustand resolve isso com seletores granulares sem boilerplate |
| "Vou guardar os dados da API no Zustand para não precisar do TanStack Query" | Zustand não tem cache inteligente, retry automático, deduplicação de requests ou sincronização de background — essas funcionalidades são o valor do TanStack Query |
| "Prefiro Redux, já conheço" | Redux é aceito se o projeto já usa; para projetos novos, Zustand tem o mesmo poder com muito menos boilerplate — decisão deve ser documentada como ADR |

---

## Checklist de conclusão

- [ ] Cada dado classificado na camada correta (local / Zustand / TanStack Query)
- [ ] `QueryClient` configurado com `staleTime`, `gcTime` e `refetchOnWindowFocus: false`
- [ ] `AuthStore` com `initialize()` chamado no RootLayout
- [ ] Tokens e credenciais em `SecureStore` — nunca em Zustand ou AsyncStorage
- [ ] Preferências não-sensíveis em Zustand + AsyncStorage persist
- [ ] Seletores granulares no Zustand (não o store inteiro)
- [ ] Nenhum `useEffect` de fetch manual — sempre TanStack Query para dados do BFF
- [ ] Sem `any` em interfaces de store
