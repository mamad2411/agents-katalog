# Easel 直连（easel）

直接驱动 Easel（`D:\AI\repos\Easel`）的**脚本层**做短视频，不经过它自带的 openclaw agent。

## 为什么不走 `easel chat` / `easel skill`

`easel chat` 和 `easel skill` 最终都是 `openclaw_base_cmd() + tui`（见 `easel/cli.py:51-74`）——
即「再起一个 agent 来干这活」。两层 agent 套娃的代价是真实的：

- 人设偏好要在中间那层的会话历史里活下来，而 `openclaw/workspace/AGENTS.md` 的注释自己承认
  画像「超长会话被压缩后可能丢」；实测症状是同一个人的两条片子，一条克隆音色、一条退到 edge。
- 中间那层有自己的 SOUL / AGENTS / 模型选型，会「按默认值擅选」（AGENTS.md 明确禁止但会发生）。

Easel 的执行层全是纯 CLI 脚本，没有一条依赖 openclaw。编排、判断、审美由大白自己做，
确定性步骤交给脚本——**单层 agent**。

## 工具

| 工具 | 用途 |
| --- | --- |
| `easel_check` | 环境体检：根目录 / git 版本 / 实际解释器 / 人设音色配置 / ffmpeg / 脚本清单 / 最近产物 |
| `easel_run` | 白名单脚本执行：cwd 自动落在 Easel 根、自动注入 `.env` 与 UTF-8、回读产物是否存在 |

`easel_run(script, args, timeout)` 的 `script` 传脚本名（不含路径与 `.py`）；
`args` 是参数数组。根目录解析顺序：环境变量 `EASEL_ROOT` → `D:\AI\repos\Easel` → 当前工作区。

## 常用脚本

| 脚本 | 干什么 |
| --- | --- |
| `tts` | 配音（`speak` / `voices`）。不带 `--engine` 就走 `.env` 的引擎优先级 |
| `tts_index` | 本地克隆音色底层（`check` / `speak`），缺 `gradio_client` 会自动切 conda env `index-tts` |
| `assemble` | 分镜 + 配音 + BGM → `final.mp4`（`skills/openclaw/auto-short-video/scripts/assemble.py`） |
| `render_card` | HTML → 图片（playwright + chromium） |
| `video_ops` / `audio_ops` | ffmpeg 封装：cut/concat/speed/aspect/frame/info、trim/normalize/extract/concat |
| `subtitle_ops` / `asr` | 字幕处理 / 语音转字幕（faster-whisper） |
| `ai_image` / `ai_video` / `ai_music` | 文生图 / 图生视频 / 音乐（需自备 key） |
| `model_registry` | 查已配置的模型（`configured --group ... --env-file .env`） |
| `wordcount` / `social_stats` / `output_paths` | 字数校验 / 统计口径 / 产物路径门禁 |

完整清单跑 `easel_check`。

## 人设配置（音色/字体/水印）

**唯一真相源是 Easel 根 `.env`**，不是某条命令的参数、也不是某个 SKILL.md 的示例：

```
VOICE_PROVIDER=          # 留空=不用闭源云
VOICE_LOCAL=indextts     # 本地克隆音色
INDEX_TTS_REF=C:/Users/.../cangjiao.wav
INDEX_TTS_SPEED=1.5
INDEX_TTS_SERVER=http://127.0.0.1:7860/
```

引擎优先级：闭源云（`VOICE_PROVIDER`）> 本地克隆（`VOICE_LOCAL`）> edge（机械音）。
改配置改这里，任何 SKILL 调用都自动命中。

## 产物约定

- 成品：`outputs/<主题>/final.mp4`
- 素材：`outputs/<主题>/assets/`（分镜图、配音、字幕、storyboard）
- 中间试验：`outputs/_scratch/`
- 主题名必须人类可读，禁止 `test/tmp/xhs` 这类泛名

## 交付前自检（不许只报「已生成」）

1. `ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height final.mp4` 核时长/分辨率
2. 抽 3~7 帧目视（`see_image`）
3. 音轨时长与配音时长对得上
