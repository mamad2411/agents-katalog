---
name: "weibo-qr-login"
title: "Weibo QR Login on a Cloud Container"
description: "需要在云端容器登录微博时，用手机扫码完成登录，输出登录成功的浏览器会话。"
type: skill
tags: [weibo, playwright, qr-login, cloud-container, session]
created: 2026-11-08
updated: 2026-11-08
author: scriptsmay
status: active
---

# Weibo QR Login on a Cloud Container

在没有本地浏览器的云端 Linux 容器/虚拟机上，用手机扫码登录微博。Playwright + 系统 Chromium + 持久化浏览器 profile；登录二维码只发给账号本人。

Log into Weibo from a cloud Linux container/VM with no local browser: scan a QR code with the phone app. Playwright + system Chromium. The script logs in once and exits.

> **本技能不含任何真实账号、Cookie、二维码与机器信息。** 登录二维码是登录凭证，只通过私密通道发给账号本人，扫完即删；脚本写出的全部文件都只留在你自己的机器上，**不要进仓库、不要进群聊、不要进日志分享**。
> This skill contains no real account, cookie, QR code or machine identity. A QR code is a login credential: send it only to the account owner over a private channel and delete it after the login. All files the script writes stay on your own machine and must never enter a repository, a group chat or a shared log.

<!-- 技能设计至少明确六项：名称、WHEN、WHAT、HOW、REFERENCE、LIMITS。 -->

## 适用场景与触发条件（WHEN）

- **触发场景**：需要在云端 Linux 容器/虚拟机上登录微博做自动化（发博、互动、数据抓取），但容器没有本地浏览器可操作，账号本人只能用手机配合扫码。
- **典型请求**：“在云容器上登一下微博，扫码登录。”
- **不适用情形**：
  - 账号本人不在场、10 分钟内没人能扫码并在 App 里点确认——不要启动登录流程。
  - 容器没有系统 Chromium，或访问不了 `weibo.com`。
  - 需要批量登录多个账号——本技能一次只登一个号，换号要换工作目录与 profile。
  - 想用密码/短信码登录——本技能只覆盖扫码路径。
  - 需要持续检测登录态是否在线、掉线自动处理——不在本技能范围内。

## 目标、输入与输出（WHAT）

- **目标**：在云端容器里完成一次微博扫码登录，不依赖本地电脑、不输密码、不收短信码；登录态存在持久化 profile 里，供后续使用。脚本只负责登上去，登上去就退出。
- **必需输入**：
  - 一台 Linux 云容器/虚拟机，已装系统 Chromium，能直接访问 `weibo.com`。
  - Python 3.11+，`pip install playwright`（不需要 `playwright install` 下载浏览器，用系统 Chromium 作 `executable_path`）。
  - 容器里可写的持久目录（示例 `$HOME/weibo-login`）；会话 profile 落在这里。
  - 一部装了微博 App 的手机 + 要登录的账号；一个**私密通道**（自己与自己的 DM、加密笔记）用来接收二维码图片。
  - 账号本人在场：扫码与 App 内“确认登录”必须本人做，agent 不能代扫。
- **可选输入 / 默认值**：

  | 占位符 / 环境变量 | 含义 | 说明 |
  |---|---|---|
  | `WB_LOGIN_DIR` | 工作目录，默认 `$HOME/weibo-login` | profile、二维码、状态与截图全落在这里；**不要指向仓库目录** |
  | `CHROMIUM_PATH` | 系统 Chromium 路径，默认 `/usr/bin/chromium` | `which chromium` 核实；不要另下浏览器 |
  | `WB_SCAN_TIMEOUT_SEC` | 等扫码的最长等待，默认 `1800`（30 分钟） | 二维码本身约 10 分钟过期，脚本会自动刷新 |
  | `WB_USER_AGENT` | 浏览器 UA（可选） | `Chrome/<major>` 与已装 Chromium 大版本对齐 |

- **输出形式**：登录成功的持久化浏览器会话（`$WB_LOGIN_DIR/profile`）+ `state.json`；`status.json`（本次运行的最终结果：`logged_in` / `scan_timeout`）；`logged-in.jpg`（登录后首页截图，供账号本人验明身份）。脚本跑完即退出，不常驻、不监控。
- **验收标准**：
  - profile 目录与 `state.json` 已生成；`status.json` 为 `stage=logged_in`。
  - 登录后首页截图已发账号本人，确认账号无误。

## 执行流程（HOW）

执行约定（另一个 agent 按本技能执行时，不要跳步）：先确认人在场再启动；二维码只发私密通道，每次发带时间戳的新文件；全程不碰密码与 Cookie；扫码成功只确认一次，不持续检测；登录成功先让账号本人验明身份。

