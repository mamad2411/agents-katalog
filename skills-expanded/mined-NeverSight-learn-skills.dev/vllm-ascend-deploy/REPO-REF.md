# Repo Ref
- source: https://github.com/NeverSight/learn-skills.dev (path: data/skills-md/ascend/agent-skills/vllm-ascend-deploy/SKILL.md, branch: main)
- mined: 2026-10-14
- desc: 昇腾 NPU 平台 vLLM 大模型推理服务一键部署。触发：用户说'部署 模型名'、'NPU 部署模型'、'vllm serve'。流程：SSH检查 → NPU检查 → 配置发现(必须验证) → 用户确认 → 部署 → cron监控 → 验证。约束：(1) 配置必须从官方文档验证，禁止猜测；(2) 后台启动必须用cron监控，禁止手动轮询。支持 Qwen/Qwen3.5、GLM、DeepSeek、
