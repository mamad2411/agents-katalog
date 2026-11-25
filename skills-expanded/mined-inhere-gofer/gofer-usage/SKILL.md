---
name: gofer-usage
description: "gofer 使用指引（这是使用指引，不是开发 gofer 本身的文档）。gofer 把 codex / claude 等 agent 与项目桥接成异步任务控制平台。以下情况使用：工作区说明提到 gofer、仓库有 .gofer/tracker、会话开场注入了 gofer 上下文；需要在容器外或另一台机器跑命令、做多服务联调；要把活派给 codex / claude 等 agent（gofer job）；用 issue / memory / plan / todo 立项、跟踪、接手或交接开发（gofer issue brief / plan brief）；验收 job、留痕、写记忆；用户要离开电脑、想把会话交给 web 或手机继续（session relay）；对外或不可逆操作需要人在 web 批准（--hold）；gofer 命令报错（unknown project、连不上、worker / agent 被拒）需要排查。"
---

# gofer 使用指引

> 本 skill 讲**任意项目怎么用 gofer**。项目自己的约定（能否本地提交、push 是否要授权、验证命令、发版步骤）以 prime 注入的 **rule 记忆**和项目说明为准。细节在 `references/`，按第 6 节的索引按需读。完整 flag 一律以 `gofer <cmd> --help` 为准。

## 0. gofer 是什么

- 一套「server + 若干 worker」的任务执行网：`gofer job` 把命令或 agent 任务提交给 server，在 **server 本机**（`--runner server`，`local` 是同义写法）或某台 **worker**（`--runner <worker-id>`）上执行。
- server 是策略权威（哪个 project 能用哪些 agent / runner）；worker 提供能力（目录、装了哪些 agent）。
- 同时提供仓库内的 issue / memory 跟踪（`.gofer/tracker/`）、plan + todo 链、验收台、终端会话的 web 中继、工作项与 web 控制台。

## 1. 30 秒自检 + project key

```bash
command -v gofer             # 在 PATH 上吗
gofer job list 2>&1 | head   # 能列出 job = 已连上 server
gofer project list           # 找本工作区的 project key（client 模式即 server 的实时列表）
```

- `gofer` 启动时自动加载 `$GOFER_CONFIG_DIR/.env`（`GOFER_SERVER_ADDR` / `GOFER_SERVER_TOKEN`），**无需手动 source、无需传 token**。纯客户端节点只要这个 `.env` + `GOFER_RUN_MODE=client`（`gofer init client` 生成），见 [client-config.md](references/client-config.md)。
- 连不上 / 401：server 没起或 `.env` 不对，见 [troubleshooting.md](references/troubleshooting.md)；这种环境先别用 gofer。
- **project key**：提交必须带 `-p <project>`。按优先级找：① 工作区的 CLAUDE.md / AGENTS.md 写明的 key；② `gofer job list` 的 PROJECT 列；③ `gofer project list`。key 因工作区而异，**不要硬编码**；必须已在 server 注册，否则 `unknown project`。不带 `-p` 且 cwd 匹配不到项目时会落到内置 `default` 项目。

## 2. ★ 开发流程速查

一项开发从接手到收尾的常用路径。

### 开场 / 接手

- 会话开场 prime 已注入：提交策略、当前重点（进行中 plan、未提交 / 未推送的改动）、ready issue、rule 记忆全文、记忆索引。缺了就手动 `gofer repo prime`。
- 接手某个 issue / plan：**先跑** `gofer issue brief <id>` / `gofer plan brief <plan>`——一次拿齐字段、方案评论、上下文树、设计稿、相关提交与代码入口、相关 job / plan、验证命令、适用记忆。不要自己 grep / 翻 git log 拼。
- 开工：`gofer issue update <id> --claim`。

### 立项：issue + 验收标准

