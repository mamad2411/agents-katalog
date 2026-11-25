---
name: resume-autofill-agent
description: Build a verified candidate profile from resumes and evidence, prepare portfolio attachments, process application queues, fill recruitment or school forms through available browser automation, resolve conflicts, and save reviewed drafts without submitting. Use for resume autofill, online job applications, campus recruitment, internships, graduate applications, PDF/DOCX resumes, certificates, videos, archives, repositories, and browser forms. 从简历和证明材料建立可溯源的求职者资料，准备作品附件，按队列处理网申，通过可用浏览器自动化填写招聘或升学表单，处理信息冲突并保存已核验草稿；适用于简历自动填写、招聘网申、校园招聘、实习、研究生申请、PDF/DOCX、证书、视频、压缩包、代码仓库和浏览器表单。
---

# Resume Autofill Agent / 简历自动填写 Agent

## Core workflow / 核心流程

1. Inspect current attachments, workspace files, and authorized local profiles before asking questions. / 先检查当前附件、工作区文件和获准使用的本地档案，再提问。
2. Start from any usable resume or profile. Ask for a resume only when none exists. / 只要存在可用简历或档案就直接开始；完全没有时才索要简历。
3. Build a source ledger for every material fact. / 为每个重要事实记录来源。
4. Ask only about missing, conflicting, sensitive, or blocking fields, with at most three short questions at once. / 只询问缺失、冲突、敏感或阻塞字段，每次最多三个简短问题。
5. Improve wording only from verified evidence and target-role relevance. / 只依据已核验材料和岗位相关性优化表达。
6. Select and prepare the smallest relevant portfolio set. / 选择并准备最精简、最相关的作品附件。
7. Normalize repeated education, work, internship, project, award, and publication sections to reverse chronological order (latest end date first) unless the form explicitly requires another order. Do not trust parser order. / 除非表单明确要求其他顺序，否则教育、工作、实习、项目、奖项和论文等重复模块统一按结束日期从近到远倒序排列；不得直接信任简历解析顺序。
8. For multiple application URLs, initialize an application queue and process one company-role pair at a time. / 多个申请链接时，初始化投递队列，按“公司—岗位”逐个处理。
9. Select a browser-control route, then upload the resume before manual filling when parsing may overwrite fields. / 选择浏览器控制方案；若网站会解析并覆盖字段，先上传简历，再手动填写和复核。
10. When an operation fails, inspect the current state, preserve completed work, try bounded safe alternatives, and verify the result. Ask the user only when evidence is still missing, ambiguity affects correctness, or user action is unavoidable. / 操作失败时先检查当前状态并保留已完成内容，再尝试有限次安全替代方案并核验结果；仅在证据仍缺失、歧义影响正确性或必须由用户操作时才询问。
11. Read back critical fields and save a verified draft. Never submit, sign, consent, or make an irreversible declaration without explicit confirmation immediately before the action. / 回读关键字段并保存已核验草稿；未经操作前的明确确认，不得提交、签署、同意或作出不可逆声明。

## First use and learning / 首次使用与学习

On first activation, give a compact usage tip in the user's language before starting: the agent will first connect to or open a controllable browser and inspect existing tabs, so an application URL is optional; provide the latest resume and evidence; keep the first one to five applications in this task for calibration; review each completed draft; explicitly name any field the agent should learn; say “calibration complete” when the behavior is satisfactory; final submission always requires confirmation. Keep this notice brief and show it only once per calibration task. / 首次启用时，先用用户的语言简短提示：Agent 会先连接或打开可控浏览器并检查已有标签页，因此网申链接不是必需；提供最新简历与证明；前一至五份网申留在当前任务中校准；每份填完后人工检查；只学习用户明确点名的字段；满意后回复“校准完成”；最终提交始终需要确认。提示保持简短，每个校准任务只展示一次。

During calibration, after each verified draft ask whether the user changed anything and wants the agent to learn specific fields. Learning requires an explicit instruction that identifies the field or content. Never infer preferences from unmentioned edits. Outside calibration, do not ask automatically and do not learn unless the user explicitly requests it. If scope is unclear, keep the rule local to the current site or role rather than global. Store approved facts, preference rules, and their scope outside the Skill directory. / 校准期内，每份草稿核验后询问用户是否修改、是否需要学习某些明确字段。只有用户点名字段或内容时才学习，不得从未提及的改动推断偏好。校准结束后不再主动询问，也不得自动学习；仅在用户明确要求时更新。适用范围不清时，只作为当前网站或岗位的局部规则，不得升级为全局习惯。已授权的事实、偏好规则和适用范围保存在 Skill 目录之外。

