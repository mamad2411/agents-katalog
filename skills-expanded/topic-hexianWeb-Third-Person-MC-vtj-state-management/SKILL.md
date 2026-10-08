---
name: vtj-state-management
description: Manages state between Vue and Three.js via Pinia and mitt. Use when synchronizing UI state, emitting events, or implementing cross-layer communication.
---

# vite-threejs State Management (Pinia + mitt)

## Overview

本项目使用 **双通道状态管理**：
- **Pinia**：持久化状态，Vue 和 Three.js 双向同步
- **mitt**：即时事件通知，跨层通信

**核心原则**：Pinia 管状态，mitt 管事件。状态变更通过 Pinia，通知 Three.js 通过 mitt emit。

## When to Use

- 需要在 Vue UI 和 Three.js 之间共享状态
- 需要从 UI 触发 3D 场景行为
- 需要从 3D 场景通知 UI 更新
- 管理游戏设置、用户偏好等持久状态

## 双通道架构

```
┌─────────────────────────────────────────────────────────────┐
│                         Vue UI Layer                         │
│  ┌─────────────────┐          ┌─────────────────┐           │
│  │   Components    │◄────────►│   Pinia Stores  │           │
│  └─────────────────┘          └────────┬────────┘           │
└────────────────────────────────────────┼────────────────────┘
                                         │ emitter.emit()
                                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      mitt Event Bus                          │
└─────────────────────────────────────────────────────────────┘
                                         │ emitter.on()
                                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Three.js Layer                          │
│  ┌─────────────────┐          ┌─────────────────┐           │
│  │   Components    │◄────────►│   Experience    │           │
│  └─────────────────┘          └─────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Pinia Store 模式

### Store 定义

```javascript
// src/pinia/settingsStore.js
import emitter from '@three/utils/event-bus.js'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  // 状态
  const shadowQuality = ref('high')
  
  // Action：修改状态 + 通知 Three.js
  function setShadowQuality(quality) {
    shadowQuality.value = quality
    emitter.emit('shadow:quality-changed', quality)  // 通知 Three.js
    saveSettings()  // 持久化
  }
  
  return { shadowQuality, setShadowQuality }
})
```

### 在 Vue 中使用

```vue
<script setup>
import { useSettingsStore } from '@pinia/settingsStore.js'

const settings = useSettingsStore()

function handleQualityChange(quality) {
  settings.setShadowQuality(quality)
}
</script>

<template>
  <select v-model="settings.shadowQuality" @change="handleQualityChange">
    <option value="low">Low</option>
    <option value="medium">Medium</option>
    <option value="high">High</option>
  </select>
</template>
```

### 在 Three.js 中使用

```javascript
// 方式一：监听 mitt 事件（推荐）
import emitter from './utils/event-bus.js'

emitter.on('shadow:quality-changed', (quality) => {
  this.updateShadowQuality(quality)
})

// 方式二：直接读取 Pinia（需要时）
import { useSettingsStore } from '@pinia/settingsStore.js'

const settings = useSettingsStore()
const quality = settings.shadowQuality
```

## mitt Event Bus

### 事件总线定义

```javascript
// src/js/utils/event-bus.js
import mitt from 'mitt'
const emitter = mitt()
export default emitter
```

### 事件命名规范

| 前缀 | 来源 | 用途 | 示例 |
|------|------|------|------|
| `ui:` | Vue UI | UI 状态变化 | `ui:pause-changed` |
| `game:` | Vue/Three.js | 游戏逻辑事件 | `game:create_world` |
| `settings:` | Pinia Store | 设置变更通知 | `settings:environment-changed` |
| `core:` | Experience | 核心系统事件 | `core:ready`, `core:resize` |
| `shadow:` | 渲染相关 | 阴影设置 | `shadow:quality-changed` |

### 事件使用模式

```javascript
// 发送事件（Vue/Pinia 层）
emitter.emit('game:create_world', { seed, terrain, trees })
emitter.emit('ui:pause-changed', true)
emitter.emit('settings:environment-changed', { skyMode: 'HDR' })

// 监听事件（Three.js 层）
emitter.on('game:create_world', ({ seed, terrain, trees }) => {
  this.world.reset({ seed, terrain, trees })
})

emitter.on('ui:pause-changed', (paused) => {
  this.isPaused = paused
})

// 移除监听（destroy 时）
this._boundHandler = this.handleEvent.bind(this)
emitter.on('some:event', this._boundHandler)
// ...
emitter.off('some:event', this._boundHandler)
```

## 通信模式

### 模式一：UI → Three.js（最常用）

```javascript
// 1. Pinia Store 中定义 action
function setEnvFogDensity(value) {
  envFogDensity.value = value
  emitter.emit('settings:environment-changed', { fogDensity: value })
  saveSettings()
}

// 2. Three.js 组件监听
emitter.on('settings:environment-changed', (patch) => {
  if (patch.fogDensity !== undefined) {
    this.updateFog(patch.fogDensity)
  }
})
```

### 模式二：Three.js → UI

```javascript
// 1. Three.js 中发送事件
emitter.emit('game:player-health-changed', { health: 80, maxHealth: 100 })

// 2. Vue 组件监听
import emitter from '@three/utils/event-bus.js'
import { onMounted, onUnmounted, ref } from 'vue'

const health = ref(100)

