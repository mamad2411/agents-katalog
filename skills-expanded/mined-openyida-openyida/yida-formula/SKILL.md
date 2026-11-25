---
name: yida-formula
description: 宜搭公式编写与配置指南，包含常用函数速查、语法规则、字段 Schema 配置和完整嵌套示例。适用于自动计算、明细汇总、默认值、提交校验、节点筛选和报表计算；支持检查公式错误、用样例核对计算结果。
---

# 配置宜搭公式

先说明想得到什么结果，例如“单价乘数量，保留两位小数”“提交时提醒编号重复”“按上一步的金额筛选记录”。再读取已有配置，确定输入数据和结果存放位置。

公式写法、嵌套、字段引用、空值和类型转换统一在这里维护。对应的业务技能提供真实字段、输入数据和结果保存位置。同样的表达式与执行方式共用规则；需要适配哪些差异，由实际输入、保存结构和执行调用决定，不按页面名称另分一套公式能力。

## 先取得真实表单和字段 ID

配置前读取目标表单的 Schema 或创建结果，使用其中返回的真实标识：

| 标识 | 从哪里取得、用在哪里 |
| --- | --- |
| 表单 ID `formUuid` | 使用目标表单真实的 `FORM-...`，用于 CLI 的 FORM 参数；从已有应用页面、资源查询或创建结果取得 |
| 字段 ID `fieldId` | 使用目标表单组件的 `props.fieldId`，公式引用写成 `#{真实fieldId}`；字段映射中的 `fieldId` 也来自这里 |

```bash
openyida get-schema APP_XXX FORM_XXX --field-map-json
```

本文的 `APP_XXX`、`FORM_XXX`、`numberField_price` 等都是示例占位符，执行和保存前全部替换为实际值。字段显示名称、组件树节点的 `id`、自己拼出的前缀都不能代替 `props.fieldId`。新字段先创建，再读取返回的真实 ID；字段缺失或归属不清时，先定位并确认目标表单和子表，再继续配置。`UUID()` 只生成业务值，不生成宜搭的表单或字段 ID。

本地检查字段引用时传入完整真实 Schema：`formula check formula.txt --schema schema.json --strict`；没有 Schema 时，检查结果不能证明字段存在。普通子表字段也引用它自身的真实 `fieldId`，组件子属性则保留设计器提供的有效路径。

## 公式函数名按列表原样填写

宜搭公式中的函数名必须逐字照抄可用函数列表，保持大小写不变。例如 `SUM`、`ROUND`、`UserBuilder`；`sum`、`Round`、`USERBUILDER` 都不等同于这些名称。只使用目标配置提供的公式函数，不自行改名、缩写、翻译或新增函数，也不照搬其他工具中的同名函数。需要复杂计算时，组合列表中已有的函数，并按其参数说明填写。

先用 `formula functions APP_XXX --output metadata.json --json` 读取函数名称和参数，再核对目标编辑器的可用列表。保存前运行 `formula check formula.txt --metadata metadata.json --strict`，修正大小写不符、列表外函数等错误后再保存；未提供元数据文件时使用 CLI 内置参考列表。函数名写在引号内只是普通文本。页面 JavaScript 的自定义函数按代码规则处理，不能当作公式内置函数使用。

## 按公式的作用选择配置说明

按公式要完成的动作和结果保存位置选择下面的说明。字段名称和业务名称可以不同：只要目标字段支持公式，自动计算或填写字段值都适用第一行；检查字段值或字段之间的关系适用第二行。具体字段和业务例子见后面的示例。

| 需要的能力 | 要配置的内容 | 阅读说明 |
| --- | --- | --- |
| 根据输入、其他字段或系统信息，自动计算或填写字段值 | 普通字段的默认值公式，包括子表同行计算和主表汇总 | [字段取值与完整配置](references/field-values.md) |
| 检查字段值或多个字段之间的关系，判断是否允许提交 | 校验公式、提示文字和阻断方式 | [校验、动作及其他表达式](references/expression-formats.md) |
| 在节点中按条件筛选数据、决定分支或计算赋值 | 节点表达式和可供选择的上游字段 | [节点表达式](references/automation-formulas.md) |
| 通过公式执行数据查询、新增、修改或删除操作 | 业务动作及触发时机 | [表达式保存方式](references/expression-formats.md)，配合 `yida-business-rule` |
| 在数据集或报表中计算字段值、汇总结果 | 数据集表达式、数据类型和汇总方式 | [表达式保存方式](references/expression-formats.md)，配合 `yida-report` |
| 在页面代码或自定义校验代码中编写计算和判断 | JavaScript 表达式或回调函数 | [表达式保存方式](references/expression-formats.md)，配合原页面或表单技能 |

