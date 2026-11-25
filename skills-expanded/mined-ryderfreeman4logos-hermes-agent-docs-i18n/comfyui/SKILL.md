---
name: comfyui
description: "Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycle and direct REST/WebSocket API for execution."
version: 5.1.0
author: [kshitijk4poor, alt-glitch, purzbeats]
license: MIT
platforms: [macos, linux, windows]
compatibility: "Requires ComfyUI (local, Comfy Desktop, or Comfy Cloud) and comfy-cli (auto-installed via pipx/uvx by the setup script)."
prerequisites:
  commands: ["python3"]
setup:
  help: "Run scripts/hardware_check.py FIRST to decide local vs Comfy Cloud; then scripts/comfyui_setup.sh auto-installs locally (or use Cloud API key for platform.comfy.org)."
metadata:
  hermes:
    tags:
      - comfyui
      - image-generation
      - stable-diffusion
      - flux
      - sd3
      - wan-video
      - hunyuan-video
      - creative
      - generative-ai
      - video-generation
    related_skills: [stable-diffusion-image-generation, image_gen]
    category: creative
---

# ComfyUI

通过官方的 `comfy-cli` 工具进行配置与生命周期管理，并借助直接的 REST/WebSocket API 执行工作流，从而利用 ComfyUI 生成图像、视频、音频及 3D 内容。

## 本技能包含哪些内容

**参考文档（`references/`）：**

