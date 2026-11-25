# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/d/douyin-video-parser/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 抖音视频解析-把抖音视频链接（v.douyin.com 短链或 douyin.com/video/<id> 长链）转成中文字幕稿和交互式 HTML 报告。原理：多级 fallback 拿 mp4 直链（iesdouyin share API → CDP 浏览器方案 → yt-dlp）-> 下载视频 -> 本地 faster-whisper（base 模型、CPU、int8）转写 -> 本地规则提取
