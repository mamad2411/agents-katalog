---
name: teambition-bug
description: |
  Teambition Bug 管理技能，使用个人账号 userToken 直接调用官方 OpenAPI 读取、分析、留言和推进项目缺陷任务，不依赖 teambition_cli 或 MCP。
  Use when: (1) 需要读取 Teambition bug/缺陷任务详情、备注、截图图片附件和留言动态 (2) 需要识别截图内容来判断 bug 原因 (3) 需要按紧急程度排队处理 bug (4) 需要用策划等非技术人员能看懂的语言回复疑问和进展 (5) 需要修改任务状态为修改中、修复中、已认领、待验收等工作流状态，或更新标题、备注、执行人、优先级、截止时间
---

# Teambition Bug 管理

使用个人账号权限直连 Teambition 官方 OpenAPI，适合处理项目里的 bug、缺陷、任务状态推进和补充留言。

## 安装命令

```bash
npx skills add ayflying/ai-skills --skill teambition-bug
```

## 准备工作

1. 进入技能目录并安装依赖：

```bash
cd skills/teambition-bug
pip install -r requirements.txt
```

## 必须配置的参数

脚本需要两个参数才能正常运行：

| 参数 | 说明 |
|------|------|
| `TEAMBITION_TENANT_ID` | 企业 ID，对应请求头 `X-Tenant-Id` |
| `TEAMBITION_USER_TOKEN` | 个人账号 token，权限与当前 Teambition 登录账号一致 |

当前用户 ID 不需要单独配置。脚本会使用 `TEAMBITION_USER_TOKEN` 调用官方 `GET /users/me` 自动获取 `userId`，再用它校验任务第一执行者，避免多人争抢。

### 如何获取这两个参数

**获取 TEAMBITION_TENANT_ID（企业 ID）：**
1. 登录 Teambition，进入任意项目
2. 看浏览器地址栏，URL 格式为 `https://www.teambition.com/organization/<企业ID>/my/...`
3. 复制 `organization/` 后面的那串 ID 即可

**获取 TEAMBITION_USER_TOKEN（个人 token）：**
1. 打开 `https://open.teambition.com/user-mcp`
2. 使用要处理任务的 Teambition 账号登录
3. 在页面中创建或查看 `userToken`
4. 复制 `userToken`，不要复制应用 token、App Secret 或浏览器请求里的临时值

### 存储方式（二选一）

获取到参数后，有两种存储方式，请询问用户选择哪种：

**方式一：仅当前对话使用（推荐首次尝试）**

直接在对话中告诉 AI 这两个值，AI 会将它们作为环境变量传递给脚本。关闭对话后失效，不污染系统环境。

示例对话：
```
我的 Teambition 参数：
- TENANT_ID: 5f1234567890abcdef123456
- USER_TOKEN: eyJhbGciOiJIUzI1NiIs...
```

AI 会自动在每次调用脚本时带上这些参数。

**方式二：保存到电脑环境变量（持久化，所有对话可用）**

如果用户希望以后每个对话都能直接使用，需要将参数写入系统环境变量。

Windows PowerShell（管理员）：
```powershell
[Environment]::SetEnvironmentVariable("TEAMBITION_TENANT_ID", "<你的企业ID>", "User")
[Environment]::SetEnvironmentVariable("TEAMBITION_USER_TOKEN", "<你的token>", "User")
```

macOS/Linux：
```bash
echo 'export TEAMBITION_TENANT_ID="<你的企业ID>"' >> ~/.bashrc
echo 'export TEAMBITION_USER_TOKEN="<你的token>"' >> ~/.bashrc
source ~/.bashrc
```

保存后重启终端或新对话即可生效。

### 配置检测

运行以下命令检测参数是否已配置：

```bash
python scripts/teambition_bug.py check-config
```

如果缺少参数，会提示缺少哪个以及如何获取。

## 常用命令

