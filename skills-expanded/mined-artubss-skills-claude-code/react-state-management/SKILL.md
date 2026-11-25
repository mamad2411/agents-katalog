---
name: react-state-management
description: "Domine o gerenciamento moderno de estado React com Redux Toolkit, Zustand, Jotai e React Query. Use ao configurar estado global, gerenciar estado do servidor ou escolher entre soluções de gerenciamento de estado."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Gerenciamento de Estado em React

Guia abrangente de padrões modernos de gerenciamento de estado React, desde estado local do componente até stores globais e sincronização de estado do servidor.

## Não use essa skill quando

- A tarefa for não relacionada a gerenciamento de estado em React
- Você precisar de um domínio ou ferramenta diferente fora do escopo

## Instruções

- Esclareça objetivos, restrições e inputs necessários.
- Aplique as melhores práticas relevantes e valide os resultados.
- Forneça passos acionáveis e verificação.
- Se exemplos detalhados forem necessários, abra `resources/implementation-playbook.md`.

## Use essa skill quando

- Configurar gerenciamento de estado global em uma aplicação React
- Escolher entre Redux Toolkit, Zustand ou Jotai
- Gerenciar estado do servidor com React Query ou SWR
- Implementar atualizações otimistas
- Debugar problemas relacionados a estado
- Migrar de Redux legado para padrões modernos

## Conceitos Principais

### 1. Categorias de Estado

| Tipo | Descrição | Soluções |
|------|-----------|----------|
| **Estado Local** | Específico do componente, estado de UI | useState, useReducer |
| **Estado Global** | Compartilhado entre componentes | Redux Toolkit, Zustand, Jotai |
| **Estado do Servidor** | Dados remotos, cache | React Query, SWR, RTK Query |
| **Estado de URL** | Parâmetros de rota, busca | React Router, nuqs |
| **Estado de Formulário** | Valores de entrada, validação | React Hook Form, Formik |

### 2. Critérios de Seleção

```
Aplicação pequena, estado simples → Zustand ou Jotai
Aplicação grande, estado complexo → Redux Toolkit
Muita interação com servidor → React Query + estado cliente leve
Atualizações atômicas/granulares → Jotai
```

## Início Rápido

### Zustand (Mais Simples)

```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  user: User | null
  theme: 'light' | 'dark'
  setUser: (user: User | null) => void
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () => set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        })),
      }),
      { name: 'app-storage' }
    )
  )
)

// Uso em componente
function Header() {
  const { user, theme, toggleTheme } = useStore()
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  )
}
```

## Padrões

### Padrão 1: Redux Toolkit com TypeScript

```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit'
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux'
import userReducer from './slices/userSlice'
import cartReducer from './slices/cartSlice'

export const store = configureStore({
  reducer: {
    user: userReducer,
    cart: cartReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

// Hooks tipados
export const useAppDispatch: () => AppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
```

```typescript
// store/slices/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'

interface User {
  id: string
  email: string
  name: string
}

interface UserState {
  current: User | null
  status: 'idle' | 'loading' | 'succeeded' | 'failed'
  error: string | null
}

const initialState: UserState = {
  current: null,
  status: 'idle',
  error: null,
}

export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`)
      if (!response.ok) throw new Error('Falha ao buscar usuário')
      return await response.json()
    } catch (error) {
      return rejectWithValue((error as Error).message)
    }
  }
)

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.current = action.payload
      state.status = 'succeeded'
    },
    clearUser: (state) => {
      state.current = null
      state.status = 'idle'
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.status = 'loading'
        state.error = null
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.current = action.payload
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.payload as string
      })
  },
})

export const { setUser, clearUser } = userSlice.actions
export default userSlice.reducer
```

### Padrão 2: Zustand com Slices (Escalável)

```typescript
// store/slices/createUserSlice.ts
import { StateCreator } from 'zustand'

export interface UserSlice {
  user: User | null
  isAuthenticated: boolean
  login: (credentials: Credentials) => Promise<void>
  logout: () => void
}

export const createUserSlice: StateCreator<
  UserSlice & CartSlice, // Tipo de store combinado
  [],
  [],
  UserSlice
> = (set, get) => ({
  user: null,
  isAuthenticated: false,
  login: async (credentials) => {
    const user = await authApi.login(credentials)
    set({ user, isAuthenticated: true })
  },
  logout: () => {
    set({ user: null, isAuthenticated: false })
    // Pode acessar outras slices
    // get().clearCart()
  },
})

// store/index.ts
import { create } from 'zustand'
import { createUserSlice, UserSlice } from './slices/createUserSlice'
import { createCartSlice, CartSlice } from './slices/createCartSlice'

type StoreState = UserSlice & CartSlice

export const useStore = create<StoreState>()((...args) => ({
  ...createUserSlice(...args),
  ...createCartSlice(...args),
}))

