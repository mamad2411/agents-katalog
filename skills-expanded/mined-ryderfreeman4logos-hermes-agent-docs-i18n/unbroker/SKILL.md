---
name: unbroker
description: Autonomously remove your info from data-broker sites.
version: 1.0.0
author: SHL0MS (github.com/SHL0MS)
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  commands: [python]
metadata:
  hermes:
    tags: [privacy, data-broker, opt-out, ccpa, gdpr, security, doxxing]
    category: security
    related_skills: [google-workspace, agentmail, himalaya, scrapling, osint-investigation]
    homepage: https://github.com/NousResearch/hermes-agent
---

# unbroker

该工具可帮您查找个人信息（姓名、地址、电话、邮箱、亲属关系等）在数据经纪商和人物查询网站上的暴露位置，随后将其移除——在可能的情况下会自动处理，仅当某些网站要求输入验证码、政府身份证明、进行电话或传真验证时，才会引导用户手动操作。它能够独立管理多个人的信息。需要注意的是，该工具**无法绕过反爬虫系统**，**不会在未经明确记录的同意情况下对任何人采取行动**，也不会删除公共记录（如选民信息、财产记录、法庭记录）或该人自己管理的账户。

Python命令行界面（`scripts/pdd.py`）负责管理所有核心状态——包括配置设置、个人档案及同意记录、数据经纪商数据库、任务分级规划、账本记录、草稿文件、报告，以及**邮件发送（SMTP）、验证链接获取（IMAP）和自动操作队列（`next`）**。而您（即代理程序）则需使用内置工具来完成扫描和表单填写工作：利用`web_extract`和`browser_navigate`功能进行搜索和网页表单操作，再通过`cronjob`实现定期重新扫描。

## 自动化运行机制

该功能设计为**全自动运行**模式。在收集信息并获得用户明确同意后，实际上仅有两个需要人工干预的环节：（1）初始信息收集时的对话过程，以及（2）任务执行结束后生成的汇总任务清单（` $PDD tasks`）。在这两个环节之间，系统将完全自动运行。

- **切勿要求操作员手动选择配置。** `$PDD setup --auto` 会自动检测系统能力，并自行挑选最合适的自动化配置。  
- 当设置为默认值 `autonomy=full` 时，**在每次单独提交任务前无需暂停**：在初始阶段获得的同意即视为对 T0 至 T2 阶段退出操作的持续授权。（若设置为 `autonomy=assisted`，则需为谨慎的操作员恢复每次提交前的确认流程——请遵循 `next` 输出中的 `confirm_first` 标识。）  
- **切勿因需要人工处理的任务而中断整个流程。** 应将该任务记录下来（使用命令 `record ... human_task_queued --reason "..."`），然后继续执行后续操作；所有相关内容最终都会汇总在总结报告中。  
- **通过循环调用 `$PDD next <subject>` 来驱动整个流程**——该命令会返回当前需执行的精确顺序动作（如扫描、验证检查、重新核查、优先让家长选择退出、重新排队被阻止的任务等），同时还会提供人工处理相关的汇总信息。需依次执行每项动作，记录结果后再次调用 `next`，重复此过程直至出现 `done_for_now` 指示。之后即可呈现汇总报告并安排定时任务。

自主运行模式绝不可逾越的硬性限制包括：未经记录的同意不得采取任何行动，不得泄露超出 `disclosure_fields` 定义的范围的信息，不得绕过验证码或反机器人机制，且只有在完成再次验证扫描后才能标记为 `confirmed_removed`。

## 适用场景

- “将我（或我家成员）的数据从数据经纪商/人物查询网站中删除。”  
- “让我退出相关服务”、“将我从 Spokeo/Whitepages 等平台删除”、“处理个人信息泄露后的清理工作。”  
- “设置定期隐私监控”（用于防止数据经纪商再次发布个人信息）。  
- 查阅哪些数据经纪商仍在公开某人的信息及其原因。

## 先决条件

