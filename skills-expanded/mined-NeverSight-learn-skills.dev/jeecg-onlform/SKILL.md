---
name: jeecg-onlform
description: Use when user asks to create/edit Online form tables, design database tables with form controls, or says "创建Online表单", "创建online表", "新建表单配置", "online表单", "在线表单", "低代码表单", "配置表", "建online表", "online form", "create online form", "add online field". Also triggers when user describes table fields with control types like "需要一个下拉选择字段" or mentions online form requirements like "做一个请假单包含日期选择和用户选择".
---

# JeecgBoot Online 表单 AI 自动生成器

将自然语言的表单需求描述转换为 Online 表单配置 JSON，并通过 API 在 JeecgBoot 系统中自动创建/编辑表单。

> **重要：本 skill 处理「Online 表单」（元数据驱动，运行时 CRUD），不涉及「设计器表单」（desform）。两者是完全独立的表单体系。**

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

## 交互流程

### Step 0: 判断操作类型

| 用户意图关键词 | 操作类型 |
|---------------|---------|
| 创建/新建/做一个/生成 | **新增表单** → Step 1A |
| 加字段/增加字段/修改字段/删除字段/改一下 | **编辑表单** → Step 1B |

### Step 1A: 新增表单 — 解析需求

从用户描述中提取：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 表名 (tableName) | 自动生成 snake_case | `leave_application` |
| 表描述 (tableTxt) | 用户指定 | "请假申请" |
| 表类型 (tableType) | 1=单表 | 提到"主子表"→2/3，提到"树形"→1+isTree |
| 字段列表 | 从描述中解析 | 姓名(必填)、请假天数(数字)、日期(范围查询) |

**判断表类型：**
- 提到"分类/层级/树/上下级" → **树表** (tableType=1, isTree='Y')
- 提到"主子表/明细/一对多/订单+商品" → **主子表** (主表 tableType=2, 子表 tableType=3)
- 默认 → **单表** (tableType=1)

### Step 1B: 编辑表单 — 查询现有配置

1. 用户提供表单 ID 或表名
2. 通过 API 查询现有表单配置：`GET /online/cgform/api/getByHead?id={headId}`
3. 解析现有字段列表，展示给用户
4. 根据用户需求进行增/删/改字段

### Step 2: 智能字段推导

**从用户自然语言描述推导字段配置：**

| 用户描述关键词 | fieldShowType | dbType | dbLength | 说明 |
|---------------|--------------|--------|----------|------|
| 名称/标题/编码/文本 | `text` | string | 100 | 单行文本 |
| 密码 | `password` | string | 32 | 密码框 |
| 备注/描述/说明 | `textarea` | string | 500 | 多行文本 |
| 金额/价格/费用 | `text` | BigDecimal | 10(2) | 数字文本框 |
| 数量/个数/数目 | `text` | int | 9 | 整数文本框 |
| 小数/比率/double | `text` | double | 10(2) | 浮点文本框 |
| 日期/生日/入职日期 | `date` | Date | 0 | 日期选择 |
| 日期时间/下单时间 | `datetime` | Datetime | 0 | 日期时间选择 |
| 时间/几点 | `time` | string | 50 | 时间选择 |
| 年 | `date` + picker=year | Date | 0 | 年选择 |
| 月 | `date` + picker=month | Date | 0 | 月选择 |
| 周 | `date` + picker=week | Date | 0 | 周选择 |
| 季度 | `date` + picker=quarter | Date | 0 | 季度选择 |
| 是否/开关/启用 | `switch` | string | 50 | 开关 |
| 状态/类型/级别 (单选) | `radio` | string | 50 | 字典单选 |
| 下拉/选择/类别 | `list` | string | 50 | 字典下拉 |
| 多选/标签/兴趣 | `checkbox` | string | 200 | 字典多选 |
| 下拉多选 | `list_multi` | string | 250 | 字典下拉多选 |
| 下拉搜索/远程搜索 | `sel_search` | string | 50 | 字典表下拉搜索 |
| 图片/头像/照片 | `image` | string | 500 | 图片上传 |
| 文件/附件 | `file` | string | 500 | 文件上传 |
| 富文本/内容/HTML | `umeditor` | Text | 0 | 富文本编辑器 |
| Markdown | `markdown` | Blob | 0 | Markdown编辑器 |
| 用户/负责人/审批人 | `sel_user` | string | 100 | 用户选择 |
| 部门/组织/所属部门 | `sel_depart` | string | 100 | 部门选择 |
| 省市区/地区/地址 | `pca` | string | 100 | 省市区联动 |
| 分类/分类树/树选择 | `cat_tree` | string | 100 | 分类字典树 |
| 自定义树 | `sel_tree` | string | 255 | 自定义树控件 |
| 弹窗选择/popup | `popup` | string | 100 | Popup弹窗 |
| pop字典 | `popup_dict` | string | 100 | Popup字典 |
| 关联记录/引用 | `link_table` | string | 200 | 关联记录 |
| 他表字段/自动填充 | `link_table_field` | string | 32 | 他表字段(不持久化) |
| 联动下拉/级联 | `link_down` | string | 255 | 联动组件 |

