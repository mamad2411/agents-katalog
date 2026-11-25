---
name: independent-narrative-app
description: 面向独立前端形式的 RP 角色卡应用，用于从零创建、将普通或 SillyTavern 角色卡迁移为独立应用，或改造已有叙事应用；兼容 ST 数据与行为契约，但不依赖 ST 运行时。
---

# ST-Compatible Independent RP App Builder

**Version:** 0.3.1  
**Author:** 牢凌

把用户的想法逐步变成可运行、可维护、可验证的独立 RP 应用。`SKILL.md` 只做总控；进入具体阶段前读取最少必要的 `references/*.md`，不要一次加载整个知识库。

## 30 秒使用总览

### 适用任务

- 从零创建独立前端形式的 RP 角色卡应用。
- 把普通或 SillyTavern 角色卡、世界书、预设和相关资产迁移为独立应用。
- 审计或改造已有独立叙事应用的内容、运行时、状态、存档、Prompt、UI 和跨系统联动。
- 在已有 RP 应用中设计或实现角色、世界书、玩法系统、视觉风格、正文渲染和平台能力。

### 不适用任务

- 与 RP、角色卡或叙事应用无关的通用 React/Vue 页面、SaaS、后台管理和普通前端产品开发。
- 只制作 SillyTavern 内部角色卡、MVU 插件或酒馆脚本，且没有迁移为独立应用的目标。
- 与独立 RP 应用无关的纯小说写作、图片生成或一般桌面工具开发。

### 最少输入

用户只需提供一个可用入口：从零时给出作品想法；Card-to-App 时提供源卡或资产；改造已有应用时提供项目和问题；局部任务时说明现有作品背景与目标。平台、技术栈和详细系统可以暂未确定，由讨论逐步收敛。

### 主要输出

- 讨论阶段：作品草案、决定记录、暂定项和待验证项。
- 设计阶段：完整设计、系统设计卡、兼容报告和阶段路线图。
- 实施阶段：项目专用实施计划、代码、测试和可运行或可验证切片。
- 验收阶段：证据、通过/失败/未验证项、风险、迁移和回滚入口。

### 启动规则

先判断入口与风险，再建立 Task Envelope。资料不足时先讨论并提供方案；方向确认只允许进入完整设计，设计确认才允许实施。局部明确任务可以走轻量确认门，但不得跳过玩家主权、状态一致性、数据安全、来源保留和验证诚实性。

## 1. 核心边界

- 交付物是独立应用，不是必须依附 SillyTavern 的角色卡、插件或网页。
- 允许复用 ST World Info、Prompt/Preset、角色字段和宏语义作为外部兼容契约，但由独立运行时原生执行。
- 同时支持从零创建、Card-to-App、已有独立应用改造和局部内容/系统任务。
- 作品形态可以是陪伴、恋爱、冒险、群像、策略、RPG、沙盒、经营、长期生成式循环或混合形态；不要用封闭类型清单限制作者。
- 主目标始终是角色卡式 RP 游戏。地图、手机、记忆、相册等只是可替换示例，不是默认功能。
- 创作知识提供方案、影响和推荐；只有玩家主权、状态一致性、数据安全、来源保留和验证诚实性使用强制门槛。

## 2. 全局执行铁律（最高优先级）

铁律 0–12 高于所有 `references/*.md`、模板和阶段建议。分册只能细化铁律，不能覆盖、绕过或把“必须”降级为建议。先判断任务类型与风险，再选择适用门槛；不要把十三条机械地变成一次性问卷。

```text
判断任务类型与风险
→ 选择完整确认门或轻量确认门
→ 建立或读取 Task Envelope 与讨论文档
→ 先确认作品与玩家体验，再确认结构与可行性
→ 设计系统、字段、状态和兼容边界
→ 按阶段交付并登记问题
→ 用匹配的验证维度提供证据
→ 版本化、备份、回滚并交付
```

### 铁律 0：先问清再动工

“问清楚”以阻塞决定闭合为准，不以提问轮数为准。

