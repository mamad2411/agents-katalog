---
name: bailian-train-deploy
description: 用百炼 CLI (`bl`) 走完"数据→微调训练→导出→部署→调用"的完整闭环，或跳过训练直接部署基座模型。支持文本模型（SFT/DPO/CPT）、音频 TTS 模型（CosyVoice）、图像生成模型（Wan2.7）和视频生成模型（Wan i2v/kf2v）微调。涵盖数据集校验/上传、创建微调任务、等待训练、导出最佳 checkpoint、创建推理部署、等待就绪、给出调用示例。当用户提到在百炼 / DashScope / 阿里云模型工作室上"训练模型""微调""fine-tune""finetune""部署模型""模型上线""把微调模型跑起来/调用""训练一个推理模型""继续预训练""LoRA/SFT/DPO 训练""语音合成模型""TTS 微调""CosyVoice""声音克隆""图像生成微调""文生图""图生图""Wan2.7""图像模型训练""视频生成微调""图生视频""首帧生视频""首尾帧""kf2v""i2v""Wan视频""视频特效训练"等，都应激活本技能——即使用户没明说"用 bl"，只要意图是百炼平台的训练或部署，就用本技能，不要自己拼凑命令。
---

# 百炼模型训练→部署闭环 (`bl`)

用百炼 CLI `bl` 把模型部署成可调用的专属推理服务——可以先微调再部署，也可以跳过训练直接部署基座。支持文本、音频 TTS、图像生成和视频生成四种模态，两处"等待"用 Monitor 异步轮询，不阻塞主流程。

```
链路 A（先训练后部署）：
数据集 → finetune <模态> create → 等 SUCCEEDED → 导出模型(通常自动) → deploy <模态> create → 等 RUNNING → 调用

链路 B（直接部署基座，跳过训练）：
选基座 → deploy <模态> create → 等 RUNNING → 调用
```

链路 B 适用于"只想把某个基座跑成自己的部署服务"——和直接调用 API 在推理上没本质区别，但能拿到独立部署实例、可调速率/计费方式、纳入自己的运维。**仅当用户明确表示不训练 / 跳过训练 / 直接部署基座时才走这条**；用户只是没提训练细节时，默认按链路 A 引导，不要擅自跳过训练。

**模态分发**：本技能的通用流程适用于所有模态，但数据格式、超参、推理命令因模态而异。确定用户意图后，按模态查阅对应参考文件：
- **文本模型**（对话/推理）→ [`references/text.md`](references/text.md)
- **音频 TTS 模型**（语音合成/CosyVoice）→ [`references/audio.md`](references/audio.md)
- **图像生成模型**（文生图/图生图/Wan2.7）→ [`references/image.md`](references/image.md)
- **视频生成模型**（图生视频/首尾帧/Wan i2v/kf2v）→ [`references/video.md`](references/video.md)
- 未来新增模态 = 新增对应 reference 文件，本流程骨架不变

> 本技能假设 `bl`（bailian-cli）已安装。命令/flag 细节以 `bl <cmd> --help` 为准；本技能聚焦**流程编排与避坑**。

## 写操作护栏（创建前必读）

`bl finetune <模态> create` 与 `bl deploy <模态> create` 都是真实写操作，会产生计费资源（微调训练 + 推理部署）。`bl` **没有 `--dry-run`**，所以用**预检命令**代替预演、用**计费确认**把关预留资源。任何写操作前必须先过这三道闸：

