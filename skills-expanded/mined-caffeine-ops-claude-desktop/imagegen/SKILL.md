---
name: imagegen
description: |
  Generate and edit images using an OpenAI-compatible Image API for project assets — UI mockups, icons, illustrations, social cards, transparent-background cutouts, and visual references. Supports single generation, batch generation, and image editing (inpainting, background replacement, object removal, compositing).
triggers:
  - "generate image"
  - "create image"
  - "image gen"
  - "openai image"
  - "icon design"
  - "mockup"
od:
  mode: image
  category: image-generation
  upstream: "https://github.com/openai/skills"
---

# imagegen

面向 OpenAI 兼容 Image API 的图像生成 / 编辑技能。生成或编辑位图素材：网站
资源、游戏素材、UI / 产品样机、线框图、logo、写实照片、信息图、透明背景抠图等。

> [!IMPORTANT]
> ## 安静模式（面向用户产品的默认行为，务必遵守）
>
> 这是个面向普通用户的桌面产品。用户想要的是「说一句话 → 直接出图」，**不是**看
> 一屏排障日志。生图时严格遵守：
>
> 1. **不要预先 dry-run**。参数拼好直接跑真实生成命令，一步到位。dry-run 只在你
>    自己不确定参数、需要自检时才用，且不要把它当成给用户看的步骤。
> 2. **不要逐步旁白**。别播报「我先确认解释器」「dry-run 请求体正常」「现在正式
>    生成」这类中间步骤。用户不关心过程。
> 3. **不要自己 `mkdir` 建输出目录、不要指定 `--out` 到 Desktop 之类的地方**。
>    脚本已有默认输出目录（`~/.cowork/imagegen/`，见下「保存约定」），直接跑
>    `generate --prompt "..."` 即可，落盘位置交给脚本。用户没要求就别自定义路径。
> 4. **不用管代理**。脚本默认已直连网关、绕过系统代理（见下）。**不要**再去查
>    `env | grep proxy`、不要试 `env -u HTTP_PROXY`、不要纠结 SSL——那些问题脚本
>    层已经根治。命令一次跑通就好。
> 5. **成功后只说一句话收尾**。例如「生成好了。」即可——只要按下面「聊天
>    卡片渲染契约」前台跑命令，app 会自动把成图渲染在命令卡原位，你不需要
>    也不应该再做任何「展示图片」的动作。失败了才简短说原因。
>
> 目标就是复刻这个体验：用户发「黄仁勋在吃饭」→ 你回「生成好了。」+ 一张图。中间
> 不刷屏。

> [!IMPORTANT]
> ## 聊天卡片渲染契约（app UI 依赖，务必遵守）
>
> claude-desktop 聊天界面会把 `image_gen.py` 的 Bash 调用识别成专属「图片
> 生成卡」：运行中显示「正在创建图片」点阵显影动画占位卡，跑完后成图直接
> 渲染在卡片原位（用户点击可进标记改图面板）。识别与成果定位全靠命令 /
> 输出的文本特征（UI 侧实现见 `apps/studio/src/chat/components/chat/
> ThreadView/ImageGenCard.tsx`），所以：
>
> 1. **生成 / 编辑命令保持单独一条 Bash 调用**，命令文本里直接出现
>    `image_gen.py generate|generate-batch|edit`。挑解释器的 `IMG_PY=...`
>    前缀可以拼在同一条命令里；但**不要**用 `&&` / `;` 串接其它无关命令、
>    不要把脚本包进 wrapper 转调——那会污染 stdout、破坏识别。
> 2. **前台跑，且把 Bash 工具的 `timeout` 参数开到 600000（10 分钟）**。
>    edit / `--quality high` / 大图输入动辄跑 2–5 分钟，默认 2 分钟超时会把
>    命令拦腰掐死。**绝不要 `run_in_background` 跑生成命令**——后台跑法的
>    stdout 落在 task output 文件里，聊天卡拿不到成果路径，图就不上屏，
>    你还得靠轮询 Read output 文件干等（2026-07-09 超分任务实测踩过：图生
>    成功躺在磁盘上，用户在聊天里什么都看不到）。
> 3. **脚本 stdout 的 `Wrote /abs/path.png` 行是 UI 定位成果图的 wire 契约**。
>    改脚本时不许删改这行的格式；生成后也不要自己再 `echo` / `ls` 路径——
>    多打一行路径会被 UI 误认成多一张成果图。
> 4. **成功后不要再用 Read 工具去读成品图**（Read 的 image 块在聊天里不
>    渲染，白耗上下文）——成图已经在卡片里，按安静模式一句话收尾即可，
>    不必贴路径。
> 5. **兜底**：万一命令确实跑在了后台（或超时被转后台）、或走了
>    `remove_chroma_key.py` 抠图两步法（那步刻意不触发生成卡），聊天卡就
>    渲染不出成图——此时收尾那句话里**必须带上成果图的绝对路径**：消息
>    文本里的图片路径会渲染成可打开的成果文件卡，这是这些路径下唯一的
>    出图通道。

