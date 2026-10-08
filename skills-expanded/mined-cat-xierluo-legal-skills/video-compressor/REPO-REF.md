# Repo Ref
- source: https://github.com/cat-xierluo/legal-skills (path: skills/video-compressor/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: 视频压缩与静默片段剪切工具。使用 FFmpeg CRF 模式压缩视频，适配屏幕录制/课件场景；支持检测并去除静默静止片段。自动检测硬件与源码率并选择最优编码方案（高码率源走 VideoToolbox 硬件加速，低码率录屏自动改用 x264 CRF 自适应编码）。本技能应在用户需要压缩视频、减小视频大小、去除视频空档时使用。不要用于：视频剪辑、音频提取、格式转换。
