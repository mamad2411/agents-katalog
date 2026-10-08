---
name: vtj-resource-management
description: Loads and manages 3D assets via the Resources system. Use when adding models, textures, or fonts; declare in sources.js and access via core:ready event.
---

# vite-threejs Resource Management

## Overview

所有资源（模型、纹理、字体等）通过 **Resources** 类统一加载。资源在 `sources.js` 中声明，加载完成后通过 `this.experience.resources.items` 访问。

**核心原则**：在 sources.js 声明，通过 items 访问，在 `core:ready` 事件后使用。

## When to Use

- 添加新模型（GLB/GLTF/FBX/OBJ）
- 添加新纹理（PNG/JPG/HDR/EXR/KTX2）
- 添加字体、音频、视频等资源
- 需要等待资源加载完成后执行逻辑

## 资源声明 (sources.js)

所有资源在 `src/js/sources.js` 中统一声明：

```javascript
// src/js/sources.js
export default [
  {
    name: 'playerModel',        // 资源名称（用于访问）
    type: 'gltfModel',          // 资源类型
    path: 'models/character/player.glb',  // 相对于 public/ 的路径
  },
  {
    name: 'grass_block_top_texture',
    type: 'texture',
    path: 'textures/blocks/grass_block_top.png',
  },
  // ...
]
```

## 支持的资源类型

| type | 加载器 | 用途 | 示例路径 |
|------|--------|------|----------|
| `gltfModel` | GLTFLoader | GLB/GLTF 模型 | `models/xxx.glb` |
| `fbxModel` | FBXLoader | FBX 模型 | `models/xxx.fbx` |
| `objModel` | OBJLoader | OBJ 模型 | `models/xxx.obj` |
| `texture` | TextureLoader | 普通纹理 | `textures/xxx.png` |
| `hdrTexture` | RGBELoader | HDR 环境贴图 | `textures/xxx.hdr` |
| `exrTexture` | EXRLoader | EXR 高动态范围 | `textures/xxx.exr` |
| `ktx2Texture` | KTX2Loader | KTX2 压缩纹理 | `textures/xxx.ktx2` |
| `cubeTexture` | CubeTextureLoader | 立方体贴图 | `['px.jpg', 'nx.jpg', ...]` |
| `font` | FontLoader | 字体文件 | `fonts/xxx.json` |
| `audio` | AudioLoader | 音频文件 | `audio/xxx.mp3` |
| `svg` | SVGLoader | SVG 文件 | `images/xxx.svg` |
| `video` | VideoTexture | 视频纹理 | `videos/xxx.mp4` |

## 访问已加载资源

```javascript
// 在组件中访问资源
constructor() {
  this.experience = new Experience()
  this.resources = this.experience.resources
}

// 通过 items[name] 访问
const texture = this.resources.items['grass_block_top_texture']
const model = this.resources.items['playerModel']
```

### GLTF 模型结构

```javascript
const gltf = this.resources.items['playerModel']

// 完整 GLTF 对象
gltf.scene        // THREE.Group - 场景根节点
gltf.animations   // AnimationClip[] - 动画列表
gltf.cameras      // Camera[] - 相机（如有）
gltf.asset        // 元数据

// 添加到场景
this.scene.add(gltf.scene)

// 克隆模型（多实例）
const clone = gltf.scene.clone()
```

### 纹理配置

```javascript
const texture = this.resources.items['grass_block_top_texture']

// 常见纹理配置
texture.colorSpace = THREE.SRGBColorSpace  // 颜色空间
texture.wrapS = THREE.RepeatWrapping       // 水平重复
texture.wrapT = THREE.RepeatWrapping       // 垂直重复
texture.minFilter = THREE.NearestFilter    // 像素风格
texture.magFilter = THREE.NearestFilter
texture.generateMipmaps = false            // 像素风格关闭 mipmap
```

## 等待资源加载完成

资源全部加载完成后触发 `core:ready` 事件：

```javascript
import emitter from './utils/event-bus.js'

// 在需要等待资源的地方
emitter.on('core:ready', () => {
  // 此时所有资源已加载完成
  this.initWithResources()
})
```

### 典型模式：World 初始化

```javascript
// src/js/world/world.js
export default class World {
  constructor() {
    this.experience = new Experience()
    this.resources = this.experience.resources

    // 等待资源加载完成
    emitter.on('core:ready', () => {
      // 初始化需要资源的组件
      this.player = new Player()
      this.environment = new Environment()
      this.chunkManager = new ChunkManager()
    })
  }
}
```

