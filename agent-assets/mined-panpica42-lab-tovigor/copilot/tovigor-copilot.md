# Tovigor 健身应用 - AI 开发指南

> **最后更新**: 2026-03-06

## 项目概览

这是一个基于 **uni-app (Vue 3)** 的健身应用，运行在 HBuilderX 中，主要目标平台是 **Android App**。核心特点是通过自定义 UTS 插件与硬件设备（串口通信）集成，实现智能健身设备控制。

## 架构要点

### 技术栈
- **框架**: uni-app Vue 3 (Composition API)
- **构建工具**: HBuilderX + @dcloudio/uni-cli          
- **平台**: Android App (app-android)，H5 仅用于调试
- **原生集成**: UTS (TypeScript-like) 插件系统 + Kotlin AAR 库

### 目录结构
```
tovigor_v1/
├── pages/                     # 页面目录
│   ├── index/                 # 首页
│   ├── freeTraining/          # 自由训练
│   ├── partTraining/          # 部位训练
│   ├── smartAssess/           # 智能评估（含 body-strength-assess/ 等子目录）
│   ├── idle/                  # 待机页
│   └── serial-test/           # 串口调试（v1 直接调 UTS，v2 用 serialService）
├── components/                # 全局组件
│   ├── modals/                # 弹窗组件
│   └── ui-box/                # UI 基础组件
├── utils/                     # 工具函数
│   ├── serialService.js       # 【核心】串口服务层
│   └── coachManager.js        # AI 教练管理
├── uni_modules/wzl-serialbridge/  # UTS 串口插件
├── docs/                      # 项目文档（通信模块、开发日志等）
├── App.vue                    # 应用入口（串口 connect() 在此调用）
├── pages.json                 # 页面路由
└── manifest.json              # 应用配置
```

## 串口通信架构（重要！）

### 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│  Vue 页面层 (skip1.vue, free-training.vue ...)              │
│  - UI 交互                                                  │
│  - 订阅事件: on('frame', handleFrame)                       │
│  - 控制工作状态: startWorking() / stopForce()             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  JS 服务层 (utils/serialService.js)                         │
│  - 单例管理串口连接                                          │
│  - 事件订阅/分发 (on/off/emit)                              │
│  - 帧解析（拆包/粘包/CRC校验）                               │
│  - 轮询定时器管理                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  UTS 插件层 (uni_modules/wzl-serialbridge)                  │
│  - openSerial / closeSerial / readSerial / writeSerial      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  AAR 层 (serialbridge.aar)                                  │
│  - Kotlin 代码，直接操作 /dev/ttyS*                          │
└─────────────────────────────────────────────────────────────┘
```

### 页面调用串口的正确方式

**关键原则**：
- **App.vue 负责连接**：应用启动时调用 `connect()`
- **页面只订阅事件 + 控制工作状态**：不调用 `connect()`/`disconnect()`

```javascript
// ✅ 正确的页面代码
import { on, off, startWorking, stopForce, getStatus } from '@/utils/serialService.js'

onMounted(() => {
  // 1. 订阅帧事件
  on('frame', handleFrame)
  
  // 2. 检查连接状态（App.vue 已连接）
  const status = getStatus()
  if (status.isConnected) {
    console.log('串口已连接，等待用户操作')
  }
})

// 3. 用户点击"开始"按钮时，才启动工作状态
const handleStart = () => {
  startWorking(force, mode, interval)  // 周期发送指令 + 轮询读取
}

