---
name: qoder-history-recall
description: 从本机 Qoder（QoderCN）会话库（~/.qoder-cn/projects/<workspace-slug>/<session-id>.jsonl）还原历史对话，找回「我在 Qoder 里到底怎么说的 / 那个决定是哪来的 / 这话是不是只在别的 harness 说过」。默认同时抽用户原话与 agent 回复，⛔ 禁止只看用户一侧。除对话正文外还能取：尾部若干条（dump --tail）、被写过文件的清单（dump --files，来自 file-history-snapshot）、压缩点位置。当用户说「Qoder 里那个对话」「我在 qoder 说过」「翻一下 qoder 数据库」「另一个 IDE 里那场」「qoder 那边怎么定的」「qoder 会话记录」时使用。
agent_created: true
task_type: adhoc.qoder_history_recall
---

# 翻 Qoder 历史会话（还原对话，不是单方面取证）

> 与 `wb-history-recall` 是**同一条铁律的两套落点**：那边读 WorkBuddy 的 `workbuddy.db + projects/*.jsonl`，
> 这边读 Qoder 的 `~/.qoder-cn/projects/*/*.jsonl`。同一件事可能在两个 harness 都聊过，
> 只翻一边就下结论 = 漏证据；结论里**必须标明是哪一边的原话**。

## 0. 铁律：不要只读用户说了什么

用户的话和 agent 的话是一对。只抽用户一侧必然出现三种误判：

| 只看用户侧会怎么错 | 真相在哪 |
|---|---|
| 把 agent 提的方案写成「用户要求」 | agent 那条回复里有「我建议 A/B/C」，用户只回了「B」 |
| 把用户一句反问当成最终裁定 | agent 后面可能追问、可能实现成别的、可能被用户再推翻 |
| 看不懂用户在指什么（「这个」「这一版」「不是这样」） | 指代对象全在 agent 上一轮 |

⇒ **默认 `dump` 出双方**，按时间顺序读完整轮次再下结论。
只有「取用户逐字原话当引文」时才用 `--user-only` 收窄输出，**判断语境仍要回来看 agent 侧**。

第二层铁律：**「用户说了什么」和「最后落地的是什么」是两件事**。对不上时以时间靠后的那条为准，并记下推翻链。

## 1. 数据在哪

| 是什么 | 路径 |
|---|---|
| 会话正文（一个会话一个 jsonl） | `<user_home>\.qoder-cn\projects\<workspace-slug>\<session-id>.jsonl` |
| 工作目录（真实路径，别靠 slug 反推） | 每行的 `cwd` 字段，如 `<project_root>` |
| 改过哪些文件（快照） | 正文里的 `type=file-history-snapshot` → `snapshot.trackedFileBackups`（键=相对路径，值含 `version`/`backupTime`） |
| 压缩点 | 正文里的 `type=system` + `subtype=compact_boundary`（带 `compactMetadata.preTokens`） |
| 压缩快照 / 文件历史 | 同根 `file-history/`、`session-env/<session-id>/`（排查用，不是对话正文） |
| 国际版根（本机**没有 `projects/`**） | `<user_home>\.qoder` |

