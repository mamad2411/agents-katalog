---
name: organizar-estado
description: "Define a estratégia de gerenciamento de estado React entre Context API, Zustand ou Redux. Use quando o dev-frontend precisa decidir onde e como guardar estado."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: organizar-estado

Define e implementa a **estratégia de gerenciamento de estado** para uma feature ou aplicação React: decide onde o estado vive, qual ferramenta usar e como estruturar para evitar prop drilling, estado global desnecessário e re-renders excessivos.

**Agente:** dev-frontend  
**Guardrails aplicáveis:** `00-core.md`, `frontend.md`, `seguranca.md`

---

## Quando usar

- Ao iniciar uma nova feature com múltiplos componentes que compartilham dados
- Quando prop drilling ultrapassa 2-3 níveis de profundidade
- Quando há re-renders de performance ou estado inconsistente entre componentes
- Para decidir entre Context, Zustand, React Query ou estado local

---

## Modelo de decisão: onde o estado vive

Seguindo `frontend.md §3` — estado o mais local possível:

```
Estado local (useState / useReducer)
  ↓  apenas quando 2+ componentes não-relacionados precisam
Estado de componente pai (lift state up)
  ↓  apenas quando prop drilling > 2 níveis ou dado genuinamente global
Context API (para dado que não muda frequentemente)
  ↓  apenas quando há lógica complexa de atualização ou alta frequência de escrita
Zustand / estado global externo
```

### Checklist para decidir onde o estado vive

```
1. Apenas um componente usa este estado?
   → useState local. FIM.

2. Dois componentes irmãos precisam do mesmo estado?
   → Lift state up para o pai comum. FIM.

3. O estado é compartilhado por muitos componentes em árvores diferentes?
   → Continuar para 4.

4. O estado muda com alta frequência (digitação, scroll, animação)?
   → Zustand com slice isolado. FIM.

5. O estado muda raramente (tema, sessão do usuário, idioma)?
   → Context API. FIM.

6. O estado vem do servidor e precisa de cache/invalidação?
   → React Query (ou SWR). FIM.
```

---

## Implementações por estratégia

### Estado Local — `useState` e `useReducer`

```typescript
// useState — para valores simples
const [isOpen, setIsOpen] = useState(false);
const [selectedId, setSelectedId] = useState<string | null>(null);

// useReducer — para estado com múltiplos sub-valores relacionados
type FormState = { name: string; email: string; errors: Record<string, string> };
type FormAction =
  | { type: 'SET_FIELD'; field: keyof FormState; value: string }
  | { type: 'SET_ERROR'; field: string; message: string }
  | { type: 'RESET' };

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_FIELD': return { ...state, [action.field]: action.value };
    case 'SET_ERROR': return { ...state, errors: { ...state.errors, [action.field]: action.message } };
    case 'RESET': return initialFormState;
  }
}

const [formState, dispatch] = useReducer(formReducer, initialFormState);
```

### Context API — dado global de baixa frequência

```typescript
// src/contexts/AuthContext.tsx
interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);

  const logout = () => {
    setUser(null);
    // Nunca armazenar token JWT em localStorage sem necessidade
    // Usar httpOnly cookie quando possível — seguranca.md §2
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook de consumo — nunca usar o contexto diretamente nos componentes
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth deve ser usado dentro de AuthProvider');
  return ctx;
}
```

### Zustand — estado global com alta frequência de escrita

```typescript
// src/stores/cart.store.ts
import { create } from 'zustand';

interface CartItem { productId: string; quantity: number; price: number; }

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (productId: string) => void;
  clear: () => void;
  total: () => number;
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],

  addItem: (item) => set(state => {
    const existing = state.items.find(i => i.productId === item.productId);
    if (existing) {
      return { items: state.items.map(i =>
        i.productId === item.productId
          ? { ...i, quantity: i.quantity + item.quantity }
          : i
      )};
    }
    return { items: [...state.items, item] };
  }),

  removeItem: (productId) => set(state => ({
    items: state.items.filter(i => i.productId !== productId),
  })),

  clear: () => set({ items: [] }),

  total: () => get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),
}));
```

Regras do Zustand:
- Um store por domínio (cart, auth, ui-preferences) — não um store global monolítico
- Ações nomeadas com verbo: `addItem`, `removeItem`, `clear`
- Computed values como funções (não estado derivado armazenado)
- Sem lógica de negócio no store — apenas mutação de estado de UI

### Server State — React Query (para dados do BFF)

```typescript
// src/hooks/useUser.ts — com React Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchUser, updateUser } from '../services/user.service';

export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutos — dado válido sem refetch
    enabled: !!userId,
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateUserDto) => updateUser(data),
    onSuccess: (updated) => {
      // Invalida cache — próxima leitura vai ao BFF
      queryClient.invalidateQueries({ queryKey: ['user', updated.id] });
    },
  });
}
```

Quando usar React Query:
- Dados que vêm do BFF e precisam de cache, loading e erro automático
- Necessidade de invalidação de cache após mutação
- Dados compartilhados entre múltiplas telas sem prop drilling

---

## Anti-padrões bloqueados

```typescript
// ⛔ estado global para dado que poderia ser local
const useGlobalIsModalOpen = create(() => ({ isOpen: false, ... }));

// ⛔ duplicar dado do servidor no estado local
const [user, setUser] = useState(null); // busca manual + gerencia cache na mão

// ⛔ prop drilling além de 2 níveis
<PageA user={user}>
  <SectionB user={user}>
    <CardC user={user}>
      <DetailD user={user} />  // ← usar Context ou React Query aqui

// ⛔ armazenar dado sensível em estado global persistido
localStorage.setItem('token', jwtToken); // seguranca.md §2 — usar httpOnly cookie
```

---

## Saída produzida

- Decisão documentada: qual estratégia e por quê (para o PR)
- Código implementado: Context / Zustand store / React Query hooks
- Testes unitários do hook ou store quando há lógica
- Sem estado duplicado entre server state e estado local
