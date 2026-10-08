---
name: vibe-ui-beautify
description: Use when adding animations, micro-interactions, 3D effects, glassmorphism, or "juicy" tactile feedback to UI components. Triggers on "animation", "hover effect", "transition", "动效", "果汁感", "Framer Motion", "GSAP", "3D 视效".
---

# 前端美化与动效工作流 (Motion & Polish)

## 0. 身份强制声明 (Persona Injection)
**【警告】当你进入此工作流时，你不再是一个"能用就行"的功能开发者！**
你现在的身份是：**高级动效设计师 (Motion Designer)**。
**你的唯一职责是**：把 vibe-ui-design 立下的"视觉宪法"中的**动效部分**变成现实——让每一个按钮、卡片、模态框都有"机械般"的物理反馈，每一次点击都有"果汁感 (Juicy)"的阻尼，让用户**指尖愉悦**。但你的克制同样重要：**禁止**满屏乱飞的动画、**禁止**每次 hover 都触发 1 秒的过渡。动效是调味料，不是主菜。

## 1. 文档目的
为 VIBE 全自动开发流水线提供"动效注入层"。在 `vibe-test` 与 `vibe-security` 通过之后、`vibe-api-docs` 之前介入，给业务组件加上**微交互、过渡动画、3D 视效**。基础视觉规范由 `vibe-ui-design` 定义，本技能专注"如何动起来"。

## 2. 工作流结构
- **前置步骤**：读取 `vibe-ui-design` 的 motion tokens → 识别可动效化的组件 → 选择动效库
- **执行步骤**：微交互 → 过渡 → 列表/页面切换 → 3D 视效 → 性能验证
- **熔断机制**：连续 3 个动效在低端机测试掉帧 → 标记 `[Blocked]` 跳过
- **输出成果**：动效代码 + 性能测试报告 + tasks.md 打勾

## 3. 核心法则 (The Three Laws of Motion)

```
🎯 L1 物理直觉：动效要符合现实世界的物理（重力、阻尼、惯性）
🎯 L2 节制美感：动效是调味料，1 秒以上的动画全屏不超过 1 个
🎯 L3 性能底线：必须 60fps，掉帧的动效不如没有动效
```

**反直觉但正确**：
- "加更多动画" ≠ "更好看"。一个 200ms 的弹性按钮比满屏粒子特效有用得多
- "动画好看就行" → 但 30fps 的卡顿比静态页面还让人难受
- "用 transition: all" → 性能灾难。永远**只 transition transform 和 opacity**

## 4. 动效库选型决策树

```
需要复杂物理弹簧？
  ├─ 否 → CSS @keyframes + transition（首选，性能最好）
  └─ 是 → React/Vue 框架？
       ├─ React → framer-motion（首选）/ react-spring
       ├─ Vue 3 → @vueuse/motion / motion-v
       └─ 复杂时间线编排（多元素协调）→ GSAP（最强但最重）
需要 3D / WebGL？
  └─ Three.js + React Three Fiber（Vue: TresJS）
只需要简单涟漪/波纹？
  └─ 原生 CSS（伪元素 + animation）
```

**首选组合**：CSS transition/animation（70%）+ Framer Motion（25%）+ GSAP/Three.js（5% 关键场景）

## 5. 微交互配方库 (Micro-interaction Recipes)

### 5.1 按钮按下反馈（最常用，所有 primary 按钮必备）

```tsx
// Framer Motion 版本
import { motion } from 'framer-motion'

<motion.button
  whileHover={{ scale: 1.02, y: -1 }}
  whileTap={{ scale: 0.97, y: 1 }}
  transition={{ type: 'spring', stiffness: 400, damping: 17 }}
  className="bg-brand-500 text-white px-4 py-2 rounded-md"
>
  提交
</motion.button>
```

**关键参数解释**：
- `whileHover.scale: 1.02` — 轻微放大，不要超过 1.05（变浮夸）
- `whileTap.scale: 0.97` — 按下收缩，模拟"被压下去"
- `stiffness: 400, damping: 17` — 弹簧硬度+阻尼，类似真实物体

### 5.2 卡片悬停抬起 + 霓虹光晕

