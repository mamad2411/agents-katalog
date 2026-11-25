---
name: prd2case
description: 指导如何生成文本测试用例(case.md), 文本测试用例将作为后续流程中API自动化测试和Web e2e自动化测试的输入；生成Web测试分析时仅聚焦spec.md中最核心的P00功能和验证点
user-invocable: true
---

# PRD to Test Cases
- PRD2Case有两类下游测试执行任务：API自动化测试和Web e2e自动化测试，二者所需的输入信息和输出内容不同，是**互相独立**的两种任务
- 当你根据输入判定测试执行任务的类型后，直接阅读`任务类型1: 生成API自动化测试所需的文本测试用例` 或 `任务类型2: 生成Web e2e自动化测试所需的文本测试用例` 对应的内容，并忽略另一种任务类型的描述
- 任务的产出需要放在本次开发任务的对应目录下，通常为`specs/yyyymmdd-feature-name`


## 任务类型1: 生成API自动化测试所需的文本测试用例

**Attention**: 当前仅支持单接口的测试用例执行，不要生成多接口的测试用例

### 任务所需信息
1. (**必须**) spec文档(spec.md)
2. (可选) 需求文档(prd.md)
3. (可选) 技术实现文档(ERD)
4. (可选) 代码变更，可通过阅读git工作区中的内容，commit等获取

### 任务流程
**step0: `idl`文件（接口定义关键文件）寻找与确认**
- 首先检查 spec.md、plan.md、tasks.md 中是否已包含 idl 路径信息，若有则直接使用
- 若上述文档中未提及，检查项目根目录下是否存在 `idl/` 目录
- 若根目录下存在 `idl/` 目录，使用 `AskUserQuestion` 让用户确认该路径是否正确，以及 idl 所在的 git 分支是否为本次需求对应的版本
- 若根目录下不存在 `idl/` 目录，直接使用 `AskUserQuestion` 让用户提供 idl 路径和对应的 git 分支
- 用户确认或提供路径和分支后继续后续步骤

**step1: 复制模板并创建任务结果文件**
使用cp的bash命令，复制resources/api_test_template.md到本次开发任务对应的`test/`目录，命名为`case.md`

**step2: 受影响接口分析**
根据任务所需的信息，读取任务所需信息的文件、相关代码和git工作区中的内容，整理受影响的接口，结果需要包含如下信息
1. 受影响的接口（API名称）
2. 接口所属的psm(从spec.md中读取), 保持其格式(`p.s.m`, 由`.`分隔的三段式标识)
2. 接口对应的Endpoint, 包括请求方法和URI
3. 接口对应逻辑变更，使用文字描述

**step3: 测试分析**
这一步是生成API测试所需文本测试用例的核心，你需要在这一步针对每个接口，做如下分析：
1. 设计测试场景，针对接口的改动，设计正向和负向的测试场景，其中以正向的测试场景为主，验证功能被正确实现；负向的测试场景为辅，仅设计必要的负向测试场景，每个测试场景用一句话描述
  - 例如只有在观察到接口对某个字符类型字段做了长度校验或截断，或者对应的数据库字段类型为VARCHAR(xxx)时，才设计对应的负向用例
  - 除非输入中有明确的要求，否则不要设计例如查询参数为String, 但传参的值为Int这样不存在的负向场景
