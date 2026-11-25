---
name: telephony
description: Provision Twilio numbers, SMS/MMS, and AI outbound calls.
version: 1.0.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [telephony, phone, sms, mms, voice, twilio, bland.ai, vapi, calling, texting]
    related_skills: [maps, google-workspace, agentmail]
    category: productivity
---

# 电话功能——无需修改核心工具即可实现号码、通话与短信功能

这项可选技能为Hermes带来了实用的电话功能，同时不会将电话相关功能纳入核心工具列表中。

它附带了一个辅助脚本 `scripts/telephony.py`，可用于：
- 将服务提供商的凭证保存到 `${HERMES_HOME:-~/.hermes}/.env` 文件中
- 搜索并购买Twilio电话号码
- 记住已拥有的号码以便后续会话使用
- 从该号码发送短信/MMS
- 无需Webhook服务器即可轮询该号码的来电短信
- 使用TwiML中的 `<Say>` 或 `<Play>` 标签直接拨打Twilio电话
- 将已拥有的Twilio号码导入Vapi系统
- 通过Bland.ai或Vapi发起外呼AI通话

## 解决的问题

该技能旨在满足用户实际需要的各类电话功能：
- 外拨通话
- 发送短信
- 拥有一个可重复使用的智能体号码
- 查看随后发送到该号码的消息
- 在不同会话之间保留该号码及相关标识信息
- 为未来接收来电短信及其他自动化操作提供完善的电话身份管理

需要注意的是，它**不会**将Hermes转变为真正的实时来电电话网关。来电短信功能是通过轮询Twilio REST API来实现的。对于许多工作流而言，这已经足够满足需求，比如发送通知或获取一次性验证码，且无需额外搭建核心Webhook基础设施。

## 安全规则——必须遵守

1. 在拨打电话或发送短信之前，请务必先进行确认。  
2. 绝对不要拨打紧急电话号码。  
3. 禁止利用电话功能进行骚扰、发送垃圾信息、冒充他人或从事任何非法行为。  
4. 应将第三方电话号码视为敏感的操作数据：  
   - 不要将其保存在Hermes的内存中；  
   - 除非用户明确要求，否则不得将其包含在技能文档、总结或后续记录中。  
5. 可以保留**由智能体拥有的Twilio号码**，因为该号码属于用户的配置部分。  
6. VoIP号码**无法保证**适用于所有第三方双重认证流程。请谨慎使用，并向用户明确说明相关限制。  

## 决策树——应选择哪种服务？  
建议采用以下逻辑而非固定的服务路由方式：  

### 1) “我希望Hermes拥有一个真实的电话号码”  
请选择**Twilio**。  
原因：  
- 购买并保留电话号码的最简便途径；  
- SMS/MMS支持最为完善；  
- 接收来电的短信轮询机制最为简单；  
- 未来过渡到接收Webhook或处理来电的路径最为清晰。  
适用场景：  
- 后续接收短信；  
- 发送部署警报或定时通知；  
- 为智能体维护一个可重复使用的电话身份；  
- 日后尝试基于电话的认证流程。  

### 2) “目前我只需要最简单的向外发起的人工智能电话通话功能”  
请选择**Bland.ai**。  
原因：  
- 设置速度最快；  
- 仅需一个API密钥；  
- 无需自行购买或导入电话号码。  
缺点：  
- 灵活性较低；  
- 音质尚可，但并非最佳水平。  

### 3) “我追求最佳的对话式人工智能语音质量”  
请选择**Twilio + Vapi**。  
原因：
- Twilio 可为你提供专属电话号码  
- Vapi 能带来更出色的对话式 AI 通话质量，以及更高的语音和模型灵活性  

推荐操作流程：  
1. 购买/保存一个 Twilio 电话号码  
2. 将其导入 Vapi  
3. 保存返回的 `VAPI_PHONE_NUMBER_ID`  
4. 使用命令 `ai-call --provider vapi` 进行通话  

### 4) “我想使用自定义预录语音消息来电”  
此时可使用带有公共音频 URL 的 **Twilio 直接通话** 方式。  

原因：  
- 这是播放自定义 MP3 文件最简单的方法  
- 与 Hermes 的 `text_to_speech` 功能结合，并搭配公共文件托管服务或传输通道，使用效果更佳  

## 文件与持久化状态  

该技能会将电话相关状态存储在两个位置：  

### `${HERMES_HOME:-~/.hermes}/.env`  
用于存储长期有效的服务提供商凭证及专属号码 ID，例如：  
- `TWILIO_ACCOUNT_SID`  
- `TWILIO_AUTH_TOKEN`  
- `TWILIO_PHONE_NUMBER`  
- `TWILIO_PHONE_NUMBER_SID`  
- `BLAND_API_KEY`  
- `VAPI_API_KEY`  
- `VAPI_PHONE_NUMBER_ID`  
- `PHONE_PROVIDER`（AI 通话服务提供商：bland 或 vapi）  