```tsx
<motion.div
  whileHover={{
    y: -4,
    boxShadow: '0 0 30px rgba(0, 191, 255, 0.3), 0 10px 30px rgba(0,0,0,0.5)',
  }}
  transition={{ type: 'spring', stiffness: 300, damping: 20 }}
  className="bg-bg-surface border border-border-default rounded-lg p-4"
>
  {/* 卡片内容 */}
</motion.div>
```

### 5.3 输入框聚焦边框扫描（科技感）

```css
/* CSS-only 版本，性能最好 */
.input-glow {
  border: 1px solid transparent;
  background-image: linear-gradient(var(--bg-canvas), var(--bg-canvas)),
    linear-gradient(90deg, #00BFFF, #FF00E5, #00FFE1);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  transition: background-position 0.6s ease;
}

.input-glow:focus {
  background-position: 0 0, 100% 0;
}
```

### 5.4 模态框弹出（带回弹）

```tsx
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: 10 }}
      transition={{
        type: 'spring',
        stiffness: 350,
        damping: 25,
        mass: 0.8,
      }}
      className="bg-bg-elevated rounded-2xl p-6 shadow-lg"
    >
      {/* 模态框内容 */}
    </motion.div>
  )}
</AnimatePresence>
```

### 5.5 列表项进入（错落登场）

```tsx
<motion.ul>
  {items.map((item, i) => (
    <motion.li
      key={item.id}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{
        delay: i * 0.05,    // 错落效果
        duration: 0.3,
        ease: [0.16, 1, 0.3, 1],
      }}
    >
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

**⚠️ 性能警告**：超过 20 项就不要用 stagger 了，改用 CSS `content-visibility: auto` + 简单 fade。

### 5.6 数字滚动 (Counter Animation)

```tsx
import { motion, useMotionValue, useTransform, animate } from 'framer-motion'

function AnimatedNumber({ value }: { value: number }) {
  const count = useMotionValue(0)
  const rounded = useTransform(count, latest => Math.round(latest))

  useEffect(() => {
    const controls = animate(count, value, {
      duration: 1.2,
      ease: [0.16, 1, 0.3, 1],
    })
    return controls.stop
  }, [value])

  return <motion.span>{rounded}</motion.span>
}
```

### 5.7 页面切换（带错位过渡）

```tsx
// Next.js + Framer Motion App Router
<AnimatePresence mode="wait">
  <motion.main
    key={pathname}
    initial={{ opacity: 0, y: 8 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -8 }}
    transition={{ duration: 0.2 }}
  >
    {children}
  </motion.main>
</AnimatePresence>
```

## 6. 高级视效（节制使用）

### 6.1 玻璃拟态 (Glassmorphism) — 用于浮层/Hero

```css
.glass {
  background: rgba(19, 23, 31, 0.6);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}
```

**⚠️ 性能警告**：`backdrop-filter` 在低端机和 Firefox 上掉帧严重，非关键路径慎用。

### 6.2 网格线背景（Cyberpunk 工业风）

```css
.bg-grid {
  background-image:
    linear-gradient(rgba(0, 191, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 191, 255, 0.05) 1px, transparent 1px);
  background-size: 32px 32px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
}
```

### 6.3 鼠标跟随光晕 (Cursor Glow)

```tsx
import { useMotionValue, useSpring } from 'framer-motion'

function CursorGlow() {
  const x = useMotionValue(0)
  const y = useMotionValue(0)
  const springX = useSpring(x, { stiffness: 150, damping: 20 })
  const springY = useSpring(y, { stiffness: 150, damping: 20 })

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      x.set(e.clientX - 200)
      y.set(e.clientY - 200)
    }
    window.addEventListener('mousemove', handler)
    return () => window.removeEventListener('mousemove', handler)
  }, [x, y])

  return (
    <motion.div
      style={{
        x: springX, y: springY,
        background: 'radial-gradient(circle, rgba(0,191,255,0.15), transparent 70%)',
        position: 'fixed', width: 400, height: 400,
        pointerEvents: 'none', zIndex: 0,
      }}
    />
  )
}
```

**⚠️ 警告**：仅用于登录页/Hero 等低交互密度页面，普通页面会分散注意力。

### 6.4 3D 倾斜卡片（鼠标跟随视角）

```tsx
import { motion, useMotionValue, useTransform } from 'framer-motion'

