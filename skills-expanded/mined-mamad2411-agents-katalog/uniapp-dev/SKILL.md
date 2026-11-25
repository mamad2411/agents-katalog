---
name: uniapp-dev
description: UniApp跨端开发技能 - Vue3+UniApp语法、条件编译、多端差异、小程序生命周期、路由导航、分包加载、平台API、微信开放能力、审核规范。当你涉及UniApp/uni-app/小程序/微信小程序/H5跨端开发时必须使用此技能。即使用户只是说"写个小程序页面"或"uni-app加个功能"，也应触发。
---

# UniApp跨端开发技能 (UniApp Cross-Platform Skill)

## 快速规则（日常开发时自动加载，只需读到这里）

> **[UniApp核心清单]** ① 条件编译是第一工具：`#ifdef MP-WEIXIN`处理平台差异，禁止运行时判断平台做大量分支 ② 用rpx做响应式单位(750rpx=屏幕宽)，禁止px硬编码 ③ 小程序主包≤2MB，分包≤2MB(单个)/总≤20MB
> **[三禁]** ❌直接操作DOM（小程序无DOM） ❌使用浏览器特有API(window/document/cookie) ❌v-html在小程序中使用(用rich-text组件)
> **[生命周期铁律]** 页面用onLoad/onShow/onReady，组件用setup/onMounted，混用=bug

写/改UniApp代码时，强制遵守：
1. **条件编译优先**：平台差异用`#ifdef`/`#ifndef`，不用`uni.getSystemInfoSync().platform`做运行时分支
2. **rpx单位**：所有尺寸用rpx（750rpx=屏幕宽），字号可用rpx或px，图标用rpx
3. **生命周期分离**：页面级用UniApp生命周期（onLoad/onShow），组件级用Vue生命周期（onMounted）
4. **路由用uni API**：`uni.navigateTo`/`uni.redirectTo`/`uni.switchTab`，禁止vue-router
5. **存储用uni API**：`uni.setStorageSync`/`uni.getStorageSync`，禁止localStorage
6. **网络用uni API**：`uni.request`或封装后的请求库，禁止直接axios（小程序不支持XMLHttpRequest）
7. **图片压缩**：所有图片资源压缩，单张<200KB，总资源控制在主包2MB内

---

## 条件编译

### 基本语法
```javascript
// #ifdef MP-WEIXIN
// 仅微信小程序编译
wx.login({ success: (res) => {} })
// #endif

// #ifdef H5
// 仅H5编译
window.addEventListener('popstate', handler)
// #endif

// #ifndef MP-WEIXIN
// 除微信小程序外的所有平台
import VConsole from 'vconsole'
// #endif

// #ifdef MP-WEIXIN || MP-ALIPAY
// 微信或支付宝小程序
// #endif
```

### 条件编译支持范围
| 位置 | 语法 | 示例 |
|------|------|------|
| JS/TS | `// #ifdef` | 逻辑分支 |
| 模板 | `<!-- #ifdef -->` | 平台专属UI |
| CSS | `/* #ifdef */` | 平台专属样式 |
| pages.json | 不支持 | 用多个配置文件 |
| 静态资源 | 目录名 | `static/mp-weixin/` |

### 平台标识符
| 标识 | 平台 | 标识 | 平台 |
|------|------|------|------|
| `H5` | Web | `APP-PLUS` | App(iOS/Android) |
| `MP-WEIXIN` | 微信小程序 | `MP-ALIPAY` | 支付宝小程序 |
| `MP-BAIDU` | 百度小程序 | `MP-TOUTIAO` | 抖音小程序 |
| `MP` | 所有小程序 | `APP-ANDROID` | 仅Android App |

## 生命周期

### 页面生命周期（pages中注册的页面）
```javascript
import { onLoad, onShow, onReady, onHide, onUnload, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'

onLoad((options) => {
  // 页面加载，options接收路由参数（只触发一次）
  const id = options.id
})

onShow(() => {
  // 页面显示（每次从后台切回都触发，刷新数据放这里）
})

onReady(() => {
  // 页面DOM渲染完成（操作节点放这里）
})

onPullDownRefresh(() => {
  // 下拉刷新（需在pages.json开启enablePullDownRefresh）
  fetchData().finally(() => uni.stopPullDownRefresh())
})

onReachBottom(() => {
  // 触底加载更多
  if (!loading.value && hasMore.value) loadMore()
})
```