After the user says calibration is complete, use a fresh task for each company-role application when practical. Load only the compact verified profile, applicable preference rules, current role, chosen resume, and evidence needed for unresolved fields. Do not replay the calibration conversation, old screenshots, or every source document. / 用户确认“校准完成”后，在条件允许时每个“公司—岗位”使用一个新任务；只加载精简的已核验档案、适用偏好、当前岗位、选定简历及解决缺失字段所需的证据，不重放校准对话、旧截图或全部原始材料。

Read [calibration-and-efficiency.md](references/calibration-and-efficiency.md) for first-use calibration, explicit learning, and low-context production. / 首次校准、显式学习和低上下文生产流程见 [calibration-and-efficiency.md](references/calibration-and-efficiency.md)。

Read the detailed intake guide in the user's preferred language: [English](references/intake-and-profile.md) | [中文](references/intake-and-profile.zh-CN.md).

按用户偏好的语言读取详细采集指南：[English](references/intake-and-profile.md) | [中文](references/intake-and-profile.zh-CN.md)。

## Source priority / 来源优先级

Use this order: / 按以下顺序处理冲突：

1. Current explicit user confirmation / 用户当前明确确认；
2. Current official record or active-form value entered by the user / 当前官方材料或用户在表单中亲自填写的值；
3. Latest verified resume or profile / 最新且已核验的简历或档案；
4. Older resumes, marked low priority / 旧简历，标记为低优先级；
5. Model suggestions, never treated as facts until confirmed / 模型建议，确认前绝不视为事实。

Keep conflicting versions with source, date/version, confidence, and selection reason. / 保留冲突版本，并记录来源、日期或版本、置信度及采用理由。

## Supplement without fabrication / 补充但不编造

Allow evidence-preserving transformations: reorganize verified material, rewrite bullets as action-method-result, derive demonstrated skills, shorten or translate text, and apply a user-authorized form-only placeholder rule. / 可进行不改变事实的加工：重组已核验材料、按行动-方法-结果改写、提取已有证据支持的技能、精简或翻译，以及使用用户授权的表单专用占位规则。

Never invent employers, dates, metrics, awards, authorship, credentials, family details, health or political information, declarations, or project ownership. Never turn an application placeholder into a remembered fact. / 不得编造雇主、日期、指标、奖项、署名、证书、家庭信息、健康或政治信息、声明及项目归属；不得把网申占位值写成长期事实。

## Portfolio and repositories / 作品附件与代码仓库

- Inspect names and archive contents before describing or uploading. / 描述或上传前检查文件名和压缩包内容。
- Maintain project, relevance, format, size, public link, evidence status, and delivery-copy history. / 记录项目、岗位相关性、格式、大小、公开链接、证据状态及投递副本历史。
- Keep originals unchanged; rename, compress, or transcode only delivery copies. / 原件保持不变；仅对投递副本改名、压缩或转码。
- Check file type, size, count, metadata, hidden files, and privacy before upload. / 上传前检查类型、大小、数量、元数据、隐藏文件和隐私。
- Prefer a short representative demo plus a verified repository link when attachments are limited. / 附件受限时，优先短演示视频加已核验仓库链接。
- Treat account ownership, repository evidence, and the candidate's own contribution as separate claims. / 区分账号归属、仓库证据和候选人本人贡献。
- Record connector availability only; never store tokens, cookies, or credentials. / 只记录连接是否可用，绝不保存令牌、Cookie 或凭据。

Read the detailed safety guide in the user's preferred language: [English](references/fill-and-safety.md) | [中文](references/fill-and-safety.zh-CN.md).

按用户偏好的语言读取详细安全指南：[English](references/fill-and-safety.md) | [中文](references/fill-and-safety.zh-CN.md)。

## Browser control / 浏览器控制

Use the host's native browser or computer-use capability first. If it is absent or repeatedly fails to initialize, use the bundled isolated Playwright bridge; do not keep retrying a broken adapter. / 优先使用宿主已有的浏览器或 computer-use 能力。若能力不存在或连续初始化失败，改用内置的隔离 Playwright 桥接器，不要反复重试失效适配器。

When the user asks to autofill an application, initialize browser control before asking for an application URL. First list and inspect existing controlled tabs. If no controllable session exists, run the bridge doctor and open the remembered authenticated browser profile even when no URL was provided, then inspect its tabs. Use an already open recruitment form when present; otherwise ask the user to navigate to the form inside that controlled window, while offering a pasted URL only as an optional shortcut. A repository or Skill URL is not an application URL unless the user explicitly identifies it as one. / 用户要求自动填写网申时，必须先初始化浏览器控制，再考虑索要申请链接。首先列出并检查当前可控标签页；若没有可控会话，即使用户未提供 URL，也要先运行桥接器体检并打开已记忆的登录配置，再检查标签页。发现已打开的招聘表单就直接使用；没有时，让用户在这个可控窗口内打开目标页面，粘贴链接仅作为可选捷径。仓库或 Skill 地址不得当作网申链接，除非用户明确说明。

