---
name: "weibo-video-post"
title: "Post a Video to Weibo from a Cloud Container"
description: "已有微博扫码登录态的云端容器上，用保存的会话发一条视频微博：等视频传完再点发送，发布后到个人主页核验链接。"
type: skill
tags: [weibo, playwright, video-post, cloud-container, session]
created: 2026-11-08
updated: 2026-11-08
author: hoover-hash
status: active
---

# Post a Video to Weibo from a Cloud Container

在已经登好微博的云端 Linux 容器/虚拟机上，用保存的浏览器会话发一条视频微博。Playwright + 系统 Chromium；发之前先防重，**等视频真正传完再点发送**，发完到个人主页核验博文链接。

Post one video Weibo from a cloud Linux container/VM that already holds a logged-in session: Playwright + system Chromium, duplicate guard before composing, wait for the upload to actually finish before sending, verify the post on the profile page.

> **本技能不含任何真实账号、Cookie、二维码与机器信息。** 会话文件 `state.json`、日志与结果只留在你自己的机器上，**不要进仓库、不要进群聊、不要进日志分享**。结果 JSON 里含你的个人主页链接，不要贴进公开频道。
> This skill contains no real account, cookie, QR code or machine identity. The session file `state.json`, logs and result JSON stay on your own machine and must never enter a repository, a group chat or a shared log.

<!-- 技能设计至少明确六项：名称、WHEN、WHAT、HOW、REFERENCE、LIMITS。 -->

## 适用场景与触发条件（WHEN）

- **触发场景**：容器里已有微博登录态（见 `weibo-qr-login` 技能，`$WB_LOGIN_DIR/state.json` 存在），手头有一条要发的视频，想发一条视频微博并拿到可核验的博文链接。
- **典型请求**：“用登好的微博发一下这条视频，文案是……，发完把链接给我。”
- **不适用情形**：
  - 还没登录、或 `state.json` 不存在 / 已失效——先跑 `weibo-qr-login` 重新扫码登录，本技能不含登录步骤。
  - 想一次发多条、批量发——本技能一次只发一条，发完必须核验；批量发容易触发风控，也容易重发。
  - 视频不是你自己的内容，或要发到别人的账号——不要用本技能。
  - 容器没有系统 Chromium，或访问不了 `weibo.com`。

## 目标、输入与输出（WHAT）

- **目标**：发一条视频微博，发完能在个人主页上看到它，并拿到博文链接与发布时间；发失败时明确知道失败在哪一步，且不留下重复博文。
- **必需输入**：
  - 一台已装系统 Chromium、能直接访问 `weibo.com` 的 Linux 云容器/虚拟机。
  - Python 3.11+，`pip install playwright`（不需要 `playwright install` 下载浏览器，用系统 Chromium 作 `executable_path`）。
  - 登录态：`$WB_LOGIN_DIR/state.json`（`weibo-qr-login` 产出）。
  - 一条视频文件（实测通过：h264 MP4，720×720，24fps，5 秒，约 0.5MB；更长的视频转码更久，见 LIMITS）。
  - 文案（纯文本；微博发布器接受多行，首行用于防重检查）。
  - 你自己的微博数字 UID。
- **可选输入 / 默认值**：

  | 占位符 / 环境变量 | 含义 | 说明 |
  |---|---|---|
  | `WB_LOGIN_DIR` | 工作目录，默认 `$HOME/weibo-login` | profile、会话、日志全落在这里；**不要指向仓库目录** |
  | `WB_VIDEO` | 要发的视频文件（必填） | 绝对路径；脚本启动时校验文件存在 |
  | `WB_CAPTION` | 文案（必填） | 首行不可与已发博文重复，否则触发防重中止 |
  | `WB_UID` | 你自己的微博数字 UID（必填） | 只用于打开个人主页核验；不要填别人的 |
  | `CHROMIUM_PATH` | 系统 Chromium 路径，默认 `/usr/bin/chromium` | `which chromium` / `which google-chrome` 核实 |
  | `WB_PROXY` | 出站代理（可选） | 容器只能走代理出站时填，如 `http://127.0.0.1:3128`；不填则直连 |
  | `WB_USER_AGENT` | 浏览器 UA（可选） | `Chrome/<major>` 与已装 Chromium 大版本对齐 |
  | `WB_RESULT` | 结果 JSON 路径，默认 `$WB_LOGIN_DIR/post_video_result.json` | 只含 `ok` / `url` / `time_cst` / `reason`，无凭据 |

- **输出形式**：个人主页上的一条新视频博文；`post_video_result.json`（`ok=true` 时含 `url` 与 `time_cst`，`ok=false` 时含 `reason`）；运行日志（只含进度与链接，无 Cookie）。
- **验收标准**：
  - `post_video_result.json` 为 `ok=true`，且 `url` 打开后是刚发的视频博文。
  - 个人主页上文案首行能搜到，博文带视频播放器。
  - 没有重复博文（同一文案只出现一次）。

## 执行流程（HOW）

执行约定（另一个 agent 按本技能执行时，不要跳步）：先核验登录态与防重再动手；**发送按钮可用 ≠ 传完了**，必须等上传真正完成；发完必须到个人主页核验，核验不到就报失败、不盲目重发；全程不碰密码与 Cookie。

