---
name: laohu-asrcut
description: 根据录音、录屏视频、ASR JSON 或 SRT 制作可追溯的虚拟粗剪、精剪和授权重排，生成剪后时间轴与审阅页；按授权另行导出剪后媒体，并为后续动画提供可靠的讲述定位。
---

开始处理前，先把当前正式入口 SKILL.md 所在目录解析为 `{SKILL_DIR}`，读取 `{SKILL_DIR}/../../../docs/runtime.md` 并沿用本轮任务状态；从工作项目、用户指定路径和已有材料恢复目标、授权与保护项。之后按需读取本 Skill 的输入、剪辑或时间线 Reference。

# laohu-asrcut

剪辑先决定哪些真实声音留在时间线上，再决定字幕怎样呈现。ASR、审阅页和动画都必须能回到同一份源证据与剪辑决定。

## 任务范围与正常交付

承接录音、录屏视频、既有 ASR JSON、SRT、已有虚拟剪辑方案或其审阅意见。用户可以只说“帮我剪一下”，不必先准备字段表；先判断手头材料支持到哪种精度，再完成不依赖缺失材料的部分。

默认制作虚拟剪辑：保留原始识别证据，逐项记录保留、删除、合并、待确认和授权重排，编译唯一的剪后时间轴，并由 laohu-htmlshow 生成可审阅页面。标准交付为 edit-plan.json、timeline.json 和 review.html。只有本轮明确要求并授权试听、导出或应用剪后媒体时，才生成新的媒体文件；原音、原视频和工程不覆盖。

交付给用户时，优先以已成功生成并核验的 review.html 作为人阅读剪辑取舍与待确认项的入口，写明可核对的实际路径；再简要说明 edit-plan.json 记录剪辑决定，timeline.json 保存供后续制作使用的剪后时间线，由本技能的编译器统一生成。仅为真实存在且已核验的文件给出完成路径；若只有方案或部分产物，把其余文件标为待生成/未完成，不提供占位路径，也不称已完成。分别按实际状态报告虚拟计划/时间线、剪后媒体导出与音频听审；无原音时标明媒体导出不可用、听审未执行，只报告已核验的虚拟产物。

本能力以源音频实际保留区间为剪辑决定，同时可在完整声画制作已获授权时，编译有明确用途的 source-free presentation 时段。后者是成片中的独立图像/声音承接时间，不声称来源音频或 ASR 曾存在；不改写讲述内容，也不由 Motion 私自挪动已冻结时间线。删掉识别文字而仍保留那段声音，不算完成音频剪辑；修正识别文字也不改写人实际说过的话。把原始 ASR、确认听到的口语和可选屏幕显示文字分开保存。`spokenCorrections` 逐词/逐句定位，rawText 必须仍等于原识别；未核对修改只能记候选，只有注明音频核听及完全对应源范围的确认修正，才会在编译片段中另附 spokenText。屏显文字只进 `displayText`，不改声音字段。没有原音时只能交虚拟时间线，不能声称听过、试听通过或已生成剪后声音。

## 输入与证据先接稳

先读取当前工作项目的 AGENTS.md、有效项目规则、已确认的音轨对应关系和任务授权。对每个源文件记录稳定 source id、内容哈希、媒体类型、主音轨、采样率/时间基准和已知持续时间；录屏中的麦克风、系统声、摄像机画面或独立录制片段分别标识。只有真实资料给出偏移时才记录音轨偏移。偏移未知时标为 unknown；禁止默认填 0、按文件名猜顺序或把局部时钟当成项目时钟。

原始识别文本、片段顺序、原始时间值和可用词时间须作为证据保存。规范化的整数采样边界与原始时间值并列保存，注明转换采样率和精度来源。没有词级时间的 ASR 或 SRT 保留为句段级；不能按字符长度均分时间，也不能把插值伪装成识别器测得的词时间。SRT 只能支持它给出的字幕段时间范围，不能证明停顿、气口或句内切点。