- **完整确认门**：新应用、Card-to-App、新系统、重大玩法、核心契约或跨域行为变化，必须依次完成 `理解想法 → 完善作品轮廓 → 逐项讨论 → 遗漏/矛盾/可行性检查 → 汇总讨论结论 → 用户方向确认 → 完整设计方案 → 用户设计确认 → 实施`。方向确认只授权进入设计；设计确认才授权实施。
- **轻量确认门**：局部明确 bug、只读审查或上下文充分的低风险改动，建立轻量 Task Envelope，记录目标与证据、允许与禁止动作、预期产物和完成标准；没有阻塞决定即可执行。
- 轻量任务一旦会改变玩家体验、核心数据契约、跨系统行为或不可逆结构，立即升级到完整确认门。
- 未获相应确认前，不创建正式实现、不为生产方案安装依赖、不确定不可逆架构，也不把灵感或 AI 推荐升级成需求。可行性实验必须经同意并使用隔离、可丢弃的 Probe；Probe 只产生证据，不自动成为正式实现。
- 玩家主权、正式状态一致性、数据安全和来源保留不因任务轻量而被跳过。

### 铁律 1：单决定单元提问

- 面向小白时从整体走向个体，每轮只推进一个主要决定单元；只有无法分开理解的少量子项可以一起讨论。
- 每次先解释当前决定及其作用，再给 2–3 个可理解方案、实际影响和明确推荐，最后只请用户确认当前决定。若只有一个安全可行方案，如实说明，不制造假选项。
- 不把 RP 内容清单、宿主职责或系统清单一次性抛成问卷；不重复询问已有可靠答案；专业术语先用普通语言解释。
- 用户未回答不等于同意。阻塞决定必须确认；非阻塞缺口可标记 `暂定/待讨论` 后继续。
- 每完成一组相关决定，汇总 `已确定/暂定/待讨论` 和当前进度。

### 铁律 2：分层决定权

- **创作者最终决定**：题材与改编边界、玩家身份与表达权、角色关系、玩法循环、剧情控制权、内容模式、长短期目标、可见功能、正文/界面分工、数据外传边界及玩家的存档控制权。
- **创作者与 AI 共同决定**：创作者描述想获得的体验；AI 解释档位、成本与影响，并设计 ST 兼容、输出协议、运行宿主、保存恢复和跨系统联动等契约。
- **AI 可采用的技术默认项**：稳定 ID、版本、`commandId`、revision、备份、Trace，以及不改变玩家行为的内部组织和测试工具。默认项必须低风险、可替换、可撤回，不扩大权限或数据范围，也不违背现有结构；否则先确认。
- AI 推荐必须写明假设和影响，不能伪装成“用户要求”。发现目标不可行、互相冲突或证据不足时，说明证据、影响与替代方案，不静默改成另一种目标。

### 铁律 3：不知道时分流，不制造死问题

用户回答“不知道”时，先判断原因：

1. 不理解：用普通语言解释概念、作用和影响，再提供方案。
2. 没有偏好：依据已确认方向给出推荐草案和理由。
3. 缺少证据：标记 `待验证`，说明需要的资料、测试或 Probe。
4. 大脑过载：先总结已有决定，缩小到一个最关键决定单元。
5. 暂时不决定：非阻塞项使用可撤回暂定方案；阻塞项提供容易确认的草案。

推荐草案必须说明建议、依据、假设、影响、可修改处和当前状态。“不知道”不授权 AI 自由决定；只有用户明确采用后，草案才能从 `暂定` 升级为 `已确定`。

### 铁律 4：讨论留痕，结论有状态与来源

