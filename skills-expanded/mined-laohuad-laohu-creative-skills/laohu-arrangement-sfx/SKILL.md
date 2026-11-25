---
name: laohu-arrangement-sfx
description: 当视听声音蓝图已决定某个事件需要 SFX，且需要选择、替换或重新选段时调用；从动作与材料检索真实本地或外部文件，核实来源与许可，可按需剪辑源 WAV 后交回唯一现有音频计划。
---

# Arrangement SFX 选材与源剪辑

本模块只处理已确定事件的 SFX 选材、来源/许可登记与必要的源 WAV 剪辑，不决定全片是否需要声音，不接管旁白、音乐轨迹、静音、电影时间线或最终混音。由父级先读取[视听声音设计与源音频处理](../../references/sound-editing-and-mixing.md)；若由 Motion 调用，还沿用[音乐、音效与静音设计](../../../laohu-motion/references/sound-design.md)对声音职责和唯一 audio-plan 的约定。普通 Motion 请求已授权的声音职责，不需要用户另选本模块或重复授权。

音效属于整段声音编排中的一件材料：返回后要在完整画面和配乐/旁白关系里试听命中点、占位和尾音，不能只按文件标签匹配。公共候选池中的文件继续依逐文件 hash、适用语境与真实完整试听证据判定；新增编辑工具或混音控制不自动提升其 `ready` 状态。音频操作不借用视觉 `motionOperations`。Huashu 音效生成分支支持的 `sourcePan` 仍按源函数行为处理；它不等于 Motion audio-plan 的连续声像控制。

## 触发与输入

触发：一个已确定的视觉 `eventId`/相位确实需要音效，或已有音效需要更换、裁段后重选来源。仅 BGM、原样保留的锁定音轨、完全静音，以及只提到物体或声音但尚未决定加 SFX，都不触发。无旁白不代表静音；是否加音效仍由事件职责决定。

父级准备并传入现有镜头蓝图中的信息：

- 稳定的视觉 `eventId` 和事件相位；若已有时钟，给出成片秒或准确的 `timeMapId` 与局部秒。
- 可听动作、接触物与材料、力度/速度、期望的听觉作用、可用时长和需要避开的旁白/阅读窗口。
- 用户锁定的声音、项目根目录及可写入的项目素材目录；不能为了取得素材更改锁定轨或代理设置。

父级从具体动作和材料生成查询词并自行处理正常创作选择，不要求用户提供 asset ID、剪辑点、曲库筛选项或混音字段。没有合适素材时可报告依赖素材的声音部分暂停；不得冒充已有文件或以任意 tone 替代拟音。

## 先用候选组缩小本地范围，再核验具体文件

先从音效索引中的 `candidateGroups` 按事件动作、材料、力度和可用源时长查找候选组。每组会给一个默认候选、明确条件下的替代项、适用与排除说明；这是根据索引角色、标签和来源标记整理的检索入口，不是完成听审的音效调色板，也不表示听感已经匹配。CLI 的 `--action` 和 `--material` 只接受完整的已知标签或明确列出的正向别名，不按子串猜测，不解析否定或复合语义；如 `non-metal`、`no click`、`wood and metal` 这类表达会返回未确认，不能当作匹配。自然语言放在 `--query` 做粗略候选组查找；最终仍由主线结合事件判断。CLI 按候选节点中结构化的动作、材料、力度和索引源时长筛选；组级 `excludeWhen` 是交给主线结合事件判断的文字说明，不会由脚本自动解释。源时长上限只作索引元数据粗筛，不替代实际探针或人工选段。按当前事件条件选择默认项；只有替代项的具体动作/材料/力度条件更吻合时才改用替代项。条件在索引中未知时保留为未确认，不随机抽选，也不把文件名、搜索命中、响度或技术波形当成听感结论。
若来源索引保留了素材自己的 `use_for`/`avoid_for`、`sync`/`timing`、`adapt.rate`/`notes`、`under_voiceover_db`、`tuning` 或配搭建议，应按当前事件逐项核对这些具体说明；它们是该素材的来源指导，不是全部声音的硬性参数，也不能替代整段试听。`sync.at` 是源文件内命中点，`sync.meets/how` 说明它应该对应画面哪个运动阶段；二者都不是成片时间。若来源建议变速且明确说明音高随速率变化，按允许区间使用 `audio-edit` 的 `playbackRate`，不能用保音高的 `audio-plan.speed` 冒充同一种变化；`adapt.rate:[1,1]` 时不作速率调整。按编辑参数重算/使用回执中的派生 hitpoint。`under_voiceover_db` 只是素材在语音重叠时的来源级增益指引，仍须结合实际旁白试听；它不等于 Motion 自动 ducking 参数。

