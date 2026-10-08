---
name: vtj-ui-integration
description: Integrates Vue UI with Three.js while maintaining strict separation. Use when building HUDs, menus, or handling UI-to-scene communication via events.
---

# vite-threejs UI Integration (Vue ↔ Three.js)

## Overview

本项目采用 **严格的层分离架构**：
- **Vue 层**：UI、用户输入、菜单、HUD
- **Three.js 层**：3D 场景、渲染、游戏逻辑

两层之间 **禁止直接操作**，所有通信通过 Pinia + mitt 完成。

## When to Use

- 创建需要与 3D 场景交互的 Vue 组件
- 从 Three.js 更新 UI 状态
- 处理用户输入并影响 3D 场景
- 管理游戏状态（暂停、菜单、设置）

## 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         Vue UI Layer                         │
│  ┌─────────────────┐          ┌─────────────────┐           │
│  │   Components    │◄────────►│   Pinia Stores  │           │
│  │   (src/vue/)    │          │   (src/pinia/)  │           │
│  └─────────────────┘          └────────┬────────┘           │
└────────────────────────────────────────┼────────────────────┘
                                         │ emitter.emit()
                                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      mitt Event Bus                          │
│                  (src/js/utils/event-bus.js)                 │
└─────────────────────────────────────────────────────────────┘
                                         │ emitter.on()
                                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Three.js Layer                          │
│  ┌─────────────────┐          ┌─────────────────┐           │
│  │   Components    │◄────────►│   Experience    │           │
│  │   (src/js/)     │          │   (singleton)   │           │
│  └─────────────────┘          └─────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## 职责分离

| 层 | 职责 | 示例 |
|----|------|------|
| **Vue** | 界面渲染、用户输入、菜单导航 | HUD、暂停菜单、设置面板 |
| **Three.js** | 3D 渲染、物理、动画、游戏逻辑 | 玩家移动、地形生成、相机控制 |

### Vue 层 (src/vue/)

```
src/vue/
├── components/
│   ├── hud/           # 游戏内 HUD（血条、快捷栏等）
│   │   ├── HealthBar.vue
│   │   ├── Hotbar.vue
│   │   └── GameHud.vue
│   ├── menu/          # 菜单系统
│   │   ├── UiRoot.vue       # 菜单根组件
│   │   ├── MainMenu.vue
│   │   ├── PauseMenu.vue
│   │   └── SettingsMenu.vue
│   └── ui/            # 共享 UI 元素
```

### Three.js 层 (src/js/)

```
src/js/
├── experience.js      # 单例入口
├── world/             # 场景元素
├── camera/            # 相机系统
├── interaction/       # 交互系统
└── utils/
    └── event-bus.js   # mitt 实例
```

## 通信模式

### 模式一：UI → Three.js（最常用）

**场景**：用户在 UI 操作，需要影响 3D 场景

```javascript
// 1. Pinia Store 定义 action
// src/pinia/uiStore.js
function toPlaying() {
  screen.value = 'playing'
  isPaused.value = false
  emitter.emit('ui:pause-changed', false)  // 通知 Three.js
  emitter.emit('game:request_pointer_lock')
}

// 2. Three.js 组件监听
// src/js/world/player.js
constructor() {
  this._handlePause = this._handlePause.bind(this)
  emitter.on('ui:pause-changed', this._handlePause)
}

_handlePause(paused) {
  this.isPaused = paused
}

destroy() {
  emitter.off('ui:pause-changed', this._handlePause)
}
```

### 模式二：Three.js → UI

**场景**：3D 场景状态变化，需要更新 UI

```javascript
// 1. Three.js 中发送事件
// src/js/world/player.js
takeDamage(amount) {
  this.health -= amount
  emitter.emit('game:player-health-changed', { 
    health: this.health, 
    maxHealth: this.maxHealth 
  })
}

// 2. Vue 组件监听
// src/vue/components/hud/HealthBar.vue
<script setup>
import emitter from '@three/utils/event-bus.js'
import { onMounted, onUnmounted, ref } from 'vue'

const health = ref(100)
const maxHealth = ref(100)

function handleHealthChange({ health: h, maxHealth: max }) {
  health.value = h
  maxHealth.value = max
}

onMounted(() => {
  emitter.on('game:player-health-changed', handleHealthChange)
})

onUnmounted(() => {
  emitter.off('game:player-health-changed', handleHealthChange)
})
</script>
```

### 模式三：设置变更

**场景**：用户修改设置，Three.js 需要响应

```javascript
// 1. Pinia Store
// src/pinia/settingsStore.js
function setShadowQuality(quality) {
  shadowQuality.value = quality
  emitter.emit('shadow:quality-changed', quality)
  saveSettings()
}

// 2. Three.js Renderer 响应
// src/js/renderer.js
emitter.on('shadow:quality-changed', (quality) => {
  this.updateShadowMapSize(quality)
})
```

## Vue 组件模板

### 带事件监听的组件

```vue
<script setup>
import emitter from '@three/utils/event-bus.js'
import { onMounted, onUnmounted, ref } from 'vue'

// 状态
const value = ref(0)

// 事件处理函数（必须保存引用以便清理）
function handleEvent(data) {
  value.value = data.value
}

// 生命周期
onMounted(() => {
  emitter.on('game:some-event', handleEvent)
})

onUnmounted(() => {
  emitter.off('game:some-event', handleEvent)  // 必须清理！
})

// 发送事件到 Three.js
function triggerAction() {
  emitter.emit('ui:some-action', { param: 'value' })
}
</script>
```

### 菜单组件