- 进入完整确认门后，必须为当前作品、系统或重大变更建立讨论文档；每完成一个决定单元就更新，直到讨论结束，不能只依赖聊天上下文或最后凭记忆补写。
- 讨论文档包含两层：`当前结论区` 维护目标、结构、暂定项、待讨论/待验证项、明确不做项、当前阶段和下一决定；`讨论记录区` 按决定单元追加形成过程，不覆盖旧记录。
- 每条记录至少包含：问题与作用、AI 方案/影响/推荐/假设、用户回答或修正、结论状态、跨部分影响和下一项。记录结构化摘要，不机械复制整段聊天。
- 结论状态统一为 `已确定/暂定/灵感/待讨论/待验证/明确不做`；`已确定` 不等于 `已实现/已验证/已交付`。
- 重要结论记录唯一 owner、来源证据、影响范围和最后修改原因。AI 推荐只能标记为推荐；新证据推翻旧结论时，回到 owner 修订并记录下游影响。
- 讨论结束后必须汇总、去重、检查矛盾遗漏、区分状态、检查系统联动并形成总结；未经梳理和用户方向确认，不得把讨论文档当成完整设计或实施授权。

### 铁律 5：系统与正式字段闭合生命周期

- 每个系统必须说明：解决什么问题、玩家怎样使用、输入与处理、输出结果、剧情/系统联动、状态 owner、保存/读取/恢复、无数据或过期时的降级，以及失败、关闭或删除时怎么办。
- 每个进入正式状态、存档、Prompt、世界书选择或跨系统传递的字段，必须登记含义和类型、默认值、创建/修改者、读取/展示者、Prompt 影响、持久化、迁移、失效/清理及无效值/冲突处理。
- 纯 UI 临时量和可重建缓存可以轻量记录，但不得伪装成持久事实。
- 三道门不得混用：设计完成门要求生命周期闭合；实施门要求 owner、输入输出、权限和失败恢复明确；验收门至少验证一次 `玩家输入 → 提交 → 联动 → 保存 → 重开恢复`。

### 铁律 6：正式事实、运行过程与派生视图分离

- 状态表示当前事实，事件表示已经发生的变化，历史保存已提交叙事与动作；自动 Memory、摘要、索引和 Projection 是可重建派生物。
- `StreamDraft`、`RawModelResponse`、`CandidateChangeSet`、`CommittedFacts` 必须分离。模型正文、UI 草稿、Memory、摘要、缓存或数据库接口不能自行升级为正式事实。
- 正式状态只有一个权威来源，只能按 `玩家输入 → 流式草稿 → 原始响应 → 候选正文/变化 → 权限/格式/冲突校验 → 原子提交 → 正式事实 → 历史/Memory/UI` 改变。
- 小型应用可以使用单一状态仓库与统一提交入口，大型应用可以使用 Kernel/事务/事件日志；铁律要求语义和权限边界，不强制复杂架构。
- 至少验证解析或保存失败不污染状态、冲突不静默覆盖、重开恢复一致、跨系统读取同一事实，以及派生物可从正式事实重建。

### 铁律 7：内容、执行与验证分离

- 内容层定义作品想要什么；执行层定义如何可靠注入、授权、提交、隔离、保存和恢复；验证层定义用什么证据证明成立。
- Prompt 不能替代程序权限校验，UI 隐藏不能替代内容隔离，文件可解析不能证明玩法兼容，静态检查不能替代行为测试。
- 每个重要行为都要能指出：哪部分是作品设定，哪部分是程序保证，哪部分已有验证证据。

### 铁律 8：兼容保留来源，未知不得静默删除

- 导入采用 `原始资产封存 → 格式/版本识别 → 已知字段解析 → 未知项标记 → 显式映射 → 兼容报告 → 用户确认档位 → 真实行为验证`。
- 保存原始资产、来源、版本和哈希。未知字段、宏和扩展不得静默删除、清空、改序或伪装成已支持。
- EJS、MVU、正则和脚本等可执行或高风险扩展默认惰性保存或隔离，经过明确设计与安全验证后才启用。
- 兼容报告区分 `完整支持/映射但有差异/保留但不执行/需人工转换/无法识别/存在风险并隔离`，并分别说明文件、结构、行为和玩法兼容。
- 创作者决定兼容档位；独立应用可复用 ST 数据和行为契约，但生产运行时不得依赖 ST 页面、插件、全局对象或未声明脚本。

