---
name: douyin_abdm_download
description: >
  通过 AB Download Manager 的 Chrome 插件，在 9222 调试浏览器中批量静默下载抖音
  分享链接对应的视频：嗅探媒体 → 静默下载 → 按「序号_作者_标题」规整命名 → 清理
  ABDM 弹窗。已实测 19/19 零失败。
  触发词：抖音下载、下载抖音视频、抖音分享链接、批量下载视频、ABDM、
  复制打开抖音极速版、douyin download。
task_type: daily.douyin_abdm_download
---

# 抖音批量下载（ABDM 插件路线）

## 概述

不解析直链、不装新工具：用本机已有的 AB Download Manager（ABDM）Chrome 插件，在项目 9222 调试浏览器里逐页嗅探媒体并静默下载。已实测 19/19 零失败，单条约 30 秒。

**用户说这些话时的既定套路：**
- 「下载这些抖音视频」→ 直接走本 SKILL 全流程
- 「用后端开浏览器」→ 必须用 `mcp__localagent__exec_python` 跑 `<project_root>\tools\browser\start_debug_browser.py`；**禁止 agent 自己 Start-Process 拉起**（会被回收）
- 「别动我的主浏览器」→ 一切操作限定 9222 调试实例（profile `<project_root>\chrome_debug`，ABDM 插件已装，扩展 ID `bbobopahenonfdgjgaleledndnnfhooj`）
- 「下载目录」→ 看 ABDM 设置（本机 = `<data_drive>:/<system_data_root><data_drive>:/Downloads`），禁止全盘 find 搜索

## 流程（六步）

> 下方 `scripts/` 均指本 skill 目录下的 `.agents/skills/daily/douyin_abdm_download/scripts/`。

### 1. 提取链接
从分享文本提取 `v.douyin.com` 短链到 `<项目temp>/<任务名>_<日期>/links.txt`，每行一条。
推荐格式 `标题【作者】 | URL`（命名用；从「看看【某某的作品】标题...URL」原文即可整理）。

### 2. 就绪检查（三个都要过）
```bash
curl -s -m 5 http://127.0.0.1:8766/health      # 后端在线
curl -s -m 5 http://127.0.0.1:9222/json/version # 调试浏览器在线
tasklist //FO CSV | grep -i abdownload          # ABDM 在跑
```
9222 不在线 → 用 `exec_python` 跑 `start_debug_browser.py`（见上「既定套路」），**不要手拉**。

### 3. 开静默（脚本自动做）
`scripts/batch_download.py` 启动时会自动在扩展 storage 写入 `silentAddDownload`/`silentStartDownload`（UI 点开关对 React 合成事件无效，必须直写 storage，详见 `references/pitfalls.md` §2）。若脚本报静默失败则中止，先排查。

### 4. 批量执行
```bash
python scripts/batch_download.py links.txt --start 1
```
- 脚本自动：单标签页复用（不堆积标签）→ 逐页等横幅 → 点 `.abdm-media-item`（选 mp4 最大条目）→ 等落盘（体积 4 秒无增长）→ 按 `NN_作者_标题.mp4` 改名
- 后台运行（`run_in_background`），全程看 `batch_log.txt`；单条 ~30s，失败会记 `!!` 并继续下一条
- 中途断了直接 `--start N` 续跑

### 5. 清理弹窗（用户明确要求过）
静默模式下每个下载仍会弹一个 675x240 进度小窗（全部叠在同一位置）：
```bash
python scripts/close_abdm_popups.py --dry-run   # 先看清单
python scripts/close_abdm_popups.py             # 再真关
```

### 6. 汇报
给用户：成功/失败条数、落盘目录、文件清单、失败原因（如有）。

## 硬性约束

- ⛔ 不动主浏览器；9222 实例只由后端拉起
- ⛔ 静默没验证成功前不要开批量（会连弹 N 个确认框）
- ⛔ 不提前抓直链存着（douyinvod 直链带签名有时效，走插件实时嗅探）
- 排障细节（插件机制、React 开关坑、登录墙、窗口扁条、CTypes 关窗等）→ `references/pitfalls.md`
