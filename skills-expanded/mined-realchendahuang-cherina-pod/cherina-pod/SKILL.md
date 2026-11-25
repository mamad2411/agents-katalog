---
name: cherina-pod
description: Turn any podcast episode into a listening-practice lesson for language learners — an offline player page (line-by-line playback, loop, blind listening, word-by-word highlight), a printable bilingual handout, and key-phrase notes. Default is English audio with Chinese translation; Chinese audio with English translation also works. Use when the user wants to practise listening with a podcast, e.g. "把这期播客做成精听课", "用播客练听力", "做一份听力讲义", "播客精听", "make a listening lesson from this podcast".
---

# cherina-pod：一句话把播客做成精听课

所有命令都在**本 skill 的目录**里运行（就是这个 SKILL.md 所在的目录）。

## 只用这一条命令

```bash
python3 scripts/lesson.py "<来源>" [--episode <哪一集>] [--level "<水平>"] [--lang en-zh]
```

| 参数 | 怎么填 |
|---|---|
| `<来源>` | 用户给什么就原样填什么：播客名（`"6 Minute English"`）、RSS 地址、Apple Podcasts 链接、本地音频文件路径。**必须加引号。** |
| `--episode` | 不填 = 最新一集。用户说“第 3 集/倒数第三期”填 `3`（1 = 最新）。用户说出标题里的词就填那个词。 |
| `--level` | 用户提到水平才填，例如 `"四级"`、`"雅思 6"`。没提就不填。 |
| `--lang` | 英文播客配中文（默认）不用填。中文播客配英文填 `--lang zh-en`。 |

命令会打印很多进度信息。**只看最后一行**，它总是以 `RESULT ` 开头，后面是 JSON。

## 按 RESULT 行行事

**`"ok": true`** → 处理完成。用下面的模板回复用户，路径从 JSON 里原样复制：

> 已做好《{title}》（{podcast}）：{sentences} 句，分 {segments} 段，{key_phrases} 个难点表达，已自动跳过 {ads_skipped} 句广告，用时 {elapsed_minutes} 分钟。
> - 精听：打开 `{player}`，按播放键从第 1 段开始
> - 在手机上练：把 `{phone_file}` 发到手机（微信 / AirDrop），用浏览器打开即可（只有这个字段不为 null 时才写这一行）
> - 打印讲义：打开 `{handout}`，点「打印 / 存为 PDF」
> - 所有课和连续打卡：打开 `{library}`

**`"ok": false`** → 看 `stage`，按下表处理。**同一个错误最多重试 1 次**，仍失败就把 `error` 和 `fix` 原文告诉用户。

| stage | 你要做的事 |
|---|---|
| `env` | 运行 `python3 scripts/lesson.py --doctor`，把每个 `"ok": false` 项的 `fix` 告诉用户。缺 key 时请用户自己填，**不要编造、不要打印 key**。 |
| `resolve` | 播客没找到。请用户给更完整的名字，或直接给 RSS / Apple Podcasts 链接。 |
| `episode` | 运行同一来源加 `--list`，把返回的 `episodes` 前 5 条（`n` 和 `title`）列给用户选，再用 `--episode <n>` 重跑。 |
| `download` | 换一集重跑（`--episode 2`），或请用户换节目。 |
| `transcribe` / `translate` / `align` / `lesson` | **原样重跑同一条命令一次**（会自动续跑，已完成的步骤不重复花钱）。 |
| `args` | 你的参数写错了，对照上面的参数表改正后重跑。 |

## 用户没指定播客时

用户只说“想练听力”“推荐个播客”而没给节目名时，先运行：

```bash
python3 scripts/lesson.py --recommend --level "<水平>"     # 学中文再加 --lang zh-en
```

把返回的 `podcasts` 里每项的 `name`、`why` 列给用户挑，选定后用该项的 `source` 作为 `<来源>` 生成。

## 用户想在手机上练时

- 20 分钟以内的节目会自动生成手机单文件（RESULT 里的 `phone_file`），直接发到手机即可。
- 更长的节目：加 `--phone --parts 1-3` 只打包前三段，或运行 `python3 scripts/lesson.py --serve`，把它打印的 `url` 告诉用户（手机和电脑需连同一个 Wi-Fi）。`--serve` 会一直运行，用户说练完了再停止它。

## 用户没说清是哪一集时

先运行：

```bash
python3 scripts/lesson.py "<来源>" --list
```

`RESULT` 里的 `episodes` 是最近 15 集。列出前 5 条让用户挑，然后用 `--episode <n>` 正式生成。用户说“最新的”就直接生成，不用列。

## 第一次使用

先运行 `python3 scripts/lesson.py --doctor`。全部 `"ok": true` 才继续。

- 某项为 false 时，`fix` 里如果是一条命令（例如 `brew install ffmpeg`），可以替用户执行。
- 缺 `DASHSCOPE_API_KEY` 时，请用户在自己的终端运行 `python3 scripts/lesson.py --setup`，按提示粘贴 Key。**不要让用户把 Key 发给你，也不要替用户编造。**

## 不要做的事

- 不要自己调用 `scripts/` 里的其他脚本，`lesson.py` 已经串好全流程。
- 不要修改或删除 `episodes/` 里已有的文件，尤其是 `transcript.json`（重新转写要花钱）。
- 不要把生成的内容（转写、译文、讲义）上传、发布或提交到 git，它们来自第三方播客，只供用户个人学习。
- 一小时的节目需要 5–15 分钟，命令运行期间不要中断它。超时就原样重跑，会自动续跑。

## 其他用法（用户明确要求时才用）

- 只重新生成网页和讲义（不重新转写翻译）：`python3 scripts/build_lesson.py <期目录>`
- 每段时长、难点条数：`python3 scripts/build_lesson.py <期目录> --seg-seconds 120 --notes 30`
- 产物默认在 `episodes/`，设置环境变量 `CHERINA_POD_OUT=<目录>` 可以改到别处。
- 保留广告句：`python3 scripts/build_lesson.py <期目录> --keep-ads`