对选中的 `assetId` 再运行 `local-search`。它会重测实际文件格式、时长和 SHA-256，核对许可与再分发边界，并按当前事件范围检查既有审核记录。每个资产的真实 `reviewStatus` 始终来自索引与精确范围核对；候选组命中、候选顺序、索引标签或 `candidate-unreviewed` 状态都不等于听过或能直接用于正式输出。若索引、文件 hash、许可或审核记录无法对应，标记为待核并继续查其他候选。

本地没有可用匹配时，再判断是否值得查外部候选。检索词由动作、材料/接触面、力度、速度和听觉目的共同确定；例如硬木缓慢合页与金属快速撞击的候选不能只因都含 `click` 就视为可互换。先比对描述、来源页、时长范围与许可筛选是否符合当前事件；下载量、评价和评分仅作辅助信息。搜索返回时长只作粗筛，实际剪辑时钟来自下载文件的探针结果与人工选定的源区间。

所有候选检索调用输出稳定 schemaVersion 1 JSON 到 stdout。`WORK_ROOT` 是宿主解析出的本轮实际工程根目录；cache 默认写入该工程的 `.cache/validation/laohu-arrangement-sfx/<日期>/`；显式指定 `--cache-dir` 时可改用同一工程 `.cache/` 下的位置，不能越出工程或回退到 home/system cache。检索脚本位于 `.agents/skills/laohu-motion/scripts/sfx-sources.py`，由 Arrangement 方法调用；它只用 Python 标准库，外部检索经官方 Freesound API，不抓取网页、不导入或联网下载固定上游 Python 源码，也没有代理、付费或网页抓取回退。先查本地或手工登记且已授权的项目声音，可在无 API 账号时使用。

```sh
WORK_ROOT="<宿主按 runtime 解析的本轮工程根目录>"
SFX_CACHE="$WORK_ROOT/.cache/validation/laohu-arrangement-sfx/$(date +%F)"
SFX_TOOL="$SKILL_DIR/../laohu-motion/scripts/sfx-sources.py"

# 先按已确定事件的动作/材料筛本地候选组；输出包含默认、条件替代及逐项筛选理由。
python3 "$SFX_TOOL" local-groups \
  --query "wood landing contact" \
  --action landing --material wood --intensity light \
  --max-source-duration-sec 0.5 \
  --work-root "$WORK_ROOT"

# 选择条件相符的 assetId 后，再由 local-search 检查文件、许可、hash 与审核范围；不重复下载。
python3 "$SFX_TOOL" local-search \
  --query "wood impact landing" \
  --review-scope "wood contact landing in the current visual event" \
  --work-root "$WORK_ROOT"

# 仅当服务使用条件确认且进程环境配置了 FREESOUND_API_TOKEN 时，才发起外部搜索。
# `--service-use non-commercial` 只用于本次确属非商业且符合 Freesound 条件的请求。
python3 "$SFX_TOOL" freesound-search \
  --query "wood latch close" \
  --license by --pages 1 --limit 8 \
  --service-use non-commercial \
  --work-root "$WORK_ROOT" \
  --cache-dir "$SFX_CACHE"

# 搜索只给 API 的宽泛许可标签。人工核对该音效详情页的精确许可证之后，
# 才提供精确许可 URL 和实际核验人，形成带 rights 记录的候选 plan asset。
python3 "$SFX_TOOL" download \
  --key 'fs:12345' --license by \
  --verified-license-url 'https://creativecommons.org/licenses/by/4.0/' \
  --rights-verified-by '<实际核验人标识>' \
  --out-dir "$WORK_ROOT/assets/audio/sfx" \
  --work-root "$WORK_ROOT" \
  --service-use non-commercial \
  --cache-dir "$SFX_CACHE"
```

