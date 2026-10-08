---
name: vtj-anti-patterns
description: Prevents common mistakes and prohibited practices in vite-threejs projects. Use before writing code to avoid bugs, memory leaks, and maintenance issues.
---

# vite-threejs Anti-Patterns (禁止事项)

## Overview

本文档列出本项目中 **禁止的做法**。违反这些规则会导致 bug、内存泄漏或维护困难。

**在编写任何代码之前，请先检查此列表。**

## 禁止清单

### 1. 类型安全

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| `as any` | 隐藏类型错误 | 正确定义类型 |
| `@ts-ignore` | 绕过检查 | 修复类型问题 |
| `@ts-expect-error` | 绕过检查 | 修复类型问题 |

```javascript
// ❌ FORBIDDEN
const value = someObject as any
// @ts-ignore
problematicCode()

// ✅ CORRECT
const value = someObject // 确保类型正确
```

### 2. 错误处理

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 空 catch 块 | 吞掉错误，调试困难 | 记录或重新抛出 |
| 删除失败的测试 | 隐藏问题 | 修复测试或标记 skip |

```javascript
// ❌ FORBIDDEN
try {
  riskyOperation()
}
catch (e) {} // 空 catch！

// ✅ CORRECT
try {
  riskyOperation()
}
catch (e) {
  console.error('Operation failed:', e)
  // 或重新抛出
  throw e
}
```

### 3. 资源管理

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 缺少 destroy() | 内存泄漏 | 涉及 Object3D 必须实现 |
| 不清理事件监听 | 内存泄漏 | destroy() 中 emitter.off() |
| 不 dispose 材质/几何体 | GPU 内存泄漏 | 销毁时 dispose() |

```javascript
// ❌ FORBIDDEN: 创建 mesh 但没有 destroy
class BadComponent {
  constructor() {
    this.mesh = new THREE.Mesh(...)
    this.scene.add(this.mesh)
    emitter.on('event', this.handler.bind(this))
  }
  // 没有 destroy() → 泄漏！
}

// ✅ CORRECT
class GoodComponent {
  constructor() {
    this.mesh = new THREE.Mesh(...)
    this.scene.add(this.mesh)
    this._boundHandler = this.handler.bind(this)
    emitter.on('event', this._boundHandler)
  }

  destroy() {
    emitter.off('event', this._boundHandler)
    this.scene.remove(this.mesh)
    this.mesh.geometry?.dispose()
    this.mesh.material?.dispose()
    this.mesh = null
  }
}
```

### 4. 输入处理

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 手动计算 NDC | 不一致，易出错 | 使用 iMouse.normalizedMouse |
| 直接监听 window 事件 | 绕过输入系统 | 使用 mitt 事件 |
| 匿名事件监听器 | 无法清理 | 保存函数引用 |

```javascript
// ❌ FORBIDDEN
const x = (event.clientX / window.innerWidth) * 2 - 1
window.addEventListener('keydown', e => this.handle(e))
emitter.on('event', data => this.process(data))

// ✅ CORRECT
const ndc = this.iMouse.normalizedMouse
emitter.on('input:jump', this._boundHandler) // 保存引用
```

### 5. 层分离

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| Vue 直接操作 Three.js | 破坏解耦 | 通过 mitt 事件 |
| Vue 导入 3D 组件类 | 职责混淆 | 只通过事件交互 |
| Three.js 直接写 Pinia | 违反数据流 | emit 事件让 Vue 处理 |

```javascript
// ❌ FORBIDDEN (在 Vue 中)
import Experience from '@three/experience.js'
const exp = new Experience()
exp.world.player.setPosition(0, 0, 0)

// ✅ CORRECT
emitter.emit('game:player-teleport', { x: 0, y: 0, z: 0 })
```

### 6. 调试方法

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| `debuggerInit()` | 命名不一致 | 使用 `debugInit()` |
| `setDebug()` | 命名不一致 | 使用 `debugInit()` |
| 直接访问 debug.ui | 跳过 active 检查 | 先检查 debug.active |

```javascript
// ❌ FORBIDDEN
debuggerInit() { ... }
setDebug() { ... }
this.debug = this.experience.debug.ui

// ✅ CORRECT
constructor() {
  this.debug = this.experience.debug
  if (this.debug.active) {
    this.debugInit()
  }
}
debugInit() {
  this.debugFolder = this.debug.ui.addFolder(...)
}
```

