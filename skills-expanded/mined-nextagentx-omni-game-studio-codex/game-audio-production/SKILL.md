---
name: game-audio-production
description: Generate and integrate game sound effects and music using available AI audio tools or the bundled ElevenLabs adapter; validate loops, formats, provenance, and engine playback. Use when a game needs real sound effects or BGM, when AI audio must be produced and registered, or when audio does not play on a target platform.
---

# 游戏音效与音乐生成

按用户指定的风格、用途和预算制作真实音频。先检查当前会话可用的音频生成工具；可用时直接调用。未提供音频生成工具时，可使用本插件的 ElevenLabs 适配器，或按目标服务官方文档配置用户选择的其他服务。接口能力、价格、授权与地区支持以服务当前官方说明和账户状态为准。

## ElevenLabs 直接生成

`scripts/gen_ai_audio.py` 使用官方 HTTPS API，标准库即可运行。只有用户选择 ElevenLabs API 生成路线时才执行真实请求；它需要在本机配置 `ELEVENLABS_API_KEY`，请求可能计费。不要将密钥写进代码、清单或对话。可先用 `--dry-run` 预览，预览不联网、不需要密钥。脚本一次调用只发一个请求，不自动重试、覆盖文件或虚构授权信息。将 `PL` 设置为插件根目录，或改用脚本绝对路径：

```bash
# --dry-run 只检查请求，不需要密钥，也不会请求网络
python "$PL/scripts/gen_ai_audio.py" sfx --prompt "short soft sci-fi UI confirmation" --duration 1 --out assets/audio/ui_confirm.mp3 --dry-run
python "$PL/scripts/gen_ai_audio.py" sfx --prompt "crystalline pickup chime, bright and concise" --duration 1 --out assets/audio/pickup.mp3
python "$PL/scripts/gen_ai_audio.py" music --prompt "hopeful space exploration, gentle synth, no vocals" --duration 30 --instrumental --out assets/audio/exploration.mp3
```

音效支持 `--loop`、0.5–30 秒；音乐支持 3–600 秒。两者均可用 `--model` 指定账户可用的模型。输出是 MP3；具体模型、格式、价格和可用性以官方文档为准：

- [音效 API](https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert)
- [音乐 API](https://elevenlabs.io/docs/api-reference/music/compose)

如果缺密钥、权限或预算，说明阻塞原因并给出准备步骤；不要把程序合成音当成 AI 生成音。用户接受复古芯片音时可选 `gen_music.py` 和 `gen_sfx.py`，并如实标注为程序合成。

## 验收与接入

1. 为每个事件写明提示词、时长、音色情绪、循环与触发方式；按需要生成少量变体并试听。
2. 检查爆音、静音、裁切、响度、游戏内混音及循环衔接；模型的 loop 参数不等于已验证无缝。按目标平台需要转码或使用引擎导入压缩。
3. 把文件接到对应游戏事件，验证并发、暂停恢复及浏览器音频解锁。确实没有运行条件时，明确未验证。
4. 记录来源、模型、提示词或生成记录、日期与授权依据到资源清单。未经核实不要填 `commercial_ok: true`。使用 `validate_assets.py --final --strict-license` 检查清单；该脚本不检查音频内容或听感。