表单中的普通字段配置也适用于流程表单中的同类字段。节点公式用于哪些设计器，以目标节点实际提供的输入为准。自定义页面上的原生组件若暴露相同公式属性，可以沿用相同方法；页面代码里的计算则按 JavaScript 处理。

## 字段公式和字段联动怎么选

字段公式可以实现计算联动：在表单编辑时，依赖字段变化会触发重新计算。例如合计字段配置 `SUM(#{numberField_a}, #{numberField_b})`，两个输入分别为 10 和 20 时合计为 30；修改输入后重新计算。字段 ID 使用目标表单的真实值。

| 需要的效果 | 优先使用 |
| --- | --- |
| 根据字段值求和、计算、拼接或转换，得到另一个字段值 | 字段公式；子表同行计算和主表汇总同样适用 |
| 字段变化时执行指定赋值、显示隐藏或只读操作 | 通过 `use_skill` 加载 `yida-create-form-page`，使用 `create-form rule`；其中计算表达式采用 JavaScript |
| 提交后处理其他记录、通知或流程 | 对应业务规则、自动化或流程能力，并明确触发时机 |

已有事件联动也可以计算赋值；修改前先核对触发字段、执行时机和空值处理，再决定是否换成公式。平台默认值中的“数据联动”还有按条件取数回填的配置，按其实际结构处理。同表字段计算可直接配置在表单中，无需等到提交后再算。

## 字段 Schema 中怎样保存公式

宜搭的字段计算使用普通组件，例如 `NumberField`、`TextField`、`DateField`、`EmployeeField`，无需创建独立的“公式字段”组件。公式配置在组件的 `props` 中：

| 属性 | 应填写的内容 |
| --- | --- |
| `valueType` | `"formula"`，表示使用公式取值 |
| `formula` | 公式字符串 |
| `complexValue` | `{"complexType":"formula","formula":"同一公式字符串"}` |

例如，数值字段的 `props` 中保存：

```json
{
  "valueType": "formula",
  "formula": "ROUND(#{numberField_price} * #{numberField_qty}, 2)",
  "complexValue": {
    "complexType": "formula",
    "formula": "ROUND(#{numberField_price} * #{numberField_qty}, 2)"
  }
}
```

两处公式保持一致。使用 `create-form create/update` 时可以只提供 `formula`，CLI 会同步这三个属性。修改已有字段时保留其他属性；流水号的专用公式对象按流水号配置处理。完整创建、更新、恢复手动输入及子表示例见 [字段取值与完整配置](references/field-values.md)。校验和节点表达式按各自保存结构配置，不直接套用字段默认值的三个属性。

## 公式语法速查

以下规则用于原生公式原文；页面 JavaScript、数据集表达式和已编译的流程条件，按其实际输入格式处理。

| 规则 | 正确写法或说明 |
| --- | --- |
| 字段用真实 ID，并包在 `#{}` 中 | `ROUND(#{numberField_price} * #{numberField_qty}, 2)`；不要直接写裸 ID 或显示名称 |
| 普通子表字段使用子字段自身 ID | `SUM(#{numberField_lineAmount})`；当前行计算与整列汇总由绑定位置决定。组件子属性保留设计器提供的路径 |
| 使用半角括号、逗号和引号 | `IF(GT(#{numberField_total}, 100), "高", "低")` |
| 函数名保持原有大小写 | `ROUND`、`UserBuilder`、`DeptBuilder`；按函数清单填写 |
| 文本加引号，数字直接写 | `"通过"`、`100`；写进 JSON 字符串时，内部双引号写为 `\"` |
| 加减乘除使用 `+ - * /` | 先算的部分加括号；除法先处理零和空值，完整示例见下表 |
| 比较和逻辑使用函数 | `GT/GE/LT/LE/EQ/NE`、`AND/OR/NOT`；例如 `AND(GE(#{numberField_score}, 60), NE(#{textField_status}, "作废"))` |
| 嵌套时写全每个函数的参数 | `IF(条件, 满足时的值, 不满足时的值)`；内外层括号配对，两个返回分支都匹配目标类型 |
| 区分数字、文本、日期和数组 | `VALUE("12.5")` 得到数字；`TEXT` 用于格式化文本；日期对象填日期字段用 `TIMESTAMP`；成员值保留成员结构 |
| 避免循环依赖 | 允许“单价、数量 → 行金额 → 合计”，不要让合计反过来依赖自己；显示状态、计算和是否提交分别配置 |

## 按用途找函数

