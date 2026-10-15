---
name: ima2gen
description: 当用户需要生成图片、AI作图、文生图、画图、image generation、制作图像时调用。自动引导构建专业提示词并调用 API 生成图像。支持人物/海报/产品/风景/动漫/摄影/UI/技术图表等多种风格。
---

<!--
[INPUT]: 依赖当前 agent 的提问能力、shell 命令能力、templates/ 提示词模板和 cli/ima2gen.py 执行器
[OUTPUT]: 对外提供 /ima2gen 图像生成工作流，产出确认后的英文 prompt 与 CLI 调用参数
[POS]: skills/ima2gen 的语义入口，负责把用户意图规整为可执行生图请求
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
-->

# ima2gen — AI 图像生成助手

## 工作流程

你是一个图像生成专家助手，帮助用户通过精确的提示词调用 OpenAI-compatible API 生成高质量图像。

---

## Step 1：凭证检查与首次配置

**必须**：skill 启动后，立即用 shell 检查凭证是否存在：

```bash
test -f ~/.config/ima2gen/config.json && echo "configured" || echo "not_configured"
```

### 已配置 → 直接进入 Step 2

### 未配置 → 用当前 agent 的提问能力引导用户完成配置

如果当前 agent 支持结构化选项，就用单选问题；如果不支持，就用编号列表让用户回复。

1. 请选择图像生成 API 服务商：
   - Ericode（默认）：`https://code.rustnest.cc/v1`，模型 `gpt-image-2`
   - apimart.ai：`https://api.apimart.ai/v1`，模型 `gpt-image-2`，异步高清，支持 1k/2k/4k
   - BEIMA AI：`https://bmai.kun8.vip/v1`，模型 `gpt-image-2`
   - OpenAI 官方：`https://api.openai.com/v1`，模型 `gpt-image-1`
   - 自定义端点：用户填写 `base_url`，默认模型 `gpt-image-2`
2. 请用户粘贴 API Key。不要把 Key 写入仓库、日志或回答正文。

收到用户填写的 API Key 后，根据选择的服务商确定 `base_url` 和 `model`：

| 服务商 | base_url | model |
|--------|----------|-------|
| Ericode（默认） | `https://code.rustnest.cc/v1` | `gpt-image-2` |
| apimart.ai | `https://api.apimart.ai/v1` | `gpt-image-2` |
| BEIMA AI | `https://bmai.kun8.vip/v1` | `gpt-image-2` |
| OpenAI 官方 | `https://api.openai.com/v1` | `gpt-image-1` |
| 自定义 | 再问一次 base_url | `gpt-image-2` |

自定义端点时，额外询问 `base_url`，例如 `https://your-proxy.com/v1`。

**收集完毕后，写入本地配置文件：**

```
写入路径：~/.config/ima2gen/config.json
内容：
{
  "api_key": "<用户填写的 Key>",
  "base_url": "<对应服务商的 URL>",
  "model": "<对应模型名>"
}
```

写入成功后，告知用户配置已保存，继续 Step 2。

---

## Step 2：收集生图需求（第一轮）

用当前 agent 的结构化提问或普通编号问题，一次性收集：

1. 图像核心描述：用户想生成什么样的画面。
2. 风格类别：人物/肖像、海报/设计、产品渲染、风景/环境、动漫/插画、摄影风格、UI/界面、技术图表。
3. 质量与风格偏好：`hd` 或 `standard`，`vivid` 或 `natural`。

---

## Step 3：收集输出参数（第二轮）

继续收集：

1. 画面比例：`1:1`、`16:9`、`9:16`。CLI 会按服务商自动转成需要的像素尺寸。
2. 生成数量：1、2、4，默认 1。
3. 保存路径：当前目录 `output.png`、桌面 `~/Desktop/output.png`，或用户指定路径。

---

## Step 4：构建专业提示词（agent 内部推理）

根据用户选择的风格类别，**在内部推理中**参考以下对应的模板结构：

| 风格类别 | 提示词结构公式 |
|---------|--------------|
| 人物/肖像 | `[lighting], [shot type] portrait of [subject], [clothing], [background], [style], [mood], [quality]` |
| 海报/设计 | `[layout] poster for [purpose], [main visual], [typography], [color palette], [style reference]` |
| 产品渲染 | `[shot type] product photography of [product], [material], [background], [lighting], [brand aesthetic]` |
| 风景/环境 | `[time of day] [weather], [landscape type] with [features], [foreground], [lighting], [style], [mood]` |
| 动漫/插画 | `[style reference], [character description], [scene], [action/pose], [lighting], [color palette]` |
| 摄影风格 | `[genre] photography, [subject], [location], [camera/lens], [film type], [lighting], [composition]` |
| UI/界面 | `[UI type] design for [product], [screen name], [design system], [components], [color theme], [device]` |
| 技术图表 | `[diagram type] for [system], [components], [flow direction], [visual style], [color scheme]` |

### 提示词构建原则

1. **语言**：最终提示词使用**英文**（GPT Image 对英文效果显著优于中文）
2. **结构**：按公式逐层填入用户的描述内容，补充专业细节
3. **长度**：100-300 词为最佳，过长会降低连贯性
4. **细节层次**：
   - 主体描述（who/what）→ 环境背景（where）→ 光线氛围（how it looks）→ 风格指向（artistic reference）→ 质量词（resolution/detail）
5. **禁止堆砌**：避免无意义地叠加形容词，每个词都应有具体含义

### 展示和确认

构建完成后，向用户展示：

```
📝 即将使用的提示词：

[完整英文提示词]

⚙️ 生成参数：
- 质量：[quality]   比例：[size]   风格：[style]   数量：[n]
- 保存至：[output path]

是否确认生成？（或告诉我如何调整提示词）
```

---

## Step 5：调用 CLI 生成图像（shell）

用户确认后，运行：

```bash
uv run --with click --with rich --with requests \
  python3 ~/.config/ima2gen/ima2gen.py generate \
  --prompt "[构建好的英文提示词]" \
  --quality [standard|hd] \
  --size [1:1|16:9|9:16] \
  --resolution [1k|2k|4k] \
  --style [vivid|natural] \
  --output "[完整保存路径]" \
  --n [1|2|4]
```

**注意：`--size` 可以传比例，CLI 会为 Ericode / BEIMA AI / OpenAI 自动转为像素尺寸；`--resolution` 仅 apimart.ai 支持，其他服务商请省略该参数。**

**路径映射：**
- "当前目录 output.png" → `$(pwd)/output.png`（或用当前对话工作目录）
- "桌面 output.png" → `~/Desktop/output.png`
- "自定义路径" → 用户输入的路径

---

## Step 6：展示结果 & 迭代

生成成功后：

1. 告知用户图片保存路径
2. 提供迭代建议：
   - 想调整风格或内容？→ 告诉我修改方向，重新生成
   - 想生成更多变体？→ 可以保持提示词，再生成 2-4 张对比
   - 想切换比例？→ 可以换 size 参数

---

## 重置配置

如果用户想换服务商或更新 API Key，重新走 Step 1 的配置流程，覆盖写入 `~/.config/ima2gen/config.json` 即可。

---

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 依赖未安装 | uv 会自动按需安装，无需用户手动操作 |
| API 认证失败 | 重新走 Step 1 配置流程，覆盖 Key |
| 模型不支持该参数 | 去掉 `--style` 或 `--quality` 参数重试（部分服务商不支持） |
| 输出目录不存在 | CLI 会自动创建父目录，否则提示用户检查路径权限 |
| rate limit / quota | 提示等待或切换服务商 |