2. 设计每个测试场景的具体测试内容，包含三部分
  - 核心请求参数：测试这个场景所需的核心参数
    - spec目录下通常会包含部分你所需要参数的具体指，每个核心参数都必须在specs目录下的信息中搜索可能的准确值
    - 若通过已知信息能知道参数的值，则使用准确值；若无法获取，则使用文本描述说明这个参数需要是什么，例如一条数据库中存在的item_id
  - 校验点：采用**两层校验**结构，外层校验网关/传输层错误，内层校验业务响应状态和字段
    - **外层校验（网关层）**：
      - HTTP 类型接口：`status_code == 200`（校验业务 HTTP 状态码）
      - RPC 类型接口：无 HTTP 状态码概念，**禁止**生成 `status_code == 200` 等断言
      - 注意：网关自身的错误码（如 `Gateway.ErrorCode`）由测试执行框架自动校验，无需在用例中显式断言；但需了解当网关层报错时（如服务发现失败 `ErrorCode: 61003`），内层业务响应可能为空或状态码不可信
    - **内层校验（业务层）**：
      - 业务响应码校验（**必要**）：生成业务响应码断言前，必须实际读取 `base.thrift`（或对应的 base IDL 文件）中 `BaseResp` 的结构定义，确认以下三点后再编写断言：
        1. 表示状态码的字段名（如 `StatusCode` / `status_code` / `code`）
        2. 成功值（如 `0` / `200`）
        3. JSON 序列化后的实际字段路径（根据 `go.tag` 或序列化注解确定，例如 `go.tag='json:"StatusCode"'` 对应 `$.BaseResp.StatusCode`，而非 `$.base_resp.status_code`）
        - **禁止基于框架惯例推断字段名或路径，必须以 IDL 定义为准**
        - 正向场景必须校验该字段为成功值；负向场景校验对应的错误码。若IDL中接口响应结构确实不包含业务状态码字段，则跳过此项
        - **RPC 接口的业务响应码必须使用 `jsonpath` 断言**（如 `jsonpath('$.BaseResp.StatusCode') == 0`），不得使用 `status_code` 断言
      - 具体字段断言：对需要做校验的字段进行断言，断言的内容使用自然语言描述即可，但注意所有的断言都必须是明确且具体的，不要出现例如xx字段符合预期这样的模糊描述
  - **jsonpath 字段路径规则（适用于所有断言，包括业务响应码和具体字段）**：
    - 所有 `jsonpath` 断言中的字段路径必须与 JSON 实际序列化后的字段名完全一致，**禁止基于 Go/Python 等语言惯例自行将字段名转为 snake_case**
    - 确定字段路径的唯一依据是 IDL 定义：
      1. 若 IDL 字段有显式 `go.tag='json:"xxx"'` 注解，使用注解中的 `xxx` 作为 JSON 字段名
      2. 若 IDL 字段**没有** `go.tag` 或 `json` 注解，**Thrift 默认行为是保留原始字段名**（通常为 PascalCase），例如 IDL 中 `ShopID` 序列化后仍为 `ShopID`，而非 `shop_id`
    - 常见错误示例（**禁止**）：
      - `$.base_resp.StatusCode` → 应为 `$.BaseResp.StatusCode`
      - `$.shop_single_shelf_commission_list[0].shop_id` → 应为 `$.ShopSingleShelfCommissionList[0].ShopID`
      - `$.open_loop_commission_list[0].single_shelf_commission_rate` → 应为 `$.OpenLoopCommissionList[0].SingleShelfCommissionRate`
    - 编写断言前，必须阅读接口 Response 结构及其嵌套结构的 IDL 定义，逐一确认每个字段的实际 JSON 序列化名称
  - 优先级：核心、典型场景为P0; 次要场景为P1; 负向测试场景的优先级通常为P2, 但如果是影响较大的重要负向场景，可标记为P1.
  - **特别要求**：仅保留优先级为P0的测试用例


**step4: 更新test/case.md**
根据前面步骤的结果，完成`test/case.md`的编写

## 任务类型2: 生成Web e2e自动化测试所需的文本测试用例

**Global Principles**
- This workflow is not suggestion, but a **SOP** you MUST follow.
- NEVER SKIP, STRICTLY FOLLOW the INSTRUCTIONS.

### 任务所需信息
1. (**必须**) spec文档(spec.md) 或需求文档（Lark URL、本地 Markdown 等）
2. (可选) 技术实现文档(ERD)
3. (可选) 代码变更，可通过阅读git工作区中的内容，commit等获取

### 任务流程

#### Stage-0: 偏好配置（固定值，无需用户确认）
Web e2e 场景下，以下配置为固定值，直接使用，不需要询问用户：
- `Global`: Semi Auto
- `Generation Style`: Follow the input
- `CASE_GENERATION_MODE`: Web

#### Stage-1: 确定产出目录
- Web e2e 场景的所有产出文件放在本次开发任务对应 spec 目录下的 `test/` 子目录中
- 通常为 `specs/yyyymmdd-feature-name/test/`（与 spec.md 同级的 `test/` 目录）
- 如果 `test/` 目录不存在，使用 `mkdir -p` 创建
- 后续步骤中 `$TEST_DIR` 均指该目录

