---
name: debugging-deep
description: "深度调试方法论——断点诊断、堆栈分析、内存 Dump、事后调试、时间旅行调试。用于复杂 Bug 和疑难问题的深度排查。"
version: "4.3.8"
updated: "2026-05-14"
---

# 深度调试方法论

## 概述

深度调试超越"加个 log 看看"的层次，用断点、堆栈分析、内存 Dump、事后调试（post-mortem）等技术系统化定位根因。适用于框架级、并发、内存相关等复杂问题。

**核心原则：** 调试是假设驱动的调查，不是碰运气的试探。每个断点、每个变量检查都应服务于一个明确的假设。

## 何时使用

**适用场景：**
- `console.log` 无法定位的复杂 Bug
- 并发问题（竞态条件、死锁）
- 内存泄漏
- 第三方库/框架内部异常
- 仅在生产环境复现的 Bug（事后调试）
- 崩溃/段错误/核心转储分析

**不适用场景：**
- 一眼能看出的逻辑错误（直接修）
- 简单类型错误（TS 编译器已指出）
- 缺少复现步骤的问题（先复现再调试）

---

## 方法论

### 步骤 1：定义调试假设（D0）

在动手调试前，明确你的假设：

```
## 调试假设
主假设: 用户登录后 session 丢失是因为 Redis 连接在负载下断开

备选假设:
  1. Session TTL 设置过短
  2. Cookie 未正确设置
  3. 负载均衡器未保持会话亲和性

证据需求:
  - Redis 连接日志（确认断开时间）
  - Session 创建和读取的时序
  - 并发连接数监控
```

### 步骤 2：建立复现环境（D1）

```javascript
// 最小复现脚本
import { createServer } from 'node:http';
import { createClient } from 'redis';

const redis = createClient();
await redis.connect();

const server = createServer(async (req, res) => {
  // 模拟登录
  const sessionId = 'test-session';
  await redis.setEx(`session:${sessionId}`, 30, 'user-data');
  
  // 读取 session
  const data = await redis.get(`session:${sessionId}`);
  console.log('Session data:', data);
  
  res.end(data || 'NO SESSION');
});

server.listen(3000);
```

### 步骤 3：调试工具选择

| 调试场景 | 首选工具 | 备选工具 |
|---------|---------|---------|
| **Node.js 应用** | Chrome DevTools / VS Code | `ndb` |
| **Python 应用** | `pdb` / `ipdb` | VS Code Python |
| **Go 应用** | `delve` (dlv) | VS Code Go |
| **浏览器 JS** | Chrome DevTools Sources | Firefox Debugger |
| **内存泄漏** | Chrome Heap Snapshot | `clinic heapprofiler` |
| **CPU 热点** | Chrome Performance | `clinic flame` |
| **核心转储** | `lldb` / `gdb` | `node --abort-on-uncaught-exception` |

### 步骤 4：断点调试技巧（D2-D3）

#### 条件断点
只在满足条件时暂停，避免反复手动跳过：
```javascript
// Chrome/VS Code: 右键断点 → Edit Breakpoint → Condition
// 条件: user.role === 'admin' && requestCount > 100

// Node.js debugger
debugger; // 配合 --inspect-brk 使用
```

#### 日志断点（Logpoint）
不暂停执行，只输出变量值：
```javascript
// Chrome/VS Code: 右键断点 → Edit Breakpoint → Logpoint
// 无需插入 console.log，不修改代码
// 日志: "User {user.id} - {user.email} at {new Date().toISOString()}"
```

#### 调用栈导航
```
Chrome DevTools:
  Call Stack 面板 → 点击上层帧 → 查看调用者局部变量
  Scope 面板 → Local / Closure / Global 变量

VS Code:
  CALL STACK 面板 → 双击帧跳转
  VARIABLES 面板 → 展开查看对象属性
```

#### Watch 表达式
实时计算复杂表达式：
```javascript
// Watch 面板添加：
users.filter(u => u.role === 'admin').length
JSON.stringify(response.data, null, 2)
```

### 步骤 5：内存分析

#### 堆快照（Heap Snapshot）
```bash
# Node.js: 生成堆快照
node --heapsnapshot-signal=SIGUSR2 app.js
# 或代码中
const v8 = require('v8');
const fs = require('fs');
fs.writeFileSync('heap.heapsnapshot', v8.writeHeapSnapshot());

# Chrome DevTools → Memory → Load → 对比两个快照
# 查找: 两次快照之间增加的对象（泄漏源）
```

