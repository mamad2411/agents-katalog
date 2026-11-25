---
name: safe-review
description: Security & test-regression review for AI-assisted coding (Vibe Coding). Triggers on "/safe_review", "safe review", "安全审查", "回归测试", "越权检查", or after any change touching auth/permissions/data-ownership/payment/business-state logic. Prioritizes P0 risks (auth, authorization, data isolation, money, core business flow) over blanket coverage; designs normal/boundary/exception test matrices, builds a repeatable automated regression net, verifies tests are real via deliberate-break-then-restore, and performs non-destructive attacker-perspective checks on backend endpoints. Always output the final report in the exact 10-section Chinese template defined in SKILL.md — never a different structure, section count, or language.
---

# Safe Review — AI 辅助开发的测试与安全审查技能

## 一句话定位

**这不是"帮你写单元测试"或"冲覆盖率"的技能。它的唯一目标是：降低 AI 快速迭代时最容易被忽略的真实风险——权限被绕过、数据被越权访问、核心业务规则被改坏——并把这些检查沉淀成可重复运行的自动回归网。**

## 触发条件

- 用户输入 `/safe_review`（可带参数：文件路径 / 接口名 / "本次变更" / "全仓库"）
- 用户提到"安全审查"、"回归测试"、"越权检查"、"这段改动安全吗"等
- **主动建议触发**（无需用户先问）：当检测到本次改动涉及 认证/授权判断、`owner_id`/`tenant_id`/`user_id` 过滤条件、密码/Token/敏感字段、金额/库存/状态流转、文件上传下载、管理后台接口 时，应主动提示用户"这处改动建议跑一次 `/safe_review`"

## 核心原则：分清主次，不平均用力

**测试的目标是降低真实风险，不是制造测试数量。** 严禁对 P2/P3 功能生成大量低价值测试，也严禁对 P0/P1 功能偷工减料。

| 等级 | 定义 | 测试深度要求 |
|---|---|---|
| **P0** | 认证授权、数据隔离（多租户/组织/owner）、资金与核心业务流程 | 正常+边界+异常+攻击者视角+假测试验证 全覆盖，必须自动化，改动后必须运行，上线前必须通过 |
| **P1** | 常用业务路径、关键接口、重要配置 | 正常+主要边界+主要异常，建议自动化，改动后建议运行 |
| **P2** | 普通展示功能、低风险辅助功能 | 主要正常路径+少量异常，可视情况自动化 |
| **P3** | 纯 UI 样式、静态文案、低影响页面 | 只做基础冒烟/人工检查，不建议投入自动化成本 |

判定一个功能是否 P0/P1，看它是否属于以下四类之一（完整判定标准见 [references/risk-classification.md](references/risk-classification.md)）：
1. 影响当前用户身份和权限（登录/登出/注册/密码重置、Token/Session、角色权限判断、多租户隔离）
2. 影响用户数据归属和数据安全（查询/导出/下载/上传/删除/批量操作是否可能触达他人数据）
3. 影响核心业务流程（下单/支付/审批/退款/发货/库存/报价/合同/工单，状态流转与金额计算）
4. 影响系统边界（管理后台、内部接口、Webhook、第三方回调、文件上传下载、对外 API）

## 工作流程（9 步）

执行 `/safe_review` 时按顺序进行，每步做完再进入下一步：

