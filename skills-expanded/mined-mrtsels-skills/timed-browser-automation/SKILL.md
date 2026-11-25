---
name: timed-browser-automation
description: 抢课/选课/到点抢购等定时自动点击脚本的计时设计：先测系统时钟偏差，再定轮询+缓冲， 保证 click 不早于目标时刻。
metadata:
  imported_from: hermes
---

# Timed Browser Automation（定时自动点击脚本）

## When to use
Trigger: 抢课、选课、到点抢购、定时提交、任何需要在精确时刻点击的浏览器脚本（course registration / CUSIS、flash sale、ticket drop）。

## Core principle
**click 绝不能在目标时刻之前发生。** 提前点击 = 白点（窗口未开，服务器直接拒绝）；晚几十毫秒通常无影响（服务器未必处理 ms 级差异）。所有计时决策向"晚"倾斜，绝不向"早"倾斜。

## Step 1: 先测系统时钟偏差（bias）
浏览器**没有自己的 NTP 配置，完全跟随操作系统时钟**。设计计时前必须先测系统时钟相对真实时间的偏差：
- macOS: `sntp -sS <server>` 输出 `+0.068 +/- 0.096` = 本地时钟**快** 68ms（正 = 快）
- 每源采样 3 次，并用 ≥2 个独立源交叉验证（time.apple.com / time.google.com / time.nist.gov / hk.pool.ntp.org）
- 取偏差的保守上界作为设计值
- 2026-08 实测（用户 Mac）：各源 +42~146ms，稳定 ~+68ms（详见 references/cusis-enroll-2026.md）

## Step 2: 轮询 + 缓冲结构（保证不提前）
```
setInterval(60ms):                          // 轮询
  if (target > new Date()) 继续等待
  else { setTimeout(() => click(), BUFFER); clearInterval(interval); }
```
安全条件：**BUFFER > 时钟偏差 + 轮询滞后 + 余量**
- 轮询滞后 ≤ 轮询间隔（最坏情况：目标时刻刚过检查点）
- 余量 ≥ 20-30ms
- 实测例：偏差 70ms + 轮询 10ms → BUFFER 100ms 安全；80ms 危险（仅剩 10ms 余量）

## Step 3: 用 instrumentation 验证，别信数学
```js
const t0 = performance.now();
// ...click 后：
window.__timing = { detectAfterTargetMs: ..., clickAfterTargetMs: ... };
```
确认 `clickAfterTargetMs > 0`（严格晚于目标）。60ms 轮询实测：detect +80ms、click +273ms（晚，安全）。

## Step 4: 用户的 log overlay 样式偏好（其脚本通用）
用户对这些脚本的浮层日志有明确的迭代偏好：
- 位置：`position: fixed; bottom: 0`（贴屏幕底部）
- 对齐：`textAlign: center`（用户从 left → right → 最终定 center）
- 单行：`overlay.innerText = message`（替换而非 append，最多 1 行）
- 时间戳：`HH:MM:SS.mmm`（毫秒精度）
- 语言：STE100 简化技术英语（主动语态、现在时、无 "will"/"e.g."——加载 `simplified-technical-english` skill）
- **样式复用坑**：overlay 只在 `if (!overlay)` 时创建；同页重跑复用的是旧元素，旧样式残留。样式属性要写在 create-if-absent **块外**，每次运行强制应用

## Pitfalls
1. **HTTP `Date` 头是秒级精度**——误差 ±500ms 比时钟偏差还大，不能用于校准。只用 NTP。
2. **NTP 漂移**：OS 周期性校准，两次校准之间石英钟漂移（~±10ppm = 0.01ms/s）。长时间无校准可能让偏差超过缓冲——缓冲保持 ≥ 2× 实测偏差。
3. **浏览器时间 = OS 时间**：要"改 Chrome 的时间"实际是改 macOS（`sudo systemsetup -setnetworktimeserver <server>`；`/etc/ntp.conf` 显示当前服务器）。Chrome 唯一的额外机制是被动 TLS 时间校准（仅用于证书验证）。
4. **多登录限制（PeopleSoft/CUSIS）**：测试时绝不用同一账号开第二个浏览器会话——系统检测到会限制/锁定原会话（"Restricted Multiple Login Error"）。恢复 = 完全退出 Chrome 重开 + 重新登录（单会话）。只在唯一的已登录会话上测。
5. **验证 click 真的发生了**：`.click()` 要包 try/catch 且先检查元素存在；裸 `btn.click()` 失败 + 乐观日志 = "看似成功实际没点"。

## References
- `references/cusis-enroll-2026.md` — CUSIS 抢课脚本会话数据：实测 NTP 偏差、计时 instrumentation、2026 验证过的选择器、enroll.js/validate.js 位置与架构