- `<workspace-slug>` = 工作目录路径把 `:`/`\`/`/` 换成 `-`：`<project_root>` → `F--project-temp-Parcae`。
- **没有 sessions 索引表**（Qoder 不像 WorkBuddy 有 `workbuddy.db`）⇒ 标题只能现推：取**首条人类消息前 45 字**。
  该消息实测基本落在前几行（代码留到 400 行只是余量，不是"它可能在第 300 行"），`list` 扫 98 个文件不到 1 秒。
- ⛔ **别去 `AppData\Roaming\Qoder*\User\` 找会话**：那是 VSCode 壳的 `state.vscdb`，本机实测停在 8-29，
  里面没有对话正文。真正的会话只在 `~/.qoder-cn/projects/`。
- 本机实测（2026-10-30）：98 个会话文件、11 个**没有人类消息**（纯子代理/自动任务），
  体积中位 2.3 MB、最大 113 MB。
- 会话文件的 mtime 就是**最后活动时间**，`list` 按它倒序 —— 想找「最近还在动的那场」直接看列表头部。

## 2. 一条命令拿到

```bash
uv run python -m tools.qoder_history list                     # 全部会话（按最后活动倒序）
uv run python -m tools.qoder_history list -k 抽卡,管家          # 按标题筛（首条人类消息）
uv run python -m tools.qoder_history list -k 空转 --deep        # 标题不中再全文扫（慢，逐个文件）
uv run python -m tools.qoder_history dump f0c85849            # 还原该会话双方发言（默认）
uv run python -m tools.qoder_history dump f0c85849 -k 版本,回滚  # 只留命中关键词的条目（双方都筛）
uv run python -m tools.qoder_history dump f0c85849 -k 版本 -c 2  # 命中条目各带前后 2 条上下文
uv run python -m tools.qoder_history dump f0c85849 --tail 40   # 只看最后 40 条
uv run python -m tools.qoder_history dump f0c85849 --files     # 附加「改过哪些文件」
uv run python -m tools.qoder_history dump f0c85849 --user-only # 只要用户原话（逐字取证）
uv run python -m tools.qoder_history dump f0c85849 --clip 300  # agent 回复截到 300 字
uv run python -m tools.qoder_history dump f0c85849 --tools     # 额外列出每条 agent 消息调了哪些工具名
uv run python -m tools.qoder_history copy f0c85849             # 只把 jsonl 拷到 temp/qoder_hist/
```

产物：`temp/qoder_hist/<session>_chat.md`（`--user-only` 时 `_user.md`），终端同时打**首句目录**
（`[序号] U/A 字数 时间 首 90 字`，U=用户、A=agent）。**先看目录再定点读**——
113 MB 的会话整份读进来会吃掉半条上下文（脚本本身流式读，1.5 秒跑完，慢的是"人读"）。

**编号规矩（引用前必读）**：`[n]` = 该会话的**全量条目序号**，不因 `-k` / `-c` / `--tail` / `--user-only` 重排；
跳号就是被过滤掉的条目（默认会跳掉"只有工具调用、没有正文"的空回复）。写结论用这个号，
并带上 session id + 时间，因为**脚本过滤器升级会整体位移编号**（2026-10-30 就是这么变的）。

**如果要接着往下做（接手/续做）**，除还原对话外，这三条直接对应三件事：

| 想知道 | 命令 |
|---|---|
| 最近还在动的是哪场 | `list`（已按 mtime 倒序，第一屏就是） |
| 会话停在哪、最后一条是什么（正常收尾/额度用完/被打断） | `dump <id> --tail 20` |
| 这活改了哪些文件（改动面） | `dump <id> --files` → 相对路径 + 版本号 + 末次时间 |

## 3. 判读流程

1. `list -k` 多关键词扫标题（自动推的标题常和用户记忆里的叫法不一致）→ 不中加 `--deep` 扫正文。
2. `dump` 出双方 → 读首句目录，找出**用户那条**和**它紧邻的 A 条**。
3. 一轮一轮看：用户在回应什么？agent 给的选项有哪些？用户选/否了哪个？
4. 结论带**谁说的 + 时间 + 前后语境**，形如：

   > 10-30 14:46 用户：「《异环》：等我告诉你启动好了，你再来做」（`f0c85849`，关键词「等我告诉你启动好了」）
   > 10-30 16:55 用户：「启动好了，现在是角色抽卡界面……以后固定流程你自己找过去」
   > ⇒ 不是 agent 自作主张提前跑，是用户在后面那条明确放行

   ⚠ 示例**故意不写死条目号**：编号随脚本过滤器版本位移（见 §2），用「关键词 + 时间」复现最稳。

5. **引 agent 的话必须标 agent**，混着写就是伪造原话。跨 harness 时再加一句来源，如「（Qoder 侧，非 WorkBuddy）」。
6. 用 `-k` 收窄时**加 `-c 1~3`**：命中条目的前一条 agent 回复常常就是它的指代对象。
7. 引用格式固定为 `会话id前缀 #条目号 + 时间 + 原话/转述`，并注明编号口径日期。

## 4. 九个坑（都踩过）