1. **收集并检查输入**：核实系统 Chromium 路径、持久工作目录、账号本人在场且 10 分钟内能扫码。缺任何一项就停下来，不要猜、不要先启动再等人。

2. **按步骤处理**：

   ### 2.1 准备环境

   ```bash
   python3 -m venv venv
   ./venv/bin/python -m pip install playwright
   which chromium  # 记下路径，填 CHROMIUM_PATH；没有就先装系统 Chromium
   ```

   ### 2.2 把脚本传到容器

   脚本在 `references/weibo_qr_login.py`。如果本机与容器是两台机器，用 base64 传文件，不要手抄、不要 heredoc：

   ```bash
   # 在本机：取 base64 原文
   base64 -w0 references/weibo_qr_login.py
   # 在容器：把上一步的输出原样粘贴进 <b64> 位置
   echo <b64> | base64 -d > "$WB_LOGIN_DIR/weibo_qr_login.py"
   ```

   两个教训：手抄 base64 会传坏文件；heredoc 会吞单引号导致 `SyntaxError`。另外**不要在工作目录里放 `inspect.py`**——它会遮住 Python 标准库 `inspect` 模块，任何 `import asyncio` 的脚本启动即 `SyntaxError`；启动脚本一律加 `-P`（`python -P`，safe_path）绕过。

   ### 2.3 启动登录脚本

   ```bash
   export WB_LOGIN_DIR="$HOME/weibo-login" CHROMIUM_PATH="/usr/bin/chromium"
   mkdir -p "$WB_LOGIN_DIR"
   ./venv/bin/python -P "$WB_LOGIN_DIR/weibo_qr_login.py"
   ```

   脚本先以有头（headed）模式启动持久化上下文，失败再回退无头；`user_data_dir` 是持久化 profile，登录态存在这里。

   ### 2.4 打开登录弹窗

   脚本自动完成：点 weibo.com 首页的「登录/注册」按钮，弹出的不是模态层，**而是一个新窗口**（`passport.weibo.com/sso/signin?...&disp=popup`）。注意：

   - 普通 `.click()` 和 `openLoginLayer=1` 参数都打不开这个弹窗，必须用 `page.mouse.click()` 点按钮中心坐标；
   - 第一次点击经常不生效，脚本做最多 3 次重试，每次等 10 秒扫一遍 `ctx.pages` 找弹窗。

   ### 2.5 取码、发码、扫码

   脚本在弹窗里找二维码（`img[src*='qr.weibo.cn']`），并做方形尺寸校验（80–400 px、宽高差 < 40），否则会误中信息流里 URL 带 `qr` 的小图。截图一律 JPEG：整页 PNG 再 base64 会超输出上限被截断。

   - 二维码约 **10 分钟过期**，过期后弹窗出现「二维码错误，点击刷新」覆盖层，脚本点「点击刷新」换新码。
   - 发码必须用**带时间戳的新文件名**（`qr-<HHMMSS>.jpg`），同路径重发会被客户端缓存成旧码——实测中第二张码就是这样“刚发就失效”的。
   - 账号本人在手机微博 App 里扫码，并在 App 内点确认登录。**扫码到确认之间不要关闭弹窗。**

   ### 2.6 确认扫码成功（一次）

   ```python
   login_btn = page.get_by_role("button", name="登录/注册").count()
   composer = page.locator('[placeholder*="新鲜事"]').count()
   logged_in = (login_btn == 0 and composer > 0)
   ```

   两个已踩过的坑，不要再试：

   | 错误做法 | 现象 |
   |---|---|
   | 页内 `fetch("https://m.weibo.cn/api/config")` 判断登录 | 被跨域拦截（`TypeError: Failed to fetch`），永远返回未登录 |
   | `text=` 匹配“有什么新鲜事想分享给大家？” | 那是发博框的 `placeholder` 属性，不是文本内容，`text=` 永远匹配不到 |

   注意反直觉的一点：已登录的首页**没有**「登录/注册」按钮，所以“按钮找不到”本身就是登录成功的信号，不要把它当故障反复重试。确认只做一次：扫码成功后脚本保存 `state.json`、写 `status.json`（`stage=logged_in`）、截 `logged-in.jpg`，把首页截图发给账号本人验明身份，然后退出。会话维持与掉线处理不在本技能内。

3. **按输出规范生成结果**：登录成功后交付 `status.json` 的关键字段与 `logged-in.jpg`（仅发给账号本人）；二维码图片扫完即删，不作为交付物保留；脚本已退出，不留常驻进程。

4. **对照验收标准核对事实、完整性和格式；不确定项明确标注**：见“执行后检查清单”。登录态是否在线、Cookie 过期时间，均不在本技能的核对范围内。

