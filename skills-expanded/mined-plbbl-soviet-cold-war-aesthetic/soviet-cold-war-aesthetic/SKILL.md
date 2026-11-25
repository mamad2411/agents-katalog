---
name: soviet-cold-war-aesthetic
description: "Provide historically situated art direction for original Soviet Cold War visual language: classify references, choose the period and branch, define content-weighted composition, palette, print treatment, typography handoff, motion logic, critique criteria, no-image visual contracts, and downstream image prompts. Use for historical visual analysis and original briefs about space science, public construction, labor and education, peace/nuclear anxiety, Marxist-Leninist ideology, international friendship, or Intourist tourism. This is an aesthetic-guidance skill, not an image-generation or image-editing skill: it does not call image APIs or create the final bitmap. Do not use for wartime mobilization, 1919–1930s constructivism, or non-Soviet labor posters."
---

# 苏联冷战海报美学

## Mission

把 1957—1980 年代苏联冷战时期的海报机制转译成可执行的视觉合同：原创海报方向、短视频画面、动效、旁白和声音设计，以及可交给下游图像工具的提示词。默认从“公共系统正在被建成、使用和延伸”的结构出发，而不是从红色符号或复古滤镜出发。

核心句：

> 把一个社会对未来的想象，组织成可以远读的公共系统。

这里的“冷战美学”不是只有火箭，也不是泛化的红蓝复古。它包含科学竞赛、工业建设、劳动教育、和平与核威胁、马克思主义—列宁主义的官方谱系、国际友谊，以及面向外国游客的 Intourist 视觉。这里处理的是历史视觉机制的研究与原创转译，不把历史口号自动当成当代政治主张。它既可以为下游生图提供完整方向，也可以在不生图时输出可交给设计师、排版师、动效师的视觉合同。

## Tool boundary

本 skill 只负责艺术指导，不负责绘图执行。

- 负责：历史分支判断、参考图分类、社会承诺、主体优先级、版式模式、比例、色彩、材质、字体交接、动效/声音逻辑、视觉批评和下游提示词。
- 不负责：调用 GPT Image 或其他图像 API，不上传/编辑图片，不返回“已经生成”的位图结果，也不替用户保证中文或俄文在图像模型中的准确渲染。
- 当用户需要最终图片时：先使用本 skill 产出 `IMAGE-DIRECTION` 或 `NO-IMAGE-DIRECTION` 合同，再由环境中独立的图像生成/编辑工具执行；重要文字仍应后期排版。

## Golden reference protocol

当用户给出一张“我喜欢这个版本”的参考图时，先把它标成 `GOLDEN-REFERENCE`，其构图、密度、材料和色彩优先级高于本技能的通用冷战符号。不要因为出现“苏联”就自动加入红星、锤镰、火箭、俄文口号或黑色宇宙。

本项目当前锁定的黄金锚点是：**`BUILDING-SYSTEM / STRUCTURED-SYSTEM` 结构化建设系统海报**。黄金参考资产见 `assets/golden-reference-structured-system.png`。它是本技能的工作参考，不声称是某张历史原作；借用的是冷战公共建设、教育、工业与对外现代化宣传的版式机制：

- 3:4 竖幅；四周保留薄的暖纸边，主体内容约占 94%—96%；
- `GOLDEN-SYSTEM` 专属：左侧约 35%—50% 是连续奶油色功能性文字区，作为标题、引文和口播字幕的安全区；这个比例只在复现这张参考图或用户明确要求“大留白版式”时采用，不是全技能默认值；
- `GOLDEN-SYSTEM` 专属：右侧约 45%—55% 由一个向上延伸的多层平台/结构体占据，平台从右边切出画面，形成强烈右重心；主体优先版式可以让结构体更大、更居中或更偏向视觉焦点；
- 主结构由 4—6 条水平平台、1—3 根竖向支撑/色柱、少量连接线和节点组成；它是“系统的剖面”，不是办公楼效果图；
- 平台上放极小的人物、桌面、工具、课堂、车间或档案符号，只作为尺度和劳动关系，不做场景拼贴；
- 下方约 20%—35% 是远山、水面、道路、树木或台地，作为公共系统的地理/生产基座；环境不应抢过右侧结构；
- 以奶油旧纸、深海军蓝、蓝灰、橄榄绿、赭黄/金黄为主，红色只作小面积行动标记；
- 使用硬边平涂、有限套色、细均匀纸纤维/网点和轻微套印偏差；不使用体积光、镜头光晕、金属反射、渐变或重度做旧；
- 在 `GOLDEN-SYSTEM` 中远读先读“右侧系统轮廓 + 左侧标题区”；在主体优先或金句优先版式中，先读选定的主体或标题，再读平台上的人和工作，最后读环境与印刷细节；不要把画面变成 UI 卡片墙。