onBeforeUnmount(() => {
  off('frame', handleFrame)
  stopForce()  // 安全停力，但不断开连接
})
```

### serialService.js 核心 API

| API | 说明 |
|-----|------|
| `connect(options)` | 连接串口（App.vue 调用，页面不调用） |
| `disconnect()` | 断开连接（App.vue 调用） |
| `on(event, callback)` | 订阅事件：'frame', 'raw', 'connect', 'disconnect', 'error' |
| `off(event, callback)` | 取消订阅 |
| `startWorking(force, mode, interval)` | 启动工作状态（周期发送 + 轮询） |
| `stopForce(options)` | 安全停力序列（持续发 OFF 帧，不断开连接） |
| `updateWorkingForce(force, mode)` | 动态更新力量值 |
| `getStatus()` | 获取连接状态 `{ isConnected, portId, config }` |
| `send(hexData)` | 发送原始数据 |

### 通信协议

#### A9 上行帧（设备 → App，96字节）

| 偏移 | 长度 | 字段 | 说明 |
|------|------|------|------|
| 0 | 1 | header | 帧头 0x73 ('s') |
| 1 | 1 | packType | 包类型 0x09 |
| 2 | 1 | index | 包序号 |
| 3-14 | 12 | left | 左手数据（距离、速度、次数、功率、瞬时力量） |
| 15-26 | 12 | right | 右手数据 |
| 27 | 1 | setForce | 设定力量 (kg) |
| 28 | 1 | setForceMode | 力量模式 (0-7) |
| ... | ... | ... | 其他字段（温度、电压、LOG等） |
| 93-94 | 2 | crc | CRC-16 大端序 |
| 95 | 1 | tail | 帧尾 0x65 ('e') |

#### D180 下行帧（App → 设备，9字节）

| 偏移 | 长度 | 字段 | 说明 |
|------|------|------|------|
| 0 | 1 | header | 帧头 0x73 |
| 1 | 1 | packType | 包类型 0xB4 (180) |
| 2 | 1 | index | 包序号 |
| 3 | 1 | force | 力量值 (0-100 kg) |
| 4 | 1 | forceMode | 力量模式 |
| 5 | 1 | lock | 锁定标志 |
| 6-7 | 2 | crc | CRC-16 大端序 |
| 8 | 1 | tail | 帧尾 0x65 |

#### 力量模式枚举

| 值 | 模式 |
|----|------|
| 0 | 关闭 |
| 1 | 恒力 |
| 2 | 离心等张 |
| 3 | 向心等张 |
| 4 | 弹力绳 |
| 5 | 流体阻力 |
| 6 | 平衡 |
| 7 | 绳索B1 |

#### ⚠️ 力量控制重要规则

| 场景 | forceMode | force | 说明 |
|------|-----------|-------|------|
| **关闭力量** | 0 | **非0**（默认5） | 正常关闭，绳子松开 |
| **紧急停车** | 0 | **0** | 硬件级紧急停车，慎用！ |

**关闭力量的正确写法**：
```javascript
sendOnce(5, FORCE_MODE.OFF)  // ✅ 模式0 + 力量5 = 正常关闭
sendOnce(0, FORCE_MODE.OFF)  // ❌ 模式0 + 力量0 = 紧急停车！
```

#### CRC 算法（特殊口径）

```javascript
// 1. 取 CRC 字段之前的所有字节
// 2. 预处理：补0到4的倍数 + 每4字节分组倒序
// 3. CRC-32 非反射(MSB-first), Poly=0x04C11DB7, Init=0xFFFFFFFF
// 4. 取低16位，大端存储
```

详细实现见 `utils/serialService.js` 中的 `computeCrc16Fixed()` 函数。

## 关键业务逻辑

### 1. UTS 插件（底层）
**核心文件**: `uni_modules/wzl-serialbridge/`

- **API 风格**: uni-app 回调式（success/fail/complete）
- **数据格式**: HEX 字符串（例如 `"73B4000A01002AF365"`）
- **错误码**: 10001-10007
- **自定义基座必需**: 标准基座不包含 UTS 插件

### 2. 自由训练页（`freeTraining.vue`）
- **力量旋钮**: 触摸角度映射到 0-100kg
- **训练模式**: 6 种模式通过数组索引管理
- **与串口集成**: 调用 `updateWorkingForce()` 实时更新力量值

### 3. 力量评估页（`smartAssess/body-strength-assess/skip1.vue`）
- **串口集成模式**: 页面订阅事件 + 按钮触发 `startWorking()`
- **调试面板**: `DEBUG_PANEL_VISIBLE` 开关控制显示/隐藏
- **力量柱状图**: 实时显示左右手力量数据

### 4. 串口测试页（`serial-test/serial-test.vue`）
**最重要的调试工具**，用于验证底层通信功能。

## 开发调试技巧

### Debug Panel 模式

在开发阶段，可以在页面中添加调试面板实时查看串口数据：

```javascript
// 开关
const DEBUG_PANEL_VISIBLE = true  // 发布时改为 false

// 数据
const debugData = reactive({
  setForce: 0,
  setForceMode: 0,
  leftForce: 0,
  rightForce: 0
})