- `official-cli.md` —— 涵盖所有带参数选项的 `comfy ...` 命令说明
- `rest-api.md` —— REST + WebSocket 接口信息（本地及云端），以及请求数据格式规范
- `workflow-format.md` —— API 格式的 JSON 结构、常见节点类型及参数映射规则
- `template-integrity.md` —— 将编辑器格式的 `comfyui-workflow-templates` 转换为 API 格式：处理路径重定向、带点的动态输入键（如 `values.a`、`resize_type.width`）、云端使用限制（302 重定向、免费套餐仅支持同时运行 1 个任务、1080p 分辨率对应的显存上限），以及兼容 Discord 的 ffmpeg 合成功能。该文档由 [@purzbeats](https://github.com/purzbeats) 撰写。每当从官方模板开始使用时，建议先阅读此文档。

**脚本（`scripts/`）：**

| 脚本名称 | 功能说明 |
|--------|---------|
| `_common.py` | 公共的 HTTP 处理功能、云端路由逻辑以及节点目录管理功能（不可直接运行） |
| `hardware_check.py` | 检测 GPU/显存/磁盘性能，帮助判断是使用本地设备还是 Comfy Cloud 更为合适 |
| `comfyui_setup.sh` | 执行硬件检测、安装 comfy-cli 和 ComfyUI，随后启动应用并验证运行状态 |
| `extract_schema.py` | 读取工作流文件，列出所有可配置参数及所需的模型依赖项 |
| `check_deps.py` | 对比工作流与正在运行的服务器，列出缺失的节点或模型 |
| `auto_fix_deps.py` | 先执行 check_deps 的检测，再自动运行 `comfy node install` 和 `comfy model download` 命令安装缺失组件 |
| `run_workflow.py` | 注入参数、提交工作流、实时监控处理进度，并通过 HTTP 或 WebSocket 下载生成结果 |
| `run_batch.py` | 支持对同一工作流进行多次迭代运行，可根据用户套餐支持的最大并行度自动并行处理 |
| `ws_monitor.py` | 实时 WebSocket 查看器，可查看任务执行过程中的实时进度 |
| `health_check.py` | 集成多种验证功能，检查 comfy-cli、服务器、模型以及整体系统的运行状态 |
| `fetch_logs.py` | 根据给定的 prompt_id 获取对应的错误堆栈信息或状态消息 |

**示例工作流（`workflows/`）：** SD 1.5、SDXL、Flux Dev、SDXL img2img、SDXL inpaint、ESRGAN 上采样、AnimateDiff 视频生成、Wan T2V 等。更多详情请参阅 `workflows/README.md`。

## 适用场景

- 用户希望使用 Stable Diffusion、SDXL、Flux、SD3 等模型生成图像
- 用户需要运行特定的 ComfyUI 工作流文件
- 用户想要串联多个生成步骤（如 txt2img → 上采样 → 人脸修复）
- 用户需要使用 ControlNet、图像修复、img2img 或其他高级处理流程
- 用户希望管理 ComfyUI 任务队列、检查模型状态或安装自定义节点
- 用户希望通过 AnimateDiff、Hunyuan、Wan、AudioCraft 等工具生成视频/音频/3D 内容

## 架构：双层设计

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: comfy-cli (official lifecycle tool)        │
│   Setup, server lifecycle, custom nodes, models     │
│   → comfy install / launch / stop / node / model    │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│ Layer 2: REST/WebSocket API + skill scripts         │
│   Workflow execution, param injection, monitoring   │
│   POST /api/prompt, GET /api/view, WS /ws           │
│   → run_workflow.py, run_batch.py, ws_monitor.py    │
└─────────────────────────────────────────────────────┘
```

**为何需要两层架构？** 官方 CLI 在安装和服务器管理方面表现优异，但在工作流执行方面的支持极为有限。REST/WS API 则填补了这一空白——这些接口能够处理参数注入、执行监控以及输出下载等功能，而这些都是 CLI 所不具备的。

## 快速入门

### 检测环境

```bash
# What's available?
command -v comfy >/dev/null 2>&1 && echo "comfy-cli: installed"
curl -s http://127.0.0.1:8188/system_stats 2>/dev/null && echo "server: running"

# Can this machine run ComfyUI locally? (GPU/VRAM/disk check)
python3 scripts/hardware_check.py
```

如果尚未安装任何组件，请参阅下方的**设置与入门指南**——但务必先执行硬件检测。

### 一键健康检查

```bash
python3 scripts/health_check.py
# → JSON: comfy_cli on PATH? server reachable? at least one checkpoint? smoke-test passes?
```

## 核心工作流程

### 第一步：获取 API 格式的工作流 JSON 文件

工作流必须采用 API 格式（每个节点都包含 `class_type` 属性）。这些工作流可通过以下途径获取：

- ComfyUI 网页界面 → **Workflow → Export (API)**（新版界面）或旧版界面中的“Save (API Format)”按钮；
- 该技能自带的 `workflows/` 目录（即可直接运行的示例文件）；
- 社区下载的文件（如 civitai、Reddit、Discord 等平台），这类文件通常为编辑器格式，需先导入 ComfyUI 再重新导出。

编辑器格式（以顶层 `nodes` 和 `links` 数组的形式存在）**无法直接执行**。相关脚本会检测到这一点，并提示用户需要重新导出。

### 第二步：查看哪些参数是可控制的

```bash
python3 scripts/extract_schema.py workflow_api.json --summary-only
# → {"parameter_count": 12, "has_negative_prompt": true, "has_seed": true, ...}

python3 scripts/extract_schema.py workflow_api.json
# → full schema with parameters, model deps, embedding refs
```

### 第 3 步：带参数运行

```bash
# Local (defaults to http://127.0.0.1:8188)
python3 scripts/run_workflow.py \
  --workflow workflow_api.json \
  --args '{"prompt": "a beautiful sunset over mountains", "seed": -1, "steps": 30}' \
  --output-dir ./outputs

# Cloud (export API key once; uses correct /api routing automatically)
export COMFY_CLOUD_API_KEY="comfyui-..."
python3 scripts/run_workflow.py \
  --workflow workflow_api.json \
  --args '{"prompt": "..."}' \
  --host https://cloud.comfy.org \
  --output-dir ./outputs

# Real-time progress via WebSocket (requires `pip install websocket-client`)
python3 scripts/run_workflow.py \
  --workflow flux_dev.json \
  --args '{"prompt": "..."}' \
  --ws

# img2img / inpaint: pass --input-image to upload + reference automatically
python3 scripts/run_workflow.py \
  --workflow sdxl_img2img.json \
  --input-image image=./photo.png \
  --args '{"prompt": "make it watercolor", "denoise": 0.6}'

# Batch / sweep: 8 random seeds, parallel up to cloud tier limit
python3 scripts/run_batch.py \
  --workflow sdxl.json \
  --args '{"prompt": "abstract"}' \
  --count 8 --randomize-seed --parallel 3 \
  --output-dir ./outputs/batch
```

当 `seed` 参数设置为 `-1`（或使用 `--randomize-seed` 选项省略该参数）时，每次运行都会生成一个全新的随机种子。

### 第 4 步：展示结果

脚本会将描述每个输出文件的 JSON 数据输出到标准输出中：

```json
{
  "status": "success",
  "prompt_id": "abc-123",
  "outputs": [
    {"file": "./outputs/sdxl_00001_.png", "node_id": "9",
     "type": "image", "filename": "sdxl_00001_.png"}
  ]
}
```

## 决策树

| 用户输入 | 工具 | 命令 |
|-----------|------|---------|
| **生命周期管理（使用 comfy-cli）** | | |
| “安装 ComfyUI” | comfy-cli | `bash scripts/comfyui_setup.sh` |
| “启动 ComfyUI” | comfy-cli | `comfy launch --background` |
| “停止 ComfyUI” | comfy-cli | `comfy stop` |
| “安装 X 节点” | comfy-cli | `comfy node install <name>` |
| “下载 X 模型” | comfy-cli | `comfy model download --url <url> --relative-path models/checkpoints` |
| “列出已安装的模型” | comfy-cli | `comfy model list` |
| “列出已安装的节点” | comfy-cli | `comfy node show installed` |
| **执行流程（使用脚本）** | | |
| “所有准备就绪了吗？” | 脚本 | `health_check.py`（可选参数：`--workflow X --smoke-test`） |
| “在这个工作流中我可以修改什么？” | 脚本 | `extract_schema.py W.json` |
| “检查 W 的依赖项是否满足” | 脚本 | `check_deps.py W.json` |
| “修复缺失的依赖项” | 脚本 | `auto_fix_deps.py W.json` |
| “生成图像” | 脚本 | `run_workflow.py --workflow W --args '{...}'` |
| “使用这张图像”（图像到图像转换） | 脚本 | `run_workflow.py --input-image image=./x.png ...` |
| “生成 8 种随机种子版本的图像” | 脚本 | `run_batch.py --count 8 --randomize-seed ...` |
| “显示实时处理进度” | 脚本 | `ws_monitor.py --prompt-id <id>` |
| “获取任务 X 的错误信息” | 脚本 | `fetch_logs.py <prompt_id>` |
| **直接通过 REST 接口操作** | | |
| “队列中有哪些任务？” | REST | `curl http://HOST:8188/queue`（本地环境）或 `--host https://cloud.comfy.org` |
| “取消那个任务” | REST | `curl -X POST http://HOST:8188/interrupt` |
| “释放 GPU 内存” | REST | `curl -X POST http://HOST:8188/free` |

## 设置与入门指南

当用户请求设置 ComfyUI 时，**首先需要询问他们希望使用 Comfy Cloud（托管服务，无需安装，需 API 密钥）还是本地模式（在自身设备上安装 ComfyUI）**。在得到答复之前，请勿开始执行任何安装命令或硬件检测。

**官方文档：** https://docs.comfy.org/installation  
**CLI 文档：** https://docs.comfy.org/comfy-cli/getting-started  
**云服务文档：** https://docs.comfy.org/get_started/cloud  
**云服务 API 文档：** https://docs.comfy.org/development/cloud/overview  

### 第 0 步：询问本地还是云服务（务必首先进行）

建议使用的脚本内容如下：

> “您希望在自己的设备上本地运行 ComfyUI，还是使用 Comfy Cloud？
>
> - **Comfy Cloud** — 依托 RTX 6000 Pro GPU 运行，所有常用模型都已预装，无需额外设置。需要 API 密钥（实际运行工作流需订阅付费服务；免费套餐仅支持读取功能）。如果您没有性能足够的 GPU，可选择此方案。
> - **本地模式** — 免费，但您的设备必须满足以下硬件要求：
>   - 拥有 **≥6 GB VRAM** 的 NVIDIA GPU（SDXL 模型需 ≥8 GB，Flux/video 模型需 ≥12 GB），或
>   - 支持 ROCm 的 AMD GPU（Linux 系统），或
>   - 配备 **≥16 GB 统一内存** 的 Apple Silicon Mac（M1+系列，建议 ≥32 GB）。
>   - Intel Mac 以及没有 GPU 的设备无法使用此模式，建议选择云服务。
> 
> 您希望选择哪种方式？”

后续处理流程：

- **选择云服务** → 直接进入 **路径 A**。
- **选择本地模式** → 先执行硬件检测，再根据检测结果从路径 B–E 中选择相应步骤。
- **尚未确定** → 先执行硬件检测，由检测结果决定后续操作。

### 第 1 步：验证硬件规格（仅当用户选择本地模式时执行）

```bash
python3 scripts/hardware_check.py --json
# Optional: also probe `torch` for actual CUDA/MPS:
python3 scripts/hardware_check.py --json --check-pytorch
```

| 判定结果    | 含义                                                         | 操作建议 |
|------------|---------------------------------------------------------------|----------|
| `ok`       | 独立显卡显存≥8 GB，或 Apple Silicon 芯片统一内存≥32 GB         | 可本地安装——使用报告中的 `comfy_cli_flag` 参数 |
| `marginal` | SD1.5 模型可用；SDXL 模型运行较吃力；Flux及视频生成功能基本不可用 | 轻量级工作流可本地运行，否则请选择**方案A：云端服务** |
| `cloud`    | 无可用 GPU，显存<6 GB，Apple Silicon 芯片统一内存<16 GB，使用 Intel Mac 或 Rosetta 版 Python | 除非用户明确要求本地安装，否则应**切换至云端服务** |

该脚本还会显示 `wsl: true`（通过 NVIDIA passthrough 技术在 WSL2 环境中运行）以及 `rosetta: true`（在 Apple Silicon 芯片上运行 x86_64 版 Python——需重新安装为 ARM64 版本）的标识。

若判定结果为 `cloud` 但用户仍希望本地安装，则不应默许操作。需原样显示 `notes` 数组中的说明，并询问用户是选择(a)切换至云端服务，还是(b)强行进行本地安装（在现代模型上这会导致内存不足或运行速度极慢）。

### 选择安装方案

首先进行硬件检测。若用户已告知其硬件配置，则可参考下表选择方案：

| 使用场景                     | 推荐方案 |
|------------------------------|----------|
| 硬件检测结果为 `verdict: cloud` | **方案A：Comfy Cloud** |
| 无 GPU 或希望先尝试且不承担长期使用成本 | **方案A：Comfy Cloud** |
| Windows 系统 + NVIDIA 显卡 + 非技术用户 | **方案B：ComfyUI 桌面版** |
| Windows 系统 + NVIDIA 显卡 + 技术用户 | **方案C：便携版** 或 **方案D：comfy-cli** |
| Linux 系统 + 任意 GPU          | **方案D：comfy-cli**（最简单） |
| macOS 系统 + Apple Silicon 芯片 | **方案B：桌面版** 或 **方案D：comfy-cli** |
| 无显示界面环境/服务器环境/持续集成环境/Agent 环境 | **方案D：comfy-cli** |

对于完全自动化的流程（硬件检测→安装→启动→验证）：

```bash
bash scripts/comfyui_setup.sh
# Or with overrides:
bash scripts/comfyui_setup.sh --m-series --port=8190 --workspace=/data/comfy
```

它会内部运行 `hardware_check.py`，若检测结果为“云端”则拒绝进行本地安装（除非使用了 `--force-cloud-override` 参数），同时会选择合适的 `comfy-cli` 参数，并优先使用 `pipx`/`uvx` 而非全局的 `pip`，以避免污染系统 Python 环境。

---

### 方案 A：Comfy Cloud（无需本地安装）

适用于没有高性能 GPU 或希望无需任何配置的用户。服务运行在 RTX 6000 Pro 上。

**文档链接：** https://docs.comfy.org/get_started/cloud

1. 在 https://comfy.org/cloud 注册账号
2. 在 https://platform.comfy.org/login 处生成 API 密钥
3. 设置该密钥：
   ```bash
   export COMFY_CLOUD_API_KEY="comfyui-xxxxxxxxxxxx"
   ```
4. 运行工作流：
   ```bash
   python3 scripts/run_workflow.py \
     --workflow workflows/flux_dev_txt2img.json \
     --args '{"prompt": "..."}' \
     --host https://cloud.comfy.org \
     --output-dir ./outputs
   ```

**定价信息：** https://www.comfy.org/cloud/pricing  
**并发任务数量：** 免费版/标准版为1个，创作者版为3个，专业版为5个。免费版本  
**无法通过API运行工作流**——仅可浏览模型。若需使用 `/api/prompt`、`/api/upload/*`、`/api/view` 等接口，则需订阅付费服务。  

---

### 方案B：ComfyUI桌面版（Windows / macOS）  
专为非技术用户设计的单键安装程序，目前处于测试阶段。  

**文档说明：** https://docs.comfy.org/installation/desktop  
- **Windows（NVIDIA显卡）：** https://download.comfy.org/windows/nsis/x64  
- **macOS（Apple Silicon芯片）：** https://comfy.org  
桌面版**不支持Linux系统**——请选择方案D。  

---

### 方案C：ComfyUI便携版（仅限Windows）  

**文档说明：** https://docs.comfy.org/installation/comfyui_portable_windows  
可从 https://github.com/comfyanonymous/ComfyUI/releases 下载文件，解压后运行 `run_nvidia_gpu.bat`。如需更新，则执行 `update/update_comfyui_stable.bat`。  

---

### 方案D：comfy-cli（所有平台适用——推荐用于Agent场景）  
官方命令行工具是实现无界面/自动化设置的最佳选择。  

**文档说明：** https://docs.comfy.org/comfy-cli/getting-started  

#### 安装comfy-cli

```bash
# Recommended:
pipx install comfy-cli
# Or use uvx without installing:
uvx --from comfy-cli comfy --help
# Or (if pipx/uvx unavailable):
pip install --user comfy-cli
```

以非交互方式禁用分析功能：
```bash
comfy --skip-prompt tracking disable
```

#### 安装 ComfyUI

```bash
comfy --skip-prompt install --nvidia              # NVIDIA (CUDA)
comfy --skip-prompt install --amd                 # AMD (ROCm, Linux)
comfy --skip-prompt install --m-series            # Apple Silicon (MPS)
comfy --skip-prompt install --cpu                 # CPU only (slow)
comfy --skip-prompt install --nvidia --fast-deps  # uv-based dep resolution
```

默认路径为：Linux系统下为`~/comfy/ComfyUI`，MacOS/Windows系统下为`~/Documents/comfy/ComfyUI`。如需更改路径，可使用命令`comfy --workspace /custom/path install`进行指定。

#### 启动 / 验证

```bash
comfy launch --background                       # background daemon on :8188
comfy launch -- --listen 0.0.0.0 --port 8190    # LAN-accessible custom port
curl -s http://127.0.0.1:8188/system_stats      # health check
```

### 方案 E：手动安装（高级用法/不支持的硬件）

适用于 Ascend NPU、Cambricon MLU、Intel Arc 以及其他不受支持类型的硬件。

**文档链接：** https://docs.comfy.org/installation/manual_install

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
pip install -r requirements.txt
python main.py
```

### 安装完成后：下载模型

```bash
# SDXL (general purpose, ~6.5 GB)
comfy model download \
  --url "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" \
  --relative-path models/checkpoints

# SD 1.5 (lighter, ~4 GB, good for 6 GB cards)
comfy model download \
  --url "https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors" \
  --relative-path models/checkpoints

# Flux Dev fp8 (smaller variant, ~12 GB)
comfy model download \
  --url "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors" \
  --relative-path models/checkpoints

# CivitAI (set token first):
comfy model download \
  --url "https://civitai.com/api/download/models/128713" \
  --relative-path models/checkpoints \
  --set-civitai-api-token "YOUR_TOKEN"
```

列出已安装的节点：`comfy model list`。

### 安装完成后：安装自定义节点

```bash
comfy node install comfyui-impact-pack             # popular utility pack
comfy node install comfyui-animatediff-evolved     # video generation
comfy node install comfyui-controlnet-aux          # ControlNet preprocessors
comfy node install comfyui-essentials              # common helpers
comfy node update all
comfy node install-deps --workflow=workflow.json   # install everything a workflow needs
```

### 安装完成后：验证操作

```bash
python3 scripts/health_check.py
# → comfy_cli on PATH? server reachable? checkpoints? smoke test?

python3 scripts/check_deps.py my_workflow.json
# → are this workflow's nodes/models/embeddings installed?

python3 scripts/run_workflow.py \
  --workflow workflows/sd15_txt2img.json \
  --args '{"prompt": "test", "steps": 4}' \
  --output-dir ./test-outputs
```

## 图像上传（img2img / 修复绘图）

最简单的方法是使用 `run_workflow.py` 并结合 `--input-image` 参数：

```bash
python3 scripts/run_workflow.py \
  --workflow workflows/sdxl_img2img.json \
  --input-image image=./photo.png \
  --args '{"prompt": "make it cyberpunk", "denoise": 0.6}'
```

该参数会上传`photo.png`文件，随后将其服务器端的文件名注入到名为`image`的任何架构参数中。对于图像修复功能，则需要同时传入这两个参数。

```bash
python3 scripts/run_workflow.py \
  --workflow workflows/sdxl_inpaint.json \
  --input-image image=./photo.png \
  --input-image mask_image=./mask.png \
  --args '{"prompt": "fill with flowers"}'
```

通过 REST 接口手动上传：
```bash
curl -X POST "http://127.0.0.1:8188/upload/image" \
  -F "image=@photo.png" -F "type=input" -F "overwrite=true"
# Returns: {"name": "photo.png", "subfolder": "", "type": "input"}

# Cloud equivalent:
curl -X POST "https://cloud.comfy.org/api/upload/image" \
  -H "X-API-Key: $COMFY_CLOUD_API_KEY" \
  -F "image=@photo.png" -F "type=input" -F "overwrite=true"
```

## 云端特定设置

- **基础 URL：** `https://cloud.comfy.org`
- **认证方式：** 使用 `X-API-Key` 请求头（WebSocket 则使用 `?token=KEY`）
- **API 密钥：** 仅需设置一次 `$COMFY_CLOUD_API_KEY`，脚本会自动读取该密钥
- **输出文件下载：** `/api/view` 会返回一个指向带签名 URL 的 302 状态码；脚本会跟随该链接，并在从存储后端获取数据前移除 `X-API-Key`（以避免 API 密钥泄露到 S3/CloudFront）
- **与本地 ComfyUI 的端点差异：**
  - `/api/object_info`、`/api/queue`、`/api/userdata` —— 免费套餐会返回 **403 错误**，仅付费套餐可用
  - 云端的 `/history` 已重命名为 `/history_v2`，脚本会自动进行路由转发
  - 云端的 `/models/<folder>` 已重命名为 `/experiment/models/<folder>`，脚本同样会自动处理路由
  - WebSocket 中的 `clientId` 参数目前会被忽略——同一用户的所有连接都会收到相同的广播消息，需在客户端通过 `prompt_id` 进行过滤
  - 上传文件时虽支持 `subfolder` 参数，但实际会被忽略——云端采用扁平化命名空间结构
- **并发任务数量：** 免费/标准套餐为 1 个，创作者套餐为 3 个，专业套餐为 5 个。超出限额的任务会自动进入排队队列。如需充分利用当前套餐的并发上限，可使用 `run_batch.py --parallel N` 命令

## 队列与系统管理

```bash
# Local
curl -s http://127.0.0.1:8188/queue | python3 -m json.tool
curl -X POST http://127.0.0.1:8188/queue -d '{"clear": true}'    # cancel pending
curl -X POST http://127.0.0.1:8188/interrupt                      # cancel running
curl -X POST http://127.0.0.1:8188/free \
  -H "Content-Type: application/json" \
  -d '{"unload_models": true, "free_memory": true}'

# Cloud — same paths under /api/, plus:
python3 scripts/fetch_logs.py --tail-queue --host https://cloud.comfy.org
```

## 常见问题与注意事项

1. **必须使用 API 格式** — 所有脚本以及 `/api/prompt` 接口均要求输入 API 格式的流程 JSON。这些脚本会识别编辑器格式的文件（即顶层包含 `nodes` 和 `links` 数组的结构），并提示用户通过“Workflow → Export (API)”（新版界面）或“Save (API Format)”（旧版界面）重新导出。

2. **服务器必须处于运行状态** — 所有操作都需要运行中的服务器。`comfy launch --background` 可用于启动服务器，可通过 `curl http://127.0.0.1:8188/system_stats` 来确认服务器是否正常运行。

3. **模型名称必须完全准确** — 名称区分大小写，且需包含文件扩展名。`check_deps.py` 会进行模糊匹配（允许包含或不包含扩展名及文件夹前缀），但流程本身必须使用标准名称。可使用 `comfy model list` 查看已安装的模型。

4. **缺少自定义节点** — 出现“class_type not found”错误表示某个必需的节点未安装。`check_deps.py` 会提示需要安装的包，而 `auto_fix_deps.py` 可自动完成安装流程。

5. **工作目录问题** — `comfy-cli` 会自动检测 ComfyUI 的工作目录。如果出现“未找到工作目录”的错误，可使用 `comfy --workspace /path/to/ComfyUI <command>` 或 `comfy set-default /path/to/ComfyUI` 指定工作目录。

6. **云服务免费套餐的 API 限制** — 免费账户使用 `/api/prompt`、`/api/view`、`/api/upload/*`、`/api/object_info` 等接口时会返回 403 错误。`health_check.py` 和 `check_deps.py` 能够妥善处理这种情况，并给出明确的提示信息。

7. **视频/音频流程的超时设置** — 当输出节点为 `VHS_VideoCombine`、`SaveVideo` 等类型时，系统会自动检测到此类流程，并将默认超时时间从 300 秒延长至 900 秒。如需手动调整，可使用 `--timeout 1800` 指定新的超时时间。

8. **输出文件名中的路径遍历风险** — 服务器生成的文件名会经过 `safe_path_join` 处理，从而防止出现超出 `--output-dir` 范围的路径。请保持此安全机制启用，因为使用自定义保存节点的流程可能会生成任意路径。

9. **流程 JSON 可能包含恶意代码** — 由于自定义节点会执行 Python 代码，因此提交未知流程相当于执行了 `eval` 语句，存在安全风险。在运行来自不可信来源的流程之前，请务必先进行检查。

10. **自动随机化种子值** — 若希望每次运行都使用新的种子值，可在 `--args` 参数中传入 `seed: -1`（或使用 `--randomize-seed` 且不指定具体种子值）。实际生成的种子值会记录到标准错误流中。

11. **跟踪功能提示** — 首次运行 `comfy` 时可能会弹出关于数据统计的提示。如需跳过此交互式提示，可使用 `comfy --skip-prompt tracking disable` 命令。`comfyui_setup.sh` 脚本也可自动完成此操作。

## 验证清单

可通过运行 `python3 scripts/health_check.py` 一次性检查所有项目。也可手动逐一检查：

- [ ] `hardware_check.py` 的检测结果为 `ok`，或用户已明确选择 Comfy Cloud 服务  
- [ ] `comfy --version` 命令能正常执行（或 `uvx --from comfy-cli comfy --help` 命令也可）  
- [ ] `curl http://HOST:PORT/system_stats` 命令能返回 JSON 格式的数据  
- [ ] `comfy model list` 能显示至少一个检查点（本地存储的），或 `/api/experiment/models/checkpoints` 能返回云端模型列表  
- [ ] 流程 JSON 为 API 格式  
- [ ] `check_deps.py` 的检测结果显示 `is_ready: true`（若处于云服务免费套餐，则仅显示 `node_check_skipped`）  
- [ ] 使用小型流程进行测试运行后能成功完成，且输出文件会保存在 `--output-dir` 指定的目录中