### Golden reference priority order

出现冲突时按此顺序裁决：

1. 主体/标题必须先被看见；如果大留白削弱主体，先缩小留白，不得为了守比例牺牲内容识别；
2. 使用 `GOLDEN-SYSTEM` 时才执行“左侧大留白 + 右侧多层平台 + 下方环境基座”的固定骨架；其他版式按内容优先级重新分配面积；
3. 观看语气：建设中、可使用、可继续扩展、公共机构感，而非战斗动员；
4. 结构关系：平台—人物—工具—连接线必须形成一个工作的系统；
5. 色彩与材料：奶油旧纸 + 蓝灰/橄榄/赭黄套色；时代符号只有在 brief 需要时才加入。

### Content-weighted layout modes

在写 prompt 或视觉合同前，先选择一个版式模式。没有用户明确要求时，按内容选择，不把黄金参考图的留白比例自动复制到所有任务：

- **`GOLDEN-SYSTEM` / 黄金参考复刻**：用于明确要求“像这张参考图”、公共建设长版海报或短标题。左侧功能性文字区约 35%—50%，右侧结构约 45%—55%，下方环境基座约 20%—35%。左侧必须实际承载标题/引文；没有文字时不得留下空洞的大白块。
- **`FOCUS-SYSTEM` / 主体优先**：用于视频封面、产品发布、单个概念、人物/火箭/工厂主体和需要强钩子的画面。主主体或系统总轮廓约占可见画面 55%—70%，文字区约 15%—30%，可居中、偏左或偏右；连续无功能留白通常不超过 25%。
- **`QUOTE-SYSTEM` / 金句优先**：用于马克思主义经典引文、问题意识和长标题。真实文字块约占 35%—55%，主体/系统约占 30%—50%，其余只保留 10%—25% 的呼吸空间；文字后期准确排版，不能用假文字填空。

共同规则：留白是服务信息的功能区，不是审美目标；文字区面积按真实文案的字数、行数和层级计算，并只加必要内边距。若 brief 没有标题、引文或字幕，禁止预留大块连续空白。缩略图缩到约 25% 尺寸时，主体轮廓或主标题必须在一秒内可辨；若不可辨，优先扩大主体/标题、压缩装饰和留白。

### Translation rule for non-historical subjects

把现代产品、软件或抽象概念转译成“正在工作的公共基础设施”，只借用传播机制，不复制历史对象：

- 产品承诺 → 选定版式中的主系统/平台总轮廓；`GOLDEN-SYSTEM` 从右侧切入，`FOCUS-SYSTEM` 可占据中央或形成更大的偏置主体；
- 功能或工作流阶段 → 4—6 条平台层，不写成 UI 卡片；
- 用户/劳动者 → 平台上的极小人物和工具，最多 6—12 个尺度符号；
- 数据、协作、版本流转 → 1 条主连接线或 1 组节点，不能铺满网络；
- 现实环境 → 下方山水、道路、桥、树木或台地，说明系统有社会和地理基础；
- 标题/引文 → 选定版式中的功能性文字区，全部后期真实排版，不默认放在左侧。

允许出现抽象的建筑/基础设施剖面，但必须是公共系统的图形化剖面，不是写字楼、SaaS 仪表盘、卡片墙、产品截图或密集 UI。平台是大关系，不能被细节切碎。

## Historical boundary

默认主范围：1957—1980 年代。用以下三个主分支组织素材：

### A. 1957—1965：太空时代 / 科学未来

