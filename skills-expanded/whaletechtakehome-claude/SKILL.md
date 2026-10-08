# CLAUDE.md — 园区访客语音登记 Agent

## 这是什么
一个语音门卫 agent。来电者打进来，在自然对话中采集 车牌号 / 来访单位 / 手机号 / 来访事由，把结构化登记推送到企业微信群（代表保安）。从接通到推送必须在 25 秒内。面向中国部署，开源。

## 不可逾越的约束
- 从接通（agent 开始说话）到企微消息发出，必须低于 25 秒。每轮延迟和总耗时都要打日志。
- 对话要像真人门卫。一句话里能抽多个字段就一起抽，不要逐字段一问一答。
- 车牌号和手机号必须复述确认后再入库和推送。ASR 会听错（实测把"蓝色鲸鱼"听成"蓝色金鱼"）。
- 全栈国产，实时音频不出境。STT / TTS / LLM 都走阿里云百炼，共用同一把 DASHSCOPE_API_KEY。
- 任何密钥不进仓库。用 .env + pydantic-settings，仓库里只提交 .env.example。
- commit 由人手动做。你（agent）不要自动 commit。

## 锁定技术栈（不要替换）
- 语言 Python，包管理 uv。
- 编排 Pipecat（自托管）。VAD 和打断用它内置的 Silero VAD。
- STT：百炼 Paraformer 实时语音识别（或 Fun-ASR 实时），WebSocket，DASHSCOPE_API_KEY 在握手头里鉴权。需要自写一层 Pipecat STT service。注意采样率，通话音频常是 8k，选对应版本。
- LLM：Qwen，对话轮用 qwen-plus 或 qwen-turbo。走 OpenAI 兼容端点，base_url 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`，直接用 Pipecat 的 OpenAI 兼容 LLM service，不用自写。必开 streaming。
- TTS：百炼 CosyVoice，用 cosyvoice-v3-flash 走低延迟，WebSocket，同一把 key。需要自写一层 Pipecat TTS service。DashScope 的 Python SDK 已经封好了 WebSocket 和鉴权，直接用，别手搓 ws。可参考阿里官方示例仓库 alibabacloud-bailian-speech-demo。
- 音频入口：Pipecat LocalAudioTransport + 虚拟声卡（Mac 用 BlackHole）。
- 数据库：本地 PostgreSQL，docker-compose 起。访问用 asyncpg 或 SQLAlchemy（async）。
- 推送：企业微信群机器人 webhook，httpx 发 POST。
- 后端：FastAPI，与 Pipecat 同语言同进程、异步。承载企微推送和（延后的）查询端点。

## 明确不要做
- 不要用 VAPI / Retell / Twilio / Supabase / 个人微信自动化。
- 不要实现真 PSTN 接入。那是生产项，文档说明即可。
- 不要加前端看板。
- 不要现在做加分项（查询 agent / 回访识别 / 多路并发）。核心闭环跑通且有富余时间再说。

## Agent 行为（对话逻辑）
- 工具：`submit_registration(plate, company, phone, reason)`；`lookup_visitor(plate)`（回访用，延后实现）。
- 四个字段采齐、且车牌与手机号复述确认通过后，调 `submit_registration`，写库并推企微。
- 守住话题，不被诱导去做范围外的事。放行动作不在 agent 手里，agent 只负责采集和通知保安。

## 构建顺序
见 PROJECT.md。一阶段一阶段来，每阶段可独立测试、人工 commit。第一阶段先把"麦克风 → STT → Qwen → TTS → 扬声器 + 推送"的最小闭环跑通，再挂别的来电源，再打磨对话和 harness。

## 日志与证据
用结构化日志记录每轮的 STT / LLM / TTS 延迟，以及"接通到推送"的总耗时，作为 25 秒达标的证据。
