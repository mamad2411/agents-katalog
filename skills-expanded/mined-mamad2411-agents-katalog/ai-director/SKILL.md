---
name: ai-director
description: AI短剧生成全流程：账号管理、编剧、视频生产。集成X2C计费系统，适用于商业化部署。包含 ad-account-manager（账号管理）、ad-writer（编剧提示词）、ad-producer（视频生产）三大模块。
---

# AI Director - AI短剧生成全流程

完整的AI短剧生成解决方案，从创意到成片，集成X2C平台账号管理和计费。

---

## 👥 多用户支持

本Skill支持多用户共享设备，每个用户拥有独立的X2C账号和配置。

**用户凭证存储位置:** `credentials/{USER_ID}.json`

调用脚本时需设置 `USER_ID` 或 `TELEGRAM_USER_ID` 环境变量：

```bash
USER_ID=5470522468 node scripts/ad-account-manager.js check-binding
```

OpenClaw从聊天调用时会自动传递用户ID。

---

## 🎯 模块概览

### 1. Ad Account Manager（账号管理）
- **功能**: X2C平台账号绑定、验证
- **脚本**: `scripts/ad-account-manager.js`
- **独立使用**: ✅ 可以单独调用

### 2. Ad Writer（编剧）
- **功能**: 从创意点子生成完整短剧脚本
- **类型**: 提示词工程（Agent 读取指南后生成）
- **文档**: `references/AD-WRITER-GUIDE.md`
- **依赖**: ⚠️ 需要先绑定X2C账号

### 3. Ad Producer（视频生产）
- **功能**: 从剧本生成完整视频
- **脚本**: `scripts/ad-producer.js`
- **依赖**: ⚠️ 需要先绑定X2C账号

---

## 🚀 快速开始

### 第一步：获取X2C API Key

**用户必须自行完成以下步骤：**

1. 打开 https://www.x2creel.ai 注册/登录账号
2. 进入个人中心 → API管理 → 创建/复制 API Key
3. 将 API Key 发送给我

**示例对话：**
```
用户：我想生成视频
助手：好的，需要先绑定X2C账号。请打开 https://www.x2creel.ai 登录，然后在个人中心获取API Key发给我。
用户：x2c_sk_xxx...
助手：验证通过！你的账号已绑定，现在可以开始生成视频了～
```

### 第二步：验证API Key（Agent自动执行）

Agent 收到 API Key 后，调用 `ad-account-manager.js verify-key` 验证有效性：

```bash
node scripts/ad-account-manager.js verify-key x2c_sk_xxx
```

验证成功后将 key 保存到 `credentials/{USER_ID}.json`

### 第三步：查看配置和定价

```bash
node scripts/ad-producer.js config
```

### 第四步：生成短剧

**选项A - 仅编剧（Agent模式）：**
Agent 读取 `references/AD-WRITER-GUIDE.md`，根据用户创意生成剧本。

**选项B - 全流程（剧本 + 视频）：**
```bash
node scripts/ad-producer.js full-workflow "一个程序员穿越到古代当宰相" --duration 120 --wait
```

---

## ⚠️ 重要规则

**在用户提供有效的 X2C API Key 之前，禁止执行任何视频生成或剧本生成操作！**

如果用户要求生成视频但尚未绑定账号：
1. 引导用户访问 https://www.x2creel.ai
2. 告知获取API Key的步骤
3. 收到有效Key后才可进入制作流程

---

## 📦 Ad Account Manager（账号管理）

### 命令列表

```bash
# 发送验证码
node scripts/ad-account-manager.js send-code user@example.com

# 验证并获取 API Key
node scripts/ad-account-manager.js verify user@example.com 123456

# 检查绑定状态
node scripts/ad-account-manager.js check-binding

# 查看配置选项
node scripts/ad-account-manager.js config

# 解绑账号
node scripts/ad-account-manager.js unbind

# 帮助
node scripts/ad-account-manager.js help
```

### 直接绑定（如果已有 API Key）

```bash
node scripts/ad-account-manager.js bind --key "x2c_sk_<REDACTED>xxx"
```

---

## 🎭 Ad Character Manager（角色管理）

管理自定义角色，可在视频制作中用作主角。制作时系统会根据性别自动匹配角色与剧本中的人物。

**注意：** 每个用户最多 5 个角色。

### 命令列表