代表结构是火箭、轨道、卫星、原子、地球、星空、无线电、科学家和向上斜线。颜色鲜明，蓝、红、白、黄、橙可以并置；画面相信科学和劳动能够把未来变成现实。

空间科学校准重点：火箭、轨道、地球、红色手势和宇航员通过大块关系组织未来叙事。

### B. 1965—1982：建设、制度与和平

代表结构是工人、工厂、城市、学校、地铁、公共设施、马克思/列宁肖像、和平鸽、旗帜、成组人物和大块文字。它更正式、更稳定、更像公共机构持续发布的视觉系统，常用红、米白、黑、暗蓝、黄。本技能当前的默认子语法 `STRUCTURED-SYSTEM` 属于这一分支：用右侧多层平台、微型劳动者、连接线和下方环境基座，把“制度正在工作”画成一个可远读的系统剖面。

建设与制度校准重点：劳动、教育、工业、和平与公共设施形成可读的工作系统；早期工业化样例仅作为历史旁支，不作为本技能的主年代样本。

### C. 1950—1980 年代：Intourist / 对外旅游图形

旅游与文化外交校准样例体现了苏联对外旅游海报的另一面：地标、风景、交通、地图、火箭、海岸和现代化国家形象。它们属于冷战时期的文化外交与旅游传播，但不等于共产主义意识形态宣传。

使用时标记为 TOURISM / 对外宣传，不要把它们和 IDEOLOGY / 意识形态混成一套。

## Exclusion boundary

- 1941—1945 的战时命令、母亲、前线、保密和牺牲属于 soviet-wartime-aesthetic；
- 1919—1930 年代 ROSTA、构成主义、早期摄影蒙太奇和第一轮工业化海报属于早期苏联旁支；
- 早期工业/现代主义样例只能用于研究来源，不能单独证明冷战年代；
- 非苏联工运图形不能作为苏联海报的直接风格依据；
- 来源不明的后期复古再设计不能作为历史证据，除非先查到原始出处；
- 不能用“俄罗斯”“红色”“锤镰”三个符号替代年代判断。

## Invocation routing

根据交付物选择分支：

- 科学/航天：使用 SPACE-SCIENCE，强调轨道、比例关系、上升线和红蓝黄系统；
- 劳动/工业/马克思主义：使用 `BUILDING-SYSTEM / STRUCTURED-SYSTEM`，先按内容选择 `QUOTE-SYSTEM`（经典引文/长标题）、`FOCUS-SYSTEM`（封面/单一钩子）或 `GOLDEN-SYSTEM`（明确复刻参考图）；
- 和平/核威胁：使用 PEACE-NUCLEAR，强调强烈单一符号、黑色空间、白色线条、警示性大字；不因“留白”而削弱单一符号；
- 国际旅游：使用 TOURISM-Intourist，强调风景、地图、地标、交通和对外可读性；不要自动加意识形态口号；
- 若用户明确偏爱本项目的黄金参考图：使用 `BUILDING-SYSTEM / STRUCTURED-SYSTEM`，优先执行右侧平台系统、左侧留白、下方环境基座，不使用单一地貌默认语法；
- 现代产品发布：默认使用 `STRUCTURED-SYSTEM / FOCUS-SYSTEM`，把产品承诺转成“正在工作的公共基础设施”；只有 brief 明确要求复刻黄金参考图时才切换 `GOLDEN-SYSTEM`；不把产品画成政治宣传、火箭、普通写字楼或 UI 截图；
- 只有当用户明确要安静的风景目的地、没有平台/工作系统时，才使用 TOURISM-Intourist 的低密度风景子语法；
- 视频画面：先做完整静态母版，再让模块像机械系统一样拼接、轨道运行或向上展开；字幕安全区按实际字幕长度设置，不自动制造大块无内容留白；
- 美学批评：先判定分支和年代，再指出是否串入卫国战争近景警报、1920 年代构成主义或商业科幻；
- 下游图像工具：本 skill 只输出艺术指导和可复制的 prompt，不调用 GPT Image 或其他图像 API；由调用方决定是否交给独立的图像生成/编辑 skill 执行。准确中文/俄文尽量后期排版。

## Delivery mode