> [!IMPORTANT]
> ## 运行环境（本 fork 已适配 claude-desktop）
>
> 上游 imagegen 默认走 OpenAI Codex 的内置 `image_gen` 工具 + `$CODEX_HOME`，
> 那套在 claude-desktop / fusion-code 宿主里**不存在**。本 fork 已把
> `scripts/image_gen.py` 改造为**纯标准库 + OpenAI 兼容网关直连**（复用与
> `gpt-image-2` 同一份 `_shared.py`：urllib 打 `/images/generations` 和
> `/images/edits`，凭证 / base_url 从环境变量与 `.env` 读取，见下）。
>
> - **零额外依赖**：脚本只用 Python 标准库，跑在 app 自带的 Python 3.12
>   runtime 上，**不需要 `pip install openai` 或 `Pillow`**。
> - `--downscale-max-dim`（生成后本地缩图）是唯一需要 `Pillow` 的可选参数；
>   不传就不 import PIL。bundled runtime 没装 Pillow，所以**默认不要用**这个
>   参数——需要缩图时交给宿主的其它工具做。
> - 透明背景辅助脚本 `scripts/remove_chroma_key.py` **也已改写为纯标准库**
>   （手写 PNG 编解码 + 可分离腐蚀 + box-blur 高斯近似，抠图算法与上游 1:1），
>   bundled runtime 直接能跑。限制：输入输出都必须是 `.png`（8-bit 非交错）。

## 挑解释器（记到 `$IMG_PY`）

与 `gpt-image-2` 同一套约定：

1. app 自带 runtime（主进程注入 `PPT_MASTER_PYTHON_HOME`）：
   - macOS/Linux：`$PPT_MASTER_PYTHON_HOME/bin/python3`
   - Windows：`$PPT_MASTER_PYTHON_HOME\python.exe`
2. 没注入则回退系统 `python3`（3.8+ 都行，只用标准库，不挑版本）。

一行搞定（macOS/Linux）：

```bash
IMG_PY="${PPT_MASTER_PYTHON_HOME:+$PPT_MASTER_PYTHON_HOME/bin/python3}"; [ -x "$IMG_PY" ] || IMG_PY="$(command -v python3)"
```

## 环境变量（与 gpt-image-2 一致，可共用 `~/.gateway.env`）

按此顺序读取（进程环境变量优先，然后 `<cwd>/.env` → `<cwd>/.gateway.env`
→ `~/.gateway.env` → skill 自带 `.env`）：

- `OPENAI_API_KEY` — 网关凭证，必需。
- `OPENAI_BASE_URL` — 默认 `https://api.openai.com/v1`，指向 OpenAI 兼容网关。
- `OPENAI_IMAGE_MODEL` — 默认 `gpt-image-2`，可换成网关支持的型号。

> 代理：**本 fork 默认直连网关、自动绕过系统代理**（`HTTP_PROXY`/`HTTPS_PROXY`
> 常把网关连接劫持导致 SSL 握手中断，实测必挂）。你**不需要**做任何代理相关的
> 处理——直接跑命令即可。极少数必须经代理才能出网的环境，才显式加 `--use-proxy`
> 恢复「尊重系统代理」。

