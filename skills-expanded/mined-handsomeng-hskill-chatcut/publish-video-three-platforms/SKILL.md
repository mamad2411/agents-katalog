---
name: publish-video-three-platforms
description: Prepare and upload an approved local video to Xiaohongshu, Douyin, and WeChat Channels through the user's logged-in browser. Analyze the actual video or transcript with AI, generate platform-specific titles, descriptions, and hashtags from the content, validate official topic selection, apply scheduling and original-content options when available, and stop before the final publish button unless the user explicitly authorizes publishing. Trigger when a user asks to publish or prepare one video for these three Chinese creator platforms.
---

# 三平台视频发布

把已经验收的本地视频准备到小红书、抖音和微信视频号。先理解视频，再为每个平台独立生成标题、正文和话题。上传可以重叠，上传后的填写和验收严格单平台串行。最终操作默认归用户，停在最终发布按钮前。

## 前置要求

- 只处理用户已经确认完成的视频。
- 使用用户指定的本地 MP4 或 MOV 文件。
- 使用用户已经登录的平台页面。执行前完整读取浏览器控制 Skill。
- 不读取或保存 Cookie、密码、Token、本地存储和浏览器凭证。
- 设置 `final_action_owner: user` 和 `final_click_authorized_current_turn: false` 作为每个任务的默认值。
- 普通的“发布到三平台”“把三个平台搞完”等表述只授权准备发布，禁止点击最终按钮。
- 只有用户在当前任务中明确说“现在直接点击发布”“现在直接点击发表”等同义指令，才设置 `publish.mode: publish_now`、`final_action_owner: agent` 和 `final_click_authorized_current_turn: true`。历史授权、定时要求和无人值守要求均不能替代当前任务授权。

## 固定入口

- 小红书：`https://creator.xiaohongshu.com/publish/publish?source=official`
- 抖音：`https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web`
- 视频号：`https://channels.weixin.qq.com/platform/post/create`

## 核心原则

1. **内容驱动**：标题、正文和话题必须来自本期视频，不使用固定文案包。
2. **平台适配**：三个平台分别创作，禁止机械复制同一份文本。
3. **事实忠实**：不得添加视频没有表达的经历、数据、结论或承诺。
4. **AI 推理**：先分析内容和受众，再决定标题角度、正文结构和话题组合。
5. **上传重叠**：依次启动三个平台上传，让网络等待互相重叠。
6. **串行收尾**：上传完成后的填表、话题、定时、原创或声明和审核严格一次只处理一个平台。
7. **失败隔离**：一个平台卡顿时保存其状态，再串行处理下一个平台。
8. **证据验收**：重新读取页面结果，点击记录本身不算成功。

开始前读取：

- [references/content-generation.md](references/content-generation.md)：内容理解和平台化文案方法
- [references/job-and-adapters.md](references/job-and-adapters.md)：任务状态、适配器契约和恢复方法
- [references/platform-interaction-signals.md](references/platform-interaction-signals.md)：仅在当前页面快照匹配时使用的平台低自由度交互信号

## 标准流程

### 1. 分析视频

1. 确认视频路径、文件名、大小、时长和可播放状态。
2. 优先读取最终剪辑对应的转录稿。没有转录稿时，对视频转录或提取可理解的内容信息。
3. 提炼内容简报：主题、目标受众、核心观点、关键证据、冲突、结果、语气和行动建议。
4. 识别视频明确出现的专有名词、数字、品牌、人物和风险表述。
5. 内容理解不足时先补充分析，禁止只根据文件名编写发布文案。

### 2. 生成平台文案

根据内容简报分别生成三套内容：

- 一个符合平台限制的标题或短标题
- 一段符合平台阅读习惯的正文
- 3 至 5 个与视频直接相关的话题候选，或采用平台当前允许的数量

生成后执行语义核对：

- 标题准确概括视频最值得点击的真实信息。
- 正文包含视频的核心价值，不提前泄露全部内容，也不制造虚假悬念。
- 话题覆盖主题、受众、场景和细分领域，删除与内容无关的泛流量词。
- 三个平台的表达角度可以不同，核心事实必须一致。
- 用户提供了标题或正文时优先保留其意图，只做平台适配和长度调整。

### 3. 创建任务状态

为本次任务创建非敏感状态记录。可以保存在当前工作区的：

```text
.agent-state/publish-video-three-platforms/<job_id>.json
```

记录视频路径、生成文案、`active_platform`、平台步骤、验证证据和错误。`active_platform` 默认是 `null`。每个平台从任务创建起明确记录 `final_button_clicked: false`。禁止保存凭证。

创建后运行：

```bash
python3 scripts/job_state.py validate <job.json>
```

更新单个平台时使用原子更新，禁止手工复制整段平台状态：

```bash
python3 scripts/job_state.py update <job.json> <platform> --patch '{"state":"media_ready"}'
```

### 4. 页面预检

1. 接管标签前先调用 `browser.tabs.list()` 读取受控标签。
2. 目标页已经受控时调用 `browser.tabs.get()` 复用。目标页不在受控列表时，才从 `user.openTabs()` 按平台域名和发布路径精确匹配并 claim。禁止重复 claim 已受控标签。
3. 没有精确匹配的已有页面时再打开固定入口。
4. 确认页面已登录、可编辑且没有验证码或风险确认。
5. 检查页面是否已有同一视频或上一轮填写内容。
6. 检测当前页面支持的能力：定时、原创、声明、封面、话题、可见范围和最终按钮。
7. 登录或验证码问题交给用户处理，保存该平台状态后串行处理其他正常平台。

### 5. 启动全部上传