## 添加新资源步骤

### 1. 放置文件

```
public/
├── models/
│   └── character/
│       └── my-model.glb      ← 新模型
├── textures/
│   └── blocks/
│       └── my-texture.png    ← 新纹理
```

### 2. 声明资源

```javascript
// src/js/sources.js
export default [
  // ... 现有资源
  
  // 添加新资源
  {
    name: 'myModel',
    type: 'gltfModel',
    path: 'models/character/my-model.glb',
  },
  {
    name: 'myTexture',
    type: 'texture',
    path: 'textures/blocks/my-texture.png',
  },
]
```

### 3. 使用资源

```javascript
// 在组件中（确保在 core:ready 后）
const model = this.resources.items['myModel']
const texture = this.resources.items['myTexture']
```

## 资源命名规范

| 类型 | 命名模式 | 示例 |
|------|----------|------|
| 模型 | `xxxModel` | `playerModel`, `steveModel` |
| 纹理 | `xxx_texture` 或描述性 | `grass_block_top_texture`, `dirt` |
| HDR | `xxxHDRTexture` | `environmentMapHDRTexture` |
| 天空盒 | `sky_xxxTexture` | `sky_sunriseTexture` |
| 植物 | `xxx_plant_Texture` | `dandelion_plant_Texture` |
| 破坏阶段 | `destroy_stage_N` | `destroy_stage_0` ~ `destroy_stage_9` |

## 加载进度

```javascript
// Resources 提供加载进度
this.resources.loadProgress  // 0.0 ~ 1.0
this.resources.isLoaded      // boolean
this.resources.loaded        // 已加载数量
this.resources.toLoad        // 总数量
```

## Common Mistakes

### ❌ 在 core:ready 之前访问资源

```javascript
// BAD: 构造函数中直接访问（资源可能未加载）
constructor() {
  this.model = this.resources.items['playerModel']  // ❌ 可能是 undefined
}

// GOOD: 在 core:ready 回调中访问
constructor() {
  emitter.on('core:ready', () => {
    this.model = this.resources.items['playerModel']  // ✅
  })
}
```

### ❌ 忘记在 sources.js 声明

```javascript
// BAD: 直接使用加载器（绕过资源系统）
const loader = new GLTFLoader()
loader.load('models/xxx.glb', (gltf) => { ... })

// GOOD: 在 sources.js 声明
// sources.js
{ name: 'xxx', type: 'gltfModel', path: 'models/xxx.glb' }

// 组件中
const gltf = this.resources.items['xxx']
```

### ❌ 资源名称拼写错误

```javascript
// BAD: 名称不匹配
// sources.js 中是 'playerModel'
const model = this.resources.items['player_model']  // ❌ undefined

// GOOD: 名称完全一致
const model = this.resources.items['playerModel']   // ✅
```

### ❌ 路径不以 public/ 为根

```javascript
// BAD: 使用绝对路径或 src/ 路径
{ path: '/public/models/xxx.glb' }     // ❌
{ path: 'src/assets/models/xxx.glb' }  // ❌

// GOOD: 相对于 public/ 目录
{ path: 'models/xxx.glb' }             // ✅
```

### ❌ 忘记配置像素风格纹理

```javascript
// BAD: 模糊的像素纹理（Minecraft 风格需要锐利边缘）
const texture = this.resources.items['grass']
// 使用默认 filter，导致模糊

// GOOD: 配置 NearestFilter
const texture = this.resources.items['grass']
texture.minFilter = THREE.NearestFilter
texture.magFilter = THREE.NearestFilter
texture.generateMipmaps = false
```

## Quick Reference

| 操作 | 代码 |
|------|------|
| 声明资源 | `sources.js`: `{ name, type, path }` |
| 访问资源 | `this.resources.items['name']` |
| 等待加载 | `emitter.on('core:ready', () => {})` |
| 检查进度 | `this.resources.loadProgress` |
| GLTF 场景 | `gltf.scene` |
| GLTF 动画 | `gltf.animations` |

| 资源类型 | type 值 |
|----------|---------|
| GLB/GLTF | `gltfModel` |
| 普通纹理 | `texture` |
| HDR | `hdrTexture` |
| 字体 | `font` |
| 音频 | `audio` |