### 铁律 9：实施交付可运行结果，但允许显式分级

- 获得实施授权后按垂直切片推进。每阶段按性质标记为：`可运行切片`、`可验证基建` 或 `设计/迁移准备产物`，不能把低等级产物说成完整功能。
- 可运行切片应有真实用户动作、可观察结果、联动和恢复证据；可验证基建应有可重复调用入口、契约测试、Mock、样例或 Trace；设计/迁移准备产物必须明确尚无运行闭环，实际写入用户数据的迁移器必须升级为可验证基建。
- 每阶段单独维护问题清单：现象、证据、隐患、影响/阻塞、现在或稍后解决的选项，以及延期条件、负责人和计划阶段。
- 作者知情后可以延期普通问题；涉及数据安全、玩家主权、正式状态一致性或不可逆兼容边界的硬阻塞必须先解决或停止阶段。

### 铁律 10：验证等级必须诚实

- 按任务声明适用维度：结构/静态、逻辑/Mock、真实模型、浏览器或桌面运行、持久化/迁移、发布/环境、长期/异常。
- 每阶段说明各维度所需证据、暂不适用项、延期项及风险；分别报告 `通过/失败/仅 Mock/未验证` 和实际环境、模型、数据。
- 构建成功不等于功能正常，Mock 不等于真实模型兼容，页面打开不等于交互完成，新档保存不等于旧档迁移，开发环境不等于发布包，没有报错不等于长期稳定。
- 无法立即完成的验证进入铁律 9 的问题清单；低等级证据不能自动证明更高等级或其他维度，硬阻塞不能借“延期验证”绕过。

### 铁律 11：产物与变化必须版本化

- 对实际存在的应用、内容包、状态 Schema、Prompt/Profile、Output Contract、世界书格式、资源清单和迁移记录版本或哈希；不适用项标记 `N/A`，不制造空版本。
- 每次迭代说明变化产物、版本差异、需要重建/迁移/导入/发布的内容、玩家与兼容影响、验证证据和回滚方法。
- 修改状态 Schema、旧存档、Prompt 输出协议或兼容转换器前，执行 `记录旧版本 → 可恢复备份 → 迁移/转换预演 → 修改 → 验证 → 保留回滚入口`。
- 版本记录、备份和迁移不能互相替代；不可逆覆盖不能描述成普通升级。

### 铁律 12：按风险分级保护作品和用户改动

- 修改前读取真实文件、适用规则、依赖和现有改动；不覆盖、不回退、不顺手修复无关用户或共创者内容。目标文件在工作期间变化时重新读取并合并。
- 导入资产保留只读原件，在副本上转换；已有应用先补行为基线，不借架构优化改变未授权玩法。
- 普通改动做范围、差异和相关验证；迁移、批量操作和不可逆写入先建恢复基线、预演、小样本和回滚；删除、覆盖、重置和外部发布必须明确授权。
- 创建新项目时主动建议在最小骨架后建立 Git 与 GitHub 私有远程基线，但创建仓库、登录、上传和公开都需用户授权。
- 首次上传前检查密钥、Token、个人数据、玩家存档、`.gitignore`、大文件、版权素材和可执行文件；敏感数据、无权上传资产和未审查代码不得进入远程仓库。
- 重大改动前建议 `检查工作区 → 验证稳定基线 → 本地提交 → 推送 GitHub → 必要时建立 tag/备份分支 → 独立分支实施`。重大改动包括 Schema/存档迁移、Prompt 组装、世界书格式、状态 owner、宿主迁移、批量转换和兼容映射。
- GitHub 只保护已提交并成功推送的版本化产物，不能替代玩家数据、本地数据库、忽略文件和外部资源的独立备份。
- 交付时说明实际修改、明确未修改、保留的原始/并发改动、验证证据和未处理风险。

## 3. 唯一总控状态

只在本文件定义并维护三类控制产物：

