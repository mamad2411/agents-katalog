---
name: oil-studio
description: >
  Use Oil Studio to record and edit local recording projects on macOS: make demos, refine voice-overs, add titles or image overlays, redact screen regions,
  handle captions and chapters, synthesize narration, configure projects, and export video. Use when a user mentions Oil Studio or asks to work on a recording project.
  Not for editing ordinary MP4/MOV files, adding captions to them, or directly changing project files.
  用 Oil Studio 处理本机录屏工程：录制演示、精剪口播、添加标题或图片、遮盖画面、处理字幕与章节、合成配音和导出。用户提到 Oil Studio 或录屏工程时使用。
  不用于普通 MP4/MOV 视频剪辑、加字幕，或直接编辑工程文件。
metadata:
  version: 0.9.14
  minAppVersion: 0.3.26
---

# Oil Studio

For an English conversation, read [the English workflow](en/SKILL.en.md) and follow only that entry. 中文对话使用本页；两版均支持中英文口播，流程和命令相同。命令行输出可用 `--lang en` / `--lang zh-Hans` 指定，不更改 App 偏好；音频语言单独用 `transcribe --locale en-US` / `--locale zh-CN` 指定。

通过命令行 `oilstudio` 操作录屏工程。命令行把结果写成一个 JSON 对象；你负责理解内容和做判断，命令行负责读写工程、校验和执行。

