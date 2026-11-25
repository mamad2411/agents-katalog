---
name: app-ui-record-zh
description: 子 Skill：adb getevent 监控真机点击/滑动/输入，写入 runs/app/manual-<runId>/。启停录制。触发词：开始录制、停止录制、监控手机、record_app_manual、真机录步骤。
disable-model-invocation: true
---

# App 真机步骤录制

由 **app-ui-record-orchestrator-zh** 调用；只录制，不执行用例。

## 环境

- `ADB` 指向 `adb.exe`（可在 `config/local.env` 设置）
- 手机 USB 调试已连接：`adb devices`
- 可选：`--package com.android.settings`（Demo 默认系统设置）

## 启动录制

**手势模式（默认，推荐）** — `adb getevent` 捕获真实点击/滑动/长按，并映射到控件；输入框文字变化记「输入」步。Ctrl+C 结束：

```bash
python scripts/tools/record_app_manual.py --name "demo-settings-wifi" --package com.android.settings
```

**手动确认模式** — 手机上操作后回终端按 Enter 记一步，`q` 结束：

```bash
python scripts/tools/record_app_manual.py --manual-enter --name "demo-settings-wifi"
```

## 产物目录

`runs/app/manual-<runId>-<slug>/`

| 文件 | 含义 |
|------|------|
| `steps.jsonl` | 每步：**操作类型**、坐标、定位、控件、截图 |
| `screens/NN-screen.png` | 逐步截图 |
| `meta.json` | runId、录制模式、touchDevice |
| `操作步骤.md` | 人工可读（finalize 后生成） |

## 停止

- 手势模式：**Ctrl+C**
- 手动确认：终端输入 `q`

## 注意

- 依赖 `getevent` 读触摸屏 `/dev/input/eventN`
- 中文输入靠检测焦点 `EditText` 文本变化；漏记可用 `--manual-enter` 补步
- `steps.jsonl` 为 UTF-8

## 下一步

录制结束后由编排调用 **app-ui-spec-from-record-zh** → `--finalize <录制目录>`。