先判断用户要哪一种交付，不要默认生图：

- `NO-IMAGE-DIRECTION`：只输出给设计师/排版师/动效师的视觉合同，不调用图像工具，不虚构图片结果；
- `IMAGE-DIRECTION`：输出视觉合同和可直接交给 GPT Image、其他图像模型或设计师的 prompt；本 skill 不调用图像工具，并明确哪些文字必须后期完成；
- `CRITIQUE`：只评估现有图，不擅自重绘；给出 aligned / partially aligned / not aligned，以及只改一个变量的修订；
- `VIDEO-DIRECTION`：输出静态母版规范、镜头/模块顺序、动效和声音，不用动效形容词替代时间轴。

当用户没有指定分支、但给出类似本项目黄金参考的结构化右侧平台系统时，默认使用 `BUILDING-SYSTEM / STRUCTURED-SYSTEM`，不要先问用户是否要“苏联红色”；直接依据平台、人物、连接线、环境基座和纸墨关系制定方向。

`NO-IMAGE-DIRECTION` 的最低输出字段必须包含：

1. branch / period / audience / social promise；
2. selected layout mode and content priority；
3. visual thesis（一句话）；
4. canvas and safe areas；
5. zone map with approximate ratios；
6. primary silhouette and 2—3 supporting layers；
7. shape grammar and density limits；
8. palette with color roles；
9. typography and exact copy placement；
10. material/print treatment；
11. prohibited drift；
12. three-glance / thumbnail test；
13. handoff checklist。

不得把“风格很复古、很苏联、很有未来感”当作设计指导的结论；每一项都要落到比例、位置、数量、颜色角色或制作动作。

## Modern product launch profile: STRUCTURED-SYSTEM

当测试对象是软件、服务、知识系统或抽象产品时，先使用 `FOCUS-SYSTEM`；只有黄金锚点明确要求复刻用户选定的右侧平台系统海报时，才使用 `GOLDEN-SYSTEM`。以下合同先锁定信息优先级，再锁定几何关系：

- **传播语气**：像公共建设、教育设施或新系统启用公告，可信、克制、明亮、带制度重量；不是 SaaS 发布页、融资海报或科技大片。
- **版式选择**：`GOLDEN-SYSTEM` 执行左侧 35%—50% 功能性文字区与右侧平台；`FOCUS-SYSTEM` 让主体/系统占 55%—70%，文字区只占真实文案所需的 15%—30%，文字可位于顶部、底部、左侧或主体旁；`QUOTE-SYSTEM` 让准确文字块占 35%—55%，主体占 30%—50%。
- **功能性留白**：连续空白只保留给真实标题、引文、Logo 或字幕；没有实际内容就压缩、裁切或用主体关系填回。`GOLDEN-SYSTEM` 的大留白是参考图特征，不是内容不足时的默认补位。
- **右侧主系统**：在 `GOLDEN-SYSTEM` 中让从右边切出的结构体占宽度 45%—55%、高度 55%—80%；在 `FOCUS-SYSTEM` 中允许结构体扩大到 55%—70% 并进入中央，以确保主体先被看见；由 4—6 条水平平台组成，平台宽度递减/错位，形成向上延伸的系统剖面；不要做对称楼房。
- **平台关系**：每层平台只表达一种工作状态（生产、学习、协作、测试、交付等），每层最多 2—4 个极小人物/工具符号；不要把每层画成独立房间或场景插图。
- **支撑元素**：使用 1—3 根赭黄/橙黄竖向支撑色柱，或一条细连接线/节点链，贯穿部分平台；它表示基础设施关系，不是装饰。
- **环境基座**：下方 20%—35% 放远山、水面、道路、树木、桥或台地；环境以蓝灰/橄榄/赭黄压平处理，作为系统的社会地理基座，不抢主结构。
- **人物尺度**：人物必须小、成组但不抢戏；禁止大头像、英雄姿态、会议合照和情绪化肖像。人物的作用是证明平台有人使用、劳动和学习。
- **文字与符号**：准确中文/俄文/英文、Logo、引文、日期、二维码全部后期排版；图像阶段只留干净文字区，最多保留极少量无意义几何节点。
- **密度预算**：主平台 4—6 层；竖向色柱 1—3 根；主连接线 0—1 条；每层人物/工具 2—4 个；全图可辨识小对象不超过 18 个；禁止 3×3 卡片、密集图标和假 UI。
- **抽象边界**：允许结构化剖面，但必须看起来像公共系统/生产教育基础设施的图形化组织，不像商业办公楼、建筑可视化、软件截图或现代企业信息图。