```
specs/yyyymmdd-feature-name/
├── spec.md
├── plan.md
├── ...
└── test/
    ├── test_analysis.md         # Stage-2 产出，同时作为 Stage-3 的输入文档
    └── case.md
```

#### Stage-2: 测试分析（生成 test_analysis.md）

本阶段从测试执行视角分析 spec.md，产出 `test_analysis.md` 作为后续用例生成的输入文档。

**语言选择**：`test_analysis.md` 及后续生成的 `case.md` 的内容语言，跟随用户的语言习惯（即用户与 agent 交流所使用的语言）。用户用中文交流则输出中文，用英文交流则输出英文。

**step1: 测试分析**
根据上下文中的信息，特别是如下信息
- spec文档(spec.md)
- 技术实现文档(ERD)
从测试执行而非技术实现的视角，分析 spec.md 中的功能及其验证点
>> 测试执行视角：测试执行时，是由一个Browser Use Agent来根据自然语言描述的结构化脚本，进行页面操作和断言判定

补充约束：
- 不限定优先级范围，完整分析 spec.md 中涉及的功能和验证点
- 必须识别并标注哪些验证点属于 **P0 核心功能**（最核心的主链路、最影响验收结果的能力）
- 输出目标是产出完整的测试分析，同时明确区分 P0 核心验证点与其他验证点
- **前置条件必须写死到具体的测试对象**：不能只写泛化的"进入某页面"或"存在某数据"，必须明确指定满足该场景所需的具体测试对象和状态。例如：
  - 错误写法：`进入项目详情页` / `存在历史版本`
  - 正确写法：`进入包含至少 2 个版本且含 Auto Prompt 标识的项目详情页` / `当前项目存在 v1、v2 两个版本，其中 v2 带有 Auto Prompt 标识`
  - 原则：前置条件应精确到测试执行 Agent 据此能判断"当前页面/数据是否满足要求"，而不是到了页面才发现数据不满足

**step2: 编写测试分析文档（全量功能验证点）**
- 使用cp的bash命令，复制resources/test_analysis_template.md到 `$TEST_DIR` 下，命名为`test_analysis.md`
- **必须覆盖 spec.md 中所有功能的验证点**，不能只写核心功能，按"功能模块 -> 测试场景 -> 验证点"组织：
    1. 功能模块：spec.md 中涉及的**每一个**功能模块，不遗漏
    2. 测试场景：每个功能模块下的所有可执行测试场景（包括正向主链路、关键分支、异常/边界场景）
    3. 验证点：在该场景下必须明确断言的页面行为、结果状态、文案或产物
- 每个验证点需标注是否为 P0（在测试场景描述末尾标注 `[P0]`），标注依据：
  - P0：主链路、主入口、主结果等最核心的验收能力
  - 未标注：次要场景、边界场景、异常场景等
- 此步骤**只写功能测试章节**，测试执行信息章节留空，在 step4 中填充

**step3: 结合 `spec.md` 与 `test_analysis.md` 二次反思，查漏补缺**
- 完成功能测试章节后，不能直接进入下一步，必须做一次二次审查
- 审查输入至少包括：
  - `spec.md`
  - 刚生成的 `test_analysis.md`
  - 如有 ERD / 代码变更，也应一并参考
- 必须使用下面这段固定 prompt 做二次反思，不能只凭感觉补充：

```text
请结合 spec.md 与当前 test_analysis.md，对测试分析做一次系统性查漏补缺。

检查时至少覆盖以下维度：
1. 全量功能覆盖：spec 中涉及的**每一个功能模块**是否都已分析，不能只覆盖核心功能而遗漏次要功能
2. 全量场景覆盖：每个功能模块下的正向主链路、关键分支、异常/边界场景是否都已列出
3. P0 标注：P0 核心验证点的标注是否准确，是否把非核心场景错误标为 P0，或遗漏了真正的核心链路
4. 关键验证点：每个测试场景是否都写清楚了必须断言的结果、状态、文案、页面变化或产物
5. 关键分支：如果 spec 中存在必须验证的关键分支、状态切换或前后置依赖，是否已经纳入

输出要求：
- 先列出"发现的遗漏点"
- 再说明"需要如何补到 test_analysis.md"
- 如果没有遗漏，也要明确写出"未发现明显遗漏"，不能跳过这一步
```
- 审查目标：
  1. 检查 `spec.md` 中的功能与验收点是否已完整体现在 `test_analysis.md`
  2. 检查 P0 标注是否准确
  3. 检查 `test_analysis.md` 是否对测试执行足够具体、可执行