// Subscrições seletivas (previne re-renders desnecessários)
export const useUser = () => useStore((state) => state.user)
export const useCart = () => useStore((state) => state.cart)
```

### Padrão 3: Jotai para Estado Atômico

```typescript
// atoms/userAtoms.ts
import { atom } from 'jotai'
import { atomWithStorage } from 'jotai/utils'

// Atom básico
export const userAtom = atom<User | null>(null)

// Atom derivado (computado)
export const isAuthenticatedAtom = atom((get) => get(userAtom) !== null)

// Atom com persistência em localStorage
export const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light')

// Atom assíncrono
export const userProfileAtom = atom(async (get) => {
  const user = get(userAtom)
  if (!user) return null
  const response = await fetch(`/api/users/${user.id}/profile`)
  return response.json()
})

// Atom somente escrita (ação)
export const logoutAtom = atom(null, (get, set) => {
  set(userAtom, null)
  set(cartAtom, [])
  localStorage.removeItem('token')
})

// Uso
function Profile() {
  const [user] = useAtom(userAtom)
  const [, logout] = useAtom(logoutAtom)
  const [profile] = useAtom(userProfileAtom) // Suspense habilitado

  return (
    <Suspense fallback={<Skeleton />}>
      <ProfileContent profile={profile} onLogout={logout} />
    </Suspense>
  )
}
```

### Padrão 4: React Query para Estado do Servidor

```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Factory de chaves de query
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
}

// Hook de busca
export function useUsers(filters: UserFilters) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => fetchUsers(filters),
    staleTime: 5 * 60 * 1000, // 5 minutos
    gcTime: 30 * 60 * 1000, // 30 minutos (anteriormente cacheTime)
  })
}

// Hook de usuário único
export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
    enabled: !!id, // Não buscar se não houver id
  })
}

// Mutation com atualização otimista
export function useUpdateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      // Cancelar refetches pendentes
      await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) })

      // Snapshot do valor anterior
      const previousUser = queryClient.getQueryData(userKeys.detail(newUser.id))

      // Atualizar otimisticamente
      queryClient.setQueryData(userKeys.detail(newUser.id), newUser)

      return { previousUser }
    },
    onError: (err, newUser, context) => {
      // Reverter em caso de erro
      queryClient.setQueryData(
        userKeys.detail(newUser.id),
        context?.previousUser
      )
    },
    onSettled: (data, error, variables) => {
      // Refetch após mutation
      queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) })
    },
  })
}
```

### Padrão 5: Combinando Estado Cliente + Servidor

```typescript
// Zustand para estado cliente
const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  modal: null,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  openModal: (modal) => set({ modal }),
  closeModal: () => set({ modal: null }),
}))

// React Query para estado do servidor
function Dashboard() {
  const { sidebarOpen, toggleSidebar } = useUIStore()
  const { data: users, isLoading } = useUsers({ active: true })
  const { data: stats } = useStats()

  if (isLoading) return <DashboardSkeleton />

  return (
    <div className={sidebarOpen ? 'with-sidebar' : ''}>
      <Sidebar open={sidebarOpen} onToggle={toggleSidebar} />
      <main>
        <StatsCards stats={stats} />
        <UserTable users={users} />
      </main>
    </div>
  )
}
```

## Melhores Práticas

### Faça
- **Coloque o estado próximo** - Mantenha o estado o mais próximo possível de onde é usado
- **Use seletores** - Previne re-renders desnecessários com subscrições seletivas
- **Normalize dados** - Achate estruturas aninhadas para facilitar atualizações
- **Tipifique tudo** - Cobertura completa de TypeScript previne erros de runtime
- **Separe responsabilidades** - Estado do servidor (React Query) vs estado cliente (Zustand)

### Não faça
- **Não globalize excessivamente** - Nem tudo precisa estar em estado global
- **Não duplique estado do servidor** - Deixe o React Query gerenciar
- **Não mutue diretamente** - Sempre use atualizações imutáveis
- **Não armazene dados derivados** - Compute-os ao invés
- **Não misture paradigmas** - Escolha uma solução primária por categoria

## Guias de Migração

### De Redux Legado para RTK

```typescript
// Antes (Redux legado)
const ADD_TODO = 'ADD_TODO'
const addTodo = (text) => ({ type: ADD_TODO, payload: text })
function todosReducer(state = [], action) {
  switch (action.type) {
    case ADD_TODO:
      return [...state, { text: action.payload, completed: false }]
    default:
      return state
  }
}

// Depois (Redux Toolkit)
const todosSlice = createSlice({
  name: 'todos',
  initialState: [],
  reducers: {
    addTodo: (state, action: PayloadAction<string>) => {
      // Immer permite "mutações"
      state.push({ text: action.payload, completed: false })
    },
  },
})
```

## Recursos

- [Documentação Redux Toolkit](https://redux-toolkit.js.org/)
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- [Documentação Jotai](https://jotai.org/)
- [TanStack Query](https://tanstack.com/query)