### 失败处理 / Troubleshooting

| 现象 | 先查什么 |
|---|---|
| 点登录按钮没反应、弹窗不出 | 是否用了鼠标坐标点击 + 3 次重试；先看 `ctx.pages` 里有没有 `passport.weibo.com/sso/signin` 的页面 |
| 二维码“刚发就失效” | 发的是不是带时间戳的新文件；旧码是否超过约 10 分钟 |
| 登录确认永远 False | 是否还在用跨域 fetch 或 `text=` 匹配 placeholder；改 DOM 法（2.6） |
| 脚本一启动就 `SyntaxError`，提到 `asyncio` | 工作目录里是不是有个 `inspect.py` 在遮标准库；改名或用 `python -P` 启动 |
| 截图传不回来 / 内容截断 | 改 JPEG quality 60；不要传 PNG 的 base64 |
| 脚本退出后会话掉了 | 本技能只管登录一次；续期/重登是使用方自己的事，不在本技能内 |

## 参考范例（REFERENCE）

- **参考来源**：2026-11-08 云容器 + 测试号扫码登录实测（脚本 `references/weibo_qr_login.py` 即本次实测的登录流程通用化后所得）；微博登录页 `https://weibo.com/`，登录弹窗 `https://passport.weibo.com/sso/signin`；Playwright 官方文档：Persistent context（`launch_persistent_context`）与 `locator` 选择器。
- **值得沿用**：一次性扫码成功确认（无登录按钮 + 有 `placeholder*="新鲜事"`）；鼠标坐标点击登录按钮 + 3 次重试；二维码方形尺寸校验；带时间戳的二维码文件名；JPEG 截图；`python -P` 启动；base64 传文件（先取原文再粘贴）。
- **应避免**：页内跨域 fetch 判断登录；`text=` 匹配 placeholder；手抄 base64 传文件；heredoc 传脚本；工作目录放 `inspect.py`；同路径重发二维码；把 `status.json` / 二维码贴进公开频道；用本技能做持续登录态检测。

## 能力边界与安全约束（LIMITS）

- **不得**：向用户索要微博密码；把 Cookie 值、二维码、账号 UID、主页链接贴进聊天记录、日志或报告；把脚本产物（profile、`state.json`、`status.json`、二维码图）提交进任何仓库；用本技能持续检测/监控登录态、记录会话在线情况。
- **信息不足或过期时**：二维码过期（约 10 分钟）由脚本点「点击刷新」换新码；无人值守时不要启动登录；扫码成功以一次性确认为准。
- **涉及重要决策 / 外部操作时**：登录成功必须由账号本人看首页截图确认账号无误，agent 不自行认定身份；换号、换机器时换工作目录与 profile，不要复用；掉线后的处理（是否重登、何时重登）由账号本人决定，不在本技能内。

## 执行后检查清单

- [ ] 输入与前提已核实；缺失信息未被臆造。
- [ ] 结果符合目标、输出格式和验收标准。
- [ ] 事实、不确定性、过期信息与待确认事项已清楚区分。
- [ ] 未越过能力边界；需用户确认的事项已停下并说明。
- [ ] 系统 Chromium 路径已核实，`CHROMIUM_PATH` 指向它。
- [ ] 工作目录在持久盘上，不在仓库里；目录里没有 `inspect.py`。
- [ ] 二维码发的是带时间戳的新文件，走私密通道；账号本人已扫码并在 App 内确认。
- [ ] 登录后首页截图已发账号本人，确认账号无误。
- [ ] profile 目录与 `state.json` 已生成；`status.json` 为 `stage=logged_in`。
- [ ] 二维码图片已删除；`status.json` 没进过任何公开渠道。

## 实际使用案例

- 日期：2026-11-08
  - 场景 / 输入：云容器 + 测试号扫码登录；Playwright 1.64 + 系统 Chromium；账号本人在场配合扫码。
  - 结果：第一张码约 10 分钟过期、第二张疑似缓存旧图失效，第三张码扫码 + App 内确认后登录成功；登录确认最初两次方法全错（跨域 fetch、placeholder 的 `text=` 匹配），改 DOM 法后确认。
  - 后续改进：登录确认改为 DOM 法已固化进脚本；发码改为带时间戳的新文件名已固化。

## 参考 / References

- 本仓库模板：`references/weibo_qr_login.py`（登录脚本，环境变量见文件头注释）
- Playwright 官方文档：Persistent context（`launch_persistent_context`）与 `locator` 选择器
- 微博登录页：`https://weibo.com/`，登录弹窗 `https://passport.weibo.com/sso/signin`
