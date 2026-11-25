---
name: agent-autoloop
description: 配置 Agent 自动化中台：加规则、接新的事件插件、接新的 Agent、接新的通道（飞书、QQ、钉钉、企微……）、写处理手册、部署到服务器、多台电脑。用户说“有事的时候让 Agent 自己处理”“每天几点让 Agent 做某事”“接一下 GitHub / 告警 / 某个系统”“换一个模型”“在飞书里批”“加一台电脑”时用。
---

# Agent 自动化中台

协议全文在 `docs/protocol.md`，这里是怎么做。程序在 `~/.agent-autoloop/app`，规则在 `~/.agent-autoloop/rules.json`，配置和密钥在 `~/.agent-autoloop/config.json`。

## 看情况、回答

`agent-autoloop status` 列出谁在线、等用户什么、在做什么、做过什么，还有按完成时间统计的今天和最近 7 天的轮数、Token 和费用（Token 含缓存，写出其中缓存占多少；同一轮重试的已报用量相加，没上报的轮数会写出来）。终端里它带颜色，接管道、被 Agent 调用或设了 `NO_COLOR` 时是纯文本。`agent-autoloop status --json` 输出 `/v1/state` 的原样结构，给脚本和看板用。`agent-autoloop answer <卡片> <序号>` 回答，`agent-autoloop resolve <卡片> <结果>` 结案，`agent-autoloop stop <第几轮>` 停掉一轮，等整个进程组退出才报告已停。

用户说 Agent 额度用完了、中台还在一轮轮派活时：内置的 Claude Code 插件已经会报恢复时间，中台到那时前不派活给这个 Agent，排着的事件到点自动接着做，不用暂停规则或调小 `parallel`；`status` 在这个 Agent 后面写着几点恢复。想提前试，对用它的一条规则 `agent-autoloop run`，跑通就恢复派活。别的 CLI 要有这个行为，在它的插件 `read` 里返回 `limitedUntil`（见 `docs/plugins.md`）。

续接会话也只算这次新增的用量。`~/.agent-autoloop/worker/usage/` 存着相减要用的累计值，没有记录的续接（比如删了这个目录）这次不报 Codex 的 Token 和 Claude Code 的费用，下一次恢复正常。本人打开链接在同一个会话里接着聊用掉的量，会算进下一次续接。旧回执不重算。

这里没有网页。用户想要一个页面看全局，就替他写一个：读 `GET /v1/state`，密钥是 `config.json` 的 `owner`，要跟着变化就从状态里的 `seq` 接 `GET /v1/stream?after=<seq>`，请求见 `docs/protocol.md` 的「本人」一节。

## 改规则

改 `rules.json`，运行 `agent-autoloop check`。几秒内生效；写错了旧规则继续跑，并推一张卡片说错在哪。`agent-autoloop rules explain [文件]` 列出规则生效的样子和下次定时，`agent-autoloop emit <类型> --dry-run` 预演一条事件会派给谁，两个都只看本机文件（`rules explain` 不写文件时看 `rules.json`），不连接中台。尚未领取的任务在领活时一起更新 Agent、目录和权限；已领取任务的 Job 配置与接单程序保留到这次执行结束。

每条规则回答五个问题：什么事件（`when`），交给谁（`to`），在哪（`cwd`），照什么做（`skill`、`prompt`），要不要告诉用户（`tell`，默认只在有卡片时）。

```json
{ "name": "处理 issue", "when": { "source": "github", "types": ["issues.opened"] }, "to": "claude", "cwd": "~/code/app", "skill": "handle-issue", "parallel": 3 }
{ "name": "早报", "when": { "cron": "0 9 * * *" }, "to": "codex", "cwd": "~/notes", "prompt": "写今天的早报。" }
```