```bash
# 查询角色列表
node scripts/ad-character-manager.js list

# 创建角色
node scripts/ad-character-manager.js create <name> <gender> <image_url>

# 删除角色
node scripts/ad-character-manager.js delete <character_id>

# 帮助
node scripts/ad-character-manager.js help
```

### 参数说明

| 参数 | 说明 | 必填 | 选项 |
|-----|------|:----:|------|
| name | 角色显示名称 | ✅ | - |
| gender | 性别 | ✅ | male, female, other |
| image_url | 角色图片的公开 URL（最大 10MB） | ✅ | - |

### 使用示例

```bash
# 查看当前角色
node scripts/ad-character-manager.js list

# 创建女性角色
node scripts/ad-character-manager.js create Alice female https://example.com/alice.png

# 创建男性角色
node scripts/ad-character-manager.js create Bob male https://example.com/bob.png

# 删除角色
node scripts/ad-character-manager.js delete <uuid>
```

### API 接口

| Action | 说明 |
|--------|------|
| character/list | 查询角色列表 |
| character/create | 创建角色 |
| character/delete | 删除角色 |

---

## ✍️ Ad Writer（编剧）

**这是提示词工程模块**，AI Agent 读取指南后自己生成剧本。

### 功能特性

- **斯皮尔伯格风格**: 温情人性、视觉诗意、情感共鸣
- **三线并行**: 当下故事线、前史线、反派/外因线
- **工业化流程**: 严格遵循短剧市场物理生产限制
- **完整剧本结构**: 剧名、梗概、人物小传、大纲、分集、正集

### 使用方式

**Agent 工作流程：**
1. 读取 `references/AD-WRITER-GUIDE.md`（完整编剧指南）
2. 根据用户创意，按指南生成剧本
3. 输出六部分完整剧本

**用户指令示例：**
```
帮我写一个短剧剧本：一个程序员意外拯救了CEO，却不知道对方的真实身份
```

### 输出内容

1. **剧名**
2. **一句话梗概**
3. **人物小传**
4. **故事大纲**
5. **分集概况（1-30集）**
6. **剧本正集（完整台词和镜头描述）**

---

## 🎬 Ad Producer（视频生产）

### 命令列表

```bash
# 查看配置和定价
node scripts/ad-producer.js config

# 生成剧本
node scripts/ad-producer.js generate-script "你的创意" --wait

# 查询剧本状态
node scripts/ad-producer.js script-status <project_id>

# 生产视频
node scripts/ad-producer.js produce-video <project_id> 1 --wait

# 查询视频进度
node scripts/ad-producer.js video-status <project_id> 1

# 全流程（推荐）
node scripts/ad-producer.js full-workflow "创意描述" --duration 120
```

### 生成选项

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| --mode | short_video / short_drama | short_video |
| --duration | 60 / 120 / 180 / 300 | 120 |
| --ratio | 9:16 / 16:9 | 9:16 |
| --style | 风格名称 | - |
| --episodes | 集数（固定值，不可用户自定义） | short_video=1, short_drama=10 |
| --language | zh / en | zh |
| --character-ids | 角色UUID数组（逗号分隔），用作主角 | - |
| --wait | 等待完成 | false |

### 成本

| 项目 | 积分 | 美元 |
|-----|------|-----|
| 剧本（short_video） | 10 | $0.1|
| 剧本（short_drama） | 100 | $1 |
| 视频 60s | 299 | $2.99 |
| 视频 120s | 599 | $5.99 |
| 视频 180s | 799 | $7.99 |
| 视频 300s | 999 | $9.99 |

---

## 🔄 完整工作流程

### 方案A：分步执行

```bash
# 1. 绑定账号（首次使用）
node scripts/ad-account-manager.js send-code your@email.com
node scripts/ad-account-manager.js verify your@email.com 123456

# 2. 查看定价
node scripts/ad-producer.js config

# 3. 生成剧本
node scripts/ad-producer.js generate-script "一个程序员穿越古代" --wait
# → 获得 project_id

# 4. 生产视频
node scripts/ad-producer.js produce-video <project_id> 1 --wait
```

### 方案B：一键自动化

```bash
node scripts/ad-producer.js full-workflow "一个程序员穿越到古代当宰相" \
  --mode short_video \
  --duration 120 \
  --ratio 9:16
```

---

## ⚙️ 配置文件

`config.json`:
```json
{
  "x2cApiKey": "x2c_sk_<REDACTED>your_api_key_here",
  "x2cEmail": "your@email.com",
  "x2cUserId": "user-uuid"
}
```

---

## 🛡️ 安全与隐私

