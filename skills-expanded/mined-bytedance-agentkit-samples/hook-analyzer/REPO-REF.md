# Repo Ref
- source: https://github.com/bytedance/agentkit-samples (path: python/02-use-cases/video_breakdown_agent/.skills/hook-analyzer-skill/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: 视频前三秒钩子分析技能。从分镜拆解结果中提取前三秒分镜数据，为钩子吸引力评估提供结构化上下文。运行脚本 `python scripts/analyze_hook_segments.py "<breakdown_json_file>"` 或通过 stdin 传入 JSON。输出包含前三秒分镜数量、总时长和每个分镜的详细信息（含关键帧 URL）。