```bash
gofer issue create "标题" --type feature|bug|task|epic -p <0-4> -l a,b -d "背景" \
  --design "要点 / 设计稿路径" --acceptance "- 可检验的完成条件" [--parent <epic>]
```

- 大事建 epic，子项 `--parent`（id 形如 `<epic>.N`）。没写验收标准的，brief 会提示补：`gofer issue update <id> --acceptance "…"`。
- 设计稿头部写 issue id、issue 的 `--design` 写设计稿路径，brief 才找得到。顺带发现的问题立刻建 issue（`--from <id>` 或 `--parent`），不要只写在聊天里。

### 建 plan，步骤全写成 todo

```bash
gofer plan create --project <p> --title "…" --tags x,y --desc "目标 / 范围 / 验收"
gofer plan add-todo <plan> "T1 …"                 # 每一步都建；建出来是 pending（add-todo 没有 --status）
gofer plan set-todo <todo> --status doing         # 推进；完成 --status done --note "结论 / 提交 / job id"
gofer plan set-status <plan> done                 # 全部完成
gofer plan handoff <plan> --set "下一步…"          # 阶段交接
```

- 能自动接力的步骤：`add-todo … --assign <agent> --after prev [--acceptance …] [--scope 'glob,…']`，链末加 `--assign exec --cmd '<构建/测试命令>'` 复核项，然后 `gofer plan run <plan>` 一次开工：前一项 done 后一项自动出 job，失败停在那一项（plan `blocked` 并通知）。
- agent 写的方案末尾若带 `gofer-todos` 块：`gofer plan import <plan> --from-job <id> --dry-run` 直接转成 todo 链。
- 需要人拍板的分叉：MCP 工具 `gofer_ask_human` 阻塞提问，人在 web 作答。详见 [plans-workflows.md](references/plans-workflows.md)。

### 派活：job 挂 plan、带标题

```bash
gofer job run -p <p> -a exec --runner server --plan <plan> --title "<一句话>" \
  --cwd <相对项目根> [--sync --wait-timeout 60 | --timeout 1800] -- bash -lc '<命令>'
gofer job logs <id>          # 取 stdout / stderr（--sync 只回状态）
gofer job watch <id>         # 异步任务跟随到结束
```

**两条必守约定**：

① **工作目录用 `--cwd`（相对项目根），不要在命令里 `cd` 绝对路径。** job 在哪台机器执行，路径就按那台机器的项目根解析；容器路径与主机路径不同。

```bash
# ✗ 错：命令里 cd 容器绝对路径——在主机执行时该路径不存在
… -- bash -lc 'cd /<容器内绝对路径>/sub && git pull --rebase'
# ✓ 对：--cwd 相对项目根，命令只管业务
… --cwd sub -- bash -lc 'git pull --rebase 2>&1 | tail -3'
```

② **每个 job 带 `--title "<一句话>"`**，否则 `job list` 里难辨识；忘了用 `gofer job set <id> --title "…"` 补。