### `~/.hermes/telephony_state.json`  
用于存储仅在技能运行期间有效、但需在多次会话间保留的状态，例如：  
- 已保存的默认 Twilio 电话号码/SID  
- 已保存的 Vapi 电话号码 ID  
- 收件箱轮询检查点所对应的最新来电消息 SID/日期  

这意味着：  
- 下次加载该技能时，`diagnose` 功能便可显示已配置的号码信息  
- `twilio-inbox --since-last --mark-seen` 命令可从上一次的检查点继续处理任务  

## 查找辅助脚本  

安装此技能后，可通过以下方式找到对应脚本：

```bash
SCRIPT="$(find ~/.hermes/skills -path '*/telephony/scripts/telephony.py' -print -quit)"
```

如果 `SCRIPT` 的值为空，说明该技能尚未安装。

## 安装

这是一项官方提供的可选技能，可通过 Skills Hub 进行安装：

```bash
hermes skills search telephony
hermes skills install official/productivity/telephony
```

## 提供商配置

### Twilio — 自有号码、短信/MMS、直接通话、接收短信轮询

注册地址：
- https://www.twilio.com/try-twilio

随后将凭证保存至Hermes中：

```bash
python "$SCRIPT" save-twilio ACXXXXXXXXXXXXXXXXXXXXXXXXXXXX your_auth_token_here
```

搜索可用的号码：

```bash
python "$SCRIPT" twilio-search --country US --area-code 702 --limit 5
```

购买并记住一个号码：

```bash
python "$SCRIPT" twilio-buy "+17025551234" --save-env
```

列出已拥有的号码：

```bash
python "$SCRIPT" twilio-owned
```

稍后可将其中之一设置为默认值：

```bash
python "$SCRIPT" twilio-set-default "+17025551234" --save-env
# or
python "$SCRIPT" twilio-set-default PNXXXXXXXXXXXXXXXXXXXXXXXXXXXX --save-env
```

### Bland.ai — 最简单的外呼人工智能通话解决方案

注册地址：
- https://app.bland.ai

保存配置：

```bash
python "$SCRIPT" save-bland your_bland_api_key --voice mason
```

### Vapi — 更出色的对话语音质量

注册地址：
- https://dashboard.vapi.ai

请先保存 API 密钥：

```bash
python "$SCRIPT" save-vapi your_vapi_api_key
```

将您拥有的 Twilio 号码导入 Vapi，并保存返回的电话号码 ID：

```bash
python "$SCRIPT" vapi-import-twilio --save-env
```

如果您已经知道 Vapi 电话号码的编号，可直接将其保存：

```bash
python "$SCRIPT" save-vapi your_vapi_api_key --phone-number-id vapi_phone_number_id_here
```

## 诊断当前状态

随时查看该智能体已掌握的信息：

```bash
python "$SCRIPT" diagnose
```

在后续会话中恢复工作时，请首先使用此方法。

## 常见工作流程

### A. 购买代理号码并持续使用

1. 保存 Twilio 凭据：
```bash
python "$SCRIPT" save-twilio AC... auth_token_here
```

2. 搜索号码：
```bash
python "$SCRIPT" twilio-search --country US --area-code 702 --limit 10
```

3. 购买后将其保存至 `${HERMES_HOME:-~/.hermes}/.env` 文件中，并设置状态：
```bash
python "$SCRIPT" twilio-buy "+17025551234" --save-env
```

4. 在下一次会话中，运行以下命令：
```bash
python "$SCRIPT" diagnose
```
此处显示了已保存的默认号码以及收件箱检查点状态。

### B. 从智能体号码发送短信

```bash
python "$SCRIPT" twilio-send-sms "+15551230000" "Your deployment completed successfully."
```

支持媒体文件：

```bash
python "$SCRIPT" twilio-send-sms "+15551230000" "Here is the chart." --media-url "https://example.com/chart.png"
```

### C. 无 Webhook 服务器时后续查看接收到的短信

轮询默认的 Twilio 号码的收件箱：

```bash
python "$SCRIPT" twilio-inbox --limit 20
```

仅显示自上一个检查点之后收到的消息，阅读完毕后即可更新检查点。

```bash
python "$SCRIPT" twilio-inbox --since-last --mark-seen
```

这正是针对“如何在技能再次加载时获取该号码接收到的消息？”这一问题的主要解答。

### D. 使用内置文本转语音功能直接发起 Twilio 呼叫

```bash
python "$SCRIPT" twilio-call "+15551230000" --message "Hello! This is Hermes calling with your status update." --voice Polly.Joanna
```

### E. 使用预录/自定义语音消息发起通话

这是复用 Hermes 现有 `text_to_speech` 功能的主要方式。

适用场景包括：
- 您希望通话使用 Hermes 配置好的文本转语音，而非 Twilio 的 `<Say>` 功能
- 您需要单向语音传递（如简报、提醒、笑话、通知或状态更新）
- 您不需要实时对话式电话通话

请先单独生成或托管音频文件，然后：

```bash
python "$SCRIPT" twilio-call "+155****0000" --audio-url "https://example.com/briefing.mp3"
```

