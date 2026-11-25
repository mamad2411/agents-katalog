---
name: yida-formula-evaluate
description: 检查宜搭公式的语法、字段引用和常见错误。适用于用户要求“检查公式”“公式是否能用”“定位公式报错”时；也可读取已有公式、查询函数，并用样例核对计算结果。
---

# 检查和试算公式

用来回答“公式哪里写错了”“为什么没有算出值”“这个样例应该得到什么结果”。编写或修改公式时，通过 `use_skill` 加载统一的 `yida-formula`，查看语法、字段配置和完整示例。

## 推荐流程

1. 含字段引用时，先读取目标表单 Schema，确认真实字段 ID、字段类型和子表结构；可以复用当前任务中仍与表单一致的 Schema。
2. 读取已有公式，需要时查询函数参数，再检查公式语法、字段引用和结果类型。
3. 需要确认计算结果时，准备输入样例和期望结果，优先按目标字段试算。
4. 修改并保存后回读配置，再从实际页面、校验或节点入口检查结果。

## 选择操作

| 想知道什么 | 命令 |
| --- | --- |
| 有哪些保存方式，哪些已接入检查器 | `formula contracts --json` |
| 字段保存了什么公式 | `formula inspect APP FORM --json` |
| 函数需要什么参数 | `formula functions APP --name ROUND --json` |
| 字段组件支持哪些值类型 | `formula types APP --component NumberField --json`，组件名从 Schema 读取 |
| 公式写法、参数和字段引用有没有问题 | `formula check`，旧命令 `formula evaluate` 继续做本地检查 |
| 通用表达式接口对这份输入返回什么 | `formula test` |
| 已存字段公式能否正确绑定并得到目标值 | `formula test APP FORM --field 字段ID --data-file data.json --expect JSON` |
| 修改后多组样例是否都正确 | `formula test APP FORM --field 字段ID --cases cases.json` |

## 读取配置和函数

```bash
openyida get-schema APP_XXX FORM_XXX
openyida formula inspect APP_XXX FORM_XXX --field numberField_total --json
openyida formula functions APP_XXX --name ROUND --output metadata.json --json
```

需要本地检查字段引用时，将 `get-schema` 返回的完整 Schema 通过 create_file / Write / file edit tool 保存为任务目录的 `schema.json`，再传给下一节的 `--schema`。例如保存在 `<projectRoot>/.cache/openyida/<任务名>/formula/schema.json`，后续命令使用该文件的实际路径；不使用 shell 重定向或截断输出。

| 操作 | Schema 怎样提供 |
| --- | --- |
| `formula check/evaluate` 检查字段引用 | 手动获取或复用完整 Schema，通过 `--schema` 传入；未提供时，无法确认字段是否存在及其类型 |
| `formula inspect` 读取已存公式 | 命令根据 APP/FORM 自动读取，无需另传 Schema 文件 |
| `formula test` 或 `formula test --field` 试算 | 命令根据 APP/FORM 自动读取；编写候选公式和样例时仍要使用真实字段 ID |
| 只检查常量公式，如 `ROUND(12.345, 2)` | 无字段引用，本地检查可以省略 Schema |

因此，Schema 仍是字段检查和试算的依据；自动读取只是省去手动下载和传文件。公式试算也需要 Schema，CLI 已在命令内读取。

`inspect` 读取字段默认值公式及字段 `validation`；表单级、流程全局、节点和报表公式从各自完整设计配置读取。

函数签名来自当前组织的表达式元数据；可用清单还参考 CLI 自带的函数菜单。目标组件、组织开关和注入变量也会影响实际可用性，查询结果会标明 `consumerAvailabilityVerified: false`。`--output` 创建新快照，使用新文件名保留上次结果。

## 本地检查

```bash
openyida formula check formula.txt --contract field-value --schema schema.json --metadata metadata.json --target-type NumberField --strict --json
```

| `--contract` | 检查的输入 |
| --- | --- |
| `field-value` | 普通字段的取值公式；默认选项 |
| `validation-rule` | 原生校验规则中的公式原文，布尔目标可加 `--target-type Boolean` |
| `business-action` | 业务动作中的公式原文；查询条件和写入效果还需对应入口检查 |
| `node-expression` | 节点公式的执行文本或编辑器原文 |
| `dataset-expression`、`javascript` | 已识别的其他输入类型；当前检查器会明确返回未支持，使用对应编辑器或代码工具检查 |

原 `--context form/validation/business/automation` 继续作为前四种方式的兼容别名。两种参数一起提供时应匹配。这里的选择表示输入格式和参考函数菜单；不代表已模拟整张页面或整条流程。

`--metadata` 更新参考参数和类型；`--schema` 提供真实字段。自定义组件的子属性若只有父组件类型，本地不猜测子属性类型。