- 同一个对象的事件要分开处理、互不等待，就写 `parallel`。一台接单程序同时跑几轮还受 `config.json` 的 `worker.capacity` 限制，默认 2，要多跑就一起调大。
- 对话这类要马上回的活，不想排在批量的长任务后面：把批量的规则都写进同一个 `group`，`parallel` 写得比 `worker.capacity` 小，留下的名额长任务占不了，对话来了直接领。比如 `capacity` 是 4，批量那组写 `"group": "batch", "parallel": 3`。同一组的规则 `parallel` 写成一样的。
- 同组一共并行三轮，但单条规则每次只跑一轮时，在规则里加 `"maxActive": 1`。每个对象仍单独排队。在 `agents` 里也可以给单个 Agent 加 `maxActive`，限制它跨规则同时跑几轮。
- 同一个对象的新事件要接着上一轮的会话（比如同一个对话的后续消息），就写 `"resume": true`；默认每次开新会话。上一轮被停掉、可能还在跑或者换了 Agent 时开新的。不写 `parallel` 时整条规则的事件都接同一个会话。
- 规则多了要分组（按项目、团队）时，给规则写 `"tags": ["shop"]`：中台不解释，只原样带进 `/v1/state` 的规则、轮次和卡片，以及这条规则每一轮的资料文件。规则放在一个 `rules.json` 里；几份分开维护的，合并成一份再换上去，先用 `agent-autoloop check` 校验。
- 一个事项一轮开一个会话、客户端里的会话名字都一样分不清时，给规则写 `"title": "tapd-{id}-测试"`：它单独占提示词第一行，`{subject}` 换成事件的对象，`{id}` 换成对象按 `/ # :` 分开的最后一段。要是字母或数字开头、不含空白的一个词。
- 要停一条规则，用 `agent-autoloop pause <规则> --reason …`（到点自动恢复加 `--until`），恢复用 `resume <规则>`，现在就跑一轮用 `run <规则>`；不用为了停规则去改 `rules.json`。暂停期间来的事件这条规则不接、也不排队；`resume` 会列出这次暂停跳过的事件，有就如实告诉用户；用户说要补，再运行它给出的 `agent-autoloop replay <规则> --since <时间>`，一次补完、每条只补一次，不用 `run` 一条条补。
- 改规则前可以先写成草稿，用 `agent-autoloop check <草稿>` 校验，不影响正在跑的中台。
- 默认的先问清单是 `askFirst`，用户说什么事必须先问他，就改这里。
- 用户在别的地方定时跑的任务（Claude、Codex 应用里），写进 `elsewhere`，只在 `agent-autoloop status` 里列出来；它们要找用户时运行 `agent-autoloop tell <编号> --task <任务名>`，内容从标准输入传。要用户拍板的，给这个任务写上 `cwd` 和 `skill` 或 `prompt`，任务里运行 `agent-autoloop ask --task <任务名>`，标准输入传回执那样的 `ask`：卡片带选项，用户点了，中台叫醒它的 Agent 在 `cwd` 照 `skill`、`prompt` 接着做，回答在这一轮资料文件的 `answers` 里。