推荐的 Hermes TTS -> Twilio Play 工作流程如下：

1. 使用 Hermes 的 `text_to_speech` 功能生成音频文件。
2. 将生成的 MP3 文件设置为可公开访问。
3. 通过 `--audio-url` 参数发起 Twilio 通话。

示例智能体流程：
- 使用 `text_to_speech` 要求 Hermes 生成消息音频。
- 如有需要，可通过临时静态主机、隧道或对象存储地址公开该文件。
- 使用 `twilio-call --audio-url ...` 将音频通过电话传输给对方。

适合存储 MP3 文件的方案包括：
- 临时的公共对象/存储地址
- 连接到本地静态文件服务器的短生命周期隧道
- 电话服务提供商可直接获取的任何现有 HTTPS 地址

重要提示：
- Hermes TTS 非常适用于预录的外呼消息。
- 对于**实时对话式 AI 通话**，Bland/Vapi 是更佳选择，因为它们能够自行处理实时的电话音频处理流程。
- 本文中并未将 Hermes 的 STT/TTS 功能单独用作全双工电话通话引擎；实现此类功能需要比当前技能所涉及的更复杂的流媒体/ webhook 集成。

### F. 使用 Twilio 直接通话功能导航电话树/IVR 系统

如果需要在通话建立后输入数字，可使用 `--send-digits` 参数。
Twilio 会将参数 `w` 解释为短暂等待。

```bash
python "$SCRIPT" twilio-call "+18005551234" --message "Connecting to billing now." --send-digits "ww1w2w3"
```

该功能有助于在将通话转接给人工客服或发送简短状态信息之前，先进入特定的菜单分支。 

### G. 使用 Bland.ai 发起外呼 AI 电话通话

```bash
python "$SCRIPT" ai-call "+15551230000" "Call the dental office, ask for a cleaning appointment on Tuesday afternoon, and if they do not have Tuesday availability, ask for Wednesday or Thursday instead." --provider bland --voice mason --max-duration 3
```

查看状态：

```bash
python "$SCRIPT" ai-status <call_id> --provider bland
```

任务完成后，可提出与Bland分析相关的问题：

```bash
python "$SCRIPT" ai-status <call_id> --provider bland --analyze "Was the appointment confirmed?,What date and time?,Any special instructions?"
```

### H. 使用 Vapi 从您自己的号码发起 AI 外呼电话

1. 将您的 Twilio 号码导入 Vapi：
```bash
python "$SCRIPT" vapi-import-twilio --save-env
```

2. 发起通话：
```bash
python "$SCRIPT" ai-call "+15551230000" "You are calling to make a dinner reservation for two at 7:30 PM. If that is unavailable, ask for the nearest time between 6:30 and 8:30 PM." --provider vapi --max-duration 4
```

3. 查看结果：
```bash
python "$SCRIPT" ai-status <call_id> --provider vapi
```

## 推荐的智能体操作流程

当用户请求拨打电话或发送短信时：

1. 通过决策树确定适合该请求的处理路径。
2. 若配置状态不明确，则运行 `diagnose` 命令进行诊断。
3. 收集完整的任务详情。
4. 在拨打电话或发送短信前向用户确认。
5. 使用正确的命令执行操作。
6. 如有需要，轮询查询操作结果。
7. 概要说明最终结果，同时避免将第三方电话号码存储在 Hermes 内存中。

## 该智能体目前尚不支持的功能

- 实时接听来电
- 基于 webhook 的实时短信推送至智能体处理流程
- 对任意第三方双重认证提供商的全面支持

这些功能需要比普通可选智能体更复杂的基础设施。

## 常见问题与注意事项

- Twilio 的试用账户及地区限制可能会影响可拨打/发送短信的对象。
- 部分服务不接受使用 VoIP 号码进行双重认证。
- `twilio-inbox` 功能是通过轮询 REST API 获取信息的，而非即时推送。
- Vapi 的外呼功能仍依赖于已正确导入的有效号码。
- Bland 生成的语音内容虽然最简单，但音质未必最佳。
- 请勿将任意第三方电话号码存储在 Hermes 内存中。

## 验证清单

完成设置后，仅使用该智能体即可实现以下所有功能：

1. 通过 `diagnose` 命令查看服务提供商的可用状态及已保存的配置信息。
2. 搜索并购买 Twilio 号码。
3. 将该号码保存至 `${HERMES_HOME:-~/.hermes}/.env` 文件中。
4. 使用该号码发送短信。
5. 后续轮询查询该号码接收到的短信。
6. 直接拨打 Twilio 号码。
7. 通过 Bland 或 Vapi 发起人工智能语音通话。

## 参考资料

- Twilio 电话号码相关文档：https://www.twilio.com/docs/phone-numbers/api  
- Twilio 消息服务文档：https://www.twilio.com/docs/messaging/api/message-resource  
- Twilio 语音服务文档：https://www.twilio.com/docs/voice/api/call-resource  
- Vapi 文档：https://docs.vapi.ai/  
- Bland.ai 网站：https://app.bland.ai/