### 根据诊断结果修复

从输出的 `diagnostics[].code` 找到对应行，按提示修改。一次可能返回多个诊断：先修括号、引号和标点，再核对字段、函数及类型，最后重新运行检查。

| 诊断码或提示 | 含义与处理 |
| --- | --- |
| `field_ref_not_in_schema` / `field_missing` | 提供的 Schema 中找不到字段。用 `get-schema` 核对目标表单的真实字段 ID；字段有变更时更新本地文件，再检查 |
| `schema_missing` | 缺少字段信息。读取完整 Schema 并传入 `--schema` 后，再确认字段是否存在、类型是否匹配 |
| `bare_identifier` / `field_ref_missing_brace` / `field_ref_unclosed` | 字段引用写法不完整。普通字段写为 `#{numberField_total}`，保留 `#{` 和结尾的 `}` |
| `field_ref_subtable_prefix` | 普通子表字段多写了父表前缀。将 `#{tableField_items.numberField_amount}` 改成真实子字段 ID `#{numberField_amount}` |
| `comparison_operator` / `operator_invalid` | 原生公式用了比较符号等不支持的运算。将 `a > b`、`a >= b`、`a < b`、`a <= b`、`a == b`、`a != b` 分别改为 `GT/GE/LT/LE/EQ/NE(a, b)` |
| `logical_operator` | 原生公式用了 `&&` 或 `\|\|`。分别改为 `AND(条件1, 条件2)` 或 `OR(条件1, 条件2)`；取反用 `NOT(条件)` |
| `fullwidth_punctuation` / `semicolon_argument_separator` | 公式结构中用了中文标点或分号。括号、引号和参数逗号改为英文半角；引号内正常的中文文本保留 |
| `parenthesis_unclosed` / `parenthesis_extra_close` / `string_unclosed` | 括号或引号不成对。逐层补全或移除多余符号；嵌套 IF 同时核对条件、满足值、不满足值三个参数 |
| `syntax_invalid` | 表达式无法解析。按报错位置检查漏写的参数、逗号、括号或引号；先让最内层公式完整，再拼接外层 |
| `function_unknown` / `function_case` | 当前列表中没有该公式函数名，或大小写不符，检查会报错。用 `formula functions APP --json` 查询列表，并核对目标编辑器菜单；逐字照抄名称，保持大小写。更新平台元数据后仍未列出的函数不能自行构造 |
| `argument_count` | 参数数量不对。按查询结果补齐必填参数或去掉多余参数，例如 `ROUND(12.345, 2)` |
| `argument_type` / `same_type` / `target_type` | 参数之间或返回结果与字段类型不匹配。核对原始值；数字文本按需用 `VALUE` 转数字，成员字段使用成员结构，金额字段返回数字 |
| `target_branches` / `numeric_result_text` | IF 分支类型混合，或数值目标可能收到文本。逐个检查分支，让金额分支都返回数字，并分别带样例试算 |
| `date_timestamp` | 日期对象还需转换才能给日期字段赋值。今天可写为 `TIMESTAMP(TODAY())`，再核对页面显示与提交的毫秒时间戳 |
| `reference_context` / `function_context` | 当前公式位置无法使用该引用或函数。核对实际配置位置、可选上游字段和函数；按真实输入选择 `--contract`，不要仅更换检查参数让错误消失 |
| `reference_details_unknown` / `context_unknown` / `target_unknown` | 缺少子属性类型、函数可用范围或目标类型信息。读取对应组件或编辑器配置，信息不足时标明尚未确认 |
| 输入方式未支持 | 使用对应的数据集编辑器或 JavaScript 工具检查，保留实际执行的验证结果 |

原生公式的比较和逻辑修复按上表处理；页面 JavaScript、已编译流程条件按各自格式检查。

例如，同一个金额字段的常见修复：

| 原写法 | 修改后 |
| --- | --- |
| `#{numberField_total} >= 100` | `GE(#{numberField_total}, 100)` |
| `ROUND（#{numberField_total}，2）` | `ROUND(#{numberField_total}, 2)` |
| `IF(GE(#{numberField_total}, 100), "高"` | `IF(GE(#{numberField_total}, 100), "高", "低")` |

上面的 ID 是示例，使用前换成目标表单的真实字段 ID。修复后先重跑本地检查；需要验证结果时，再用正常值、边界值、零和空值试算。完整嵌套与字段配置通过 `use_skill` 加载统一的 `yida-formula` 查看。

`ok: true` 表示本地没有发现错误；`unknown` 表示缺少信息。混合类型分支、日期对象及数值目标中的文本结果会提示进一步试算。`checks.consumerPreprocessing/platform/runtime: not_run` 表示未完成预处理、平台执行和实际运行。`--strict` 在发现错误时返回失败退出码。