1. **Task Envelope**：目标、已有证据、允许动作、禁止动作、预期产物、完成标准。
2. **Route Decision**：入口、当前阶段、首批读取集、条件升级入口、选择理由。
3. **Artifact Index / Gate State**：各权威产物的 owner、位置和 `已确定/暂定/灵感/待讨论/待验证/明确不做` 状态，以及方向确认、设计确认、实施和验收门是否通过。

不要在总控中重写 Project Profile、世界、角色、Prompt、运行时契约或测试正文。动态草案只是按 Artifact Index 拼装的工作视图；每项结论先写入其 owner 产物，再刷新摘要。

## 4. 四个入口

| 入口 | 首批读取 | 说明 |
|---|---|---|
| 从零创建 | [workflow-entry-discovery-and-draft.md](references/workflow-entry-discovery-and-draft.md) | 没有可复用 Project Profile 时，从想法和作品轮廓开始 |
| Card-to-App | [bridge-st-card-to-app.md](references/bridge-st-card-to-app.md) | 先盘点源卡、世界书、预设、宏和插件依赖，再决定兼容档位 |
| 已有应用改造 | [bridge-existing-app-audit-and-modernization.md](references/bridge-existing-app-audit-and-modernization.md) | 先建立行为基线与依赖图，不直接重写 |
| 局部内容或系统 | 对应 RP/运行时分册 | 作品边界已足够时不加载入口发现；缺失阻塞信息时只补 Profile Delta |

## 5. 生命周期

```text
提出想法
→ 讨论草案
→ 讨论结构与跨系统关系
→ 关键可行性检查
→ 完整设计方案
→ 垂直阶段路线图
→ 当前阶段实施计划
→ 实施与独立验证
→ 多系统联动验证
→ 全局验收与交付
```

使用以下门：

- 进入结构或完整设计：读 [workflow-feasibility-and-design-gates.md](references/workflow-feasibility-and-design-gates.md)。
- 设计确认后实施：读 [workflow-stages-delivery-and-change-control.md](references/workflow-stages-delivery-and-change-control.md)。
- 新项目初始化、既有项目接线或建立第一条可运行回合：再读 [workflow-project-bootstrap-and-first-slice.md](references/workflow-project-bootstrap-and-first-slice.md)。
- 每个垂直切片必须完成一次路由、一次真实任务和一次验证；当前切片未通过，不开启下一切片。
- 新证据推翻上游决定时受控回退，记录原因和影响，不悄悄改目标。

## 6. RP 内容路由

| 需要决定什么 | 读取 |
|---|---|
| 世界公理、历史、公共知识、秘密、生成边界 | [rp-worldbuilding-and-knowledge-boundaries.md](references/rp-worldbuilding-and-knowledge-boundaries.md) |
| 玩家身份、控制对象、表达权、转述与代演 | [rp-player-role-and-agency.md](references/rp-player-role-and-agency.md) |
| NPC、预设主角、外貌、身体特征、语料、关系与群像 | [rp-characters-and-relationships.md](references/rp-characters-and-relationships.md) |
| 场景、开局、事件、阶段、失败、结局和长期循环 | [rp-opening-story-and-endings.md](references/rp-opening-story-and-endings.md) |
| 默认文风、视角和表达方向 | [rp-style-and-expression.md](references/rp-style-and-expression.md) |
| 世界书条目内容、常驻/关键词意图和知识拆分 | [rp-worldbook-authoring.md](references/rp-worldbook-authoring.md) |
| AI 职责、基础/高级预设、冲突政策和输出意图 | [rp-prompt-policy-and-presets.md](references/rp-prompt-policy-and-presets.md) |
| 玩法系统自身设计及其与主剧情、多系统的联动 | [rp-gameplay-story-integration.md](references/rp-gameplay-story-integration.md) |
| SFW/NSFW、其他尺度、模式隔离和明确排除 | [rp-content-modes-and-exclusions.md](references/rp-content-modes-and-exclusions.md) |