| 要做什么 | 常用函数名 |
| --- | --- |
| 数值计算 | `SUM`、`AVERAGE`、`MAX`、`MIN`、`ROUND`、`INT`、`ABS`、`MOD`、`PRODUCT`、`SUMPRODUCT`、`SQRT`、`POWER` |
| 判断与校验 | `IF`、`AND`、`OR`、`NOT`、`EQ`、`NE`、`GT`、`GE`、`LT`、`LE`、`ISEMPTY`、`EXACT`、`ARRAYREPEATED` |
| 文本处理 | `CONCATENATE`、`LEFT`、`RIGHT`、`MID`、`LEN`、`TRIM`、`UPPER`、`LOWER`、`REPLACE`、`TEXT`、`VALUE`、`UUID`、`RMBFORMAT`、`SPLIT`、`ARRAYGET` |
| 日期与时间 | `TODAY`、`NOW`、`YEAR`、`MONTH`、`DAY`、`DAYS`、`DATEDELTA`、`NETWORKDAYS`、`DATE`、`TIMESTAMP`、`CASCADEDATEINTERVAL`、`TIMECOMPARE` |
| 人员与部门 | `USER`、`GETUSERNAME`、`LOGINUSERWORKNO`、`DEPTNAME`、`DIRECTOR`、`UserBuilder`、`DeptBuilder`、`DirectorBuilder` |
| 多选集合 | `UNIONSET`、`INTERSECTIONSET`、`DIFFERENCESET`、`SUBSET` |
| 查已有记录或执行数据动作 | `EXIST`、`COUNT`、`INSERT`、`UPDATE`、`DELETE` 等；先确认表单上下文、预处理和触发时机 |

参数写法、返回值、完整分类名单和例子见 [公式函数速查](../../references/formula-functions.md)。查询当前组织的函数签名后，再核对目标配置实际提供的函数清单；索引中的函数不保证在每个输入位置都可用。

## 写配置前先处理这些易错点

按当前任务读取下表相关项，再写字段、规则或节点配置。相同用法在不同设计器中共用这些步骤。

| 正在做什么 | 先做这一步 |
| --- | --- |
| 修改已有公式 | 读取目标位置的完整配置，保留规则 ID、其他公式、提示、触发时机和无关属性；`formula inspect` 只覆盖字段配置 |
| 引用同表新字段 | 创建基础字段后复用返回的真实字段映射，再添加计算；已有字段直接读取映射，无需重新创建 |
| 获取数据时设置过滤条件 | 左边选目标表字段；右边明确选“值、字段、公式”：固定门槛用值，上游金额用字段，上游金额乘二用公式 |
| 引用子表字段 | 使用子字段自身的 ID，并明确取当前行还是整列；主表汇总和子表同行计算分别配置 |
| 避免循环依赖 | 目标字段的公式不引用自身，同时检查 A→B→A 等间接循环；把计算整理成“输入字段 → 中间结果 → 最终结果” |
| 隐藏计算字段 | 分别核对显示、计算依赖和提交策略；需要隐藏后仍提交时检查 `submittable: ALWAYS`，再验证实际计算与提交值 |
| 比较日期 | 使用兼容类型的日期比较函数，统一秒/毫秒、时区及按天或时刻的精度；日期可以直接判断，无需一律转文本 |
| 保存节点公式 | 同时保留执行文本、编辑器原文和显示文字；上游节点及输出字段应真实存在，才能再次打开编辑 |
| 配置校验 | 先确认返回值含义：原生阻断公式为真时阻断；JS 自定义校验返回真时通过。提示文字与判断条件一起保存 |
| 处理空值、零、日期或成员 | 保留原始类型和结构；分别考虑空值与零、日期单位、单个成员与成员数组，避免用统一转文本或默认值替代 |
| 给日期字段自动填今天 | 使用 `TIMESTAMP(TODAY())`，把日期对象转换为字段需要的毫秒时间戳；再核对页面显示和提交值 |
| 选择函数 | 查询参数并核对目标配置提供的菜单；`EXIST` 查已有记录，`COUNT` 统计表单提交数，各按真实用途选择 |
| 用公式新增、修改或删除记录 | 通过 `use_skill` 加载 `yida-business-rule` 或对应自动化技能，配置目标记录和触发时机；普通字段计算不执行数据写入 |
| 本地通过或保存成功 | 分别记录检查、保存回读和实际运行结果；接口探查未覆盖的页面联动、提交校验、节点上下文及聚合保持待验证 |
| 试算字段公式 | 使用 `formula test APP FORM --field 目标字段ID --data-file data.json --expect JSON`；直接读取已存公式，按依赖顺序重算，并核对转换前后的值 |
| 公式依赖其他计算字段 | 提供最初的输入数据；试算会先计算依赖字段，再计算结果。子表数据按“表 ID → 多行对象”提供，每行使用子字段 ID |

用户已要求暂停测试时，完成配置说明和本地修改，并注明实际运行尚未验证；保留后续验收步骤即可。

