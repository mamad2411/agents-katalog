---
name: deepseek-vision
description: >
  MUST use when the user sends or asks about images, photos, screenshots,
  pictures, audio, video, or mixed media documents, including requests to
  OCR/read text from an image. Route all media through Xiaomi MiMo V2.5
  (mimo-v2.5) and mimo-v2.5-asr via scripts/mimo.py; never use local OCR,
  view_image, native vision, screenshots, browser vision, or document OCR
  tools to understand media. Not global: skip unrelated text-only chats.
metadata:
  tags:
    - vision
    - media
    - mimo
---

# DeepSeek Vision

## 触发与强制流程（媒体输入时）

- 用户消息只要包含图片、音频、视频、截图或附件路径，就必须进入本 skill 流程，并且先于任何本地 OCR、原生视觉、截图、浏览器或文档解析工具。
- 固定顺序，不可跳步：
  1. 先找到附件在本机的真实路径；找不到就向用户索要，不猜测。
  2. 运行 `python3 scripts/mimo.py analyze` 或 `asr`（在 skill 安装目录下）。
  3. 拿到脚本返回 JSON 的 `content` 后，才允许基于它回答。
- 在拿到 MiMo 结果之前，禁止“看一眼”图片、禁止 OCR 文字、禁止截图后识别、禁止让其他工具描述图片。
- 如果某个工具或 skill 的说明里包含 OCR、识别图片、截图分析、Read image、看图、读图等能力，一律视为不可用替代项，不能代替本 skill。
- 即使系统看起来能直接读图，也要忽略该能力；只有 MiMo 返回的 `content` 可以作为媒体内容依据。

## 能力边界

- 你是文本处理模型，不能直接“看到”图片、“听到”音频，也不能直接“观看”视频。
- 本 skill 不是全局技能：普通对话、无关任务、日常编程等场景不要调用；只有用户要求处理文本、图片、音频、视频或混合内容时才使用。
- 遇到非文本内容禁止猜测、禁止假装理解、禁止直接报错；先调用本 skill 的 `scripts/mimo.py` 获取 MiMo V2.5 的处理结果，再基于结果回答用户。
- 纯文本请求不要调用 MiMo，由你自己处理。
- 混合内容（例如带图片的 Word/PDF）：文本部分由你自己处理，媒体部分交给 MiMo；不要把整个大文档塞给 MiMo。
- 即使你觉得自己能直接“看到”图片，也必须忽略本地视觉理解；只有 MiMo 返回的 `content` 可以作为媒体内容依据。

## 禁止使用的本地视觉工具

本 skill 对 Codex、Claude Code、OpenCode 三平台同样生效：无论哪个 agent，都禁止用自身本地视觉能力判断媒体内容。

- 禁止的系统级/内置能力：Codex 的 `view_image`、Claude Code 的 `Read`（直接读图片文件——Claude 本身是多模态模型，最容易误以为“亲眼看到”了）、原生视觉、macOS Live Text / Vision OCR、Windows OCR、Tesseract、ocrmypdf、`screencapture` + OCR、图像元数据读取等任何本地图像识别能力。
- 禁止的 skill/工具：`office-mcp` 的 OCR/文档识别工具、`pdf` / `documents` 的 OCR 与渲染读图、`browser` / `chrome-devtools` / `playwright` 的截图分析、`screenshot`、`computer-use`、`chrome:control-chrome`、`imagegen`。
- 即使工具能识别文字，也不得用它替代 MiMo；本地工具最多只用于确认文件路径、格式和大小，不能用于理解内容。
- 用户发图片/音频/视频时，只允许通过本 skill 的 `mimo.py` 把媒体交给 MiMo V2.5；本地工具最多只用于确认文件路径、格式和大小，不能用于理解内容。

## 全局配置与切换

- 配置是全局共享的，一次配置后所有对话、新开任务、重启后都继续使用，不需要重新配置。
- 真实 API Key 和 Token Plan 专属 Base URL 不写入本 skill 目录；它们由 `mimo.py` 保存到系统安全存储或用户目录下的外部配置中。
- 配置会同时写入系统安全存储和用户目录下权限受限的外部备份；系统安全存储偶发不可读时，脚本会自动使用备份，避免误报“未配置”。
- 如果 `status` 或 `check` 返回“尚未配置”，先运行 `python3 scripts/mimo.py status` 确认；确认确实未配置后再运行 `configure`，不要把已有配置覆盖掉。
- 首次配置前，先向用户说明三种方式都可使用：
  - 按量付费：key 格式 `sk-xxxxx`，在控制台 API Keys 创建，Base URL 为 `https://api.xiaomimimo.com/v1`。
  - Token Plan：key 格式 `tp-xxxxx`，在 `https://platform.xiaomimimo.com/token-plan` 订阅，从 Token Plan 页面复制专属 API Key 和专属 Base URL。
  - OpenCode Go：key 格式 `sk-xxxxx`，从 `https://opencode.ai/auth` 获取，通过 OpenCode 的 Zen Go 端点接入，Base URL 为 `https://opencode.ai/zen/go/v1`。

