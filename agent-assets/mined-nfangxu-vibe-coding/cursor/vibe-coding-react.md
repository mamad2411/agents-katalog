---
description: React 前端开发规范，适用于 React 18 + TypeScript + Vite 项目
globs: ["**/*.tsx", "**/*.jsx", "**/vite.config.*"]
alwaysApply: false
---

# React 开发规范

## 技术栈

- **框架**: React 18
- **语言**: TypeScript（严格模式）
- **构建工具**: Vite
- **状态管理**: Zustand / Redux Toolkit（按项目复杂度选择）
- **路由**: React Router v6
- **数据获取**: TanStack Query (React Query)
- **表单**: React Hook Form + Zod
- **代码规范**: ESLint + Prettier

## 组件规范

### 命名规范

- 组件文件使用 PascalCase：`UserProfile.tsx`、`AppHeader.tsx`
- 组件名与文件名一致
- Hook 文件使用 camelCase，以 `use` 开头：`useAuth.ts`

### 组件定义

- 使用函数组件（不使用类组件）
- 使用具名函数便于调试（而非匿名箭头函数赋值）

```tsx
// 推荐：具名函数组件
interface UserCardProps {
  userId: string
  userName: string
  onSelect: (id: string) => void
}

export function UserCard({ userId, userName, onSelect }: UserCardProps) {
  return (
    <div className="user-card" onClick={() => onSelect(userId)}>
      <span>{userName}</span>
    </div>
  )
}
```

### Props 规范

- 始终使用 TypeScript interface 定义 Props
- 使用解构赋值获取 Props，在参数处设置默认值
- 避免将过多 Props 透传（超过 3-4 个考虑组合模式）

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  children: React.ReactNode
  onClick?: () => void
}

export function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? <Spinner /> : children}
    </button>
  )
}
```

## Hooks 规范

### 内置 Hooks

- `useState`：本地 UI 状态
- `useEffect`：副作用（数据获取、订阅、DOM 操作）
- `useCallback`：缓存函数引用（传递给子组件或 useEffect 依赖时）
- `useMemo`：缓存计算结果（计算开销大时）
- `useRef`：DOM 引用或不触发重渲染的可变值

```tsx
// 推荐：useEffect 正确使用
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    
    async function loadUser() {
      setLoading(true)
      try {
        const data = await fetchUser(userId)
        if (!cancelled) setUser(data)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadUser()
    
    // 清理函数防止竞态条件
    return () => { cancelled = true }
  }, [userId]) // 依赖数组完整声明

  if (loading) return <Spinner />
  if (!user) return <NotFound />
  return <div>{user.name}</div>
}
```

### 自定义 Hooks

- 以 `use` 开头，封装可复用的逻辑
- 放在 `hooks/` 目录下
- 优先使用 TanStack Query 处理数据获取

```tsx
// hooks/useUser.ts - 推荐使用 TanStack Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 分钟
  })
}

export function useUpdateUser() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: UpdateUserInput) => updateUser(data),
    onSuccess: (updatedUser) => {
      queryClient.setQueryData(['user', updatedUser.id], updatedUser)
    },
  })
}
```

## 状态管理

### 状态层次

1. **服务端状态**：使用 TanStack Query（缓存、同步、更新）
2. **全局 UI 状态**：使用 Zustand（模态框、主题、用户偏好）
3. **表单状态**：使用 React Hook Form
4. **本地组件状态**：使用 useState / useReducer

### Zustand Store

```typescript
// stores/useAppStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  setTheme: (theme: 'light' | 'dark') => void
  toggleSidebar: () => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      theme: 'light',
      sidebarOpen: true,
      setTheme: (theme) => set({ theme }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
    }),
    { name: 'app-storage' }
  )
)
```

## 表单处理

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email('请输入有效的邮箱地址'),
  password: z.string().min(8, '密码至少 8 个字符'),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    await authApi.login(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} placeholder="邮箱" />
      {errors.email && <span>{errors.email.message}</span>}
      
      <input {...register('password')} type="password" placeholder="密码" />
      {errors.password && <span>{errors.password.message}</span>}
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '登录中...' : '登录'}
      </button>
    </form>
  )
}
```

## 性能优化

- 使用 `React.memo` 包裹纯展示组件
- 使用 `useCallback` 缓存传递给子组件的回调
- 使用 `useMemo` 缓存开销大的计算（避免过度使用）
- 使用 `React.lazy` + `Suspense` 代码分割

```tsx
// 懒加载路由
const UserDashboard = React.lazy(() => import('./pages/UserDashboard'))

// 代码分割
function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<UserDashboard />} />
      </Routes>
    </Suspense>
  )
}

// memo 优化
const UserListItem = React.memo(function UserListItem({
  user,
  onSelect,
}: UserListItemProps) {
  return (
    <li onClick={() => onSelect(user.id)}>
      {user.name}
    </li>
  )
})
```

## 项目目录结构

```
src/
├── api/            # API 请求函数
├── assets/         # 静态资源
├── components/     # 通用组件
│   └── ui/         # 基础 UI 组件
├── hooks/          # 自定义 Hooks
├── layouts/        # 布局组件
├── pages/          # 页面组件
├── stores/         # Zustand Stores
├── types/          # TypeScript 类型定义
├── utils/          # 工具函数
├── App.tsx
└── main.tsx
```

## 避免的反模式

```tsx
// ❌ 在渲染中定义组件（每次都会重新挂载）
function Parent() {
  function Child() { return <div>child</div> } // 避免！
  return <Child />
}

// ✅ 在组件外定义
function Child() { return <div>child</div> }
function Parent() { return <Child /> }

// ❌ useEffect 中缺少清理
useEffect(() => {
  const sub = subscribe(callback) // 忘记取消订阅
}, [])

// ✅ 添加清理函数
useEffect(() => {
  const sub = subscribe(callback)
  return () => sub.unsubscribe()
}, [])

// ❌ 直接修改状态
const [items, setItems] = useState([])
items.push(newItem) // 直接修改，不触发重渲染

// ✅ 创建新数组
setItems([...items, newItem])
```
