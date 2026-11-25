---
name: build
description: 编译当前 SDK 仓库的固件。用 trae-builder 读取 builder.json，按预设或参数执行构建脚本并收集产物。当用户要求"编译/构建/烧录固件""build firmware""用某个预设编译"时自动调用。
---

# build skill

本 skill 指导你使用 trae-builder 插件编译当前 SDK 仓库的固件。

## 前提

当前工作区 `${workspaceFolder}` 根目录需存在 `builder.json` 或 `robin_builder.json`。若不存在，先建议用户运行 `/build-init` 生成。

## 核心入口

构建运行器位于 `${COCO_PLUGIN_ROOT}/trae_build_runner.py`，用 Python 调用。**不要自己拼编译命令**，一律通过 runner。

## 子命令

### info — 查看配置
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" info
```
返回 JSON：sdk 信息、parameters、presets、artifacts 配置、toolchain、script。

### list — 列出产物
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" list
```
返回 artifacts 数组（path、size、mtime），按修改时间倒序。

### build — 执行编译
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" build --preset <预设名> [--param 键=值 ...] [--timeout 秒] [--dry-run]
```
- `--preset`：用 builder.json 中定义的预设名（如 `rx_default`、`b80_release`）。
- `--param 键=值`：覆盖单个参数，可多次。键须匹配 builder.json 的 parameters。
- `--timeout`：覆盖超时秒数。
- `--dry-run`：只打印将要执行的命令，不真正编译。

返回 JSON 含：status（success/failed/timeout/dry-run/error）、exit_code、elapsed_seconds、artifacts、command。

## 判断用户意图

用户说"编译/构建/build"且当前仓库有 builder.json 时，主动用 build 子命令：
- 用户给了预设名（如"用 rx_default 编译"）→ `build --preset rx_default`
- 用户给了参数（如"Target 设成 tx"）→ `build --param Target=tx`（可叠加预设）
- 用户只想看配置/产物 → 用 info / list
- 用户不确定有哪些预设 → 先跑 info 列出 presets，让用户选

## 汇报规范

- 成功：status、产物路径+大小、耗时
- dry-run：展示完整命令，提醒去掉 --dry-run 即可真编译
- 失败：exit_code、日志路径（robin_build_variant.log 或 eclipse_headless_build.log）
- 超时：提示增大 --timeout

## 多芯片仓库

部分 Telink 仓库有多个 Eclipse 工程（B80/B80B/TC1211 等），builder.json 会为每个工程生成一个预设。用户说"编译 B80 固件"时，选匹配芯片名的预设。

## 烧录与调试（完整闭环）

除编译外，runner 还支持烧录（bdt.exe）和串口抓取，构成"编译→烧录→看串口"闭环。用户说"烧录/flash/下载固件""复位""查看 PC""抓串口"时用对应子命令。

### flash — 烧录/读写/调试（调用 Telink bdt.exe）
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" flash --chip <芯片> --command <命令> [选项]
```
- `--chip`：bdt 芯片名（如 TL721X、B80、TC321X；空=builder.json flash.default_chip 或从预设推断）
- `--command`：bdt 命令：
  - `wf` 烧录 flash（不指定 --input 时自动取 build_variants 最新 .bin）
  - `rf` 读 flash 到文件（配合 --output --size）
  - `wc`/`rc` 读写 core（含 sram 和数字寄存器）
  - `wa`/`ra` 读写 analog 寄存器
  - `wo`/`ro` 读写 OTP
  - `lf` 锁 flash
  - `rst` 复位（`--command rst` 后加 -f/-c 用 extra_flags，或直接 rst 默认 -f）
  - `pc` 查看 PC/反汇编（`--input file.lst` 传 .lst 对照）
  - `ac` 分析芯片（仅 evk 模式）
  - `sws` set sws（仅 evk 模式）
- `--input`：-i 输入文件（wf 的 .bin，pc 的 .lst）
- `--output`：-o 输出文件（rf/rc/ro）
- `--size`：-s 大小（如 512k、12k）
- `--erase`：-e 写前擦除
- `--device-id`：BDT 设备 id，数字（1,2）或 SN 十六进制串（如 61174f1a603）；空=配置默认(1)
- `--verify`：wf 后读回前 64 字节与文件对比，确认烧录正确
- `--retry N`：wf 失败时重试 N 次，每次先跑恢复序列（ac→rst→ac→lf）再重试
- `--pre-check`：wf 前先 ac 探测芯片连接（仅 EVK 模式），避免无效烧录
- `--dry-run`：只打印 bdt 命令

**BDT 后端兼容**：runner 自动探测 bdt.exe（libusbBDT）和 Cmd_download_tool.exe（BDT_Beta/release_v5.9.3），并设置正确的 cwd（Cmd_download_tool.exe 必须在其自身目录运行）。

**输出解析**：失败时 runner 返回 `error_reason` 字段（如 "chip not found / not connected"、"address out of range"），便于诊断。

烧录成功后默认自动 `rst -f` 复位（builder.json flash.reset_after_flash，默认 true）。

### serial — 抓串口验证
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" serial list
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" serial capture --port COM3 --baud 115200 --duration 5
```

### 完整闭环
用户说"编译并烧录看效果"时，依次：build → flash(wf) → serial capture，把串口日志给用户判断固件行为（如有没有 boot ok / 版本号）。

### bin — 固件检查
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" bin inspect
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" bin inspect --path build_variants/firmware.bin
```
检查编译产物的头信息（startup_flag、fw_version、bin_size、ram_code_size），CRC 校验。

### device — 设备探测
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" device probe
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" device probe --port COM3 --baud 1152000
```
通过串口识别连接的设备类型、固件版本和设备 ID。

### log — 日志分析
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" log analyze
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" log analyze --file _ota_car.log --patterns boot,error,ota
```
从串口日志中提取启动、配对、错误、OTA 进度等关键事件。

### boot — 启动监控
```
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" boot monitor
python "${COCO_PLUGIN_ROOT}/trae_build_runner.py" --project "${workspaceFolder}" boot monitor --port COM3 --duration 10
```
通过 BDT 复位设备并捕获完整启动序列，自动分析启动阶段和错误。

## 注意

- `${COCO_PLUGIN_ROOT}` 是插件安装目录，runner 在其中。
- `${workspaceFolder}` 是当前打开的工作区根。
- runner 输出是 JSON，解析后向用户汇报，不要原样堆 JSON。
- 编译可能耗时较长（Telink IDE headless 几十秒到几分钟），用 Bash 工具执行时确保超时充足（builder.json 的 timeout_seconds，默认 900-1200）。