## 优先按目标字段试算

```bash
openyida formula test APP_XXX FORM_XXX --field numberField_total --data-file data.json --expect 24.6 --json
openyida formula test APP_XXX FORM_XXX --field numberField_total --cases cases.json --json
```

字段试算读取已保存公式及其依赖，将组件类型、子表行和计算顺序交给平台原生字段计算接口。也可以在 APP/FORM 后提供候选公式，只用于本次试算。完整样例、保存后重试和日期说明由统一的 `yida-formula` 技能提供，按其“字段绑定与样例验证”参考执行。

`--cases` 文件每项包含唯一 `name`、`data` 和 `expect`，单次 1 至 100 项；与 `--data-file/--expect` 分开使用。字段试算的 `--context` 为默认 `form`，省略 `--binding`；原始数据保持组件格式，子字段放入子表行对象。`--timezone-offset` 单位为分钟、向东为正，范围 -840 至 840 的整数，默认 480；仅用于带 `--field` 的试算。

`verification: field-runtime` 表示平台字段计算已调用。`rawValue` 是平台组件绑定后的字段值；`value` 是 CLI 按部分原生回填规则转换后的值。没有预期值时 `assertion: not_requested`；结果缺失、转换为空或只解析出部分数字会明确失败。批量结果保留每个样例名称和失败原因。

试算不保存字段、不提交记录。`widgetFormatting/submission: not_run` 表示字段精度、日期显示、页面事件及提交还需实际验收。依赖公式会重新计算，不把样例中预填的计算结果当成已验证结果。

### 试算失败时怎么处理

| 诊断码或提示 | 处理 |
| --- | --- |
| `missing data: 字段ID` | 在样例中补齐最初的输入字段；子字段放在对应子表的行对象中，计算字段由试算重算 |
| `table rows required` / `table data field` | 核对子表 ID、子字段归属和行数组结构，按统一公式 Skill 的完整子表示例修改 |
| `field_result_missing` | 请求完成但目标字段没有返回值。核对公式依赖、空明细及绑定；空明细要返回零时显式配置 `IF(ISEMPTY(#{子字段ID}), 0, SUM(#{子字段ID}))`，再试算 |
| `target_conversion_empty` / `target_conversion_partial` | 回填转换后为空或只保留了部分数字。检查返回值类型、日期单位及混入的文字，修改公式后重新核对原始值和转换后的值 |
| `assertion: failed` | 实际值与预期不同。同时核对数值和 JSON 类型，如数字 `12.35` 与字符串 `"12.35"`；按业务预期检查公式及样例 |
| 提示需要原生预处理或函数不允许试算 | 使用实际校验或业务动作入口验证；先确认输入与触发方式，不把查询、写入函数替换成普通计算来宣称通过 |

## 调用表达式接口

创建 `data.json`，用真实字段 ID 作为键、样例原始值作为值：

```json
{"numberField_total":12.345}
```

```bash
openyida formula test APP_XXX FORM_XXX 'ROUND(#{numberField_total}, 2)' --data-file data.json --json
```

默认 `--binding platform` 原样提交公式和 `varMap`。命令返回结果及原始类型，并输出本次送出的 `expression`。它不保存公式或提交表单数据，只接受已确认不写业务数据的函数。

需要单独探查“把数字直接写进公式后，接口如何计算”时，可显式使用：

```bash
openyida formula test APP_XXX FORM_XXX 'ROUND(#{numberField_total}, 2)' --data-file data.json --binding numeric-literals --json
```

此模式只将数值样例替换为数字常量，字符串和其他值仍走 `varMap`。这是独立的接口探查方式，不是页面原生取值过程。两种模式结果不同，应继续查真实调用的预处理和字段转换，不能用替换数字掩盖差异。

加 `--expect` 可按 JSON 值和类型核对结果，例如平台返回字符串 `"12.35"` 时使用 `--expect '"12.35"'`。

需要原生预处理的 `EXIST/EQUAL` 在这个入口停止；写数据函数和未知函数也停止。校验、自动化、子表和图表聚合使用各自实际执行入口验证。当前 `test --context` 仅接受 `form/validation`，用于选择参考菜单，不增加对应运行上下文。

## 说明验证范围

分别报告本地检查、原生字段试算或接口探查、配置回读和实际执行。通用接口返回 `verification: expression-endpoint`；字段试算返回 `field-runtime`，批量返回 `field-runtime-cases`。这些结果仍标记 `runtimeVerified: false`，避免把部分试算当成页面、校验、节点或图表的完整验收。

用户要求暂停测试时，保留上述步骤作为后续验收说明，不执行接口探查或实际业务操作。