### STRUCTURED-SYSTEM self-test

生成或交稿前遮住所有文字，问三句：

1. 第一眼能否读出当前模式规定的主标题/主体：`FOCUS-SYSTEM` 先读主体，`QUOTE-SYSTEM` 先读标题，`GOLDEN-SYSTEM` 先读左侧标题区与右侧平台总轮廓？
2. 第二眼能否读出平台上有人在生产、学习、协作或交付，而不是一栋普通办公楼？
3. 第三眼是否发现纸、墨、层次、微型人物和环境基座，而不是假文字、功能图标或 UI 卡片？

若第一问失败，先扩大主体/标题、缩小无功能留白并合并平台轮廓；若第二问失败，补足平台—人物—工具的关系，不增加装饰；若第三问失败，减少小对象和纹理，不增加文字。

### Platform-system test

在 `STRUCTURED-SYSTEM` 中，平台必须形成一个可一眼识别的整体轮廓；不论它位于右侧还是更居中，都应读成“一个向上延伸的公共系统”，而不是若干互不相关的房间。若平台被细节切碎，删减场景；若平台像普通写字楼，增加切边、错位、环境基座和微型劳动关系，不添加玻璃幕墙或现代建筑光效。

### Subject-prominence gate

- 缩略图约 25% 尺寸时，主标题或主体轮廓必须在一秒内被识别；
- `FOCUS-SYSTEM`：主体/系统总轮廓目标为可见画面的 55%—70%；
- `QUOTE-SYSTEM`：文字块目标为 35%—55%，不能因为留白把金句压成细小角落；
- `GOLDEN-SYSTEM`：允许左侧 35%—50% 大留白，但它必须承载实际文字；若最终无字，缩小文字区并放大主体；
- 任何模式都不得用连续空白替代内容。主体不突出时，修订顺序为：扩大主体 → 提高明暗/色彩对比 → 减少支撑细节 → 缩小留白，而不是反过来扩大留白。

## Non-negotiable creative principles

1. 结构先于装饰。先划定大块、方向线、主体尺度和文字区，再放火箭、地球或人物。
2. 每个物件都必须属于一个系统。火箭要和轨道、地球、科学或制度连接，工人要和工具、工厂或教育连接。
3. 未来必须有生产基础。不把宇宙画成魔法，不让火箭脱离劳动、科学和国家基础设施。
4. 模块必须是大版块，不是 UI 卡片。允许切边、重叠、碰撞、错位；禁止 3×3 小卡片网格。
5. 文字是版式骨架。一条主标题、一条辅助宣告、少量编号/地点/年份足够；长文放后期。
6. 乐观也要有制度重量。不是霓虹赛博未来，而是纸张、印刷、工厂、学校、档案和公共墙面的未来。
7. 对外旅游与意识形态必须分层。旅游海报可以明亮、优雅、图形化，但不自动等于马克思主义宣传。

## Required workflow

### 1. Select a branch and social promise

填写：

- branch：SPACE-SCIENCE / BUILDING-SYSTEM / PEACE-NUCLEAR / TOURISM-Intourist；
- audience：国内群众、工人/学生、国际游客或青年；
- social promise：科学进步、共同建设、和平安全、文化交流或国家现代化；
- central object：火箭、工人、工厂、地球、地标、地图或和平符号。

## Calibration notes from the development reference set and first image pass

校准集合中适合作为本技能主参考的是空间科学、建设系统、和平/核风险等分支样例：它们把火箭、轨道、地球、宇航员、红色手势、和平与风险组织成大块关系。旅游样例用于 Intourist 旅游与文化外交；早期工业化或非苏联图形只作为边界参照。这些分支不能在执行时被混用；未获公开许可的历史参考图不随仓库分发。