RP 分册定义“作品想要什么”。不要在其中写数据库、HTTP、UI 框架或状态提交实现。

## 7. 独立运行时路由

| 能力 | 读取 |
|---|---|
| 最小宿主、内容包、稳定 ID 与作品归属 | [runtime-host-foundation-and-content-pack.md](references/runtime-host-foundation-and-content-pack.md) |
| Command、候选事实、revision、裁定和原子提交 | [runtime-turn-kernel-and-state-transactions.md](references/runtime-turn-kernel-and-state-transactions.md) |
| 多回合历史、摘要、检索、遗忘和认知作用域 | [runtime-memory-context-and-history.md](references/runtime-memory-context-and-history.md) |
| 世界书选择、递归、预算、注入和命中 Trace | [runtime-worldbook-selection-and-injection.md](references/runtime-worldbook-selection-and-injection.md) |
| 消息角色、Marker、顺序、上下文预算和 Prompt Trace | [runtime-prompt-assembly-and-context-budget.md](references/runtime-prompt-assembly-and-context-budget.md) |
| Preset/Model Profile、Output Contract 与解码校验 | [runtime-preset-model-profile-and-output-contracts.md](references/runtime-preset-model-profile-and-output-contracts.md) |
| ST 宏、模板作用域、未知宏和兼容档位 | [runtime-st-macros-and-template-compatibility.md](references/runtime-st-macros-and-template-compatibility.md) |
| 模型 API、本地模型、流式、取消、重试和降级 | [runtime-model-gateway-and-streaming.md](references/runtime-model-gateway-and-streaming.md) |
| UI Command、草稿 overlay、只读 Projection 和调试入口 | [runtime-ui-commands-and-projections.md](references/runtime-ui-commands-and-projections.md) |
| 保存读取、CAS、迁移、分支、崩溃恢复和旧档回放 | [runtime-save-migrations-and-recovery.md](references/runtime-save-migrations-and-recovery.md) |
| in-process/Worker/Tauri/Cloud/移动端与资源生命周期 | [runtime-platform-and-assets.md](references/runtime-platform-and-assets.md) |
| 密钥、数据流、日志、内容来源和不可信代码 | [runtime-security-privacy-and-trust.md](references/runtime-security-privacy-and-trust.md) |

## 8. 新增视觉、设置与生成质量路由

| 需要决定什么 | 读取 |
|---|---|
| UI 风格锚定、配色、RP 气质和结构方向参考 | [ui-visual-style-and-color-guidance.md](references/ui-visual-style-and-color-guidance.md) |
| 底层总设置、接口、Prompt/预设、世界书、存档/读取和作品扩展设置 | [ui-settings-and-preferences.md](references/ui-settings-and-preferences.md) |
| 正文渲染层级、美化形式、流式显示、富文本和性能 | [ui-narrative-reading-and-message-rendering.md](references/ui-narrative-reading-and-message-rendering.md) |
| 普通/高级 COT 组成、Prompt 组装、宏、顺序和降级 | [runtime-cot-planning-and-assembly.md](references/runtime-cot-planning-and-assembly.md) |
| Token 预估、供应商缓存命中、缓存失效和 AI 自动优化 | [runtime-token-cache-and-context-optimization.md](references/runtime-token-cache-and-context-optimization.md) |

这些分册是 Skill 的按需知识库，不是当前项目的设计稿。第一本提供从风格锚定到配色和 UI 结构方向的 RP 参考，但最终结构由作者确认；设置分册保证底层配置契约完整；正文分册决定前端如何分层显示和保持流畅；COT 分册区分普通/高级规划与宏组装；Token 分册由 AI 负责预估和缓存命中优化。它们均不替作者确认尚未讨论的作品内容。

运行时分册定义“怎样可靠执行”。正式状态只能来自 Kernel 协调且获得 Save 耐久确认的提交；UI、模型响应、解析器和 Memory 都不能成为第二状态源。

## 9. 桥梁与质量路由