```vue
<script setup>
import { useUiStore } from '@pinia/uiStore.js'

const ui = useUiStore()

function handlePlay() {
  ui.toPlaying()  // Pinia action 内部会 emit 事件
}

function handleSettings() {
  ui.toSettings('mainMenu')
}
</script>

<template>
  <div class="menu">
    <button @click="handlePlay">Play</button>
    <button @click="handleSettings">Settings</button>
  </div>
</template>
```

## 现有 Stores

| Store | 文件 | 职责 |
|-------|------|------|
| `useUiStore` | `uiStore.js` | 屏幕状态、菜单导航、世界管理 |
| `useSettingsStore` | `settingsStore.js` | 游戏设置、持久化、Three.js 通知 |
| `useHudStore` | `hudStore.js` | HUD 状态（血量、快捷栏等） |
| `useSkinStore` | `skinStore.js` | 皮肤选择状态 |

## 事件命名规范

详见 `vtj-state-management` skill，此处简要回顾：

| 前缀 | 来源 | 示例 |
|------|------|------|
| `ui:` | Vue UI | `ui:pause-changed` |
| `game:` | 游戏逻辑 | `game:create_world` |
| `settings:` | 设置变更 | `settings:environment-changed` |
| `core:` | 系统级 | `core:ready`, `core:resize` |

## 路径别名

Vue 组件中使用标准别名：

```javascript
// ✅ GOOD: 使用别名
import emitter from '@three/utils/event-bus.js'
import { useUiStore } from '@pinia/uiStore.js'

// ❌ BAD: 相对路径
import emitter from '../../../js/utils/event-bus.js'
```

| 别名 | 路径 |
|------|------|
| `@` | `src/` |
| `@ui` | `src/vue/` |
| `@ui-components` | `src/vue/components/` |
| `@pinia` | `src/pinia/` |
| `@three` | `src/js/` |

## Common Mistakes

### ❌ 在 Vue 中直接操作 Three.js

```javascript
// BAD: 直接操作 Three.js 实例
import Experience from '@three/experience.js'

function handleTeleport() {
  const exp = new Experience()
  exp.world.player.setPosition(0, 0, 0)  // ❌ 违反层分离
}

// GOOD: 通过事件通信
function handleTeleport() {
  emitter.emit('game:player-teleport', { x: 0, y: 0, z: 0 })
}
```

### ❌ 忘记清理事件监听

```vue
<script setup>
// BAD: 没有 onUnmounted 清理
onMounted(() => {
  emitter.on('game:event', handleEvent)  // 内存泄漏！
})

// GOOD: 完整生命周期
onMounted(() => {
  emitter.on('game:event', handleEvent)
})

onUnmounted(() => {
  emitter.off('game:event', handleEvent)
})
</script>
```

### ❌ 在 Three.js 中直接修改 Pinia

```javascript
// BAD: Three.js 直接写 Pinia
import { useUiStore } from '@pinia/uiStore.js'

function onPlayerDeath() {
  const ui = useUiStore()
  ui.screen = 'gameOver'  // ❌ 跨层直接操作
}

// GOOD: 通过事件让 Vue 层处理
function onPlayerDeath() {
  emitter.emit('game:player-died')
}

// Vue 层响应
emitter.on('game:player-died', () => {
  ui.toGameOver()
})
```

### ❌ 匿名函数无法清理

```javascript
// BAD: 匿名函数
emitter.on('game:event', (data) => this.handle(data))  // 无法 off

// GOOD: 保存引用
this._boundHandler = this.handle.bind(this)
emitter.on('game:event', this._boundHandler)
// ...
emitter.off('game:event', this._boundHandler)
```

### ❌ 在 Vue 中导入 Three.js 组件类

```javascript
// BAD: 导入并实例化 Three.js 组件
import Player from '@three/world/player.js'

const player = new Player()  // ❌ Vue 不应该创建 3D 组件

// GOOD: 只通过事件/状态交互
emitter.emit('game:spawn-player', { x: 0, y: 0, z: 0 })
```

## 允许的例外

### 独立预览场景

用于 UI 预览的独立 Three.js 场景（如皮肤预览）可以在 Vue 组件中创建：

```javascript
// src/js/components/skin-preview-scene.js
// 这是独立场景，不使用 Experience 单例
class SkinPreviewScene {
  constructor(canvas) {
    this.scene = new THREE.Scene()
    this.camera = new THREE.PerspectiveCamera(...)
    this.renderer = new THREE.WebGLRenderer({ canvas })
  }
}
```

```vue
<!-- src/vue/components/menu/SkinSelector.vue -->
<script setup>
import SkinPreviewScene from '@three/components/skin-preview-scene.js'
import { onMounted, onUnmounted, ref } from 'vue'

const canvasRef = ref(null)
let preview = null

onMounted(() => {
  preview = new SkinPreviewScene(canvasRef.value)
})

onUnmounted(() => {
  preview?.destroy()
})
</script>
```

这是唯一允许 Vue 直接操作 Three.js 的情况，因为是隔离的预览场景。

## Quick Reference

| 需求 | 解决方案 |
|------|----------|
| UI 触发 3D 动作 | Pinia action → `emitter.emit()` |
| 3D 更新 UI | `emitter.emit()` → Vue `emitter.on()` |
| 共享状态 | Pinia Store |
| 即时通知 | mitt 事件 |
| Vue 读取 3D 状态 | 通过 Pinia（3D 写入 Pinia 或 emit 事件） |

| 禁止 | 原因 |
|------|------|
| Vue 直接操作 Experience | 破坏层分离 |
| Vue 导入 3D 组件类 | 职责混淆 |
| Three.js 直接写 Pinia | 违反单向数据流 |
| 匿名事件监听器 | 无法清理，内存泄漏 |