### Step 3: 字典配置推导

**字典数据来源有三种方式，按以下优先级选择：**

#### 方式一：系统字典（dictField 有值，dictTable 为空）
用户提到"字典 sex"、"使用 urgent_level 字典" 等：
```json
{ "dictField": "sex", "dictTable": "", "dictText": "" }
```

#### 方式二：字典表（dictTable 有值）
用户提到"从 sys_user 表取"、"关联部门表"等：
```json
{ "dictTable": "sys_depart", "dictField": "id", "dictText": "depart_name" }
```

#### 方式三：字典表带条件
用户提到"过滤/筛选/where"等：
```json
{ "dictTable": "sys_user where username like '%a%'", "dictField": "username", "dictText": "realname" }
```

**常用 JeecgBoot 系统字典编码：**

| 字典编码 | 说明 | 适用控件 |
|---------|------|---------|
| `sex` | 性别 (1=男, 2=女) | list/radio/checkbox |
| `priority` | 优先级 (L/M/H) | list/radio |
| `valid_status` | 有效状态 (0/1) | list/radio/switch |
| `urgent_level` | 紧急程度 | list/checkbox/list_multi |
| `yn` | 是否 (Y/N) | radio/switch |

### Step 4: 特殊控件配置

#### switch 开关
```json
{
  "fieldShowType": "switch",
  "fieldExtendJson": "[\"Y\",\"N\"]",
  "dictField": "", "dictTable": "", "dictText": ""
}
```

#### date 日期扩展 (年/月/周/季度)
```json
{
  "fieldShowType": "date",
  "fieldExtendJson": "{\"labelLength\":6,\"picker\":\"year\"}"
}
```
picker 可选值: `year`、`month`、`week`、`quarter`

#### popup 弹窗
dictField 和 dictText 成对映射（逗号分隔）：
```json
{
  "fieldShowType": "popup",
  "dictTable": "report_user",
  "dictField": "username,realname",
  "dictText": "popup,popback"
}
```
其中 dictText 的值对应本表接收回填的字段名。

#### sel_tree 自定义树
```json
{
  "fieldShowType": "sel_tree",
  "dictTable": "sys_category",
  "dictField": "0",
  "dictText": "id,pid,name,has_child"
}
```
dictField 填根节点值，dictText 填 `id,pid,显示字段,是否有子节点字段`。

#### link_down 联动下拉
dictTable 填 JSON 配置字符串：
```json
{
  "fieldShowType": "link_down",
  "dictTable": "{\n\ttable: \"sys_category\",\n\ttxt: \"name\",\n\tkey: \"id\",\n\tlinkField: \"field2,field3\",\n\tidField: \"id\",\n\tpidField: \"pid\",\n\tcondition:\"pid = '0'\"\n}",
  "dictField": "", "dictText": ""
}
```

#### link_table 关联记录
```json
{
  "fieldShowType": "link_table",
  "dictTable": "demo_staff",
  "dictField": "id",
  "dictText": "name,age,sex",
  "fieldExtendJson": "{\"showType\":\"card\",\"multiSelect\":false,\"imageField\":\"\"}"
}
```
多选带图片：`{"showType":"card","multiSelect":true,"imageField":"top_pic"}`

#### link_table_field 他表字段
```json
{
  "fieldShowType": "link_table_field",
  "dictTable": "guanljil",
  "dictField": "",
  "dictText": "name",
  "dbIsPersist": 0
}
```
dictTable 填本表中 link_table 控件的字段名（不是数据库表名）。`dbIsPersist=0` 表示不持久化到数据库。