1. **收集并检查输入**：核实 `state.json` 存在、视频文件存在、文案与 UID 已给。缺任何一项就停下来，不要猜。

2. **按步骤处理**：脚本在 `references/post_weibo_video.py`，按以下顺序执行（环境变量见上表）：

   ```bash
   export WB_LOGIN_DIR=$HOME/weibo-login
   export WB_VIDEO=/path/to/your-video.mp4
   export WB_CAPTION="你的文案"
   export WB_UID="<YOUR_WEIBO_UID>"
   # 按需：export CHROMIUM_PATH=/usr/bin/google-chrome WB_PROXY=http://127.0.0.1:3128
   python3 references/post_weibo_video.py
   cat $WB_LOGIN_DIR/post_video_result.json
   ```

   ### 2.1 防重检查

   先打开 `https://weibo.com/u/<UID>`，搜文案首行。已出现就中止（`caption already posted`），不要发第二条。

   ### 2.2 打开编辑器、填文案、选视频

   点首页 `新鲜事` 输入框进编辑器，填文案；用同一个文件上传口选视频（发布器的 `input[type=file]` 同时接受图片与视频，`accept` 含 `video/mp4`、`video/*`、`.mkv`、`.flv`）。发布按钮叫 **发送**，不是“发布”。

   ### 2.3 等上传完成（最关键的一步）

   **不要以发送按钮是否可用为准。** 实测：选完文件后发送按钮立刻就可用，但此时视频还没传完；这时点发送，发布会静默失败——不报错、主页上什么都不出现。

   正确做法是同时满足三点再点发送：
   - 视频封面已出现：页面上 `sinaimg` 图片数高于选文件前的基线；
   - 没有 `上传中` 字样；
   - 距选文件至少过去 15 秒（脚本常量 `MIN_UPLOAD_SETTLE_SEC`；实测 5 秒小视频约 10 秒传完，留余量）。

   3 分钟内三点不齐就中止并截图（`post-video-fail.jpg`），不要点发送。

   ### 2.4 点发送并核验

   点发送后视频还要在服务端转码，**不要立刻断言**。脚本会到个人主页轮询最多 6 次（约 2 分钟），文案首行出现即成功，取第一条博文链接写进结果 JSON。6 次都找不到就报失败并截图（`post-video-unverified.jpg`）。

3. **失败处理**：
   - `not logged in`：登录态丢了，先跑 `weibo-qr-login` 重新登录，不要在本技能里加登录逻辑。
   - `video upload did not finish`：网络或转码卡住；先看截图与日志，确认主页上没有这条博文再决定是否重发。
   - `send clicked but video post not found`：最常见原因是 2.3 没等够就点了发送。先到主页人工确认到底有没有这条博文——**没有再重发，有就绝不重发**（重发会产生重复博文）。
   - 任何一次失败都只写 `ok=false` 的结果，不自动重试；重试是调用方的决定，且重试前必须先过 2.1 的防重检查。

## 安全与隐私（Security & Privacy）

- **凭据不出本机**：`state.json`、浏览器 profile、日志、截图、结果 JSON 只留在运行脚本的那台机器上；不要提交进仓库、不要发群聊、不要贴进工单或日志分享。仓库里只放带 `<PLACEHOLDER>` 的技能文档与脚本。
- **脚本不含真实身份**：不要把 UID、主页链接、视频文件名、文案写进技能文件；一律走环境变量。提交前自查：`grep -r` 自己的 UID、域名、IP、token。
- **只发自己的内容**：本技能只用于往你自己的账号发你自己的视频；不要用它发别人的内容、不要代人发帖。
- **防重就是防事故**：每次运行都先查文案首行是否已发；定时任务场景下，每条视频配唯一文案，杜绝重复发布。
- **不要高频调用**：一次运行只发一条；连续发多条、短时间内反复重试容易触发平台风控，失败时先停下来看日志。
- **日志脱敏**：日志只记进度、耗时与博文链接；不要把 Cookie、二维码内容、`state.json` 原文写进任何日志。

## 参考（REFERENCE）

- `references/post_weibo_video.py`：发视频的完整脚本（Playwright 同步 API；先跑 `pip install playwright`，用系统 Chromium 作 `executable_path`）。前置登录见 `weibo-qr-login` 技能（`references/weibo_qr_login.py`）。

## 限制（LIMITS）

- 一次运行只发一条视频博文；不含登录（登录态丢了要先重登）、不含删博、不含评论互动。
- 只验证过短视频（h264 MP4，5 秒，约 0.5MB）；更长 / 更大的视频转码时间更长，`UPLOAD_TIMEOUT_SEC` 与 `VERIFY_ATTEMPTS` 可能需要按实测调大。
- 发布按钮的文案、上传口的 `accept` 列表、封面图域名（`sinaimg`）都来自 2026-11-08 的实测，微博改版后可能变化；先跑一次小流量验证再上定时任务。
- 浏览器优先有头模式（headed），启动失败才回落到 headless；无显示环境的容器需配 `DISPLAY` 或接受 headless。
- 本技能不保证绕过平台风控；账号异常、限流、验证码出现时停下来人工处理，不要反复重试。