onMounted(() => {
  emitter.on('game:player-health-changed', handleHealthChange)
})

onUnmounted(() => {
  emitter.off('game:player-health-changed', handleHealthChange)
})

function handleHealthChange({ health: newHealth }) {
  health.value = newHealth
}
```

### 模式三：状态同步（双向）

```javascript
// Pinia Store 持有状态
const isPaused = ref(false)

function toPauseMenu() {
  isPaused.value = true
  emitter.emit('ui:pause-changed', true)
}

function toPlaying() {
  isPaused.value = false
  emitter.emit('ui:pause-changed', false)
}

// Three.js 层响应
emitter.on('ui:pause-changed', (paused) => {
  this.isPaused = paused
})
```

## 现有 Stores

| Store | 文件 | 职责 |
|-------|------|------|
| `useUiStore` | `uiStore.js` | 屏幕状态、菜单导航、世界管理 |
| `useSettingsStore` | `settingsStore.js` | 游戏设置、持久化、Three.js 通知 |
| `useHudStore` | `hudStore.js` | HUD 状态（血量、快捷栏等） |
| `useSkinStore` | `skinStore.js` | 皮肤选择状态 |

## 现有事件

### core: 系统事件

| 事件 | 数据 | 触发时机 |
|------|------|----------|
| `core:ready` | - | 所有资源加载完成 |
| `core:resize` | - | 窗口尺寸变化 |
| `core:tick` | - | 每帧更新 |

### ui: UI 事件

| 事件 | 数据 | 触发时机 |
|------|------|----------|
| `ui:pause-changed` | `boolean` | 暂停/恢复 |

### game: 游戏事件

| 事件 | 数据 | 触发时机 |
|------|------|----------|
| `game:create_world` | `{ seed, terrain, trees }` | 创建新世界 |
| `game:reset_world` | `{ seed, terrain, trees }` | 重置世界 |
| `game:request_pointer_lock` | - | 请求锁定鼠标 |

### settings: 设置事件

| 事件 | 数据 | 触发时机 |
|------|------|----------|
| `settings:environment-changed` | `{ skyMode?, sunIntensity?, ... }` | 环境设置变更 |
| `settings:postprocess-changed` | `{ speedLines }` | 后期处理变更 |
| `settings:camera-rig-changed` | `{ fov, bobbing }` | 相机设置变更 |
| `settings:chunks-changed` | `{ viewDistance?, unloadPadding? }` | 区块设置变更 |
| `settings:front-view-changed` | `{ enabled }` | 前视图开关 |
| `settings:mouse-sensitivity-changed` | `number` | 鼠标灵敏度变更 |

### shadow: 阴影事件

| 事件 | 数据 | 触发时机 |
|------|------|----------|
| `shadow:quality-changed` | `string` | 阴影质量变更 |

## Common Mistakes

### ❌ 直接在 Vue 中操作 Three.js

```javascript
// BAD: Vue 组件直接操作 Three.js
import Experience from '@three/experience.js'

function handleClick() {
  const exp = new Experience()
  exp.world.player.setPosition(0, 0, 0)  // ❌ 直接操作
}

// GOOD: 通过 mitt 事件
function handleClick() {
  emitter.emit('game:player-teleport', { x: 0, y: 0, z: 0 })
}
```

### ❌ 忘记清理事件监听

```javascript
// BAD: 没有清理
constructor() {
  emitter.on('some:event', (data) => this.handle(data))
}

// GOOD: 保存引用并清理
constructor() {
  this._boundHandler = this.handle.bind(this)
  emitter.on('some:event', this._boundHandler)
}

destroy() {
  emitter.off('some:event', this._boundHandler)
}
```

### ❌ 在 Three.js 中直接修改 Pinia 状态

```javascript
// BAD: Three.js 直接写 Pinia
import { useUiStore } from '@pinia/uiStore.js'

function onPlayerDeath() {
  const ui = useUiStore()
  ui.screen = 'gameOver'  // ❌ 直接写状态
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

### ❌ 事件命名不规范

```javascript
// BAD: 无前缀、大小写混乱
emitter.emit('pauseChanged', true)
emitter.emit('CreateWorld', data)

// GOOD: 使用规范前缀
emitter.emit('ui:pause-changed', true)
emitter.emit('game:create_world', data)
```

### ❌ 事件数据结构不一致

```javascript
// BAD: 有时传对象，有时传原始值
emitter.emit('settings:fog-changed', 0.01)
emitter.emit('settings:fog-changed', { density: 0.01 })

// GOOD: 统一使用对象（可扩展）
emitter.emit('settings:environment-changed', { fogDensity: 0.01 })
```

## Quick Reference

| 场景 | 使用 |
|------|------|
| 持久化状态 | Pinia Store |
| UI → Three.js 通知 | Pinia action + `emitter.emit()` |
| Three.js → UI 通知 | `emitter.emit()` |
| Three.js 读取状态 | Pinia Store 或 `emitter.on()` |
| 事件清理 | `destroy()` 中 `emitter.off()` |

| 事件前缀 | 用途 |
|----------|------|
| `core:` | 系统级（ready/resize/tick） |
| `ui:` | UI 状态变化 |
| `game:` | 游戏逻辑 |
| `settings:` | 设置变更 |
| `shadow:` | 渲染相关 |