```bash
# 解析 Teambition 链接中的 projectId、taskId、viewId
python scripts/teambition_bug.py parse-url --url "https://www.teambition.com/project/6a292e9b13e121404ffea8c5/tasks/view/6a292e9b8e598fd9e0fb2515"

# 查询项目/产品详情
python scripts/teambition_bug.py project --project-id "<projectId>"

# 按项目 TQL 查询任务
python scripts/teambition_bug.py search --project-id "<projectId>" --tql "content CONTAIN \"登录\""

# 读取 bug 完整上下文：标题、备注、动态、进展、富文本图片/附件真实下载链接
python scripts/teambition_bug.py context --task-id "<taskId>"

# 决定要修复某个任务时，先改为“修改中”，再返回完整上下文
python scripts/teambition_bug.py claim-context --task-id "<taskId>" --status-name "修改中" --yes

# 下载可访问截图，供 AI 识别图片内容
python scripts/teambition_bug.py download-images --task-id "<taskId>"

# 按官方富文本字段标识手动渲染，可用于排查图片/附件链接
python scripts/teambition_bug.py render-rich-text --rtf-fields "<taskId>:note"

# 只读取留言/动态记录
python scripts/teambition_bug.py activities --task-id "<taskId>"

# 从动态中过滤评论记录
python scripts/teambition_bug.py comments --task-id "<taskId>"

# 遇到疑问 bug 时留言追问
python scripts/teambition_bug.py ask --task-id "<taskId>" --question "请先说明如何复现：页面入口、具体操作步骤、账号/数据/环境、期望结果和实际结果，方便定位。"

# 回复任务，可引用某条动态或评论 ID
python scripts/teambition_bug.py reply --task-id "<taskId>" --reply-to "<activityId>" --content "我已开始排查。"

# 使用常用模板回复
python scripts/teambition_bug.py quick-reply --task-id "<taskId>" --template need-info

# 将任务状态/标签状态改为“修改中”
python scripts/teambition_bug.py start --task-id "<taskId>" --status-name "修改中" --yes

# 只读审计真实卡片字段，确认工作流状态、看板列、任务列表、卡片类型/自定义字段
python scripts/teambition_bug.py audit-task --task-id "<taskId>"

# 如果已知道正确面板字段，完成时同步校验；任一字段不匹配会直接报错
python scripts/teambition_bug.py finish --task-id "<taskId>" --verification "远程容器编排启动并验证通过" --expect-tasklist-id "<待验收列表ID>" --expect-custom-field "类型=Bug" --yes

# 或按当前工作流已有状态更新，例如待验收
python scripts/teambition_bug.py update-status --task-id "<taskId>" --status-name "待验收" --yes

# 修复并验证完成后，推进到“待验收”或待测试/待确认等近义状态
python scripts/teambition_bug.py finish --task-id "<taskId>" --verification "写明实际自测/构建/远程验证结果" --yes
```

## 操作规则

