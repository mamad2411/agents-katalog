---
name: test-guardian
description: Test Guardian enforces test discipline. Use when modifying code, fixing bugs, adding features, or before PR submission. Triggers a 4-phase testing workflow and prevents shipping untested code. Trigger on "fix", "add feature", "refactor", "修复", "新增功能", "重构".
---

# Test Guardian - 测试守护者

## 目标
解决"无测试意识"和"测试质量低"的问题，强制执行测试标准。

## 核心原则
**"代码未测试 = 代码未完成"**

## 触发场景
- 任何代码修改（Edit/Write 工具被调用后）
- 用户说"修复 bug"、"添加功能"、"重构"
- PR 提交前

---

## 工作流程

### 阶段1：代码修改前 — 理解现有测试
```markdown
## 📋 测试现状分析

1. **定位测试文件**
   - 搜索对应的测试文件（`*.test.ts`, `*.spec.ts`, `*.test.tsx`）
   - 如果不存在，标记为 🚨 警告

2. **理解现有测试覆盖**
   - 读取现有测试用例
   - 分析覆盖的场景：正常流程、边界条件、异常情况
   - 识别测试空白区

3. **设定测试目标**
   - 本次修改需要新增的测试用例
   - 需要更新的现有测试用例
```

### 阶段2：代码修改时 — 同步编写测试
```markdown
## ✍️ 测试驱动开发（TDD Lite）

### 规则：
1. **修改业务代码前，先写/更新测试**
2. **测试必须覆盖**：
   - ✅ Happy Path（正常流程）
   - ✅ Edge Cases（边界条件）
   - ✅ Error Handling（异常处理）
3. **测试命名规范**：
   ```ts
   it('should <action> when <condition>', () => { ... })
   // 例如：it('should return 401 when user not authenticated', ...)
   ```

### 测试质量标准：
- [ ] 使用 Given-When-Then 结构
- [ ] Mock 外部依赖（数据库、API、文件系统）
- [ ] 断言清晰明确
- [ ] 包含失败时的错误信息
```

### 阶段3：代码修改后 — 运行验证
```bash
# TypeScript / Next.js 项目标准流程

## Step 1: 类型检查（必须）
npx tsc --noEmit

## Step 2: 运行相关测试
npm test -- --testPathPattern=<module_name>

## Step 3: 运行完整测试套件
npm test

## Step 4: 如果测试失败
# 分析失败原因（见阶段4）
```

### 阶段4：测试失败时 — 智能修复
```markdown
## 🔧 测试失败处理流程

### 1. 分析失败原因
- 读取完整的错误堆栈
- 定位失败的断言
- 理解期望值 vs 实际值的差异

### 2. 分类处理

**类型A：代码 Bug**
→ 修复业务逻辑，重新运行测试

**类型B：测试过时**
→ 审查测试是否仍然有效
→ 更新期望值，添加注释说明原因

**类型C：遗漏的边界情况**
→ 补充新的测试用例
→ 修复代码以处理该情况

### 3. 回归验证
- 运行完整测试套件
- 确保没有引入新的失败
```

---

## 测试模板库

### Next.js API Route 测试
```typescript
import { NextRequest } from 'next/server'
import { GET, POST } from '@/app/api/<route>/route'

describe('GET /api/<route>', () => {
  it('should return 200 with data when authenticated', async () => {
    // Given
    const req = new NextRequest('http://localhost/api/<route>', {
      headers: { cookie: 'next-auth.session-token=valid-token' }
    })

    // When
    const res = await GET(req)
    const data = await res.json()

    // Then
    expect(res.status).toBe(200)
    expect(data).toHaveProperty('id')
  })

  it('should return 401 when not authenticated', async () => {
    const req = new NextRequest('http://localhost/api/<route>')
    const res = await GET(req)
    expect(res.status).toBe(401)
  })
})
```

### React Component 测试
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import Component from './Component'

describe('Component', () => {
  it('should render successfully', () => {
    render(<Component title="Test" />)
    expect(screen.getByText('Test')).toBeInTheDocument()
  })

  it('should handle user interaction', async () => {
    const mockOnClick = vi.fn()
    render(<Component onClick={mockOnClick} />)

    fireEvent.click(screen.getByRole('button'))

    await waitFor(() => {
      expect(mockOnClick).toHaveBeenCalledTimes(1)
    })
  })

  it('should show error state on API failure', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('API Error'))
    render(<Component />)

    fireEvent.click(screen.getByText('Load Data'))

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument()
    })
  })
})
```

### Zustand Store 测试
```typescript
import { act, renderHook } from '@testing-library/react'
import { useCanvasStore } from '@/stores/canvasStore'

describe('canvasStore', () => {
  beforeEach(() => {
    useCanvasStore.setState({ nodes: [], edges: [] })
  })

  it('should add node correctly', () => {
    const { result } = renderHook(() => useCanvasStore())

    act(() => {
      result.current.addNode({ id: '1', type: 'text', position: { x: 0, y: 0 }, data: {} })
    })

    expect(result.current.nodes).toHaveLength(1)
    expect(result.current.nodes[0].id).toBe('1')
  })
})
```

---

## 测试覆盖率要求

| 模块类型 | 最低覆盖率 | 推荐覆盖率 |
|---------|----------|----------|
| 核心业务逻辑 | 80% | 90%+ |
| API Route | 90% | 95%+ |
| 工具函数 | 70% | 85%+ |
| UI 组件 | 60% | 75%+ |

---

## 禁止行为

❌ **绝对不允许**：
1. 修改代码后不运行测试
2. 看到测试失败但忽略它
3. 删除测试用例来"修复"测试失败
4. 只写 happy path 测试
5. Mock 掉整个业务逻辑（测试变成摆设）
6. `npx tsc --noEmit` 有错误时提交代码