- API keys 存储在本地 `config.json`
- 显示时自动脱敏
- 所有API调用使用 HTTPS

---

## 🔧 故障排查

### 账号未绑定

```
❌ X2C Account Not Bound
```

**解决方案:**
```bash
node scripts/ad-account-manager.js send-code your@email.com
node scripts/ad-account-manager.js verify your@email.com <code>
```

### 积分不足

```
❌ Error: Insufficient credits
```

**解决方案:**
访问 https://x2creel.ai 充值

### API Key 无效

```
❌ Error: Invalid or missing API key
```

**解决方案:**
```bash
node scripts/ad-account-manager.js unbind
node scripts/ad-account-manager.js send-code your@email.com
```

---

## 📊 X2C Open API

Base URL: `https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api`

### 接口列表

| Action | 说明 |
|--------|------|
| auth/send-code | 发送验证码 |
| auth/verify | 验证获取 API Key |
| config/get-options | 获取配置选项 |
| character/list | 查询角色列表 |
| character/create | 创建角色 |
| character/delete | 删除角色 |
| script/generate | 生成剧本 |
| script/query | 查询剧本状态 |
| video/produce | 生产视频 |
| video/query | 查询视频进度 |

详细 API 文档见 `references/X2C-OPEN-API.md`

---

## 📚 文档参考

- **编剧指南**: `references/AD-WRITER-GUIDE.md`
- **剧本示例**: `references/example.md`
- **X2C API**: `references/X2C-OPEN-API.md`

---

## 🎓 最佳实践

### 成本优化

1. **先用 short_video 测试**
   - 60s 视频成本低（299 积分）
   - 确认风格满意后再做长视频

2. **选择合适的时长**
   - 60s: 简短宣传片
   - 120s: 标准短剧（推荐）
   - 180s-300s: 完整剧情

### 提高成功率

1. **创意要清晰具体**
   - 明确主角、背景、冲突
   - 避免过于抽象的描述

2. **选择合适的风格**
   - 用 `config` 命令查看可用风格
   - 3D古风、现代都市等

---

**适用场景：** 商业化部署、付费短剧生成服务、B端创作工具

---

## 🔍 Quality Evaluator（质量评估）

使用 Gemini 2.0 Flash 分析视频质量，按标准打分。

### 评估维度

**维度一：单片段质量 (100分)**
| 指标 | 权重 | 说明 |
|-----|------|-----|
| 时空一致性 | 35% | 主体特征在镜头内保持稳定 |
| 动态动力学 | 30% | 运动符合物理规律，无跳帧 |
| 视觉纯净度 | 20% | 纹理清晰，无 AI 噪点 |
| 光影交互 | 15% | 阴影随物体运动同步变化 |

**维度二：合成视频质量 (100分)**
| 指标 | 权重 | 说明 |
|-----|------|-----|
| 视觉流一致性 | 30% | 镜头间色调匹配 |
| 剪辑节奏感 | 25% | 转场自然，匹配 BGM |
| 叙事匹配度 | 25% | 准确传达剧本剧情 |
| 音画同步率 | 20% | 音效与视觉契合 |

### 使用方式

```bash
# 评估单个视频
node scripts/quality-evaluator.js <video_url> --prompt "原始提示词"

# JSON 输出
node scripts/quality-evaluator.js <video_url> --json
```

### 输出示例

```json
{
  "total_score": 75,
  "pass": false,
  "issues": ["人物面部不一致", "光影不自然"],
  "suggestions": ["简化角色描述", "明确光源方向"],
  "prompt_improvements": "改进后的提示词..."
}
```

---

## 🔄 Auto-Iterate（自动迭代）

自动评估 + 改进提示词 + 重新生成，直到质量达标。

### 规则

- **及格线:** 80 分
- **最大迭代:** 5 次
- 每次迭代：生成 → 评估 → 如果不及格则改进提示词重试

### 使用方式

```bash
node scripts/auto-iterate.js "你的创意" \
  --duration 60 \
  --style "吉卜力" \
  --threshold 80 \
  --max-iterations 5
```

### 配置要求

`config.json` 需要包含：
```json
{
  "x2cApiKey": "x2c_sk_<REDACTED>xxx",
  "geminiApiKey": "your_gemini_api_key"
}
```

---

**适用场景：** 商业化部署、付费短剧生成服务、B端创作工具

---

## 📋 用户参数确认格式（强制）