1. **识别项目技术栈**：语言、框架、测试框架、API 风格、鉴权方式、数据模型、当前 Git diff。可运行 `scripts/detect_stack.sh`（Unix/Codex 容器）或 `scripts/detect_stack.ps1`（Windows，执行策略限制时用 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detect_stack.ps1`，脚本本身只读不写）辅助探测，也可以直接读 `package.json`/`go.mod`/`*.csproj` 等 manifest 和 `git diff` 自行判断。
2. **判断审查范围**：当前变更（默认，`git diff` / 最近几次 commit）/ 用户指定文件 / 指定接口 / 指定业务功能 / 全仓库关键路径。范围不明确时优先问用户，而不是默认扫全仓库。
3. **对功能进行风险分级**：P0/P1/P2/P3，并说明分级理由（哪些是高风险、为什么、哪些只需轻量测试、哪些不值得投入）。
4. **为高风险功能生成测试矩阵**：正常/边界/异常/权限与数据隔离/攻击者视角。每个关键功能至少 1 个正常 + 2~5 个边界 + 2~5 个异常用例，每条说明测试目标、输入条件、操作步骤、预期结果、断言点。设计参考 [references/test-matrix-guide.md](references/test-matrix-guide.md)。
5. **生成或补充自动化测试**：优先复用项目已有测试框架（对照表见 [references/framework-cheatsheet.md](references/framework-cheatsheet.md)），尽量少改业务代码，关注行为和结果而非脆弱的实现细节。没有测试框架时推荐最小可用方案。
   - **"纯语法适配"例外**：如果测试框架本身跑不起来是因为模块系统不匹配（如 CommonJS `require`/`module.exports` vs ESM `import`/`export`）、缺少测试运行所需的构建配置等**与业务逻辑无关**的原因，允许做最小必要的语法/配置调整让测试能执行；但这类调整**不算业务逻辑修改**，不需要按"修改安全相关逻辑前必须提醒用户确认"走确认流程，只需在报告第 5 段简单注明"为了让测试可运行，调整了 XXX（模块语法/构建配置），未改变任何业务逻辑"。如果调整已经涉及业务逻辑本身（哪怕一行），必须走确认流程，不能借"为了跑测试"绕过。
6. **运行测试**：能跑就跑并报告结果；不能跑要说明原因并给出用户可手动执行的命令。
7. **执行"当下假测试"有效性验证**（仅限本地/测试分支，不影响生产、不提交）：对关键测试做小范围故意改错 → 确认对应测试失败 → 恢复代码 → 确认测试通过 → 报告验证结果。流程与场景清单见 [references/mutation-verification.md](references/mutation-verification.md)。
8. **用脚本生成报告草稿文件（不要凭记忆手打标题）**：如果当前环境能执行 Python，跑：
   ```bash
   python skills/safe-review/scripts/new_report.py <草稿路径，如 .safe_review/draft.md 或系统临时目录下的等价路径>
   ```
   这一步会把 [assets/report-skeleton.md](assets/report-skeleton.md) 原样写成一个真实文件——标题是脚本复制出来的字节，不经过你的"回忆"，天然不存在翻译/繁体化/意译的空间。然后**只用 Edit 工具**在每个 `#`/`##` 标题行下方插入内容，绝对不要把 Edit 的 `old_string`/`new_string` 涉及到标题行本身（也就是说，你的每一次编辑都应该保留标题所在的那一行原封不动）。
   - **如果当前环境不能执行 Python**（纯文本对话、无文件系统等场景），退回手动方式：用 Read 工具原样读取 [assets/report-skeleton.md](assets/report-skeleton.md)，把读到的原文整段复制作为回答骨架，只在标题下面填内容，不改标题文字、不改顺序、不合并、不省略。
9. **输出前用脚本校验格式（提交最终回答前必做，不可跳过）**：
   ```bash
   python skills/safe-review/scripts/check_report_format.py <第 8 步的草稿文件路径>
   ```
   - 输出 `[PASS]` 才可以把这份文件的内容作为最终回答发出去；输出 `[FAIL]` 必须按报错提示改到通过为止，不允许把"内容对但格式没过校验"的版本直接发出去
   - 最终回答里，把这份已通过校验的文件内容**原样搬进对话**（可以用 Read 工具读出来再原文粘贴），不要在搬运过程中重新打字或"顺手润色"标题
   - **如果当前环境没有 Python 可用**，退回人工逐字自检：把最终回答和 [assets/report-skeleton.md](assets/report-skeleton.md) 逐字符比对——标题数量是否正好 11 个（1 个 H1 + 10 个 H2）、文字是否字符级相同（不能翻译成英文、不能改写成别的说法、不能是繁体字形）、正文是否为**简体中文**（除非用户明确要求英文）；任何一条不满足都必须重写

