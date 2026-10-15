---
name: e-checker
description: |
  Excel配置检查工具，用于验证Excel文件数据是否符合YAML规则定义。使用场景：用户说"检查配置"、"验证Excel"、"检查规则"、"跑一下检查"、"验证数据"，用户想要更新规则文件、修改验证规则、添加新的检查规则，用户询问如何配置规则、某个验证怎么实现、操作符怎么用，涉及Excel数据验证、字段关联检查、跨表引用验证、格式校验等需求；重要约束：如果需求无法通过现有规则实现，必须列出原因，禁止修改validate.py或src/下的检测脚本代码，规则无法实现的情况包括：需要全新的操作符类型、需要修改引擎核心逻辑、需要自定义代码逻辑等
---

# e-checker Excel配置检查工具

基于YAML规则文件的Excel配置检查器，采用V3 Pipeline原子化操作符架构。

## 核心功能

### 1. 检查配置
调用 validate.py 执行Excel数据验证。

**使用方法**：
```bash
# 基本用法（默认查找 checker_rules.yaml）
python validate.py

# 指定规则文件
python validate.py rules.yaml

# 显示详细信息
python validate.py rules.yaml -v

# 列出所有操作符
python validate.py --list-operators
```

### 2. 更新规则文件
根据用户需求生成或修改YAML规则文件。

## YAML规则文件结构

### 基本格式

```yaml
version: "3.0"

# 定义外部数据源（可选）
refs:
  product_ref:
    file: "reference.xlsx"
    sheet: "ProductInfo"
    columns:
      id: "A"
      type: "D"
      level: "F"

# 校验规则
rules:
  - target: "file.xlsx:Sheet.range"
    id: "规则唯一标识"
    description: "规则描述"
    validations:
      - pipeline:
          - 操作符1: 配置
          - 操作符2: 配置
        message: "验证失败时的错误信息"
```

### Target 格式

```yaml
# 完整格式
- target: "data.xlsx:Sheet1.H5:*"

# 简写格式（自动补全 .xlsx）
- target: "data:Sheet2.A5:*"

# 带括号的工作表名
- target: "reference.xlsx:Product(Data).A5:*"

# 文件夹通配符
- target: "data/*.xlsx:Sheet1.A1:*"

# 递归匹配子文件夹
- target: "configs/**/*.xlsx:*.A1:*"
```

### 动态范围支持

使用 `*` 作为结束标记，自动检测数据末尾：

```yaml
rules:
  # 从A5开始，自动找到最后一个非空行
  - target: "file.xlsx:Sheet1.A5:*"
    id: "validate_all"
    validations:
      - pipeline:
          - eq: 1
```

检测逻辑：从起始行向下扫描，遇到连续3个空行后停止。

## 操作符列表

### 操作符类型说明

| 类型 | 说明 |
|------|------|
| SOURCE | 数据源操作符，获取初始数据 |
| TRANSFORM | 转换操作符，对数据进行变换处理 |
| LOOKUP | 查找操作符，跨表/跨文件查询数据 |
| COLLECTION | 集合操作符，处理集合运算 |
| AGGREGATE | 聚合操作符，跨行/跨表聚合数据 |
| VALIDATE | 验证操作符，执行最终验证 |

### SOURCE 类型 - 数据源

| 操作符 | 配置 | 说明 |
|--------|------|------|
| `source` | `{column: "H"}` 或 `"@row.H"` | 从指定列获取源值 |
| `as` | `{name: "var_name"}` 或 `"var_name"` | 保存当前结果到变量 |
| `use` | `"@var_name"` | 使用之前保存的变量 |

### TRANSFORM 类型 - 数据转换

