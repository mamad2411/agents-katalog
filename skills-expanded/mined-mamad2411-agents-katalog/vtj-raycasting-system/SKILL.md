---
name: vtj-raycasting-system
description: Implements ray picking and collision detection. Use when selecting objects, detecting block interactions, or optimizing raycaster performance.
---

# vite-threejs Raycasting System

## Overview

本项目的射线系统主要用于 **方块交互**（挖掘、放置）和 **目标选择**。

**核心原则**：始终使用 `iMouse.normalizedMouse` 获取 NDC 坐标，射线检测结果通过 mitt 事件通知。

## When to Use

- 实现点击拾取功能
- 检测鼠标悬停对象
- 实现方块交互（挖掘、放置）
- 添加目标锁定功能

## 基础 Raycaster 模式

```javascript
import * as THREE from 'three'
import Experience from './experience.js'
import emitter from './utils/event-bus.js'

export default class ObjectPicker {
  constructor() {
    this.experience = new Experience()
    this.scene = this.experience.scene
    this.camera = this.experience.camera.instance
    this.iMouse = this.experience.iMouse
    
    this.raycaster = new THREE.Raycaster()
    this.intersects = []
    
    // 配置
    this.params = {
      enabled: true,
      maxDistance: 100,
    }
    
    // 绑定事件
    this._handleClick = this._handleClick.bind(this)
    emitter.on('input:mouse_down', this._handleClick)
  }
  
  _handleClick({ button }) {
    if (button !== 0 || !this.params.enabled) return
    
    // 使用 IMouse 的 normalizedMouse（MANDATORY）
    const ndc = this.iMouse.normalizedMouse
    this.raycaster.setFromCamera(ndc, this.camera)
    
    // 检测交叉
    this.intersects = this.raycaster.intersectObjects(
      this.scene.children,
      true  // recursive
    )
    
    if (this.intersects.length > 0) {
      const hit = this.intersects[0]
      emitter.emit('game:object-picked', {
        object: hit.object,
        point: hit.point,
        distance: hit.distance,
      })
    }
  }
  
  destroy() {
    emitter.off('input:mouse_down', this._handleClick)
  }
}
```

## 屏幕中心射线（第一人称准星）

```javascript
const CENTER_SCREEN = new THREE.Vector2(0, 0)

update() {
  // 第一人称：从屏幕中心发射
  this.raycaster.setFromCamera(CENTER_SCREEN, this.camera)
  
  // 或者第三人称：从鼠标位置发射
  // this.raycaster.setFromCamera(this.iMouse.normalizedMouse, this.camera)
  
  const intersects = this.raycaster.intersectObjects(this.targets, true)
  // ...
}
```

## 方块交互模式

本项目的 `BlockRaycaster` 实现了体素方块的射线检测：

```javascript
// src/js/interaction/block-raycaster.js
export default class BlockRaycaster {
  constructor() {
    this.experience = new Experience()
    this.camera = this.experience.camera.instance
    this.iMouse = this.experience.iMouse
    
    this.raycaster = new THREE.Raycaster()
    this.raycaster.far = 8  // 最大交互距离
    
    this.params = {
      useMouse: false,  // false = 屏幕中心, true = 鼠标位置
    }
    
    this.result = {
      hit: false,
      blockPos: null,
      faceNormal: null,
      adjacentPos: null,  // 放置方块的位置
    }
  }
  
  update(terrainMeshes) {
    // 选择射线原点
    const ndc = this.params.useMouse
      ? this.iMouse.normalizedMouse
      : new THREE.Vector2(0, 0)
    
    this.raycaster.setFromCamera(ndc, this.camera)
    
    const intersects = this.raycaster.intersectObjects(terrainMeshes, false)
    
    if (intersects.length > 0) {
      const hit = intersects[0]
      
      // 计算方块坐标（向下取整到格子中心）
      const blockX = Math.floor(hit.point.x - hit.face.normal.x * 0.5)
      const blockY = Math.floor(hit.point.y - hit.face.normal.y * 0.5)
      const blockZ = Math.floor(hit.point.z - hit.face.normal.z * 0.5)
      
      // 计算相邻方块位置（放置用）
      const adjacentX = blockX + Math.round(hit.face.normal.x)
      const adjacentY = blockY + Math.round(hit.face.normal.y)
      const adjacentZ = blockZ + Math.round(hit.face.normal.z)
      
      this.result = {
        hit: true,
        blockPos: new THREE.Vector3(blockX, blockY, blockZ),
        faceNormal: hit.face.normal.clone(),
        adjacentPos: new THREE.Vector3(adjacentX, adjacentY, adjacentZ),
        distance: hit.distance,
      }
    } else {
      this.result.hit = false
    }
    
    return this.result
  }
}
```

## 交互管理器

