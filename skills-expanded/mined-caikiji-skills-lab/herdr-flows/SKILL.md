---
name: herdr-flows
description: 在 Herdr 中做多智能体与长任务工作流前必须读取并遵守本 skill。覆盖：agent start 调用 subagent（默认 claude）、pane 新建与 split、把长命令放 Herdr 面板当后台任务、长驻服务与交互式程序。用户提到"派几个 agent 并行"、"开个服务跑着别停"、"每个分支一个 agent"、"看进度/状态"，或任务含长阻塞命令、需持续输入的交互式程序时，即使没点名 Herdr 也用。仅限 HERDR_ENV=1，依赖 herdr skill。
---

# Herdr Flows

命令语法见 herdr skill；本文件只约定选择与边界。要求 HERDR_ENV=1。

## 布局

- 主 pane 固定左半，用户主要关注主 pane，一切新增从右半开始；禁止把主 pane 拆窄，禁止重复同向向右拆（<100 列不可读）。
- 新建后立即 rename 语义名；串行任务共用一个 pane 排队；堆积过多拆到独立 tab，关注留前台、次要放背后，拆后刷新引用。
- 操作前后跑 `herdr api snapshot` 对照自建登记（一次拿全 workspace/tab/pane/agent/宽度，不必逐个 list）；收尾必须回到「只有主 pane 和用户既有 pane」，有残留必清。
- 关闭前核对 label 与登记一致；用户面板只读；误关如实报告并给恢复命令。

## 调用子 agent

- 启动必须带 `--agent herdr-child`（身份/安全红线/协议全文由 [agents/herdr-child.md](../herdr-chat/agents/herdr-child.md) 提供），禁止裸启动。
- 必须显式传 `--permission-mode auto`：subagent frontmatter 里的 permissionMode 不生效，省略会回到逐条审批（每条命令弹窗）。
- 启动失败依次排查：integration status → install claude → pane 注入降级（[references/agent-lifecycle.md](references/agent-lifecycle.md)）。
- 派活简报只含任务 + 动态值（主控 pane id、agent 名），模板见 [references/chat-briefing.md](references/chat-briefing.md)；结论要求写报告文件；验收用轮询（[references/polling.md](references/polling.md)）——先看反向消息再 cat 报告文件，不使用 `--wait`。
- 收尾顺序：确认子 agent 回 idle/done 不阻塞 → agent list 无残留 → 主控注入退出 → 关面板。
- 子 agent 无法退出自己：完成时发消息告知「可以关闭我」，退出/关面板都是主控职责。

## 双向通信

- 子 agent 可给主 pane 注入 `[名字] 消息`；简报必须告知它主控 pane id。
- 协议全文见 [herdr-chat](../herdr-chat/SKILL.md)；打回/卡死/接力/并发写入见 [references/agent-lifecycle.md](references/agent-lifecycle.md)。

## 边界

- 轮询匹配不加行首锚（输出带前导空格/前缀）；哨兵字面量不得出现在简报（回显会假阳性）。
- 匹配到完成标志 ≠ 完成，必须文件二次验证。
- auto 模式仍拦截高危命令，出现审批是预期安全行为，读屏后按 blocked 处理，不绕过。
- 组合命令（如 `mkdir && node`）不受单命令白名单覆盖，会弹审批。
- 审批框的 enter 可能被吞，确认后必须重读屏。
- 参数以 `/` 开头会被改写成 Windows 路径，注入命令加 `MSYS_NO_PATHCONV=1` 前缀。

## 长命令进面板

- 耗时/需持续输入的命令放其它 pane，主 pane 不干等。
- 服务启动判定用行为探针（curl 探端口/接口），横幅只作兜底。
- 停止服务后探针反向验证（连接失败 = 端口已释放）再关面板，最后 list 确认无残留。

长驻服务 / 状态看板 / REPL 驱动速查见 [references/scenarios.md](references/scenarios.md)。

## 等待纪律

1. 每个等待周期结束先检查现场（read / agent get / 看结果文件），确认状态后才决定下一轮等待或处理；禁止醒后无检查直接再睡。
2. 短轮询 6-8 轮（约 25s）无进展即停，改用现场检查定位，不无限续等。
3. `--timeout` 设 15~60s（默认 30s），超时先看现场再决定续等或上报；禁止长时黑盒等待。
4. 轮询节奏先短后长（1s → 5s → 30s），每轮真实检查。
5. working 超长（>60s 无进展）先读屏；子 agent 生成期不注入（可能被吞），多轮意图合并成一条简报。
6. 写操作前核对 pane_id 在自建登记清单。

## 常见坑

- JSON 错误在 stderr 且 exit 1，exit 2 是语法错；pane move 后旧 ID 失效。
- 本 skill 未覆盖的问题走 skill-feedback 流程沉淀，不在本文件内私自扩写。