| 操作符 | 配置 | 说明 |
|--------|------|------|
| `split` | `{delimiter: "\|"}` 或 `"\|"` | 按分隔符分割字符串。输入为列表时，对每个元素分割后扁平化 |
| `extract` | `{index: 0}` 或 `0` | 提取列表指定索引元素 |
| `filter` | `{type: "regex", pattern: "^[A-Z]"}` | 过滤数组元素，支持 `regex`/`prefix`/`suffix` |
| `map` | `{operation: "strip"}` 或子pipeline列表 | 列表映射操作，支持 `strip`/`lower`/`upper`/`int`/`float`/`str`，或自定义子pipeline |
| `flatten` | - | 扁平化嵌套列表 |
| `count` | - | 计算元素个数。字符串按分隔符分割后计数，列表直接返回长度 |
| `unique` | - | 去重，保持原有顺序 |
| `math` | `{op: "add", value: 1}` | 数学运算，支持 `add`/`sub`/`mul`/`div`，value 支持变量引用 |
| `round` | `{decimals: 2}` 或 `2` | 四舍五入到指定小数位，默认 0 位（整数） |
| `floor` | - | 向下取整 |
| `ceil` | - | 向上取整 |
| `regex_extract` | `{pattern: "^Item(\d+)$", group: 1}` | 正则捕获组提取。`group: 0` 表示完整匹配，默认 1。输入为列表时，对每个元素处理，不匹配的元素会被过滤 |

### LOOKUP 类型 - 数据查找

| 操作符 | 配置 | 说明 |
|--------|------|------|
| `lookup` | `"ref[id].column"` | 跨表查找，从refs定义的数据源中查找值 |
| `where` | `{ref_source: "ref", match_column: "id", conditions: [...]}` | 条件过滤查找 |
| `get` | `{column: "field"}` | 获取记录属性 |
| `sheet_exists` | `{sheet_pattern: "Sheet({value})"}` | Sheet存在验证 |

#### `sheet_exists` 详细说明

验证指定Sheet是否存在于Excel文件中。支持多个占位符变量和备选文件搜索。

**配置参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sheet_pattern` | string | 是 | - | Sheet名称模式，支持占位符 |
| `search_in` | string | 否 | 当前文件 | 主搜索文件路径 |
| `extra_refs` | array | 否 | `[]` | 备选文件路径列表 |
| `case_sensitive` | boolean | 否 | `false` | 是否区分大小写 |
| `split_by` | string | 否 | - | 分隔符，用于拆分单元格值为多个值 |

**占位符变量**：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{value}` | 当前单元格值 | `Config({value})` → `Config(A)` |
| `{value:lower}` | 当前单元格值（小写） | `Config({value:lower})` → `Config(a)` |
| `{value:upper}` | 当前单元格值（大写） | `Config({value:upper})` → `Config(A)` |
| `{@row.X}` | 同行第X列的值 | `Config({@row.B})` → 使用B列值 |

**使用示例**：

```yaml
# 基础用法：验证 Sheet 存在
- sheet_exists:
    sheet_pattern: "Config({value})"

# 多文件搜索（先搜当前文件，再搜备选文件）
- sheet_exists:
    sheet_pattern: "Level({value})"
    search_in: "main.xlsx"
    extra_refs:
      - "fallback1.xlsx"
      - "fallback2.xlsx"
    case_sensitive: true

# 使用其他列的值
- sheet_exists:
    sheet_pattern: "{value:upper}_{@row.B}"

# 验证多个值（用分隔符拆分）
- sheet_exists:
    sheet_pattern: "Tab({value})"
    split_by: "|"
```

### COLLECTION 类型 - 集合操作

| 操作符 | 配置 | 说明 |
|--------|------|------|
| `union` | `{sources: ["@var1", "@var2"]}` | 集合并集，自动去重，结果排序 |
| `intersect` | `{sources: ["@var1", "@var2"]}` | 集合交集，结果排序 |

### AGGREGATE 类型 - 聚合操作