```javascript
// src/js/interaction/block-interaction-manager.js
export default class BlockInteractionManager {
  constructor(terrainRenderer) {
    this.terrainRenderer = terrainRenderer
    this.raycaster = new BlockRaycaster()
    
    this._handleMouseDown = this._handleMouseDown.bind(this)
    emitter.on('input:mouse_down', this._handleMouseDown)
  }
  
  _handleMouseDown({ button }) {
    const result = this.raycaster.result
    if (!result.hit) return
    
    if (button === 0) {
      // 左键：挖掘方块
      this.terrainRenderer.removeBlock(
        result.blockPos.x,
        result.blockPos.y,
        result.blockPos.z
      )
    } else if (button === 2) {
      // 右键：放置方块
      this.terrainRenderer.placeBlock(
        result.adjacentPos.x,
        result.adjacentPos.y,
        result.adjacentPos.z,
        this.currentBlockType
      )
    }
  }
  
  update() {
    // 每帧更新射线检测
    const meshes = this.terrainRenderer.getMeshes()
    this.raycaster.update(meshes)
  }
  
  destroy() {
    emitter.off('input:mouse_down', this._handleMouseDown)
  }
}
```

## 层过滤

使用 `layers` 过滤检测对象：

```javascript
// 设置层
const LAYER_TERRAIN = 1
const LAYER_PLAYER = 2
const LAYER_UI = 3

// 设置对象层
terrainMesh.layers.set(LAYER_TERRAIN)
playerMesh.layers.set(LAYER_PLAYER)

// 配置 Raycaster 只检测特定层
this.raycaster.layers.set(LAYER_TERRAIN)  // 只检测地形

// 或启用多个层
this.raycaster.layers.enable(LAYER_TERRAIN)
this.raycaster.layers.enable(LAYER_PLAYER)
```

## 性能优化

### 限制检测距离

```javascript
this.raycaster.near = 0.1
this.raycaster.far = 50  // 限制最大距离
```

### 分组检测

```javascript
// 只检测相关对象组，而非整个场景
const intersects = this.raycaster.intersectObjects(
  this.interactableGroup.children,
  false  // 不递归检测子对象
)
```

### 降低检测频率

```javascript
update() {
  this._frameCount++
  
  // 每 3 帧检测一次
  if (this._frameCount % 3 !== 0) return
  
  this.raycaster.setFromCamera(...)
  // ...
}
```

### 使用 BVH（边界体积层次）

对于复杂几何体，考虑使用 `three-mesh-bvh`：

```javascript
import { computeBoundsTree } from 'three-mesh-bvh'

// 为复杂几何体构建 BVH
mesh.geometry.computeBoundsTree()

// 射线检测会自动使用 BVH 加速
```

## 悬停检测

```javascript
export default class HoverDetector {
  constructor() {
    this.hoveredObject = null
  }
  
  update() {
    const ndc = this.iMouse.normalizedMouse
    this.raycaster.setFromCamera(ndc, this.camera)
    
    const intersects = this.raycaster.intersectObjects(this.targets)
    
    const newHovered = intersects.length > 0 ? intersects[0].object : null
    
    if (newHovered !== this.hoveredObject) {
      if (this.hoveredObject) {
        emitter.emit('game:hover-exit', { object: this.hoveredObject })
      }
      if (newHovered) {
        emitter.emit('game:hover-enter', { object: newHovered })
      }
      this.hoveredObject = newHovered
    }
  }
}
```

## Common Mistakes

### ❌ 手动计算 NDC

```javascript
// BAD
const x = (event.clientX / window.innerWidth) * 2 - 1
const y = -(event.clientY / window.innerHeight) * 2 + 1
this.raycaster.setFromCamera(new THREE.Vector2(x, y), this.camera)

// GOOD
this.raycaster.setFromCamera(this.iMouse.normalizedMouse, this.camera)
```

### ❌ 检测整个场景

```javascript
// BAD: 检测所有对象，性能差
const intersects = this.raycaster.intersectObjects(this.scene.children, true)

// GOOD: 只检测相关对象
const intersects = this.raycaster.intersectObjects(this.interactables, false)
```

### ❌ 忘记设置 far 距离

```javascript
// BAD: 默认 far = Infinity
this.raycaster = new THREE.Raycaster()

// GOOD: 限制检测距离
this.raycaster = new THREE.Raycaster()
this.raycaster.far = 50
```

### ❌ 在事件处理中忘记检查条件

```javascript
// BAD: 没有检查是否有效
_handleClick({ button }) {
  const hit = this.intersects[0]  // 可能为空！
  this.doSomething(hit.object)
}

// GOOD: 检查条件
_handleClick({ button }) {
  if (button !== 0) return
  if (!this.result.hit) return
  
  this.doSomething(this.result.blockPos)
}
```

## Quick Reference

| 需求 | 做法 |
|------|------|
| 从鼠标发射射线 | `raycaster.setFromCamera(iMouse.normalizedMouse, camera)` |
| 从屏幕中心发射 | `raycaster.setFromCamera(new Vector2(0, 0), camera)` |
| 限制距离 | `raycaster.far = 50` |
| 层过滤 | `raycaster.layers.set(LAYER_ID)` |
| 获取点击位置 | `intersects[0].point` |
| 获取面法线 | `intersects[0].face.normal` |

| 体素方块特有 | 说明 |
|--------------|------|
| 方块坐标 | `floor(hit.point - normal * 0.5)` |
| 相邻方块 | `blockPos + round(normal)` |
| 面法线 | 用于确定点击的是哪个面 |