- 如果发现遗漏，必须先回写并更新 `test_analysis.md`，再继续下一步

**step4: 梳理测试执行信息（页面 URL + 可执行数据要求）**
- 遍历 `test_analysis.md` 中所有验证点，梳理每个验证点的前置条件需要访问的页面**以及页面内的数据状态要求**
- 将所有不重复的页面汇总到 `test_analysis.md` 的"测试执行信息"章节，填写三列信息：
  - **页面名称**
  - **页面 URL**：从 spec.md、输入信息及上下文中能获取到的直接填写，无法获取的填 `<TO_FILL>`
  - **可执行数据要求**：该页面必须满足的数据状态，用例才能跑通。例如：
    - "该项目至少存在 2 个可比较版本"
    - "其中至少 1 个版本带有 Auto Prompt 标识"
    - "列表中至少有 1 条可操作记录，不能是空态"
  - 如果数据要求无法从 spec 直接得出，在该列填写 `<TO_FILL>`，在 step5 由用户补充
- 同一个页面只列一行，去重

**step5: 用户确认测试执行信息（页面、URL 与数据要求）**
- 必须把 `test_analysis.md` 中"测试执行信息"章节展示给用户确认
- 必须确认的内容包括：
  - 页面名称
  - 页面 URL
  - **可执行数据要求是否完整、准确**
  - 是否还有缺失页面
  - URL 是否对应本次实际测试环境
- 当存在 `页面URL` 或 `可执行数据要求` 列为 `<TO_FILL>` 的占位符，或内容不完整/不准确，则使用 `AskUserQuestion` 工具让用户依次补充
- 只有在用户明确确认后，才能继续进入 Stage-3
- 如果用户修改了页面、URL 或数据要求，必须先更新 `test_analysis.md`，再继续下一步

#### Stage-3: 用例生成
- **[强制]** 读取 `references/case_generation_workflow.md`，严格遵循其中的指令
- 本阶段以 Stage-2 产出的 `test_analysis.md` 作为输入文档
- 偏好配置使用 Stage-0 的固定值（Semi Auto / Decide by Agent / Web）

用例生成的核心流程（详见 `references/case_generation_workflow.md`）：

**step0: 输入确认（Input Confirmation）**
- 确认 `test_analysis.md`（Stage-2 产出）已就绪
- 检查 Business Identifier 是否可用
- 检查其他可选输入（PRD、技术设计文档、代码变更、Figma）
- 向用户展示检查结果，缺少必要输入时请求补充

**step1: 生成风格（固定）**
- Web e2e 场景下，`Generation Style` 固定为 **Follow the input**，由本地 agent 直接将 `test_analysis.md` 转换为 `case.md`，不调用远程 API

**step2: 上下文收集（Context Gathering）**
- 搜索工作区（特别是 Knowledge Base 目录）查找相关的：
  - 业务知识（`business_knowledge/${Business Identifier}`）
  - 测试用例编写规则
  - 回归测试用例
  - 业务自定义技能（`skills/custom/${Business Identifier}`）
- 业务自定义知识/技能优先级高于通用信息，如有冲突以自定义为准
- 基于收集到的上下文，制定更新 `test_analysis.md` 的计划，经用户确认后执行

**step3: 用例生成（Test Case Generation）**

采用 Follow the input 风格，由本地 agent 直接生成用例：
- **[强制]** 读取 `references/test_case_grammar.md`，了解用例的文本格式和 JSON 格式语法
- **[强制]** 读取 `references/ab_setting_rule.md`，了解 A/B 实验分组下的用例组织方式
- 忠实于 `test_analysis.md`，将其转换为 `case.md`
- **前置条件严格性检查**：生成 `case.md` 时，检查每个 `前置条件` 节点是否精确到具体的测试对象和状态，避免泛化描述导致测试执行 Agent 进入不满足条件的页面。如果 `test_analysis.md` 中的前置条件不够具体，在转换时主动补充细化
- 使用 `scripts/case_grammar_check.py` 检查生成的用例
- 再次读取 `references/test_case_grammar.md` 确认用例格式一致性

