---
name: vtj-shader-development
description: Creates custom GLSL shaders with vite-plugin-glsl. Use when writing vertex/fragment shaders, managing uniforms, or adding ShaderMaterial debug panels.
---

# vite-threejs Shader Development

## Overview

本项目使用 **vite-plugin-glsl** 支持 GLSL 文件导入，着色器存放在 `src/shaders/` 目录。

**核心原则**：所有着色器必须存放在 shaders 目录，所有 uniform 必须有调试面板。

## When to Use

- 创建自定义着色器效果
- 修改现有着色器
- 添加后处理效果
- 需要理解着色器导入和 uniform 管理

## 目录结构

```
src/shaders/
├── includes/              # 共享工具函数
│   ├── ambientLight.glsl
│   ├── directionalLight.glsl
│   └── pointLight.glsl
├── sky/                   # 天空盒
│   ├── vertex.glsl
│   └── fragment.glsl
├── speedlines/            # 后处理：速度线
│   ├── vertex.glsl
│   └── fragment.glsl
├── blocks/                # 方块着色器
│   ├── ao.vert.glsl       # 环境光遮蔽
│   ├── ao.frag.glsl
│   ├── mining.vert.glsl   # 挖掘效果
│   ├── mining.frag.glsl
│   └── wind.vert.glsl     # 植物风动
├── glass/                 # 玻璃折射
├── halftone/              # 半调渲染
└── grid/                  # 调试网格
```

## 导入着色器

### vite.config.js 配置

```javascript
import glsl from 'vite-plugin-glsl'

export default {
  plugins: [
    glsl(),  // 启用 .glsl 文件导入
  ],
}
```

### 导入方式

```javascript
// 使用路径别名（推荐）
import skyFragment from '@/shaders/sky/fragment.glsl'
import skyVertex from '@/shaders/sky/vertex.glsl'

// 或相对路径
import speedLinesFragment from '../shaders/speedlines/fragment.glsl'
```

## ShaderMaterial 模式

### 基础 ShaderMaterial

```javascript
import fragmentShader from '@/shaders/effect/fragment.glsl'
import vertexShader from '@/shaders/effect/vertex.glsl'

export default class EffectMesh {
  constructor() {
    this.experience = new Experience()
    this.scene = this.experience.scene
    this.debug = this.experience.debug
    
    // Shader 配置参数
    this.config = {
      color: { r: 255, g: 255, b: 255 },
      intensity: 1.0,
      speed: 1.0,
    }
    
    this._createMaterial()
    this._createMesh()
    
    if (this.debug.active) {
      this.debugInit()
    }
  }
  
  _createMaterial() {
    this.material = new THREE.ShaderMaterial({
      uniforms: {
        uTime: { value: 0 },
        uColor: { value: new THREE.Color(1, 1, 1) },
        uIntensity: { value: 1.0 },
        uTexture: { value: null },
      },
      vertexShader,
      fragmentShader,
      transparent: true,
      side: THREE.DoubleSide,
    })
  }
  
  update() {
    const elapsed = this.experience.time.elapsed
    this.material.uniforms.uTime.value = elapsed * 0.001
  }
  
  // 必须实现调试面板！
  debugInit() {
    this.debugFolder = this.debug.ui.addFolder({
      title: 'Effect Shader',
      expanded: false,
    })
    
    // 颜色 uniform 使用 view: 'color'
    this.debugFolder.addBinding(this.config, 'color', {
      label: 'Color',
      view: 'color',
    }).on('change', (ev) => {
      this.material.uniforms.uColor.value.setRGB(
        ev.value.r / 255,
        ev.value.g / 255,
        ev.value.b / 255
      )
    })
    
    // 数值 uniform 使用 addBinding
    this.debugFolder.addBinding(this.config, 'intensity', {
      label: 'Intensity',
      min: 0, max: 2, step: 0.01,
    }).on('change', (ev) => {
      this.material.uniforms.uIntensity.value = ev.value
    })
  }
  
  destroy() {
    this.material.dispose()
    // ...
  }
}
```

### 后处理 ShaderPass

```javascript
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js'
import fragmentShader from '@/shaders/effect/fragment.glsl'
import vertexShader from '@/shaders/effect/vertex.glsl'

// 在 Renderer 中
this.effectPass = new ShaderPass({
  uniforms: {
    tDiffuse: { value: null },  // 必需：接收上一个 pass 的输出
    uTime: { value: 0 },
    uOpacity: { value: 1.0 },
  },
  vertexShader,
  fragmentShader,
})
this.composer.addPass(this.effectPass)
```

## GLSL 代码规范

### 标准结构

```glsl
// ===== Uniforms =====
uniform float uTime;
uniform vec3 uColor;
uniform sampler2D uTexture;

// ===== Varyings =====
varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vPosition;

// ===== Helper Functions =====
float random(float seed) {
  return fract(sin(seed) * 43758.5453);
}

// ===== Main =====
void main() {
  // ...
  
  gl_FragColor = vec4(color, 1.0);
  
  // Three.js 色彩空间校正
  #include <tonemapping_fragment>
  #include <colorspace_fragment>
}
```