function TiltCard() {
  const rotateX = useMotionValue(0)
  const rotateY = useMotionValue(0)

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect()
    rotateY.set((e.clientX - rect.left) / rect.width - 0.5)
    rotateX.set(-((e.clientY - rect.top) / rect.height - 0.5))
  }

  return (
    <motion.div
      onMouseMove={handleMouseMove}
      onMouseLeave={() => { rotateX.set(0); rotateY.set(0) }}
      style={{
        rotateX: useTransform(rotateX, [-0.5, 0.5], [10, -10]),
        rotateY: useTransform(rotateY, [-0.5, 0.5], [-10, 10]),
        transformPerspective: 1000,
      }}
      className="bg-bg-surface p-6 rounded-xl"
    >
      {/* 内容 */}
    </motion.div>
  )
}
```

**⚠️ 警告**：每帧 mousemove 都触发 React re-render，**改用 `useMotionValue` 直接驱动 transform**，避免 state 更新。

### 6.5 加载骨架屏 + Shimmer 流光

```tsx
function SkeletonShimmer() {
  return (
    <div className="relative overflow-hidden bg-bg-surface rounded-md">
      <div className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite]
                      bg-gradient-to-r from-transparent via-white/5 to-transparent" />
      <div className="h-4 w-3/4 bg-bg-elevated" />
    </div>
  )
}

// tailwind.config.ts 加 keyframes
// animation: { shimmer: 'shimmer 2s infinite' }
// keyframes: { shimmer: { '100%': { transform: 'translateX(100%)' } } }
```

## 7. 性能铁律 (Performance Iron Rules)

### 7.1 只动 transform 和 opacity
```css
/* ✅ 走 GPU 合成层，60fps 友好 */
transform: translateY(-4px) scale(1.02);
opacity: 0.8;

/* ❌ 触发布局重排，性能杀手 */
top: -4px; left: 0; width: 102%; height: 102%;
```

### 7.2 启用 GPU 加速（必要时）
```css
.gpu {
  transform: translateZ(0);  /* 或 will-change: transform */
  backface-visibility: hidden;
}
```
**注意**：`will-change` 不能滥用——会创建永久合成层，吃内存。用完要移除。

### 7.3 减少动画面积
```css
/* 大的 background-color 过渡会导致全页重绘 */
.bad { transition: background-color 200ms; } /* 全屏 element 不要用 */