需要新增识别时，先复用可用 ASR。用户要求剪录音/录屏但没有任何转写时，剪辑意图通常包含取得可用转写；若本地 provider 已配置、上传授权与费用边界已在本任务或项目中明确成立，就直接识别，不要求用户使用“识别/重识别”等术语。若上传授权、费用或媒体限制未覆盖，只暂停识别这一步，先完成不依赖它的材料盘点并指出缺少的授权/成本信息。服务调用必须显式执行，不因音频文件单独出现就上传。极速版调用须先用 ffprobe 验证本地媒体时长，未知或超过两小时即不上传；同时限制大小与格式。原始识别参数关闭语义平滑；先将原始 JSON 保存在新路径，再导入。用户级配置优先、环境变量覆盖，凭据绝不回显。详见 [输入与 ASR 证据](references/input-and-asr.md)。

## 粗剪、精剪与顺序决定

先从完整连续表达中识别主题段、表达单元和可疑剪辑位置，不把 ASR 片段边界直接当成句子边界。粗剪保留叙述者的中心、必要前提、否定/限定、证据和结论；先标记明显误录、无关录制、明确重来段和可疑重复，形成候选与理由，不因停顿、语气词或相似句自动删除。
在用户已授权的完整声画制作中，若仍有会改变节奏、声画呈现或观看时间的新选择，且当前项目资料库已确认存在，则按项目共用[本地作品方法库检索路径](../../../references/exemplar-study.md#从本地作品方法库检索并返回决定)查询相关材料/方法卡、读取选中详情，再回到本次表达决定；同目的已有新鲜查询和必要详情时复用。用户明确提出剪辑表达研究/作品比较或查找剪辑方法时，也按该路径检索相应方法并核读选中原媒介。普通口播转写、精剪保护、锁定纠错/清理、锁定计划或时间轴的忠实执行/编译仍不触发。检索只提供表达选择的参考，不授权重排源音、改变 raw transcript、源时间码或核听证据，也不扩大已授权的编辑范围。

精剪才逐个比较候选：所删语音是否在后文有完整保留，前后是否拼成自然且真实存在的表达，切点是否落在完整词/句边界，是否误删呼吸之外的辅音起音、爆破音、必要停顿或正在演示的系统声。重复内容按最小完整意义单元比较；保留重复句中独有的对象、条件、证据、转折、态度或结论。识别相似度、字数、停顿长度和 VAD 只提出候选，不产生删剪授权。

### 口播与画面节奏

完整口播视频/动画制作已获授权时，主动检查讲述单元与紧接的视觉解释是否需要不同节拍。先核对保留原声中已有且可用的停顿，再判断是否需要补足观看时间；已有停顿足够就不新增，不足才按净差加入 `/2` presentation。普通创作中由作者按画面任务记录决定和预算，不逐段询问用户；纯音频、锁定原音/总长或必须改讲述内容时，暂停冲突部分。源停顿、剪口保护与无源画面时间的证据和分支见 [粗剪与精剪](references/editing.md)；完整插入接口和下游时钟见 [时间线与交接](references/timeline-and-handoff.md)。Motion 的请求只能进入共享 plan 重编译，不能私自移动冻结后的 `filmTimeSec`。

默认保留录制顺序。用户明确要求重点前置、重排或重新组织时，才允许修改顺序；把授权范围与每项重排原因写入方案。修复连续表达和调整整段顺序是两种不同决定，不相互推定。每段删除必须记录源区间与原因；删除重复时另指向保留的完整实例，不能只留一条“已去重复”的结论。

逐源核对已知输入范围是否被标为保留、删除或待确认。未知尾段、缺失时钟、音轨偏移、重叠说话和无法确认的切点列为问题，不把未知范围归成静默。保留静默是保留区间的一部分；只有有证据且满足授权时才删静默。边界切到一个有词级时间的词内部时拒绝编译；句段级材料只能在该句段边界做精剪，句内切点须先获得更可靠的词时间或原音核听。详见 [粗剪与精剪](references/editing.md)。

## 编译、审阅和下游交接

edit-plan.json 是剪辑决定的唯一真源；timeline.json 由本 Skill 的确定性编译器生成，消费者不得自行重算目标时间。`edit-plan/1` 与 `timeline/1` 保留原有 source-only 行为与哈希语义；加入 presentation 后升级为 `/2`，其中 `sequence` 唯一表达 source 与 presentation 的交错顺序，编译器为每个 `timeline/2.units[]` 分配连续目标范围，`timeline.clips[]` 仅是 source-only 派生视图。采用单一项目输出采样率；每个 source range 是主音轨时钟上的半开整数采样范围，presentation 用正整数项目样本时长且无 source range。删除区间关闭目标时间；保留区间中的原有静默仍计入其 source 时长；新增 presentation 的时长只计入独立 unit。每次源片段出现都要有独立 occurrenceId，避免重复素材或同词多次出现时发生身份混淆。唯一编译器负责平移所有后续词与片段，禁止 Motion、字幕和音频消费者自行累计时长。

每次修改剪辑决定或源证据，递增 revision 并重算 planSha256；旧时间线、旧审阅反馈和动画锚点只在 project id、revision、哈希、source id 与 token/occurrence 仍匹配时有效。过期、删除或含糊引用必须报错，不可静默挪到同名词或邻近片段。时间线的 draft/frozen 只表示方案状态；review.status 单独记录未请求、待审阅、通过或要求修改，不得把冻结或哈希有效说成用户已批准、已听审。

调用 laohu-htmlshow，把方案和编译时间线传给其 HTML 展示能力。页面展示原始 ASR、保留区间的实际源词、可选显示文字、源/目标时间、完整留存与删除理由、待确认项和版本状态。若存在真实可访问原音，提供原始区间试听与剪后拼接试听两个独立控件；实际剪后媒体不存在时，拼接试听必须明确禁用，不能假装播放。页面反馈必须绑定 project/revision/planSha256；反馈文件仅供 Agent 复核，不自动改 JSON、应用剪辑或表示审批。详见 [时间线与交接](references/timeline-and-handoff.md)。

时间线供 laohu-motion 读取。asrcut 提供真实保留词实例、句段范围、精度来源、occurrenceId 和统一 targetRange；motion 自行判断哪些词/范围应成为画面动作锚点。一个关键词不自动生成一个动画，动画设计不能复活已删声音或改写口播。若完整声画制作尚未冻结而画面需要可解释的停讲时段，motion 提交边界与阅读/观看任务供 asrcut 作者判断；作者在授权范围内可加入 /2 presentation unit。冻结后任何新增时长都必须回到共享 plan 重新编译和审核；motion 不能自己拉长一镜、平移后续事件或保留一条私有 film clock。普通 source pause 与新增 presentation 不能混作一类：前者是原录音的一部分，后者是有独立决定、视觉/声音 handoff 和目标样本范围的无源画面时段。

当前编译器只接受等速剪切、拼接、已授权重排，以及经授权的 `/2` presentation 插入。有限音频导出器只写新的 PCM WAV：验证被冻结计划、授权、原音哈希、全源时长、主音轨时钟与最新编译时间线，按编译器范围裁切/重采样 source，并按精确项目样本数在 presentation 单元插入零样本。来源片段只导出一次，不分别导出后重播；receipt 将全长新 WAV 标成一条 voice track，voiceWindows 只列 source units 的保守范围，不把无语音证明的原始停顿伪装成 VAD，也不把 presentation 描述成最终混音必须全静音。导出器生成未试听声明的 artifact receipt，不做变速、叠化、交叉淡化、混音、变调、视频导出或工程应用。多轨关联和视频交给对应适配器；依赖未知同步的操作必须拒绝。具体字段、时钟方向、失效规则和命令见时间线 Reference。

## 命令、接口和验证

普通用户只需提供录音/录屏或转写和“帮我剪一下”这类目标；Agent 负责解析转写、形成剪辑判断和校验。下列命令是实现入口，不要求用户手写 JSON：

    node .agents/skills/laohu-asrcut/scripts/asrcut.mjs import --input transcript.json --project-id my-project --out edit-plan.json
    node .agents/skills/laohu-asrcut/scripts/asrcut.mjs merge --project-id my-project --plans mic-a.json,mic-b.json --source-order mic-a,mic-b --out edit-plan.json
    node .agents/skills/laohu-asrcut/scripts/asrcut.mjs compile --plan edit-plan.json --out timeline.json
    node .agents/skills/laohu-asrcut/scripts/asrcut.mjs insert-presentation --plan edit-plan.json --spec presentation.json --out edit-plan.json --authorize-presentation-timing --update-plan
    node .agents/skills/laohu-asrcut/scripts/asrcut.mjs freeze --plan edit-plan.json --out frozen-plan.json
    node .agents/skills/laohu-asrcut/scripts/asrcut.mjs export-audio --plan frozen-plan.json --timeline timeline.json --out cut-audio.wav

已知录音采样率、持续样本数和源媒体时，显式传入 --source、--source-sample-rate、--source-duration-samples；有多个音轨时用 --audio-stream-index 指定原音轨。未知值留空并记录问题。SRT 导入使用相同 import 命令，保存字幕行原时间戳与 evidenceRef，只支持句段精度。多个来源逐一导入后，必须给 `merge` 显式 `--source-order`，不能从文件名猜顺序。Cap 原始文件只有 schema 与 timeBasis 明确匹配时才采用 sourceStartMs/EndMs 作为录音本地时钟，并将 global 时间保留为分开的原序证据；可用 `--recording-segment` 单独导入一个录制段，并按真实源媒体分别关联。

脚本 API：`importAsrJson(raw,{projectId,sourceId,sampleRateHz,sourceSampleRateHz,sourceDurationSamples,mediaPath,mediaSha256,transcriptSha256,timeUnit,evidenceRef,recordingSegment})`、`importSrt(text,options)`、`mergePlans(plans,{projectId,sourceOrder})`、`verifyPlanEvidence(plan,{baseDir})`、`validatePlan(plan)`、`compilePlan(plan)`、`insertPresentationInterval(plan,spec,{authorized})`、`hashPlan(plan)`、`exportAudio({plan,timeline,outPath,tmpDir,baseDir})`。`insert-presentation` 的 `spec` 由作者根据真实视觉/声音任务生成，包含 `id`、`decisionId`、`reason`、`afterOccurrenceId`（仅用来按当前 sequence 找插入边界，不写回 plan）、`sceneId`、`durationSamples`、`visualHandoff`、`audioHandoff` 与当前 revision/hash；它不能绕过任务授权、稳定顺序和失效检查。单输入 `/2` plan 的 `mergePlans` 原样保留 sequence；含 presentation 的多 plan merge 明确拒绝，需先合并来源再编排其间展示段。`verifyPlanEvidence` 对 raw-bytes 模式重新读取 evidenceRef 指向的文件并校验 SHA；相对路径按 edit-plan 文件所在目录解析。`sampleRateHz` 是项目输出时钟，`sourceSampleRateHz` 是源主音轨时钟；导入与编译不触网，识别仅由显式 provider 调用执行。provider API 为 `loadVolcConfig(options)`、`probeAudioDuration(audioPath,options)`、`transcribeVolcFlash({audioPath,config,fetchImpl,ffprobePath,probeDurationImpl})`；其时长探测必须在上传前成功。脚本不会擅自试听、删除或改写源文件。实现细节由 scripts/asrcut.mjs 与 scripts/asr-provider.mjs 承载，不复制第二份时钟算法。

交付前核对完整覆盖及待确认项、保留词未被剪成残片、删除理由与保留实例对应、重排授权、源哈希和时钟、目标时间连续性、revision/hash 一致、输出未与任何输入路径或符号链接/硬链接别名重合。媒体导出还必须有可读取且哈希未变的源媒体、已知持续时间/主音轨时钟、无导出阻断问题与 mediaExport 授权；在同一外接盘写临时文件后原子生成新 WAV 与 artifact receipt，不覆盖源文件或既有目标。receipt 记录样本数、哈希、源区间和 `auditionStatus=not_auditioned`，机械导出成功不等于听审通过。没有满足项时只阻断依赖它的精度或动作，明确报告可继续的虚拟结果与最小补充材料。