// 在 handleFrame 中更新
const handleFrame = (data) => {
  if (DEBUG_PANEL_VISIBLE) {
    debugData.setForce = data.parsed.setForce
    // ...
  }
}
```

```html
<!-- 调试面板（右下角半透明） -->
<view v-if="DEBUG_PANEL_VISIBLE" class="debug-panel">
  <text>设定力量: {{ debugData.setForce }} kg</text>
  <!-- ... -->
</view>
```

### ADB 调试命令

```bash
# 查看串口相关日志
adb logcat | grep -i "serial\|wzl"

# 查看可用串口设备
adb shell ls -l /dev/tty*

# 设置串口权限
adb shell chmod 666 /dev/ttyS3
```

## 开发工作流

### 本地开发
```powershell
# H5 调试（仅 UI，串口不可用）
运行 → 运行到浏览器 → Chrome

# Android 真机调试（需自定义基座）
运行 → 运行到手机或模拟器 → 运行到 Android App 基座
```

### 自定义基座制作
1. `运行 → 制作自定义调试基座`（云端打包 3-5 分钟）
2. 基座 APK 下载到 `unpackage/debug/android_debug.apk`
3. 安装到设备后，代码修改支持热更新

**常见错误**:
- "Cannot read property 'openSerial' of undefined" → 使用了标准基座
- "打开串口失败 (10001)" → 设备路径错误或权限不足

## 代码约定

### Vue 组件风格
- **Composition API** (`<script setup>`)
- **响应式数据**: `ref` 而非 `reactive`（便于解构）
- **生命周期**: `onMounted`, `onBeforeUnmount` 等组合式 API
- **页面生命周期**: `onShow`, `onHide` 从 `@dcloudio/uni-app` 导入

### 样式规范
- **单位**: 全部使用 `rpx`，避免 `px`
- **布局**: Flexbox，避免浮动
- **Scoped 样式**: 所有组件必须加 `<style scoped>`

### uni-app image 组件注意事项
- **禁止使用 `height: auto`**：uni-app 的 `<image>` 不支持 `height: auto`，会导致图片不显示
- **禁止使用 `min-height` 替代**：`min-height: 100%` 等写法同样无效，必须用固定值
- **必须指定具体尺寸**：使用固定 `rpx` 或 `px` 值，如 `width: 550rpx; height: 300rpx;`
- **父容器 overflow: hidden 会裁掉超出部分**：如需图片溢出显示，确保父容器无此属性
- **游戏/动画场景**：对于需要超出容器显示的图片，使用固定大值（如 `height: 800px`）配合 `object-fit: cover` 和 `object-position` 控制显示区域

### 文件命名
- 页面目录: 小驼峰或短横线（`freeTraining/`、`body-strength-assess/`）
- 组件: 短横线（`modal-dialog.vue`、`bubble-dialog-box.vue`）
- 静态资源: 下划线（`ic_power.svg`、`bg_stat_board.png`）

## 弹窗组件使用

### modal-dialog.vue（对话框弹窗）

```vue
<ModalDialog 
  v-model:show="showModal"
  title="提示"
  confirmText="确定"
  @confirm="handleConfirm"
  @cancel="handleCancel"
>
  <text>弹窗内容</text>
</ModalDialog>
```

### 浮动关闭按钮模式

```vue
<!-- 弹窗外部的关闭按钮 -->
<view class="modal-wrapper">
  <view class="modal-card">
    <!-- 内容 -->
  </view>
  <view class="floating-close-btn" @click="close">
    <image src="/static/icons/general/btn_general_close.svg" />
  </view>
</view>
```

## 关键文件速查

| 文件 | 说明 |
|------|------|
| `utils/serialService.js` | 串口通信服务层（单例） |
| `App.vue` | 应用入口，串口 `connect()` 在此调用 |
| `pages/serial-test/serial-test.vue` | 串口调试工具 |
| `uni_modules/wzl-serialbridge/` | UTS 串口插件 |
| `docs/通信模块/通信架构.md` | 通信架构详细文档 |
| `pages.json` | 页面路由配置 |
| `manifest.json` | 应用配置（权限等） |

## 重要提醒

1. **H5 仅用于 UI 预览**，串口必须在 Android 真机测试
2. **修改 UTS 插件或 AAR 后必须重新制作基座**
3. **页面不要调用 `connect()`**，连接由 App.vue 管理
4. **HBuilderX 版本需 >= 3.6.0**
5. **串口设备路径**通常为 `/dev/ttyS3`，需在目标硬件确认
