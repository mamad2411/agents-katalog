---
name: chatppt-creator
description: 专业级智能 PPT 全生命周期创作与增强套件。支持通过 yoo-ai API 自动生成、编辑与美化 PPT。当需要执行以下任务时使用此 Skill：(1) 【多源生成】：将简单主题、结构化大纲、本地文件（.docx, .txt）或 AI 编码项目（架构分析）转化为专业 PPT；(2) 【专家流】：需要“先审阅大纲、后生成内容”的高质量创作流程，支持对大纲进行增删改查；(3) 【后期增强】：为已有任务添加演讲稿（Speaker Notes）、在指定位置插入新页面、或更换全局风格（字体、颜色、模板）；(4) 【互动引导】：预览精美封面、实时追踪异步生成任务进度、以及针对“内容太少”或“格式错误”等生成失败情况进行自动诊断与修复。适用于“帮我做个 PPT”、“总结这个项目的架构”、“给 PPT 加演讲稿”等指令。
---

# ChatPPT-Creator 智能 Skill 套件

这是一个基于意图识别的 PPT 处理工具集。Agent 应根据用户需求自动路由到相应的函数。

## 核心函数套件

> **注意**: 在调用以下命令时，请确保使用脚本的完整路径（相对于项目根目录或绝对路径）。

### 1. PPT 创建 (Creation)

#### create_ppt_from_text
当用户提供主题或简单描述时调用。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js create_from_text --text "<主题>" --font_name "<字体>" --color "<颜色>" --language "<语言>" --report "<true/false>"`
- **可用字体**: [黑体|宋体|仿宋|幼圆|楷体|隶书] (注意：不支持微软雅黑)。
- **注意**: `report` 默认为 `true`，启用在线编辑报告模式。

#### create_ppt_from_custom_outline
当用户提供详细结构化大纲时调用。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js create_from_custom_outline --custom_data '<JSON大纲>' --font_name "<字体>" --color "<颜色>" --report "<true/false>"`
- **可用字体**: [黑体|宋体|仿宋|幼圆|楷体|隶书]。
- **注意**: `report` 默认为 `true`。

#### create_ppt_from_file (Agent 复合任务)
当用户提供本地文件（.txt, .docx 等）时：
1. **读取文件**: 使用 `Read` 工具读取文件内容。
2. **大模型转换**: 将内容转换为 `create_ppt_from_custom_outline` 所需的 JSON 格式。
3. **展示并确认 (关键)**: **必须**将生成的结构化大纲（标题、章节、页面主题）以易读的格式展示给用户，并明确询问：“这是为您生成的大纲，您看是否满意？如果有需要调整的地方请告诉我。”
4. **调用函数**: 仅在用户确认满意后，才执行 `create_ppt_from_custom_outline`。

#### create_ppt_from_file_with_review
使用专家级 Prompt 驱动的工作流，生成高质量 Markdown 大纲，解析为 JSON，供审阅与微调后再生成。
- **阶段一（生成 Prompt）**  
  `node {{SKILL_PATH}}/scripts/chatppt_creator.js create_from_file_with_review --file_path "<本地文件>" --user_prompt "<要求>" --count_1 5 --count_2 3 --language zh-CN`  
  输出 `[PROMPT_START]...[PROMPT_END]`，请用 LLM 生成 Markdown 并保存到文件。
- **阶段二（解析与审阅）**  
  `node {{SKILL_PATH}}/scripts/chatppt_creator.js create_from_file_with_review --file_path "<本地文件>" --user_prompt "<要求>" --count_1 5 --count_2 3 --language zh-CN --markdown_path "<markdown文件路径>"`  
  输出 `[OUTLINE_REVIEW_START]...[OUTLINE_REVIEW_END]`。
- **用户确认 (强制)**: Agent 必须将输出的大纲内容呈现给用户，并等待用户确认或修改意见。**严禁跳过此步骤直接生成。**
- **应用修改（按用户反馈）**  
  准备补丁 JSON（支持 remove_catalog/rename_catalog/remove_sub_catalog/rename_sub_catalog），执行：  
  `node {{SKILL_PATH}}/scripts/chatppt_creator.js apply_outline_patch --json_path "<outline.json>" --patch_path "<patch.json>"`
- **最终生成**  
  仅在用户明确表示“可以生成”后，执行：
  `node {{SKILL_PATH}}/scripts/chatppt_creator.js generate_from_outline --json_path "<outline.json>" --font_name "<字体>" --color "<颜色>" --language "zh-CN" --report "<true/false>"`
- **可用字体**: [黑体|宋体|仿宋|幼圆|楷体|隶书]。
- **注意**: `report` 默认为 `true`。

#### create_ppt_from_project_analysis
自动分析当前 AI 编码项目的架构 and 技术栈，生成项目总结或汇报 PPT。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js create_from_project_analysis --project_path "<项目绝对路径>" --user_prompt "<汇报重点>"`
- **适用场景**: 当用户说“为这个项目写个汇报”或“总结一下我的代码架构”时。
- **工作流**: 
  1. 脚本扫描项目（依赖、目录、入口点）。
  2. 输出专家 Prompt，Agent 调用 LLM 生成 Markdown。
  3. 脚本解析并展示大纲供用户审阅。
  4. 确认后执行生成。

### 2. 修改与增强 (Modification)

#### add_speaker_notes_to_ppt
为已有任务生成演讲稿。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js add_notes --task_id "<ID>" --report "<true/false>"`

