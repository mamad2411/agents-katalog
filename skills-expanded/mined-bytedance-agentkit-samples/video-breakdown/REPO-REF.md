# Repo Ref
- source: https://github.com/bytedance/agentkit-samples (path: python/02-use-cases/video_breakdown_agent/.skills/video-breakdown-skill/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: 视频分镜拆解技能（自包含，无需外部后端）。使用 FFmpeg 预处理视频并生成分镜数据。(1) 视频 URL 直接处理 `python scripts/process_video.py "<video_url>"`；(2) 本地文件先上传 `python scripts/video_upload.py "<file_path>"` 获取 URL 后再处理。需要本机安装 FFmpeg。
