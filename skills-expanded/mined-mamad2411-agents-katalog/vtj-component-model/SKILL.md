---
name: vtj-component-model
description: Creates 3D components using the Experience singleton pattern. Use when building new classes in src/js/, implementing lifecycle methods, or managing Three.js objects.
---

# vite-threejs 3D Component Model

## Overview

All 3D components in this project follow a **class-based singleton pattern**. Components access shared resources through the `Experience` singleton and implement standardized lifecycle methods.

**Core principle**: Extract only what you need, implement all required lifecycle methods, always clean up resources.

## When to Use

- Creating any new class in `src/js/`
- Building 3D objects, managers, controllers, or utilities that interact with the scene
- Wrapping Three.js functionality in reusable components

## Component Template

```javascript
import Experience from '@/js/experience.js'
import emitter from '@/js/utils/event-bus.js'
import * as THREE from 'three'

export default class YourComponent {
  constructor(options = {}) {
    // 1. 获取 Experience 单例
    this.experience = new Experience()

    // 2. 按需提取依赖（仅取所需，避免冗余）
    this.scene = this.experience.scene
    this.resources = this.experience.resources
    this.debug = this.experience.debug

    // 3. 组件参数
    this.params = {
      enabled: options.enabled ?? true,
      // ... 其他参数
    }

    // 4. 组件状态
    this.mesh = null

    // 5. 初始化
    this._init()

    // 6. 调试面板（必须在 debug.active 条件下调用）
    if (this.debug.active) {
      this.debugInit()
    }
  }

  _init() {
    // 创建 3D 对象并添加到场景
    this.mesh = new THREE.Mesh(/* ... */)
    this.scene.add(this.mesh)
  }

  debugInit() {
    // 调试面板 - 详见 vtj-debug-panel skill
  }

  update() {
    // 每帧更新逻辑
    // 时间通过 this.experience.time 访问，不通过参数传递
  }

  resize() {
    // 窗口尺寸变化时调用
  }

  destroy() {
    // 清理资源 - 涉及 Object3D 的组件必须实现
    if (this.mesh) {
      this.scene.remove(this.mesh)
      this.mesh.geometry?.dispose()
      this.mesh.material?.dispose()
      this.mesh = null
    }
  }
}
```

## Dependency Extraction Rules

**只提取组件实际需要的依赖**：

| 组件类型 | 典型依赖 |
|----------|----------|
| 渲染对象 | `scene`, `resources` |
| 交互组件 | `scene`, `camera.instance`, `iMouse` |
| 动画组件 | `scene`, `time` |
| 调试组件 | `debug` |
| UI 相关 | `sizes`, `canvas` |

```javascript
// ✅ GOOD: 只取所需
this.scene = this.experience.scene
this.resources = this.experience.resources

// ❌ BAD: 提取全部
this.scene = this.experience.scene
this.camera = this.experience.camera
this.renderer = this.experience.renderer
this.time = this.experience.time
this.sizes = this.experience.sizes
this.iMouse = this.experience.iMouse
this.debug = this.experience.debug
// ... 大部分根本用不到
```

## Lifecycle Methods

| 方法 | 必需条件 | 调用方 |
|------|----------|--------|
| `debugInit()` | 有可调参数 | 构造函数，`if (debug.active)` |
| `update()` | 有逐帧逻辑 | 父组件的 `update()` |
| `resize()` | 响应尺寸变化 | 父组件的 `resize()` |
| `destroy()` | **涉及 Object3D** | 父组件的 `destroy()` |

### destroy() 是强制要求

**任何涉及 Object3D 的组件必须实现 `destroy()` 方法**。

