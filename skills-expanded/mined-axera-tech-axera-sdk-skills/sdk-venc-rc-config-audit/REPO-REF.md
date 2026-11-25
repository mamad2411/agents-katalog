# Repo Ref
- source: https://github.com/axera-tech/axera-sdk-skills (path: skills/sdk-venc-rc-config-audit/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 审查 AX615/AX VENC 码控配置和可选码流结构。用户提供 `/proc/ax_proc/venc`、VENC RC 参数、码流文件，或描述呼吸效应、码率偏高/超出、竞品对比、GOP/IP 比例、帧率异常等问题时使用；解析单次 proc，不要求两次采样，并在有码流时调用 ffprobe 分析实际 GOP、I/P/B 帧、帧大小、码率和时间戳，再结合编码模式给出证据、风险和修改建议。用户要求