##### Web 场景特殊后处理（两种风格均需执行）
当 `case_mode` 为 `Web` 时，必须执行以下后处理：
- **前置条件添加 URL**：在每个 `前置条件` 节点开头添加 `访问: $URL\n`
  - `$URL` 来源于 `test_analysis.md`（Stage-2 产出）或上下文，如无具体 URL 信息则使用 AskUserQuestion 向用户索取
  - URL 必须对应本次实际测试环境（prod / ppe / boe）
- **移除冗余步骤**：如果 `操作步骤` 中已有 `打开浏览器`、`访问 $URL` 等步骤，移除它们，只保留访问后的操作
- **添加 e2e 标签**：在 `前置条件` 节点内容末尾追加 `**[tag]** e2e`（新起一行，属于前置条件内容的一部分，遵循 `references/test_case_grammar.md` 中 tag 语法）
- **添加 P0 优先级标签**：对 `test_analysis.md` 中标注了 `[P0]` 的验证点，该验证点对应的**每一个** `预期结果` 节点都要在其内容后面换行追加 `**[priority]** P0`。一个场景下有多个 `预期结果` 时，每个 `预期结果` 都独立打标，不能只打最后一个。未标注 P0 的验证点不打优先级标签。示例：
  ```text
  ####### **操作步骤** 1. 步骤1
  2. 步骤2
  ######## **预期结果** 断言1
  **[priority]** P0
  ######## **预期结果** 断言2
  **[priority]** P0
  ```

##### markdown2Midscene 调用注意事项
`case.md` 中的 `前置条件` 节点包含了完整的测试前提描述（数据要求、状态约束等），但 midscene 执行时会把前置条件当作可执行步骤。因此：
- **调用 markdown2Midscene 转换时，`前置条件` 内容仅保留 `访问: $URL` 这一行**，其余描述性文本（数据要求、状态总结等）和标签（`**[tag]**`、`**[priority]**`）均剔除
- **`case.md` 本身不做任何修改**，保持完整的前置条件描述，裁剪仅发生在传给 markdown2Midscene 的过程中

#### Stage-4: 归档到 Bits（强制自动执行，不得跳过）
`case.md` 生成或更新后，**必须立即自动执行归档到 Bits**，不需要询问用户、不需要用户确认、不需要等待用户指令。

- **case-title**：与 spec.md 的标题（第一行 `#` 标题）保持一致
- **user-name**：使用 git 仓库作者的邮箱前缀（通过 `git config user.email` 获取，取 `@` 前的部分）

**首次归档**（`$TEST_DIR/save_result.json` 不存在时）：

```bash
CASE_TITLE="$(head -1 specs/yyyymmdd-feature-name/spec.md | sed 's/^#\s*//')"
python scripts/case_management.py save "$TEST_DIR/case.md" \
  --case-title "$CASE_TITLE" \
  -o "$TEST_DIR/save_result.json"
```

归档成功后，`save_result.json` 中会包含返回的 `case_id`，后续更新时使用。

**更新归档**（`$TEST_DIR/save_result.json` 已存在，从中读取 `case_id`）：

当 `case.md` 有更新时，**不要新建 Bits 用例**，使用已有的 `case_id` 更新：

```bash
CASE_ID="$(python3 -c "import json; d=json.load(open('$TEST_DIR/save_result.json')); print(d.get('data',{}).get('case_url',{}).get('caseId') or d.get('data',{}).get('case_id',''))")"
CASE_TITLE="$(head -1 specs/yyyymmdd-feature-name/spec.md | sed 's/^#\s*//')"
python scripts/case_management.py save "$TEST_DIR/case.md" \
  --case-title "$CASE_TITLE" \
  --case-id "$CASE_ID" \
  -o "$TEST_DIR/save_result.json"
```

#### TTAT 用例组更新（case.md 有更新时）

当 `case.md` 更新后，如果已有 TTAT 用例组（`case_group_id` 已知），**不要新建用例组**，直接使用 `edit_with_cases` 接口更新已有用例组的数据：