任务导航：[精剪](#精剪) · [画面元素与打码](#添加画面元素与打码) · [生成字幕](#生成字幕) · [校对字幕](#校对字幕) · [导出成片](#导出成片)。其余任务见下方选择表。

## 开始前

1. 用本文件 frontmatter 的 `metadata.version` 运行 `OILSTUDIO_SKILL_VERSION=0.9.14 oilstudio status`。
   - 命令不存在：告诉用户打开 Oil Studio，在「设置 › AI Agent」里点「安装」，然后停止。
   - 有 `skill.compatible` 时，若为 false，向用户转达 `skill.action.message` 和 `skill.action.hint` 并停止；为 true 时继续。若为 null，说明版本未被正确提供，重新核对后停止。
   - 没有 `skill.compatible` 表示 App 版本较旧：按语义版本各段数字比较 `app.version` 与本文件的 `minAppVersion`，版本过低请用户升级 Oil Studio 并停止；版本无法取得时说明无法核对，不用 `cli.version` 代替。
2. 确定工程路径。Oil Studio 工程是以 `.oilstudio` 结尾的包。
   - 用户给了 `.oilstudio` 路径：直接使用。
   - 用户给的是其他录屏软件的工程：运行 `oilstudio import <路径>`，用返回的 `path` 继续，并告诉用户"已转换为 Oil Studio 工程，保存在 <path>，原工程没有改动"。同一工程再次 import 会直接返回已有的转换结果，不会重复复制。
   - 没给：运行 `oilstudio projects`（只列 `.oilstudio`），按标题和时间挑出最可能的一个；有多个候选时列出来请用户选。
3. 失败时读 `error.code` 和 `error.hint`，按提示处理；同一命令失败两次就停下，把 `message` 告诉用户。
   - `SKILL_OUTDATED`：立即停止重试，把 `message` 和 `hint` 告诉用户。
   - `needs_import`：路径不是 Oil Studio 工程，按上一步先 import。
   - `read_only`：工程由更新版本的 Oil Studio 创建，只能读取和导出；不要提交修改，请用户先升级 Oil Studio。

## 选择任务

| 用户要什么 | 走哪一节 |
| --- | --- |
| 录一段某个应用或网页的操作演示 | 录制演示 |
| 按步骤编排网页演示、重点卡片和缩放 | 网页 Playbook 录制 |
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
  - `false`：等用户在 App 里确认。不要说"已剪好"，要说"已提交，等你在 Oil Studio 里确认"。保存 `proposalId` 和尚未完成的后续任务；一次等待超时不代表用户拒绝，也不代表整项任务完成。
  - `true`：修改已经生效（你自己录的工程，或用户为这个工程打开了"AI 的修改直接生效"）。汇报 `applied` 的条数和 `skipped` 的原因，告诉用户可以在 Oil Studio 里按 ⌘Z 撤销；不需要再运行 `proposal status --wait`。
  - 提交前想知道是哪一种：看 context 的 `autoApply`。它为 true 而返回 `autoApplied: false`，说明工程没有在 Oil Studio 里打开，修改会在用户打开工程时自动生效；这时不要接着导出，先告诉用户。
- `subtitles generate` 是生成并保存字幕的 App 操作，完成后可撤销，不经过提案确认；它不同于只生成转录缓存的 `transcribe`。
- `narration generate / import` 生成或导入字幕配音后直接保存；已打开工程通过 App 一步撤销，离线工程检查版本后保存。详见 [字幕配音](references/narration.md)。
- `chapters apply` 始终直接应用，不受工程的自动应用开关影响，也不需要章节确认。`autoApplied: false` 只表示工程未打开、尚未就绪或排在另一个审阅后；按 `pendingReason` 续接，不把它说成等待章节确认。
- 时间只用发言编号（如 `U0012`）或源时间毫秒（`sourceStartMs` 这类字段），剪切与缩放不用成片时间；布局、导出范围明确使用成片时间。
- 在提交最终修改或完成导出之前的中间步骤，每完成一步运行一次 `oilstudio progress "<这一步做了什么>" --step <第几步>/<总步数> --project <工程>`，让用户在 App 里看到进度；最终修改已提交或整项任务完成后不要再调用 `oilstudio progress`。返回 `delivered: false` 表示 App 没开，继续工作即可。
- `--out` 写临时文件时每次用新文件名（例如加上步骤编号）；命令不会覆盖已有文件。
- 提交前必须先校验；校验不通过就修正后再校验，不要跳过。`plan validate` 只检查提交条目是否可执行，不会发现没有写进方案的漏删。
- 标题、标签、图片/B-roll 与打码作为 `plan submit` 的 `overlays`、`redactions` 提案提交；`plan validate` 只校验，不写工程或导入素材。图片只有在应用被接受时才导入工程，并按提交回执核对实际应用与跳过项。
- 用户回来继续、纠正或询问进度时，先查已保存的 `proposal status`。若已 `applied`，基于当前工程自动续做已授权任务，不重复索要确认；若仍在审阅，保留待办。`USER_DISMISSED` 不自动重提；工程变化导致失效时重新取证，不把新指纹直接贴进旧方案。

## 录制演示

你用命令行开始和停止录制，用你自己的工具（Computer Use、浏览器工具）操作被录的应用。先读 [录制](references/recording.md)，里面有操作时的规矩和出错时的处理。录制会生成新工程，所以"开始前"的第 2 步（确定工程路径）在这里跳过。

网页动作多、需要按拍编排缩放或画面解剖卡片时，使用[网页 Playbook](references/recording.md#网页-playbook) 和 `scripts/record_playbook.py`。该流程只通过网页自动化接口操作网页，不使用 Computer Use；**演示录制默认不加字幕（除非用户明确要求加字幕）**。

1. `oilstudio status` 的 `app.running` 为 false：运行 `open -a "Oil Studio"`，等几秒后再查一次。
2. 把要录的窗口准备到开场状态（打开页面、登录、调好窗口大小）。准备过程不录。
3. 运行 `oilstudio record sources`，按 `app` 和 `title` 找到要录的那个窗口，记下 `id`。
   - 录制要过两道授权，都只能由用户完成：macOS 的屏幕录制权限（给 Oil Studio），以及 Oil Studio 里的"允许 AI Agent 发起录制"。第一次使用时 Oil Studio 会弹出确认框，命令会等用户点"允许"；不要自己去点这个确认框，也不要去改系统设置。
   - 返回 `PERMISSION_REQUIRED`：把 `message` 原样告诉用户（它写明了缺哪一项），这一轮到此停止。用户说已经授权后，再从这一步重新开始。
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

## 删除空档

用于没有口播的录屏，或操作之间等待很长的录屏。有口播的录屏优先用"收紧停顿"或"精剪"。

- 你自己刚录的工程：直接运行 `oilstudio idle <工程> --submit`，返回里同时有找到的空档和应用结果，不用先单独查一遍；它会将延迟的点击申报对齐到画面响应，并结合剪辑和变化区域重构自动缩放。
- 其他工程：先运行 `oilstudio idle <工程>`，把找到几处、能缩短多少告诉用户；用户同意后再加 `--submit`（其余参数相同）。
- 想保留更多等待：加大 `--keep <毫秒>`（每处空档两端保留的时间，默认 400）；只想删长等待：加大 `--threshold <毫秒>`（默认 1500）。
- 提交后按共同规则里的 `autoApplied` 汇报。没有找到空档时不会提交任何东西，返回里也没有 `proposalId`。

## 精剪 + 字幕一气呵成（标准命令流）

用户同时要求“剪辑视频 + 处理字幕”时，按以下 5 步在同一轮连续执行，**不要在提交剪辑方案后停下等用户点确认**：

```sh
# 1. 若尚无字幕（subtitles.count == 0），先生成初始字幕与转录缓存
oilstudio subtitles generate "<工程>" --engine auto

# 2. 导出剪辑上下文与停顿清理草案
oilstudio context "<工程>" --out "$WORK/01-context.json"
oilstudio pauses "<工程>" --out-plan "$WORK/02-plan.json"

# 3. 在 02-plan.json 中追加语义删减，做口头禅覆盖检查、校验并提交剪辑方案
python3 -B "<Skill目录>/scripts/check_filler_coverage.py" --context "$WORK/01-context.json" --plan "$WORK/02-plan.json" --out "$WORK/03-coverage.json"
oilstudio plan validate "$WORK/02-plan.json"
oilstudio plan submit "$WORK/02-plan.json"

# 4. 带 --plan 读取剪后可见字幕与自动诊断清单（无需等待用户先在 App 里点应用）
oilstudio subtitles get "<工程>" --plan "$WORK/02-plan.json" --out "$WORK/04-subtitles.json"

# 5. 清零 diagnostics 中的错词、大小写不一、残留语气词/口吃与断行告警，直接提交字幕修改（不加 --review）
oilstudio subtitles apply "<工程>" "$WORK/05-subtitle-edits.json"
```

需要章节时，可在第 1 步后用 `--plan` 读取剪后字幕并准备章节；等剪辑实际应用后，再按「划分章节」对当前工程提交，避免剪辑前的指纹失效。

## 精剪

1. 运行 `oilstudio context <工程> --transcript-first --out <临时文件>`，读取这个文件。
   - 用户同时要求处理字幕且 `subtitles.count` 为 0 时：直接先运行 `oilstudio subtitles generate <工程> --engine auto`（它会一次生成工程字幕与转录缓存），完成后再用新文件名重新取 context。
   - 只做剪辑且 `utterances` 为空：先运行 `oilstudio transcribe <工程>`，完成后用新文件名重新取 context。
2. 先自动清理停顿：运行 `oilstudio pauses <工程> --out-plan <清理草案.json>`，读取 `planPath` 指向的方案。它只生成草案，不会提前剪工程；保留指纹与 `decisions`，后续语义删减追加到同一份方案。
   - 草案已经包含字词边缘保护，不要再把每个切口改成“开始加 50 ms、结束减 50 ms”。需要额外气口时只通过 `pauses --keep <毫秒>` 设置一次；用户没指定时沿用默认值。
   - 清理失败就按提示处理，不静默跳过；没有停顿时 `decisions` 为空，继续找重说。
   - 草案与 context 的两份指纹必须一致；不一致说明工程已变化，重新读取 context 和草案。
3. 读 [剪辑判断](references/editing-judgment.md)，通读全部发言，找重说、口误、放弃的半句与可独立删除的口头禅。语义判断使用源时间；清理只影响预期成片节奏，原声仍包含拟删停顿。
   - 用户指定了风格（保守 / 标准 / 紧凑）就按风格；没指定用“标准”。
   - 对 `fillerCandidates` 全量逐项复核，按[剪辑判断](references/editing-judgment.md)区分无词义犹豫音、语气词和有语义的词。每个候选必须有 `cut`、`keep` 或 `review` 及具体理由；被整段重说删减完整覆盖的记为已覆盖，不重复切。
   - `utterances[].audio` 包含置信度、字速、响度、句内停顿与未识别人声；`screen` 是画面 OCR 时间线。它们是证据，不直接决定删减，不把未识别当成应删除。
   - 听原声：`oilstudio audio <工程> --source-ms <起>,<止> --out <wav>`，最长 60 秒。
   - 看画面：`oilstudio frame <工程> --source-ms <毫秒> --zoom none --text --out <png>`；看一段用 `oilstudio storyboard <工程> --utterances <起>-<止> --out <png>` 或 `--source-ms <起>,<止>`，最长 40 秒。`--every 1000` 控制截图间隔，`--no-frames` 只看声音和文字。
4. 按 [提案格式](references/proposal-formats.md) 在清理草案中追加语义删减与候选保留/复核结论；需要调整缩放时一起写进 `zooms`。按其中的覆盖检查确认没有漏查候选，统计整段覆盖、单独删减、保留和待复核。不能只挑少数长“呃”，或只报停顿数量就结束精剪。重叠删减不重复计时；没有可执行修改时不提交空方案。
5. 运行 `oilstudio plan validate <方案文件>`，修正所有 `rejected` 后重新校验；`uncheckedByDefault` 留给用户复核。
   - `cutAdjustments` 包含已核对的字词接缝校准和严格静音收尾；试听、提交与字幕预投影使用同一套范围。`boundaryReviews` 表示边界外仍有未确认可删的内容，已保留并写入条目说明；核对这些具体接缝，不把“方案已应用”当作“所有碎片已消除”。
   - 能听声音时，可运行 `oilstudio plan preview <方案文件> --index <results 中从 0 开始的条目编号> --out <wav>` 试听接缝。返回 `joinOutputMs` 是接缝在 WAV 中的位置，`ranges` 是保留原声范围。变速、重复、重排、全删或没有麦克风时不支持；没有音频理解能力时跳过试听。
6. 只运行一次 `oilstudio plan submit <方案文件>`，记下 `proposalId`。不要直接改工程文件。
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

1. 运行 `oilstudio subtitles generate <工程> --engine auto`；需要指定语音语言时加 `--locale zh-CN` 或 `en-US`。
2. 遇到 `APP_REQUIRED`：运行 `open -a "Oil Studio" <工程>`，等待 `status.openProjects` 出现该工程后重试。同一生成命令失败两次就按开始前的规则汇报。
3. 自动模式先用所选地域已配置 Key 的云端识别，否则使用已安装并校验的 Whisper，再考虑系统已安装的可用模型。没有模型时，说明需要在 App 设置配置云端 API Key 或安装本地模型；不索取密钥、不偷偷下载。云端识别会上传工程录音到所选地域；用户指定本地时使用 `--engine whisper` 或 `--engine system`，不走云端。两者都有时默认云端优先。
4. 云端失败不自动反复请求或切换引擎；根据错误说明处理。地域可用 `--region beijing|singapore` 覆盖，不修改 App 偏好。
5. 以最终 `ok: true` 为准，`generated: true` 表示字幕已保存；`generated: false` 表示已有字幕，本次保留。回执中的 `engine` 才是实际引擎，不能把 `auto` 当成本地识别；向用户说明实际用了云端还是本地。随后 `subtitles get` 回读再继续。仅在用户要求重新识别时加 `--force`；已有手工校对的字幕保留。
6. 用户本次要求生成字幕且没有明确不要章节时，继续运行 `oilstudio chapters get <工程>`。`outputDurationMs` 严格大于 180000 且 `chapters` 为空时，按「划分章节」通读刚生成的字幕、生成并应用章节；短视频或已有章节时跳过，不覆盖手动划分。语义划分由你完成，CLI 不会自动生成章节。

用户明确连初始字幕也必须先确认时，`subtitles generate` 没有提案模式；先用 `transcribe` 准备分析并说明此限制，不把生成保存伪称为提案。`transcribe` 只准备剪辑分析的发言缓存，不会创建工程字幕。

## 调整工程配置

先读 [工程配置与导出](references/video-settings-and-export.md)，使用 `settings schema` 获取字段与范围，`settings get <工程>` 获取当前值与指纹，只提交用户要求的字段。`settings apply` 按工程的直接生效设置处理，`--review` 强制确认；等待实际应用、回读后再导出。

## 校对字幕

1. 运行 `oilstudio subtitles get <工程> --out <临时文件>`（若同轮刚提交了精剪方案 `<方案文件>`，加上 `--plan <方案文件>` 按剪后时间线投影 `outputStartMs`、`displayText` 和 `diagnostics`）。
   - 报"没有字幕"：按「生成字幕」执行，成功后用新临时文件名重新读取。
   - 同时读取返回的 `glossary.replacements`、`glossary.hotwords` 以及 `diagnostics`（`inconsistentTerms`、`residualFillers`、`repeatedWords`、`glossaryMatches`、`lowConfidenceWords`、`layoutWarnings`），逐项核对错词、全片大小写一致性、残留书面语气词/口吃重复和超宽/孤字断行；词表不是无条件替换指令，也不读取其他工具的私有配置。
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
5. `autoApplied: true` 后再次 `chapters get` 回读，汇报实际章节数，并说明可撤销、可在 App 中修改或删除。为 false 时按 `pendingReason` 处理工程未就绪或排队状态。
6. 同一轮还有剪辑方案时，等剪辑实际应用后再按当前工程提交章节；不要用剪辑前的旧指纹让章节排队失效。

## 英文字幕

1. 运行 `oilstudio subtitles get <工程> --out <临时文件>`。字幕还没校对过时，先问用户是否要先校对：翻译以中文定稿为准。
2. 读 [章节与翻译](references/chapters-and-translation.md) 的"翻译"一节，逐句翻译。原音本来就是英文时，直接校对或导出原字幕，不重复生成翻译。
3. 写翻译文件，运行 `oilstudio subtitles apply <工程> <翻译文件> --locale en`，按共同规则和精剪第 7 步汇报。
4. 用户要文件时运行 `oilstudio subtitles export <工程> --locale en --out <路径.srt>`。

## 导出字幕

运行 `oilstudio subtitles export <工程> --out <路径.srt>`，默认放在工程所在目录、与工程同名。目标已存在时先问用户是否覆盖，同意后才加 `--overwrite`。

## 导出成片

先读 [工程配置与导出](references/video-settings-and-export.md) 的导出一节。运行 `oilstudio export <工程> --out <路径.mp4>`，未指定的参数沿用工程已保存的导出设置；默认放在工程所在目录。支持 MP4 / GIF、极小等质量、HEVC 压缩和成片时间范围。

- 要烧录字幕：加 `--subtitles burn`；同时要 SRT：加 `--srt`。
- 目标已存在时先问用户，不自己覆盖。
- 导出可能要几分钟；完成后报告文件路径和时长。
- 刚提交过修改时，确认修改已经生效（`autoApplied: true`，或 `proposal status` 为 `applied`）再导出，否则导出的是修改前的内容。

## 完成时

用两三句话汇报：做了什么、提交了什么（附 `proposalId`）或导出了什么文件、还需要用户做什么。不要贴出整份 JSON。

字幕配音：用户要求 TTS 或外部音频配音时，读取 [字幕配音](references/narration.md)，使用 `narration status / generate / import`；生成和导入直接保存，App 中一步可撤销。