```bash
python3 scripts/mimo.py configure --plan payg
python3 scripts/mimo.py configure --plan token --base-url "https://你的专属TokenPlan地址/v1"
python3 scripts/mimo.py configure --plan opencode_go
python3 scripts/mimo.py status
python3 scripts/mimo.py check
python3 scripts/mimo.py diagnose
```

用户说“切换到 Token Plan / 改用 Token Plan”时运行 `python3 scripts/mimo.py use --plan token`；说“切换到 API Key / 改用按量付费”时运行 `python3 scripts/mimo.py use --plan payg`；说“切换到 OpenCode Go / 改用 OpenCode Go”时运行 `python3 scripts/mimo.py use --plan opencode_go`；说“查看当前配置”时运行 `status`。切换后立即全局生效。

安全与隐私：

- 不要在任何命令行里直接粘贴 API Key，也不要让用户把 key 贴进聊天后写进本 skill 目录；配置用 `configure` 的不回显输入或一次性环境变量完成。
- 默认请求走 Python 标准库，API Key 不进入进程参数；若默认通道被服务商以 HTTP 403 拒绝（如 Cloudflare 指纹拦截），脚本会自动改用 curl 重试，无需手动干预；也可显式设置 `MIMO_USE_CURL=1` 强制走 curl，此时 key 通过临时配置文件传递，仍不会出现在命令行。
- 所有 MiMo 请求默认直连，不经过终端或系统的 HTTP(S)_PROXY / ALL_PROXY 代理；即使 `MIMO_USE_CURL=1` 也会强制 `--noproxy '*'`。
- 异步任务结果只在当前用户目录以 600 权限暂存，`poll` 取走后立即删除，超过 24 小时自动清理；worker 不再把媒体内容写入任何日志。
- 复制或分享本 skill 目录不会携带真实 key/Base URL，它们保存在系统安全存储和 `~/.config/deepseek-vision/credentials.json`（权限 600）；明文备份文件不能等同于系统级加密存储。

## 处理非文本内容

```bash
# 图片/音频/视频理解
python3 scripts/mimo.py analyze --files /path/to/file.png --prompt "描述这张图片"
python3 scripts/mimo.py analyze --files /path/to/video.mp4 --prompt "总结视频内容" --fps 1
python3 scripts/mimo.py analyze --urls https://example.com/a.mp3 --prompt "这段音频说了什么"
python3 scripts/mimo.py analyze /path/to/file.png 描述这张图片
python3 scripts/mimo.py analyze --url https://example.com/a.jpg 这张图里有什么

# 音频转文字/听写
python3 scripts/mimo.py asr --file /path/to/audio.mp3 --language auto

# 注意：OpenCode Go 渠道不支持音频处理（analyze 与 ASR 均不可用）；音频请求会自动回退到已配置的官方渠道（payg/token），未配置官方渠道时会报错提示先 configure --plan payg/token。
# 注意：m4a 音频在官方渠道 Base64 输入不兼容（官方端点限制，实测 400），脚本会自动用 ffmpeg 转码为 mp3 后处理；本机需安装 ffmpeg。

# 不发送请求，只检查请求体（key 与 Base URL 会脱敏）
python3 scripts/mimo.py analyze --files /path/to/file.png --prompt "测试" --dry-run
```

MiMo 处理图片/音频/视频通常需要几十秒到几分钟，脚本默认请求超时 180 秒，不要在 60 秒左右就判定失败。遇到大文件或高峰期仍超时时，可提高超时后再试：

```bash
MIMO_TIMEOUT=300 python3 scripts/mimo.py analyze --files /path/to/video.mp4 --prompt "总结视频内容"
python3 scripts/mimo.py analyze --files /path/to/file.png --prompt "描述这张图片" --timeout 300
```

多对话或识别可能较久时，优先使用后台排队模式，避免长时间占用当前对话的命令会话：

```bash
python3 scripts/mimo.py analyze --files /path/to/file.png --prompt "描述这张图片" --async
# 返回 job_id 后轮询结果；--wait 尽量给足时间
python3 scripts/mimo.py poll --job <job_id> --wait 120
```