### 7. 时间访问

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 通过参数传递 deltaTime | 不一致 | 通过 Experience 访问 |

```javascript
// ❌ FORBIDDEN
update(deltaTime) {
  this.mesh.rotation.y += deltaTime
}

// ✅ CORRECT
update() {
  const delta = this.experience.time.delta
  this.mesh.rotation.y += delta * 0.001
}
```

### 8. 着色器

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 着色器放 js 目录 | 组织混乱 | 放 src/shaders/ |
| 无调试面板的 uniform | 无法调参 | 必须有 debugInit |
| 颜色不用 view: 'color' | 调参困难 | Tweakpane 用 color view |

```javascript
// ❌ FORBIDDEN
import shader from './world/effect.glsl'  // 在 js 目录

folder.addBinding(config, 'color')  // 没有 view: 'color'

// ✅ CORRECT
import shader from '@/shaders/effect/fragment.glsl'

folder.addBinding(config, 'color', { view: 'color' })
```

### 9. 性能

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 每个对象创建几何体 | 内存浪费 | 共享几何体 |
| splice 移除实例 | O(n) 复杂度 | swap-and-pop |
| 主线程阻塞操作 | 卡顿 | 使用 IdleQueue |
| 忘记 needsUpdate | 渲染不更新 | 修改后标记 |

```javascript
// ❌ FORBIDDEN
blocks.forEach((b) => {
  const geo = new THREE.BoxGeometry(1, 1, 1) // 每个都创建！
})
instances.splice(index, 1) // O(n)

// ✅ CORRECT
const sharedGeo = new THREE.BoxGeometry(1, 1, 1) // 共享
instances[index] = instances[instances.length - 1]
instances.pop() // O(1)
```

### 10. Git 操作

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 未请求时 commit | 过度主动 | 只在明确请求时 |
| 无验证就声称完成 | 可能有问题 | 先运行诊断 |
| 修改 bug 时重构 | 范围蔓延 | Bug 修复要最小化 |

### 11. 组件结构

| 禁止 | 原因 | 正确做法 |
|------|------|----------|
| 不使用 Experience 单例 | 不一致 | `new Experience()` 获取 |
| 提取全部依赖 | 冗余 | 只取所需 |
| 继承 EventEmitter | 已弃用 | 使用 mitt |

```javascript
// ❌ FORBIDDEN
class BadComponent extends EventEmitter {
  constructor() {
    // 提取全部
    this.scene = exp.scene
    this.camera = exp.camera
    this.renderer = exp.renderer
    this.time = exp.time
    this.sizes = exp.sizes
    this.iMouse = exp.iMouse // 大部分用不到
  }
}

// ✅ CORRECT
class GoodComponent {
  constructor() {
    this.experience = new Experience()
    // 只取需要的
    this.scene = this.experience.scene
    this.resources = this.experience.resources
  }
}
```

## 检查清单

在提交代码前，确认以下事项：

- [ ] 没有 `as any`、`@ts-ignore`、`@ts-expect-error`
- [ ] 没有空的 catch 块
- [ ] 涉及 Object3D 的类都有 `destroy()` 方法
- [ ] 所有事件监听在 destroy 中清理
- [ ] 射线拾取使用 `iMouse.normalizedMouse`
- [ ] Vue 和 Three.js 之间只通过 mitt 通信
- [ ] 调试方法命名为 `debugInit()`
- [ ] 时间通过 `this.experience.time` 访问
- [ ] 着色器在 `src/shaders/` 目录
- [ ] ShaderMaterial 的 uniform 有调试面板
- [ ] 颜色控件使用 `view: 'color'`
- [ ] 没有主线程阻塞操作
- [ ] InstancedMesh 修改后调用 `needsUpdate = true`

## 严重程度

| 级别 | 说明 | 示例 |
|------|------|------|
| 🔴 CRITICAL | 必然导致 bug 或崩溃 | 缺少 destroy、空 catch |
| 🟠 HIGH | 导致性能问题或内存泄漏 | splice 移除、不 dispose |
| 🟡 MEDIUM | 违反架构规范 | 跨层直接操作 |
| 🟢 LOW | 代码风格问题 | 命名不一致 |

**所有级别的违规都应避免。**
