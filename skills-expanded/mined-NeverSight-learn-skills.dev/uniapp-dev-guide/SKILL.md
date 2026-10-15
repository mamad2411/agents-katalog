---
name: uniapp-dev-guide
description: uni-app 跨平台框架的完整开发规范，包含样式、组件、API、状态管理、TypeScript、网络请求、性能优化、renderjs、WXS、自定义导航栏、登录支付分享、调试部署等商业级开发所需的全栈知识。当用户开发 uni-app 项目、询问组件使用、跨平台适配、网络请求、状态管理、性能优化、或遇到任何 uni-app 相关问题时，务必使用此技能。
---

# uni-app 商业级开发指南

## 技能概述

本技能提供 uni-app 框架的完整开发知识体系，涵盖从基础规范到企业级架构的所有内容，帮助开发者快速构建高质量的跨平台应用。

**适用场景：** 小程序（微信/支付宝/百度/抖音等）、H5、App（iOS/Android）、鸿蒙应用

**核心价值：** 一套代码 -> 多端运行 -> 原生性能 -> 商业级质量

---

## 快速导航：按场景查阅

| 场景 | 推荐查阅 |
|------|----------|
| 样式适配问题 | [CSS 规范](#css-核心规范) + [踩坑点](#踩坑点速查) |
| 组件使用 | `references/components.md` |
| 网络请求/存储 | `references/api-network.md` |
| 设备能力（位置/相机/蓝牙等） | `references/api-device.md` |
| 状态管理（Pinia/Vuex） | `references/state-management.md` |
| TypeScript 项目 | `references/typescript.md` |
| UI 组件库 | `references/uni-ui.md` |
| 性能优化 | [性能优化](#性能优化核心策略) |
| 平台差异 | `references/platform-differences.md` + [平台差异速查](#平台差异速查) |
| 项目创建/配置/分包 | `references/project-setup.md` |
| renderjs / WXS | `references/renderjs-wxs.md` |
| 自定义导航栏 | `references/custom-navigation.md` |
| 登录/支付/分享 | `references/login-payment-share.md` |
| nvue 原生渲染 | `references/nvue-guide.md` |
| 调试/部署/CI/CD | `references/debugging-deployment.md` |
| 架构模式/踩坑大全 | `references/patterns-pitfalls.md` |
| 组件通信/事件系统 | `references/component-communication.md` |
| uni-app x 新项目 | `references/uni-app-x.md` |

---

## 项目创建速查

```bash
# Vue3 + Vite + JavaScript
npx degit dcloudio/uni-preset-vue#vite my-project

# Vue3 + Vite + TypeScript（推荐）
npx degit dcloudio/uni-preset-vue#vite-ts my-project

# 开发命令
npm run dev:h5          # H5
npm run dev:mp-weixin   # 微信小程序
npm run dev:mp-alipay   # 支付宝小程序
npm run dev:app         # App

# 构建命令
npm run build:h5
npm run build:mp-weixin
```

**完整项目配置：** `references/project-setup.md`

---

## CSS 核心规范

### 单位与适配

| 单位 | 说明 | 使用场景 |
|------|------|----------|
| **rpx** | 750rpx = 屏幕宽度 | 响应式布局首选，自动适配所有屏幕 |
| **px** | 物理像素 | 固定尺寸元素（图标、边框） |
| **vh/vw** | 视口比例 | 仅 Vue 页面支持，H5 常用 |
| **百分比** | 父容器比例 | **nvue 不支持** |

**rpx 关键规则：**
- 设计稿以 750px 宽度为基准
- 屏幕宽度超过 960px 时，rpx 按 375px 基准计算（防止过度拉伸）
- rpx 用于高度和字体时会缩放，固定尺寸用 px
- 可通过 `pages.json` 配置 `rpxCalcMaxDeviceWidth` 调整阈值

### 内置 CSS 变量

| 变量 | 说明 | 用途 |
|------|------|------|
| `--status-bar-height` | 状态栏高度（微信 25px，App 为实际值） | 自定义导航栏留白 |
| `--window-top` | 内容区距顶部偏移（H5 为 NavigationBar 高度） | H5 定位 |
| `--window-bottom` | 内容区距底部偏移（H5 为 TabBar 高度） | H5 底部固定元素 |

**自定义导航栏必须添加占位：**
```html
<view style="height: var(--status-bar-height);"></view>
```

### 选择器限制

- **不支持 `*` 通配符选择器**
- 微信小程序自定义组件仅支持 class 选择器
- `::before`/`::after` 仅在 Vue 页面生效
- `html`、`body`、`:root` 仅能在 App.vue 中使用
- **scoped 会导致页面级背景样式失效**——页面背景色避免 scoped

### 背景图与字体

- **小程序不支持 CSS 引用本地文件**（背景图/字体）
- 小于 40kb 自动转 base64；大于需网络 URL 或手动 base64
- 本地资源使用 `~@/static/path` 绝对路径
- 微信小程序网络资源需 https

### Flex 布局

- **框架推荐 Flex 布局**，跨平台兼容性最佳
- view 组件默认 flex 布局
- nvue 仅支持 flex，不支持 float 和部分 position:fixed

---

## 组件核心规范

### view 组件

- 容器组件，类似 `<div>`
- 默认 flex 布局
- `hover-class`：按下样式类
- **nvue 中文本必须包裹在 `<text>` 中**

### text 组件（关键踩坑）

**text 不继承父级 color**

```html
<!-- 错误：text 不会继承 view 的 color -->
<view style="color: #FFF">
  <text>白色文本</text>
</view>

<!-- 正确：直接在 text 上设置 color -->
<text :style="{ color: '#FFF' }">白色文本</text>
```

**原因：** App.vue 全局 `page { color: #333 }` 会直接作用于所有 text，父级 view 的 color 无法继承。**必须使用内联 `:style` 动态绑定**。

### image 组件

- **必须设置明确宽高**——默认 320x240px 通常不合适
- **mode 选项：** scaleToFill（拉伸）、aspectFit（完整显示）、aspectFill（裁剪）、widthFix（宽度固定）
- `lazy-load` 仅部分小程序支持（H5/App 不支持）
- SVG 在小程序中仅支持网络地址
- 自定义组件中相对路径可能失败，优先用绝对路径

### scroll-view 组件

- **纵向滚动必须设置固定高度**（CSS `height: 300rpx`）
- **不适合长列表**——性能差，应使用页面级滚动
- 不触发页面级回调（onPullDownRefresh、onReachBottom）
- iOS 支持 `enable-back-to-top`

### swiper 组件

- **必须设置固定高度**
- **仅允许 `<swiper-item>` 作为子组件**
- swiper-item 内 fixed 定位无效
- 适合 banner 轮播，不适合复杂长列表

**完整组件文档：** `references/components.md`

---

## 页面与路由

### 页面生命周期

| 钩子 | 触发时机 | 用途 |
|------|----------|------|
| `onLoad(options)` | 页面加载 | 接收参数、数据初始化 |
| `onShow` | 每次显示（包括返回） | 刷新数据 |
| `onReady` | 首次渲染完成 | DOM 操作、ref 查询 |
| `onHide` | 页面隐藏 | 暂停计时器 |
| `onUnload` | 页面销毁 | 清理资源、移除事件监听 |
| `onPullDownRefresh` | 下拉刷新 | |
| `onReachBottom` | 触底加载 | |
| `onPageScroll` | 页面滚动（**避免复杂操作**） | |

### 导航 API

| 方法 | 行为 | 场景 |
|------|------|------|
| `uni.navigateTo` | 保留当前页，跳转新页 | 普通跳转 |
| `uni.redirectTo` | 关闭当前页，跳转新页 | 替换当前页 |
| `uni.reLaunch` | 关闭所有页面，打开目标页 | 重新进入应用 |
| `uni.switchTab` | 跳转 tabBar 页面 | tab 切换 |
| `uni.navigateBack` | 返回上 N 页 | 返回操作 |

**关键限制：**
- **tabBar 页面必须用 `switchTab`**
- **`switchTab` 不支持传参**——使用全局变量、storage 或事件通道
- 页面栈有深度限制（小程序 10 层）
- URL 参数特殊字符需 `encodeURIComponent()`

---

## 配置文件

### pages.json

```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页"
      }
    }
  ],
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "uni-app",
    "navigationBarBackgroundColor": "#F8F8F8",
    "backgroundColor": "#F8F8F8"
  },
  "tabBar": {
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "static/home.png",
        "selectedIconPath": "static/home-active.png"
      }
    ]
  },
  "easycom": {
    "autoscan": true,
    "custom": {}
  }
}
```

**tabBar 要点：**
- 最少 2 个、最多 5 个 tab
- 图标小于 40KB，推荐 81x81px
- 原生 tabBar 无法被前端遮罩覆盖

**分包配置：**
```json
{
  "subPackages": [
    {
      "root": "pagesA",
      "pages": [
        { "path": "detail/index", "style": { "navigationBarTitleText": "详情" } }
      ]
    }
  ],
  "preloadRule": {
    "pages/index/index": {
      "network": "all",
      "packages": ["pagesA"]
    }
  }
}
```

**完整配置参考：** `references/project-setup.md`

### manifest.json

**关键配置：**
- `name`：应用名称
- `appid`：DCloud appid（**区别于微信 appid、iOS bundle id**）
- `versionName`/`versionCode`：版本号
- 平台配置在对应节点：`mp-weixin`、`app-plus`、`h5`

---

## 条件编译

### 语法

```javascript
// #ifdef PLATFORM
  仅在指定平台编译的代码
// #endif

// #ifndef PLATFORM
  在指定平台以外编译
// #endif
```

### 平台标识符

| 标识符 | 平台 |
|--------|------|
| `APP-PLUS` | 原生 App |
| `APP-ANDROID`/`APP-IOS` | Android/iOS 专属 |
| `APP-NVUE` | nvue 页面 |
| `H5`/`WEB` | 浏览器 |
| `MP-WEIXIN` | 微信小程序 |
| `MP-ALIPAY` | 支付宝小程序 |
| `MP-BAIDU` | 百度小程序 |
| `MP-TOUTIAO` | 抖音小程序 |
| `VUE2`/`VUE3` | Vue 版本区分 |

**适用范围：** JS/TS（`//`）、模板（`<!-- -->`）、样式（`/* */`）、pages.json

**目录级条件编译：** `static/mp-weixin/`、`platforms/app/`

---

## renderjs 与 WXS 速查

### renderjs（App + H5）

在视图层运行 JS，支持 DOM 操作和第三方库：

```vue
<script module="moduleName" lang="renderjs">
export default {
  methods: {
    updateData(newValue, oldValue, ownerInstance) {
      // 直接操作 DOM 或使用 ECharts 等
      const el = document.getElementById('chart')
      // ownerInstance.callMethod('logicMethod', data) 调用逻辑层
    }
  }
}
</script>

<!-- 模板中绑定 -->
<view :prop="data" :change:prop="moduleName.updateData"></view>
```

**平台：** App-Vue + H5（小程序不支持）

### WXS（全平台通用）

在视图层运行的轻量脚本，用于数据格式化和高性能触摸动画：

```vue
<script module="filters" lang="wxs">
function formatPrice(price) {
  return Number(price).toFixed(2)
}
module.exports = { formatPrice: formatPrice }
</script>

<!-- 模板中使用 -->
<text>{{ filters.formatPrice(item.price) }}</text>
```

**注意：WXS 只支持 ES5 语法（var, function），不支持 ES6+**

**完整指南：** `references/renderjs-wxs.md`

---

## 性能优化核心策略

### 启动优化

- 减少代码包体积、背景图、本地字体
- App 首页使用 nvue + fast 启动模式（约 2 秒）
- 启用分包加载（subPackages）
- 移除不需要的 App 模块（地图、蓝牙等）

### 渲染优化

- **分批加载数据**：首次 50 条，之后每 500ms 追加
- 减少组件数量和嵌套深度
- 页面切换延迟 100-300ms 再渲染图片
- 使用轻量动画（slide-in-right）

### 数据绑定优化

- 频繁更新区域封装为独立组件
- 列表项做成组件实现数据隔离
- `data` 中只放视图需要的变量

### 长列表优化

- **避免 scroll-view 实现长列表**——使用页面级滚动
- nvue 使用 `<list>` 组件（自动回收资源）
- Vue 页面使用虚拟列表插件

### 通信优化

- 减少 scroll 事件监听频率
- 避免 scroll 中实时操作 scroll-top/scroll-left
- **少用 `onPageScroll`**——频繁跨层通信
- CSS 动画替代 JS 定时器
- App-vue 使用 renderjs 做 canvas 操作
- 使用 wxs（App/H5/小程序）处理手势交互

### 图片优化

- 避免大尺寸图片（导致切换卡顿、内存峰值）
- 单屏不要显示多张缩放后的多 MB 图片——**会导致白屏崩溃**
- 避免大型 base64

---

## 踩坑点速查

### 样式相关

1. **text 不继承父级 color** -> 必须在 `<text>` 上直接设置
2. **scoped 导致页面背景失效** -> 页面级 `page` 样式不用 scoped
3. **`*` 选择器不支持** -> 使用 class 选择器
4. **rpx 在大屏异常** -> 超过 960px 按 375px 基准换算
5. **nvue 不支持百分比** -> 只能用 px 和 flex
6. **小程序 CSS 不能引用本地文件** -> 背景图/字体用网络 URL 或 base64
7. **overflow: hidden 不裁剪 image 圆角** -> 在 image 上直接设置 border-radius
8. **CSS gap 在部分小程序不生效** -> 使用 margin 代替 gap
9. **cover-view 只支持基本样式** -> 原生组件层级问题用 cover-view 覆盖
10. **safe-area padding 只能加一次** -> 多层嵌套会叠加偏移

### 组件相关

11. **image 必须设明确宽高** -> 默认 320x240px 不适用
12. **scroll-view 纵向滚动必须设固定高度** -> 否则无法滚动
13. **scroll-view 不触发页面级事件** -> onReachBottom 等无效
14. **scroll-view 长列表性能差** -> 用页面级滚动或虚拟列表
15. **swiper 只能放 swiper-item** -> 其他组件导致未定义行为
16. **swiper 需设固定高度** -> 默认高度不符合设计要求
17. **swiper-item 内 fixed 定位无效**
18. **scroll-view scroll-x 嵌套在 scroll-y 内不响应** -> 改用 swiper

### 导航相关

19. **switchTab 不支持传参** -> 用全局变量、storage 或事件通道
20. **tabBar 页面只能用 switchTab 跳转** -> navigateTo/redirectTo 无效
21. **原生 tabBar 无法被前端遮罩覆盖** -> 需要模态时先隐藏 tabBar
22. **页面栈有深度限制** -> 小程序 10 层，避免无限 navigateTo
23. **URL 参数特殊字符** -> 必须 encodeURIComponent

### 平台差异

24. **H5 的 --window-top/--window-bottom** -> 仅 H5 有值，其他平台为 0
25. **微信小程序自定义组件只支持 class 选择器**
26. **onShareTimeline 仅微信支持**
27. **lazy-load 仅部分小程序支持** -> H5/App 不支持 image lazy-load
28. **自定义 tabBar 各平台实现完全不同** -> H5 用 Vue 组件，微信用 wxml
29. **非 H5 平台无 window/document** -> DOM API 不可用
30. **SVG 不能用于小程序 image** -> 必须转 PNG
31. **原生组件（video/map/canvas/textarea）层级最高** -> 用 cover-view 或条件隐藏
32. **v-if vs v-show** -> 频繁切换用 v-show（小程序避免重复创建销毁）

### 通信相关

33. **uni.$on 必须在 onUnload 中 $off** -> 否则内存泄漏
34. **eventChannel 页面间通信** -> navigateTo 的 events 参数
35. **getCurrentPages 直接调用上一页方法** -> 耦合性高，优先事件通道
36. **组件 ref 在小程序中 onReady 后才能访问**

### 性能相关

37. **onPageScroll 频繁跨层通信** -> 能不用就不用
38. **大图片导致白屏崩溃** -> 单屏不渲染多张未压缩大图
39. **data 中放太多非视图数据** -> 增加 setData 传输量，拖慢渲染
40. **scroll-view 内实时操作滚动位置** -> 造成卡顿，减少频率
41. **修改数组某项需要 splice 或展开运算** -> 触发响应式更新
42. **WXS 只支持 ES5 语法** -> 不支持 let/const/箭头函数/Promise
43. **renderjs 不支持小程序** -> 使用 WXS 替代或条件编译

**完整踩坑与解决方案：** `references/patterns-pitfalls.md`

---

## 平台差异速查

| 特性 | H5 | 小程序 | App |
|------|-----|--------|-----|
| DOM 操作 | 支持 | 不支持 | 不支持 |
| window/document | 支持 | 不支持 | 不支持 |
| CSS 本地背景图 | 支持 | 不支持 | 支持 |
| `*` 选择器 | 部分 | 不支持 | 部分 |
| --window-bottom | TabBar 高度 | 0 | 0 |
| 路由模式 | hash/history | 小程序原生 | 原生 |
| Cookie/Session | 支持 | 不支持 | 部分 |
| 第三方 JS 库 | 大部分可用 | DOM 依赖不可用 | 大部分可用 |
| image lazy-load | 不支持 | 部分平台 | 不支持 |
| 自定义 tabBar | Vue 组件 | 平台原生文件 | 原生/Vue |
| 代码包大小限制 | 无 | 主包 2MB/总 20MB | 无 |
| 并发请求限制 | 无 | 10 个 | 无 |

**完整平台差异：** `references/platform-differences.md`

---

## 进阶主题

| 主题 | 文档 |
|------|------|
| 项目创建/工程化/分包 | `references/project-setup.md` |
| renderjs / WXS 高性能方案 | `references/renderjs-wxs.md` |
| 自定义导航栏（状态栏/安全区域/透明导航） | `references/custom-navigation.md` |
| 登录/支付/分享/开放能力 | `references/login-payment-share.md` |
| nvue 原生渲染开发 | `references/nvue-guide.md` |
| 网络请求封装、拦截器、错误处理 | `references/api-network.md` |
| 设备能力（位置/相机/蓝牙/传感器） | `references/api-device.md` |
| 状态管理（Pinia/Vuex + 持久化） | `references/state-management.md` |
| TypeScript 配置与类型定义 | `references/typescript.md` |
| uni-ui 组件库使用 | `references/uni-ui.md` |
| 动画、主题切换、国际化 | `references/advanced-features.md` |
| 调试/部署/CI/CD/热更新 | `references/debugging-deployment.md` |
| 架构模式/踩坑大全/表单验证/列表分页 | `references/patterns-pitfalls.md` |
| 组件通信与事件系统 | `references/component-communication.md` |
| uniCloud 云开发（云函数/云对象/云数据库/云存储/uni-id） | `references/unicloud-guide.md` |
| 隐私合规（PIPL/小程序隐私协议/App合规/安全加固） | `references/privacy-security.md` |
| 测试（单元测试/组件测试/E2E自动化/Mock策略） | `references/testing-guide.md` |
| 错误码与排查 | `references/error-codes.md` |
| uni-app x / 鸿蒙开发 | `references/uni-app-x.md` |

---

## 代码模板

**网络请求封装（JS）：** `scripts/request-wrapper.js`

**网络请求封装（TS）：** `scripts/request-wrapper-ts.ts`

**Pinia Store 模板：** `scripts/store-template.js`

**组件模板（Options API）：** `scripts/component-template.vue`

**组件模板（Composition API + TS）：** `scripts/component-template-setup.vue`

---

## 参考资源

- [uni-app 官方文档](https://uniapp.dcloud.net.cn/)
- [uni-app 性能优化专题](https://uniapp.dcloud.net.cn/tutorial/performance.html)
- [uni-app x 文档](https://doc.dcloud.net.cn/uni-app-x/)
- [DCloud 社区](https://ask.dcloud.net.cn/)
- [uni-ui 组件库](https://uniapp.dcloud.net.cn/component/uniui/uni-ui.html)
- [uni-app renderjs 文档](https://uniapp.dcloud.net.cn/tutorial/renderjs.html)
- [微信小程序 WXS 文档](https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxs/)
- [DCloud 插件市场](https://ext.dcloud.net.cn/)
