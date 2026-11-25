---
name: js-ts-dev
description: JavaScript/TypeScript开发技能 - JS/TS语法、Node.js、异步编程、模块系统、npm/pnpm包管理、ESM/CJS。当你涉及JavaScript/TypeScript/Node.js代码开发、async/await、Promise、npm/pnpm、ESM模块、类型定义时必须使用此技能。即使用户只是说"写个JS函数"或"改下TS代码"，也应触发。
---

# JavaScript/TypeScript 开发技能 (JS/TS Development Skill)

## 快速规则（日常开发时自动加载，只需读到这里）

> **[JS/TS核心清单]** ① 用`const`优先、`let`次之、❌禁止`var` ② async函数必须try/catch或.catch()，禁止未处理的Promise rejection ③ 用`===`严格比较、❌禁止`==`（除null检查`x == null`）
> **[类型铁律]** TS项目禁止`any`（用`unknown`+类型守卫），函数参数和返回值必须有类型注解
> **[模块规范]** 新项目用ESM(`import/export`)，`"type": "module"`写入package.json

写/改JS/TS代码时，强制遵守：
1. **变量声明**：`const` > `let` > ❌`var`。const不是"不可变"是"不可重新赋值"，对象属性仍可变
2. **严格比较**：一律`===`/`!==`，唯一例外是`x == null`同时检查null和undefined
3. **异步处理**：async函数必须有错误处理，Promise链必须.catch()，设置全局`unhandledRejection`兜底
4. **类型安全**：TS项目禁止`any`（用`unknown`+类型收窄），函数签名必须有类型注解
5. **空值处理**：用可选链`?.`和空值合并`??`，禁止`x && x.y && x.y.z`链式检查
6. **解构优先**：函数参数>3个用对象解构`({ name, age }: Props)`，便于扩展和默认值
7. **不可变优先**：数组用`map/filter/reduce`而非`for`+push，对象用展开`{...obj, key: val}`而非直接修改

---

## TypeScript 规范

### 类型定义
```typescript
// ✅ interface用于对象形状（可扩展/合并）
interface User {
  id: number
  name: string
  email?: string  // 可选
}

// ✅ type用于联合/交叉/工具类型
type Status = 'active' | 'inactive' | 'banned'
type UserWithRole = User & { role: string }

// ❌ 禁止any
function process(data: any) {}     // 绕过类型检查=定时炸弹
// ✅ 用unknown+类型守卫
function process(data: unknown) {
  if (typeof data === 'string') {
    // data在这里是string
  }
}
```

### 类型守卫
```typescript
// 自定义类型守卫
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj && 'name' in obj
}

// 使用
if (isUser(data)) {
  console.log(data.name)  // 类型安全
}
```

### 泛型
```typescript
// ✅ 实用泛型
function first<T>(arr: T[]): T | undefined {
  return arr[0]
}

// ✅ 泛型约束
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}

// ✅ 常用工具类型
Partial<T>      // 所有属性可选
Required<T>     // 所有属性必需
Pick<T, K>      // 选取部分属性
Omit<T, K>      // 排除部分属性
Record<K, V>    // 键值对映射
```

### 枚举替代
```typescript
// ❌ 避免enum（编译产物大，tree-shaking差）
enum Color { Red, Green, Blue }

// ✅ 用const对象+as const
const Color = { Red: 0, Green: 1, Blue: 2 } as const
type Color = typeof Color[keyof typeof Color]  // 0 | 1 | 2
```

## 异步编程

### async/await
```typescript
// ✅ 标准错误处理
async function fetchUser(id: number): Promise<User> {
  try {
    const res = await fetch(`/api/users/${id}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return await res.json()
  } catch (err) {
    console.error(`获取用户失败 id=${id}:`, err)
    throw err  // 重新抛出让调用方决定
  }
}

// ✅ 并行请求
const [users, orders] = await Promise.all([
  fetchUsers(),
  fetchOrders(),
])

