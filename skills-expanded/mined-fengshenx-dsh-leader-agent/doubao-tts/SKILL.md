---
name: doubao-tts
description: 用豆包语音合成 2.0（火山 V3 HTTP 单向流式接口）生成中文旁白：鉴权、音色、分段、语速、测长、补静音、响度标准化与时间轴。需要把文案转成配音、旁白或可对齐的口播音频时使用。
whenToUse: 视频/播客/演示需要中文旁白，或已有旁白要调整语速、分段与时长时。
---

# 豆包 TTS 2.0

把文案转成可剪辑的旁白音频。核心不是“调通接口”，而是**每个叙事节拍一段、每段可测长、拼起来不漂移**。

## 凭据

只从环境变量读取，不读文件、不接受命令行明文密钥：

- `DOUBAO_TTS_KEY` —— 豆包语音控制台的新版 API Key（优先）
- `DOUBAO_TTS_API_KEY` —— 同上，兼容别名

```sh
# 用户自己的 shell 配置里已有变量；不要在这里 echo 它的值
source ~/.zshrc
node .agents/skills/doubao-tts/scripts/tts.mjs --help
```

缺变量时脚本直接报错并退出，不会打印密钥。生成的文件与日志里也不写密钥。

## 模型与音色

- Resource ID：`seed-tts-2.0`。2.0 音色必须以 `_uranus_bigtts` 结尾，不能和 1.0 的 `_moon_bigtts` / `_mars_bigtts` 混用。
- 本仓宣传片在用的男声解说音色：zh_male_jieshuoxiaoming_uranus_bigtts。
- 常用通用女声：zh_female_shuangkuaisisi_uranus_bigtts；多语种女声：zh_female_vv_uranus_bigtts。
- 请求走 `https://openspeech.bytedance.com/api/v3/tts/unidirectional`，响应是 NDJSON，每行一段 base64 音频；脚本负责拼接。不要用旧版 `/api/v1/tts` 的 AppID + Token 形态代替。

## 快速使用

```sh
source ~/.zshrc

# 单段旁白
node .agents/skills/doubao-tts/scripts/tts.mjs \
  --text "同时跑五个任务，是什么感觉？这个等你确认，那个又报错。" \
  --out /tmp/vo-01.mp3 \
  --speaker zh_male_jieshuoxiaoming_uranus_bigtts \
  --rate -5

# 从文件读长文案（仍建议按节拍拆段）
node .agents/skills/doubao-tts/scripts/tts.mjs \
  --text-file /tmp/script.txt \
  --out /tmp/vo.mp3
```

脚本只负责一次合成；**测长、补静音、拼接、响度**由下面的命令完成。视频场景边界与录制见 [`promo-video`](../promo-video/SKILL.md)。

## 测长、补静音与拼接

每段生成后立刻测长，把读数写进 `timeline.json`：

```sh
ffprobe -v error -show_entries format=duration \
  -of default=nw=1:nk=1 .dev/promo/audio/s1.mp3
```

每段前补 `lead`、后补到目标 `duration`，用 WAV 中间态避免 MP3 编码延迟累积：

```sh
# 例：lead=0.35s，目标 8.958s
ffmpeg -y -i .dev/promo/audio/s1.mp3 \
  -af "adelay=350:all=1,apad" -t 8.958 \
  -ar 48000 -ac 1 -c:a pcm_s16le .dev/promo/audio/s1.wav

# concat.txt 里写绝对路径，避免 ffmpeg 相对 concat 文件目录解析
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -c:a pcm_s16le .dev/promo/audio/narration.wav

# 整条做一次响度标准化，再编码
ffmpeg -y -i .dev/promo/audio/narration.wav \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 48000 -c:a libmp3lame -b:a 192k .dev/promo/audio/narration.mp3
```

检查：

```sh
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 narration.mp3
ffmpeg -hide_banner -nostats -i narration.mp3 -af volumedetect -f null -
```

期望：总长等于 `timeline.duration`；平均约 −17 dB、峰值低于 0 dB；段间静音约 0.8–1.5 秒，不要出现 3 秒以上的死区。

## 分段纪律