1. **`type=user` 大多不是用户**。本机实测 76,916 条 user 行里只有 769 条是人类：其余是**工具回显**
   （带 `toolUseResult`）与内部重试。真人类判据 = `origin.kind == "human"`（新版本另带 `humanInput`）。
   `origin.kind` 还有 `task-notification` / `malformed-tool-use-retry` / `stream-recovery` 三种，一律不是人话。
   附带好处：347 条 `This session is being continued…` 实测**全部不是 human**，不用再加前缀黑名单。
2. **一条 agent 回复被拆成多行**。thinking / text / tool_use 各占一行、共用 `message.id`，
   实测一条回复最多 5 行；不按 `message.id` 聚合，一个回合会碎成几百条「只有工具调用」的空回复
   （首次实现就踩了：4.8 MB 会话抽出 586 条，其中 405 条是空的）。脚本已聚合，别改成逐行 yield。
3. **压缩摘要冒充原话**。user 行的 `This session is being continued from a previous conversation…`
   是 agent 写的摘要；`[Request interrupted by user]` 是中断标记。两者都不是用户原话，脚本默认丢弃。
4. **压缩点之后，当时的 agent 看不见原文**。`type=system` + `subtype=compact_boundary` 就是这条线
   （本机 362 条，带 `compactMetadata.preTokens`）。压缩点之前的轮次在库里仍是原文，
   但**当时的 agent 只看到摘要** ⇒ 别据此推断「它当时知道这些」，也别把摘要里的转述当原话。
   写结论时区分「原文（可直接引）」与「摘要区（只能当线索）」。
5. **标题对不上用户记忆**。没有标题字段，只有首条人类消息；用户说「审查提示词那个」，
   实际首条可能是「看一下抽卡记录汇总项目里面的那些工作区…」。⇒ 多关键词 + `--deep`。
6. **时间戳两种格式**。user/assistant 是 ISO 字符串（`2026-10-30T06:46:22.298Z`，**UTC**），
   `runtime-config` / `active-leaf` 是毫秒 epoch。脚本统一转本地时区，别自己 `fromtimestamp` 字符串。
   渲染只到**分钟**：同一分钟内多条分不出先后，跨 harness 比「谁更晚」撞到同分钟要回原始值看。
7. **11/98 个文件没有人类消息**。那是子代理或自动任务落的盘，不代表「会话丢了」，更别当正文读。
8. **大文件别整份读**。最大 113 MB；`--deep` 会逐个文件全文扫，配合 `-n` 用，别默认开。
   `--files` 读的是 `trackedFileBackups`（本机实测 31/31 非空），它给的是**快照版本**不是编辑次数；
   版本号大 = 这文件被反复改过，是接手时的重点，想数逐次编辑只能 `--tools` 或读原文。
9. **两版根目录并存**。国内版 `~/.qoder-cn`（本机活跃）、国际版 `~/.qoder`；
   脚本按「真有 `projects/*/*.jsonl`」选根，可用 `QODER_HOME` 覆盖。拿不准时看 `list` 打印的 `[根]`。
   另：命令行里出现家目录路径可能被沙箱拒（与 wb 同坑），绕法是路径写进脚本（已内置）或先 `copy`。

## 5. 和 wb-history-recall 怎么配合

| 场景 | 走哪个 |
|---|---|
| 明确说「WorkBuddy / 另一个账号 / wb 数据库」 | `wb-history-recall`（有 `sessions` 索引，可跨账号分组、有 status） |
| 明确说「Qoder / 那个 IDE / qoder 里」 | 本 skill |
| 只记得「我说过」，不记得在哪说 | 两边都翻：先 `qoder_history list -k`，再 `wb_history list -k`；对不上就 `--deep` |
| 同一决定两边都有 | 以**时间靠后**的为准，并把「哪边说、什么时候、谁推翻谁」写进结论 |
| 想知道「这活停在哪、改过哪些文件」 | 两边各跑 `dump <id> --tail 20` / `--files`，再按文件路径求并集——同一任务常跨 harness 改同一批文件 |

⛔ 别把两边的原话混成一段当证据：同一个用户在两边措辞不同，混写等于制造一句他没说过的话。