Before asking the user to log in, run the bridge doctor and inspect `profile`, `profileSource`, and `profileState`. Reuse the remembered profile. If the bridge reports `PROFILE_CONFLICT` or `AMBIGUOUS_LEGACY_PROFILE`, stop and pin the known authenticated profile with `--profile`; never guess or switch to a new empty profile. Treat `canonical-new` as a first-time login. If a remembered profile is genuinely signed out on the target page, keep that profile and ask the user to restore its session instead of changing directories. / 要求用户登录前，先运行桥接器体检并检查 `profile`、`profileSource` 和 `profileState`。必须复用已记忆的配置；若报告 `PROFILE_CONFLICT` 或 `AMBIGUOUS_LEGACY_PROFILE`，立即停止并用 `--profile` 锁定已登录配置，不得猜测或切换到新的空配置。`canonical-new` 才表示首次登录；若目标页证明已记忆配置确实过期退出，仍须保留原路径并请用户恢复会话，不得改用其他目录。

Read the browser guide before operating a live form: [English](references/browser-control.md) | [中文](references/browser-control.zh-CN.md). The bridge supports page inspection, navigation, form filling, dropdowns, keyboard input, uploads, screenshots, and guarded clicks. / 操作真实表单前读取浏览器指南：[English](references/browser-control.md) | [中文](references/browser-control.zh-CN.md)。桥接器支持页面检查、导航、填写、下拉选择、键盘输入、上传、截图及带保护的点击。

For Codex Computer Use, Tencent WorkBuddy, or another host adapter, read [platform-adapters.md](references/platform-adapters.md). For several job URLs, read [batch-application.md](references/batch-application.md) and start from [application-queue-template.json](assets/application-queue-template.json). / 使用 Codex Computer Use、腾讯 WorkBuddy 或其他宿主适配器时，读取 [platform-adapters.md](references/platform-adapters.md)；处理多个岗位链接时，读取 [batch-application.md](references/batch-application.md)，并从 [application-queue-template.json](assets/application-queue-template.json) 开始。

## Privacy and memory / 隐私与记忆

- Never place real private data in this skill, examples, tests, or templates. / 不得把真实隐私数据写入本 Skill、示例、测试或模板。
- Keep raw data only in the active form or an authorized profile outside the skill directory. / 原始数据仅放在当前表单或 Skill 目录外的授权档案中。
- Redact identifiers in screenshots or artifacts intended for sharing. / 对准备分享的截图和文件进行身份信息脱敏。
- Update reusable memory only when authorized, with source and confidence. / 仅在用户授权时更新长期资料，并记录来源和置信度。
- Use [profile_guard.py](scripts/profile_guard.py) to initialize, sanitize, or audit profiles. / 使用 [profile_guard.py](scripts/profile_guard.py) 初始化、脱敏或审计档案。

## Completion report / 完成报告

Report sources used, fields completed, attachment choices, unresolved conflicts, placeholders, draft-save verification, and actions still requiring user confirmation. / 报告所用来源、已填字段、附件选择、未解决冲突、占位值、草稿保存验证，以及仍需用户确认的操作。

## Resources / 资源

- English intake: [intake-and-profile.md](references/intake-and-profile.md)
- 中文采集流程：[intake-and-profile.zh-CN.md](references/intake-and-profile.zh-CN.md)
- English safety guide: [fill-and-safety.md](references/fill-and-safety.md)
- 中文安全指南：[fill-and-safety.zh-CN.md](references/fill-and-safety.zh-CN.md)
- Blank profile / 空白档案：[candidate-profile-template.json](assets/candidate-profile-template.json)
- Privacy guard / 隐私工具：[profile_guard.py](scripts/profile_guard.py)
- English browser guide: [browser-control.md](references/browser-control.md)
- 中文浏览器指南：[browser-control.zh-CN.md](references/browser-control.zh-CN.md)
- Browser bridge / 浏览器桥接器：[browser_bridge.js](scripts/browser-bridge/browser_bridge.js)
- Native CDP launcher / 原生浏览器启动器：[native_cdp_launcher.js](scripts/browser-bridge/native_cdp_launcher.js)
- Platform adapters / 平台适配：[platform-adapters.md](references/platform-adapters.md)
- Batch workflow / 批量流程：[batch-application.md](references/batch-application.md)
- Application queue / 投递队列：[application-queue-template.json](assets/application-queue-template.json)
- Calibration and efficiency / 校准与省 Token：[calibration-and-efficiency.md](references/calibration-and-efficiency.md)
- Skill packager / Skill 打包器：[package_skill.py](scripts/package_skill.py)
