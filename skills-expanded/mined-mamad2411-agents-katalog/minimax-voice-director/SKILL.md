---
name: minimax-voice-director
description: 用 MiniMax 云端为视频制作可审批的声音导演稿，再生成、挑选和验收人声，最后以定稿音频产生字幕。用于用户明确选择 MiniMax 配音、继续已有 MiniMax 视频配音项目，或明确请求 MiniMax Voice ID/克隆/设计。泛指本地 TTS 或 IndexTTS 不使用本 skill；音乐、BGM、歌曲使用同级 music Skill。
metadata:
  tags: minimax, tts, voice-director, voiceover, subtitles, cloud-api
---

# MiniMax 声音导演

把口播稿变成可审批、可复现、可局部返工的声音表演。不得把本 skill 缩减为“文本进、MP3 出”的单次 TTS 调用。

## 路由边界

- 用户明确选择 MiniMax 配音，或当前项目已经用 MiniMax：进入三阶段主流程。
- 用户只说 TTS、旁白、自己的声音，但没有选 MiniMax：不自动替换引擎，先根据上下文路由到合适的本地或云端工作流。
- 用户要 MiniMax Voice ID、声音克隆、声音设计或旧函数兼容：读 `references/runtime.md`，该分支不自动触发配音主流程。
- 音乐、BGM、歌曲或 cover：改用同级 `music`（ElevenLabs Music API）。
- 不因其他 TTS 失败而静默转用 MiniMax；先说明云端费用、声音差异和数据上传。

## 三阶段主流程

### 1. 先导演，再审批

1. 定义原稿和字幕文本真值，先处理产品名、人名、数字、缩写和多音字。
2. 读 `references/directing.md` 设计全片基线、言语动作、潜台词、情绪弧线、节奏曲线、焦点词、语调和必要的声音事件。
3. 读 `references/schema.md`，从 `assets/voice-direction.template.yaml` 创建 `work/tts/voice-direction.yaml`。平台私有标签不得出现在导演中间层。
4. 运行 `scripts/validate_direction.py` 和 `scripts/compile_direction.py`，产生审查视图、lint、MiniMax manifest 和干净字幕稿。
5. 用独立审查回合检查导演逻辑，重点展示改写、强焦点、强转折、长停顿、声音事件、局部参数和多 Take 段落；通过后运行 `scripts/mark_reviewed.py` 固化审查 hash。
6. **停在这里等待用户批准。** 用户没有明确批准时，不得运行 `approve_direction.py`，不得调用 MiniMax。
7. 用户批准后运行 `scripts/approve_direction.py`，再重新编译。`render_allowed` 必须为 `true`。

### 2. 生成、选 Take，再批准音频

1. 读 `references/workflow.md` 和 `references/runtime.md`，加载项目 `.env.r2`，不输出任何密钥或 Voice ID。
2. 运行 `scripts/render_segments.py`。它必须同时验证人工批准、lint 和内容 hash；任一失效就拒绝云端生成。
3. 正式生成优先使用长连续块：开头约 40 秒一块，后续约 3 分钟一块；时长只是软目标，必须在句号或完整意群结尾切分，绝不从句子中间硬截。每块默认 1 个 Take，局部问题只重生局部。
4. 听审候选并写入 `take-selection.yaml`，然后运行 `scripts/select_takes.py` 和 `scripts/finalize_voice.py`。不得把原始候选或未重建停顿的拼接音频冒充最终成果。
5. 在最终速度下验收开头 15 秒、一个中段、所有主要转折和收尾；检查发音、节奏、焦点、情绪连续性、音色漂移和声音标签执行。
6. **再次停下等待用户批准最终音频。** 获得批准后运行 `scripts/approve_audio.py` 和 `scripts/publish_voice.py`。

### 3. 只从定稿音频生成字幕

1. 只对 `audio_approved` 且 hash 匹配的最终 WAV 生成时间轴；M4A/MP3 是发布衍生物，不作为字幕时间基准。任何 Take、速度、裁剪或拼接变化都使旧时间轴失效。
2. 使用 `audio-to-subtitles` 生成 ASR 时间轴。该步骤需要 R2/MediaKit 凭证并会上传最终音频；使用项目已授权凭证，不打印密钥。
3. ASR 只提供时间轴。用 `work/tts/subtitle-source.txt` 回填最终显示文本，不显示呼吸、停顿和发音标记。
4. 读 `references/output-layout.md` 交付 SRT/VTT/JSON 和 raw ASR 证据，通过 `scripts/mark_subtitled.py` 把交付文件的 hash 绑定到已批准音频。数字人、口型和正式剪辑都必须以这份定稿音频为唯一时间基准。

## 引擎能力边界

导演稿使用 sound tags、局部参数或要求重音/语调控制时，读 `references/capabilities.md`。每个导演意图必须被标识为：

- 引擎原生执行；
- 通过口语改写、分段、整段参数和 Take 挑选近似执行；
- 或引擎不支持。

不得把词级重音、局部音高 contour 或未验证的 Speech 2.8 `emotion` 字段宣称为精确控制。

## 停止条件

只有同时满足下列条件才能报告完成：

- 导演稿、审查视图、lint、render manifest 和字幕干净稿已归档。
- 最终 Take 和最终速度音频已经人工批准。
- 正式 WAV/M4A/MP3 已发布，旧成果已可恢复备份。
- 字幕来自定稿音频，显示文本已回填为干净原稿。
- 开头、中段、主要转折和收尾已听审，没有未记录的局部返工。