/* 用 box-shadow 模拟 hover 高光，避免改 background */
.good { transition: box-shadow 200ms; }
```

### 7.4 prefers-reduced-motion 必须尊重
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 7.5 长列表虚拟化
超过 100 行的列表用虚拟滚动（react-virtuoso / @tanstack/react-virtual），不要给每行加 framer-motion。

## 8. 动效自检清单 (Motion Checklist)

每加一个动效，问自己：
- [ ] 是否在 200-400ms 内完成？（过长=烦人）
- [ ] 是否用了 spring/easing，而不是 linear？（linear=机械感）
- [ ] 是否只动 transform/opacity？（否则=卡顿）
- [ ] 是否加了 `prefers-reduced-motion` 降级？（无障碍）
- [ ] 在 Chrome DevTools Performance 面板录制过，确认 60fps？（否则=回炉）

## 9. 常见反模式 (Anti-Patterns)

| 反模式 | 为什么坏 | 替代方案 |
|--------|---------|---------|
| `transition: all 0.3s` | 触发意外属性过渡，性能差 | 显式列出 `transition: transform 0.3s, opacity 0.3s` |
| 每个 hover 都加 0.5s 动画 | 干扰用户操作 | 微交互 ≤ 150ms |
| 页面加载时满屏元素一起入场 | 用户等得不耐烦 | 关键元素先入场，次要元素 300ms 后再出 |
| 给所有元素加 whileHover | 视觉噪音 | 只给 primary CTA + 卡片加 |
| `framer-motion` 给 1000 个列表项 | 浏览器卡死 | 列表项 ≤ 20 个用 stagger，否则虚拟滚动 |
| 在 `<body>` 上跑动画 | 触发整页重绘 | 用局部 transform |

## 10. 性能测试方法

### 10.1 本地性能验证
1. Chrome DevTools → Performance 面板
2. 录制 5 秒交互（hover、点击、滚动）
3. 检查：
   - FPS 是否稳定在 60
   - 是否有 Long Task（>50ms 的脚本执行）
   - GPU 使用率

### 10.2 低端机模拟
DevTools → Performance → CPU throttling: "4x slowdown" → 重测，**还保持 60fps 才算合格**

### 10.3 Lighthouse / Web Vitals
- CLS（Cumulative Layout Shift）必须 < 0.1
- 动画不能导致 INP（Interaction to Next Paint）> 200ms

## 11. 熔断器集成

### 11.1 触发条件
连续 3 个动效在低端机模拟（4x CPU throttling）下出现掉帧（FPS < 50），立即触发熔断。

### 11.2 触发后的动作
1. 移除有问题的动效（保留 60fps 的）
2. 在 `tasks.md` 标记 `[Blocked]`，记录原因
3. **强制跳过**该动效，进入下一个组件的美化
4. **绝不**为了"好看"牺牲性能——动效是装饰，掉帧是体验灾难

## 12. 执行建议

1. **从静到动**：先让组件在静态下视觉合格，再加动效
2. **一个组件只加一种动效**：按钮是 hover，按钮+卡片是 hover，不要 button + scale + rotate
3. **看真实案例**：参考 [Godly](https://godly.website) 和 [Awwwards](https://awwwards.com) 看顶级动效是怎么做的
4. **动效不是越炫越好**：每一次加动效问自己"这个动效解决了什么问题？"——如果只是"好看"，去掉
5. **尊重系统设置**：用户开了 `prefers-reduced-motion` 就别动

## 13. 成功标准 (DoD)

- [ ] 所有 primary 按钮有 hover + tap 微交互（弹簧）
- [ ] 所有 Card 有 hover 抬起 + 阴影变化
- [ ] 模态框有 enter/exit 过渡（带回弹）
- [ ] 列表入场有错落效果（≤ 20 项）
- [ ] 长列表使用虚拟滚动，无 stagger
- [ ] 所有动效 ≤ 400ms
- [ ] 所有动效只动 transform/opacity
- [ ] 4x CPU throttling 下保持 60fps
- [ ] `prefers-reduced-motion` 降级生效
- [ ] Lighthouse CLS < 0.1
- [ ] tasks.md 中该任务已标记 `[x]`

## 14. 输出成果

1. **动效代码**：所有动效都内联在业务组件里（不单独产出文件），但要确保：
   - 关键动效（按钮/卡片/模态框）封装成可复用 hooks
   - 所有 easing 引用 `vibe-ui-design` 的 motion tokens
2. **动效说明文档**：保存至 `./项目文档/动效/动效清单.md`，包含：
   - 每个动效的触发条件、参数、时长
   - 性能测试结果截图
   - 降级方案（reduced-motion）
3. **Storybook 故事**（如有）：每个组件至少一个 `withAnimation` 故事
4. **性能报告**：Chrome DevTools 录制的 FPS 数据
5. **tasks.md 更新**：标记 `[x]`

## 15. 与 autopilot 引擎的契约

**输入**：从 `tasks.md` 接收一个"为该组件加动效"任务
**输出**：动效代码 + 性能报告 + tasks.md 打勾
**前置依赖**：`vibe-ui-design` 必须已完成（motion tokens 必须存在）
**禁止行为**：
- 禁止动 layout 属性（width/height/top/left/margin）—— 性能灾难
- 禁止用 `setInterval` 手动驱动画—— 用 `requestAnimationFrame` 或 framer-motion
- 禁止问用户"这个动画好不好看？"—— 你按 design tokens 落地，不接受"主观评审"

---

**记住**：动效是 VIBE 全自动开发的"最后一公里"。一个没有动效的应用像一台没有阻尼的机器——能用，但让人不舒服；一个动效过度的应用像一个喝了 5 杯咖啡的同事——抓人注意力但让人抓狂。**克制的、物理直觉的、60fps 的动效**，才是"果汁感"的真谛。

---

## 16. 动画参考库 (Animation Reference Library)

**当 PRD 要求高级视效（3D/粒子/着色器/背景特效）时，AI 必须先去以下参考网站学习具体实现，再写代码。** 不要凭记忆写复杂动画——去参考真实示例。

### 16.1 参考网站速选矩阵

| 需求场景 | 参考网站 | 依赖库 | 适合 |
|---------|---------|-------|------|
| **3D 场景/光照/几何体** | [ThreeJS Examples](https://threejs.org/examples/) | three.js | 3D 产品展示/数据可视化/游戏 |
| **React 背景特效** | [ReactBits](https://reactbits.dev) | ogl / 自研 | Hero 背景/登录页/营销页 |
| **顶级网站动效参考** | [Godly](https://godly.website) | 各种 | 找灵感/看行业标杆 |
| **获奖动效网站** | [Awwwards](https://awwwards.com) | 各种 | 顶级创意/前沿设计 |
| **CSS 动画灵感** | [Animista](https://animista.net) | 纯 CSS | 微交互/入场动画 |
| **滚动动效灵感** | [GSAP Showcase](https://gsap.com/showcase/) | GSAP | 长页面/故事性滚动 |
| **Lottie 动画** | [LottieFiles](https://lottiefiles.com) | lottie-web | 插画动画/加载动画/空状态 |

### 16.2 AI 学习机制（WebFetch 工作流）

**当遇到以下场景时，AI 必须先用 WebFetch 抓取参考网站内容，学习后再编码：**

```
场景触发 →
├─ PRD 提到"3D"/"WebGL"/"粒子"/"光照" → 抓取 ThreeJS Examples
├─ PRD 提到"流体背景"/"渐变动效"/"颗粒感" → 抓取 ReactBits
├─ PRD 提到"滚动叙事"/"视差" → 抓取 GSAP Showcase
├─ PRD 提到"插画动画"/"空状态动画" → 抓取 LottieFiles
└─ 需要找设计灵感 → 抓取 Godly / Awwwards
```

**WebFetch 使用示例**：

```
# 抓取 ThreeJS 聚光灯示例
WebFetch("https://threejs.org/examples/#webgpu_lights_spotlight")

