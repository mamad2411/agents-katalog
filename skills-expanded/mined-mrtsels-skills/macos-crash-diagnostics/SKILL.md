---
name: macos-crash-diagnostics
description: Use when a macOS app crashes or won't open at launch.
license: MIT
metadata:
  hermes:
    tags:
    - macos
    - crash
    - ips
    - dyld
    - diagnostics
    - launch
    - beta
    related_skills:
    - systematic-debugging
    - macos-network-diagnostics
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
  imported_from: hermes
---

# macOS Crash & Launch Diagnostics

Diagnose "app 打不开 / 点开就退出 / 升级系统后不能用" on macOS from crash reports and system state. Everything is read-only until the fix plan is confirmed with the user.

## When to Use

- 用户报某 app 打不开、闪退、启动转圈后消失
- 系统升级后 app 突然不能用
- 需要判断问题在 app 侧还是 OS 侧

## Triage batch (one terminal call, all read-only)

1. `pgrep -fl -i "<app>"` — 主进程卡死？只剩 helper（如缩略图扩展）= 没卡死
2. 崩溃报告：`ls -t ~/Library/Logs/DiagnosticReports/ | grep -i <app> | head` — 同一秒多份 = 启动循环崩溃
3. `df -h /` — 剩余 <10GB 影响更新，但通常不是崩溃直接原因
4. 应用身份：`/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' -c 'Print :CFBundleShortVersionString' <app>/Contents/Info.plist`；安装日期 `stat -f '%Sm' <app>`；`Contents/_MASReceipt/` 存在 = App Store 版
5. 时间线：`system_profiler SPInstallHistoryDataType` — 系统/app 各自何时变过
6. `softwareupdate --list` — 有无待装更新（顺带 beta 检测，见下）

## Parse the .ips report

格式：**一行 JSON header + 换行 + JSON body**（在第一个 `\n` 处拆分）：

```python
raw = open(path, encoding='utf-8', errors='replace').read()
i = raw.find('\n'); hdr = json.loads(raw[:i]); body = json.loads(raw[i+1:])
print(hdr.get('app_version'), hdr.get('os_version'), hdr.get('timestamp'))
print(body['termination'], body['exception'])
th = body['threads'][body['faultingThread']]   # frames；符号名在 body['usedImages'][idx]
```

## Key: read `termination` before theorizing

- `namespace: DYLD` + `indicator: 'Symbol missing'` + details `'(terminated at launch; ignore backtrace)'`
  → app 链接了当前系统不再提供的符号。**不是损坏、不是权限、不是卡死**；backtrace 只是 dyld abort，除 dyld 帧外不要分析。
- 其它 namespace：先逐字读 `reasons`/`details` 数组再下结论，不要凭 namespace 猜。
- 同一符号缺失可能只出现在一个 app 的报告里（系统没坏到影响别人），这不矛盾。

## PITFALL: system dylib 在磁盘上不存在（共享缓存）— 会得出反向错误结论

现代 macOS 把系统框架二进制放进 dyld shared cache，**磁盘路径常常没有文件**：

- `nm` / `grep -a` / `strings` / `file` 打在 `/System/Library/Frameworks/.../Foo` 上会 ENOENT 或输出为空 —
  **空输出 ≠ "符号被移除"**。曾因 `nm | grep -c` 得 0 误判整套 API 被删。
- 下结论前先验证工具本身成功了：看 nm 的 stderr 原文、`dyld_info -exports | wc -l` 有没有数据行。
- **运行时 dyld 报错（.ips 里的 termination）才是 ground truth**；磁盘探测只是辅助。
- app 自带 framework（/Applications 下）不受此影响，`otool -L` 正常可用。
- SDK 头文件（`xcrun --show-sdk-path`）可作旁证，但 CLT SDK 布局可能精简，缺文件不代表 API 被移除。

## Beta OS detection

- build 号带尾字母（`26B5086k`）= 预发布 seed；正式版无尾字母
- `softwareupdate --list` 直接打印 seed 名（如 `macOS 27.2 Beta 2-26B5091g`）
- 用 install history 日期 × app 最后可用时间，锁定"哪次系统变更杀掉了它"

## Fix routing

| 证据 | 第一步 |
|---|---|
| 系统刚升级 + app 很旧 + 符号缺失 | 先更新 app（`_MASReceipt` 在 → `open "macappstore://showUpdatesPage"`），无需重启 |
| beta 系统 + app 已是最新仍缺符号 | 装下一个 beta seed（需重启）或等修复——兼容性可能只存在于配对的 build |
| 磁盘将满 / 主进程真卡死 / 收据损坏 | 对应的便宜修复——但仅当证据指向它再动手 |

## Workflow preference (this user)

诊断输出 = 结论 + 证据表；动手修复前列**编号选项（纯文本）**，逐条确认后再执行。

## Worked example

Logic Pro 11.2 在 macOS 27.2 beta 上 DYLD 符号缺失 → `references/dyld-symbol-missing-case.md`.