1. **预检代替 dry-run**（创建前必跑，确认可行再写）。这些预检命令本身都需先通过下方[前置检查](#前置检查动作流起点)的认证——未认证先 `bl auth login` 再预检：
   - 训练前：`bl finetune capability --base-model <base>` —— 确认基座支持你选的 training-type（不支持会快速失败且不耗配额；`create` 提交时也会再校验一次）。
   - 部署前：`bl deploy models --source custom`（链路 A 微调输出）或 `--source base`（链路 B 基座）—— 确认目标模型可部署、看清可用 plan，再决定 `--plan`。
   - 复用检测：`bl deploy list --status RUNNING` —— 若已有引用同一 `finetuned_output` 且 RUNNING 的部署，直接复用其 `deployed_model`，**不要再建第二个计费实例**。
2. **计费确认硬闸门（mu/ptu）**：
   - `lora`（默认，按 token 计费，闲置一般不计费）—— 安全默认，可直接创建。
   - `mu` / `ptu` 是**预留/独占资源，闲置也计费**——创建前**必须**向用户显式说明计费方式并取得确认。在 agent / CI 等非交互环境**不能自动开通预留资源**。命中 mu/ptu 时，把“这会产生闲置计费”连同命令交还给真人在终端确认（`bl` 当前不提供 `--yes` 跳过确认 flag，确认行为完全由真人把控）。
3. **账号就绪检查**：`bl auth status` —— `authenticated: false` 即停，给 `bl auth login --api-key sk-...`。百炼走 API key / access token 认证，**没有独立的实名闸门**，`auth status` 即账号就绪检查。

## 反触发表（不归本 skill 的意图，附完整命令）

| 用户意图 | 路由到 | 完整示范命令 |
|---|---|---|
| 只想试模型效果 / 一次性对话 | `bailian-cli` | `bl text chat --model qwen3-8b --message "..."` |
| 已确定模型，只要调用方式 | `bailian-cli` | `bl text chat --model <model> --message "..."` |
| 不知道选哪个基座 / 模型选型 | `bailian-model-recommend` | （让该 skill 按场景推荐）|
| 纯查模型参数 / 价格 / 上下文窗口 | `bailian-docs-llm-wiki` | （查模型数据目录）|
| 已有部署，只想生成调用示例 | `bailian-cli` | `bl text chat --model <deployed_model> --message "..."` 或 `bl speech synthesize --model <deployed_model> --voice default --text "..."` 或异步 API + 触发词（图像生成，见 [image.md](references/image.md#推理与调用)）|
| 对已有训练任务 / 部署做查删（生命周期） | `bl` 直接 | `bl finetune list` / `bl deploy list` / `bl deploy delete --deployed-model <id>` |

> 本 skill 只负责"新建训练任务 + 新建部署 + 调用交付"这一条闭环。训练任务与部署的**全生命周期管理**（list / stop / delete 历史任务、删除部署等）不在本 skill 流程内，用 `bl finetune list` / `bl deploy list` / `bl deploy delete` 直接操作。

## 反幻觉清单

- **`--base-model` / `--model-name` / `--model` 分属不同命令，切勿复用**：
  - `bl finetune <模态> create --base-model` → 基座模型名（文本 `qwen3-8b`，音频 `cosyvoice-v3-flash`，图像 `wan2.7-image-pro`）。
  - `bl deploy <模态> create --model-name` → 导出模型名（链路 A：`qwen3-8b-ft-...` / `cosyvoice-v3-flash-ft-...` / `wan2.7-image-pro-ft-...`；链路 B：基座名）。
  - 推理命令 `--model` → 必须用 `deploy <模态> create` 响应里的 `deployed_model`，**不是**你传给 deploy <模态> create 的名字。
- **`--training-type` 取值穷举**：`sft` / `sft-lora`（默认）/ `dpo` / `dpo-lora` / `cpt`。映射在 CLI 边界完成（`sft-lora`→`efficient_sft`），永远传 CLI 值，不要传服务端字符串。`cpt` 无 `-lora` 变体。音频 TTS 和图像生成都只用 `sft-lora`——`finetune audio create` / `finetune image create` **不暴露此 flag**，仅 `finetune text create` 接受。
- **`--plan` 取值穷举**：`lora`（默认，token 计费）/ `ptu`（需 `--input-tpm`/`--output-tpm`）/ `mu`（需 `--deploy-spec`/`--capacity`）。链路 B 基座通常**不支持 `lora`**。音频 TTS 微调模型**只支持 `mu`**。图像生成微调模型**只支持 `lora`**。
- **`--deploy-spec`**（非 ~~template-id~~）：mu plan 的部署规格 flag。CLI 从 catalog 读取 `template_id`，在请求体中发送为 `deploy_spec`。
- **`--source` 取值穷举**（`bl deploy models`）：`custom`（微调输出）/ `base`（基座）/ `public`。
- **`--learning-rate` 必须字符串**：传 `"3e-4"`，不要传数字 `3e-4`，避免 JSON 精度丢失（文本适用，音频/图像不需要传此参数）。
- **推理命令因模态不同**：文本模型用 `bl text chat`，音频 TTS 用 `bl speech synthesize --voice default`，图像生成用异步 API + 触发词（详见 [`references/image.md`](references/image.md#推理与调用)）。
- **没有这些 flag/子命令**：`bl` 无 `--dry-run`、无裸 `finetune create`/`deploy create`（**必须带模态段**：`finetune text|audio|image create`、`deploy text|audio|image create`）、无 `finetune start`、无 `deploy stop`（停用/恢复用 `bl deploy pause` / `bl deploy resume`；pause 对 mu/ptu 停止计费）。
- **必填**：`finetune <模态> create` 的 `--base-model` / `--datasets`；`deploy <模态> create` 的 `--model-name` / `--display-name`。

## 前置检查（动作流起点）

- 认证：`bl auth status`，确认已配置 API key（`DASHSCOPE_API_KEY` 或 `bl auth login --api-key sk-...`）。
- 基座选型：查询训练能力用 `bl finetune capability`（查 listFoundationModels，走 API key、无需 console 登录）：
  - `bl finetune capability --base-model <base>` —— 该模型支持哪些训练类型。
  - `bl finetune capability --training-type sft-lora` —— 反向查：哪些模型支持该训练类型（返回 `models` 列表，含中文名）。
  - 选定基座后可直接进入第 2 步；`bl finetune <模态> create` 提交前也会再用 listFoundationModels 校验，不支持会快速失败。
  - 文本推理推荐 Qwen3 系列（`qwen3-8b` / `qwen3-14b` / `qwen3.6-flash`）；音频 TTS 用 `cosyvoice-v3-flash`；图像生成用 `wan2.7-image-pro` / `wan2.7-image`。

## 第 1 步：准备数据集

支持三种数据来源，由你（Agent）根据用户意图灵活选用，不必写死交互流程——你本身具备主动提问能力，知道有哪些选项后自然向用户确认即可：

1. **本地数据集** —— 用户提供本地文件路径，直接使用。
2. **已上传数据集** —— 从百炼上已有的数据集中选取（`bl dataset list`）。
3. **生成示例数据** —— 征得用户同意后，由你生成一份小规模示例数据，仅用于跑通流程（效果有限，需如实告知用户）。

**数据格式因模态不同**，详见对应参考文件：
- **文本模型**：`.jsonl` 文件（ChatML/DPO/CPT schema），详见 [`references/text.md`](references/text.md#数据格式)。
- **音频 TTS**：`.zip` 包（内含 `data.jsonl` + `train/*.wav`），详见 [`references/audio.md`](references/audio.md#数据格式)。
- **图像生成**：`.zip` 包（内含 `data.jsonl` + 图像文件平铺），详见 [`references/image.md`](references/image.md#数据格式)。

提交训练前用 `bl dataset validate --file <path>` 校验通过再继续（CLI 自动探测 schema，也可 `--schema tts` / `--schema image` / `--schema chatml` 显式指定）。

## 第 2 步：创建微调任务

```bash
bl finetune <模态> create \
  --base-model <base-model> \
  --datasets <path-or-file-id> \
  --output json
```

**training-type 取值与映射**详见 [`references/finetune.md`](references/finetune.md)。**模态特异性超参**见对应参考文件：
- 文本模型（`finetune text create`）：接受 `--training-type` / `--n-epochs` / `--learning-rate` 等，详见 [`references/text.md`](references/text.md#创建训练任务)。
- 音频 TTS（`finetune audio create`）：**不暴露 `--training-type`**（内部固定 `sft-lora`），超参由 CLI 自动注入，详见 [`references/audio.md`](references/audio.md#创建训练任务)。
- 图像生成（`finetune image create`）：**不暴露 `--training-type`**（内部固定 `sft-lora`），超参由 CLI 自动注入，详见 [`references/image.md`](references/image.md#创建训练任务)。

从响应记下：`output.job_id`、`output.finetuned_output`（输出模型名，形如 `<base>-ft-<ts>-<id>`）。

## 第 3 步：等待训练完成（异步）

用 Monitor 工具运行本技能自带的等待脚本——它会在状态变化时通知，到终态退出：

```
Monitor command: bash <本技能目录>/scripts/wait.sh finetune <JOB_ID>
```

`<本技能目录>` 即本技能的 base 目录（技能加载时会给出，含 `scripts/wait.sh`），用实际路径替换。脚本每 30s 轮询，终态为 `SUCCEEDED`/`FAILED`/`CANCELED`/`PARTIALLY_SUCCEEDED`。

⚠️ **避坑：不要在 zsh 里手写 `status=...` 轮询循环。** `status` 是 zsh 的只读内置变量，赋值会报 `read-only variable` 并让脚本 exit 1。用本技能的 bash 脚本（`#!/usr/bin/env bash`）规避，或自写时改用 `st` 等变量名。

## 第 4 步：导出最佳模型（通常可跳过）

任务 SUCCEEDED 后，平台**会自动导出 best checkpoint** 为可部署模型——直接进第 5 步即可，无需手动导出。

只有要部署**非 best** 的某个 checkpoint 时才显式导出：
```bash
bl finetune checkpoints --job-id <JOB_ID>          # 列出可用 checkpoint
bl finetune export --job-id <JOB_ID> --checkpoint <name> --model-name <自定义名>
```

## 第 5 步：创建部署

> 创建前先过[写操作护栏](#写操作护栏创建前必读)：`bl deploy list --status RUNNING` 查是否已有同模型部署可复用；`bl deploy models --source custom|base` 确认可用 plan；`mu`/`ptu` 必须先取得用户计费确认。

⚠️ **关键避坑：微调后的模型不能直接用微调输出名调用，会 404 `Model not exist`。必须先创建部署。**（链路 B 部署基座同理——直接调用走的是公共推理，不经过你的部署实例。）

```bash
bl deploy <模态> create \
  --model-name <finetuned-output> \   # 微调输出名(链路A) 或基座名(链路B)
  --display-name <display-name> \
  --plan <lora|ptu|mu> \              # 见下方说明
  --output json
```

- **模态段**（`text` / `audio` / `image`）须与部署模型模态匹配；三个模态子命令 flag 完全相同。
- `--model-name`：链路 A 传第 2 步的 `finetuned_output`；链路 B 直接传基座模型名。
- `--plan`：
  - 文本微调模型默认 `lora`（token 计费），也可用 `mu`。
  - **音频 TTS 微调模型只支持 `mu`**（不支持 `lora` / `ptu`），需 `--deploy-spec` + `--capacity`。
  - **图像生成微调模型只支持 `lora`**（不支持 `mu` / `ptu`）。
  - 链路 B 基座通常只支持 `ptu`/`mu`，**不支持 `lora`**。
  - 各 plan 必填参数与计费细则见 [`references/deploy.md`](references/deploy.md)。
- `--deploy-spec`：mu plan 的部署规格（如 `dps-20260521172224-1vabse`），省略时自动从 catalog 匹配。
- 不确定支持哪些 plan：链路 A 用 `bl deploy models --source custom`，链路 B 用 `bl deploy models --source base`，按返回的 `plans` 选。

⚠️ **避坑（最高频错误）：`--model-name` 与推理命令的 `--model` 含义不同**——`deploy <模态> create --model-name` 传导出模型名，响应返回的 `output.deployed_model` 才是部署实例 id，推理命令 `--model` 必须用 `deployed_model`，**不要复用**。详见 [`references/deploy.md`](references/deploy.md)。

从响应记下：`output.deployed_model`。

## 第 6 步：等待部署就绪（异步）

```
Monitor command: bash <本技能目录>/scripts/wait.sh deploy <DEPLOYED_MODEL>
```

`<本技能目录>` 同第 3 步。每 15s 轮询，`RUNNING` 即就绪（`FAILED`/`STOPPED` 终止）。

⚠️ **避坑：状态传播延迟。** 部署刚到 `RUNNING` 时立即调用，可能短暂返回 404 `Model not exist`——这是服务端状态传播延迟，不是用错模型名。`bl deploy get` 也可能还显示 `PENDING`。约 1 分钟内会稳定，遇 404 等十几秒重试即可；若持续 404，先核对用的是 `deployed_model` 而非微调输出名。

## 第 7 步：调用与交付

**推理命令因模态不同**：

文本模型：
```bash
bl text chat --model <DEPLOYED_MODEL> --message "你的问题"
```

音频 TTS 模型：
```bash
bl speech synthesize --model <DEPLOYED_MODEL> --voice default --text "你要合成的文本" --out result.mp3
```

图像生成模型（异步 API，需触发词）：
```bash
# 详见 references/image.md —— 需 X-DashScope-Async 头 + prompt 含触发词
```

> `--model` 必须用 `deploy <模态> create` 响应中的 `deployed_model`，**不是**微调输出名。音频 TTS 的 `--voice` 固定为 `default`。图像生成需异步调用且 prompt 包含触发词。详见对应模态参考文件。

向用户交付时给出：
- **部署实例 id**（`deployed_model`）——调用用它，不是微调输出名
- 一条可直接运行的推理示例命令
- 常用运维命令：`bl deploy get --deployed-model <id>` 查状态；`bl deploy delete --deployed-model <id>` 删除部署；`bl finetune list` 查历史任务。

## 收尾提示
- **闲置计费与删除**：`lora` 闲置一般不计费；`mu`/`ptu` 闲置也计费，不用要清理；`bl deploy delete` 只能删 STOPPED/FAILED 的部署，RUNNING 的 mu/ptu 可先 `bl deploy pause`（停止计费）再删。细则见 [`references/deploy.md`](references/deploy.md#计费与运维细则)。
- **复用数据集**：多次训练同一数据时，先 `bl dataset upload` 拿 file-id，再用 `--datasets <file-id>` 避免重复上传。
- **效果不好**：优先加数据（量与质量），其次调 `n-epochs`/`learning-rate`，最后才考虑全参 `sft`。小数据集（<100 条）效果上限有限，要管理预期。