## 覆盖范围检查清单（精简版，详情见 references）

- **正常情况**：合法输入、权限正确、数据状态正确、返回预期成功结果
- **边界情况**：空值/最小值/最大值/超长字符串/特殊字符/临界金额数量时间/分页首末页与越界/文件大小临界/权限刚好满足或不满足/状态刚好可流转或不可流转
- **异常情况**：未登录/Token 过期/权限不足/参数缺失或类型错误/非法 ID/访问不存在或他人数据/重复提交/业务状态不允许/后端依赖或数据库第三方服务异常
- **自动回归网五类**：单元测试（业务规则/权限判断/参数校验）、接口测试（认证授权/参数校验/返回字段不多不少）、集成测试（完整流程/状态流转/DB 读写/第三方 Mock）、安全回归测试（未登录拒绝/越权拒绝/非法参数拒绝/敏感字段不泄露/普通用户调不了管理员接口）、关键路径冒烟（登录→取当前用户→创建核心对象→查自己数据→改自己数据→删/关自己数据→权限不足应失败）
- **攻击者视角十大场景**：未登录访问 / 低权限调高权限接口 / 水平越权 / 垂直越权 / 参数篡改（user_id、role、price、is_admin 等）/ 敏感字段泄露 / 注入类风险（低风险 payload）/ 文件安全（非法扩展名、路径穿越）/ 业务逻辑绕过（重复提交、跳过审批、改状态改金额、重放）/ 速率限制与防刷。完整方法与预期结果见 [references/attacker-playbook.md](references/attacker-playbook.md)。

## 安全边界（强制，不可绕过）

- 默认只在**本地环境、测试环境、预发环境或用户明确授权的环境**执行验证；未授权时只输出测试计划和本地验证建议，不实际执行攻击性测试
- 不主动扫描公网未知目标；不执行破坏性 payload；不删除/篡改/拖库/提权/持久化；不绕过真实系统防护；不生成恶意利用工具
- "当下假测试"的故意改错必须小范围、可回滚，只在本地/测试分支进行；验证完必须恢复代码；**不得提交故意改错的代码**；不得制造破坏性数据
- **修改安全相关逻辑（鉴权、权限判断、数据过滤条件等）前必须提醒用户确认**，不得未经确认直接改动业务代码
- 不确定的地方一律在报告中标记"需要人工确认"，不要臆断

## 避免过度测试

不要对简单 getter/setter、纯展示组件、静态文案写大量测试；不要为覆盖率测试实现细节而非业务行为；不要 Mock 掉所有关键逻辑导致测试形同虚设；不要只测"函数被调用"而不测结果正确性；不要为测试而重构业务代码引入不必要的复杂度。P2/P3 功能不需要机械性生成大量低价值用例。

## 输出格式

**硬性约束（不可协商）：最终回答必须使用下面这 10 个段落标题，按顺序完整输出，一个不能少：**

- **不得合并**多个段落（例如不能把第 6 段"当下假测试验证"并进第 7 段"安全攻防测试结果"里一起讲）
- **不得改名**（标题文字必须和下面模板一致，不能自行翻译成英文或换一种说法）
- **不得省略**——某段这次审查确实没跑（比如没有可用测试环境、范围太小用不上攻击者视角），也要把该段标题保留，内容写"未执行 / 需要人工确认"及具体原因，而不是直接删掉整段
- 报告语言固定用**简体中文**（除非用户明确要求用英文）——**不得使用繁体中文**，不得把"审查范围"写成"審查範圍"、"主次判断"写成"風險總覽"/"风险总览"、"自动回归网"写成"建議自動化測試"这类看似同义但文字不同的改写，标题必须和模板字符级完全相同
- **执行方法（机械化，降低自由发挥空间，对应工作流程第 8/9 步）**：不要凭记忆重打标题、不要意译、不要转换成繁体字形。正确做法是——用 [scripts/new_report.py](scripts/new_report.py) 生成一份草稿文件（标题由脚本写入，不经过你的记忆），只用 Edit 工具在标题下面填内容、不碰标题行本身；写完后用 [scripts/check_report_format.py](scripts/check_report_format.py) 做程序化校验，`PASS` 后把文件内容原样搬进最终回答。不要只在脑子里"自认为"格式对了，也不要相信自己能凭自觉在最终回答里现场打对标题——这一点已经被前向测试反复证明不可靠，必须让脚本承担这个责任

