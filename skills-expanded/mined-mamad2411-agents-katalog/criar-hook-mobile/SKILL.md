---
name: criar-hook-mobile
description: "Extrai lógica em hook customizado — dados via TanStack Query, UI, APIs nativas e persistência. Use quando o dev-mobile precisa isolar lógica reaproveitável."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-hook-mobile

Extrai lógica de estado, efeito ou integração com API em **hook customizado React Native**: hooks de dados (TanStack Query), hooks de lógica de UI e hooks de acesso a APIs nativas do dispositivo.

**Agente:** dev-mobile  
**Guardrails aplicáveis:** `mobile.md §4`, `mobile.md §7`, `mobile.md §9`  
**Referências rápidas:** `Guidelines/mobile/estado.md`

---

## Quando usar

- Para encapsular chamadas ao BFF via TanStack Query
- Para extrair lógica de UI complexa de um componente ou tela
- Para abstrair acesso a APIs nativas (câmera, localização, biometria, notificações)
- Para integrar com `expo-secure-store` ou `AsyncStorage`
- Para criar hooks de comportamento reutilizável entre telas

---

## Classificação de hooks mobile

| Tipo | Responsabilidade | Exemplo |
|---|---|---|
| **Dados (Query)** | Busca dados do BFF via TanStack Query | `useOrders`, `useUser`, `useProduct` |
| **Mutation** | Envia dados ao BFF e invalida cache | `useCreateOrder`, `useUpdateProfile` |
| **Estado de UI** | Lógica de estado que não é dado do servidor | `useModal`, `usePagination`, `useFormStep` |
| **Nativo** | Abstrai API nativa do Expo | `useCamera`, `useLocation`, `useNotifications` |
| **Persistência** | Lê/escreve SecureStore ou AsyncStorage | `useAuthToken`, `usePreferences` |
| **Lifecycle** | Reage ao ciclo de vida do app | `useAppState`, `useNetworkState` |

---

## Processo de execução

### Passo 1 — Identificar o tipo e a responsabilidade

Antes de implementar, responder:
- O dado vem do BFF? → Hook de dados com TanStack Query
- É lógica de UI que a tela não deve conter? → Hook de estado de UI
- Envolve API nativa? → Hook nativo com tratamento de permissão
- Precisa persistir entre sessões? → Hook de persistência com SecureStore/AsyncStorage

### Passo 2 — Hook de dados (TanStack Query)

Padrão obrigatório para integração com o BFF:

```typescript
// src/hooks/useOrders.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/services/api';
import type { Order, CreateOrderDto } from '@/types/api';

// Query keys centralizadas — previnem magic strings espalhadas
export const orderKeys = {
  all: ['orders'] as const,
  list: (filters?: OrderFilters) => [...orderKeys.all, 'list', filters] as const,
  detail: (id: string) => [...orderKeys.all, 'detail', id] as const,
};

// Hook de lista
export function useOrders(filters?: OrderFilters) {
  return useQuery({
    queryKey: orderKeys.list(filters),
    queryFn: () => api.get<Order[]>('/orders', { params: filters }).then((r) => r.data),
  });
}

// Hook de detalhe — habilitado apenas quando o ID existe
export function useOrder(id: string | undefined) {
  return useQuery({
    queryKey: orderKeys.detail(id!),
    queryFn: () => api.get<Order>(`/orders/${id}`).then((r) => r.data),
    enabled: !!id,
  });
}

// Hook de mutation com invalidação de cache
export function useCreateOrder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (dto: CreateOrderDto) =>
      api.post<Order>('/orders', dto).then((r) => r.data),
    onSuccess: () => {
      // Invalida a lista após criar novo item
      queryClient.invalidateQueries({ queryKey: orderKeys.all });
    },
  });
}

// Hook de mutation com update otimístico
export function useCancelOrder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      api.patch<Order>(`/orders/${id}/cancel`).then((r) => r.data),
    onMutate: async (id) => {
      // Cancelar queries em andamento para evitar sobrescrever
      await queryClient.cancelQueries({ queryKey: orderKeys.detail(id) });
      // Snapshot do valor anterior
      const previous = queryClient.getQueryData<Order>(orderKeys.detail(id));
      // Update otimístico
      queryClient.setQueryData<Order>(orderKeys.detail(id), (old) =>
        old ? { ...old, status: 'cancelled' } : old
      );
      return { previous };
    },
    onError: (_err, id, context) => {
      // Reverter em caso de erro
      queryClient.setQueryData(orderKeys.detail(id), context?.previous);
    },
    onSettled: (_data, _err, id) => {
      queryClient.invalidateQueries({ queryKey: orderKeys.detail(id) });
    },
  });
}
```

### Passo 3 — Hook de estado de UI

```typescript
// src/hooks/useDisclosure.ts
import { useState, useCallback } from 'react';

export function useDisclosure(initialState = false) {
  const [isOpen, setIsOpen] = useState(initialState);

  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);
  const toggle = useCallback(() => setIsOpen((s) => !s), []);

  return { isOpen, open, close, toggle };
}

// Uso:
// const deleteModal = useDisclosure();
// <Modal visible={deleteModal.isOpen} onClose={deleteModal.close} />
// <Button onPress={deleteModal.open} label="Excluir" />
```

