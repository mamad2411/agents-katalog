---
name: vtj-scene-management
description: Orchestrates World lifecycle and component initialization. Use when managing initialization order, update sequences, or implementing proper disposal chains.
---

# vite-threejs Scene Management

## Overview

World 类作为场景 orchestrator，管理所有 3D 组件的生命周期。核心原则：**等待资源、顺序注册、顺序更新、逆序清理**。

## When to Use

- 创建新的 World 或主场景管理器
- 添加新的 3D 组件到场景
- 管理组件初始化顺序
- 确保资源正确清理

## Core Patterns

### 1. 等待资源 (Wait for Resources)

所有依赖资源的组件在 `core:ready` 后初始化：

```javascript
constructor() {
  this.experience = new Experience()

  emitter.on('core:ready', () => {
    // 资源已加载完成，开始初始化
    this.initComponents()
  })
}
```

### 2. 顺序注册 (Registration Order)

示例: 按依赖关系顺序创建组件：

```javascript
initComponents() {
  // 1. 先初始化地形（玩家需要地形数据）
  this.chunkManager = new ChunkManager()

  // 2. 再初始化玩家（需要地形做碰撞检测）
  this.player = new Player()

  // 3. 相机跟随玩家
  this.cameraRig = new CameraRig()
  this.cameraRig.attachPlayer(this.player)

  // 4. 环境效果
  this.environment = new Environment()

  // 5. 交互系统（依赖地形和玩家）
  this.blockRaycaster = new BlockRaycaster({
    chunkManager: this.chunkManager
  })
}
```

### 3. 顺序更新 (Update Order)

update() 中按依赖顺序调用：

```javascript
update() {
  // 1. 先更新地形流式加载
  this.chunkManager?.updateStreaming()
  this.chunkManager?.update()

  // 2. 玩家依赖地形数据
  this.player?.update()

  // 3. 环境效果
  this.environment?.update()

  // 4. 交互系统
  this.blockRaycaster?.update()
}
```

### 4. 逆序清理 (Reverse Disposal)

destroy() 中按相反顺序清理：

```javascript
destroy() {
  // 与注册顺序相反：后创建的先销毁
  this.blockRaycaster?.destroy()      // 5
  this.environment?.destroy()         // 4
  this.cameraRig?.destroy()           // 3
  this.player?.destroy()              // 2
  this.chunkManager?.destroy()        // 1
}
```

## Quick Reference

| 阶段 | 原则 | 代码位置 |
|------|------|----------|
| 初始化 | 等待 core:ready | `emitter.on('core:ready', ...)` |
| 注册 | 依赖先行 | constructor 或 init 方法 |
| 更新 | 数据流顺序 | `update()` 方法 |
| 清理 | 逆序销毁 | `destroy()` 方法 |

## Common Mistakes

### ❌ 在 core:ready 之前访问资源
```javascript
// BAD
constructor() {
  this.model = this.resources.items['playerModel']  // undefined!
}

// GOOD
emitter.on('core:ready', () => {
  this.model = this.resources.items['playerModel']
})
```

### ❌ 忘记更新子组件
```javascript
// BAD
update() {
  // 没有调用 chunkManager.update()
  this.player.update()
}

// GOOD
update() {
  this.chunkManager?.update()
  this.player?.update()
}
```

### ❌ 清理顺序错误
```javascript
// BAD: 先销毁 chunkManager，但 player 还在引用它
destroy() {
  this.chunkManager?.destroy()
  this.player?.destroy()  // 可能崩溃
}

// GOOD: 先销毁依赖者
destroy() {
  this.player?.destroy()
  this.chunkManager?.destroy()
}
```