1. 在第一个正常平台选择视频，确认出现文件名、进度或预览占位。
2. 立即切换到下一个正常平台并启动上传。
3. 三个平台都开始上传后，再轮询完成状态。
4. 只有出现预览、封面或明确完成提示时，才记录上传完成。
5. 单个平台上传失败时最多重试一次。重试前确认没有残留重复视频。

### 6. 严格串行填写并验证内容

三个上传完成后选择一个平台完成以下全部步骤并达到 `review_ready`，再切换到下一个平台。用 `job_state.py update` 更新 `copy_ready`、`topics_ready`、`options_ready` 时，脚本会自动设置和校验唯一的 `active_platform`。活动平台非空时，禁止更新其他平台：

1. 读取现有字段，清除与本期视频无关的自动内容。
2. 填写该平台专用标题和正文。富文本正文必须通过真实键盘输入或粘贴完成。禁止使用 `innerHTML`、`textContent` 或对编辑器根节点调用 `fill()`。
3. 重新读取字段，确认内容完整、只出现一次且没有被截断。
4. 逐个输入内容驱动的话题候选。
5. 每个话题通过真实输入或粘贴完成，再输入尾随空格或点击完全匹配的联想项。
6. 按 [references/platform-interaction-signals.md](references/platform-interaction-signals.md) 读取正式话题元素。视觉颜色、输入动作和点击记录均不能单独作为成功证据。
7. 平台拒绝某个话题时，根据视频内容选择语义最接近的正式话题，禁止换成无关热词。

### 7. 设置发布选项

- 用户指定定时时间时，分别设置三个平台并重新读取页面显示的日期、时间和页面时区。
- 用户未指定时间时，优先使用用户已经保存的明确偏好。用户可交互时询问。用户明确要求无人值守完成时，采用页面时区次日 12:00，小红书 12:00、抖音 12:05、视频号 12:10，并在执行前说明这一假设。
- 页面存在原创能力且用户拥有原创权利时开启，并将读回结果记录到 `original_status`。
- 平台存在自主声明时按内容真实属性选择，并将读回结果记录到 `declaration_status`。原创能力和自主声明禁止合并记录。
- 原创或声明功能未显示、不适用或未设置时记录真实结果。
- 用户未指定可见范围时保留平台默认值。
- 不修改用户没有授权的商业推广、同步分发、合集或商品关联选项。

### 8. 最终页面审核

每个平台获取截图或等价页面快照，并检查：

- 视频预览或封面存在，上传已经完成。
- 标题来自本期视频并符合平台限制。
- 正文与视频事实一致，只出现一次。
- 所有话题都与内容相关，并已成为正式话题元素。
- 联想下拉框已经关闭。
- 定时、原创能力和自主声明状态与用户要求一致。
- 最终发布按钮可见且没有被点击。

发现问题时修正并重新审核。全部通过后才能交付页面。

当前任务明确授权代理点击最终按钮时，每个平台仍须先达到 `review_ready`。点击并读回发布完成后，将该平台原子更新为 `published` 和 `final_button_clicked: true`。`job_state.py update` 只允许旧状态为 `review_ready` 的平台进入 `published`。只有 `publish_now`、`final_action_owner: agent`、`final_click_authorized_current_turn: true` 同时成立时允许此状态。其他模式和未发布状态必须保持 `final_button_clicked: false`。

## 平台表达方向

以下方向用于帮助 AI 做平台适配，不是固定模板：

### 小红书

- 标题强调具体问题、经历、反差、结果或可获得价值。
- 正文保持可阅读的短段落，补充背景和观众收获。
- 话题优先覆盖内容主题、目标人群和使用场景。

### 抖音

- 标题尽快给出核心判断、冲突或结果。
- 正文简短，突出视频最值得看完或转发的观点。
- 话题优先选择平台已存在且与视频高度相关的主题。

### 视频号

- 短标题表达完整，避免过度标题化。
- 正文概括观点和价值，适合熟人传播和观点分享。
- 话题围绕内容领域、受众和核心问题选择。

平台限制和页面结构可能变化。以当前页面实时显示为准，不把历史字符限制写成永远有效的事实。

## 卡顿与恢复

1. 不刷新已有上传进度或填写内容的页面。
2. 保存最后一个已验证状态。
3. 重新接管同一标签页并读取现状。
4. 已完成的字段不重复填写，已有视频预览时不重新上传。
5. 同类操作最多重试两次。仍失败时记录截图和具体错误，继续其他平台。
6. 禁止盲点坐标、连续重复输入和从头重做整个任务。

恢复时仍执行单平台串行状态机。先把当前平台恢复到 `review_ready`、`published` 或 `blocked`，保存验证时间和证据，再切换下一个平台。详细状态转换见 [references/job-and-adapters.md](references/job-and-adapters.md)。

## 交付

交付前重新调用 `browser.tabs.list()`。只把仍在受控列表中的三个交付页标记为 deliverable，再执行 finalize。用户原有且未受控的标签保持打开，禁止将其加入 finalize 范围。

默认将页面停在最终发布按钮前，并用以下格式汇报：

```text
小红书：视频已完成｜标题正文已核对｜正式话题已确认｜定时状态｜原创状态｜声明状态｜待发布
抖音：视频已完成｜标题正文已核对｜正式话题已确认｜定时状态｜原创状态｜声明状态｜待发布
视频号：视频已完成｜标题正文已核对｜正式话题已确认｜定时状态｜原创状态｜声明状态｜待发表
发布状态：所有可完成页面均停在最终按钮前，没有点击发布
```

存在失败时写清平台、失败阶段、最后一个已验证状态、已完成内容和用户只需补的最小动作。