- **同步 / 异步**：`--sync` 等到终态（默认约 30 秒，`--wait-timeout` 放宽，等不到转异步）；长任务不加 `--sync`，配 `--timeout` 后 `job watch`。脚本里取 job id：`… 2>&1 | grep -oE '(job-)?[0-9]{8}-[0-9]{6}-[0-9a-f]{8}' | head -1`（新 id 形如 `job-20261021-212412-6a715d34`；没有 `job-` 的旧 id 照常可用，故此模式两种都认）。
- **agent**（`-a`）：`exec` 跑命令（命令放 `--` 之后）；`codex` / `claude` 等跑 AI agent（`--prompt "…"` 或任务文件 `-f task.md`）。能用哪些看项目的 `allowed_agents` / `gofer agent list`。
- **runner**（`--runner`）：默认 `server`（server 本机）；`<worker-id>` 派到那台 worker。容器里能做的活直接在容器里跑，不必绕 gofer。
- 交给 agent 的实施 job 带 `--acceptance "<验收列表>"` / `--scope 'glob,…'`：gofer 会注入「验收标准」「交付约定」两节；对独占 job，`--scope` 还会把目录锁收窄到声明的路径——只改范围内的东西，范围外发现写进汇报的「## 发现但不碰」，可复用经验写进「## 可复用经验」。
- **给 agent job 带 `--prime-keywords "子系统,语言,模块"`**：注入的规则 / 记忆里，命中的给全文、排最前并标「（相关）」，任务要用的资料不会被预算截掉。派活时写上任务涉及的子系统 / 语言 / 模块名（缺省读 `$GOFER_PRIME_KEYWORDS`，显式 flag 优先）；记忆侧给专属记忆补 `when.keywords` 以被命中，见 [tracker.md](references/tracker.md)「按任务关键词选材」。
- 中断了用 `gofer job resume <id> --prompt "…"` 续跑同一会话，**不要重派整份任务书**。只读审查加 `--read-only`。更多（持续会话、模型、预算、verify、worktree、模板、故障转移）见 [job-advanced.md](references/job-advanced.md)。
- **派长 job 加 `--notify`**（或 `--notify-session <sid>`）：job 一结束就经传话人推一条系统通知给你，不必等自己停下才发现；默认关（每条通知起一次传话人进程）。详见 [job-advanced.md](references/job-advanced.md)。

### 并行实施

- 多个 agent 同时改同一 checkout 的不同目录：各自带 `--scope 'glob,…'`，目录锁会随声明收窄，互不重叠时可以并行；同一处要并行改或需要独立提交，用 job 的 `--worktree`。
- **开 worktree 前先提交 tracker**：worktree 里的 `.gofer/tracker` 是建分支那一刻的副本，之后新建的 issue 它看不到。
- 多个 worktree 各自改 tracker 后，`git merge` 由 tracker 合并驱动按记录自动合并；新克隆跑一次 `gofer repo merge-driver --install`。并行改 `CHANGELOG.md`「未发布」段的，再跑一次 `gofer repo changelog-merge --install`。
- 子 agent 的任务书可以很短：「先跑 `gofer repo prime` 和 `gofer issue brief <id>` 接手，然后实施」+ worktree 路径 + 不许 push + 验证要求 + 汇报要有「发现但不碰」。

### 验收与留痕

```bash
gofer job review <id>                     # 汇报、验收标准、提交、越界文件、发现
gofer job accept <id> | reject <id> --note "…" [--resume]   # 开了 --review 的 job
gofer job findings <id> --create-issues   # 「发现但不碰」逐条建成 issue
gofer memory candidates | accept <id> --key k | reject <id>  # 经验候选
gofer job comment <id> "验收：…；我补了 <提交>；后续 …"
gofer issue comment <id> "…"  /  gofer issue close <id> --reason "版本 + 提交 + 验证"
```

- **汇报不当验收依据**：合并前自己看 diff、跑测试；必要时要求 agent 贴出指定命令的原始输出。
- job 评论写结论、自己做的修改、发现的问题、后续 job id；简单的 exec / 检测类 job 不必评。**不要写 `@名字`**——人的评论里 `@agent` 会真的派出 job。

### 记忆：写现状，不写进度