首轮样张的结论：

- **SPACE-SCIENCE：partially aligned**。红手—火箭—地球—轨道关系已经成立，远读层级也成立；但黄色斜光容易滑向现代科幻海报，火箭和手部的阴影略显立体，轨道线多了一点装饰性。
- **BUILDING-SYSTEM：aligned with structure, not yet fully period-specific**。阶梯模块、工厂、课堂、桥和制图台符合“系统正在工作”，但照片蒙太奇偏多，整体更像当代复古编辑海报，而不是苏联公共宣传的硬切色块。

第二轮的共同修正：

- **先做几何命题，再放物件**：至少 3 个、最多 5 个大模块；每个模块必须改变叙事关系，不能只是装饰卡片。
- **压平现代光效**：火箭、手掌、人物和桥只用平面色块、粗轮廓和有限套色；禁止宽大的体积光束、镜头光晕、金属反射和柔焦。
- **减少摄影感**：BUILDING-SYSTEM 最多保留 1—2 个被压成棕褐色的照片/蒙太奇窗口，其余必须是剪影、线稿或印刷色面。
- **保留公共版式区**：顶部或底部留 15%—25% 干净文字区；所有俄文、中文、英文标题后期排版，模型不生成字。
- **分支自检**：SPACE-SCIENCE 要有科学/劳动/地球的关系；BUILDING-SYSTEM 要有生产/教育/基础设施的关系；若只剩“酷火箭”或“怀旧拼贴”，判定不通过。

### 2. Write one visual thesis

使用：

> 这张海报把“<社会承诺>”变成“<一个可见系统>”，让观众沿着“<方向线>”看到从现实到未来的路径。

例：

> 这张海报把“劳动创造未来”变成工人、工厂和火箭共享的一条上升结构，让观众看到火箭并不是凭空起飞。

### 3. Build the layout contract

#### SPACE-SCIENCE

- 画布：3:4 竖幅或 2:3 竖幅；
- 上部 50%—70%：深蓝/黑色宇宙空间或留白；
- 主体：一个火箭、卫星、宇航员或向上的手/人物；
- 辅助结构：2—4 条轨道线、地球弧线或射线；
- 文字区：顶部或底部 15%—25%，粗重窄体；
- 颜色：深蓝、亮红、米白、金黄；高饱和但不霓虹。

#### BUILDING-SYSTEM

- 画布：3:4 或 4:5；
- 默认使用 `STRUCTURED-SYSTEM`，但必须先选择版式：封面/产品/单一钩子用 `FOCUS-SYSTEM`；经典引文/长标题用 `QUOTE-SYSTEM`；明确复刻黄金参考图用 `GOLDEN-SYSTEM`。只有最后一种模式固定使用左侧 35%—50% 文字区、右侧 45%—55% 平台系统和下方 20%—35% 环境基座；
- 主结构由 4—6 条水平平台、1—3 根赭黄/橙黄竖向支撑和 0—1 条连接线组成；平台从右侧切出画面，形成向上延伸的整体轮廓；
- 平台上只放极小人物、工具、课堂、车间或档案符号，每层 2—4 个；人物证明系统被使用，不承担英雄叙事；
- 工厂、地铁、学校、钢架、齿轮、地图、档案可作为平台或环境关系，但不要把每个对象做成独立卡片；
- 红色是行动和组织，米色是纸和历史，蓝色是科学/制度冷面；黄金参考优先使用蓝灰、橄榄、赭黄，红色只作小面积强调；
- 用横向平台、垂直支撑、错位切边、微型劳动关系和下方山水/道路/桥表现“系统正在工作”。

#### PEACE-NUCLEAR

- 大面积黑/深蓝空间；
- 一个极简单一符号：白色轨迹、心电线、和平鸽、地球或细长火箭；
- 少量红/黄警示块；
- 标题短而硬，留白和沉默必须保留；
- 不做爆炸大片，重点是“理性面对巨大风险”。

#### TOURISM-Intourist

- 地标/景观占 45%—65%，地图、交通或水面提供底层结构；
- 颜色可以更明亮、更商业化，但保留平面插画和印刷层次；
- 放置目的地、路线、机构标识时要后期排版；
- 不把游客、风景和火箭全部挤成意识形态拼贴。