// ✅ 部分失败容忍
const results = await Promise.allSettled([task1(), task2(), task3()])
const successes = results.filter(r => r.status === 'fulfilled')
const failures = results.filter(r => r.status === 'rejected')
```

### 全局错误兜底
```typescript
// Node.js
process.on('unhandledRejection', (reason, promise) => {
  console.error('未处理的Promise拒绝:', reason)
})

// 浏览器
window.addEventListener('unhandledrejection', (event) => {
  console.error('未处理的Promise拒绝:', event.reason)
})
```

## 现代JS模式

### 空值处理
```typescript
// ✅ 可选链 + 空值合并
const city = user?.address?.city ?? '未知'

// ❌ 旧写法
const city = user && user.address && user.address.city ? user.address.city : '未知'

// ⚠️ 注意：?? 和 || 的区别
0 || 'default'   // 'default' （0是falsy）
0 ?? 'default'   // 0         （0不是nullish）
'' || 'default'  // 'default'
'' ?? 'default'  // ''
```

### 解构与默认值
```typescript
// ✅ 参数解构+默认值
function createUser({
  name,
  age = 0,
  role = 'user',
}: {
  name: string
  age?: number
  role?: string
}) {
  // ...
}

// ✅ 数组解构
const [first, ...rest] = items
const [, second] = items  // 跳过第一个

// ✅ 对象展开（浅拷贝+覆盖）
const updated = { ...user, name: 'new name' }
```

### 数组操作（函数式优先）
```typescript
// ✅ 链式操作
const activeNames = users
  .filter(u => u.status === 'active')
  .map(u => u.name)
  .sort()

// ✅ reduce聚合
const byRole = users.reduce<Record<string, User[]>>((acc, user) => {
  const key = user.role
  acc[key] = acc[key] || []
  acc[key].push(user)
  return acc
}, {})

// ✅ 查找
const admin = users.find(u => u.role === 'admin')
const hasAdmin = users.some(u => u.role === 'admin')
const allActive = users.every(u => u.status === 'active')
```

## 模块系统

### ESM (推荐)
```typescript
// 导出
export function add(a: number, b: number) { return a + b }
export default class User {}

// 导入
import User, { add } from './utils'
import * as utils from './utils'

// 动态导入（代码分割）
const { Chart } = await import('chart.js')
```

### package.json
```json
{
  "type": "module",           // 启用ESM
  "exports": {                // 明确导出入口
    ".": "./dist/index.js"
  },
  "engines": {                // 声明Node版本要求
    "node": ">=18"
  }
}
```

## Node.js 规范

### 文件操作
```typescript
import { readFile, writeFile } from 'node:fs/promises'

// ✅ 异步文件操作
const content = await readFile('data.json', 'utf-8')
await writeFile('output.json', JSON.stringify(data, null, 2))

// ❌ 禁止同步操作（阻塞事件循环）
import { readFileSync } from 'node:fs'  // 只在启动阶段允许
```

### 环境变量
```typescript
// ✅ 统一读取+类型转换+默认值
const PORT = Number(process.env.PORT) || 3000
const DEBUG = process.env.DEBUG === 'true'
const DB_URL = process.env.DATABASE_URL ?? ''
if (!DB_URL) throw new Error('DATABASE_URL未配置')
```

### 进程信号处理
```typescript
// 优雅关闭
process.on('SIGTERM', async () => {
  console.log('收到SIGTERM，开始优雅关闭...')
  await server.close()
  await db.disconnect()
  process.exit(0)
})
```

## 包管理

```bash
# npm
npm install package          # 安装依赖
npm install -D package       # 开发依赖
npm ci                       # CI环境安装（严格按lockfile）
npm audit                    # 安全漏洞检查
npx package                  # 临时执行