当用户要求创建视频时，**必须用文字让用户直接回复选项来确认参数**。**必须等用户确认全部参数后才能开始生成**：

```
📋 参数确认

请回复你的选择：

🎬 模式：短剧(10集) 或 短视频(1集)

⏱️ 时长/价格：60秒/299、120秒/599、180秒/799、300秒/999

📐 比例：竖屏(9:16) 或 横屏(16:9)

🎨 风格：3D古风 / 2D漫剧 / 吉卜力 / 皮克斯 / 写实 / 二次元 / 国风水墨

📂 分类：玄幻 / 悬疑 / 科幻 / 都市 / 热门 / 霸总 / 仙侠

例如：「短剧、180秒、竖屏、3D古风、仙侠」

**语言**: 中文 / English

## ⚡ 异步任务处理（重要！）

当用户要求生成视频时，必须使用**异步方式**，不要等待完成！

### 流程：

1. **启动任务，不等待**
```bash
# 启动视频生成，返回project_id
USER_ID=$USER_ID node scripts/ad-producer.js full-workflow "主题" --mode short_video --duration 60 --style "风格" --language zh
```

2. **添加任务到跟踪列表**（必须！）
```bash
# 视频开始生成后，立即调用：
/opt/storyclaw/add-video-task.sh "$USER_ID" "$project_id" "$CHAT_ID"
# 参数: user_id, project_id, chat_id (Telegram用户ID)
```

3. **完成后自动通知**
- cron job每2分钟检查一次 /tmp/active-video-tasks.json
- 完成后自动发送消息通知用户

### 关键点：
- **不要用 --wait 参数**，会阻塞
- 启动任务后立即返回"正在生成，稍等"
- **必须调用 add-video-task.sh 添加任务到跟踪列表**
- 创建cron job监控进度
- 完成后通过对应渠道通知用户

用户创建短剧时，以下5个参数**只能从配置选项中选取**，不允许自定义值：

1. **模式**: `short_video` 或 `short_drama`
2. **时长**: `60` / `120` / `180` / `300`
3. **比例**: `9:16` 或 `16:9`
4. **风格**: `3D古风` / `2D漫剧` / `吉卜力` / `皮克斯` / `写实风格` / `二次元` / `国风水墨`
5. **分类**:
   - 中文: `玄幻异能` / `悬疑惊悚` / `科幻末世` / `都市复仇` / `热门综合` / `霸总甜宠` / `仙侠古装`
   - 英文: `Werewolf & Shifter` / `Suspense & Horror` / `Power & Revenge` / `Sweet & CEO` / `Magic & Fantasy` / `AI Drama Lab`

**如果用户提供的任何一项不在配置列表中，必须提示用户从列表中重新选择，不得自行替换或忽略。**

**集数规则（强制）：**
- `short_video` → 固定1集，不询问用户
- `short_drama` → 固定10集，不询问用户
- **不允许用户自定义集数**，引导流程中不展示集数选项

## 🎬 视频生产流程（强制）

### 重要规则：同一集只能发起一次制作

**每个episode只能提交一次 `produce-video` 命令！**
- ✅ 可以多次查询 `video-status`
- ❌ 不能重复提交 `produce-video`

如果任务失败，等待第三方系统修复，不要重复提交。

### short_video (1集)
```
1. 生成剧本
2. 视频生成 → 完成后通知用户
```

### short_drama (10集) - 必须逐集生产
```
1. 生成剧本 (10集)
2. 等待剧本完成
3. EP1 视频生成 → 等待完成
4. EP2 视频生成 → 等待完成
5. EP3 视频生成 → 等待完成
...
10. EP10 视频生成 → 等待完成
11. 全部完成 → 通知用户
```

**关键点：**
- **必须等上一集完成后再开始下一集**，不能并行
- 每集生成完成后记录状态
- 全部10集完成后统一通知用户

调用 `config/get-options` API可获取最新配置列表（风格和分类可能会更新）。

## ⚠️ Agent 输出规范

1. **链接必须完整输出**，不得截断（视频 URL 带签名很长，但必须完整）
2. 使用代码块 ``` 包裹长链接，避免被聊天软件截断
3. 关键信息（Project ID、Video URL）必须清晰展示

## 📢 视频完成通知规则

**短剧(10集)模式下，当前集完成后必须询问用户是否继续制作下一集！**

当一集视频生成完成后：
1. 展示视频链接
2. 展示本集积分消耗
3. **询问用户是否继续制作下一集**

