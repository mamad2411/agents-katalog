# Repo Ref
- source: https://github.com/lix19937/tensorrt-plugin-autoresearch (path: .claude/skills/trt-plugin-kernel-latency-auto-opt/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 本技能基于kernel延迟 + NCU 硬件计数器瓶颈诊断，全自动迭代优化 CUDA Kernel，唯一优化目标：最小执行延迟（latency, ms）。严格遵循工程约束：仅允许修改 exp/*.cu 文件，其他文件固定不可改动；自动构建、测速、记录实验日志、择优提交 / 回滚代码，长期后台无人值守运行。