```bash
curl 'https://ttat-openapi-sg.tiktok-row.net/ui/web_e2e/case_group/edit_with_cases' \
  -H 'Content-Type: application/json' \
  -H 'X-Custom-Token: fb1202cb29e923298f002b71e0889cc6' \
  --data-raw '{
    "creator": "<git user.email 邮箱前缀>",
    "case_group_name": "<用例组名称>",
    "web": {"bridgeMode": "false"},
    "tasks": <更新后的 tasks 数组>,
    "extras": <原有 extras 配置>,
    "case_group_id": <已有用例组 ID>
  }'
```

**关键规则**：
- `case_group_id`：使用已有用例组的 ID，不得省略，否则会新建用例组
- `tasks`：根据更新后的 `case.md` 重新生成完整的 tasks 数组
- `extras`：保持与原用例组一致的 `execEnv` 等执行环境配置
- `creator`：与原用例组创建者一致
- `case_group_name`：与原用例组名称一致
- 只有当 `edit_with_cases` 接口调用失败时，才考虑新建用例组

### 读取 Lark 文档
使用 `lark-docs` MCP 读取 Lark 文档，不要使用 fetch

### Available Tools

#### 读写 Bits 测试用例
使用 `scripts/case_management.py` 读写 Bits 用例：

- 从 Bits 获取用例并保存到本地（需提升权限执行）：
```bash
python scripts/case_management.py fetch "<bits_case_url>" -o "$TEST_DIR/case_xxx.json"
```

- 将本地用例上传到 Bits（新建，需提升权限执行）：
```bash
python scripts/case_management.py save "$TEST_DIR/case.md" \
  --case-title "<标题>" \
  -o "$TEST_DIR/save_result.json"
```

- 更新已有 Bits 用例（传入 `--case-id`，需提升权限执行）：
```bash
python scripts/case_management.py save "$TEST_DIR/case.md" \
  --case-title "<标题>" \
  --case-id <已有用例ID> \
  -o "$TEST_DIR/save_result.json"
```

#### 更新 TTAT 用例组
使用 `edit_with_cases` 接口更新已有用例组（不新建）：

```bash
curl 'https://ttat-openapi-sg.tiktok-row.net/ui/web_e2e/case_group/edit_with_cases' \
  -H 'Content-Type: application/json' \
  -H 'X-Custom-Token: fb1202cb29e923298f002b71e0889cc6' \
  --data-raw '{
    "creator": "<邮箱前缀>",
    "case_group_name": "<用例组名称>",
    "web": {"bridgeMode": "false"},
    "tasks": [...],
    "extras": {...},
    "case_group_id": <用例组ID>
  }'
```

## Lessons Learned

### 前置条件必须精确到具体测试对象，URL 不等于可执行

**问题**：泛化的前置条件（如"进入项目详情页"、"存在历史版本"）会导致测试执行 Agent 进入不满足条件的页面，产生误判。只写页面 URL 只能保证"进到哪个页面"，不能保证"页面里的数据状态满足可执行前置条件"。

**典型失败场景**：
- URL 指向一个项目详情页，但该项目只有 v1，没有可比较的历史版本
- URL 指向一个列表页，但列表为空态，没有可操作记录
- URL 指向一个详情页，但该页面不包含所需的特定标识（如 Auto Prompt）

**正确做法**：
- 前置条件写死到具体测试对象的特征和状态
- `test_analysis.md` 的测试执行信息不能只给 URL，必须额外补充"可执行数据要求"
- 如果数据要求无法从 spec 直接得到，必须在生成用例前显式向用户确认
- 测试执行 Agent 应能据此判断"当前页面 + 数据状态是否满足要求"

### 失败归因不要过度依赖自动分析的保守结论

**问题**：自动分析脚本可能给出保守兜底结论（如"低置信度 - 步骤描述问题"），但实际报错信息中已包含足够的业务语义（如"当前项目只有 v1，没有可比较历史版本"），应优先从报错信息提取精确的失败原因。

**正确做法**：
- 优先从平台原始报错中提取业务含义，翻译成准确的测试前置问题
- 归因粒度要足够细："进入了不满足前置条件的详情页"比"空数据/没有数据"更准确