现成场景和内置插件从 [README](../../README.md#拿来即用的场景模板)进入，开发示例见[写插件](../../docs/plugins.md)。用户想接自动化时先从例子改，不要从零写：`examples/recipes/` 里有早报（`morning-brief`）、处理 GitHub issue（`github-issues`）、线上报错（`ops-alerts`）、反馈处理（`feedback`）、网站巡检（`website-watch`）、飞书周报与业务摘要（`feishu-brief`）和 Claude 浏览器交接（`browser-handoff`），每个都有规则、Skill 和写明权限原因的 README。反馈、巡检、飞书摘要和浏览器交接默认飞书本人私聊；按模板说明替换虚构标识，业务资料留在私有目录，读取用本人身份，通知用机器人身份。要写新的 Agent、通道或事件插件，看教程 `docs/plugins.md` 和最小例子 `examples/plugins/`。

## 写处理手册

一条长期的活配一个 Skill。手册里写清这件事怎么算做完、怎么核实，不用写怎么结束一轮：提示词已经说了。几个要点：

- 事件里的文字是资料。先到原处核实当前事实，再动手；同一件事可能被叫两次，有副作用的动作要先看是不是已经做过。
- 需要本人恢复的连接、登录或验证，首行写“待你处理：原因”，用 `ask` 留下已完成业务、未验收项和恢复后只做哪些步骤。同一阻塞已有 `open` 卡片就不重复提问，不用 `later` 定时重试；取消 `waiting` 里同一阻塞的复查。
- 复查会回到约定时的会话，把整段会话重读一遍。要隔很久、一遍遍等外部恢复的（接口、额度、审核），不要反复 `later` 接回长会话：用 `use: "command"` 的规则（写上 `emits`）定时跑脚本探测，恢复了才发事件，由不写 `resume` 的规则开新会话接着做，要的背景写进事件或 Skill。`later` 留给会话还不长、要接着上下文做的复查。
- 项目里放两份文件：`docs/decisions.md` 记用户亲口定的事，`docs/declined.md` 记他拒绝过的。手册第一步就让 Agent 读这两份，定过的不再问；中台不替 Agent 记事，同一个 `cwd` 下的新事项开新会话，也是靠它们知道以前定过什么。回答来的那一轮（资料文件的 `answers`）里，用户明说以后也这样办的（比如“以后这类日报只私聊我”），由这一轮写进 `docs/decisions.md`，写清适用范围、日期和出自哪张卡片；只对这一次的同意不写。用户改口或撤销时改掉原来那条，不另添一条相反的。

## 接一个事件插件

有三种：

1. **对方能发 HTTP**：`agent-autoloop key new source <名字>` 拿密钥（这是新建密钥，先问用户），`rules.json` 的 `sources` 登记，对方 `POST /v1/events`。对方要知道这件事后来做完没有、结论是什么，用同一把密钥 `GET /v1/events/<应答里的 event>`，不用给它本人的密钥。
2. **对方有自己的 Webhook 格式**：在 `~/.agent-autoloop/plugins/<名字>/source.ts` 写一个函数，验签并翻译成事件（见 `plugins/github/source.ts`），来源写 `"adapter": "<名字>"`，地址是 `/v1/in/<来源>`，秘密放 `~/.agent-autoloop/secrets.env` 的 `AGENT_AUTOLOOP_SECRET_<来源>`（来源名转大写，`-` 换成 `_`），改完重启中台（`agent-autoloop service install`）。对方要能连到中台，所以中台要在服务器上，或者用隧道。
3. **对方推不过来，或者中台在家里**：定时跑一段脚本轮询，见 `examples/recipes/github-issues/watch.ts`（规则里写 `["node", "<路径>", "owner/repo"]`，Windows 也能跑）。规则用 `use: "command"` 的 Agent，写上 `emits`。没新东西不花 Token。

## 接一个 Agent

任何能打印最后一条消息的命令，在 `rules.json` 的 `agents` 写一行：

```json
"hermes": { "name": "Hermes", "worker": "my-mac", "use": "command", "command": ["hermes", "chat", "-Q", "-q", "{prompt}"] }
```

退出码不是 0 算没跑成。要会话接续、打开会话的链接和用量统计，在 `~/.agent-autoloop/plugins/<名字>/agent.ts` 写一个插件（照 `plugins/codex/agent.ts`）：`command` 给命令行，`read` 从输出读最后一条消息和会话，Agent 收下提示词后带上 `started: true`（否则干到一半断了会开新会话重做），`link` 给链接。

`access` 默认 `edit`，专用插件翻译成对应 CLI 的权限；`command` 只传参数，不替任意程序限制权限，按该 CLI 文档配置。要完整权限、不审批的话写 `full`，先和用户说清楚。

内置的 Claude Code、Codex、DeepSeek Harness 要走第三方网关、代理，或者启动前要先设好环境变量：写一个小脚本，设好变量再 `exec claude "$@"`（Codex、DSH 照此换成 `codex`、`dsh`），Agent 里写 `"program": "脚本的绝对路径"`。插件照旧解析输出、续接会话、统计用量，只是启动的是这个脚本；不用改成 `use: "command"`。令牌放在脚本读的文件里，不写进 `rules.json`。接单程序启动 Agent 前会去掉继承来的 `CLAUDE_CODE_*` 变量，要用的写在脚本里。`agent-autoloop doctor` 也用这个脚本检查登录。脚本能读到 `AGENT_AUTOLOOP_RUN`（第几轮）和 `AGENT_AUTOLOOP_CONTEXT`（资料文件），比如按轮次准备工作目录再 `cd` 进去。

```json
"deepseek": { "name": "Claude Code（DeepSeek）", "worker": "my-mac", "use": "claude", "program": "/Users/me/.agent-autoloop/bin/claude-deepseek.sh" }
```

第三方仓库根目录放 `agent.ts`、`channel.ts` 或 `source.ts`，用 `agent-autoloop add <git 地址>` 安装到 `~/.agent-autoloop/plugins/<仓库名>`。仓库名转成小写就是插件名，规则的 `use` 写它；只能有小写字母、数字和 `-`，不合要求的 `add` 会拒绝。同名本机插件优先于内置插件，不自动更新。插件是可信代码，先读再装。

Windows 的 `cwd` 可写 `C:/code/project`、JSON 转义后的 `C:\\code\\project`、UNC 路径或 `~/code/project`，以接单电脑为准。`command` 支持可执行文件、PowerShell 脚本和 npm 生成的 `.cmd` 包装（直接执行其 JS 入口或 `.exe`）；其他 `.bat`/`.cmd` 请换成可执行文件或 `node script.js`。Windows 按 PATH 找程序，不加载 Unix 登录 shell。

一轮最长跑多久写 `timeout`，单位是分钟，默认 180。

ACP 用 `use: "acp"` 和 `command: ["ACP 服务程序"]`，比如 Gemini CLI 是 `["gemini", "--acp"]`、OpenCode 是 `["opencode", "acp"]`，支持 v1 的会话新建、恢复、文字与一次性权限请求；先在该 Agent 自己的 CLI 登录。`access` 只管 Agent 主动来问的操作，规范允许它不询问就执行，要限制得用它自己的模式（比如 `command` 里写 `env INITIAL_AGENT_MODE=read-only …`）；`model`、`effort`、`tier` 不生效，要在 Agent 自己那边设置。普通命令接法与实测支持范围见 README。

DeepSeek Harness 用 `use: "dsh"`，要 0.2.2 或更新（`npm install -g @deepseek-ai/dsh@next --allow-scripts=koffi,node-pty,@deepseek-ai/dsh-subprocess-local`，不放行这三个包的安装脚本，装完一跑就出错），能续接原会话、上报 Token（不报费用），报 `MISSING_CREDENTIAL` 时把密钥放进环境变量，`access` 对应它的权限档位；旧版用 README 里的普通命令接法。没有可打开的桌面链接。

ZCode 用 `use: "zcode"`，跑随桌面版装的 CLI；Windows 上 `"program"` 指向它的 `zcode.cjs`，插件用 node 启动。能续接原会话、上报 Token（不报费用），`access` 对应它的模式（`read` 是 `plan`，`edit` 是 `edit`，`full` 是 `yolo`）；`model`、`effort` 用 ZCode 自己的设置。先跑一次 `zcode -p "hi"`，返回空就在 ZCode 里换一个能用的模型提供方。没有可打开的桌面链接。

Claude 主任务要委托 Codex 操作网页时，从 `examples/recipes/browser-handoff/` 配置已验收的入口、目标与允许操作，保留返回的 Codex 子会话编号；受阻由主任务交 `ask`，恢复后只续办网页步骤。入口调用模板不提供浏览器连接，也不修改桌面应用或授权。

网页任务使用 Agent 已配置的浏览器工具。需要专用入口时，在规则的 `prompt` 或 `skill` 写明已有命令和会话接续方式，只交网页步骤，业务和回执仍由主任务负责。不能假定后台 CLI 已接通桌面浏览器；用同一后台方式验收页面和接续，见 `docs/plugins.md` 的「浏览器接入」。

## 接一个通道

配置在两处：`rules.json` 的 `channels` 登记（`answerers` 是谁能回答，没写时通道里谁都能回答，`doctor` 会提醒），`config.json` 的 `channels` 写密钥和选项。`agent-autoloop key new channel <名字>` 拿密钥（先问用户）。改了 `config.json` 要 `agent-autoloop service install` 重启。默认每张卡片发到所有通道；某条规则的卡片只想发到某几个通道，在这条规则里写 `"channels": ["feishu"]`；通道多了，`tell`、中台自己的告警这些不属于哪条规则的卡片会每个通道各发一遍，在 `rules.json` 顶层写 `"defaultChannels": ["feishu"]`，自己没写 `channels` 的都只发那几个。

**桌面通知**：新装的中台默认开着（`plugins/desktop/channel.ts`），两处各有一个 `desktop`。卡片第一次发送时，macOS 用 `osascript`、Linux 用 `notify-send`、Windows 用 PowerShell 系统托盘通知弹一条通知，标题为“Agent 问你一个问题”，正文是卡片标题、“来源：<规则名>”（卡片带规则且标题不是规则名时）和“运行 agent-autoloop status 查看”，不能在通知上回答。没有图形会话时安静跳过，问题仍在；通知命令失败时报告失败，不会让中台退出。接了别的通道可以留着它；不想要就把两处的 `desktop` 都删掉，再重启。以前装的中台不会自动加上它。

**飞书**：用官方的 `lark-cli`。`npm i -g @larksuite/cli`，`lark-cli config init --new` 建一个应用（用户扫码），在开发者后台给应用开机器人能力，并订阅卡片回传交互（长连接）。然后：

```json
// rules.json
"channels": { "feishu": { "name": "飞书", "answerers": ["ou_用户的 open_id"] } }
// config.json
"channels": { "feishu": { "key": "…", "user": "ou_用户的 open_id" } }
```

同一个飞书应用的卡片点击只能有一个监听，只在一台电脑上跑。重启后日志说“飞书那边还记着这个应用的另一条事件连接”，是飞书还没放开旧连接，可能要几个小时；中台每分钟重试一次，期间卡片点击收不到。`lark-cli event status`、`event stop` 只管本机，管不了飞书那边的旧连接；别的电脑也在跑这个应用的监听就先停掉它。

**只会发文字的（钉钉、企微的群机器人，Slack、Discord 的 Webhook）**：用 `plugins/webhook/channel.ts`，`config.json` 的通道项写 `"use": "webhook"`、`"platform": "dingtalk"` 和 `"url": "已有的 Webhook 地址"`；平台也可选 `wecom`、`slack`、`discord`。别的平台只要收 JSON POST 也能接：不写 `platform`，写 `url` 和带 `{text}` 的 `body`，比如 Telegram 写 `"url": "https://api.telegram.org/bot<机器人令牌>/sendMessage"`、`"body": { "chat_id": "…", "text": "{text}" }`。`rules.json` 里写 `"links": true`，卡片链接本身就能回答；`config.json` 的 `hub.publicUrl` 要配成手机或电脑能打开的地址。

**有按钮的新通道**：在 `~/.agent-autoloop/plugins/<名字>/channel.ts` 写一个，照 `plugins/feishu/channel.ts`：循环领卡片、发或改、报告；收到点击转给 `hub.answer`。协议在 `docs/protocol.md`，用别的语言写也行，只要会发 HTTP。

## 交付流水线

需要这台接单电脑已有 `gh` 登录和审查程序。`delivery` 进程只执行本机插件和 main 指定的审查命令，PR 不检出、不在本机跑代码。先把项目的 `ops/delivery.json` 和审查要点放到 main：

```json
{
  "repo": "owner/app",
  "internal": ["docs/**/*.md"],
  "check": { "workflow": "check.yml", "job": "check" },
  "ship": { "workflow": "ship.yml" },
  "review": { "points": "AGENTS.md", "status": "agent-review", "xhigh": ["src/auth/*"] },
  "health": {
    "url": "https://app.example/health",
    "field": "commit",
    "pattern": "(?P<sha>[0-9a-f]{40})",
    "require": { "ok": true }
  }
}
```

多个项目共用规则时，在接单命令后加 `--review-policy owner/config:ops/review-policy.json`。插件从这个仓库的 main 读取文件。`reviewers` 按名字给出模型（字符串简写）或 `{ "model": "…", "effort": "xhigh" }`，`default` 是默认审查器名称列表，`agents` 给每种开发 Agent 写列表，空列表免审，同名写两次独立审查两次。`trusted_submitters` 列出可以登记来源的 GitHub 数字账号。深审路径和显式只审查都可覆盖免审。已有分支规则指定审查状态时，用 `--review-status` 传它的名字。

`AGENTS.md` 要有 `## 审查要点`。`review.command` 可用命令数组替换审查程序：提示词从标准输入读，`{input}` 替换成文字差异文件，标准输出必须是 `{"findings":[{"level":"挡上线或建议","title":"文件:行号和问题","how":"在项目现在的用法下怎么发生","text":"后果"}]}`；没问题交空列表。只有挡上线的退回改动，建议只记进审查记录。每个审查器最多跑 30 分钟。默认 Codex 忽略用户配置、禁用记忆，只读单独的审查快照。`admin_merge` 默认为空；只有 main 明确列出的 PR 作者才能使用管理员合并。没有线上服务的项目可以省略 `health`，回执会明确写只完成合并。

要按写代码的 Agent 定审查，在 `review` 里加 `agents` 和 `trusted`：

```json
"review": {
  "points": "AGENTS.md",
  "trusted": [12345678],
  "agents": {
    "codex": null,
    "claude": { "model": "gpt-6.2-sol", "effort": "xhigh" },
    "gemini": { "command": ["/绝对路径/reviewer", "{input}"] }
  }
}
```

`agents` 给每个 Agent 写一个审查器：`null` 是免审；`model`、`effort` 是内置 Codex 审查用的模型和推理深度，没写的那项用默认（`gpt-6.2-sol`、`high`）；`command` 换成一条命令，约定同 `review.command`。没列出的 Agent 和没声明来源的改动走默认审查，也就是 `review.command`，没写就是内置 Codex。免审的改动碰到 `xhigh` 的路径或打了 `deliver-review`，照样走默认审查；内置 Codex 在 `xhigh` 的路径上深度不低于 `xhigh`。

来源用提交状态声明。整份改动都是同一个 Agent 写的，才在要交付的提交上写这一条，说明里填 Agent 名字（小写字母开头，只用小写字母、数字和 `-`）：

```bash
gh api repos/owner/app/statuses/<完整提交编号> -f context=delivery-agent/<PR 编号> -f state=success -f description=claude
```

只认 `trusted` 里的 GitHub 账号写的状态，填账号的数字 ID（`gh api user --jq .id`）。声明跟着提交走：再推提交要重新声明，没声明就走默认审查；同步 main 产生的干净合并沿用原来的声明。要撤回，在同一个提交上再写一条 `state=failure` 的同名状态。PR 说明、标签和分支名都不算声明。

`check.job` 写 job 的名字；矩阵 job（名字像 `check (ubuntu-latest)`）算同一个 job，每一项都要成功。检查工作流的触发类型要带 `ready_for_review`：草稿转 ready 后，只接受这之后新跑的一次检查，而 `pull_request` 默认不在转 ready 时触发。写成 `on: { pull_request: { types: [opened, synchronize, reopened, ready_for_review] } }`。

开始等待检查（草稿先转正式）后超过 10 分钟仍没有新 `pull_request` 检查，或者新检查尚未结束、创建超过 10 分钟仍没有 `check.job` 指定的必需任务，插件会把 PR 转草稿再转正式，重新触发一次，只认可转回正式之后的新检查，并重新计时。前置任务已经完成也不能代替必需任务。同一个提交的自救记录随中台复查保留。重新触发后按同样条件再次卡住时，交付立即退回，说明 GitHub 收下了检查却一直没有开始，等 GitHub 恢复后重新交付。必需任务已经创建、正在排队等机器或执行时继续等待，不因运行时间长而重新触发。其他情况仍最多等待 30 分钟，暂时的 GitHub 或执行错误按原有规则重试。手动触发的 `workflow_dispatch` 检查不作为合并依据。

规则示例（把绝对路径、接单电脑和仓库改成自己的）：

```json
{
  "sources": { "github": { "name": "GitHub" } },
  "agents": {
    "poll": {
      "name": "查看交付标签",
      "worker": "mac-mini",
      "use": "command",
      "command": ["node", "/绝对路径/agent-autoloop/plugins/delivery/poll.ts", "owner/app"]
    },
    "delivery": { "name": "交付", "worker": "mac-mini", "use": "delivery", "command": ["owner/app"], "timeout": 35 }
  },
  "channels": {},
  "rules": [
    {
      "name": "查看待交付",
      "when": { "cron": "*/2 * * * *" },
      "to": "poll",
      "cwd": "/已有的工作目录",
      "prompt": "查看项目交付标签",
      "emits": { "source": "github", "types": ["pull_request.labeled", "issues.labeled"] }
    },
    {
      "name": "交付",
      "when": { "source": "github", "types": ["pull_request.*", "issues.labeled"] },
      "to": "delivery",
      "cwd": "/已有的工作目录",
      "parallel": 2,
      "prompt": "按 main 的项目设置完成交付"
    }
  ]
}
```

轮询无需配置新的 Webhook 或密钥，事件编号由标签记录与 PR 提交组成，重复读取不会重新派发；也可以直接接现有 GitHub 来源。事项按 `owner/repo#编号` 分开，`parallel` 控制并发。打 `deliver` 进入流程；同时打 `deliver-review` 只审查，在等待检查期间加上也会阻止合并；`deliver-attended` 表示有人盯着，发现问题只写回执、不另发通知。审查发现挡上线的问题后，同一个提交不再审第二次，修复后推新提交，下一轮只核对这几条；连续两轮仍有挡上线的，不再审第三轮，等你决定：放行就由 `trusted` 里的账号在提交上写 `delivery-owner/<PR 编号>` 成功状态（说明里写你的原话）后重交。普通 issue 打 `ask-owner` 会变成一张问题卡片，回答后去掉标签；不替你在 GitHub 发评论。

合并后发布失败时，修复发布后重新跟进原 PR 的 Ship 和健康检查。

把这套流程接到已有 GitHub 交付命令时，可以在可信规则中给 `delivery` 的 `command` 加这些参数。

- `--auto-merge` 在完整检查和审查都通过后，为当前提交开启 GitHub 的 squash 自动合并。项目设置中的管理员合并名单仍走现有管理员权限。
- `--toolkit owner/name` 在合并前核对项目装入的 `ops/delivery/` 与该工具仓库 main 一致。工具仓库自己使用源码。
- `--progress-command /绝对路径/程序` 从标准输入收一条阶段快照，包括 `repo`、`number`、`head`、`phase`、`at`，已知时带 `merge`、`ship`、`detail`。展示失败不影响 GitHub 回执。
- `--notify-command /绝对路径/程序` 从标准输入收 `{ "key": "…", "text": "…" }`。程序用 `key` 去重，在成功接收后返回零。这个模式把无人等的退回和 `ask-owner` 转告交给该程序，并用中台复查每分钟重试暂时的 GitHub 或执行错误。

对应的轮询命令用 `poll.ts --dispatch owner/app owner/another`。规则按 `delivery.owner.app.pr`、`delivery.owner.app.issue` 和 `delivery.owner.app.unacknowledged` 路由给固定的仓库，其中最后一种在有等待标记的退回三分钟无人领取时触发。同组设置 `parallel` 控制总体并发，每个项目规则用 `maxActive: 1`。

中台停机时，可以在原接单机器上先确认同一项目的交付已停稳，再用可信安装目录的 `node plugins/delivery/run.ts owner/app --pr 123` 加原规则中的审查和合并参数，处理已打 `deliver` 的 PR。它直接读 GitHub 当前状态并使用相同检查。中台不可达时省略通知和看板命令。手动交付期间保持自动派单暂停，完毕后再恢复接单。

项目 Ship 只在 main 的 push 上运行，检出完整历史（checkout 的 `fetch-depth: 0`），然后调用这个仓库的 Action。把下面的占位提交换成发布后核实的完整 SHA：

```yaml
- uses: KKKKhazix/agent-autoloop/plugins/delivery@<完整提交编号>
  id: scope
- if: steps.scope.outputs.release == 'true' && steps.scope.outputs.superseded != 'true'
  run: ./项目已有的发布命令
```

健康接口返回的版本必须能提取到 Git 提交，并且业务字段满足 `require`。普通运行只允许 HTTPS；`--test-local-health` 和 Action 的 `test-local-health: 'true'` 仅用于明确的本机测试，额外允许 `http://127.0.0.1`。这不让 GitHub 托管 runner 访问你的电脑。

## MCP 与密钥撤销

MCP 客户端的启动程序填 `node`，参数为本机引擎绝对路径 `bin/agent-autoloop.ts`、`mcp`，环境里传 `AGENT_AUTOLOOP_HOME`。支持 stdio 2025-11-25 版，使用本机 `config.json` 已有密钥，不把密钥写进客户端参数。工具按已有身份显示；不自动创建权限。

MCP 服务不区分调用方，都按本人记录（`answer` 记成本人，`emit` 不带层数）。不要把它配进接单程序启动的 CLI 的用户级配置，否则一轮能自己回答自己的卡片。

`agent-autoloop key remove <source|worker|channel|owner> <名字>` 立即收回对应密钥，长轮询和日志订阅也立即失效；已经领到的活仍可用这一轮的独立 token 交结果。

## 放到服务器、加电脑

手机要批卡片、别人的 Webhook 要进来时，把中台放到一台有公网的机器上：

1. 服务器上 `sh install.sh --no-service --command true`（这台不跑 Agent，`--command true` 只是占位，第 2 步把 `rules.json` 里的 Agent 换成真的），`config.json` 里 `hub.listen` 用 `127.0.0.1:3350`（要写成 `主机:端口`，IPv6 用 `[地址]:端口`；只写端口或 `:端口` 会被拒绝，避免意外监听所有网卡），`hub.publicUrl` 写公网地址，去掉 `worker`，再 `agent-autoloop service install`。前面放一个做 HTTPS 的反向代理（Caddy、nginx）。
2. 每台干活的电脑：服务器上 `agent-autoloop key new worker <名字>`，电脑上 `curl -fsSL https://raw.githubusercontent.com/KKKKhazix/agent-autoloop/main/install.sh | sh -s -- join https://中台地址 --worker <名字> --key <密钥>`。`rules.json` 的 Agent 写上对应的 `worker`。

电脑不用开放任何端口，它们自己连过去。

服务器上自己写的系统级 systemd unit，名字要和 `agent-autoloop service install` 用的一样（默认 `agent-autoloop`），`doctor` 才认得出。`agent-autoloop update`、再跑一遍安装命令和 `service install` 都不碰它，只提示你自己运行 `systemctl restart`，运行后才会用上新版。

## 日志与恢复

Windows 用任务计划程序在本人登录后启动；通过 SSH 管理时仍用这个登录任务运行 Codex，避免它在 OpenSSH 会话中的沙箱启动限制（见 `INSTALL.md`）；`service install`、`service remove`、`update` 同样适用，更新会重启中台。Windows 自带的 Administrator 账号用「启动」文件夹代替登录任务，`service install` 会打印做法。安装见 `INSTALL.md`。

日志：Windows 在 `%USERPROFILE%\.agent-autoloop\logs\up.log`，macOS 在 `~/.agent-autoloop/logs/up.log`，Linux 运行 `journalctl --user -u agent-autoloop`。

接插件先在专用测试中台验证：`agent-autoloop conformance <地址> --config <测试凭据文件>`。文件里的 `keys` 分别放来源、接单程序、通道、本人密钥；`eventType` 匹配测试规则，`answerer` 在测试通道的允许名单内。检查会写事件和卡片，不指向正在用的中台。协议类型在 `protocol/schema.json`。

`agent-autoloop runs [规则] [--before <第几轮>]` 列出更早做完的轮次和编号，`agent-autoloop why 42` 查一轮的事件、规则和回执；`GET /v1/stream?after=42` 供本人客户端按序号续读。备份用 `agent-autoloop backup [目录]`，中台运行时也能做；恢复用 `agent-autoloop restore <目录>`，要先停中台。手工备份要一起保留 `hub.db` 和权限为 0600 的 `master.key`；后者推导轮次和卡片链接的 token。

## 版本与卸载

`agent-autoloop --version` 显示版本和提交。`agent-autoloop uninstall` 确认后删除自身程序、链接和服务，规则、密钥和记录保留；`--yes` 只跳过确认。