### 4. Apply the visual system

- 共同颜色：印刷黑 #11151C、旧纸 #E7D3A9、宣传红 #D9342B、米白 #F3EBDD；
- 科学蓝 #163B72、冷蓝 #2E6C9E；
- 未来黄 #E9B83F、橙红 #E25C2C；
- 建设棕/砖红 #7C3028；
- 单张主色 4—6 种；校准样例中较鲜明的蓝红黄可以保留，但禁止发光渐变；
- 用硬边平色、块面重叠、照片蒙太奇或丝网/平版印刷纹理；
- 文字使用窄体无衬线或几何大写，英文和俄文可作为历史视觉参考，中文后期采用粗重无衬线；
- 背景要有纸、墙、印刷或公共展示的物理感，不能像 3D 游戏菜单。

### 5. Define motion and sound

默认动效：

- SPACE-SCIENCE：轨道线先绘制，主体沿对角线上升，文字块锁定；
- BUILDING-SYSTEM：模块从不同方向卡入，工人/工厂/数字关系逐层连接；
- PEACE-NUCLEAR：黑场、细线、一次脉冲或白色轨迹，最后出现标题；
- TOURISM-Intourist：地图展开、路线划过、景观块翻入，避免军事雷达感。

声音：

- 科学：低噪电子脉冲、机械继电器、广播室空气；
- 建设：金属、车间、铅笔、纸张、脚步与低速合成器；
- 和平/核威胁：低频脉冲、稀疏心电/电报码、留白；
- 旅游：列车、海浪、城市环境与轻微公共广播。

不要默认使用史诗铜管、现代科幻音效包或商业广告的上升音效。

### 6. Run the quality gate

生成后检查：

- 是否先看到结构和方向，再看到装饰；
- 是否明确属于四个分支之一；
- 是否有生产/科学/制度/地理关系，而不是孤立火箭；
- 模块是否为大版块而非 UI 卡片；
- 蓝色是否是冷战科学/公共系统的色彩，不是赛博霓虹；
- 文字是否远读、少而有层级；
- 是否误用了 1941—45 的战时警报、牺牲和敌人压迫构图；
- 是否误用了 1920 年代的纯几何先锋构成；
- 去掉文字后，观众是否仍然能读出“这个社会正在建设、探索、警告或交流什么”。
- 若为 `STRUCTURED-SYSTEM`：去掉文字后是否仍然能读出当前模式的主系统与下方环境基座；若只剩普通办公楼、装饰性建筑或大块无功能空白，判定不通过。

## Output contracts

### Image / poster

输出：

1. branch and period；
2. social promise；
3. visual thesis；
4. layout contract；
5. subject/system relationships；
6. palette and print treatment；
7. GPT Image prompt；
8. negative constraints；
9. post-production text plan；
10. quality gate verdict。

### Video frame

输出：

1. branch；
2. duration and aspect ratio；
3. module entry order；
4. one directional motion；
5. caption timing；
6. sound carry；
7. final locked-poster frame。

### Critique

输出 verdict：aligned / partially aligned / not aligned；然后指出：

- 更接近哪一个冷战分支；
- 哪个视觉元素串入了战争、早期构成主义或现代商业科幻；
- 三个只改一个变量的修订建议；
- 一条修订后的提示词。

## Prompt template

Use this order:

Use case: stylized-concept or historical-scene.
Asset type: original Soviet Cold War poster, not a replica.
Period: <1957–1965 space-age / 1965–1982 building-system / late-Cold-War peace-warning / Intourist tourism>.
Branch: <SPACE-SCIENCE / BUILDING-SYSTEM / PEACE-NUCLEAR / TOURISM-Intourist>.
Social promise: <science, collective construction, peace, international exchange>.
Primary request: <one system and one directional relationship>.
Composition: 3:4 vertical poster unless another ratio is requested, 3–5 large hard-edged modules, strong asymmetry, one dominant diagonal or vertical direction, content-weighted layout with a functional text field sized to the actual copy, crisp far-distance hierarchy; do not reserve a large empty field without a content reason.
Style/medium: historically grounded Soviet offset/lithographic poster, original artwork, simplified figures, hard flat colors, selective photo montage or silkscreen texture, no exact reproduction.
Palette: print black #11151C, propaganda red #D9342B, aged paper #E7D3A9, science blue #163B72, future yellow #E9B83F, optional orange #E25C2C.
Materials: offset print, paper fiber, halftone, limited registration shift, clean hard shapes, restrained wear.
Text: if required, include only the exact short text "<text>"; otherwise leave clean reserved text blocks for post.
Avoid: 1941–1945 wartime mobilization, battlefield imagery, motherland recruitment, exact famous poster reproduction, 1920s constructivist abstraction, cyberpunk neon, glossy CGI, generic NASA aesthetic, corporate infographic cards, dense fake microtext, watermark.

### STRUCTURED-SYSTEM prompt addendum

当 branch 为 `BUILDING-SYSTEM / STRUCTURED-SYSTEM` 时，先在 prompt 中写明一个版式模式，再追加对应约束；不要只写“模块化”或“苏联风”：

```text
Layout mode: choose exactly one — GOLDEN-SYSTEM (reference-match: functional cream title field on the left 35–50%, right-entering system 45–55%), FOCUS-SYSTEM (subject/system 55–70%, text field 15–30%, subject may be central or off-center), or QUOTE-SYSTEM (accurate post-typed quote block 35–55%, subject/system 30–50%). Never reserve a large empty field unless it will carry real copy.
Structure: build one asymmetrical public-system section from 4–6 stacked horizontal platforms with 1–3 ochre vertical support bars, slight offsets, hard cropped edges, and one restrained connection line. In GOLDEN-SYSTEM it enters from the right edge; in FOCUS-SYSTEM it may enter from the right but can expand toward center; in QUOTE-SYSTEM keep the system subordinate to the quote while preserving a strong silhouette. Place 2–4 tiny workers, tools, study or production marks on each platform only for scale and labor relationships.
Visual hierarchy: first the selected primary subject or title, second the platform/system and miniature people/tool relationships, third the landscape and offset-print texture. In GOLDEN-SYSTEM, the left title field and right system are read together.
Foundation: use a compressed blue-grey landscape, water, road, bridge, trees, or terraces across the lower 20–35% when the brief needs a social and geographic foundation; reduce it when it competes with the primary subject.
Medium: flat offset/lithographic poster, cream stock, navy and blue-grey structure, olive terrain, ochre support bars, limited registration shift, fine paper grain, no gradients or glossy light.
Post typography: leave all accurate Chinese, Russian, English, logos, dates, QR codes, and quotations for later typesetting in the selected functional text field, not automatically in the left blank field.
Avoid: glass office tower, architectural visualization, SaaS dashboard, card grid, UI screenshot, large portraits, heroic pose, photorealistic room scenes, neon, 3D lighting, random hammer-and-sickle symbols, fake microtext.
```

## Hard prohibitions

- Do not make every Cold War image a rocket in a star field.
- Do not use random hammer-and-sickle stickers, red stars or Lenin portraits without a social relationship.
- Do not turn optimism into plastic 3D futurism or glowing sci-fi.
- Do not use the war-mode palette and close-up threat grammar for a peaceful science/education poster.
- Do not use 1930s workers, formulas, slogans or typography as evidence for a 1960s/70s image without labeling the historical shift.
- Do not use tourist landscape posters as the main template for Marxist theory content.
- Do not render large Chinese or Russian copy if it must be accurate; compose text in post.
- Do not copy the exact composition, face, emblem arrangement or wording of a historical reference.

## Reference navigation

Read examples/reference-study.md before making a historical claim. If a reference set is supplied, classify the supplied files directly and do not assume that local reference files are bundled with this skill. For final image generation or editing, hand the visual contract to the separately installed image-generation skill and follow that skill's prompt-craft guidance.

## Final check

The work passes only if the viewer can answer:

1. Which Cold War promise or fear is this image organizing?
2. What objects, people or infrastructure make that promise visible?
3. Which branch and approximate period does the color/typography/layout imply?

If the answer is only “blue space poster” or “red Soviet poster,” revise.