按以下 10 段结构输出报告（可参考完整填空模板 [references/report-template.md](references/report-template.md)、可直接复制的骨架 [assets/report-skeleton.md](assets/report-skeleton.md)，与示例 [../../examples/sample-report.md](../../examples/sample-report.md)）：

```markdown
# Safe Review 测试与安全审查报告

## 1. 审查范围
- 项目/路径：
- 当前分支：
- 当前变更：
- 技术栈：
- 测试框架：
- 审查模式：

## 2. 主次判断
| 功能/接口 | 风险等级 | 原因 | 测试深度 |
|---|---|---|---|

## 3. 关键风险摘要
- P0 风险：
- P1 风险：
- 需要人工确认：

## 4. 测试矩阵
| 功能/接口 | 正常情况 | 边界情况 | 异常情况 | 权限/数据隔离 | 攻击者视角 |
|---|---|---|---|---|---|

## 5. 自动回归网
- 已有测试：
- 新增测试：
- 建议新增测试：
- 建议加入 CI/CD 的命令：

## 6. 当下假测试验证
| 验证对象 | 故意改错 | 改错后结果（应失败） | 恢复后结果（应通过） | 结论 |
|---|---|---|---|---|

## 7. 安全攻防测试结果
| 接口 | 攻击视角 | 测试方法 | 预期结果 | 风险等级 | 建议 |
|---|---|---|---|---|---|

## 8. 避免过度测试说明
- 不建议深度测试的部分：
- 原因：
- 建议保留的轻量测试：

## 9. 修复和补测建议
- 立即补充：
- 本次迭代补充：
- 后续优化：

## 10. 最终结论
- 是否可以继续开发：
- 是否建议合并：
- 是否建议上线：
- 阻断项：
- 可接受风险：
```

报告要求：不要只给泛泛的安全建议，必须结合当前代码/当前 diff/当前接口或业务功能；不确定处标记"需要人工确认"；不要为覆盖率制造大量低价值测试；优先保护权限、数据、身份、核心业务和安全边界。

## 示例命令

```
/safe_review                     # 审查当前 Git 变更（默认范围）
/safe_review src/api/orders.ts   # 审查指定文件
/safe_review 订单导出接口         # 审查指定业务功能
/safe_review --full-repo         # 审查全仓库关键路径（耗时较长，谨慎使用）
```

## 参考文件索引（按需读取，不要一次性全部加载）

| 何时读取 | 文件 |
|---|---|
| 判定功能风险等级 | [references/risk-classification.md](references/risk-classification.md) |
| 设计测试用例细节 | [references/test-matrix-guide.md](references/test-matrix-guide.md) |
| 执行"当下假测试"验证 | [references/mutation-verification.md](references/mutation-verification.md) |
| 做安全攻防测试 | [references/attacker-playbook.md](references/attacker-playbook.md) |
| 找测试框架/运行命令/CI 建议 | [references/framework-cheatsheet.md](references/framework-cheatsheet.md) |
| 填写最终报告 | [references/report-template.md](references/report-template.md) |
| **生成报告草稿文件**（第 8 步必执行，不是可选参考） | [scripts/new_report.py](scripts/new_report.py)（内部读取 [assets/report-skeleton.md](assets/report-skeleton.md)） |
| **发送报告前，程序化校验格式**（第 9 步必执行，不是可选参考） | [scripts/check_report_format.py](scripts/check_report_format.py) |
| 参考完整范例 | [../../examples/sample-report.md](../../examples/sample-report.md) |