- 长期约定：`gofer memory set <key> "…" --kind rule --summary "一句话"`（正文超 200 字必须带 `--summary`）；一般知识用 `note`（默认）；无 plan 的零散交接用 `--kind handoff`（默认 14 天过期），有 plan 的写 `plan handoff`。
- 跨仓库 / 只给某类 agent：`--global` 或 `--project <p>`；`--tag agent:claude` 只注入给 claude；`--when-paths` / `--when-keywords` / `--when-commands` 只在相关时注入。工作区根目录共用一个 tracker、子项目各自是 git 仓时，**在子仓里新写的记忆会自动带上 `when.paths = <子仓>/**`**（整仓通用显式写 `--when-paths '**'`；工作区通用写成项目记忆 `--project`）；存量记忆用 `gofer memory scope`（默认只读）建议 / `--apply` 补标。
- 注入的记忆与实际不符（过时）：先确认——确认过时就直接改正，不必等人：`gofer memory set <key> "新正文"`（改正文即清除标记）或 `gofer memory archive <key>`；确认不了就 `gofer memory flag <key> --reason "…"`，不要静默绕过。定期 `gofer memory doctor`。
- 看 tracker 改了什么用 `gofer repo status --changed`，**不要** diff `.gofer/tracker/*.jsonl`；jsonl 变化随功能点一起提交。详见 [tracker.md](references/tracker.md)。

### 收尾

- 验证命令、提交、push 与发版以项目 rule 记忆为准（brief 的「验证命令」给出起点）。
- 偶发失败先单独重跑确认；连续出现或单跑也挂的不要当偶发，查根因。

### 对外 / 不可逆操作被拦时：--hold

`git push`、发布、对外发消息这类操作被自己的权限拦下时，交成**待批 job**，请人在 web（手机也行）批准：

```bash
gofer job run -p <p> -a exec --hold --hold-reason "推送 feat/x 到 origin" --title "push feat/x" -- git push origin feat/x
```

把输出里 `awaiting approval:` 那行链接发给用户。**agent 绝不自己批准**（不调 `job approve`、不调 HTTP approve），只等结果；拒绝或超时 = 命令从未执行。见 [hold-approval.md](references/hold-approval.md)。

被权限拒了（403）先自查：`gofer auth whoami` 看本 token 持有哪些权限、每项从哪来（root 根管理员 / config 配置推出 / db 数据库授权），`gofer auth routes` 看某条路由要什么；缺的权限由根管理员发（授权存在 server 数据库里，见 [server-config.md](references/server-config.md) 末尾的权限段）。

## 3. 会话交给 web（session relay）

```bash
gofer init hooks [--agent claude|codex|omp|all] [--global]   # 一次性安装 hook
gofer session relay on|auto|off      # on = 每次停下都在 web 等回复；auto（缺省）= 键盘空闲或久无人工输入时自动等
gofer session ls                     # 哪些会话在等回复
gofer session say <id> "<回复>"      # CLI 代答；"/off" = 关中继并放行
```

- **用户说「我要离开了 / 打开中继 / 交给 web」→ 执行 `gofer session relay on`，然后正常结束回合。** 之后每次回合结束都在 web 等回复，直到 web 回 `/off`、终端有人输入或 `relay off`。
- 在 gofer job 里（有 `GOFER_JOB_ID`）不会触发中继。转达来的消息：`[来自 web…]`（含 `[来自 web 回复，…]`）是**用户本人**写的，`[gofer · <类型>]` 是 gofer 的系统消息（job 完成 / 唤醒 / 工作项请求 / 记忆 / 提示），不要当成用户回话或授权；需要拍板的事在中继里问。
- 送话给空闲会话、唤醒已结束的会话、`session watch` 盯 job、催办等见 [sessions-relay.md](references/sessions-relay.md)。
- 随手记一个想法 / 问题 / 需求先丢进收集箱：`gofer work capture "<内容>"`，之后再整理分派（见 [work-items.md](references/work-items.md)）；`gofer session topic "<主题>"` 记下当前会话在做什么、`gofer session find` 找谁在做某件事（见 sessions-relay.md）。

## 4. job 速查表