- **抢占优先**：从清单中确认要处理某个任务后，**立即**执行 `claim-context --task-id "<taskId>" --status-name "修改中" --yes`。该命令会先尝试把任务推进到修改中/修复中/已认领等处理中状态，并在成功后返回完整上下文。不要先读取完整详情再改状态，读取期间任务可能被其他人认领。
- **抢占必须复核**：`claim-context`、`start`、`update-status` 会发起 Teambition 状态更新请求，检查响应中的业务错误，并在更新后回读任务状态。只有输出中 `verifiedTask.statusId` 等于 `targetStatus.id` 才算状态修改成功；如果命令报错或没有 `verifiedTask`，必须停止处理、如实告知状态未变，不能声称任务已在修改中。
- **看板必须复核**：Teambition 的看板列、任务列表、卡片类型可能不是 `taskflowstatusId`，还可能由 `stageId`、`sfcId`、`tasklistId` 或 `customfields` 决定。用户反馈“还在未开始/未完成/类型乱”时，先运行 `audit-task --task-id "<taskId>"` 读取真实字段；已知道期望值时，在 `start`、`claim-context`、`update-status`、`finish` 上传 `--expect-stage-id`、`--expect-sfc-id`、`--expect-tasklist-id` 或 `--expect-custom-field "字段=值"`。如果审计 `ok=false` 或命令报“卡片面板复核失败”，不能声称已拖到目标列或类型已修正。
- 如果只是判断任务是否归自己、是否需求明确，可以先用 `search/get/context` 做只读检查；一旦决定要开始修，就必须先 `claim-context` 或 `start` 抢占状态。抢占失败时不要继续改业务代码，先以真实 API 错误和回读结果为准说明原因；不要把本地推断的工作流字段当成最终结论。
- 修改状态、执行人、优先级、截止时间或留言前，先读取任务详情确认目标任务。
- 用户只给产品/项目链接时，先用 `parse-url` 解析 `projectId`，后续项目级命令都显式传 `--project-id <projectId>`；`tasks/view/<id>` 是视图 ID，不当作任务 ID。
- 如果项目级命令缺少 `--project-id`，引导用户复制 Teambition 产品/项目分享链接给 AI，让 AI 从链接里的 `/project/<id>` 提取产品 ID 后重试。
- 任务列表必须按紧急程度从高到低处理；优先看任务 `priority`、优先级名称、截止时间、标题/备注中的紧急关键词，再决定顺序。
- 只读取和处理第一执行者为自己的任务。任务列表必须先按 `/users/me` 返回的当前 `userId` 过滤；单任务读取、留言、改状态或更新字段前，也必须确认第一执行者等于当前 `userId`。
- 如果无法确认任务第一执行者，或第一执行者不是自己，跳过该任务，不读取详情、不留言、不修改，避免与他人争抢。
- 读取 bug 清单或上下文时，截图是判断 bug 原因的重要证据，不能只看文字。`context/get --with-rich-text` 会按官方 `GET /v3/task/rtf/render` 自动渲染 `taskId:note`、`taskId:trace:<traceId>` 和可识别的 `taskId:cf:<cfId>`，从 `rtfValueToken.attachments` 提取真实图片/附件下载链接。
- 对可访问截图，先运行 `download-images --task-id <taskId>` 下载，再用可用的视觉工具查看本地图片内容，并把截图里看到的页面、报错、异常状态纳入 bug 判断；OSS 图片直链不能带 OpenAPI 的 `Authorization` 头，脚本已自动区分 API 请求和图片下载。
- 如果 `context` 仍然只有 `[图片]` 占位但没有 `mediaResources.images`，再留言请用户补充可访问截图或把截图中的关键信息转成文字。
- 单个 bug 需求不明确时，必须先问清楚“如何复现”，再用 `ask`、`comment` 或 `quick-reply --template need-info` 留言追问；至少追问页面入口、具体操作步骤、账号/数据/环境、期望结果、实际结果或报错，不要猜测修改，也不要一直等待这个任务；把它记为“待回复”，继续处理下一个明确任务。
- 每完成一个明确任务后，从队列开头重新检查之前“待回复”的任务：读取 `activities/comments/context` 判断是否有新回复；如果需求已明确再开始修改，否则可以继续追问并处理后续任务。
- 可以多次留言追问来澄清如何复现、期望结果、实际结果、环境信息、账号/权限、截图或验收标准；复现方式不清楚或需求明确前千万不要乱改。
- “修改中”不是固定 ID，必须先调用状态列表并按名称或语义匹配；这里的状态包含产品工作流里的状态/标签状态。
- 进入处理状态时优先匹配“修改中”，如果没有，选择“修复中”“处理中”“进行中”“开发中”“已认领”“已领取”“已接收”等可表示正在处理的近义状态；不要把“待验收”“已完成”“关闭”等终态当作处理中。
- 明确修复完成并完成必要验证后，必须执行 `finish --verification "<实际验证结果>" --yes` 推进到目标状态，默认“待验收”；如果没有精确状态，匹配“待验证”“待测试”“待确认”“待审核”“验收中”“提测”等表示等待验收/确认的近义状态。`finish` 不允许省略验证结果，也不能推进到“已完成/关闭”等终态。
- 不要把“已完成”“关闭”“已解决”“上线”等终态当作待验收。除非用户明确要求直接关闭，否则修完后只推进到待验收类状态，让产品/测试能看见并验收。
- 官方公开文档未提供单独“回复某条评论”的任务接口；`reply` 会引用动态/评论 ID 并创建一条新的任务评论。
- 疑问 bug 优先留言追问，不擅自推进状态；疑问通常包括不知道如何复现、缺少具体步骤、期望结果、实际结果、环境信息或截图无法访问。
- 回复必须简单明了，默认写给策划、测试、运营等非技术人员看：先说结论或当前状态，再说需要对方补充什么；少用技术术语，不贴长日志，不展开实现细节。必须提技术原因时，用一句业务化解释。
- 删除、批量替换、移动到不可逆状态等破坏性操作必须获得用户明确授权。
- 个人 token 失效或权限不足时，让用户重新登录 Teambition 后刷新 token，或确认该账号是否已加入对应企业和项目。

## API 参考

需要接口细节时读取 `references/api.md`。脚本封装了常用路径，但 Teambition API 可能更新，遇到字段不匹配时先查官方文档再调整脚本。