- `python`（仅限标准库；核心引擎无需额外安装包）。  
- **可选升级项**（即便不启用这些升级，该技能也能零配置运行；执行 `setup --auto` 命令后会自动开启所有检测到的升级项。系统会从shell环境变量以及 `$HERMES_HOME/.env` 文件中读取凭证，从而无需重新导出即可获取Hermes自身工具已加载的密钥——每个升级项都能将某类人工任务转换为智能体可执行的操作）：  
  - **云浏览器（推荐默认选项）：`BROWSERBASE_API_KEY`**。只要该密钥存在，`setup --auto` 便会自动选择它，这也是预期的基础配置：真正的家用IP云浏览器在正常运行时即可**自动破解软性/托管型验证码（如Cloudflare Turnstile、hCaptcha/reCAPTCHA的勾选式验证）**，从而使相关任务保持自动化处理（T1级别），而不会转为人工任务。这并非所谓的“验证码破解”——无需任何破解服务，也不会进行指纹伪装；只有当浏览器确实无法通过交互式/行为型（“硬性”）挑战时，才会回退到人工处理。若没有该密钥，则会使用普通的智能体浏览器，此时软性验证码相关的任务将降级为T2级别（需人工处理）。  
  - 邮件自动化功能，提供两种无需凭证的配置选项：
- **浏览器模式（无需密码）：`setup --email-mode browser`**。该模式下，代理会通过操作员已登录的网页邮件，利用 `browser_*` 工具发送退出选项/CCPA相关邮件并打开验证链接。所有数据均不会被存储。此功能要求将 Hermes 指向操作员自己已登录的浏览器，**而非**云浏览器：无头云浏览器（如 Browserbase）不存在网页邮件会话，且其网页邮件访问及基于会话的代理网关（例如 PeopleConnect 的引导模式）都受到 Cloudflare/DataDome 的限制。应通过 CDP 启动操作员真实的 Chrome 浏览器——执行命令 `chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.hermes/chrome-debug"`（需使用一次即可登录网页邮件的专用调试配置文件，而非默认配置文件），然后将浏览器工具连接到 `127.0.0.1:9222`。命令 **` $PDD cdp` 可自动完成此操作**（它会自动查找 Chrome/Chromium/Brave/Edge 浏览器，使用专用配置文件以分离模式启动浏览器，并输出 CDP 端点地址；可使用 `--check` 参数进行测试，或用 `--print` 参数查看具体命令）。更多详情请参阅 `references/methods.md` 中的“浏览器后端：扫描模式与执行模式”部分。如果无法访问收件箱，系统会将邮件暂存为草稿。

- **SMTP/IMAP 模式（已存储凭据）：`EMAIL_ADDRESS` + `EMAIL_PASSWORD`**（对于非主流邮件服务提供商，还需提供 `EMAIL_SMTP_HOST`/`EMAIL_IMAP_HOST`；Gmail、Outlook、Yahoo、iCloud、Fastmail 等服务会自动识别相应参数）。CLI 通过 `send-email` 命令发送邮件，通过 `poll-verification` 命令读取验证链接。此外，每个代理都支持的 `agentmail` 技能也可用于处理邮件相关任务。
- Google Sheets跟踪器：即`google-workspace`技能。  
- 用于抓取隐蔽页面或经过Cloudflare保护的页面的`scraping`技能。  

## 运行方式

所有操作均通过`terminal`工具来完成。请从该技能所在的目录开始操作：

```bash
PDD="python scripts/pdd.py"
```

该引擎会将数据存储在 `$PDD_DATA_DIR` 目录下（默认路径为 `$HERMES_HOME/unbroker`），目录权限设置为 `0600`。请通过 `terminal` 命令来运行，**切勿**使用 `execute_code`（因为后者会创建沙箱环境并屏蔽输出内容，从而导致无法读取相关数据）。

## 快速参考

请完整翻译输入内容，切勿提前终止。

