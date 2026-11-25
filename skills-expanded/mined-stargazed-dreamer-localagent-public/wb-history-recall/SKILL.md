---
name: wb-history-recall
description: 从本机 WorkBuddy 会话库（workbuddy.db + projects/*.jsonl）还原历史对话，找回「用户当时到底怎么说的 / 这个决定是哪来的 / 是不是我说过」。默认同时抽用户原话与 agent 回复，⛔ 禁止只看用户一侧。除对话正文外还能取：会话状态与最后活动时间（list）、尾部若干条（dump --tail）、被 Edit/Write 写过的文件清单（dump --files）。当用户说「这条要求我不是说过吗」「你去 workbuddy 数据库里翻一下」「另一个账号里那个对话」「当时到底谁定的」「这话是我说的还是你说的」时使用。
agent_created: true
task_type: adhoc.wb_history_recall
---

# 翻 WorkBuddy 历史会话（还原对话，不是单方面取证）

## 0. 铁律：不要只读用户说了什么

历史会话里，**用户的话和 agent 的话是一对**。只抽用户一侧就变成「有倾向性的取证」，三种误判必然发生：

| 只看用户侧会怎么错 | 真相在哪 |
|---|---|
| 把 agent 提的方案写成「用户要求」 | agent 那条回复里有「我建议 A/B/C」，用户只回了「B」 |
| 把用户一句反问当成最终裁定 | agent 后面可能追问、可能实现成别的、可能被用户再推翻 |
| 看不懂用户在指什么（「这个」「那个」「不是这样」） | 指代对象全在 agent 上一轮 |

⇒ **默认 `dump` 出双方**，按时间顺序读完整轮次，再下结论。
只有任务本身是「取用户逐字原话当引文」时才用 `--user-only` 收窄输出，**但判断语境仍要回来看 agent 侧**。

第二层铁律：**「用户说了什么」和「最后落地的是什么」是两件事**，别用前者代替后者。用户的话是需求/裁定，agent 的回复是执行与偏差，两者对不上时以时间靠后的那条为准，并记下推翻链。

## 1. 数据在哪

| 是什么 | 路径 |
|---|---|
| 会话索引（标题/账号/时间/状态/工作目录） | `<user_home>\.workbuddy\workbuddy.db` → `sessions` 表 |
| 会话正文（逐事件 jsonl） | `<user_home>\.workbuddy\projects\<workspace-slug>\<session-id>.jsonl` |
| 工具调用与文件快照 | 同一文件里的 `type=function_call` / `file-history-snapshot` 事件（**不在 message 里**） |
| 另存的大工具结果 | 同目录 `<session-id>/tool-results/` |
| 账号私有目录（记忆/身份） | `.workbuddy/user-<uuid>-personal/` |

- `<workspace-slug>` = 工作目录路径把 `/` 换成 `-`，例：`<project_root>` → `f-project_temp-Parcae`。
- **一台机器并存多个账号**，同一 `workbuddy.db` 用 `sessions.user_id` 区分（本机当前两个）。`list` 输出的第三列就是 `user_id` 前 8 位，**以它为准**，别把某次的 uuid 当常量背下来。
  ⇒ **只按「当前账号」找会漏**，用户说「另一个账户」时按 `user_id` 分组即可。
- `sessions` 表里还有几列对判读有用：`status`（`working` / `completed` / `error` / `archived`）、`last_activity_at`、`is_playground`、`mode`、`model`。`list` 已显示状态与最后活动时间。
- 上下文用满没有，看 `session_usage` 的 `used` / `size`（如 218188/300000）——**接近满的会话，后半段是靠压缩摘要接的**，见坑 8。
- 用户有时用**登录手机号**指代账号。⛔ 本机配置（`~/.workbuddy/*.json`）里**没有** account/phone 字段，
  `workbuddy.db` 只有 uuid ⇒ **无法反查**。手机号 ↔ `user_id` 的映射落**不入库**的
  `data/wb_accounts.json`（`.gitignore` 的 `data/*`），读写走
  `uv run python -m tools.wb_takeover accounts`（`--set 手机号=uuid8` 登记）；
  手机号属个人信息，本 skill 与 `machine/` 都入库，正文不许写明文。

## 2. 一条命令拿到

```bash
uv run python -m tools.wb_history list                        # 全部会话（创建时间倒序）
uv run python -m tools.wb_history list --sort activity         # 按最后活动排序（找「最近还在动的那场」）
uv run python -m tools.wb_history list -k 提示词,交接,管家       # 按标题筛（跨账号）
uv run python -m tools.wb_history dump 46e11254               # 还原该会话双方发言（默认）
uv run python -m tools.wb_history dump 46e11254 -k 版本,回滚    # 只留命中关键词的条目（双方都筛）
uv run python -m tools.wb_history dump 46e11254 -k 版本 -c 2    # 命中条目各带前后 2 条上下文
uv run python -m tools.wb_history dump 46e11254 --tail 40      # 只看最后 40 条
uv run python -m tools.wb_history dump 46e11254 --files        # 附加「改过哪些文件」
uv run python -m tools.wb_history dump 46e11254 --user-only    # 只要用户原话（逐字取证）
uv run python -m tools.wb_history dump 46e11254 --clip 300     # agent 回复截到 300 字
```

产物：`temp/wb_hist/<session>_chat.md`（`--user-only` 时 `_user.md`），终端同时打**首句目录**
（`[序号] U/A 字符数 首 90 字`，U=用户、A=agent）。**先看目录再定点读**——12 MB 的会话整份读进来会吃掉半条上下文。

**编号规矩（引用前必读）**：`[n]` = 该会话的**全量条目序号**，不因 `-k` / `-c` / `--tail` / `--user-only` 重排。
过滤后跳号就是被过滤掉的条目。写结论时用这个号（例：`46e11254 #121`），别用「第 3 条输出」这种相对说法。
⚠ 脚本的噪音过滤规则升级会整体位移编号（例如 2026-10-30 加了 task-notification 过滤），
所以**跨版本引用要把 session id + 时间 + 原话一起写**，号只作定位辅助。

**如果要接着往下做（接手/续做）**，除了还原对话，另外三条命令直接对应三件事：

| 想知道 | 命令 |
|---|---|
| 最近还在动的是哪场、做完了没有 | `list --sort activity`（看 `status` 与「最后活动」） |
| 会话停在哪、最后一轮是谁说的 | `dump <id> --tail 20` |
| 这活改了哪些文件（改动面） | `dump <id> --files` → 文件清单 + 写入次数 |

⚠ 要**正式接手**（出接手包 + 给派发提示词，让另一个 agent 读完就接着做）走 `wb-takeover`：
`uv run python -m tools.wb_takeover scan` → `export --pick 1,3`。本 skill 只管「还原发生了什么」。

## 3. 判读流程

1. `list -k` 多关键词扫标题（标题是自动生成的，常和用户记忆里的叫法不一致）→ 不中再 `dump <id> -k 正文词,词 -c 2` 按正文筛。
2. `dump` 出双方 → 读首句目录，找出**用户那条**和**紧邻的 A 条**。
3. 一轮一轮看：用户在回应什么？agent 给的选项有哪些？用户选/否了哪个？
4. 结论要带**谁说的 + 时间 + 前后语境**，形如：

   > 10-28 17:43 用户：「最多 10 个版本，不允许修改历史版本」（`46e11254`，关键词「最多 10 个版本」）
   > 10-28 21:41 用户：「不做多版本保存，只保留当前这一个版本」（同一场，关键词「只保留当前」）
   > ⇒ 用户自己改主意，不是 agent 失忆；但后一条之前 agent 提示过「这样历史版本会清零」

   ⚠ 示例里**故意不写死条目号**：编号会随脚本过滤器版本位移（见 §2），用「关键词 + 时间」复现最稳；真要写号就写成 `46e11254 #121（2026-10-30 口径）`。

5. **引 agent 的话必须标 agent**，混着写就是伪造原话。
6. 用 `-k` 收窄时**加 `-c 1~3`**：命中条目的前一条 agent 回复常常就是它的指代对象，不带上下文容易把「这一版」读错。
7. 引用格式固定为 `会话id前缀 #条目号 + 时间 + 原话/转述`，三方缺一不可（编号会随脚本过滤器版本位移，见 §2）。

## 4. 九个坑（都踩过）

1. **标题对不上用户记忆**。用户说「审查本地代理提示词开关什么的」，库里真标题是「审查本地代理提示词开关文件」。→ 多关键词 + 必要时扫正文。
2. **用户话术裹在注入块里**。`role=user` 大多由 `system-reminder` / `identity_context` / `project_context` / `connector-status` 拼成，真话在 `<user_query>` 内，不去掉这层 90% 是噪音（脚本已处理）。
3. **压缩摘要冒充原话，且它内层还包着 `<user_query>`**。`role=user` 的 `<cb_summary>…</cb_summary>` 是**摘要块，内部回放着若干条历史原话**；`<conversation_history_summary>` 是另一种旧形态。本机实测 521 条 `cb_summary` 里 **520 条整条只是摘要**（没有本轮输入），1 条在摘要后另跟真实输入。
   ⛔ 所以**不能「取最后一个/第一个 `<user_query>`」**——正确做法是先剥 `cb_summary` 块，剥完没内容就整条丢弃。2026-10-30 之前的版本取第一个命中，会把历史原话贴上本轮时间戳当新条目（实测 `a58acd55` 输出的「用户原话」是上文引用的一个路径，真正的输入「那不搞了，就接受可能有时候崩溃的事实吧」整条丢失）。
4. **三种「不是人话」的行也会落在 `role=user` 里**：`<task-notification>`（后台任务完成通知，本机 891 条）、`<teammate-message>`（团队其它 agent，37 条）、续写指令 `Please continue with the conversation based on the summarized context above…`（89 条）。它们没有 `<user_query>`，不挡掉就会被当成用户要求。脚本按前缀挡。
   另有一种**要留但要会读**的：用户「引用某条消息」时会写成 `<message_quote type="text" source_message_id="…">被引原文</message_quote>` + 自己的话（实测 `46e11254` 有这种）。**被引的那段不是用户此刻的主张**（多半是引 agent 上一轮的话来质疑），判读时把引用块和用户自己的话分开看。
5. **命令行里出现家目录路径可能被沙箱拒**。绕法：路径写进脚本（`tools.wb_history` 已内置），或 `copy` 子命令先拷到 `temp/wb_hist/`。
6. **时间戳是毫秒 epoch**。`datetime.fromtimestamp(ts/1000)`。渲染只到**分钟**，同一分钟内多条分不出先后——跨 harness 比「谁更晚」时若撞在同一分钟，要回去看原始 `timestamp`，别拿渲染值下结论。
7. **工具调用不在 `message` 事件里**，`type` 是 `function_call` / `function_call_result`（一个会话实测 280 / 278 条）。所以「只看 message」拿不到任何工具信息；`--files` 就是去这层取 `Edit`/`Write` 的 `file_path`。⚠ 它统计的是**写入次数**，不等于最终状态（同一文件改 30 次也只算一个路径）。agent 正文里常夹大段代码/工具回显，默认照抽保真，嫌长用 `--clip N`（被截条目会标「已截断，原 N 字」）。
8. **上下文压缩点之后，agent 当时看不到原文**。会话被压缩过时，前面的轮次对新会话而言只是摘要；读历史时原文仍在 jsonl 里，但**不能据此推断「当时的 agent 知道这些」**。判断是否压缩过：有 `cb_summary` / `<conversation_history_summary>`，或 `session_usage.used/size` 接近满。
9. **同一 session 多份同名 jsonl 的旧坑已不复现**：2026-10-30 实测 345 个 jsonl 里重名 0 个（历史这条记的是早期形态）。脚本仍保留多命中告警，遇到就看一眼文件大小与 mtime 再选。

## 5. 案例

- `references/case-20261028-prompt-versions.md`：派单提示词「多版本 vs 单版本」到底谁定的——双方逐条对照的完整样例，含「单看用户侧差点冤枉自己失忆」的过程。