### ⚠️ 生命周期陷阱
| 陷阱 | 说明 | 正确做法 |
|------|------|----------|
| onLoad vs onMounted | onLoad先于onMounted执行 | 页面初始化逻辑放onLoad |
| onShow频繁触发 | 切tab/从子页面返回都触发 | 用标志位防重复请求 |
| 组件中用onLoad | 组件不是页面，onLoad不触发 | 组件用onMounted |
| onUnload清理 | 定时器/事件监听必须清理 | onUnload中clearInterval |

## 路由与导航

```javascript
// 保留当前页，跳转（最多10层栈）
uni.navigateTo({ url: '/pages/detail/index?id=123' })

// 关闭当前页，跳转
uni.redirectTo({ url: '/pages/result/index' })

// 关闭所有页，跳转
uni.reLaunch({ url: '/pages/index/index' })

// 切换Tab页（只能跳tabBar页面）
uni.switchTab({ url: '/pages/home/index' })

// 返回上一页
uni.navigateBack({ delta: 1 })

// 接收参数
onLoad((options) => {
  // options.id = '123'（注意：值都是string类型）
  const id = Number(options.id)
})
```

### 页面通信
```javascript
// 方式1：EventChannel（推荐，navigateTo专用）
uni.navigateTo({
  url: '/pages/select/index',
  events: {
    onSelect(data) { /* 接收子页面数据 */ }
  },
  success(res) {
    res.eventChannel.emit('initData', { id: 1 })
  }
})
// 子页面
const channel = this.getOpenerEventChannel()
channel.on('initData', (data) => {})
channel.emit('onSelect', { selected: true })

// 方式2：uni.$emit / uni.$on（全局事件，记得off）
uni.$on('refreshList', handler)
uni.$emit('refreshList', { page: 1 })
onUnload(() => uni.$off('refreshList', handler))

// 方式3：globalData / Pinia
```

## 网络请求封装

```javascript
// utils/request.js
const BASE_URL = import.meta.env.VITE_API_BASE || ''

export function request(options) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
        ...options.header,
      },
      timeout: options.timeout || 15000,
      success: (res) => {
        if (res.statusCode === 401) {
          uni.removeStorageSync('token')
          uni.reLaunch({ url: '/pages/login/index' })
          return reject(new Error('登录过期'))
        }
        if (res.statusCode !== 200) {
          return reject(new Error(`HTTP ${res.statusCode}`))
        }
        if (res.data.code !== 0) {
          uni.showToast({ title: res.data.msg || '请求失败', icon: 'none' })
          return reject(new Error(res.data.msg))
        }
        resolve(res.data)
      },
      fail: (err) => {
        uni.showToast({ title: '网络错误', icon: 'none' })
        reject(err)
      },
    })
  })
}

export const get = (url, data) => request({ url, data, method: 'GET' })
export const post = (url, data) => request({ url, data, method: 'POST' })
```

## 分包加载

### pages.json配置
```json
{
  "pages": [
    { "path": "pages/index/index" },
    { "path": "pages/login/index" }
  ],
  "subPackages": [
    {
      "root": "pages-order",
      "pages": [
        { "path": "list/index" },
        { "path": "detail/index" }
      ]
    },
    {
      "root": "pages-user",
      "pages": [
        { "path": "profile/index" },
        { "path": "settings/index" }
      ]
    }
  ],
  "preloadRule": {
    "pages/index/index": {
      "network": "all",
      "packages": ["pages-order"]
    }
  }
}
```

### 分包规则
| 限制 | 微信小程序 | 支付宝小程序 |
|------|-----------|-------------|
| 主包大小 | ≤2MB | ≤2MB |
| 单个分包 | ≤2MB | ≤2MB |
| 总包大小 | ≤20MB | ≤8MB |

### 分包优化策略
- 主包只放tabBar页面+公共组件+启动必需资源
- 按功能模块分包（订单/用户/设置各一个分包）
- 大图片/字体放分包或CDN
- 用`preloadRule`预加载下一步可能访问的分包
- 独立分包(`independent: true`)可不依赖主包独立运行

## 微信开放能力

### 登录
```javascript
async function wxLogin() {
  const { code } = await uni.login({ provider: 'weixin' })
  // code发给后端换openid/session_key
  const res = await post('/api/wx/login', { code })
  uni.setStorageSync('token', res.data.token)
}
```

