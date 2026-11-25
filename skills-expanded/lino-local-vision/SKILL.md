---
name: lino-local-vision
description: 调用本机 LM Studio 的 Qwen3.5-9B 视觉模型本地看图/OCR，纯本地免费无需 API key（lms server start 启动，localhost:1234 OpenAI 兼容接口）
---

# Local Vision（LM Studio 本地视觉模型）

调用本机 LM Studio 的本地多模态模型分析图片，纯本地、不走网络、不需要 API key、无费用。默认模型 `qwen3-vl-8b-instruct`（官方指令版，无思维链、直接输出，识别更准）；备选 `qwen3.5-9b-uncensored-hauhaucs-aggressive`（第三方社区模型，带思维链需压 reasoning，可在 LM Studio 的 Model 搜索里找到，或从 ModelScope / HuggingFace 的 lmstudio-community 组织下载）。

## 适用场景

用户想"看图/OCR/描述图片"，且希望本地推理（隐私、离线、免费）时使用。若模型未加载或服务未开，先按下方启动步骤操作。

## 前提检查与启动（按需）

1. 检查服务是否在运行（端口 1234）：
   ```powershell
   Test-NetConnection 127.0.0.1 -Port 1234 -WarningAction SilentlyContinue -InformationLevel Quiet
   ```
2. 未运行则启动并加载模型（LM Studio 的 lms CLI 默认在 `$env:USERPROFILE\.lmstudio\bin\lms.exe`，路径因安装方式而异，也可直接用 LM Studio 图形界面启动服务）：
   ```powershell
   & "$env:USERPROFILE\.lmstudio\bin\lms.exe" server start
   # 模型通常会自动加载；未加载时用：
   & "$env:USERPROFILE\.lmstudio\bin\lms.exe" load qwen3.5-9b-uncensored-hauhaucs-aggressive
   & "$env:USERPROFILE\.lmstudio\bin\lms.exe" status   # 确认 Server: ON + 已加载模型
   ```
   模型 id：`qwen3-vl-8b-instruct`（官方 Qwen3-VL-8B，含 mmproj-Qwen3-VL-8B-Instruct-F16.gguf 投影）或 `qwen3.5-9b-uncensored-hauhaucs-aggressive`（含 mmproj-Qwen3.5-9B-Uncensored-HauhauCS-Aggressive-BF16.gguf 投影）。
   **注意**：mmproj 投影文件一旦丢失，模型会退化为纯文本（报 "does not support image inputs"），需重新下载并 `lms unload --all` 后重载。
   注意：LM Studio 设置里 `enableLocalService` 必须为 true（或用 lms server start 启动）。

## 调用

```powershell
$env:PYTHONIOENCODING='utf-8'
python "<skill目录>\scripts\analyze.py" --image "图片路径.png" --prompt "用一句话描述这张图片的内容"
```

- `--image`：本地图片路径（自动缩放至宽 ≤ 256px、JPEG 压缩后 base64 传入，规避大图 token 膨胀）
- `--prompt`：对图片的问题/指令（默认 "用一句话描述这张图片的内容"）
- `--max-tokens`：默认 2048。该模型是 reasoning 模型，思维链会先消耗 token；脚本默认带 `--reasoning-effort minimal` 压缩思维链，一般不会卡住。若仍出现"只有 thinking、正式回答为空"，调大 `--max-tokens` 或加 `--reasoning-effort none`。
- `--reasoning-effort`：`minimal`（默认）| `low` | `medium` | `high` | `none`（none 时改用 enable_thinking=false 参数关思维链）。
- `--model`：默认 `qwen3-vl-8b-instruct`；换旧社区版用 `--model qwen3.5-9b-uncensored-hauhaucs-aggressive`。

## 输出

stdout 打印 JSON：`model` / `reply`（正式回答）/ `reasoning`（思维链，可忽略）/ `usage`。模型返回空 content 且 usage 里 reasoning_tokens 占满时，调大 `--max-tokens` 重试。

## 与云端视觉方案的取舍

- 需要精细、复杂视觉理解、能接受图片数据上云 → 用云端多模态 API（如通义千问 qwen-vl 系列、OpenAI 等），模型更强、延迟低
- 隐私/离线/免费/无 key → 本 skill（本地 9B，速度取决于本机 GPU/CPU，思维链较啰嗦）

## 注意

- 模型未加载时 LM Studio 会报错，先 `lms load <模型id>` 再调用。
- **LM Studio 下大模型慢的提速法**：`python scripts/chunk_download.py <URL> <输出路径>`（分段并发下载，绕过长连接限速，实测 4.68GB 95 秒）。源优先用 ModelScope（modelscope.cn/lmstudio-community/...）国内直连快；LM Studio 的 HF_ENDPOINT 环境变量对已运行进程不生效。
- 只读操作，不保存图片，不修改任何文件。
