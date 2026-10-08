---
name: myagents-speech-recognition
description: >-
  当用户要把当前 MyAgents Workspace 内的单个本地音频或视频附件转成带时间戳的文字稿，或要查询、等待、取消、列出自己当前 Session 发起的语音识别任务时使用。通过内置 `myagents speech` CLI 调用 App 持有的离线异步任务；不用于录制会议、读取 Record、在线 ASR、批量目录、URL、说话人区分或 AI 纪要。
metadata:
  author: MyAgents
---

# myagents-speech-recognition — 本地附件转写

这是 MyAgents 随 App 发布的离线附件转写能力。任务由 Desktop App 持有，并自动绑定发起调用的真实 Session 与 authoritative Workspace；不要传、猜测或请求用户提供 Session ID / Workspace 参数。

## 使用顺序

1. 先运行 `myagents speech --help` 选择命令。
2. 调用前读取 exact leaf help，例如 `myagents speech transcribe --help`；参数、格式与错误恢复以当前安装版本为准。
3. 需要机器读取结果时加 `--json`。这个命令组不支持 `--dry-run`。

## 核心命令

```bash
myagents speech transcribe --file <input> [--output <directory>] [--wait] [--json]
myagents speech status <job-id> [--json]
myagents speech wait <job-id> [--json]
myagents speech cancel <job-id> [--json]
myagents speech list [--limit <1..100>] [--json]
```

`transcribe` 每次必须且只能接收一个当前 Workspace 内的本地普通文件。`--output` 是 Workspace 内的输出根目录；省略时使用 `myagents_files/speech-transcriptions/`。命令不创建 Record、不运行说话人区分，也不生成纪要或待办。

任务默认提交后立即返回 job ID。只有当前工作必须拿到文字稿时才用 `--wait` 或独立 `wait`。Ctrl-C 只停止等待，不取消 App 持有的 job；需要停止任务时显式调用 `cancel`。

成功后只发布：

```text
<output-root>/<job-id>/transcript.md
<output-root>/<job-id>/transcript.json
```

使用响应中的实际 artifact 路径，不猜目录。`list/status/wait/cancel` 只能看到当前 Session 自己发起的任务；其它 Session 的精确 job ID 也会表现为不存在。

## 输入与安全边界

- 支持范围由文件内容的 container + codec probe 决定，不依赖扩展名：WAV/PCM/ADPCM、AIFF/PCM、MP3、FLAC、OGG/Vorbis、M4A/AAC-LC/ALAC、MP4/AAC-LC/ALAC/MP3、MOV/PCM/AAC-LC/MP3。
- 只传一个本地普通文件；不传 URL、目录、stdin、glob、特殊设备或 Workspace 外路径。
- 单文件最大 4 GiB，可探测时长最大 8 小时；处理使用本地模型，不上传媒体。
- 不从 RecordStore 猜文件、不把 `recordId` 当输入，也不为用户附件自动创建 Record。
- 失败时保留 structured `code` 和 `suggestion`，按 leaf help 恢复；partial 目录不是成功产物。

常用流程：

```bash
myagents speech transcribe --file ./meeting.m4a --json
myagents speech status <job-id> --json
myagents speech list --limit 20 --json
```

任何不确定项都回到 exact help：`myagents speech <command> --help`。