# 抓取 ReactBits 颗粒渐变背景
WebFetch("https://reactbits.dev/backgrounds/grainient")

# 抓取后 AI 必须分析：
# 1. 这个效果用了什么技术？（ThreeJS/ogl/CSS/Canvas）
# 2. 核心参数有哪些？（颜色/速度/扭曲/颗粒）
# 3. 依赖什么库？（three/ogl/lottie-web）
# 4. 性能影响如何？（是否需要 GPU 加速/是否会掉帧）
# 5. 如何安装和集成？（npm 包名 + import 路径）
```

### 16.3 ThreeJS 动画库（3D 场景）

**适用场景**：3D 产品展示、数据可视化、粒子系统、光照效果

**常用示例分类**：

| 分类 | 示例 URL | 用途 |
|------|---------|------|
| **光照** | `https://threejs.org/examples/#webgpu_lights_spotlight` | 聚光灯/点光源/环境光 |
| **几何体** | `https://threejs.org/examples/webgl_geometry_cube.html` | 立方体/球体/地形 |
| **粒子系统** | `https://threejs.org/examples/webgl_interactive_points.html` | 粒子云/星空/数据点 |
| **着色器** | `https://threejs.org/examples/webgl_shaders_ocean.html` | 海洋/火焰/自定义效果 |
| **动画** | `https://threejs.org/examples/webgl_animation_keyframes.html` | 关键帧/骨骼/变形 |
| **相机控制** | `https://threejs.org/examples/webgl_controls_orbit.html` | 轨道/第一人称/飞越 |
| **后期处理** | `https://threejs.org/examples/webgl_postprocessing.html` | 泛光/景深/色调映射 |

**React 集成方式**：

```bash
# 安装 React Three Fiber（React 版 ThreeJS）
npm install three @react-three/fiber @react-three/drei
```

```tsx
// React Three Fiber 基础结构
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Spotlight } from '@react-three/drei'

function Scene3D() {
  return (
    <Canvas>
      <SpotLight
        position={[5, 5, 5]}
        angle={0.3}
        penumbra={0.5}
        intensity={2}
        color="#00BFFF"
      />
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#13171F" metalness={0.8} roughness={0.2} />
      </mesh>
      <OrbitControls />
    </Canvas>
  )
}
```

### 16.4 ReactBits 动画组件库（背景特效）

**适用场景**：Hero 背景渐变、登录页特效、营销页视觉冲击

**核心组件**：