## 共用步骤

1. 读取已有配置，确认真实字段 ID、输入类型、目标值类型，以及什么时候执行。修改时保留原公式和其他设置。
2. 选择函数并写公式，先用一句话说明结果。共用例子见 [常用函数](../../references/formula-functions.md)。
3. 按目标输入的格式保存。字段公式保存字符串；节点公式通常还保存编辑器内容；校验还需要提示和阻断设置。
4. 回读配置，核对字段、公式和原有属性。用户要求验证时，再用实际入口检查计算、提交或节点执行结果。

```bash
openyida get-schema APP_XXX FORM_XXX --field-map-json
openyida formula inspect APP_XXX FORM_XXX --json
openyida formula functions APP_XXX --name ROUND --json
openyida formula types APP_XXX --component NumberField --json
openyida formula contracts --json
```

`inspect` 查看字段默认值公式和字段校验；完整表单校验、流程全局规则、节点和报表配置从各自的完整设计数据读取。`contracts` 列出 CLI 识别的保存方式与检查范围，不访问应用。

`types` 查询组件支持的值类型；省略 `--component` 可列出全部映射。读取 Schema 中的 `componentName` 后再查询，不从字段名猜类型。函数的参数和返回类型来自 `functions`，字段组件的兼容类型来自 `types`；两边匹配后仍需核对实际值及回填转换，详见 [组件、参数与结果类型](references/field-values.md#组件参数与结果类型)。

## 复杂配置先选一个完整示例

需要嵌套时，先选下表对应示例，保留其外层结构，再替换真实字段和业务常量。每例都说明配置位置、替换项和输入对应的预期结果；只读取需要的小节。

| 需要配置什么 | 直接读取 |
| --- | --- |
| 三档判断、多个 IF | [嵌套 IF 与完整字段变更](references/nested-examples.md#三档判断嵌套-if) |
| A 且（B 或 C）、取反 | [AND/OR/NOT 嵌套](references/nested-examples.md#多层条件andornot) |
| 数量为零时避免除零 | [非零除数与完整字段变更](references/nested-examples.md#数量为零让除数始终非零) |
| 子表同行计算后主表汇总 | [两个目标字段的完整变更](references/field-values.md#子表同行计算与主表汇总的完整变更) |
| 同时使用字段、公式、固定值过滤 | [完整取数 spec](references/node-examples.md#按编号字段嵌套公式和固定状态取数) |
| 分支命中后再分支 | [两层 route 与兜底](references/node-examples.md#嵌套分支先决定是否复核再决定级别) |
| 复杂提交校验 | [同一规则的原生公式与 JS 配置](references/nested-examples.md#同一提交规则原生阻断公式与-js-通过条件) |

## 常用写法

下面用字段默认值公式举例，字段 ID 换成读取到的真实值：

| 目的 | 公式 |
| --- | --- |
| 单价乘数量，保留两位小数 | `ROUND(#{numberField_price} * #{numberField_qty}, 2)` |
| 金额超过 100 显示“高” | `IF(GT(#{numberField_total}, 100), "高", "低")` |
| 汇总子表金额列 | `SUM(#{numberField_lineAmount})` |
| 成员字段填当前登录人 | `USER()` |
| 文本字段填当前登录人昵称 | `GETUSERNAME()` |
| 文本字段填当前登录人的部门名称 | `DEPTNAME(LOGINUSERWORKNO())` |
| 拼接姓名和编号 | `CONCATENATE(#{textField_name}, "-", #{textField_code})` |
| 空备注显示默认文本 | `IF(ISEMPTY(#{textField_remark}), "无备注", #{textField_remark})`；配置在另一个输出字段，避免引用自身 |
| 生成业务编号字符串 | `UUID()`；用于业务字段的值，不能代替真实表单或字段 ID |

## 检查结果怎么看

```bash
openyida formula check formula.txt --contract field-value --schema schema.json --target-type NumberField --json
```

本地检查帮助找出写法、参数和部分类型问题。`formula functions` 查询函数签名；实际可选函数还取决于目标配置传入的函数清单和组织开关。

`formula test --field` 使用平台原生字段计算接口，保留组件类型、子表行和公式依赖，并检查数值、日期及成员的部分回填转换。复杂试算、样例文件和返回值说明见 [字段绑定与样例验证](references/runtime-examples.md)。多组输入可保存成 `--cases` 文件，每组都给出期望结果。

不带 `--field` 的 `formula test` 继续探查通用表达式接口。字段试算也需要补页面显示、组件精度和提交检查；原生校验、节点及图表计算仍从各自实际入口验收。详细检查命令见 `yida-formula-evaluate`。

本技能不依赖跨会话 memory。字段映射、原配置和变更文件保存在当前任务目录中。
