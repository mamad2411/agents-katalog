---
name: criar-hook
description: "Extrai lógica React em custom hooks para reúso. Use quando o dev-frontend precisa isolar lógica de estado ou efeito reaproveitável."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-hook

Extrai lógica de estado, efeitos colaterais ou comunicação com BFF para um **hook customizado React**: encapsula complexidade, promove reutilização e mantém componentes focados exclusivamente em renderização.

**Agente:** dev-frontend  
**Guardrails aplicáveis:** `00-core.md`, `frontend.md`, `seguranca.md`

---

## Quando usar

- Quando um componente tem mais de 2-3 `useState` relacionados à mesma preocupação
- Quando lógica de fetch de dados precisa ser reutilizada em múltiplos componentes
- Quando um `useEffect` complexo polui o componente
- Para encapsular integração com API do BFF (request, loading, error, data)
- Para lógica de formulário, debounce, polling, WebSocket, etc.

---

## Classificação de hooks

| Tipo | Responsabilidade | Exemplo |
|---|---|---|
| **Dados (fetch)** | Busca dados do BFF, gerencia loading/error/data | `useUser`, `useOrderList` |
| **Mutação** | Envia dados ao BFF (POST/PUT/PATCH/DELETE) | `useCreateOrder`, `useUpdateProfile` |
| **UI/Comportamento** | Lógica de interação sem HTTP | `useDebounce`, `useLocalStorage`, `useMediaQuery` |
| **Formulário** | Validação, submissão, estado de campos | `useLoginForm`, `useCheckoutForm` |

---

## Pré-requisitos

- Contrato do endpoint do BFF (para hooks de dados/mutação)
- Identificação clara da lógica a encapsular (não criar hook "por criar")

---

## Processo de execução

### Passo 1 — Nomear o hook corretamente

- Sempre prefixo `use`: `useUser`, `useCreateOrder`, `useDebounce`
- Nome descreve **o que o hook faz**, não como: `useUser` (não `useFetchUserFromBff`)
- Hooks de mutação com verbo de ação: `useCreateOrder`, `useUpdateProfile`, `useDeleteItem`

### Passo 2 — Implementar hook de dados (fetch)

```typescript
// src/hooks/useUser.ts
import { useState, useEffect } from 'react';
import { fetchUser } from '../services/user.service';

interface UseUserResult {
  user: UserDto | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useUser(userId: string): UseUserResult {
  const [user, setUser] = useState<UserDto | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Trigger manual de refetch
  const [trigger, setTrigger] = useState(0);

  useEffect(() => {
    if (!userId) return;

    let cancelled = false; // evita setState em componente desmontado
    setIsLoading(true);
    setError(null);

    fetchUser(userId)
      .then(data => {
        if (!cancelled) setUser(data);
      })
      .catch(err => {
        if (!cancelled) setError(err.message ?? 'Erro ao carregar usuário');
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => { cancelled = true; };
  }, [userId, trigger]);

  return { user, isLoading, error, refetch: () => setTrigger(t => t + 1) };
}
```

### Passo 3 — Implementar hook de mutação

```typescript
// src/hooks/useCreateOrder.ts
import { useState } from 'react';
import { createOrder } from '../services/order.service';

interface UseCreateOrderResult {
  execute: (dto: CreateOrderDto) => Promise<OrderDto | null>;
  isLoading: boolean;
  error: string | null;
  reset: () => void;
}

export function useCreateOrder(): UseCreateOrderResult {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async (dto: CreateOrderDto): Promise<OrderDto | null> => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await createOrder(dto);
      return result;
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Erro ao criar pedido';
      setError(message);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  return { execute, isLoading, error, reset: () => setError(null) };
}
```

### Passo 4 — Separar comunicação HTTP em service

O hook não deve fazer `fetch` diretamente — delegar para um service:

```typescript
// src/services/user.service.ts
// Toda comunicação com o BFF fica aqui — mockável em testes
export async function fetchUser(userId: string): Promise<UserDto> {
  const response = await fetch(`/api/v1/users/${userId}`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail ?? `HTTP ${response.status}`);
  }

  return response.json();
}
```

Benefícios:
- Service é mockável em testes do hook sem interceptar `fetch` global
- Lógica de headers, auth e tratamento de status fica em um lugar só
- Hook permanece simples e testável

### Passo 5 — Implementar hook de UI (sem HTTP)

```typescript
// src/hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}

// src/hooks/useLocalStorage.ts
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [stored, setStored] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    setStored(value);
    localStorage.setItem(key, JSON.stringify(value));
  };

  return [stored, setValue] as const;
}
```

### Passo 6 — Regras de hooks obrigatórias

Do React — não violar:
- Só chamar hooks no **top level** — nunca dentro de `if`, `for` ou funções aninhadas
- Só chamar hooks em **componentes funcionais** ou outros hooks customizados

```typescript
// ⛔ hook dentro de condição
if (isLoggedIn) {
  const { user } = useUser(userId); // viola a regra
}

// ✅ hook no top level, condição dentro
const { user } = useUser(isLoggedIn ? userId : '');
```

### Passo 7 — Estrutura de arquivos

```
src/hooks/
├── useUser.ts
├── useUser.test.ts
├── useCreateOrder.ts
├── useCreateOrder.test.ts
└── useDebounce.ts
```

```
src/services/
├── user.service.ts       # comunicação HTTP com o BFF
└── order.service.ts
```

---

## Checklist de conclusão

- [ ] Nome começa com `use`
- [ ] Lógica HTTP delegada para service (não no hook diretamente)
- [ ] Sem memory leak: `useEffect` com cleanup para evitar `setState` em componente desmontado
- [ ] Hook de dados retorna `{ data, isLoading, error }` como mínimo
- [ ] Hook de mutação retorna `{ execute, isLoading, error, reset }`
- [ ] Sem `any` nos tipos retornados (`frontend.md §4`)
- [ ] Testes escritos com `gerar-teste-componente`
