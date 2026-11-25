# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: other/speculators-response-regen-ascend-msagent/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 重采样：把已有多轮对话数据的每条 assistant 回答丢弃，用 verifier 模型/vLLM 服务逐轮重生成，产出可直接进训练的预分词样本（每行含 input_ids/loss_mask）。依赖支持 return_token_ids 的 OpenAI 兼容 chat 服务（服务需由用户提前就绪，本技能不负责拉起服务）。触发：用某模型对某个数据集做重采样/重生成（如“对这个数据集用这个模型做