#### popup_dict Pop字典
```json
{
  "fieldShowType": "popup_dict",
  "dictTable": "report_user",
  "dictField": "id",
  "dictText": "realname"
}
```

### Step 5: 展示摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

**重要：必须明确展示 6 个标准系统字段 + 业务字段，让用户清楚看到完整表结构！**

```
## Online 表单配置摘要

- 表名：leave_application
- 表描述：请假申请表
- 表类型：单表
- 目标环境：https://boot3.jeecg.com/jeecgboot

### 标准系统字段（6个，每个Online表必须包含）

| 序号 | 字段名 | 标签 | DB类型 | 说明 |
|------|--------|------|--------|------|
| 1 | id | 主键 | string(36) | 主键，自动生成 |
| 2 | create_by | 创建人 | string(50) | 系统自动填充 |
| 3 | create_time | 创建时间 | Datetime | 系统自动填充 |
| 4 | update_by | 更新人 | string(50) | 系统自动填充 |
| 5 | update_time | 更新时间 | Datetime | 系统自动填充 |
| 6 | sys_org_code | 所属部门 | string(50) | 系统自动填充 |

### 业务字段（N个）

| 序号 | 字段名 | 标签 | 控件类型 | DB类型 | 必填 | 查询 | 字典 |
|------|--------|------|---------|--------|------|------|------|
| 7 | name | 姓名 | text | string(100) | 是 | 是(模糊) | - |
| 8 | leave_type | 请假类型 | list | string(50) | 是 | 是(精确) | leave_type |
| 9 | start_date | 开始日期 | date | Date | 是 | 是(范围) | - |
| 10 | end_date | 结束日期 | date | Date | 是 | 否 | - |
| 11 | days | 请假天数 | text | int(9) | 是 | 否 | - |
| 12 | reason | 请假原因 | textarea | string(500) | 否 | 否 | - |
| 13 | attachment | 附件 | file | string(500) | 否 | 否 | - |
| 14 | approver | 审批人 | sel_user | string(100) | 否 | 是(精确) | - |

**合计：6 个标准字段 + 8 个业务字段 = 14 个字段**

### 索引

| 索引名 | 字段 | 类型 |
|--------|------|------|
| (无) | | |

确认以上配置？(y/n)
```

### Step 6: 生成配置 JSON 并调用 API

用户确认后，**优先使用持久化脚本** `scripts/onlform_creator.py`（同目录下），只需生成 JSON 配置文件即可完成创建/编辑。

> **重要：优先使用 `scripts/onlform_creator.py` 脚本 + JSON 配置文件的方式，避免每次重头编写 Python 代码。只有当脚本无法满足特殊需求时，才编写自定义脚本。**

#### 6.1 使用持久化脚本（推荐方式）

**脚本位置：** 与本 SKILL.md 同目录下的 `scripts/onlform_creator.py`

**使用步骤：**
1. 根据用户需求生成 JSON 配置文件（Write 到工作目录的临时 `.json` 文件）
2. 用 Bash 执行脚本：`python <skill目录>/scripts/onlform_creator.py --api-base <URL> --token <TOKEN> --config <config.json>`
3. 删除临时 JSON 配置文件

**脚本自动完成：**
- 生成6个系统默认字段 + 业务字段
- 调用 addAll/editAll API
- 查询 headId
- 同步数据库
- 输出菜单 SQL

#### 6.2 JSON 配置文件格式

**单表创建示例：**

```json
{
  "action": "create",
  "tables": [
    {
      "tableName": "leave_application",
      "tableTxt": "请假申请表",
      "tableType": 1,
      "themeTemplate": "normal",
      "fields": [
        {"dbFieldName": "name", "dbFieldTxt": "姓名", "fieldShowType": "text", "dbType": "string", "dbLength": 100, "fieldMustInput": "1", "isQuery": 1},
        {"dbFieldName": "days", "dbFieldTxt": "请假天数", "fieldShowType": "text", "dbType": "int", "dbLength": 9, "fieldMustInput": "1"},
        {"dbFieldName": "reason", "dbFieldTxt": "请假原因", "fieldShowType": "textarea", "dbType": "string", "dbLength": 500}
      ]
    }
  ]
}
```

**主子表创建示例（主表 tableType=2，子表 tableType=3）：**