### Include 模式

共享代码放在 `includes/` 目录：

```glsl
// includes/pointLight.glsl
vec3 pointLight(
  vec3 lightColor,
  float lightIntensity,
  vec3 normal,
  vec3 lightPosition,
  vec3 viewDirection,
  float specularPower,
  vec3 position,
  float lightDecay
) {
  vec3 lightDelta = lightPosition - position;
  float lightDistance = length(lightDelta);
  vec3 lightDir = normalize(lightDelta);
  
  float decay = 1.0 / (1.0 + lightDistance * lightDecay);
  float shading = max(0.0, dot(normal, lightDir));
  
  // Phong specular
  vec3 reflectDir = reflect(-lightDir, normal);
  float specular = pow(max(dot(viewDirection, reflectDir), 0.0), specularPower);
  
  return lightColor * lightIntensity * decay * (shading + specular);
}
```

使用 include：

```glsl
// halftone/fragment.glsl
#include ../includes/ambientLight.glsl
#include ../includes/directionalLight.glsl
#include ../includes/pointLight.glsl

void main() {
  vec3 light = ambientLight(vec3(1.0), 0.2);
  light += pointLight(uLightColor, 1.0, vNormal, uLightPos, viewDir, 32.0, vPosition, 0.1);
  // ...
}
```

## Custom Shader Material (CSM)

用于扩展标准材质（如添加 AO 到 MeshStandardMaterial）：

```glsl
// ao.vert.glsl - 顶点着色器
attribute float aAo;
varying float vAO;

void main() {
  vAO = 1.0 - aAo;
  
  // CSM 特殊变量：替代标准顶点变换
  csm_PositionRaw = projectionMatrix * modelViewMatrix * instanceMatrix * vec4(position, 1.0);
}
```

```glsl
// ao.frag.glsl - 片元着色器
varying float vAO;

void main() {
  float aoFactor = mix(0.5, 1.0, vAO);
  
  // CSM 特殊变量：修改漫反射颜色
  csm_DiffuseColor.rgb *= vec3(aoFactor);
}
```

## Uniform 类型对照

| GLSL 类型 | JS 设置方式 |
|-----------|-------------|
| `float` | `{ value: 1.0 }` |
| `vec2` | `{ value: new THREE.Vector2(1, 1) }` |
| `vec3` | `{ value: new THREE.Vector3(1, 1, 1) }` |
| `vec3` (颜色) | `{ value: new THREE.Color(1, 1, 1) }` |
| `mat4` | `{ value: new THREE.Matrix4() }` |
| `sampler2D` | `{ value: texture }` |

## 调试面板要求（MANDATORY）

**所有 ShaderMaterial 的 uniform 都必须有调试面板**：

```javascript
debugInit() {
  const folder = this.debug.ui.addFolder({ title: 'Shader' })
  
  // 颜色 → view: 'color'
  folder.addBinding(this.config, 'color', { view: 'color' })
  
  // 数值 → min/max/step
  folder.addBinding(this.config, 'value', { min: 0, max: 1 })
  
  // 向量 → 分轴控制或 point2d
  folder.addBinding(this.config, 'offset', {
    x: { min: -10, max: 10 },
    y: { min: -10, max: 10 },
  })
}
```

## Common Mistakes

### ❌ 着色器放错位置

```javascript
// BAD: 着色器在 js 目录
import shader from './world/effect.glsl'

// GOOD: 着色器在 shaders 目录
import shader from '@/shaders/effect/fragment.glsl'
```

### ❌ 缺少调试面板

```javascript
// BAD: 有 uniform 但没有 debugInit
this.material = new THREE.ShaderMaterial({
  uniforms: { uIntensity: { value: 1.0 } },
  // ...
})
// 没有 debugInit() → 无法调参

// GOOD: 必须有调试面板
debugInit() {
  this.debugFolder.addBinding(this.config, 'intensity', {...})
}
```

### ❌ 颜色 uniform 不使用 view: 'color'

```javascript
// BAD: 颜色使用默认控件
folder.addBinding(this.config, 'color')  // 显示为数字输入框

// GOOD: 使用颜色选择器
folder.addBinding(this.config, 'color', { view: 'color' })
```

### ❌ 忘记色彩空间校正

```glsl
// BAD: 直接输出（颜色可能偏暗）
gl_FragColor = vec4(color, 1.0);

// GOOD: 添加色彩空间校正
gl_FragColor = vec4(color, 1.0);
#include <tonemapping_fragment>
#include <colorspace_fragment>
```

## Quick Reference

| 需求 | 做法 |
|------|------|
| 创建着色器 | 在 `src/shaders/<name>/` 创建 vertex.glsl 和 fragment.glsl |
| 导入着色器 | `import shader from '@/shaders/<path>.glsl'` |
| 共享代码 | 放入 `includes/`，使用 `#include` |
| 更新 uniform | `material.uniforms.uValue.value = newValue` |
| 调试面板 | 必须在 `debugInit()` 中为每个 uniform 创建控件 |
| 颜色控件 | 使用 `view: 'color'` |