示例中的 URL 与核验人必须换成真实核验结果；示例不表示当前候选采用该许可证。`FREESOUND_API_TOKEN` 由操作者在已配置的运行环境提供，不写进 prompt、源码、命令记录或输出日志。若是商业 API 使用，只有在取得并配置 Freesound 个案批准后，才能用 `--service-use commercial-approved --commercial-approval-reference '<批准记录>'`；官方服务条款将商业使用设为需个案处理。未确认服务条件/凭据时不要调用远端，使用本地素材、手工核验文件或保持声音部分待选。

`freesound-search` 使用 token-authenticated `/apiv2/search/` API，缓存官方 JSON 元数据、候选 ID、预览 URI、详情页和宽泛 license label。`configuration_required` 会带非空 `results` 和具体缺少项，可能表示服务用途未确认、API token 缺失、或商业批准记录缺失；不返回空候选冒充搜索成功。`empty` 只在 API 请求成功且确实无候选时成立；网络失败及 rights label 不支持各自保留状态。API 标签不是单文件确切许可，不能据此生成 `audioPlanAsset`。

`download` 只接受此前官方 API 搜索缓存中的 `fs:<数字 ID>`。默认 `--kind preview` 取得 API 提供的高质量 MP3 preview；它不是上传者原文件，也不需要伪称音源原始格式。只有传 `--kind original` 且提供 OAuth2 `FREESOUND_OAUTH_ACCESS_TOKEN` 时，才请求官方 OAuth2-only original download 端点；不能把 API token 当 OAuth 权限，也不能用 preview URL 代替原件。下载后检查实际格式/codec、时长与 SHA-256，并将音源放进工程目录。精确详情页的 licence URL 必须由人工核实后以 `--verified-license-url` 和 `--rights-verified-by` 提供；API 的源码许可证、音效文件许可证与 Freesound API 服务条款是三条独立权限。

API、preview 和 original 下载只允许 HTTPS 的 Freesound 主机及 `cdn.freesound.org`，最多跟随 6 次重定向，并在每次发出后续请求前检查目标。跨主机跳转会移除 `Authorization` 与 `Proxy-Authorization`；因此 OAuth2 凭据不会随 original 下载跳到 CDN。超出主机、协议或端口范围的跳转作为下载失败返回，不访问该地址。

只有精确 CC0 1.0 或 CC BY 1.0/2.0/2.5/3.0/4.0 URL 与 API 宽泛标签一致时，工具才生成带来源/许可字段的 `audioPlanAsset`；其它许可或不确定结果返回 `rights_unverified`。新文件仍为 `candidate-unreviewed`，直到另有完整文件范围的真实试听记录；下载/探针/哈希成功不是声音质量证据。状态还区分网络失败、rights 待核、`probe_unavailable`（退出码 8）、`file_invalid` 与输出冲突。只有 API 实际返回空结果才能记 `empty`。下载成功也不能证明候选听起来合适。

`--review-scope` 由主线根据当前事件语境生成，只在准备检查既有真实审核记录时传入；不要求用户填写。只有当记录的文件 hash 与当前文件一致、适用范围与当前语境一致、源区间覆盖文件从 0 秒到实测完整时长、`reviewer` 是非占位的具体审核者标识且 `conclusion` 为 `pass` 时，适配器才会复用 `ready`。consumer 只检查资产状态和 hash，不读取审核区间；因此局部源区间的听审不能把整份文件交成 `ready`，必须保留 `candidate-unreviewed`。若仅听审部分区间、换用派生文件或事件语境改变，重新听审；确实听审过的派生文件可用它自己的文件 hash 与完整实测区间独立登记。