```json
{
  "action": "create",
  "tables": [
    {
      "tableName": "demo_order_main",
      "tableTxt": "订单主表",
      "tableType": 2,
      "themeTemplate": "erp",
      "subTableStr": "demo_order_product",
      "fields": [
        {"dbFieldName": "order_code", "dbFieldTxt": "订单编号", "fieldShowType": "text", "dbType": "string", "dbLength": 50, "fieldMustInput": "1", "isQuery": 1},
        {"dbFieldName": "order_date", "dbFieldTxt": "下单日期", "fieldShowType": "date", "dbType": "Date", "dbLength": 0, "fieldMustInput": "1", "isQuery": 1, "queryMode": "group"},
        {"dbFieldName": "customer_name", "dbFieldTxt": "客户名称", "fieldShowType": "text", "dbType": "string", "dbLength": 100, "fieldMustInput": "1", "isQuery": 1},
        {"dbFieldName": "total_amount", "dbFieldTxt": "订单总额", "fieldShowType": "text", "dbType": "BigDecimal", "dbLength": 10, "dbPointLength": 2},
        {"dbFieldName": "order_status", "dbFieldTxt": "订单状态", "fieldShowType": "list", "dbType": "string", "dbLength": 50, "fieldMustInput": "1", "isQuery": 1, "dictField": "valid_status"},
        {"dbFieldName": "remark", "dbFieldTxt": "备注", "fieldShowType": "textarea", "dbType": "string", "dbLength": 500}
      ]
    },
    {
      "tableName": "demo_order_product",
      "tableTxt": "订单商品明细",
      "tableType": 3,
      "relationType": 0,
      "tabOrderNum": 1,
      "fields": [
        {"dbFieldName": "order_id", "dbFieldTxt": "订单ID", "fieldShowType": "text", "dbType": "string", "dbLength": 36, "fieldMustInput": "1", "isShowForm": 0, "isShowList": 0, "mainTable": "demo_order_main", "mainField": "id"},
        {"dbFieldName": "product_name", "dbFieldTxt": "商品名称", "fieldShowType": "text", "dbType": "string", "dbLength": 200, "fieldMustInput": "1"},
        {"dbFieldName": "price", "dbFieldTxt": "单价", "fieldShowType": "text", "dbType": "BigDecimal", "dbLength": 10, "dbPointLength": 2, "fieldMustInput": "1"},
        {"dbFieldName": "quantity", "dbFieldTxt": "数量", "fieldShowType": "text", "dbType": "int", "dbLength": 9, "fieldMustInput": "1"},
        {"dbFieldName": "subtotal", "dbFieldTxt": "小计", "fieldShowType": "text", "dbType": "BigDecimal", "dbLength": 10, "dbPointLength": 2}
      ]
    }
  ]
}
```

**树表创建示例：**

```json
{
  "action": "create",
  "tables": [
    {
      "tableName": "product_category",
      "tableTxt": "产品分类",
      "tableType": 1,
      "isTree": "Y",
      "treeParentIdField": "pid",
      "treeIdField": "has_child",
      "treeFieldname": "name",
      "fields": [
        {"dbFieldName": "pid", "dbFieldTxt": "父级ID", "fieldShowType": "text", "dbType": "string", "dbLength": 36, "isShowForm": 0, "isShowList": 0},
        {"dbFieldName": "has_child", "dbFieldTxt": "是否有子节点", "fieldShowType": "text", "dbType": "string", "dbLength": 10, "isShowForm": 0, "isShowList": 0},
        {"dbFieldName": "name", "dbFieldTxt": "分类名称", "fieldShowType": "text", "dbType": "string", "dbLength": 100, "fieldMustInput": "1", "isQuery": 1}
      ]
    }
  ]
}
```

**编辑表单示例：**

```json
{
  "action": "edit",
  "headId": "表单的headId",
  "addFields": [
    {"dbFieldName": "new_field", "dbFieldTxt": "新字段", "fieldShowType": "text", "dbType": "string", "dbLength": 100}
  ],
  "deleteFields": ["old_field_name"],
  "modifyFields": [
    {"dbFieldName": "existing_field", "dbFieldTxt": "修改后的标签", "dbLength": 200}
  ]
}
```

#### 6.3 字段配置属性参考

