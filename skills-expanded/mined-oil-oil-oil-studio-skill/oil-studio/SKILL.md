---
name: oil-studio
description: >
  Use Oil Studio to record and edit local recording projects on macOS: make demos, refine voice-overs, add titles or image overlays, redact screen regions,
  handle captions and chapters, synthesize narration, configure projects, and export video. Can also turn an existing MP4/MOV/M4V into a project to cut a clip
  from it and review the cut points in context. Use when a user mentions Oil Studio, asks to work on a recording project, or wants a video brought into Oil Studio.
  Not for quick edits of ordinary video files the user does not want in Oil Studio, or for directly changing project files.
  用 Oil Studio 处理本机录屏工程：录制演示、精剪口播、添加标题或图片、遮盖画面、处理字幕与章节、合成配音和导出；也可以把现成的 MP4/MOV/M4V 导入成工程，
  从中切出一段并在完整视频里核对切点。用户提到 Oil Studio、录屏工程，或要把视频放进 Oil Studio 剪辑时使用。不用于不想进 Oil Studio 的普通视频快剪，或直接编辑工程文件。
metadata:
  version: 0.14.6
  minAppVersion: 0.3.44
---

# Oil Studio

For an English conversation, read [the English workflow](en/SKILL.en.md) and follow only that entry. 中文对话使用本页；两版均支持中英文口播，流程和命令相同。命令行输出可用 `--lang en` / `--lang zh-Hans` 指定，不更改 App 偏好；音频语言单独用 `transcribe --locale en-US` / `--locale zh-CN` 指定。

通过命令行 `oilstudio` 操作录屏工程。命令行把结果写成一个 JSON 对象；导入、转录这类较长的命令会先逐行输出进度，最后一行才是结果。你负责理解内容和做判断，命令行负责读写工程、校验和执行。