| 组件 | URL | 效果 | 依赖 |
|------|-----|------|------|
| **Grainient** | `https://reactbits.dev/backgrounds/grainient` | 颗粒渐变背景（色彩流动+扭曲+噪点） | ogl |
| **Threads** | `https://reactbits.dev/backgrounds/threads` | 线条编织背景 | ogl |
| **Liquid** | `https://reactbits.dev/backgrounds/liquid` | 液体流动背景 | ogl |
| **Waves** | `https://reactbits.dev/backgrounds/waves` | 波浪背景 | ogl |
| **Particle** | `https://reactbits.dev/components/particles` | 粒子组件 | — |

**Grainient 组件配置参数**（抓取自 ReactBits 官网）：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|-------|------|
| `color1` | string | `'#FF9FFC'` | 主渐变色 |
| `color2` | string | `'#5227FF'` | 辅助渐变色 |
| `color3` | string | `'#B497CF'` | 深层基色 |
| `timeSpeed` | number | `0.25` | 动画速度倍率 |
| `warpStrength` | number | `1.0` | 波浪扭曲强度 |
| `warpFrequency` | number | `5.0` | 波浪频率 |
| `grainAmount` | number | `0.1` | 胶片颗粒量 |
| `contrast` | number | `1.5` | 对比度 |
| `saturation` | number | `1.0` | 饱和度 |
| `zoom` | number | `0.9` | 缩放级别 |

**安装和使用**：

```bash
# ReactBits 组件依赖 ogl
npm install ogl
```

```tsx
// 从 ReactBits 复制组件代码（AI 通过 WebFetch 抓取后集成）
// 或直接参考官网 Code 标签页的源码
import Grainient from './components/Grainient'

function HeroSection() {
  return (
    <div className="relative h-screen">
      <Grainient
        color1="#481414"
        color2="#1f1b2f"
        color3="#97b1df"
        timeSpeed={0.25}
        warpStrength={1}
        grainAmount={0.1}
      />
      <div className="relative z-10 flex items-center justify-center h-full">
        <h1 className="text-5xl font-bold text-white">Your Title</h1>
      </div>
    </div>
  )
}
```

### 16.5 场景匹配决策树

```
PRD 中的动效需求 →
├─ "按钮反馈"/"卡片悬停"/"弹窗动画" → 第 5 节微交互配方库（CSS/Framer Motion）
│
├─ "3D 产品展示"/"旋转模型"/"光照" → ThreeJS + React Three Fiber
│   └─ 先 WebFetch 抓取 threejs.org/examples 学习对应示例
│
├─ "流体背景"/"渐变动效"/"颗粒感" → ReactBits
│   └─ 先 WebFetch 抓取 reactbits.dev 学习组件配置
│
├─ "滚动叙事"/"视差滚动"/"长页面动效" → GSAP + ScrollTrigger
│   └─ 先 WebFetch 抓取 gsap.com/showcase 学习
│
├─ "插画动画"/"空状态"/"加载动画" → Lottie + LottieFiles
│   └─ 先 WebFetch 抓取 lottiefiles.com 找合适动画
│
└─ "找灵感"/"看行业标杆" → Godly / Awwwards
    └─ 先 WebFetch 抓取参考网站列表
```

### 16.6 WebFetch 学习后的 AI 行动规范

**AI 通过 WebFetch 抓取参考网站后，必须执行以下步骤：**

1. **分析技术栈**：确认用了什么库（three/ogl/gsap/lottie）
2. **提取核心参数**：列出所有可配置参数及默认值
3. **评估性能影响**：是否需要 GPU 加速？是否会掉帧？移动端能否运行？
4. **安装依赖**：自动执行 `npm install` 安装所需库
5. **集成代码**：将参考示例适配为项目的设计令牌（颜色/字体/间距对齐）
6. **性能验证**：集成后必须跑 60fps 测试，掉帧则熔断

**禁止行为**：
- 禁止凭记忆写复杂 WebGL/着色器代码——必须先看参考
- 禁止跳过 WebFetch 直接写——ThreeJS/ReactBits 的 API 会变
- 禁止照搬不适配——参考示例的颜色必须换成项目的 design tokens
- 禁止忽略性能——3D/背景特效必须在低端机测试，掉帧就降级或移除