JSON 配置中每个字段对象支持以下属性（未指定的使用默认值）：

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| dbFieldName | string | **必填** | 字段名(snake_case) |
| dbFieldTxt | string | **必填** | 字段标签 |
| fieldShowType | string | "text" | 控件类型(text/list/radio/date/file等) |
| dbType | string | "string" | 数据库类型(string/int/BigDecimal/Date/Datetime/Text/Blob等) |
| dbLength | int | 100 | 字段长度 |
| dbPointLength | int | 0 | 小数位数 |
| fieldMustInput | string | "0" | 是否必填("1"=是) |
| isQuery | int | 0 | 是否查询(1=是) |
| queryMode | string | "single" | 查询模式(single=精确/模糊, group=范围) |
| isShowForm | int | 1 | 是否在表单中显示 |
| isShowList | int | 1 | 是否在列表中显示 |
| isReadOnly | int | 0 | 是否只读 |
| dictField | string | "" | 字典编码(系统字典) |
| dictTable | string | "" | 字典表名(字典表) |
| dictText | string | "" | 字典显示字段 |
| fieldExtendJson | string | "" | 扩展配置JSON(switch/date picker等) |
| fieldDefaultValue | string | "" | 默认值 |
| fieldValidType | string | "" | 校验规则(m=手机/e=邮箱/n=数字等) |
| fieldLength | int | 120 | 控件宽度 |
| mainTable | string | "" | 主表名(子表外键字段用) |
| mainField | string | "" | 主表关联字段(子表外键字段用) |
| sortFlag | string | "0" | 是否可排序 |
| queryConfigFlag | string | "0" | 是否个性查询 |
| queryShowType | string | null | 个性查询控件类型 |
| queryDictField | string | "" | 个性查询字典编码 |
| queryDefVal | string | "" | 个性查询默认值 |

#### 6.4 回退方案：手动编写 Python 脚本

当 `scripts/onlform_creator.py` 无法满足需求时（如需要特殊的字段联动逻辑、复杂的条件判断等），才手动编写 Python 脚本。

**重要限制：**
1. **Windows 环境下 curl 发送中文/长JSON会出错**，必须使用 Python
2. **禁止使用 `python3 -c "..."` 内联方式**
3. **必须先用 Write 工具写入 `.py` 临时文件，再用 Bash 执行，最后删除临时文件**

手动编写时可参考 `scripts/onlform_creator.py` 中的 `make_system_fields()`、`make_field()`、`api_request()` 等函数实现。

### Step 7: 输出结果

**创建成功后，脚本会自动执行以下操作：**
1. 调用 addAll 创建表单配置
2. 查询刚创建的表单获取 headId
3. 调用同步数据库 API：`GET /online/cgform/api/doDbSynch/{headId}/normal`
4. 输出菜单 SQL
5. **本地环境自动执行菜单 SQL**：如果 API_BASE 以 `http://127.0.0.1` 或 `http://localhost` 开头，自动通过 MySQL 执行菜单升级 SQL（见下方规则）

```
## Online 表单创建成功

- 表名：{tableName}
- 表描述：{tableTxt}
- 表类型：{单表/主子表/树表}
- 字段数量：{N} 个业务字段 + 6 个系统字段
- 目标环境：{API_BASE}
- 数据库同步：已完成 ✓
- 菜单 SQL：{已自动执行 ✓ / 需手动执行}

### 菜单 SQL
INSERT INTO sys_permission(id, parent_id, name, url, component, component_name, redirect, menu_type, perms, perms_type, sort_no, always_show, icon, is_route, is_leaf, keep_alive, hidden, hide_tab, description, status, del_flag, rule_flag, create_by, create_time, update_by, update_time, internal_or_external)
VALUES ('{menuId}', NULL, '{tableTxt}', '/online/cgformList/{headId}', '1', 'OnlineAutoList', NULL, 0, NULL, '1', 0.00, 0, NULL, 0, 1, 0, 0, 0, NULL, '1', 0, 0, 'admin', now(), NULL, NULL, 0);

### 后续操作
1. 点击「功能测试」预览表单效果
2. 如菜单未自动执行，手动执行上方 SQL 或在后台手动「添加菜单」
```

### 同步数据库 API 说明

```
POST /online/cgform/api/doDbSynch/{headId}/{syncType}
```

| 参数 | 说明 |
|------|------|
| headId | 表单配置的 ID（从 addAll 后查询获得） |
| syncType | `normal` = 普通同步, `force` = 强制同步（会删除已有表重建） |

### 本地环境自动执行菜单 SQL 规则

**判断条件：** API_BASE 以 `http://127.0.0.1` 或 `http://localhost` 开头（不区分大小写）。