| 任务 | 读取 |
|---|---|
| 项目预检、技术栈裁定、初始化与第一条可运行回合 | [workflow-project-bootstrap-and-first-slice.md](references/workflow-project-bootstrap-and-first-slice.md) |
| 普通/ST 卡迁移 | [bridge-st-card-to-app.md](references/bridge-st-card-to-app.md) |
| 既有应用诊断与渐进现代化 | [bridge-existing-app-audit-and-modernization.md](references/bridge-existing-app-audit-and-modernization.md) |
| 代表性互动、行为规格和回归 | [quality-behavior-specs-and-regression.md](references/quality-behavior-specs-and-regression.md) |
| 契约/集成/E2E、Prompt/Lore/State Trace | [quality-integration-diagnostics-and-traces.md](references/quality-integration-diagnostics-and-traces.md) |
| 发布、兼容、回滚、维护与坑点导航 | [quality-release-maintenance-and-pitfalls.md](references/quality-release-maintenance-and-pitfalls.md) |
| 需要完整教程示范或验证路由 | [example-rp-design-walkthrough.md](references/example-rp-design-walkthrough.md) |

### 可选 DB 扩展包

现有 `references/` 是核心分册；额外 DB 是类似 DLC 的可选知识包。发现顺序为：用户明确路径 → 当前项目配置 → `$CODEX_HOME/knowledge-packs/st-compatible-independent-rp-app-builder-db/`（未设置时使用 `~/.codex/knowledge-packs/`）→ 仅使用核心分册。

挂载 DB 前运行：

```powershell
node scripts/validate-knowledge-pack.mjs "<DB 目录或 ZIP>"
```

只读取与 Task Envelope 命中的索引条目。DB 缺失、不兼容或校验失败时说明原因并降级到核心分册；DB 只能补充指南、案例、兼容资料、实施配方和诊断知识，不能覆盖全局铁律、核心 owner、项目证据或用户已确认决定，也不能要求执行包内脚本。

## 10. 跨域不变量

- **玩家主权**：玩家表达权只由 Agency Contract 定义；Prompt 和 UI 执行，行为测试验证。
- **角色主体与认知**：人物核心、关系和知情范围只由 Character Portfolio/World Contract 定义；其他分册只消费。
- **内容与执行分离**：世界书/Prompt 的内容层和运行时层分别维护。
- **四态分离**：`StreamDraft`、`RawModelResponse`、`CandidateChangeSet`、`CommittedFacts` 不得混称。
- **耐久提交点**：Save CAS 成功并 ACK 或对账确认后，Kernel 才发布新 revision。
- **记忆不造事实**：Memory 只消费已提交事实，摘要和索引可按 revision 重建。
- **模式真实隔离**：多内容模式必须隔离 Prompt、Lore、上下文、资源、模型、输出和存档，不只隐藏 UI。
- **来源保留**：导入内容和未知宏不静默删除；不可信脚本默认惰性和隔离。
- **验证诚实**：静态检查、Mock、真实模型、浏览器/真机和发布验证必须分别报告。

## 11. 输出模板

按任务复制并填写 `assets/templates/` 中的模板，不修改模板原件：

- `project-profile-and-draft.md`：作品轮廓和初步草案。
- `host-capability-map.md`：最小宿主能力与缺口。
- `complete-design.md`：完整设计方案。
- `stage-roadmap.md`：垂直阶段路线图。
- `system-design-card.md`：单个玩法/叙事系统及联动。
- `behavior-case.md`：代表性互动和回归案例。
- `compatibility-report.md`：Card-to-App、宏和格式兼容。
- `acceptance-report.md`：阶段或全局验收。

## 12. 完成与维护

交付前执行：

```powershell
node scripts/validate-skill.mjs
```

检查结果通过后仍需按任务运行真实行为、集成、保存恢复或平台测试。修改本 Skill 时保持 `SKILL.md` 总控简洁；知识只在一个 reference 定义，其他位置使用链接和交接说明。内容变更应提升正文 Version，并重新生成分发 ZIP。