#### insert_page_into_ppt
在指定位置插入新页面。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js insert_page --task_id "<ID>" --slide_number "<页码>" --slide_type "<类型>" --text "<内容>" --report "<true/false>"`

#### regenerate_ppt_with_new_style
更换风格重新生成。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js regenerate --task_id "<ID>" --font_name "<字体>" --color "<颜色>" --cover_id "<模板ID>" --transition "<1/2>" --report "<true/false>"`

### 3. 模板与预览 (Template & Preview)

#### preview_ppt_covers
根据标题和风格偏好预览可选的 PPT 模板封面。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js preview_covers --title "<标题>" --style "<风格>" --color "<颜色>" --count 4`
- **可用风格**: 科技风, 商务风, 小清新, 极简风, 中国风, 可爱卡通。

#### check_task_status
查看历史任务或特定任务的实时生成进度。
- **命令**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js check_status --task_id "<ID>"`
- **无参数调用**: `node {{SKILL_PATH}}/scripts/chatppt_creator.js check_status` (显示最近 10 条记录)

## 交互准则

### 1. 意图识别
Agent 应从自然语言中提取参数。
**重要**: 
- 对于**高质量、专业性强**的汇报需求，Agent **必须**优先引导用户使用 `create_ppt_from_file_with_review` 或 `create_ppt_from_project_analysis` 流程。
- 基本的 `create_from_text` 仅适用于极其简单的草稿需求，内容会非常简略。

### 2. 参数传递约束 (Parameter Whitelist)
**重要**: 为了避免 API 报错，Agent 必须严格遵守以下参数规定：
1.  **禁止推测字体**: 绝对禁止自行推测或默认添加 `--font_name "微软雅黑"`。
2.  **静默政策**: 如果用户没有在指令中明确要求特定字体（例如：“用宋体”），你**绝对禁止**在生成的命令中包含 `--font_name` 参数。
3.  **字体白名单**: 仅允许使用以下字体：`黑体`、`宋体`、`仿宋`、`幼圆`、`楷体`、`隶书`。如果用户要求的字体不在名单内（如微软雅黑），请忽略该要求或引导用户选择白名单内的字体。

### 3. 立即反馈，后台处理
启动任何生成任务后，脚本会立即输出 `[EDITOR_URL_START]url[EDITOR_URL_END]` 作为“实时工作台”。
**Agent 动作**:
1. 立即提取此链接。
2. 告知用户：“任务已成功启动，正在后台异步处理。您可以点击此处 **[进入在线工作台]** 实时观看 PPT 的渲染生成过程。生成完成后我会自动为您下载到本地。”
3. 严禁在任务未完成前阻塞用户。

### 4. 分开输出与链接约束 (Output Constraints)
**重要**: 为了保持交互的清晰度，Agent 必须**强制执行**以下输出规范：
1.  **严禁混合输出**: 在线工作台链接（任务开始时）和本地下载成功的确认信息（任务完成下载后）**绝对禁止**在同一次对话回复中同时展示。
2.  **禁用 Markdown 链接**: 不要使用 `[文本](链接)` 语法。必须将 URL 放置在**代码块**中，或以**纯文本**形式展示。
3.  **识别标记**:
    - 实时工作台: 识别 `[EDITOR_URL_START]` 和 `[EDITOR_URL_END]`。
    - 最终编辑链接: 任务完成后再次确认 `[EDITOR_URL_START]`。
    - 预览图片: 识别 `[IMAGE_URL_START]` 和 `[IMAGE_URL_END]`。
4.  **分阶段展示**:
    - 任务启动后：仅展示“实时工作台链接”。
    - 任务完成后：仅展示“下载路径”和“编辑链接”。

### 5. 错误诊断与协议 (Error Handling & Protocol)
如果接口调用返回 400 错误，或运行报错：
1.  **任务失败 (-1/3)**: 
    - Agent **禁止**仅复读错误信息。
    - 必须从脚本输出中提取失败原因，并主动调用 `node {{SKILL_PATH}}/scripts/chatppt_creator.js validate_outline --json_path "<path>"` 进行诊断。
    - 反馈示例：“生成中断了，原因是‘内容长度不足’。我已经找到了问题，是否需要我为您补充内容后重新生成？”
2.  **API Key 缺失**: 
    - Agent 应主动询问用户：“我发现您还没有配置 yoo-ai 的 API Key。如果您已有 Key，请告诉我，我将为您自动创建配置文件。如果您还没有 Key，可以前往 yoo-ai 官网获取。”
    - 获取 Key 后，调用 `Write` 工具将 Key 写入 `{{SKILL_PATH}}/config.json`，格式为 `{"API_KEY": "用户提供的KEY"}`。
3.  **JSON 校验失败**: 
    - Agent 应调用 `node {{SKILL_PATH}}/scripts/chatppt_creator.js validate_outline --json_path "<path>"` 来获取具体的错误列表。
4.  **重试**: 修复后，再次运行 `generate_from_outline`。

### 6. 异步追踪 (Asynchronous Tracking)
如果用户关闭了对话或链接失效，Agent 应引导用户使用：
- `node {{SKILL_PATH}}/scripts/chatppt_creator.js check_status --task_id "<ID>"` 找回任务状态及最新链接。

### 7. 主动引导 (Proactive Guidance)
**重要**: 每次任务完成（看到 `[TASK_COMPLETED]` 标记）后，Agent **必须**主动询问用户是否需要进一步修改，例如：
> "您的 PPT 已生成并下载。需要我为您做进一步的修改吗？例如 **添加演讲稿**、**更换主题色或模板**，或者 **插入新的页面**？"

如果在开始前用户对风格不确定，可以引导：
> "在生成之前，您想先看看几种不同风格（如商务风、极简风）的**模板封面**吗？"

## 配置
确保 `config.json` 中已配置 `API_KEY`。参考 `config.json.template`。
