# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-NeverSight-learn-skills.dev/verl-async-dapo/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: Verl 单异步 DAPO 训练配置生成器。触发场景：(1) 启动单异步 DAPO 训练 (2) 生成训练脚本 (3) 配置特性参数 (4) 训练前检查。**特性策略**：用户未指定时默认开启性能特性（flash_attn/dynamic_batch/remove_padding/gradient_checkpointing），显存特性（offload/recompute）默认关闭。OOM 时自动