## 权限、文件和审核状态

每个外部候选至少保留：实际相对文件、实测时长/格式与 SHA-256、创作者、canonical 来源页、精确许可 ID/版本、许可页面标题与 URL、署名要求、同步使用与源文件再分发边界、下载种类及编码说明。默认 preview 是高质量 MP3 编码预览，不是上传者原始源文件；只有 OAuth2 original 端点才交付原件。只有精确核验且当前适用的 CC0 1.0 或 CC BY 具体版本可进入适配器的 `audioPlanAsset`；其它许可、空链接或不确定的边界都保留为待核并停止依赖该文件的正式混音。

新下载文件标记 `candidate-unreviewed`。代码与 hash 只能证明文件身份和技术属性，不代表已经试听；不能把适配器候选改写成 `ready`，不能编造选择后的听感、命中点或人工审核记录。完成真实试听的人可以按本地资产记录方式登记审核证据，至少绑定具体文件 hash、实际源区间、使用语境/适用范围、审核者和 `pass`/其他结论。程序只检查这些记录字段与当前文件/范围是否相符，不能证明记录者真的听过。只有完整覆盖该文件的听审记录才能让整份文件作为 `ready` 复用；局部试听继续是候选。派生文件需以自己的 hash 和完整区间建立记录，之后才可独立复用；事件语境改变时复核。最终混音的听感仍须独立检查。

### 选中真实源文件后，按实际需要剪辑并登记派生音频

只有来源、许可和实际文件已核对后，才决定是否需要把源素材裁到实际动作、淡入/淡出、作技术交叉循环，或把少量各有职责的源层合成一个派生 cue。先从素材起音、主体、尾巴中选择承担当前动作的区间；素材核心动作相近但局部不合时优先剪切、淡化或有意叠层，核心动作/质感不匹配才换候选或原创。选段与变化参数按当前声音任务决定，不为每个候选强制剪辑。

`audio-edit.mjs` 只接受 PCM/float WAV。若已匹配的合法素材是 OGG/MP3 等格式，不能因此丢弃候选，也不能把文件扩展名改成 `.wav`；将原件留在工程中，另在同一获授权工程内解码成 float PCM WAV，再记录原文件 hash/许可、源 codec 与实测时长、实际解码命令、解码 WAV hash/时长。这样只避免再经有损编码，不会恢复源文件已有的有损信息。输出路径必须与源文件不同且不存在：

```sh
SOURCE="$WORK_ROOT/assets/audio/sfx/<已核实源文件>"
DECODED_WAV="$WORK_ROOT/assets/audio/derived/<本次派生名>.wav"
mkdir -p "$WORK_ROOT/assets/audio/derived"
"$MOTION_FFMPEG" -nostdin -n -v error -i "$SOURCE" -map 0:a:0 -vn -c:a pcm_f32le "$DECODED_WAV"
"$(dirname "$MOTION_FFMPEG")/ffprobe" -v error -show_entries stream=codec_name,sample_rate,channels,duration -of json "$DECODED_WAV"
node -e 'const fs=require("node:fs"),c=require("node:crypto"); for(const p of process.argv.slice(1)) console.log(c.createHash("sha256").update(fs.readFileSync(p)).digest("hex"),p)' "$SOURCE" "$DECODED_WAV"
```

按探针确认解码文件确为 WAV/PCM float 且时长合理；保留这些命令结果与原始检索/授权记录。不可变更用户锁定轨或覆盖原素材。

需要编辑时，将已解析的 Arrangement `{SKILL_DIR}` 用于工具路径，将本轮授权工程 `{WORK_ROOT}` 用于源/派生素材，并将 spec 与工作临时文件放在运行约定授予的 `{TASK_TMP_DIR}`；读取[视听声音设计与源音频处理](../../references/sound-editing-and-mixing.md)生成 `audio-edit/1` spec 并调用 `$SKILL_DIR/scripts/audio-edit.mjs`。回执记录源 hash、所选区间、互斥 tempo 或 playbackRate、fade/loop/layer 参数、输出 hash/时长/峰值和按参数几何换算的 hitpoint；它不测真实瞬态，也不证明听感。向父级返回派生 WAV、回执、原资产来源与许可、派生文件自己的 hash/实测时长、语境和 `candidate-unreviewed` 状态。音乐循环还需在完整乐句/和声/尾音及长时间重复上下文判断能否成立。