**自动执行方式：** 在 Python 脚本中生成菜单 SQL 后，通过 Bash 工具执行 MySQL 命令：

```bash
mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3 -e "INSERT INTO sys_permission(...) VALUES (...);"
```

**注意事项：**
- 执行前先检查菜单是否已存在：`SELECT id FROM sys_permission WHERE id='{menuId}'`，避免重复插入
- 如果 MySQL 执行失败，回退为输出 SQL 让用户手动执行，不要中断整体流程
- 数据库连接参数默认 `mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3`，与 jeecg-codegen 保持一致

### 菜单 SQL 说明

| 字段 | 值 | 说明 |
|------|-----|------|
| url | `/online/cgformList/{headId}` | Online 表单列表页路由 |
| component | `1` | 固定值，表示 Online 组件 |
| component_name | `OnlineAutoList` | 固定值 |
| menu_type | `0` | 0=菜单 |
| is_route | `0` | 0=不路由（Online组件特殊处理） |
| is_leaf | `1` | 1=叶子节点 |

---

## 主子表创建流程

使用 `scripts/onlform_creator.py` 创建主子表，只需在 JSON 配置的 `tables` 数组中按顺序定义主表和子表即可。脚本会自动依次创建并同步数据库。

### 关键配置要点

1. **主表**：`tableType=2`，`subTableStr` 填子表名（多个用逗号分隔）
2. **子表**：`tableType=3`，必须设置 `relationType`(0=一对多/1=一对一) 和 `tabOrderNum`(排序号)
3. **子表外键字段**：必须包含关联主表的字段，设置 `mainTable` 和 `mainField`，且 `isShowForm=0, isShowList=0`
4. **tables 数组顺序**：主表在前，子表在后（脚本按顺序创建）

完整 JSON 配置示例见上方 Step 6.2 中的「主子表创建示例」。

### 主题模板说明

| themeTemplate | 说明 | 适用场景 |
|--------------|------|---------|
| `normal` | 默认主题 | 子表少、字段少 |
| `tab` | TAB页签 | 多个子表 |
| `erp` | ERP风格 | 上方主表+下方明细 |
| `innerTable` | 内嵌子表 | 子表行内编辑 |

---

## 树表创建

使用 `scripts/onlform_creator.py` 创建树表，在表配置中设置 `isTree: "Y"` 及相关树字段即可。

### 关键配置要点

1. `tableType=1`，`isTree="Y"`
2. 必须设置 `treeParentIdField`(父ID字段)、`treeIdField`(是否有子节点字段)、`treeFieldname`(树展示字段)
3. 字段中必须包含 `pid` 和 `has_child` 字段（隐藏，不在表单和列表中显示）

完整 JSON 配置示例见上方 Step 6.2 中的「树表创建示例」。

---

## 查询配置

### 基础查询 (isQuery + queryMode)
| queryMode | 说明 | 适用控件 |
|-----------|------|---------|
| `single` | 精确/模糊匹配 | text, list, radio, sel_search 等 |
| `group` | 范围查询 | date, datetime, time |

### 个性查询 (queryConfigFlag='1')
用于覆盖默认的查询控件和字典：
```python
make_field(6, 'status', '状态', 'text', 'string', 50,
           is_query=1, query_mode='single')
# 然后手动添加个性查询配置：
fields[-1]['queryConfigFlag'] = '1'
fields[-1]['queryShowType'] = 'list'
fields[-1]['queryDictField'] = 'sex'
fields[-1]['queryDefVal'] = '1'
```

---

## 索引配置

```python
indexs = [
    {
        "id": rand_id("idx"),
        "indexName": "idx_unique_code",
        "indexField": "code",
        "indexType": "unique"
    },
    {
        "id": rand_id("idx"),
        "indexName": "idx_status",
        "indexField": "status",
        "indexType": "normal"
    }
]
```

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `数据库表[xxx]已存在` | 表已存在，需从数据库导入或使用 editAll |
| `附表必须选择映射关系！` | tableType=3 时必须设置 relationType |
| `附表必须填写排序序号！` | tableType=3 时必须设置 tabOrderNum |
| `未找到对应实体` | editAll 时 head.id 不正确 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |

## 参考文档

- `scripts/onlform_creator.py` — **可复用的创建/编辑工具脚本**，优先使用此脚本 + JSON 配置文件
- `references/onlform-api-reference.md` — 完整 JSON 数据结构和字段枚举（手动编写脚本时参考）
