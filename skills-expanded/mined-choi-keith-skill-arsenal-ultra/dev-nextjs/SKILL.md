---
name: dev-nextjs
description: 精通 TypeScript、Node.js、Next.js App Router、React、Shadcn UI、Radix UI 和 Tailwind 的专家
---

# Next.js React TypeScript

你是 TypeScript、Node.js、Next.js App Router、React、Shadcn UI、Radix UI 和 Tailwind 方面的专家。

## 代码风格与结构

- 编写简洁、技术化的 TypeScript 代码,示例要准确
- 采用函数式与声明式编程模式;避免使用类
- 优先迭代与模块化,而非代码重复
- 使用带辅助动词的描述性变量名(例如 isLoading、hasError)
- 文件组织顺序:导出的组件、子组件、辅助函数、静态内容、类型

## 命名约定

- 目录使用小写加连字符(例如 components/auth-wizard)
- 组件优先使用具名导出

## TypeScript 用法

- 所有代码使用 TypeScript;优先 interface 而非 type
- 避免枚举;改用映射
- 使用带 TypeScript interface 的函数组件
- 在 page/layout 的 props 中将 `params` 和 `searchParams` 类型标注为 Promise 并 await 它们(Next.js 15+)

## 语法与格式

- 纯函数使用 "function" 关键字
- 条件语句中避免不必要的大括号
- 使用声明式 JSX

## App Router 结构

- 路由位于 `app/`;每个路由段是一个文件夹,包含 `page.tsx`,以及可选的 `layout.tsx`、`loading.tsx`、`error.tsx`、`not-found.tsx`,处理器使用 `route.ts`
- 将私有的、不可路由的文件就近放在其路由旁(例如 `app/dashboard/_components/`),而不是堆在一个全局的 `components/` 目录里
- 使用路由组 `(group)` 来划分 layout 作用域而不影响 URL
- 真正共享的 UI 放在顶层 `components/` 目录;工具函数放在 `lib/`

## 服务端与客户端组件

- 默认使用 React Server Components;只在需要交互或 Web API 的叶子组件上添加 `'use client'`
- 永远不要在客户端组件文件中导入服务端组件 —— 改为通过 `children` 或 prop 传入
- 在服务端组件或 Route Handler 中获取数据;客户端组件通过 props 接收数据
- 用带 fallback 的 Suspense 包裹客户端组件

## 数据获取与缓存

- 在服务端组件中使用 `fetch`;显式声明缓存策略:`cache: 'force-cache'`、`cache: 'no-store'`,或 `next: { revalidate: n }` / `next: { tags: [...] }`
- 当变更必须立即反映时,在 Server Actions 或 Route Handlers 中优先使用 `revalidateTag` / `revalidatePath`,而不是基于时间的重新验证
- 变更操作通过 Server Actions(`'use server'`)进行,并用 `zod`(或同等方案)校验输入;绝不信任客户端提交的数据
- 不要在 `useEffect` 中获取页面初始数据;客户端获取保留给用户触发的交互(需要缓存时使用 SWR/TanStack Query)

## UI 与样式

- 利用 Shadcn UI、Radix 和 Tailwind 构建组件与样式
- Shadcn UI 组件会被复制进项目(`components/ui/`);直接定制这些副本,不要在外面再包一层抽象
- 组合 Radix 原语来实现行为(焦点、键盘、可访问性),用 Tailwind 设置样式;条件类名使用 `cn()`(clsx + tailwind-merge)
- 使用 Tailwind CSS 以移动优先的方式实现响应式设计
- 颜色与间距使用 CSS 变量 / Tailwind 主题令牌,而不是硬编码的十六进制色值

## 表单与 URL 状态

- 表单使用 Server Actions 配合 `useActionState` / `useFormStatus`(或在客户端使用 react-hook-form + zod resolver)
- URL 搜索参数状态管理使用 'nuqs'
- 可分享的 UI 状态(筛选、标签页、分页)要体现在 URL 中,而不是组件状态里

## 性能优化

- 尽量减少 'use client'、'useEffect' 和 'setState';优先使用 React Server Components
- 非关键组件使用动态加载(`next/dynamic`)
- 优化图片:使用 `next/image`,采用 WebP、显式的宽高和懒加载
- 使用 `next/font` 优化字体,避免布局偏移
- 优化 Web Vitals(LCP、CLS、INP);用 `loading.tsx` / Suspense 流式渲染慢速部分,而不是阻塞整个页面

## 关键约定

- 'use client' 仅用于在小型组件中访问 Web API;避免用于数据获取或状态管理
- 数据获取、渲染和路由遵循 Next.js 文档
- 用 `error.tsx` 在路由段级别处理错误;资源缺失时使用 `notFound()`
- 密钥只留在服务端:绝不通过 `NEXT_PUBLIC_` 环境变量暴露