| 命令 | 用途 |
|---|---|
| `gofer job run`（`add`） | 提交 |
| `gofer job logs / show / watch <id>` | 输出 / 状态 / 跟随到结束 |
| `gofer job list`（`ls`）`[-p] [--status] [--tag] [--plan]` | 列 job |
| `gofer job cancel <id>` / `job set <id> --title` | 取消 / 改标题 |
| `gofer job resume <id> --prompt "…"` / `job rerun <id>` | 续跑同一会话 / 原请求新会话重跑 |
| `gofer job review / accept / reject <id>` | 验收 |
| `gofer job run --hold …` / `job approve\|reject <id>` | 待批 job（approve 只给人用） |
| `gofer job say <id> "…"` / `job end <id>` | ACP 持续会话（`--session`） |
| `gofer job comment <id> "…"` / `job findings <id>` | 留痕 / 发现但不碰 |
| `gofer job worktree ls / merge / rm` | `--worktree` job 的 worktree |
| `gofer job wakeup create "$GOFER_JOB_ID" …` | 登记唤醒后结束，条件到达自动续投 |
| `gofer tool cp <src> <runner>:<project>/<path>` | 传文件（不要 base64 进日志） |

## 5. 常见坑

1. **在 gofer 配置目录（含 `config.yaml`）里执行 gofer 会连本地 127.0.0.1**：先 cd 回工作区再提交。
2. **命令里写死容器绝对路径**：在主机执行时目录不存在，用 `--cwd`。
3. **`--sync` 默认只等约 30 秒**：长任务加 `--wait-timeout` 或改异步 + `job watch`；`--sync` 不带输出，用 `job logs`。
4. **看到 `recovering` 就重派**：那是 worker 断线后在等重连，不是失败；等它回到 running 或 failed。
5. **主机是 Windows**：命令用 `cmd /c "…"` 包（PowerShell 会吞 git 输出）；派给主机 agent 的任务书要禁止用 PowerShell 双引号字符串写文件（反引号会被吃掉），见 [job-advanced.md](references/job-advanced.md)「派活给主机 agent 的注意事项」。

## 6. references 索引

| 文件 | 何时读 |
|---|---|
| [commands.md](references/commands.md) | 查某组命令的常用写法（job 之外的全部命令索引） |
| [job-advanced.md](references/job-advanced.md) | 续跑、持续会话、交互 pty、只读、模型、预算、verify、验收、worktree / 目录锁、故障转移、任务书模板、日志 |
| [plans-workflows.md](references/plans-workflows.md) | plan / todo 链、plan import 与方案规则、决策点问人、workflow（含 verify / release 起步与内置步骤）与多 agent 择优 |
| [sessions-relay.md](references/sessions-relay.md) | 会话交给 web 的完整用法：hooks、自动布防、送话、接管 / 唤醒、转达、watch、催办 |
| [tracker.md](references/tracker.md) | issue / memory / brief / prime 的细节、记忆体检、子项目适用路径、经验候选、合并驱动、从 bd 迁移 |
| [hold-approval.md](references/hold-approval.md) | 待批 job 的提交、批准、结果与限制 |
| [work-items.md](references/work-items.md) | 被要求 `work report` 时；工作项、整理、管家、随手记（收集箱）与分派 |
| [web-console.md](references/web-console.md) | 要告诉用户去 web 哪一页做什么 |
| [files-and-wakeup.md](references/files-and-wakeup.md) | 传文件（`tool cp` / `--upload` / `--collect`）、登记唤醒 |
| [troubleshooting.md](references/troubleshooting.md) | gofer 报错、job 卡住、project 不在 worker、找日志 |
| [operations.md](references/operations.md) | 管理 worker（登记 / 重载 / 升级）、受管 server 服务、HTTPS、job 环境清洗 |
| [client-config.md](references/client-config.md) | 配置纯客户端节点（容器里最常见） |
| [server-config.md](references/server-config.md) | 写 server 的 `config.yaml`：projects / runners / agents / 常用项 |
| [worker-config.md](references/worker-config.md) | 写 `worker.yaml`：LEGACY vs POLICY、roots、容器 worker |
| [setup-recipes.md](references/setup-recipes.md) | 加 project、接 worker、迁 POLICY、加 agent 的分步配方 |