### 支付
```javascript
async function wxPay(orderId) {
  // 后端生成支付参数
  const { data } = await post('/api/wx/pay', { orderId })
  // 调起支付
  await uni.requestPayment({
    provider: 'wxpay',
    timeStamp: data.timeStamp,
    nonceStr: data.nonceStr,
    package: data.package,
    signType: data.signType,
    paySign: data.paySign,
  })
  uni.showToast({ title: '支付成功' })
}
```

### 分享
```javascript
// 页面中定义分享（只在页面级生效，组件中无效）
import { onShareAppMessage, onShareTimeline } from '@dcloudio/uni-app'

onShareAppMessage(() => ({
  title: '分享标题',
  path: '/pages/index/index?from=share',
  imageUrl: '/static/share.png', // 5:4比例
}))

onShareTimeline(() => ({
  title: '朋友圈标题',
  query: 'from=timeline',
}))
```

## 常见坑与解决方案

| 问题 | 原因 | 解决 |
|------|------|------|
| v-html不生效 | 小程序不支持v-html | 用`<rich-text :nodes="html" />` |
| 动态class不生效 | 小程序不支持对象语法 | 用数组语法`:class="[active ? 'on' : '']"` |
| 背景图不显示 | 小程序不支持本地背景图 | 用网络图片URL或base64 |
| scroll-view高度 | 需明确设置高度 | `calc(100vh - navHeight)` |
| 组件样式穿透 | scoped+小程序组件隔离 | 用`:deep()`或`/deep/`或`page`级样式 |
| textarea层级最高 | 原生组件层级问题 | 用`cover-view`覆盖 |
| 页面栈溢出 | navigateTo超10层 | 用redirectTo或reLaunch |
| 图片模糊 | 未用2x/3x图 | 图片宽度用实际显示尺寸的2-3倍 |
| 请求并发限制 | 微信最多10个并发 | 用请求队列控制 |

## 性能优化

### 启动速度
- 主包精简：只放首页+tabBar页，其余全部分包
- 代码按需引入：组件/工具函数用到才import
- 图片懒加载：`<image lazy-load />`
- 数据预拉取：`preloadRule`预加载分包

### 渲染性能
- 减少setData数据量：只传变化的字段，不传整个对象
- 长列表用虚拟滚动：`<recycle-list>`或三方虚拟列表组件
- 避免频繁setData：节流/防抖scroll/input事件
- 减少WXML节点数：单页<1000个节点
- 图片用webp格式：体积减少30%+

### 包体积
```
主包checklist:
□ 图片已压缩（tinypng）且<200KB/张
□ 大图已移至CDN
□ 未使用的页面/组件已删除
□ 第三方库按需引入（不全量import）
□ static/目录无冗余文件
```

## 小程序审核红线

| 红线 | 说明 |
|------|------|
| 虚拟支付 | iOS小程序禁止虚拟商品支付（用IAP或引导到App） |
| 分类资质 | 涉及金融/医疗/教育需对应资质证书 |
| 用户隐私 | 必须有隐私弹窗，收集信息需说明用途 |
| 内容安全 | UGC内容必须接入内容安全API过滤 |
| 登录授权 | 不能强制登录才能使用基础功能 |
| 诱导分享 | 不能强制分享后才能使用功能 |
| 跳转限制 | 不能跳转到未关联的小程序/外部链接 |

## pages.json常用配置

```json
{
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "应用名",
    "navigationBarBackgroundColor": "#FFFFFF",
    "backgroundColor": "#F5F5F5",
    "enablePullDownRefresh": false
  },
  "tabBar": {
    "color": "#999",
    "selectedColor": "#1890ff",
    "backgroundColor": "#fff",
    "borderStyle": "white",
    "list": [
      { "pagePath": "pages/index/index", "text": "首页", "iconPath": "static/tab/home.png", "selectedIconPath": "static/tab/home-active.png" },
      { "pagePath": "pages/user/index", "text": "我的", "iconPath": "static/tab/user.png", "selectedIconPath": "static/tab/user-active.png" }
    ]
  }
}
```

## 约束
- 所有发现必须有file:line引用
- 优先UniApp官方API，不引入不必要的平台特有库
- 条件编译处理平台差异，禁止运行时大量平台判断
- 保持项目现有的代码风格，不引入新范式
- 小程序审核规范必须遵守，不绕过平台规则