| 操作符 | 配置 | 说明 |
|--------|------|------|
| `collect` | `{key: "ids", transform: "split:\|"}` | 跨行收集数据。支持 `transform` 转换： `"split:分隔符"`、`"extract:分隔符:索引"` |
| `sequential` | `{prefix: "id", start_from: 1, allow_gap: false}` | 顺序ID验证，检查ID是否按 prefix + number 格式顺序累加 |
| `previous` | `{ref_column: "A", row_offset: 1, allow_empty_first: true}` | 跨行引用验证，验证当前行值是否等于偏移行指定列的值 |
| `no_duplicate` | `{key: "default"}` | 跨行唯一性验证，空值/None 忽略不计 |

### VALIDATE 类型 - 验证操作

| 操作符 | 配置 | 说明 |
|--------|------|------|
| `match_structure` | `{type: "regex", pattern: "^[A-Z]", mode: "each"}` | 结构验证。`mode`: `each`（验证每个元素）或 `single`（整体验证）。支持 `regex`/`prefix`/`suffix` |
| `exists_in` | `"ref.id"` | 存在性验证，验证值是否存在于引用表的指定列中 |
| `eq` | `"@row.D"` 或数值/字符串 | 等于验证 |
| `lt` | `10` 或 `"@row.D"` | 小于验证 |
| `lte` | `10` 或 `"@row.D"` | 小于等于验证 |
| `gt` | `0` 或 `"@row.D"` | 大于验证 |
| `gte` | `0` 或 `"@row.D"` | 大于等于验证 |
| `ne` | `0` 或 `"@row.D"` | 不等于验证 |
| `all` | `[{lt: 10}]` | 全满足验证，验证列表所有元素都满足指定条件 |
| `same` | `"@row.I"` | 真假性一致验证，验证当前值与目标值的真假性（是否为空）相同 |
| `in` | `{values: ["a", "b", "c"]}` 或 `"@list"` | 包含验证，验证值是否在指定列表中 |

## 变量引用语法

| 语法 | 说明 | 示例 |
|------|------|------|
| `@value` | 当前单元格值 | `source: "@value"` |
| `@row.X` | 同行第X列 | `source: "@row.H"` |
| `@var_name` | Pipeline变量 | `use: "@series_h"` |

## 表达式语法

支持 `${...}` 模板语法，可在规则配置中直接使用数学运算、函数调用和变量引用：

| 语法 | 说明 | 示例 |
|------|------|------|
| 数学运算 | `+`, `-`, `*`, `/`, `%`, `**` | `${@row.A + @row.B * 2}` |
| 比较运算 | `==`, `!=`, `<`, `>`, `<=`, `>=` | `${@value >= 100}` |
| 函数调用 | `len()`, `abs()`, `max()`, `min()`, `sum()` | `${max(@row.A, 100)}` |
| 模板字符串 | 字符串插值 | `"ID_${@row.A + 1}"` |

**使用示例**：

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    validations:
      # 数学表达式验证
      - eq: "${@row.Price * 1.1 + 5}"

      # 函数调用
      - validate: "${len(@value) > 0}"

      # 模板字符串动态查找
      - lookup:
          from: "ref.xlsx:Sheet2"
          where: "ID_${@row.B + 1}"
```

## 常见验证场景示例

### 1. 验证数组元素格式

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_item_format"
    validations:
      - pipeline:
          - split: "|"
          - extract:
              delimiter: ":"
              index: 0
          - match_structure:
              type: "regex"
              pattern: "^(ItemA|ItemB|Category)"
              mode: "each"
              message: "商品名必须是ItemA、ItemB或以Category开头"
        message: "格式不正确"
```

### 2. 跨表引用存在性验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_exists"
    validations:
      - pipeline:
          - split: "|"
          - exists_in: "ref_data.id"
        message: "ID不存在于引用表"
```

### 3. 数值范围验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.B1:*"
    id: "check_range"
    validations:
      - pipeline:
          - match_structure:
              type: "regex"
              pattern: "^[0-9]+$"
          - gte: 0
          - lte: 100
        message: "数值必须在0-100之间"
```

