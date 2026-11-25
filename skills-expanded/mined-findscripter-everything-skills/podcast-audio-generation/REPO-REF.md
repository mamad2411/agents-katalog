# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 06-creative/podcast-audio-generation/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当需要把文本/文稿转成自然口播的播客音频时使用；经 Azure OpenAI Realtime API（gpt-realtime-mini）走 WebSocket 流式收 PCM 音频+逐字稿，转 WAV 并 base64 回传前端播放；不适用于无 Azure 凭据、要求精确逐字音色克隆或长篇离线批量 TTS 的场景，后者回退专用 TTS；触发词：文本转语音播客、文稿配音、Realtime 语音合