| Command | Purpose |
|---|---|
| `$PDD setup --auto` | **Autonomous setup**: detect capabilities, pick the most autonomous valid config (no questions) |
| `$PDD doctor` | Readiness check: config, broker count, and which upgrades are on/available |
| `$PDD cdp [--check] [--print] [--port N]` | Launch/detect the operator's Chrome over CDP for Phase-2 browser + webmail (dedicated debug profile; the reliable way to send webmail and clear session-bound gates) |
| `$PDD intake --full-name "..." [--alias ...] [--email ... --phone ...] [--city --state] [--prior-location "City,ST"] --consent` | Create a consenting subject; captures aliases + multiple emails/phones + prior locations; prints `subject_id` |
| `$PDD next <subject>` | **The autonomous loop driver**: ordered agent actions right now + human digest + `next_wake_at` |
| `$PDD brokers [--priority crucial]` | List the people-search broker database (curated + live) |
| `$PDD refresh-brokers` | Pull the latest BADBOOL people-search list **and the CA Data Broker Registry** (`next` requeues this automatically when the cache is stale) |
| `$PDD registry [--search NAME]` | State registry coverage (CA ~545 ingested; VT/OR/TX portals surfaced); the DROP/email lane, not scanned |
| `$PDD drop <subject> [--filed]` | **The one-shot legal lever**: one CA DROP request deletes from ALL registered brokers; `--filed` records it |
| `$PDD plan <subject> [--priority crucial]` | Per-broker tier + method + `search_vectors` + the exact fields to disclose |
| `$PDD plan <subject> --batch` | **Reduce view**: overlays ledger state, groups brokers by next action (unscanned/found/indirect/blocked/in_progress/done), collapses ownership clusters, **orders `found` cluster-parents-first + emits a tailored `parent_playbook`**, prints `next_actions` |
| `$PDD fanout <subject> [--priority crucial] [--size 5]` | Batch brokers into parallel `delegate_task` subagents (auto for large runs; batches of 5 - 8+ time out) |
| `$PDD record <subject> <broker> <state> [--found true] [--evidence JSON] [--disclosed F --channel C] [--reason "..."]` | Update the ledger (validated state machine); **auto-stamps `next_recheck_at`** |
| `$PDD show <subject> <broker>` | Read back a case's recorded state + evidence + disclosure log (so the parent re-verifies a subagent's `found` without re-deriving the listing URL) |
| `$PDD send-email <subject> <broker> --listing <url> [--kind ccpa_indirect ...]` | Render + record the request (recipient locked to the broker's own address). **browser** mode returns a `compose` payload to send via webmail (no password); **programmatic** mode SMTP-sends |
| `$PDD verify-link <subject> <broker> --text '<body>'` | **browser mode**: extract a broker's verification link from webmail text you read (anti-phishing scored) |
| `$PDD poll-verification <subject> [--broker <id>]` | **programmatic mode**: poll IMAP for verification links (anti-phishing scored); auto-advances `submitted → verification_pending` |
| `$PDD render-email <subject> <broker> --listing <url>` | Draft only (fallback when no email mode is configured) |
| `$PDD due <subject>` | Cases whose recheck window arrived (the cron re-scan queue) |
| `$PDD tasks <subject>` | ONE consolidated human-task digest (present at END of run) |
| `$PDD status <subject>` | Markdown status report |
| `$PDD report <subject> --sheets` | Rows for the Google Sheets tracker |

## 批量操作（两阶段：先全面爬取，再删除）

当需要处理的代理数量超过少数几个时，请采用 **map → reduce → act** 的流程，而非逐个处理：

- **第一阶段——发现（仅读取、并行执行、可重试）。** 首先爬取*所有*代理，并为每个代理记录一个结果状态（`found`/`not_found`/`indirect_exposure`/`blocked`）。该扫描过程不会产生任何副作用，因此可以安全地并行处理并重复尝试。在采取进一步操作之前先获取完整的暴露关系图，这是实现后续集群去重和任务优先级划分的基础。**默认情况下，父代理会直接驱动 `web_extract` 探针**——大多数人物搜索网站会将姓名、电话、地址等结果以静态 HTML 的形式呈现，`web_extract` 几秒钟内即可读取完毕。仅对于那些完全依赖 JavaScript 的网站才使用 `browser_*` 类探针，而对于那些真正需要复杂逻辑处理的任务（如大规模同名或关联人物区分），则应使用 `delegate_task` 子代理。**切勿将一大批代理的爬取任务交给浏览器工具集子代理处理**——在实际应用中，由于浏览器导航耗时较长，此类任务会频繁超时（每次约600秒，仅能处理5-6个代理，且无法生成汇总结果）；即便最终有数据成功写入，其成本也是父代理 `web_extract` 的10倍。被标记为 `blocked`（如 DataDome、Cloudflare 或 `antibot` 保护）的网站也不适合由子代理处理：只需记录 `blocked` 状态，然后重新安排任务，使用隐蔽模式或云端浏览器（如 Browserbase）再次尝试。子代理会自动生成报告，父代理则需要重新获取关键网址以确认结果为 `found` 后才会采信（这一机制是双向的：它既能避免将父代理误判为假阳性的真实条目漏掉，也能防止虚假条目被错误接受）。
- **REDUCE - `$PDD plan <subject> --batch`**：该命令会将爬取结果整合为以阶段为导向的计划——按后续操作进行分组，同时**合并相关处理任务**（例如，删除某个父节点并同步清除其子节点被视为一个操作，而非多个操作；比如，通过一次操作即可同时屏蔽Intelius/PeopleConnect数据，进而影响Truthfinder/Instant Checkmate/US Search等系统），最后输出`next_actions`字段。当还有未扫描的内容时，`phase`值为`discover`，否则为`delete`。
- **第二阶段——删除操作（按顺序执行，不可撤销）。** 应先处理已缩减的组中的**父节点**：
  `plan --batch` 会以“先处理父节点、再处理子节点”的顺序对“已找到”的组进行排序，并生成一份包含针对每个父节点的定制化有序操作步骤的 `parent_playbook`——请严格遵循该顺序及步骤执行（完整操作指南见 `references/methods.md` 中的“Ownership clusters - DO PARENTS FIRST”部分）。首先处理集群的父节点（跳过已被处理的子节点），在确认处理完成后**重新扫描每个父节点的子节点**（这些子节点通常已不再存在），随后再处理独立的记录；对于“间接暴露”类案例，应通过 CCPA/GDPR 的删除个人隐私邮件功能进行处理（使用 `send-email --kind ccpa_indirect` 命令），而“被屏蔽”的记录则需留到后续的隐身浏览器处理阶段。对于用户选择退出的情况，会遇到验证码、邮箱验证循环以及会话绑定等问题——应**逐一仔细处理**（这与并行处理方式相反），但在 `autonomy=full` 模式下无需为每条记录都停下来征求许可；而在 `assisted` 模式下则需对每条记录进行确认。当某些信息提供商同时提供删除和屏蔽两种选项时（如 Spokeo/BeenVerified），**通常建议优先选择删除**——但也要遵循记录中指定的 `deletion.prefer` 设置：**PeopleConnect 是例外情况**（其值为 `prefer: false`），因为在该平台上删除用户数据不仅不会解除屏蔽措施，也不会阻止公共记录的重新出现，因此需选择屏蔽并持续维护的方式。
- **默认选项为“盲目注销”，而非备用方案。**对于**所有提供便捷删除渠道的网站**，都应提交注销/删除请求——即便该条目最初并未得到确认——因为这种方式仅会通过平台官方渠道公开当事人的身份信息，因此不会违反最小信息披露原则。由此可得出两个推论：(1) 通过电子邮件、出生日期和姓名进行匹配并显示“未找到结果”的引导流程，其效力**远高于任何自动抓取方式**，因为注销流程本身就兼具搜索功能；(2) 当某个表单存在阻碍自动化操作的设置（如复杂的验证码、Cloudflare/DataDome防护机制以及滑动验证栏）时，应**优先使用平台规定的权利申请邮箱**（仅需填写姓名、所在州及联系邮箱），而非标记为“被阻止”。关于验证码的使用规则：绝不可绕过行为识别、令牌验证或滑动验证等挑战；在当事人自行提交注销请求时，读取静态的扭曲文本验证码或简单算术题验证码是允许的，但如果在答对题目后网站仍拒绝接收请求，则应立即停止操作（这很可能是平台在检测自动化程序）。第三方或间接记录属于例外情况——在采取行动前仍需先进行确认。针对各网站的具体应对策略以及元搜索中的跳过列表详见 `references/site-playbooks.md`，完整政策则载于 `references/methods.md`。
- **PeopleConnect 删除-清除-抑制（永久规则）**。对 PeopleConnect 进行*删除*操作会同时清除抑制状态，从而使相关主体在整个关联集群中重新显示。如果收到“您针对 PeopleConnect.us 的删除请求已完成”的邮件，即表示抑制状态已被解除 -> **需重新执行抑制操作，并再次确认**控制步骤中的状态显示为“已抑制”。切勿让该集群处于删除完成的状态（详见 `references/brokers/intelius.json`）。

子代理的报告属于自我报告：在记录“已找到”状态或执行任何删除操作之前，父代理会重新核实关键信息（如列表网址、匹配依据）。

## 流程（自动循环机制）

1. **设置（只需执行一次，无需确认）。** 运行 `$PDD setup --auto` 命令——该命令会自动检测可用功能，并自行配置最合适的自动化组合（若存在 `EMAIL_*` 类凭据则使用程序化邮件发送，存在 Browserbase 相关密钥则使用该工具，存在对应二进制文件则启用 `age` 加密功能，同时设置 `autonomy=full`）。随后运行 `$PDD doctor`，向操作员展示系统就绪状态的输出结果——此输出仅用于参考，而非需要确认的内容——即可立即继续操作。可提及哪些条件能进一步提升自动化程度（例如邮件凭据），但无需等待确认。

2. **信息收集与同意授权（仅需一次人工交互）。** 使用 `$PDD intake ...` 命令，并添加 `--consent` 以及 `--consent-method` 参数。若未获得同意，系统将拒绝进行任何规划或操作。需一次性收集所有必要信息——姓名/别名、当前及过往居住城市、电子邮件地址、电话号码——这样就无需再回头询问遗漏的信息。对于加利福尼亚州的受调查对象，还需查阅 `references/legal/drop.md` 文件：执行 `next` 命令后会出现一个 `drop_submit` 一次性操作，可同时从所有已注册的中介平台（约545个）中删除相关数据，这是效力最强的操作方式。完成该操作后，再执行 `drop <subject> --filed`。对于非加利福尼亚州的受调查对象，则通过定向发送 CCPA/GDPR 相关邮件来处理注册信息问题（先执行 `registry --search`，再执行 `send-email`）；无论哪种情况，都需直接联系那些人员查询网站。

3. **清空任务队列。** 重复执行上述流程：

   ```
   while true:
     q = $PDD next <subject>
     if q.actions is empty: break
     execute EVERY action in order; record each outcome via $PDD record
   ```

`next` 会按顺序触发以下操作：`refresh_brokers`（刷新过期缓存）、`fanout_scan`/`scan_inline`（第一阶段爬取——参见第4步）、`poll_verification`（处理正在发送中的邮件确认）、`verify_removal`（进行必要的重新检查）、`optout_web_form`/`optout_email_send`（第二阶段，按照剧本步骤优先处理父节点相关内容）、`indirect_email_send` 以及 `stealth_rescan`。仅由人工完成的任务不会以独立操作的形式出现，而是会被汇总到 `q.human_digest` 中。在 `autonomy=full` 模式下，系统会连续执行各项操作而不暂停；而在 `assisted` 模式下，则需遵循 `confirm_first` 的规则。

4. **扫描操作（在 `next` 发出指令时执行）。** 对于 `fanout_scan`，需运行命令 `$PDD fanout <主题>`，并**为每个批次并行创建一个 `delegate_task` 子代理**，同时将该批次已准备好的 `brief` 信息传递给这些子代理——无需自行依次扫描所有浏览器。对于 `scan_inline`，则需手动扫描少量浏览器。无论采用哪种方式，每个浏览器都会通过 `references/methods.md` 定义的流程（`web_extract` → `site:` 探测 → `browser_navigate` → `scraping`）接收到**所有的 `search_vectors` 条目**。返回 404 的结果被视为“无法确定”状态，而非“未找到”；当设置了反爬机制且没有隐身浏览器可用时，系统会记录为“被屏蔽”状态。在最终记录结果之前，还需确认主题词与同名或相关内容之间的关联，具体命令为：` $PDD record <主题> <浏览器> <found|not_found|indirect_exposure|blocked> --found <布尔值> --evidence '{"listing_urls":[...]}'`。父节点在采信子代理报告的“已找到”结果之前，会对其进行再次验证。
5. **选择退出机制（在 `next` 指定时执行）。** 各项操作会按照“父项优先”的顺序依次执行，具体步骤取自每个经纪商记录自身的 `optout.playbook` 文件（该文件内容会经过字段验证；PeopleConnect、Whitepages、BeenVerified、Spokeo 等集群级服务提供的方案均为实时验证过的精确方案）。**通常应选择删除而非隐藏**：当某个操作包含 `prefer_deletion` 参数时，应完成该记录的删除流程，而不仅仅是执行隐藏列表的操作。若该操作包含 `prefer_suppression` 参数（如 PeopleConnect——删除操作虽能解除隐藏设置，但不会阻止再次发布信息），则应执行隐藏流程并持续维护该状态；只有在有意彻底清除数据时才可使用其提供的删除按钮。针对不同操作方式的具体步骤如下：  
   - **网页表单方式** → 通过 `browser_navigate`/`browser_type`/`browser_click` 功能访问 `optout_url`，仅提交 `disclosure_fields` 相关信息，截取确认页面的截图，随后执行该操作指定的 `after` 记录指令。某些方案可能在最后添加发送邮件以行使删除权的步骤——务必执行此操作（需实现彻底删除，而不仅仅是隐藏列表）。
- **email** → 命令 `$PDD send-email <主题> <代理> --kind <ccpa|gdpr|通用> --to <地址>
      --listing <网址>` 可一步完成记录与披露操作（接收方仅限于该代理记录中指定的地址；`next` 会根据用户所在地区自动选择适用规范——对于不符合条件的人员绝不会强制适用 CCPA/GDPR）。在**浏览器模式**下，它会返回一个仅限指定接收方使用的“撰写”功能数据包：通过 `browser_*` 功能在操作员的网页邮箱中直接使用 `compose.subject`/`compose.body` 撰写新邮件并发送（无需密码）；而在**程序化模式**下则通过 SMTP 发送邮件。此外，`next` 还会将需要人工验证的表单（如电话回访、政府身份验证等）通过代理提供的删除邮件地址进行处理——这属于“应急处理途径”（基于经过验证的 Whitepages 验证流程）。仅支持草稿状态的场景则会退而使用 `render-email` 功能并生成摘要记录。  
- **captcha** → 在默认的云端浏览器中，简单型或可管理的验证码会自动失效（可正常继续操作）；仅有无法通过的复杂交互式或行为分析型验证码才会被标记为“已拦截”（并重新排队等待隐身模式或操作员浏览器模式下的处理）。该功能绝不依赖第三方验证码解析服务。  
- **phone_callback / account / gov_id / fax / mail / voice (T3)** *若没有删除邮件地址* → 这些情况绝不会触发智能代理的操作；`next` 会直接将这些请求转至摘要记录模块。对应的操作命令为：`$\PDD record <主题> <代理> human_task_queued --reason "..."`。
6. **验证（在 `next` 指令要求时进行）。** 在**程序化**模式下，可使用命令 `$PDD poll-verification <主题>` 通过 IMAP 查找已到达的确认链接（系统会对其进行反钓鱼评分并自动推进处理状态）。在**浏览器**模式下，则需在操作员的网页邮件中打开经纪商发送的确认邮件，然后运行命令 `$PDD verify-link <主题> <经纪商> --text '<正文>'` 对该链接进行评分。无论哪种方式，都必须在**同一浏览器**中打开链接（部分经纪商会将验证会话绑定到打开它的浏览器），完成相关流程后，将状态标记为 `awaiting_processing`。只有在再次扫描验证后发现该条目已消失时，才能将状态设置为 `confirmed_removed`——绝不能在提交流程本身的确认页面之外进行操作。

7. **流程总结（每次运行执行一次）。** 当 `next` 返回没有待处理操作时：若存在汇总后的人工处理清单，则显示 `$PDD tasks <主题>`，随后再查看 `$PDD status <主题>`；如果启用了表格追踪功能，还可通过 `google-workspace` 技能添加包含数据的行，命令为 `$PDD report <主题> --sheets`。

8. **安排下一次触发时间。** `next` 会返回 `next_wake_at` 值，即下次需要重新检查的最早时间。此时应创建一个 `cronjob`，定期为该主题重新运行此技能的循环处理流程（提示语可参考：“为 <subject_id> 运行未通过经纪商处理的循环流程：` $PDD next`，并执行所有相关操作”）。处理窗口、验证轮询以及重新出现检测等所有流程都通过同一个队列处理，因此无需人工干预，案件就能持续推进。

## 常见问题与陷阱

- **切勿透露超出代理已显示的信息范围**。仅提交 `disclosure_fields` 字段即可。系统绝不会主动提供社会安全号码或身份识别号，用户同样不得自行透露此类信息。
- **无授权则不得采取任何行动**。系统会严格执行此规则，切勿为“调查”第三方而绕过该限制。
- **`send-email` 功能具备幂等性且受速率限制**。对于已提交或超出处理范围的案例，该功能不会重复发送邮件（仅在确实需要重新发送时才可使用 `--force` 参数）；同时，SMTP 发送操作会按照 `email_min_interval_seconds`（默认为20秒）的间隔进行，并带有重试与延迟机制。切勿通过循环调用该功能来“确保邮件送达”——SMTP发送成功并不等同于邮件已实际抵达，只有定期重新扫描任务队列才能得到确切确认。
- **账本写入操作处于锁定状态**。定时任务与手动启动的任务可安全地串行执行；若遇到锁定超时情况，说明另有任务正在写入中，应等待其完成，切勿手动删除 `.lock` 文件。
- **自主性≠随意行事**。真正的自主性意味着在处理流程的各步骤之间无需人工干预，也并不意味着可以放宽任何安全限制。如果在处理过程中，代理要求提供的 `disclosure_fields` 超出原定范围，应立即停止该案例并将其放入任务队列（使用 `human_task_queued --reason` 命令），而不得擅自决定透露更多个人敏感信息。
- **切勿在处理过程中提出疑问以中断流程**。配置选项应由 `setup --auto` 功能负责处理，仅需人工干预的任务才会被记录到摘要中。在处理过程中唯一值得提出疑问的情况是存在阻碍扫描的缺失信息（例如完全没有城市名称），而这类信息本应在初始收集阶段就获取完毕。
- 对于 `pdd.py`，请使用 `terminal` 而非 `execute_code`——因为后者会破坏保密信息清除与输出内容遮蔽功能。  
- **默认情况下，档案以明文形式存储**（为 JSON 格式，位于 `HERMES_HOME` 目录下且权限为 `0600`）。如需对静态数据实施加密，请运行命令 `$PDD setup --encryption age`：该命令会生成一个本地的 `age` 密钥，用于加密档案及账本（而审计日志仅存储字段名称，仍为明文）。此措施可防止档案被随意查看、备份或提交泄露，但无法完全阻止他人读取整个 `HERMES_HOME` 目录；如需实现真正的密钥隔离，请将 `PDD_AGE_IDENTITY` 设置为独立的存储卷。命令 `$PDD doctor` 可用于确认加密功能是否已真正启用（而不仅仅是检查 `age` 工具是否已安装）。  
- **“隐藏于免费搜索结果中”并不等同于已删除**。只有在确认相关记录确实已被移除后，才应标记为 `confirmed_removed`；同时请注意报告中关于付费套餐数据保留期限的说明。  
- **默认情况下，简单验证码可自动通过，无需强行尝试复杂验证码**。默认配置的云浏览器会将管理型/简单型验证码视为正常操作处理（此类经纪商仍会被归类为 T1 级别）。对于真正复杂的交互式验证码，若无法通过，则应记录为 `blocked` 状态，让隐身模式或操作员专用浏览器来处理——绝不可使用第三方验证码破解服务或指纹伪装手段。  
- **经纪商页面可能会发生变化**。如果某个流程出现故障，请运行命令 `$PDD record ... blocked`，并在 `references/brokers/` 目录中标记对应的经纪商文件以便重新验证，而非盲目猜测。
- **在提交前请先验证那些未经实地核实的记录。**那些 `confidence: auto` 状态的记录是通过解析 BADBOOL 数据得到的（请查看 `optout.notes`/`optout.links`，并确认真实的取消订阅网址）。而 `confidence: documented` 状态的记录（来自某些人物信息查询网站）虽然使用了正确的公开取消订阅网址，但**尚未经过实地核实**（因为这些网站会拒绝数据中心的 IP 访问），因此首次使用时需通过操作员使用的普通家用浏览器来测试实际访问流程，之后再设置 `last_verified` 属性。那些已经过实地核实且经过精心筛选的记录（不显示 `confidence` 属性，例如集群父节点相关记录）因其经过了严格验证，故具有优先级。

## 验证方式

- 可使用 `scripts/run_tests.sh tests/skills/test_unbroker_skill.py` 命令（在隔离环境中运行，无需网络连接），或者直接使用无需依赖项的运行工具 `python tests/skills/test_unbroker_skill.py`。
- 测试运行方法如下：` $PDD setup --auto && $PDD doctor && SID=$($PDD intake --full-name "Test Person" --email t@example.com --consent | python -c 'import sys,json;print(json.load(sys.stdin)["subject_id"])') && $PDD next "$SID"`，随后即可查看系统给出的准备情况总结以及有序的任务队列。