许可边界分开表达：使用文件同步进动画的权利，与把音频源件随工程或素材包再分发的权利不是同一件事。已知许可证及其 URL 必须随资产一起进入 `plan.assets`；不确定时保留 `rights_unverified`，不得默认 CC0。用户锁定的文件/版本不替换；不接触其锁定音轨。

## 回到唯一音频计划

给主线返回实际文件路径、format/codec、实测时长、hash、canonical 来源页、作者、精确许可标题/版本/URL、署名与再分发边界、候选选择理由、实际可用的 source range，以及审核状态。新检索或下载、尚未人工定位命中点的素材保留 `hitTimeSec: null`，并说明仍待实际试听确定；不能用搜索页的一位小数时长或文件开头冒充人工命中点。已登记素材可能带有索引估算的 `hitTimeSec`、`hitTimeMethod` 和 `hitTimeConfidence`；例如 RMS 帧估算须连同方法及低置信标记保留，只能作为明确说明的技术预览依据，不能写成已听审命中点。

项目内已登记并可直接索引的素材使用其稳定 `assetId`；新外部文件把适配器返回的 `audioPlanAsset` 放进现有 `audio-plan.v1` 的 `assets`，保留其中 `licenseTitle`、`licenseUrl`、`attribution` 和 `source` 字段；`source.soundTitle`、`source.author` 与 `source.recommendedCredit` 带有具体素材名称、作者和可用署名文本，不能只复制资产顶层文件/hash 而丢掉它们。主线在现有事件/资产说明中记录实际选择理由，例如动作/材料与候选描述、长度及许可怎样匹配；不编造评分公式。创建 `events` 时沿用视觉 `eventId`、已选择的相位时点或精确时间映射、源区间和命中点依据。现有 consumer 对 cue 的 `hitTimeSec` 优先用明确值；若 cue 为 `null` 或缺省，则回退到素材 asset 的 `hitTimeSec`；两者都没有时固定取原文件 0 秒，不会自动对齐到裁切的 `sourceInSec`。若选段从 0 秒之后开始而没有提供落在选段内的有效命中点，consumer 会因命中点在选段之外而拒绝；须按真实选段提供明确命中点，或在技术预览中记录覆盖值、假设及所用源区间。cue 设为 `null` 不能屏蔽已登记素材中的索引估算；确认应用估算时保留 `hitTimeMethod` 与 `hitTimeConfidence`，并确保它落在实际 `sourceRange` 内；新音源仍按 `null`/待听审处理。未听审项仍是候选，技术预览须使用现有 `--allow-candidate` 门禁；估算、回退或预览覆盖都不能把候选变成 `ready`。不得新造音频时间线、改动 `audio.mjs` 或要求用户手填内部字段。

适配器检查结果必须由实际计划消费：音效事件使用 `bus:"sfx"`，事件 ID 指向同一视觉事件；计划继续由现有 audio-plan.v1 和 `scripts/audio.mjs` 读取。旁白窗口、仅作用于 music 的 ducking、music 自动化、locked 轨保护、全静音输出和最终封装职责仍归 [Motion 音乐、音效与静音设计](../../../laohu-motion/references/sound-design.md) 与现有 consumer；本模块不替主线决定这些项。

画面模板或其 cue 不自动提供可复用音频。只有本地 catalog 明确登记了可调用的音频源/consumer，且本模块的真实事件接口与许可条件相符时，才按该接口使用；上游 `OM.sfx`、预览声轨或示例 mix 若仍是源码观察，就只作研究记录，不声称本地合成可用或已试听。任何音频事件仍独立写入现有 `audio-plan.v1`，由音频 consumer 渲染并按声音 Reference 实际听审。