任务导航：[精剪](#精剪) · [画面元素与打码](#添加画面元素与打码) · [生成字幕](#生成字幕) · [校对字幕](#校对字幕) · [导出成片](#导出成片)。其余任务见下方选择表。

## 开始前

1. 用本文件 frontmatter 的 `metadata.version` 运行 `OILSTUDIO_SKILL_VERSION=0.14.6 oilstudio status`。
   - 命令不存在：运行 Oil Studio 官网的安装脚本 `curl -fsSL https://studio.oiloil.org/agent/install.sh | sh`，运行前告诉用户这是在安装 Oil Studio 命令行。Mac App Store 版会直接装好，装好后重新运行这一步；脚本提示官网版自带命令行时，请用户在 Oil Studio「设置 › AI Agent」里点「安装」，然后停止；提示没有找到 Oil Studio 或版本还不支持时，把提示转告用户并停止。
   - 有 `skill.compatible` 时，若为 false，向用户转达 `skill.action.message` 和 `skill.action.hint` 并停止；为 true 时继续。若为 null，说明版本未被正确提供，重新核对后停止。
   - 没有 `skill.compatible` 表示 App 版本较旧：按语义版本各段数字比较 `app.version` 与本文件的 `minAppVersion`，版本过低请用户升级 Oil Studio 并停止；版本无法取得时说明无法核对，不用 `cli.version` 代替。
   - 有 `skill.update`：本机有比 App 内置版本旧的 Skill 副本（可能就是你正在读的这一份）。把 `skill.update.message` 告诉用户；用户同意后运行 `installations[].command`，把那一份换成随 App 更新的链接（原目录会改名备份），换完后新开的会话才会读到新版本。不影响本次任务，继续。
   - `app.relaunchRequired` 为 true：正在运行的 Oil Studio 已被移动或删除，录制等操作会失败。请用户退出 Oil Studio，再从“应用程序”文件夹重新打开，然后停止。
   - 核对 `app.channel`、`app.otherInstallations`、`warnings` 与 `speech`（若有）：本机同时装有官网版与 Mac App Store 版时，各版本的设置与云端 API Key 相互独立；若 `warnings` 提示多版本共存或长视频任务下 `speech.autoResolvedEngine` 为 `system` / `null`，先提醒用户核对连接的版本与语音引擎设置，再开始长时间识别。
2. 确定工程路径。Oil Studio 工程是以 `.oilstudio` 结尾的包。
   - 用户给了 `.oilstudio` 路径：直接使用。
   - 用户给的是其他录屏软件的工程：运行 `oilstudio import <路径>`，用返回的 `path` 继续，并告诉用户"已转换为 Oil Studio 工程，保存在 <path>，原工程没有改动"。同一工程再次 import 会直接返回已有的转换结果，不会重复复制。
   - 用户给的是视频文件（MP4 / MOV / M4V）：按「从视频切一段」先 import。视频每次 import 都新建一个独立工程，可用 `--name` 起名。
   - 没给：运行 `oilstudio projects`（只列 `.oilstudio`），按标题和时间挑出最可能的一个；有多个候选时列出来请用户选。
3. 失败时读 `error.code` 和 `error.hint`，按提示处理；同一命令失败两次就停下，把 `message` 告诉用户。
   - `SKILL_OUTDATED`：立即停止重试，把 `message` 和 `hint` 告诉用户。
   - `CLI_UPDATE_REQUIRED`：Oil Studio 更新过，命令行还是旧版本。运行第 1 步的安装命令，再重试一次。
   - `APP_NOT_INSTALLED`：本机没有安装 Oil Studio，请用户先安装，然后停止。
   - `PERMISSION_REQUIRED`：把 `message` 和 `hint` 告诉用户后停止。它写明了缺哪项授权（旧版 Oil Studio 里也可能是用户在授权框里选了取消）；如果提示当前终端或 AI 沙箱限制了本机连接权限，请用户允许在沙箱外运行 `oilstudio`，不要试图通过 `open -a "Oil Studio"` 重开 App 或在沙箱内重试。
   - `needs_import`：路径不是 Oil Studio 工程，按上一步先 import。
   - `UNSUPPORTED_MEDIA`：视频格式或编码不支持、没有画面，或受版权保护；把 `message` 告诉用户，不要换参数重试。
   - `read_only`：工程由更新版本的 Oil Studio 创建，只能读取和导出；不要提交修改，请用户先升级 Oil Studio。

## 选择任务

| 用户要什么 | 走哪一节 |
| --- | --- |
| 录一段某个应用或网页的操作演示 | 录制演示 |
| 按步骤编排网页演示、重点卡片和缩放 | 网页 Playbook 录制 |
| 口播已经录好（只有人和声音），要补上对应的屏幕操作 | 给口播补画面 |
| 把现成视频（MP4 / MOV / M4V）放进 Oil Studio 剪辑，或从长视频里切出一段 | 从视频切一段 |
| 去掉没有操作的等待时间（没有口播的录屏） | 删除空档 |
| 剪掉重说、口误、废话，并把字幕也处理好 | 精剪 + 字幕一气呵成（标准命令流） |
| 剪掉重说、口误、废话，让口播更紧凑 | 精剪 |
| 只去掉停顿和空白 | 收紧停顿 |
| 调整放大效果，让观众看清正在讲的地方 | 调整缩放 |
| 加标题、标签、图片/B-roll，或遮盖画面中的敏感区域 | 添加画面元素与打码 |
| 生成初始字幕、给录屏加字幕 | 生成字幕 |
| 改字幕里的错词、专有名词、残留语气词或断行 | 校对字幕 |
| 改画幅、背景、光标、摄像头、声音或导出选项 | 调整工程配置 |
| 给视频划分章节（进度条上的章节名） | 划分章节 |
| 要英文字幕 | 英文字幕 |
| 拿到字幕文件 | 导出字幕 |
| 导出视频 | 导出成片 |
| 了解工程内容、时长、说了什么 | 运行 `oilstudio context <工程> --out <临时文件>` 后回答，不提交任何东西 |

## 共同规则

- 不直接读写工程目录里的文件，一律通过 `oilstudio`。
- 修改只能以提案提交（`plan submit`、`subtitles apply`、`chapters apply`、`pauses --submit`、`idle --submit`、`settings apply`）。提交命令的返回里看 `autoApplied`：
  - `false`：等用户在 App 里确认。不要说"已剪好"，要说"已提交，等你在 Oil Studio 里确认"。保存 `proposalId` 和尚未完成的后续任务；一次等待超时不代表用户拒绝，也不代表整项任务完成。如果同时返回了 `skipped`、而 `applied` 为空，说明这次什么都没有应用（工程会直接应用 AI 修改，但这些条目被跳过了），按 `skipped` 里的原因处理，不要说成等待确认。
  - `true`：修改已经生效（你自己录的工程，或用户为这个工程打开了"AI 的修改直接生效"）。汇报 `applied` 的条数和 `skipped` 的原因，告诉用户可以在 Oil Studio 里按 ⌘Z 撤销；不需要再运行 `proposal status --wait`。
  - 提交前想知道是哪一种：看 context 的 `autoApply`。它为 true 而返回 `autoApplied: false`，说明工程没有在 Oil Studio 里打开，修改会在用户打开工程时自动生效；这时不要接着导出，先告诉用户。
- `subtitles generate` 和章节一样直接生效，不需要用户确认，之后在 App 里可以撤销；工程不需要先在 App 里打开，App 没开也能用。工程里还有等待用户确认的 AI 修改时，它会拒绝并说明原因，不识别、不改工程：先请用户在 Oil Studio 里处理那条修改；Oil Studio 正在处理别的修改时也会拒绝，稍后重试一次即可。它不同于只生成转录缓存的 `transcribe`。
- `narration generate / import` 生成或导入字幕配音后直接保存；已打开工程通过 App 一步撤销，离线工程检查版本后保存。详见 [字幕配音](references/narration.md)。
- `chapters apply` 始终直接应用，不受工程的自动应用开关影响，也不需要章节确认。`autoApplied: false` 只表示工程未打开、尚未就绪或排在另一个审阅后；按 `pendingReason` 续接，不把它说成等待章节确认。
- 时间只用发言编号（如 `U0012`）或源时间毫秒（`sourceStartMs` 这类字段），剪切与缩放不用成片时间；布局、导出范围、补画面的 `--at-output-ms` 与录屏片段的 `move` 明确使用成片时间。命令带 `--plan <方案文件>` 时，其中的成片时间指方案剪后的时间。
- 在提交最终修改或完成导出之前的中间步骤，每完成一步运行一次 `oilstudio progress "<这一步做了什么>" --step <第几步>/<总步数> --project <工程>`，让用户在 App 里看到进度；最终修改已提交或整项任务完成后不要再调用 `oilstudio progress`。返回 `delivered: false` 表示 App 没开，返回 `PROJECT_NOT_FOUND` 表示 App 里打开的不是这个工程，两种情况都继续工作即可。
- `--out` 写临时文件时每次用新文件名（例如加上步骤编号）；命令不会覆盖已有文件。
- 提交前必须先校验；校验不通过就修正后再校验，不要跳过。`plan validate` 只检查提交条目是否可执行，不会发现没有写进方案的漏删。
- 标题、标签、图片/B-roll 与打码作为 `plan submit` 的 `overlays`、`redactions` 提案提交；`plan validate` 只校验，不写工程或导入素材。图片只有在应用被接受时才导入工程，并按提交回执核对实际应用与跳过项。
- 用户回来继续、纠正或询问进度时，先查已保存的 `proposal status`。若已 `applied`，基于当前工程自动续做已授权任务，不重复索要确认；若仍在审阅，保留待办。`USER_DISMISSED` 不自动重提；工程变化导致失效时重新取证，不把新指纹直接贴进旧方案（唯一的例外是“给口播补画面”第 8 步：变化只是你自己补录的片段）。

## 录制演示

你用命令行开始和停止录制，用你自己的工具（Computer Use、浏览器工具）操作被录的应用。先读 [录制](references/recording.md)，里面有操作时的规矩和出错时的处理。录制会生成新工程，所以"开始前"的第 2 步（确定工程路径）在这里跳过。

网页动作多、需要按拍编排缩放或画面解剖卡片时，使用[网页 Playbook](references/recording.md#网页-playbook) 和 `scripts/record_playbook.py`。该流程只通过网页自动化接口操作网页，不使用 Computer Use；**演示录制默认不加字幕（除非用户明确要求加字幕）**。
**不要录正在被 Agent 接管的浏览器窗口**：这类浏览器会在页面上画控制条、边框和动作气泡，会原样录进成片。网页演示用 Playbook 的独立舞台（默认），需要登录态或多个标签页时用 cdp 宿主连接用户自己启动的浏览器，见[录制](references/recording.md#浏览器宿主)。

1. `oilstudio status` 的 `app.running` 为 false：运行 `open -a "Oil Studio"`，等几秒后再查一次。
2. 把要录的窗口准备到开场状态（打开页面、登录、调好窗口大小）。准备过程不录。
3. 运行 `oilstudio record sources`，按 `app` 和 `title` 找到要录的那个窗口，记下 `id`。
   - 录制需要 macOS 的屏幕录制权限（给 Oil Studio），只能由用户授权，不要去改系统设置。旧版 Oil Studio 第一次录制时还会弹出确认框，命令会等用户点"允许"，不要自己去点。
   - 返回 `PERMISSION_REQUIRED`：把 `message` 和 `hint` 原样告诉用户（它写明了缺哪一项授权、是否被沙箱拦住本机连接，或者 App 需要重新打开），这一轮到此停止。用户处理完后再从这一步重新开始。
   - 有多个窗口都像目标：列出来请用户选。只录用户要的那个窗口；用户没说录整块屏幕就不要选屏幕。
4. 可先运行 `oilstudio record prepare --source <id> --size 1280x800 --center --activate` 调整窗口；`--position X,Y` 与 `--center` 二选一。也可将这些参数直接加到 `record start`。调整外部窗口需要辅助功能权限。
5. 运行 `oilstudio record start --source <id>`。默认不录麦克风、摄像头和系统声音；用户明确要求时才加 `--microphone`、`--camera`、`--system-audio`。
   - `RECORDER_BUSY`：用户正在自己录制，告诉用户后停止。
6. 按计划操作被录的窗口。不用赶时间，操作之间的等待稍后会剪掉。
   - **每次点击前先申报**：`oilstudio record click --at <x>,<y>`（或 `--at-fraction <u>,<v>`），命令返回后立刻去点；加 `--perform` 可由 Oil Studio 原生执行点击，不再额外点击。成片里的光标是 Oil Studio 按你的申报生成的，你的真实鼠标不会被录进去；不申报，那一步就没有光标，也没有跟随点击的缩放。
   - 想让观众看某个地方但不点（悬停、指一下）：`oilstudio record move`，参数相同；加 `--perform` 可同时移动真实光标。
   - 位置怎么给见 [录制](references/recording.md) 的"申报位置"。
7. 运行 `oilstudio record stop`，记下返回的 `path`。
   - 录坏了想重来：`oilstudio record stop --discard`，回到第 2 步。
8. 按"删除空档"处理这个工程。
9. 需要让观众看清小字或细节时，按"调整缩放"处理；用户要成片时按"导出成片"处理。
10. 汇报：工程路径、成片时长、删了多少空档。

录制过程中不用运行 `oilstudio progress`（这时还没有工程）；停止录制拿到 `path` 之后的步骤再照常汇报进度。

## 给口播补画面

口播工程是用户用“仅录口播”录的：主线只有人（摄像头）和声音，context 的 `voiceOver` 为 true。还没补任何录屏时成片是人像全屏；补了以后显示录屏、人像缩成小窗，录屏轨上的空档不会切回人像，而是停在上一段的最后一帧。你的任务是按讲解内容录出对应的屏幕操作，让每个操作落在讲到它的那一刻，并**把录屏轨填满**：有讲话的地方都要有画面，没有讲话的等待剪掉。录屏片段和普通录屏一样有光标、点击缩放与打码。先读 [录制](references/recording.md)。

1. 运行 `oilstudio context <口播工程> --out <临时文件>`；`utterances` 为空时先 `transcribe`。看三样：`utterances`（每句的 `outputStartMs / outputEndMs`，每个词的 `outputStartMs`）、`screenGaps`（还没有画面的成片区间）、已有的 `screenClips`。
2. 口播里有明显的等待（长停顿）或口误时，先剪再补画面，补画面的时刻都按剪后的成片时间算：
   - context 的 `autoApply` 为 true：按“收紧停顿”或“精剪”照常提交，生效后重新取 context，再补画面。
   - 否则：按“精剪”写好方案并 `plan validate`，**先不要提交**。补录会改变工程，已提交但还没确认的方案会因此失效。之后的 `context`、`record start`、`frame` 都加 `--plan <方案文件>`，命令按方案剪后的时间线读写，返回的 `plan.stale` 为 true 只说明补录改了工程，投影照常可用。
3. 按讲解拆成几段画面，每段对应一句或连续几句：这段讲什么 → 在哪个窗口做什么 → 讲到哪个词时做哪一步。各段首尾相接：每段从上一段结束的时刻开始录，录到下一段开始。讲的是概念、没有可演示的操作时也要有画面：把相邻那段录长一点，停在相关页面上，不要留空档。相邻两段之间零点几秒的缝不用管，画面会停在上一段的最后一帧。说不清要演示哪个页面或功能时问用户，不要编造操作。超过 5 段时先把计划列给用户。
4. 把要录的窗口准备到这段的开场状态（准备过程不录），用 `record sources` 找到窗口 `id`。
5. 录一段：`oilstudio record start --source <id> --into <口播工程> --at-output-ms <这段开始的成片毫秒> [--plan <方案文件>]`。不要加 `--microphone`、`--camera`、`--system-audio`。
   - 录制从这一刻起按真实时间走：开始后第 N 毫秒就是成片里的 `at-output-ms + N`。某一步要在讲到某个词时发生，就在开始后 `词的 outputStartMs − at-output-ms` 毫秒执行；用 `record status` 的 `durationSourceMs` 看已经录了多久。点击前照常 `record click` 申报。
   - 操作需要等待（页面加载、动画）时，把那一步提前开始，让结果出现在讲到它的时候。
   - 到这段该结束的时刻（这几句讲完，或下一段开始）运行 `oilstudio record stop`。返回的 `screenClip` 就是挂到口播上的片段，已经保存，`path` 是口播工程。
   - **重录某一段**：加 `--replace-until-output-ms <这段结束的成片毫秒>`，并入时先清掉 `[at-output-ms, 这个时刻)` 里的旧片段再放新片段，旧片段不会在新片段后面残留；新片段比这段短时，剩下的部分会出现在 `screenGaps` 里。
   - **带 `--plan` 时每段都加 `--replace-until-output-ms <这段结束的成片毫秒>`**：方案剪掉的部分在当前工程里还在，不写终点时，排在这段后面的旧片段会在方案生效后盖住新片段的结尾。
   - 网页演示用 [网页 Playbook](references/recording.md#网页-playbook) 的 `attach` 与动作的 `atMs`，脚本会按录制时钟等到每一步；`attach.plan` 和 `attach.replaceUntilOutputMs` 对应上面两个参数。
6. 核对：对每段讲到关键词的时刻运行 `oilstudio frame <口播工程> --output-ms <毫秒> --zoom none --text --out <png> [--plan <方案文件>]`，确认画面就是讲解说的内容。偏早或偏晚用 `plan submit` 的 `screenClips` 移动（`move`）、裁剪（`trim`）或变速（`speed`）；录错了就按上一步重录这一段。格式见 [提案格式](references/proposal-formats.md)。
7. 所有段补完后再取一次 context（有方案草稿时加 `--plan`），确认 `screenGaps` 为空（段与段之间不到 0.5 秒的缝可以不管）。还有空档时：这段口播里有人在讲话，就补录或把相邻片段录长；这段是没有讲话的等待，就把这段口播加进精剪方案。用户明确要某处人像全屏时，才在布局轨提交 `camera` 布局。
8. 有方案草稿时最后提交一次：补录改变了工程，方案里的两份指纹已经过期。用新文件名重新取 context，确认 `utterances` 和起草方案时一致（期间只多了你录的片段）后，把新的 `projectFingerprint`、`contextFingerprint` 写进方案，`plan validate` 后 `plan submit`，按共同规则汇报。`utterances` 变了就说明用户改过工程，重新准备方案。用户要成片时，等方案生效后按“导出成片”处理。
9. 汇报：补了几段、各对应哪几句话、剪掉了哪些等待、哪些地方需要用户看一眼。

## 从视频切一段

用户给了现成的视频，要放进 Oil Studio 剪辑，或要从长视频里切出一段或几段。一个工程只导出一段：每段各用一个工程。

1. 先导入一次用来选片段：`oilstudio import <视频> --name "<视频名>（全片）" [--directory <保存目录>]`，用返回的 `path` 继续。这个工程保留完整视频，方便用户对照全片。原视频不会被修改，之后删掉或移走也不影响工程；视频和工程在同一块磁盘上时几乎不占额外空间。视频不接受 `--force`。
2. 这类工程没有鼠标和键盘数据：不要调整光标、按点击自动缩放或按键提示。默认没有背景，成片看起来就是原视频。剪辑、字幕、章节、贴图、打码和导出照常可用；视频的声音按人声分析，可以照常转录、删停顿和口误。
3. 选片段：运行 `oilstudio context <工程> --transcript-first --out <临时文件>`，`utterances` 为空时先运行 `transcribe`。按词级时间定入点和出点，不切在半个词或半句话上；用 `storyboard`、`frame`、`audio` 看清切点前后的内容。用户已经给了时间的，以用户的为准，只微调到最近的词边界。
4. 每段各导入一次并起名：`oilstudio import <视频> --name "<这段讲什么>"`，目录与第 1 步相同。同一个视频再次导入会直接复用声音和转录，不用再 `transcribe`，也不产生费用。
5. 给每个片段工程提交一份只含 `clip` 的方案：取这个工程的 context 指纹，写 `{"schemaVersion":1, "projectFingerprint":…, "contextFingerprint":…, "clip":{"sourceStartMs":入点, "sourceEndMs":出点, "reason":"…"}}`，校验后提交。不要再用两条 `cut` 剪掉前后。格式见 [提案格式](references/proposal-formats.md#片段范围-clip)。命令行导入的工程会直接应用 Agent 的修改：返回 `autoApplied: true` 就表示已经剪好并保存，App 没开也一样，不需要等用户确认。
6. 汇报：每段的工程名、从哪句开始到哪句结束、多长。告诉用户打开工程就是剪好的片段，剪掉的内容没有删除，把片段两端往外拖就能看到前后的内容并微调，按 ⌘Z 可以撤销；“全片”工程是完整视频。用户要成片时按「导出成片」导出。

## 删除空档

用于没有口播的录屏，或操作之间等待很长的录屏。有口播的录屏优先用"收紧停顿"或"精剪"。口播工程（context 的 `voiceOver` 为 true）不能删空档。

- 你自己刚录的工程：直接运行 `oilstudio idle <工程> --submit`，返回里同时有找到的空档和应用结果，不用先单独查一遍；它会将延迟的点击申报对齐到画面响应，并结合剪辑和变化区域重构自动缩放。
- 其他工程：先运行 `oilstudio idle <工程>`，把找到几处、能缩短多少告诉用户；用户同意后再加 `--submit`（其余参数相同）。
- 想保留更多等待：加大 `--keep <毫秒>`（每处空档两端保留的时间，默认 400）；只想删长等待：加大 `--threshold <毫秒>`（默认 1500）。
- 提交后按共同规则里的 `autoApplied` 汇报。没有找到空档时不会提交任何东西，返回里也没有 `proposalId`。

## 精剪 + 字幕一气呵成（标准命令流）

用户同时要求“剪辑视频 + 处理字幕”时，按以下 5 步在同一轮连续执行，**不要在提交剪辑方案后停下等用户点确认**：

```sh
# 1. 若尚无字幕（subtitles.count == 0），先生成初始字幕与转录缓存（纯口播无需系统音时可加 --mic-only）
oilstudio subtitles generate "<工程>" --engine auto

# 2. 单命令导出剪辑上下文与停顿清理草案（旧版 CLI 不支持 --out-plan 时再单独跑 oilstudio pauses --out-plan）
oilstudio context "<工程>" --out "$WORK/01-context.json" --out-plan "$WORK/02-plan.json"
python3 -B "<Skill目录>/scripts/dump_transcript.py" --context "$WORK/01-context.json" --out "$WORK/01-transcript.md" --audit-template "$WORK/03-filler-audit.json"

# 3. 将可执行剪点和需保护剪点的 keep/review 写入 02-plan.json，其余保留与复核记录写进 03-filler-audit.json，再核对并提交
python3 -B "<Skill目录>/scripts/verify_plan.py" --context "$WORK/01-context.json" --plan "$WORK/02-plan.json" --audit "$WORK/03-filler-audit.json" --coverage-out "$WORK/03-coverage.json"
oilstudio plan submit "$WORK/02-plan.json" --compact

# 4. 带 --plan 读取剪后可见字幕与自动诊断清单（无需等待用户先在 App 里点应用）
oilstudio subtitles get "<工程>" --plan "$WORK/02-plan.json" --out "$WORK/04-subtitles.json"

# 5. 清零 diagnostics 中的错词、大小写不一、残留语气词/口吃与断行告警，直接提交字幕修改（不加 --review）
oilstudio subtitles apply "<工程>" "$WORK/05-subtitle-edits.json" --plan "$WORK/02-plan.json"
```

需要章节时，成片时长 > 3 分钟（180000 ms）且尚无章节的工程，可用剪后保留的中文 `fromCue` 编写章节并运行 `oilstudio chapters apply "<工程>" "$WORK/06-chapters.json" --plan "$WORK/02-plan.json"`。检查回执的 `warnings` / `chapterWidthWarnings`，按「划分章节」里的 `autoApplied` 规则处理超宽标题。提案会排在剪辑与字幕提案之后接续生效。

## 精剪

1. 运行 `oilstudio context <工程> --transcript-first --out <临时文件>`，读取这个文件。
   - 用户同时要求处理字幕且 `subtitles.count` 为 0 时：直接先运行 `oilstudio subtitles generate <工程> --engine auto`（纯口播工程不希望识别系统音时加 `--mic-only`），完成后用 `oilstudio context <工程> --out <新文件> --out-plan <清理草案.json>` 一次拿到最新上下文与停顿草案。
   - 只做剪辑且 `utterances` 为空：先运行 `oilstudio transcribe <工程>`，完成后同样用新文件名重新取 context（可带 `--out-plan`）。
   - 上下文较大时，运行 `python3 -B <Skill目录>/scripts/dump_transcript.py --context <context.json> --out <transcript.md> --audit-template <filler-audit.json>` 导出紧凑文稿与编号后的语气词表，不必手写一次性解析脚本。
2. 若上一步未带 `--out-plan`（或需自定义 `--threshold` / `--keep`）：运行 `oilstudio pauses <工程> --out-plan <清理草案.json>`，读取 `planPath` 指向的方案。它只生成草案，不会提前剪工程；保留指纹与 `decisions`，后续语义删减追加到同一份方案。
   - 草案已经包含字词边缘保护，不要再把每个切口改成“开始加 50 ms、结束减 50 ms”。需要额外气口时只通过 `pauses --keep <毫秒>` 设置一次；用户没指定时沿用默认值。
   - 清理失败就按提示处理，不静默跳过；没有停顿时 `decisions` 为空，继续找重说。
   - 草案与 context 的两份指纹必须一致；不一致说明工程已变化，重新读取 context 和草案。
3. 读 [剪辑判断](references/editing-judgment.md)，通读全部发言，找重说、口误、放弃的半句与可独立删除的口头禅。语义判断使用源时间；清理只影响预期成片节奏，原声仍包含拟删停顿。
   - 用户指定了风格（保守 / 标准 / 紧凑）就按风格；没指定用“标准”。
   - 对 `fillerCandidates` 全量逐项复核，按[剪辑判断](references/editing-judgment.md)区分无词义犹豫音、语气词和有语义的词。每个候选必须有 `cut`、`keep` 或 `review` 及具体理由；被整段重说删减完整覆盖的记为已覆盖，不重复切。
   - `utterances[].audio` 包含置信度、字速、响度、句内停顿与未识别人声；`screen` 是画面 OCR 时间线。它们是证据，不直接决定删减，不把未识别当成应删除。
   - 听原声：`oilstudio audio <工程> --source-ms <起>,<止> --out <wav>`，最长 60 秒。
   - 看画面：`oilstudio frame <工程> --source-ms <毫秒> --zoom none --text --out <png>`；看一段用 `oilstudio storyboard <工程> --utterances <起>-<止> --out <png>` 或 `--source-ms <起>,<止>`，最长 40 秒。`--every 1000` 控制截图间隔，`--no-frames` 只看声音和文字。
4. 按 [提案格式](references/proposal-formats.md) 将可执行 `cut`、需要调整的 `zooms` 等写入 `plan.json`。会约束相邻剪点的 `keep` / `review` 也留在方案里，其余保留与复核记录写入 `filler-audit.json`。运行 `scripts/verify_plan.py` 核对覆盖率、剪点扩展与校验异常，统计整段覆盖、单独删减、保留和待复核。不能只挑少数长“呃”，或只报停顿数量就结束精剪。重叠删减不重复计时；没有可执行修改时不提交空方案。
5. 修正所有 `rejected` 后重新校验；`uncheckedByDefault` 留给用户复核，可通过条目里的 `matchedActivity` 查看具体命中的操作类型（如 `click`、`mouseUp`、`key`、`screenChange`）与源时间。
   - `cutAdjustments` 包含已核对的字词接缝校准和严格静音收尾；试听、提交与字幕预投影使用同一套范围。`boundaryReviews` 表示边界外仍有未确认可删的内容，已保留并写入条目说明；核对这些具体接缝，不把“方案已应用”当作“所有碎片已消除”。
   - 能听声音时，可运行 `oilstudio plan preview <方案文件> --index <results 中从 0 开始的条目编号> --out <wav>` 试听接缝。返回 `joinOutputMs` 是接缝在 WAV 中的位置，`ranges` 是保留原声范围。变速、重复、重排、全删或没有麦克风时不支持；没有音频理解能力时跳过试听。
6. 只运行一次 `oilstudio plan submit <方案文件> --compact`，记下 `proposalId`。不要直接改工程文件。
   - 若用户同时要求处理或校对字幕：提交 `plan submit` 后**不要停下等用户先点确认**，紧接着进入「校对字幕」，用 `oilstudio subtitles get <工程> --plan <方案文件> --out <字幕文件>` 按剪后时间线校对并提交 `subtitles apply`。
7. 按 `autoApplied` 处理：为 true 时核对实际 `applied` 与 `skipped`；为 false 时保存 `proposalId`，用 `oilstudio proposal status <proposalId> --wait --timeout 30` 有界等待（用户明确不用等时跳过）。仍待审阅时如实说明待确认与后续待办。实际应用后重新运行 `context <工程> --no-pauses --out <新文件>`，对照本次接受条目的源时间检查残留犹豫音、半句和重复。汇报实际应用数与未处理项，说明可用 ⌘Z 撤销；时长按源时间并集合计，不凭候选数估算。

## 收紧停顿

1. 运行 `oilstudio pauses <工程>`，告诉用户找到几处、能缩短多少。
   - 用户给了停顿门限或保留气口：加 `--threshold <毫秒>`、`--keep <毫秒>`。
2. 用户同意后运行 `oilstudio pauses <工程> --submit`（参数与上一步相同），按共同规则和精剪第 7 步汇报。

## 调整缩放

1. 运行 `oilstudio context <工程> --out <临时文件>`，读 `utterances`、`activity` 和 `zooms`。精剪时可以和精剪共用同一份 context。
2. 读 [缩放判断](references/zoom-judgment.md)，逐段决定哪里该推近、推多近、哪些现有缩放要改或删。
   - 看画面用 `oilstudio frame <工程> --source-ms <毫秒> --zoom none --text --out <png>`：拿到不带缩放的完整屏幕和上面的文字位置。
   - 改完想确认效果时，不带 `--zoom none` 再看一次。
3. 按 [提案格式](references/proposal-formats.md) 把缩放写进方案的 `zooms`；同时在精剪时，剪辑和缩放放进同一份方案。
4. 按精剪第 5–7 步校验、提交和汇报。

## 添加画面元素与打码

用于在录屏中增加标题、标签或静态图片/B-roll，或遮盖敏感信息。先运行 `oilstudio context <工程> --out <临时文件>`，读取现有 `overlays` 与 `redactions`；需要确认画面内容时，用 `oilstudio frame <工程> --source-ms <毫秒> --text --out <png>` 查看带文字识别的画面。

1. 按[提案格式](references/proposal-formats.md)在计划的顶层填写 `overlays` 和/或 `redactions`，可与 `decisions`、`zooms`、`layouts` 放在同一方案。计划里的字段是扁平的；已有 `context.overlays` 的读取结构不必复制成提案结构。
2. 对图片，`sourcePath` 必须是本机图片的绝对路径，也可以引用工程素材目录中已有的文件名。`plan validate` 不会改工程或导入图片；提交被接受后，图片才导入工程素材目录，并按 SHA-256 去重。
3. 运行 `oilstudio plan validate <方案文件>`，修正所有拒绝项后再提交一次校验；通过后运行一次 `oilstudio plan submit <方案文件>`。按回执里的 `applied` 和 `skipped` 核对每个条目。若 `autoApplied: false`，保存 `proposalId` 并按共同规则等待审阅结果；已应用的修改可在 Oil Studio 里按 ⌘Z 撤销。
4. 应用后在相关时间点用 `oilstudio frame <工程> --output-ms <毫秒> --text --out <png>` 检查标题、图片和遮盖的实际画面；用户需要成片时再导出，并检查导出中打码持续覆盖敏感区域。若 OCR 或画面检查仍能看到敏感内容，先调整提案并重新校验，不要把未验证的遮盖说成已完成。

打码区域是源画面上的固定矩形，不会自动跟踪移动对象。对象会移动时，不要承诺自动跟随；需要多个位置时按各自时间与区域单独提出，并逐段检查，无法确定覆盖范围就请用户复核。

## 生成字幕

用户要生成、校对、翻译或导出字幕而工程尚无字幕时，由你执行生成，无需让用户去点击「字幕」标签。

1. 运行 `oilstudio subtitles generate <工程> --engine auto`；需要指定语音语言时加 `--locale zh-CN` 或 `en-US`；纯口播录制无需识别系统音频时加 `--mic-only`。
2. 不需要先打开工程，也不要替用户打开。只有较旧的 App 会返回 `APP_REQUIRED`：这时运行 `open -a "Oil Studio" <工程>`，等 `status.openProjects` 出现该工程后重试。同一生成命令失败两次就按开始前的规则汇报；不要直接读取工程内部缓存目录绕过命令行。
3. 自动模式先用所选地域已配置 Key 的云端识别，否则使用已安装并校验的 Whisper，再考虑系统已安装的可用模型。选中系统识别时，待识别音频超过 5 分钟才会报错，提示检查云端 Key、Whisper 或多版本连接。有效缓存直接复用，纯画面段不计时。确需使用系统识别时显式传 `--engine system` 或 `--allow-fallback`。没有模型时，说明需要在 App 设置配置云端 API Key 或安装本地模型；不索取密钥、不偷偷下载。云端识别会上传工程录音到所选地域；用户指定本地时使用 `--engine whisper` 或 `--engine system`，不走云端。两者都有时默认云端优先。
4. 云端失败不自动反复请求或切换引擎；根据错误说明处理。地域可用 `--region beijing|singapore` 覆盖，不修改 App 偏好。
5. 以最终 `ok: true` 为准，`generated: true` 表示字幕已保存；`generated: false` 表示已有字幕，本次保留。回执中的 `engine` 才是实际引擎，不能把 `auto` 当成本地识别；向用户说明实际用了云端还是本地。随后 `subtitles get` 回读再继续。仅在用户要求重新识别时加 `--force`；已有手工校对的字幕保留。
6. 用户本次要求生成字幕且没有明确不要章节时，继续运行 `oilstudio chapters get <工程>`。`outputDurationMs` 严格大于 180000 且 `chapters` 为空时，按「划分章节」通读刚生成的字幕、生成并应用章节；短视频或已有章节时跳过，不覆盖手动划分。语义划分由你完成，CLI 不会自动生成章节。

用户明确连初始字幕也必须先确认时，`subtitles generate` 没有等待确认的模式；先用 `transcribe` 准备分析并说明此限制。`transcribe` 只准备剪辑分析的发言缓存，不会创建工程字幕。

## 调整工程配置

画幅、背景、光标、摄像头、水印、字幕样式和导出选项都在这里改。先读 [工程配置与导出](references/video-settings-and-export.md)，使用 `settings schema` 获取字段与范围，`settings get <工程>` 获取当前值与指纹，只提交用户要求的字段。`settings apply` 按工程的直接生效设置处理，`--review` 强制确认；等待实际应用、回读后再导出。

## 校对字幕

1. 运行 `oilstudio subtitles get <工程> --out <临时文件>`（若同轮刚提交了精剪方案 `<方案文件>`，加上 `--plan <方案文件>` 按剪后时间线投影 `outputStartMs`、`displayText` 和 `diagnostics`）。
   - 报"没有字幕"：按「生成字幕」执行，成功后用新临时文件名重新读取。
   - 同时读取返回的 `glossary.replacements`、`glossary.hotwords` 以及 `diagnostics`（`inconsistentTerms`、`residualFillers`、`repeatedWords`、`glossaryMatches`、`lowConfidenceWords`、`layoutWarnings`、`overlappingCues`），逐项核对错词、全片大小写一致性、残留书面语气词/口吃重复、超宽/孤字断行与双轨重叠串音；词表不是无条件替换指令，也不读取其他工具的私有配置。
2. 读 [字幕校对](references/subtitle-proofreading.md)，逐句检查：修正有证据的同音错字和专有名词、统一同一术语的大小写、清理因连读或画面操作保留在成片里的书面语气词（如句首或孤立的“呃、嗯、额、啊”）与口吃重复词（如“然后然后”“比较比较”），并处理 `layoutWarnings` 提示的超宽或孤字行。
3. 按 [提案格式](references/proposal-formats.md) 写字幕修改文件，每条的 `expectedText` 从 `subtitles get` 结果的 `text` 原样复制（不是 `displayText`）。
4. 运行 `oilstudio subtitles apply <工程> <修改文件>`，提交时自动核对旧文字。中文字幕校对默认直接调用（不加 `--review`）：即使剪辑提示词里有通用的“修改以方案提交，由我在 App 里确认”，那也是指 `plan submit` 的剪辑方案；除非用户明确要求逐条审核字幕文字修改，否则不要给 `subtitles apply` 加 `--review`。当 App 正在等待用户确认剪辑方案时，不带 `--review` 的 `subtitles apply` 会自动排队（`pendingReason: review_in_progress`），用户点一次确认就会同时生效。
5. 只以回执判断是否生效：`autoApplied: true` 核对 `applied` 与 `skipped`；为 false 时查询 `proposal status --wait`，`pendingReason: review_in_progress` 表示在其他提案后排队。`dismissed` 时检查 `reason`：工程变化或校验失败才基于当前字幕重新准备；`USER_DISMISSED` 不自动重提。
6. 修改生效后，用新文件名再次运行 `subtitles get`，逐条核对改后文字和跳过项，确认 `diagnostics` 中的同名异写、残留语气词/口吃和版式告警已清零，且字幕时间没有被改；有不确定词如实列出。
7. 汇报实际生效条数、两三处重要纠错和未应用项，说明 ⌘Z 可撤销。`glossary` 是学习建议，仍须用户在 App 中加入词库，不把建议已提交说成词库已更新。

## 划分章节

1. 运行 `oilstudio chapters get <工程>`。用户没有明确要求重新划分或增删时，保留已有章节不重复提交；用户明确要求添加、修改或重划章节时，不受视频时长限制，直接按用户要求在现有章节基础上增删或重新划分。
2. 运行 `oilstudio subtitles get <工程> --out <临时文件>`，通读全部字幕；没有字幕时先按「生成字幕」处理。
3. 读 [章节与翻译](references/chapters-and-translation.md) 的"章节"一节，决定章节边界和标题。位置不在章节文件里设置；用户要求顶部或底部时，另用 `settings apply` 修改 `subtitles.chapterProgressPosition`。
4. 按格式写章节文件，运行 `oilstudio chapters apply <工程> <章节文件>`。章节直接生效并自动开启进度条，不需要用户确认，也不要额外等待章节审阅。
5. `autoApplied: true` 时可直接缩短超宽标题并重提，随后用 `chapters get` 回读实际章节数，说明可撤销、可在 App 中修改或删除。仍在排队时，按 `pendingReason` 续接，先把超宽标题和缩短建议告诉用户，或等提案处理完再提交修改。
6. 同一轮还有剪辑方案时，引用剪后仍保留的 `fromCue` 或源时间运行 `oilstudio chapters apply <工程> <章节文件> --plan <方案文件>`，它会自动排在剪辑与字幕提案之后接续生效。

## 英文字幕

1. 运行 `oilstudio subtitles get <工程> --out <临时文件>`。字幕还没校对过时，先问用户是否要先校对：翻译以中文定稿为准。
2. 读 [章节与翻译](references/chapters-and-translation.md) 的"翻译"一节，逐句翻译。原音本来就是英文时，直接校对或导出原字幕，不重复生成翻译。
3. 写翻译文件，运行 `oilstudio subtitles apply <工程> <翻译文件> --locale en`，按共同规则和精剪第 7 步汇报。
4. 用户要文件时运行 `oilstudio subtitles export <工程> --locale en --out <路径.srt>`。

## 导出字幕

运行 `oilstudio subtitles export <工程> --out <路径.srt>`，默认放在工程所在目录、与工程同名。目标已存在时先问用户是否覆盖，同意后才加 `--overwrite`。

## 导出成片

先读 [工程配置与导出](references/video-settings-and-export.md) 的导出一节。运行 `oilstudio export <工程> --out <路径.mp4>`，未指定的参数沿用工程已保存的导出设置；默认放在工程所在目录。支持 MP4 / GIF、极小等质量、H.264 / HEVC / AV1 编码和成片时间范围。

- 要烧录字幕：加 `--subtitles burn`；同时要 SRT：加 `--srt`。
- 目标已存在时先问用户，不自己覆盖。
- 导出可能要几分钟；完成后报告文件路径和时长。
- 刚提交过修改时，确认修改已经生效（`autoApplied: true`，或 `proposal status` 为 `applied`）再导出，否则导出的是修改前的内容。

## 完成时

用两三句话汇报：做了什么、提交了什么（附 `proposalId`）或导出了什么文件、还需要用户做什么。不要贴出整份 JSON。

字幕配音：用户要求 TTS 或外部音频配音时，读取 [字幕配音](references/narration.md)，使用 `narration status / generate / import`；生成和导入直接保存，App 中一步可撤销。