示例回复：
```
🎉 视频生成完成！

📊 积分消耗：599积分

继续制作下一集吗？
- 是，继续EP3
- 暂时停止
```

**注意：**
- short_video (1集) 无需询问
- 短剧模式必须询问
- 用户选择"是"后，再发起下一集的制作

## ⚠️ 视频失败处理规则

**视频生成失败后，禁止自动重试生成！**

原因：每次生成都会扣除用户积分，自动重试会导致额外扣费。

处理流程：
1. 查询失败原因（通过 `video-status` 命令查看 status 和 progress）
2. 将失败原因告知用户
3. 等待用户指示是否重试或调整参数

示例回复：
```
❌ 视频生成失败
原因: 人物生成失败 (character step failed at 14%)
当前余额: 20,013 积分

请选择：
- 重试生成（将从余额中扣除相应积分）
- 更换风格/参数后重试
- 取消任务
```

## 🔄 多集短剧生产规则（short_drama）

**视频必须逐集生产，不能同时启动多集。** 流程：
1. 生成剧本时必须传 `total_episodes` 参数（如 `"total_episodes": 10`），否则只会生成1集
2. 调用 `video/produce` 启动第1集视频制作
3. 轮询第1集状态，等待完成
4. 第1集完成后，调用 `video/produce` 启动第2集
5. 重复直到所有集完成
6. 每集完成后通知用户进度（如 "EP3/10 完成"）
7. 全部完成后发送总积分报告

## 🎬 视频播放优化

CDN返回的视频URL末尾带有 `&response-content-disposition=attachment`，会导致浏览器强制下载而非播放。

**规则：拿到视频URL后，必须去掉 `&response-content-disposition=attachment` 参数，然后可以直接在浏览器中播放，无需下载到本地。**

流程：
1. 获取视频URL（从 `video-status` 命令）
2. 去掉 `&response-content-disposition=attachment`
3. 直接 `browser navigate` 到清理后的URL → 即可播放
4. **询问用户是否需要下载视频**（默认不下载，只播放）
5. 如用户要下载/发送到Telegram：下载+压缩到16MB以下（480p, crf 32）再发送

---

## 📱 WebChat 消息推送

WebChat 是 StoryClaw 设备的网页聊天渠道，通过 `webchat-stream-ws.sh` 脚本推送消息。

### 脚本位置
```
/opt/storyclaw/webchat-stream-ws.sh
```

### 使用方法

```bash
# 发送新消息（INSERT 模式）
webchat-stream-ws.sh <user_id> --file <message_file> <agent_id>

# 更新现有消息（UPDATE 模式）
webchat-stream-ws.sh <user_id> --update <message_id> --file <message_file> <agent_id>
```

### 参数说明

| 参数 | 说明 |
|------|------|
| user_id | WebChat 用户 ID（32位hex） |
| message_id | 已有消息的 ID，用于更新 |
| message_file | 包含消息内容的文件路径（**必须用 --file 传递，避免 $ 符号丢失**） |
| agent_id | 目标 agent ID（如 `director`） |

### 示例

```bash
# 1. 发送确认消息并获取 message_id
echo "正在生成视频..." > /tmp/msg.txt
MSG_ID=$(webchat-stream-ws.sh "180d08e23cdac976b4" --file /tmp/msg.txt "director")
echo "Message ID: $MSG_ID"

# 2. 任务完成后更新消息
echo "✅ 视频生成完成！" > /tmp/result.txt
webchat-stream-ws.sh "180d08e23cdac976b4" --update "$MSG_ID" --file /tmp/result.txt "director"
```

### 注意事项

1. **必须使用 --file 模式** — 直接传文本会导致 `$` 符号丢失
2. **message_id 用于原地更新** — 避免产生多条消息
3. **异步任务配合** — 视频生成等长时间任务，先发送"处理中"消息，任务完成后再 update

### 视频任务进度推送

使用 `add-video-task.sh` 添加任务时，chat_id 格式决定通知渠道：

```bash
# WebChat 推送（chat_id 格式：webchat:<user_id>:<agent_id>）
add-video-task.sh "180d08e23cdac976b4" "project-id" "webchat:180d08e23cdac976b4:director"

# Telegram 推送（chat_id 为纯数字）
add-video-task.sh "5470522468" "project-id" "5470522468"
```

`check-video-tasks.sh` 会每2分钟检查任务状态，根据 chat_id 格式自动选择推送渠道。

---

**版本：** 2.1.2 (X2C Open API + WebChat 推送支持)