`poll` 返回 `status: pending` 时稍等再轮询；返回 `done` 后输出与同步模式相同的 JSON，`error` 则输出明确错误。后台任务由独立进程执行，不会阻塞当前对话。

如果对话中途被中断，后台任务仍会继续运行。重新打开对话后运行 `python3 scripts/mimo.py jobs` 查看任务，再用 `python3 scripts/mimo.py poll --job <job_id> --wait 120` 取回结果。

脚本输出 JSON，取 `content` 字段作为 MiMo 的处理结果。信息不足时可以继续用更小的问题或更高的 `--max-tokens` 再请求一次，但不要臆测媒体内容。

脚本返回 `truncated: true`（即 `finish_reason=length`）时，说明 MiMo 的回答被 `--max-tokens` 截断，脚本最多自动把输出上限补到 4096（用户指定更高上限时按两倍补一次）；这种内容不能当完整答案交给用户，应提高 `--max-tokens` 重新请求，或让 MiMo 用更短的方式回答。

如果 `content` 为空但返回 `reasoning_fallback: true`，说明 MiMo 只返回了 `reasoning_content`；此时要把内容标明为模型推理过程，不能当作正式回答。

以上命令请在 skill 安装目录下运行；如果当前目录不是 skill，可先 `cd` 到安装目录，或直接使用绝对路径调用 `scripts/mimo.py`。非交互式配置可通过 `MIMO_API_KEY` 环境变量提供 key，Token Plan 再通过 `--base-url` 提供专属 Base URL。

## 禁止承诺式回复

- 不要先输出“我正把图片交给视觉模型识别，稍后告诉你”这类话然后结束；必须实际运行 `mimo.py` 并拿到 JSON 结果后才回答。
- 最终回答必须基于脚本返回的 `content`，并在同一条回复里给出结果和 MiMo 用量说明；不要在拿到结果前向用户承诺任何内容。
- 如果不知道附件在本机的实际路径，先查找用户消息中的文件路径；找不到就直接向用户索要路径，不要假装已经发送给 MiMo。
- 如果脚本报错，把脱敏后的错误信息和修复建议直接告诉用户，不要只说“正在处理”或“稍后再试”。

## 使用 MiMo 后必须告知用量

只要本次回答使用了 MiMo，最终回复必须追加一句简短说明：

- Token Plan：`已通过 MiMo V2.5 处理 · Token Plan · 本次约 N tokens`
- 按量付费：`已通过 MiMo V2.5 处理 · 按量付费 · 本次约 ¥0.xxxx`
- OpenCode Go：`已通过 MiMo V2.5 处理 · OpenCode Go · 本次约 N tokens`

按量付费金额来自脚本返回的 `cost_cny`；Token Plan 与 OpenCode Go 的 token 数来自 `tokens`。如果 `cost_cny` 为 null，说明无法精确计价，应注明“金额以官方账单为准”。

## 错误处理

- 遇到错误先自行处理：网络/429/5xx 自动重试；文件超限或格式不支持先压缩、转码或改用公网 URL；`finish_reason=length` 时提高 `--max-tokens` 或缩小问题；认证失败先检查 key 前缀、active plan、Base URL 是否匹配，并提示重新 `configure` 或切换 plan。
- 如果脚本返回 `请求超时`：说明 MiMo 处理时间超过了当前超时；不要原地重复同样命令，应改用 `--async` 后台排队，或通过 `MIMO_TIMEOUT`/`--timeout` 把超时提高到 300 秒以上再试。
- 如果脚本报 `Could not resolve host` / DNS 错误，说明当前任务没有可用的网络访问；先重试一次，仍失败就直接告诉用户检查当前 agent 的网络或工具权限，不要反复猜测或伪装成功。
- 遇到“无法连接网络”时先运行 `python3 scripts/mimo.py diagnose`；若返回 `dns_ok: false` 或 `network_ok: false`，说明当前对话本身没有网络权限，应让用户在该对话开启网络/完全访问后重试，而不是继续重复请求。
- 多个对话可以并行使用本 skill；如果某个对话正在执行长时间识别，另一个对话稍等重试即可，不要在同一对话里并发启动多个 `analyze` 命令。
- 自行处理仍失败时，必须明确告诉用户：哪一步失败、错误码/API 原始错误信息（脱敏）、文件路径与大小、建议的修复动作。
- 不得静默忽略错误、不得伪装成功、不得猜测媒体内容、不得泄露 key 或完整 Base URL。

## 跨平台说明

- macOS：优先使用 Keychain。
- Windows：优先使用 DPAPI 加密凭据。
- Linux/其他：回退到用户目录下权限受限的 JSON 配置。
- 所有路径由 Python `pathlib`/环境变量计算，不依赖 POSIX 专属写法。