# pnpm（推荐，更快+节省磁盘）
pnpm add package
pnpm add -D package
pnpm install --frozen-lockfile  # CI环境
```

## 常见陷阱

| 陷阱 | 示例 | 正确做法 |
|------|------|----------|
| 浮点精度 | `0.1 + 0.2 !== 0.3` | 金额用整数分表示 |
| this丢失 | `setTimeout(obj.method, 100)` | 箭头函数或.bind() |
| 数组判断 | `typeof [] === 'object'` | `Array.isArray(arr)` |
| 对象拷贝 | `{...obj}`只是浅拷贝 | `structuredClone(obj)`深拷贝 |
| for...in | 会遍历原型链属性 | 用`for...of`或`Object.keys()` |
| parseInt | `parseInt('08') === 0`(旧) | 始终传基数`parseInt(s, 10)` |
| JSON丢失 | `JSON.stringify`会丢失undefined/函数/Symbol | 序列化前检查数据类型 |

## TypeScript 5.x 现代特性

### satisfies（类型检查不拓宽）
```typescript
// ✅ 保留字面量类型，同时检查满足接口
const config = {
  port: 3000,
  host: "localhost",
} satisfies Record<string, string | number>
// config.port 的类型是 3000（不是number），config.host 是 "localhost"（不是string）
```

### using 声明（显式资源管理 - TS 5.2+）
```typescript
// 自动释放资源（类似Go的defer/Python的with）
function processFile() {
  using file = openFile("data.txt")
  // 作用域结束自动调用 file[Symbol.dispose]()
}

// 异步版
async function fetchData() {
  await using conn = await getConnection()
  // 作用域结束自动 await conn[Symbol.asyncDispose]()
}
```

### const 类型参数 (TS 5.0+)
```typescript
function createRoute<const T extends string[]>(paths: T): T {
  return paths
}
const routes = createRoute(["home", "about"])  // 类型是 ["home", "about"] 不是 string[]
```

## 运行时类型校验（Zod）

```typescript
import { z } from "zod"

// 定义Schema = 运行时校验 + 类型推导一体
const UserSchema = z.object({
  id: z.number(),
  name: z.string().min(1).max(50),
  email: z.string().email().optional(),
  role: z.enum(["admin", "user"]).default("user"),
})

// 自动推导TS类型
type User = z.infer<typeof UserSchema>

// API入参校验
const result = UserSchema.safeParse(requestBody)
if (!result.success) {
  return res.status(400).json({ errors: result.error.flatten() })
}
const user: User = result.data  // 类型安全
```

## 高级异步模式

### AbortController（请求超时/取消）
```typescript
// 超时控制
async function fetchWithTimeout(url: string, ms: number) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), ms)
  try {
    return await fetch(url, { signal: controller.signal })
  } finally {
    clearTimeout(timeout)
  }
}

// 取消所有并发请求
const controller = new AbortController()
const requests = urls.map(url => fetch(url, { signal: controller.signal }))
// 某个条件触发时取消所有
controller.abort()
```

### p-limit（并发数控制）
```typescript
import pLimit from "p-limit"
const limit = pLimit(5)  // 最多5个并发

const results = await Promise.all(
  urls.map(url => limit(() => fetch(url).then(r => r.json())))
)
```

### 重试模式
```typescript
async function withRetry<T>(fn: () => Promise<T>, retries = 3, delay = 1000): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try { return await fn() }
    catch (err) {
      if (i === retries - 1) throw err
      await new Promise(r => setTimeout(r, delay * 2 ** i))  // 指数退避
    }
  }
  throw new Error("unreachable")
}
```

## 约束
- 所有发现必须有file:line引用
- 遵循项目已有的代码风格（ESLint/Prettier配置）
- 优先标准API（`fetch`/`URL`/`URLSearchParams`），不引入不必要的库
- Node.js内置模块用`node:`前缀（`import { readFile } from 'node:fs/promises'`）
- 保持项目现有风格，不引入新范式