#### 内存泄漏排查流程
1. 拍快照 1（基线）
2. 执行疑似泄漏操作 100 次
3. 拍快照 2
4. 对比快照：按 `Shallow Size` 或 `Retained Size` 排序
5. 找到持续增长的对象类型
6. 追溯到持有该对象的引用链

#### 典型泄漏模式：
```javascript
// 1. 全局变量累积
global.cache = [];  // 持续 push 未清理

// 2. 闭包引用
function createHandler() {
  const bigData = loadHugeFile();  // 闭包持有引用
  return () => bigData.length;     // 即使只用了 length
}

// 3. 事件监听器未移除
emitter.on('data', handler);  // 忘记 removeListener
```

### 步骤 6：事后调试（Post-Mortem）

适用于仅在生产环境发生的崩溃：

```bash
# Node.js: 生成核心转储
node --abort-on-uncaught-exception app.js
# 崩溃后生成 core dump 文件

# 分析核心转储
llnode node -c core.node.12345
# llnode> v8 findjsobjects
# llnode> v8 findjsinstances User
# llnode> jsstack

# 或使用 Node.js 内置诊断
node --report-on-fatalerror --report-uncaught-exception app.js
# 生成 report.YYYYMMDD.HHMMSS.PID.SEQUENCE.txt
```

**报告文件分析：**
```
关键字段:
  - JavaScript Stack Trace: JS 层崩溃位置
  - Native Stack Trace: 原生(C++)层崩溃位置
  - JavaScript Heap: 堆内存使用情况
  - Resource Usage: CPU/内存/文件描述符
  - libuv Handle Summary: 活动句柄数（检查泄漏）
```

### 步骤 7：时间旅行调试（可选）

```bash
# rr (Record and Replay) — 用于 C/C++/Rust
rr record ./myapp
rr replay  # 可以反向执行、反向打断点

# Replay.io — 用于浏览器 JS
# 录制用户操作，回放时附加 DevTools

# Wallaby.js — 实时时间旅行测试
```

---

## 常见问题诊断指南

### 问题：异步操作顺序混乱
```
诊断:
  1. 在所有 async 调用前后打断点
  2. 记录每个 Promise 的创建和 resolve 时间戳
  3. 对比预期顺序 vs 实际顺序

常见原因:
  - Promise.all 中某个 reject 未被 catch
  - await 遗漏导致并发执行
  - 事件监听器中的异步操作未排队
```

### 问题：偶尔出现的 null 引用
```
诊断:
  1. 条件断点: 变量 === null 或 undefined 时暂停
  2. 回溯调用栈，找到 null 产生的源头
  3. 检查是否有竞态条件（两个操作同时修改状态）

常见原因:
  - 异步数据还未加载就被访问
  - 缓存过期但未重新加载
  - Map/Set 中 key 不存在时继续操作 value
```

### 问题：生产环境特定 Bug
```
诊断（按优先级）:
  1. 检查环境差异: 配置、依赖版本、数据量
  2. 增加结构化日志（trace id、关键变量）
  3. 如可能，在 staging 复制生产数据子集
  4. 使用特性开关在生产只对内部用户开启调试日志
```

---

## 反模式

| 反模式 | 正确做法 |
|--------|---------|
| "加个 try-catch 包住就好了" | 掩盖错误不是修复，try-catch 必须处理或重抛 |
| 不写假设就开始打断点 | 无假设 = 随机探索 = 低效 |
| 同时改多个变量排查 | 一次只改一个变量，否则不知道哪个是原因 |
| `console.log` 替代断点 | log 看不到完整上下文，断点可以检查所有作用域 |
| 修好了但不补回归测试 | 无测试保护 = 同一个 Bug 可以再现 |
| 不清除调试代码 | 残留的 `debugger;` 在生产环境可能导致意外暂停（如果开启了 inspect） |

## 验证清单

- [ ] 调试假设已明确记录
- [ ] 最小复现脚本可稳定复现（100% 或高概率）
- [ ] 根因已定位到具体文件和行号
- [ ] 修复方案已与假设对比验证
- [ ] 回归测试已添加
- [ ] 调试代码（logpoint、debugger 语句、临时日志）已清除
- [ ] 类似代码模式已排查