## 子命令

```bash
# 1. 文本生图（不传 --out 即落到默认目录 ~/.cowork/imagegen/，文件名自动带时间戳）
$IMG_PY skills/imagegen/scripts/image_gen.py generate \
  --prompt "A cute baby sea otter" --size 1024x1024 --quality high

# 2. 批量生图（一个 JSONL 每行一个 job；不传 --out-dir 也落默认目录）
$IMG_PY skills/imagegen/scripts/image_gen.py generate-batch \
  --input jobs.jsonl

# 3. 编辑已有图（inpainting / 背景替换 / 抠除 / 合成）
$IMG_PY skills/imagegen/scripts/image_gen.py edit \
  --image assets/source.png \
  --prompt "Replace the background with a clean studio scene"

# 4. 带遮罩的局部编辑
$IMG_PY skills/imagegen/scripts/image_gen.py edit \
  --image assets/source.png --mask assets/mask.png \
  --prompt "Replace only the masked area with a glass vase"
```

每个子命令都支持 `--dry-run` 先打印将要发出的请求体，不真正调网关——建议先
dry-run 确认参数无误再实跑。

## 独有能力（相对 gpt-image-2）

- `--input-fidelity high`：编辑时更强地保留原图结构 / 身份（人像、产品）。
- `generate-batch`：一次描述多个 job 顺序出图（本 fork 已把上游的异步并发
  降级为同步顺序，因为 bundled runtime 无 `AsyncOpenAI`；功能不变，只是不并发）。
- **透明背景工作流（两步法，bundled runtime 可用）**：
  1. 先生成**平色底**图——prompt 里明确要求主体放在纯色背景上（默认用纯绿
     `#00ff00`；若主体本身含大量绿色，换 `#ff00ff` 品红等与主体色相远的键色），
     背景必须平整无渐变无阴影。
  2. 再本地抠除键色：
     ```bash
     $IMG_PY skills/imagegen/scripts/remove_chroma_key.py \
       --input 生成的图.png --out 透明结果.png \
       --auto-key corners --soft-matte --despill
     ```
     `--auto-key corners` 自动从四角采键色（比手填 `--key-color` 稳）；
     `--soft-matte` 平滑边缘、`--despill` 去除主体边缘的键色污染；毛边可再
     加 `--edge-feather 1`。纯标准库实现，无需 Pillow；输入输出限 `.png`。
  - 若网关型号本身支持 `--background transparent --output-format png`
    （gpt-image-2 不支持），可跳过两步法直接产出。

## 提示词方法论与样例

写 prompt 前读这两个参考文件（imagegen 的核心价值）：

- `references/prompting.md` — 提示词工程指南（结构、字段、如何问用户）。
- `references/sample-prompts.md` — 可直接复用的样例 prompt 库。
- `references/cli.md` / `references/image-api.md` — CLI 参数与 API 字段细节。

## 保存约定

- **默认输出目录**：用户没指定 `--out` / `--out-dir` 时，图片落到
  `~/.cowork/imagegen/`（与 local-kb 同套路的用户主目录隐藏文件夹，恒可写、用户
  找得到、能备份）。这个绝对路径由 claude-desktop 主进程经
  `CLAUDE_DESKTOP_IMAGEGEN_DIR` 注入；脱离 app 直接命令行裸跑时回退到相对
  工作区的 `output/imagegen/`。文件名取任务语义短名 + 时间戳，避免重名。
- 显式传 `--out /abs/path.png` 或 `--out-dir /abs/dir/` 时一切照旧，尊重用户路径。
- 编辑现有图默认**不覆盖**原文件——产出 `xxx-edited.png` 之类的兄弟文件，除非
  用户明确要求替换。

## 何时提问

只在缺失且显著影响结果时问：没有 prompt 目标、改图没原图、主体身份 / 视觉类型
决定走向、商品 / 价格 / 文案是画面核心、用户表达了互相冲突的目标。其它情况优先
做合理默认并继续。