### 4. 数组长度验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.C1:*"
    id: "check_length"
    validations:
      - pipeline:
          - split: "|"
          - count
          - gte: 1
          - lte: 10
        message: "数组长度必须在1-10之间"
```

### 5. 顺序ID验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_sequential"
    validations:
      - pipeline:
          - collect: "ids"
          - sequential:
              prefix: "item"
              start_from: 1
              allow_gap: false
        message: "ID必须按顺序累加"
```

### 6. 正则捕获组提取验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_item_number"
    validations:
      - pipeline:
          - regex_extract:
              pattern: "^Item(\d+)$"
              group: 1
          - eq: "${@row.B}"
        message: "Item编号与B列值不匹配"
```

### 7. 跨行唯一性验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_unique_id"
    validations:
      - pipeline:
          - collect: "ids"
          - no_duplicate:
              key: "default"
        message: "ID存在重复"
```

### 8. 集合并集验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_union"
    validations:
      - pipeline:
          - split: "|"
          - as: "list_a"
          - source: "@row.B"
          - split: "|"
          - as: "list_b"
          - union:
              sources: ["@list_a", "@list_b"]
        message: "并集验证失败"
```

### 9. 集合交集验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_intersect"
    validations:
      - pipeline:
          - split: "|"
          - as: "list_a"
          - source: "@row.B"
          - split: "|"
          - as: "list_b"
          - intersect:
              sources: ["@list_a", "@list_b"]
        message: "交集验证失败"
```

### 10. Sheet存在性验证

```yaml
rules:
  - target: "data.xlsx:Sheet1.A1:*"
    id: "check_sheet_exists"
    validations:
      - pipeline:
          - sheet_exists:
              sheet_pattern: "Config({value:upper})"
              search_in: "main.xlsx"
              extra_refs:
                - "fallback.xlsx"
              case_sensitive: false
              split_by: "|"
        message: "对应Sheet不存在"
```

### 11. 复杂嵌套结构验证

验证`bigCoinGuarantee`列的值`"101:2,4|102:2,5|103:2,6"`中，每个范围的上下限都小于`bNum`列的值：

```yaml
rules:
  - target: "file.xlsx:PassNewABCD.F5:*"
    id: "big_coin_guarantee_range_check"
    description: "bigCoinGuarantee中每个范围的上下限必须小于bNum"
    validations:
      - pipeline:
          # 步骤1: 拆分为项目列表
          - split: "|"                      # ["101:2,4", "102:2,5", ...]

          # 步骤2: 对每个项目提取范围部分
          - map:
              - split: ":"                 # → [["101","2,4"], ["102","2,5"], ...]
              - extract: 1                  # → ["2,4", "2,5", ...]
              - split: ","                  # → [["2","4"], ["2","5"], ...]

          # 步骤3: 扁平化
          - flatten                         # ["2","4","2","5", ...]

          # 步骤4: 转数字
          - to_number                       # [2, 4, 2, 5, ...]

          # 步骤5: 验证所有值 < bNum
          - all:
              - lt: "@row.D"                # 都小于 D列(bNum)
```

### 12. 派生集合一致性验证

验证recoverySeries等于First、Forth和RebuyChest元素的series并集：

```yaml
version: "3.0"

refs:
  element_pass_new:
    file: "elementPassNew.xlsx"
    sheet: "element(PassNew)"
    columns:
      id: "A"
      series: "E"
      level: "F"

  element_chest:
    file: "elementPassNew.xlsx"
    sheet: "element(Chest)"
    columns:
      id: "A"
      series: "E"

rules:
  - target: "file.xlsx:PassNewList.G5:*"
    id: "recovery_series_consistency"
    description: "recoveryElementSeries必须是First、Forth和RebuyChest元素的series并集"
    validations:
      - pipeline:
          # 收集H列的series
          - source: "@row.H"
          - split: "|"
          - map:
              - lookup: "element_pass_new[id].series"
          - as: "series_h"

          # 收集I列的series
          - source: "@row.I"
          - split: "|"
          - map:
              - lookup: "element_pass_new[id].series"
          - as: "series_i"

          # 收集L列的series（复合值提取）
          - source: "@row.L"
          - split: "|"
          - map:
              - split: ":"
              - extract: 0
              - lookup: "element_chest[id].series"
          - as: "series_l"

          # 计算并集
          - union: ["@series_h", "@series_i", "@series_l"]
          - unique
          - as: "expected"

          # 获取实际值
          - source: "@value"
          - split: "|"
          - as: "actual"

          # 比较
          - use: "@expected"
          - eq: "@actual"
```

