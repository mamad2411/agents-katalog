---
name: myagents-task-alignment
description: >-
  MyAgents 产品内“任务讨论/智能创建”的对齐工作流。只要首轮消息带有
  <TASK_DISCUSSION> 上下文，就使用本 Skill 与用户澄清需求、判断是否需要创建
  Task，并在创建前生成完整 task.md 候选稿与参数说明供用户确认。讨论不必以
  Task 为终点；也可以继续探索、留在当前 Session 执行或明确放弃。不要把普通
  对话中泛泛提到的“任务”误判为此产品工作流。
metadata:
  author: MyAgents
---

# MyAgents Task Alignment

你正在承接 MyAgents 发起的任务讨论。目标不是把每条 Record 都变成 Task，而是先把用户真正想完成的事情聊清楚，再选择最合适的承载方式。

## 先读取产品能力

开始讨论前完整读取 `myagents-task-automation` Skill。它是 Task 支持的执行模式、时间、触发策略、Session 策略、结束条件和 CLI 参数的权威能力说明。本 Skill 只负责需求对齐、`task.md` 质量与创建前确认，不复制那份能力表。

首轮消息的隐藏 `<TASK_DISCUSSION>` 中会给出：

- `candidatesDir`
- `workspaceId`
- `workspacePath`
- 可选的 `sourceRecordId`
- 音频 Record 还会提供 `sourceRecordDocumentPath` 与 `sourceRecordAudioPaths`

`discussionId` 和 `discussionDir` 由应用在准备持久候选目录时内部使用，不进入 Agent 上下文。写候选稿时直接使用 `candidatesDir`，不要自行从路径反推或要求用户提供这两个内部字段。音频讨论以 `sourceRecordDocumentPath` 指向的当前态文稿为准；只有需要核对原始声音时才读取 `sourceRecordAudioPaths`，不要把音频复制进候选目录。

这些值来自应用，不要要求用户重填，也不要自行猜测或改写。若隐藏上下文缺失或路径无效，说明当前讨论无法安全创建 Task；仍可继续普通讨论，但不要调用 Task 创建命令。

## 像同事一样讨论

先用自己的话复述你理解的目标，并问最能改变方案的一两个问题。根据问题复杂度决定讨论轮数：信息已经充分时直接收敛，存在产品、技术或验收岔路时继续追问。不要把六维清单逐项问成表单。

能通过代码、文件或工具确认的事实先自行核实。主动提出具体的完成标准，让用户修正；不要只问一句“怎么验收”。

讨论过程中持续判断承载方式：

- 留在当前 Session：用户希望实时参与、马上执行，或讨论本身就是结果。
- 创建 Task：工作需要未来触发、独立调度、持久跟踪、隔离 Session 或清晰的独立交付。
- 不做：收益不足、前提不成立或用户明确放弃。

这三种结局都正常。不要为了完成流程而强推创建 Task。

## 撰写一份完整的 task.md

只有当双方倾向创建 Task 时，才把全部执行上下文写成一个候选 `task.md`。一个未参与讨论的 Agent 只读这一个文件，也应能完成工作并判断是否完成。

内容通常覆盖：

- 背景与动机
- 目标和预期结果
- 范围、边界与非目标
- 已确认的关键决策和约束
- 已知现状、相关文件或输入
- 风险、异常处理和需要保留的用户强调
- 验收与验证，包括适合的自动检查、自查和端到端场景

结构应服务于具体任务，不必机械套模板。简单任务可以很短，复杂任务可以使用清晰章节。是否要求独立子 Agent 验收由任务风险决定；高风险、跨模块或主观偏差明显时应写入，低风险机械任务不必强加。

将候选稿写到：

`<candidatesDir>/<candidateId>/task.md`

`candidateId` 使用小写字母、数字和连字符，保持简短且在本次讨论内唯一。候选目录不是 Task，不调用调度，也不写 `verify.md`、`progress.md`、`alignment.md` 或 Task 数据行。

## 创建前确认

写好候选稿后，在同一条回复中给用户一个可审阅的创建提案：

1. 用几句话说明 Task 的核心逻辑。
2. 给出可点击的绝对文件路径：`[查看 task.md](<absolute-path>)`。
3. 用 Markdown 表格列出将提交的最终参数，至少包含名称、工作区、执行模式、触发/时间、Session 策略、结束条件；未设置的参数明确写“未设置”或“跟随 Agent”。
4. 明确说出确认后将执行的动作，例如“创建并启用周期任务”或“创建一次性 Task 并立即派发”。
5. 请求用户明确确认，或让用户提出修改。

用户在确认前提出任何内容或参数调整时，更新候选 `task.md` 和表格，再次等待确认。模糊的“看看”“继续聊聊”不算创建确认。

## 确认后创建

收到明确确认后，按 `myagents-task-automation` 的能力说明调用通用 CLI。创建统一使用候选文件：

执行 mutation 前先运行 `myagents task create-direct --help`，以当前 App 随附 CLI 的 leaf help 核对最终参数名；若提案还包含立即派发，再同样核对 `myagents task run --help`。不要仅凭 Skill 中的示例猜测可能已变化的 CLI 细节。

```bash
myagents task create-direct --name "<name>" \
  --workspaceId "<workspaceId>" \
  --workspacePath "<workspacePath>" \
  --taskMdFile "<absolute-candidate-task.md>" \
  <其余已确认参数> --json
```

若有 `sourceRecordId`，传入 `--sourceRecordId`；不要创建第二份 Task 文档。解析 JSON 中的权威 `taskId`，回读确认。只有提案明确包含“立即派发/启用”，且用户一并确认时，才继续 `myagents task run <taskId> --json`；否则保持创建后的默认状态。

完成后简洁报告 Task 名称、ID、实际模式、下一次执行信息（如有）和 Task Center 入口。创建失败时保留候选稿，说明可重试的具体错误，不伪造成功结果。

## 留在 Session 或结束讨论

如果用户选择直接在当前 Session 做，先用简短的“目标 + 完成标准”复述约定，再按普通 Agent 工作流执行；不要创建候选目录或 Task。纯探索或明确不做时，总结关键结论即可。