1. **一段一个语义节拍**，通常 1–3 句、6–10 秒。不要把整条 60 秒文案塞进一次请求；后面无法按句对齐画面。
2. 保留标点与口语停顿。`？`、`。`、`：` 会自然产生停顿，比在文本里硬塞空格可靠。
3. 语速从 `0` 起步；宣传片口播常用 `-10` 到 `-5`。改语速后必须重新测长，不能沿用旧时长。
4. 每段用 `ffprobe` 测实际时长，记录在 JSON 或表格里；后续场景边界只认这个读数。
5. 每段前留 `0.2–0.4s` 静音、后留 `0.4–1.0s` 静音，再把整条拼起来。段间静音是转场和动画的呼吸，不是浪费。
6. 整条混音做一次响度标准化（例如 `loudnorm=I=-16:TP=-1.5`），再编码 AAC/MP3；不要在每段单独拉满。

## 时间轴接口

`timeline.json` 是音频与时间轴之间的唯一契约，字段定义只在这里维护：

```json
{
  "segments": [
    { "key": "s1", "text": "同时跑五个任务，是什么感觉？", "speech": 7.608, "lead": 0.35, "tail": 1.0, "duration": 8.958 }
  ],
  "starts": { "s1": 0 },
  "duration": 66.914
}
```

| 字段 | 含义 |
|---|---|
| `segments[].key` | 场景/节拍标识（`s1`…），与分镜表一致 |
| `segments[].text` | 该段旁白的字幕原文；SRT 用它 |
| `segments[].speech` | 纯语音时长（`ffprobe`） |
| `segments[].lead` | 场景开始到语音开始的静音 |
| `segments[].tail` | 语音结束到场景结束的静音 |
| `segments[].duration` | `lead + speech + tail`，该场景占用的总时长 |
| `starts` | 每个场景的全局起点；`s1` 为 0，其余是前面所有 `duration` 的累加 |
| `duration` | 全片总长，等于最后一个 `starts[key] + duration` |

场景起点 = 前面所有 `duration` 累加；不要把总时长写死成 60/72 秒。字幕起点 = `starts[key] + lead`，字幕终点 = 起点 + `speech`。SRT 生成命令见 [`promo-video`](../promo-video/references/timeline-and-render.md) 的“字幕 SRT”。

## 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--text` | — | 待合成文本；与 `--text-file` 二选一 |
| `--text-file` | — | UTF-8 文本文件 |
| `--out` | — | 输出音频路径；编码由 `--format` 决定，扩展名不参与推断 |
| `--speaker` | zh_male_jieshuoxiaoming_uranus_bigtts | 2.0 音色 ID |
| `--rate` | `0` | 语速 `-50..100`，负值更慢 |
| `--loudness` | `0` | 音量 `-50..100` |
| `--format` | `mp3` | `mp3` / `wav` / `pcm` / ogg_opus |
| `--sample-rate` | `24000` | 采样率 |
| `--resource-id` | `seed-tts-2.0` | 模型版本 |
| `--endpoint` | 官方 V3 地址 | 仅本地 mock/可信代理时覆盖；Key 会发到该地址 |

`--endpoint` 指向非默认地址时，脚本会在 stderr 打印警告。不要把 Key 发到不可信地址；未知参数与位置参数都会直接报错并列出可用参数。

## 排错

- **401/403**：Key 不是新版控制台的 API Key，或没有开通对应模型/音色权限；不要改用别人的 Key。
- **音色不匹配**：`seed-tts-2.0` 只接受 `*_uranus_bigtts`；1.0 音色要换 `seed-tts-1.0`，但不要在同一片里混版本。
- **响应有 code 但没有 data**：先看 `message`；常见是文本为空、音色无权限、资源 ID 写错。
- **合成成功但听起来太快**：先降 `--rate` 到 `-8` 左右，再重新测长；不要靠后期加速掩盖。
- **段间有爆音**：检查每段是否裁掉了尾部静音；保留 0.1s 以上余量再拼接。
- **脚本报“没有音频分片”**：确认响应是 NDJSON 而不是被代理改成了 SSE；看第一行 `code`，不要把 HTML 错误页当音频写盘。

## 产物

- 每段一个音频文件，命名带节拍号（`vo-01.mp3`）。
- 一份 `timeline.json`，字段定义见上面“时间轴接口”。
- 一条拼好的旁白音轨，供视频 mux。
- 一份 SRT：由 `promo-video` 的“字幕 SRT”步骤从 `timeline.json` 生成，时间来自 `starts + lead`，不要手写时间码。

**不要把 API Key、控制台截图、带 token 的请求头写进仓库或技能文件。**