```javascript
destroy() {
  // 1. 移除事件监听
  emitter.off('some:event', this._handler)

  // 2. 从场景移除对象
  if (this.mesh) {
    this.scene.remove(this.mesh)
  }

  // 3. 销毁几何体
  this.mesh?.geometry?.dispose()

  // 4. 销毁材质
  if (this.mesh?.material) {
    if (Array.isArray(this.mesh.material)) {
      this.mesh.material.forEach(m => m.dispose())
    } else {
      this.mesh.material.dispose()
    }
  }

  // 5. 销毁纹理（如果组件自己创建的）
  this.texture?.dispose()

  // 6. 销毁子组件
  this.childComponent?.destroy()

  // 7. 清空引用
  this.mesh = null
}
```

## Debug Access Pattern

**统一使用以下方式访问调试系统**：

```javascript
// 在构造函数中
this.debug = this.experience.debug

// 检查是否激活
if (this.debug.active) {
  this.debugInit()
}

// 在 debugInit() 中创建面板
debugInit() {
  this.debugFolder = this.debug.ui.addFolder({
    title: 'Component Name',
    expanded: false,
  })

  this.debugFolder.addBinding(this.params, 'someValue', {
    label: '参数名称',
    min: 0,
    max: 1,
  })
}
```

**注意**：
- 方法名统一使用 `debugInit()`（不是 `debugInit` 或 `setDebug`）
- 通过 `this.debug.ui` 访问 Tweakpane 实例
- 通过 `this.debug.active` 判断是否启用

## Common Mistakes

### ❌ 缺少 destroy() 方法

```javascript
// BAD: 组件创建了 mesh 但没有 destroy
class BadComponent {
  constructor() {
    this.mesh = new THREE.Mesh(...)
    this.scene.add(this.mesh)
  }
  // 没有 destroy() → 内存泄漏
}
```

### ❌ 调试方法命名不一致

```javascript
// BAD: 使用其他命名
debuggerInit() { }      // ❌
setDebug() { }       // ❌

// GOOD: 统一命名
debugInit() { }   // ✅
```

### ❌ 直接访问 debug.ui 而非 debug

```javascript
// BAD: 直接提取 ui
this.debug = this.experience.debug.ui // ❌

// GOOD: 提取 debug 对象
this.debug = this.experience.debug // ✅
// 然后通过 this.debug.ui 访问面板
```

### ❌ 事件监听未清理

```javascript
// BAD: 绑定事件但没清理
constructor() {
  emitter.on('game:event', this.handler.bind(this))
}
// 没有在 destroy() 中 emitter.off()

// GOOD: 保存引用并清理
constructor() {
  this._boundHandler = this.handler.bind(this)
  emitter.on('game:event', this._boundHandler)
}
destroy() {
  emitter.off('game:event', this._boundHandler)
}
```

### ❌ 通过 update() 参数传递时间

```javascript
// BAD: 通过参数传递
update(deltaTime) {
  this.mesh.rotation.y += deltaTime
}

// GOOD: 通过 Experience 访问
update() {
  const delta = this.experience.time.delta
  this.mesh.rotation.y += delta * 0.001
}
```

## Special Case: Independent Scene

如需创建独立于主场景的 3D 视图（如 UI 预览），**不使用 Experience 单例**：

```javascript
// 参考 src/js/components/skin-preview-scene.js
class IndependentScene {
  constructor(canvas) {
    // 创建独立的 scene/camera/renderer
    this.scene = new THREE.Scene()
    this.camera = new THREE.PerspectiveCamera(...)
    this.renderer = new THREE.WebGLRenderer({ canvas })
  }
}
```

这是唯一允许不使用 Experience 单例的情况。

## Quick Reference

| 规则 | 要求 |
|------|------|
| 单例访问 | `this.experience = new Experience()` |
| 依赖提取 | 只取所需 |
| 调试方法 | `debugInit()`（统一命名） |
| 调试访问 | `this.debug = this.experience.debug` |
| 时间访问 | `this.experience.time`（不通过参数） |
| destroy | 涉及 Object3D 必须实现 |
| 事件清理 | destroy() 中 `emitter.off()` |
