# Repo Ref
- source: https://github.com/nuwax-ai/nuwax-backend (path: skills/nuwax-agent-task/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 当用户要「让某个子智能体去做一件事」或查看/管理已派发的子任务时使用：派发新任务（★触发真实模型执行，产生费用与副作用）、续聊已有任务、现在有哪些任务在跑、按主题搜历史任务（含已结束的）、查某个任务的进度、拿已完成任务的最终结果、取消一个还在执行的任务。用户没指明派给哪个智能体时，目标缺省取环境变量 AGENT_ID（= 本沙箱智能体），即默认派给自己，无需追问目标。可见范围恒为当前凭据（SAND