### 13. 跨行引用校验

验证previousPassId等于上一行的id：

```yaml
version: "3.0"

rules:
  - target: "file.xlsx:PassNewList.K5:*"
    id: "previous_pass_id_check"
    validations:
      - pipeline:
          - previous:
              ref_column: "A"
              row_offset: 1
              allow_empty_first: true
```

### 14. 使用表达式语法

使用 `${...}` 表达式语法简化规则：

```yaml
version: "3.0"

rules:
  # 验证数组长度等于指定值+1
  - target: "file.xlsx:Sheet1.J5:*"
    id: "arr_length_check"
    validations:
      - pipeline:
          - source: "@row.J"
          - split: "|"
          - count
          - as: "len_j"
          # 使用表达式：len_j 应该等于 len_h + 1
          - source: "@row.H"
          - split: "|"
          - count
          - as: "len_h"
          - use: "@len_j"
          - eq: "${@len_h + 1}"

  # 数学运算验证
  - target: "file.xlsx:Sheet1.E5:*"
    id: "price_calculation"
    validations:
      - pipeline:
          # 验证：Price * 1.1 + 5 >= MinPrice
          - validate: "${@row.Price * 1.1 + 5 >= @row.MinPrice}"
```

### 15. 文件夹批量验证

```yaml
# 验证 data 文件夹下所有 xlsx 文件的 Sheet1
rules:
  - target: "data/*.xlsx:Sheet1.A1:*"
    validations:
      - pipeline:
          - exists: true
    message: "ID不能为空"

# 递归验证所有子文件夹
rules:
  - target: "configs/**/*.xlsx:*.A1:*"
    validations:
      - pipeline:
          - regex_match: "^\d+$"
    message: "必须是数字"
```

## 重要约束

### 规则无法实现的情况

以下情况无法通过规则实现，必须说明原因：

1. **需要全新的操作符类型** - 如果现有操作符无法组合实现需求
2. **需要修改引擎核心逻辑** - 如修改Pipeline执行流程、添加新的操作符类型分类
3. **需要自定义Python代码** - 如复杂的业务逻辑计算、外部API调用等
4. **需要修改validate.py或src/下的脚本** - 严禁修改检测引擎代码

### 可实现的替代方案

如果需求看似无法实现，考虑以下替代方案：

1. **组合现有操作符** - 大部分复杂验证可以通过多个操作符组合实现
2. **修改数据源** - 在Excel中添加辅助列简化验证逻辑
3. **拆分验证规则** - 将复杂验证拆分为多个简单规则

## 使用步骤

### 检查配置流程

1. 确定要检查的目录和规则文件位置
2. 默认查找 `checker_rules.yaml`，如不存在使用用户指定的规则文件
3. 运行验证命令：`python validate.py [规则文件] [-v]`
4. 解析输出结果，向用户展示错误信息

### 更新规则流程

1. 理解用户的验证需求
2. 判断需求是否可通过现有操作符实现
3. 如无法实现，列出原因并说明约束
4. 如可实现，编写或修改YAML规则文件
5. 验证规则语法正确性

## 关联脚本

本技能包含以下关联脚本：
- `scripts/validate.py` - 主验证脚本
- `scripts/src/` - eChecker 核心代码

使用技能时直接调用 `python scripts/validate.py` 执行验证。
