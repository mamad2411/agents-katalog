# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/s/senseaudio-let-claw-talk/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当用户希望把 AudioClaw 变成一个持续监听、开口就说、停顿就回答的本机语音助手时使用。这个 skill 会在 macOS 上启动常驻监听流程，默认优先使用内置 Swift 录音器减少 Python 音频依赖；用户语音通过 SenseAudio ASR 转文字，再发给 audioclaw agent，并用 SenseAudio TTS 或系统 say 读回结果。它保留可选的 WeSpeake