### Passo 4 — Hook de API nativa (com permissão)

```typescript
// src/hooks/useLocation.ts
import { useState, useCallback } from 'react';
import * as Location from 'expo-location';
import { Alert, Linking } from 'react-native';

interface LocationState {
  coords: Location.LocationObjectCoords | null;
  isLoading: boolean;
  error: string | null;
}

export function useLocation() {
  const [state, setState] = useState<LocationState>({
    coords: null,
    isLoading: false,
    error: null,
  });

  const requestLocation = useCallback(async () => {
    setState((s) => ({ ...s, isLoading: true, error: null }));

    // Permissão sob demanda — nunca no startup (mobile.md §10)
    const { status } = await Location.requestForegroundPermissionsAsync();

    if (status !== 'granted') {
      setState((s) => ({ ...s, isLoading: false, error: 'Permissão negada' }));
      Alert.alert(
        'Permissão necessária',
        'Para usar esta funcionalidade, habilite o acesso à localização nas configurações do app.',
        [
          { text: 'Cancelar', style: 'cancel' },
          { text: 'Abrir configurações', onPress: () => Linking.openSettings() },
        ]
      );
      return;
    }

    try {
      const location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Balanced,
      });
      setState({ coords: location.coords, isLoading: false, error: null });
    } catch {
      setState((s) => ({ ...s, isLoading: false, error: 'Erro ao obter localização' }));
    }
  }, []);

  return { ...state, requestLocation };
}
```

### Passo 5 — Hook de lifecycle do app

```typescript
// src/hooks/useAppState.ts
import { useEffect, useRef } from 'react';
import { AppState, AppStateStatus } from 'react-native';

export function useAppState(
  onChange: (state: AppStateStatus) => void
) {
  const appState = useRef(AppState.currentState);

  useEffect(() => {
    const subscription = AppState.addEventListener('change', (nextState) => {
      if (appState.current !== nextState) {
        appState.current = nextState;
        onChange(nextState);
      }
    });

    return () => subscription.remove();
  }, [onChange]);
}

// Uso — refetch quando app volta ao foreground
useAppState((state) => {
  if (state === 'active') {
    queryClient.invalidateQueries({ queryKey: orderKeys.all });
  }
});
```

### Passo 6 — Hook de persistência segura

```typescript
// src/hooks/useAuthToken.ts
import { useState, useEffect, useCallback } from 'react';
import * as SecureStore from 'expo-secure-store';

const TOKEN_KEY = 'auth_token';

export function useAuthToken() {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Carregar token na inicialização
  useEffect(() => {
    SecureStore.getItemAsync(TOKEN_KEY)
      .then(setToken)
      .finally(() => setIsLoading(false));
  }, []);

  const saveToken = useCallback(async (newToken: string) => {
    await SecureStore.setItemAsync(TOKEN_KEY, newToken);
    setToken(newToken);
  }, []);

  const clearToken = useCallback(async () => {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
    setToken(null);
  }, []);

  return { token, isLoading, saveToken, clearToken };
}
```

### Passo 7 — Estrutura de arquivos

```
src/hooks/
├── useOrders.ts           ← hooks de dados agrupados por domínio
├── useUser.ts
├── useLocation.ts         ← hook de API nativa
├── useAppState.ts         ← hook de lifecycle
├── useDisclosure.ts       ← hook de UI reutilizável
└── __tests__/
    └── useOrders.test.ts
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Vou fazer o fetch direto com useEffect dentro da tela" | Fetch manual duplica lógica de cache, retry e loading — TanStack Query é obrigatório para dados do BFF (`mobile.md §4`) |
| "Não preciso de um hook separado, é só 2 linhas" | Extrair em hook garante testabilidade isolada e reutilização; a quantidade de linhas não é o critério |
| "Posso solicitar a permissão no `useEffect` do componente" | Permissões devem ser solicitadas sob demanda contextual — não em mount automático (`mobile.md §10`) |
| "Posso guardar o token em `useState`" | Estado React não persiste entre sessões e é exposto em ferramentas de debug — use `SecureStore` (`mobile.md §7`) |

---

## Checklist de conclusão

- [ ] Hook nomeado com prefixo `use`
- [ ] Sem `any` em TypeScript — tipos de retorno explícitos
- [ ] Hooks de dados usam TanStack Query (nunca fetch manual)
- [ ] Query keys centralizadas em objeto exportado
- [ ] Hooks de API nativa solicitam permissão sob demanda (não no mount)
- [ ] Tokens persistidos em `SecureStore` (nunca em `useState` ou `AsyncStorage`)
- [ ] Efeitos colaterais têm cleanup adequado (`useEffect` retorna `() => subscription.remove()`)
- [ ] Testes escritos com `gerar-teste-componente-nativo`
