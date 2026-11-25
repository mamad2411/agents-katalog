---
name: wujie
description: >
  无界（wujie）微前端框架接入指南。涵盖主/子应用集成、Vue2/Vue3/React 组件封装、
  startApp/setupApp/preloadApp API、路由同步与跳转、保活预加载、bus 通信、插件与生命周期、
  子应用改造、部署排障与常见问题。当用户提到 wujie、无界、微前端、子应用接入、
  主应用加载子应用时使用。
---

# 无界（wujie）微前端

> 适配 wujie >= 2.1.0。详细 API 与排障见 `references/`。

## 框架速览

无界用 **同源 iframe** 跑子应用 JS（天然 window 沙箱），用 **WebComponent（shadow DOM）** 渲染子应用 DOM（天然 CSS 隔离）。子应用路由在 iframe 内独立运行，通过劫持 `history` 与主应用 URL 同步。

对比：
- **iframe 方案**：隔离完美但路由丢失、弹窗受限、通信困难
- **qiankun**：需改造路由，无法多应用同时激活、Vite ESM 支持差
- **无界**：组件式接入、多应用同时在线、子应用几乎零改造

## 包选择

| 主应用技术栈 | npm 包 | 组件名 |
|-------------|--------|--------|
| 无框架 / 任意 | `wujie` | 直接调 API |
| Vue 2 | `wujie-vue2` | `<WujieVue>` |
| Vue 3 | `wujie-vue3` | `<WujieVue>` |
| React | `wujie-react` | `<WujieReact>` |

子应用**无需**安装 wujie 包，通过 `window.$wujie` 访问注入对象。

## 接入决策

```
用户问题
  ├─ 选包 / 组件怎么用？        → references/main-app.md
  ├─ API 参数 / $wujie？        → references/api.md
  ├─ 子应用要不要改？怎么改？    → references/sub-app.md
  ├─ 路由 / 菜单 / 跳转 / 多Tab → references/routing.md
  ├─ 保活 / sync / 预加载 / 性能 → references/modes.md
  ├─ props / bus 通信？         → references/communication.md
  ├─ 插件 / 生命周期？          → references/plugin-lifecycle.md
  ├─ 部署 / 发版 / 404？        → references/deployment.md
  └─ 报错 / 组件异常？          → references/faq.md（先查索引）
```

## 最小接入（Vue3 主应用）

```bash
npm i wujie-vue3
```

```javascript
// main.js
import { createApp } from "vue";
import WujieVue from "wujie-vue3";

const app = createApp(App);
app.use(WujieVue);
app.mount("#app");
```

```vue
<!-- 页面组件 -->
<template>
  <WujieVue name="vue3" url="//localhost:7300/" width="100%" height="100%" :sync="true" />
</template>
```

子应用满足跨域（CORS）时通常**零改造**即可运行。Vite 子应用需将 `window.location` 改为 `$wujie.location`。

## 三种运行模式（速查）

| 模式 | 条件 | 改 url 能否跳路由 | 子应用改造 |
|------|------|------------------|-----------|
| **重建** | 默认 | 能（sync 时受限于 URL 同步参数） | 不需要 |
| **保活** | `alive: true` | **不能**，需 bus 通信 | 不需要 |
| **单例** | `alive: false` + 生命周期改造 | 能 | 需要 `__WUJIE_MOUNT` |

详见 [references/modes.md](references/modes.md)。

## 推荐接入流程

```
- [ ] 确认主应用框架 → 选 npm 包
- [ ] 子应用配置 CORS（跨域 + cookie 场景加自定义 fetch）
- [ ] 确定运行模式：重建 / 保活 / 单例
- [ ] 是否需要路由同步 sync、预加载 preloadApp
- [ ] 设计主应用路由结构（见 routing.md）
- [ ] 确定通信方式：props / bus / window.parent
- [ ] 按需读取 references，不猜测 API 参数
- [ ] 代码对照 examples 官方 demo 写法
```

## Reference 索引

| 文件 | 何时读 |
|------|--------|
| [api.md](references/api.md) | 查 setupApp/startApp/preloadApp 参数、bus、$wujie |
| [main-app.md](references/main-app.md) | Vue2/Vue3/React 组件 Props、setupApp 配合 |
| [sub-app.md](references/sub-app.md) | 子应用 CORS、生命周期改造、Vite 特殊处理 |
| [routing.md](references/routing.md) | **主应用菜单跳转、保活路由、多 Tab、deep link** |
| [modes.md](references/modes.md) | alive/sync/degrade/fiber、预加载策略、性能优化 |
| [communication.md](references/communication.md) | props/bus/window 三种通信方式 |
| [plugin-lifecycle.md](references/plugin-lifecycle.md) | 插件配置、生命周期钩子、attrs 空页 |
| [deployment.md](references/deployment.md) | nginx 缓存、发版 404、自定义 fetch |
| [faq.md](references/faq.md) | 报错排障索引（CORS、弹层错位、富文本等） |

## AI 工作约束

1. **保活模式下禁止建议改 `url` 来跳子应用路由**，必须用 bus 通信（见 routing.md）
2. **Vite 子应用**中 `window.location` 拿到的是主应用地址，必须用 `$wujie.location`
3. **`name` 必须全局唯一**；多 Tab 同 name 会冲突（见 routing.md 多标签页章节）
4. 给出方案前确认子应用是重建/保活/单例，三者路由行为不同
5. 排障先查 faq.md 索引，再深入对应 reference
