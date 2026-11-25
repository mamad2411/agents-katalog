---
name: jeecg-onlreport
description: Use when user asks to create/edit Online reports, SQL reports, data reports, or says "创建报表", "生成报表", "新建报表", "做一个报表", "online报表", "SQL报表", "数据报表", "统计报表", "查询报表", "create report", "generate report", "data report". Also triggers when user describes report requirements like "做一个销售统计报表" or mentions SQL-driven data display like "通过SQL查询生成报表".
---

# JeecgBoot Online 报表 AI 自动生成器

将自然语言的报表需求描述转换为 Online 报表配置，并通过 API 在 JeecgBoot 系统中自动创建/编辑报表。

> **重要：本 skill 处理「Online 报表」（SQL 驱动的数据报表），不涉及「Online 表单」（cgform）或「设计器表单」（desform）。**

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
| 创建/新建/做一个/生成报表 | **新增报表** → Step 1A |
| 修改报表/改字段/加字段/删字段 | **编辑报表** → Step 1B |

### Step 1A: 新增报表 — 解析需求

从用户描述中提取：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 报表编码 (code) | 自动生成 snake_case | `sales_report` |
| 报表名称 (name) | 用户指定 | "销售统计报表" |
| SQL 语句 (cgrSql) | 从需求推导或用户提供 | `SELECT ... FROM ...` |
| 数据源 (dbSource) | 空（默认数据源） | `second_db` |

**两种 SQL 来源：**

1. **用户直接提供 SQL** — 直接使用，调用 parseSql 解析字段
2. **用户描述需求，AI 推导 SQL** — 需要用户确认数据库表结构或已知表名

### Step 1B: 编辑报表 — 查询现有配置

1. 用户提供报表 ID 或编码
2. 通过 API 查询现有报表配置：`GET /online/cgreport/head/queryById?id={headId}`
3. 通过 API 查询字段列表：`GET /online/cgreport/item/listByHeadId?cgrheadId={headId}`
4. 通过 API 查询参数列表：`GET /online/cgreport/param/listByHeadId?cgrheadId={headId}`
5. 展示现有配置，根据用户需求进行修改

### Step 2: 调用 parseSql 解析字段

**必须先调用 parseSql 接口获取 SQL 的字段和参数列表：**

```
GET /online/cgreport/head/parseSql?sql={urlEncodedSql}&dbKey={dbKey}
```

- `sql`：URL 编码后的 SQL 语句
- `dbKey`：数据源编码，默认数据源可不传

**实测返回结构（已验证）：**
```json
{
  "success": true,
  "message": "",
  "code": 200,
  "result": {
    "fields": [
      {
        "id": "2032684046700560386",
        "cgrheadId": null,
        "fieldName": "id",
        "fieldTxt": "id",
        "fieldWidth": null,
        "fieldType": "String",
        "searchMode": null,
        "isOrder": null,
        "isSearch": null,
        "dictCode": null,
        "fieldHref": null,
        "isShow": 1,
        "orderNum": 1,
        "replaceVal": null,
        "isTotal": null,
        "createBy": null,
        "createTime": null,
        "updateBy": null,
        "updateTime": null,
        "groupTitle": null
      }
    ],
    "params": []
  },
  "timestamp": 1773464616834
}
```

### Step 3: 智能字段配置

根据字段名和业务语义，AI 自动推导每个字段的配置：

#### 3.1 字段显示名称 (fieldTxt)

parseSql 返回的 fieldTxt 默认等于 fieldName，AI 需要根据语义翻译为中文：

| 字段名模式 | 推导中文名 |
|-----------|-----------|
| id | ID/主键 |
| name / title | 名称/标题 |
| code / no | 编码/编号 |
| status | 状态 |
| type / category | 类型/分类 |
| amount / money / price | 金额/费用/价格 |
| count / qty / num | 数量 |
| date / time | 日期/时间 |
| create_by | 创建人 |
| create_time | 创建时间 |
| update_by | 更新人 |
| update_time | 更新时间 |
| sex | 性别 |
| age | 年龄 |
| email | 邮箱 |
| phone / mobile / tel | 电话/手机号 |
| address | 地址 |
| remark / content / description | 备注/内容/描述 |
| dept / org | 部门/组织 |
| salary | 薪资 |
| birthday | 生日 |

#### 3.2 是否显示 (isShow)

| 规则 | isShow |
|------|--------|
| 业务字段（默认） | 1（显示） |
| id / 主键字段 | 0（隐藏）— 通常不在报表中展示 |
| create_by / update_by | 0（隐藏）— 系统字段 |
| create_time / update_time | 视需求而定 |
| sys_org_code / tenant_id | 0（隐藏）— 系统字段 |

#### 3.3 是否查询 (isSearch) + 查询模式 (searchMode)

| 字段类型 | isSearch | searchMode | 说明 |
|---------|----------|------------|------|
| 名称/标题等文本 | 1 | `like` | 模糊查询 |
| 状态/类型/分类 | 1 | `single` | 精确匹配 |
| 日期/时间 | 1 | `range` | 范围查询（开始~结束） |
| 金额/数量等数值 | 0 | - | 通常不查询 |
| 系统字段 | 0 | - | 不查询 |

#### 3.4 是否排序 (isOrder)

| 规则 | isOrder |
|------|---------|
| 日期/时间字段 | 1 |
| 金额/数量字段 | 1 |
| 其他 | 0 |

#### 3.5 字段类型 (fieldType)

| SQL 列类型 | fieldType |
|-----------|-----------|
| varchar / char / text | String |
| int / tinyint / smallint | Integer |
| bigint | Long |
| decimal / double / float | BigDecimal |
| date | Date |
| datetime / timestamp | Datetime |

> **注意**：parseSql 返回的 fieldType 可能都是 String，AI 应根据字段名语义或用户描述修正。

#### 3.6 字典配置 (dictCode)

支持两种方式：

**方式一：系统字典编码**
```
"dictCode": "sex"
```

**方式二：SQL 字典**
```
"dictCode": "SELECT id as value, name as text FROM sys_category"
```

常用系统字典：

| 字典编码 | 说明 |
|---------|------|
| `sex` | 性别 (1=男, 2=女) |
| `priority` | 优先级 |
| `valid_status` | 有效状态 |
| `urgent_level` | 紧急程度 |
| `yn` | 是否 |

#### 3.7 取值表达式 (replaceVal)

用于将数据库值替换为显示文本（导出时使用）：
```
"replaceVal": "男_1,女_2"
```
格式：`显示文本_数据库值,显示文本_数据库值,...`

#### 3.8 是否合计 (isTotal)

| 规则 | isTotal |
|------|---------|
| 金额/费用/价格字段 | "1"（合计） |
| 数量字段 | "1"（合计） |
| 其他 | "0" 或 null |

#### 3.9 分组表头 (groupTitle)

多个字段可以共用一个分组表头，实现多级表头效果：
```json
{"fieldName": "q1_amount", "groupTitle": "第一季度"},
{"fieldName": "q1_count", "groupTitle": "第一季度"},
{"fieldName": "q2_amount", "groupTitle": "第二季度"},
{"fieldName": "q2_count", "groupTitle": "第二季度"}
```

#### 3.10 字段跳转 (fieldHref)

```
"fieldHref": "/details?id=${id}"
```
支持 `${fieldName}` 变量替换。

### Step 4: SQL 参数配置

SQL 中的 `${paramName}` 会被解析为参数：

```sql
SELECT * FROM sales
WHERE 1=1
${#if($startDate != '')} AND sale_date >= '$startDate' ${#end}
${#if($endDate != '')} AND sale_date <= '$endDate' ${#end}
```

参数配置：

| 属性 | 说明 |
|------|------|
| paramName | 参数名（对应 SQL 中的 ${xxx}） |
| paramTxt | 参数显示名称 |
| paramValue | 默认值（可为空） |
| orderNum | 排序序号 |

### Step 5: 展示摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## Online 报表配置摘要

- 报表编码：sales_report
- 报表名称：销售统计报表
- 数据源：默认
- 目标环境：https://boot3.jeecg.com/jeecgboot

### SQL 语句
SELECT s.id, s.name, s.amount, s.sale_date, s.status
FROM biz_sales s
WHERE 1=1

### 字段配置

| 序号 | 字段名 | 显示名称 | 类型 | 显示 | 查询 | 排序 | 字典 | 合计 |
|------|--------|---------|------|------|------|------|------|------|
| 0 | id | ID | String | 否 | 否 | 否 | - | - |
| 1 | name | 名称 | String | 是 | 是(模糊) | 否 | - | - |
| 2 | amount | 金额 | BigDecimal | 是 | 否 | 是 | - | 是 |
| 3 | sale_date | 销售日期 | Date | 是 | 是(范围) | 是 | - | - |
| 4 | status | 状态 | String | 是 | 是(精确) | 否 | valid_status | - |

### 参数

| 参数名 | 显示名称 | 默认值 |
|--------|---------|--------|
| (无) | | |

确认以上配置？(y/n)
```

### Step 6: 调用 API 创建/编辑报表

用户确认后执行。

#### 6.1 构造请求 JSON

**新增报表 (add)：**

```json
{
  "head": {
    "code": "report_code",
    "name": "报表名称",
    "cgrSql": "SELECT ... FROM ...",
    "dbSource": ""
  },
  "items": [
    {
      "id": "前端生成的长数字ID",
      "cgrheadId": null,
      "fieldName": "field_name",
      "fieldTxt": "显示名称",
      "fieldWidth": null,
      "fieldType": "String",
      "searchMode": null,
      "isOrder": null,
      "isSearch": null,
      "dictCode": null,
      "fieldHref": null,
      "isShow": 1,
      "orderNum": 0,
      "replaceVal": null,
      "isTotal": null,
      "groupTitle": null,
      "createBy": null,
      "createTime": null,
      "updateBy": null,
      "updateTime": null
    }
  ],
  "params": [
    {
      "paramName": "paramName",
      "paramTxt": "参数名称",
      "paramValue": "",
      "orderNum": 1
    }
  ]
}
```

**编辑报表 (editAll)：**

```json
{
  "head": {
    "id": "existing_head_id",
    "code": "report_code",
    "name": "报表名称",
    "cgrSql": "SELECT ... FROM ...",
    "dbSource": ""
  },
  "items": [...],
  "params": [...],
  "deleteItemIds": "item_id1,item_id2",
  "deleteParamIds": "param_id1"
}
```

**字段 ID 生成规则：**
- add 时使用**雪花ID格式**（19位数字字符串），如 `"2032681654277947394"`
- 可用 Python 的 `str(int(time.time() * 1000) * 1000 + random.randint(0, 999))` 近似生成

#### 6.2 使用 Python 调用 API

**重要限制：**
1. **Windows 环境下 curl 发送中文/长 JSON 会出错**，必须使用 Python
2. **禁止使用 `python3 -c "..."` 内联方式**
3. **必须先用 Write 工具写入 `.py` 临时文件，再用 Bash 执行，最后删除临时文件**

**完整 Python 脚本模板（已实测验证通过）：**

以下脚本已在 `https://boot3.jeecg.com/jeecgboot` 环境成功创建报表（2026-03-14 验证）。

```python
import urllib.request
import json
import time
import random
import ssl
import urllib.parse

API_BASE = '{用户提供的后端地址}'
TOKEN = '{用户提供的 X-Access-Token}'

# 忽略SSL验证（开发环境）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def api_request(path, data=None, method=None):
    """发送 API 请求"""
    url = f'{API_BASE}{path}'
    headers = {
        'X-Access-Token': TOKEN,
        'Content-Type': 'application/json; charset=UTF-8'
    }
    if data is not None:
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        if method is None:
            method = 'POST'
        req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    else:
        if method is None:
            method = 'GET'
        req = urllib.request.Request(url, headers=headers, method=method)
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read().decode('utf-8'))

def gen_id():
    """生成雪花ID格式的字符串（19位数字）"""
    return str(int(time.time() * 1000) * 1000000 + random.randint(100000, 999999))

# ====== Step 1: 调用 parseSql 解析字段 ======
sql = "SELECT id, table_name, table_txt, table_type, create_time FROM onl_cgform_head WHERE 1=1"
encoded_sql = urllib.parse.quote(sql, safe='')
parse_result = api_request(f'/online/cgreport/head/parseSql?sql={encoded_sql}')
print('解析结果:', json.dumps(parse_result, ensure_ascii=False, indent=2))

if not parse_result.get('success'):
    print('SQL 解析失败:', parse_result.get('message'))
    exit(1)

# ====== Step 2: 直接构造字段配置（不依赖 parseSql 返回的默认值） ======
# 注意：parseSql 返回的 fieldType 全部是 String，AI 需根据语义修正
# 注意：parseSql 返回的 fieldTxt 等于 fieldName，AI 需翻译为中文
items = [
    {"id": gen_id(), "cgrheadId": None, "fieldName": "id", "fieldTxt": "ID",
     "fieldWidth": None, "fieldType": "String", "searchMode": None, "isOrder": None,
     "isSearch": None, "dictCode": None, "fieldHref": None, "isShow": 0,
     "orderNum": 0, "replaceVal": None, "isTotal": None, "groupTitle": None,
     "createBy": None, "createTime": None, "updateBy": None, "updateTime": None},
    {"id": gen_id(), "cgrheadId": None, "fieldName": "table_name", "fieldTxt": "表名",
     "fieldWidth": None, "fieldType": "String", "searchMode": "like", "isOrder": None,
     "isSearch": 1, "dictCode": None, "fieldHref": None, "isShow": 1,
     "orderNum": 1, "replaceVal": None, "isTotal": None, "groupTitle": None,
     "createBy": None, "createTime": None, "updateBy": None, "updateTime": None},
    # ... 继续添加其他字段 ...
]

# ====== Step 3: 构造请求 ======
report_data = {
    "head": {
        "code": "onl_cgform_list",
        "name": "Online表单清单",
        "cgrSql": sql,
        "dbSource": ""
    },
    "items": items,
    "params": []
}

# ====== Step 4: 调用 add API 创建报表 ======
result = api_request('/online/cgreport/head/add', report_data)
print('创建结果:', json.dumps(result, ensure_ascii=False, indent=2))

if result.get('success'):
    print('\n报表创建成功！')
    # Step 5: 查询报表 ID 并生成菜单 SQL
    list_result = api_request(f'/online/cgreport/head/list?code=onl_cgform_list')
    if list_result.get('success') and list_result['result']['records']:
        head_id = list_result['result']['records'][0]['id']
        print(f'报表 ID: {head_id}')
        print(f'\n菜单 SQL:')
        print(f"INSERT INTO sys_permission (id, parent_id, name, url, component, component_name, is_route, is_leaf, keep_alive, hidden, hide_tab, description, del_flag, rule_flag, status, internal_or_external, perms_type, sort_no, menu_type, route_redirect) VALUES ('{head_id}', NULL, 'Online表单清单', '/online/cgreport/{head_id}', 'modules/online/cgreport/auto/OnlCgreportAutoMain', NULL, 1, 1, 0, 0, 0, NULL, 0, 0, '1', 0, '0', 1.0, 1, NULL);")
else:
    print('\n创建失败:', result.get('message'))
```

### 实测记录（2026-03-14）

**测试场景**：创建 Online 表单清单报表，查询 `onl_cgform_head` 表

**SQL**：
```sql
SELECT id, table_name, table_txt, table_type, table_version, is_tree, is_page, theme_template, create_time, create_by, update_time
FROM onl_cgform_head WHERE 1=1
```

**验证结果**：
1. `parseSql` API 成功解析 11 个字段，所有 fieldType 均返回 String（需 AI 修正）
2. `add` API 成功创建报表，返回 `{"success": true, "message": "添加成功！"}`
3. `head/list` API 成功查询到报表 ID: `2032684085556592641`
4. 菜单 SQL 生成正确

**关键发现**：
- parseSql 返回的 `orderNum` 从 1 开始，但 add 时 items 的 `orderNum` 从 0 开始也能正常工作
- 不需要的字段值（isSearch/isOrder/dictCode 等）传 `null` 即可，不需要传空字符串
- `replaceVal` 格式 `"单表_1,主表_2,附表_3"` 可以替代 dictCode 实现值翻译（导出时有效）
- gen_id() 生成的 19 位数字字符串与前端生成的雪花 ID 格式一致，API 接受

### Step 7: 生成菜单 SQL（可选）

报表创建成功后，需要查询报表 ID 来生成菜单 SQL：

```python
# 查询刚创建的报表
import urllib.parse
list_result = api_request(f'/online/cgreport/head/list?code={urllib.parse.quote(report_code)}')
if list_result.get('success') and list_result['result']['records']:
    head_id = list_result['result']['records'][0]['id']
    report_name = list_result['result']['records'][0]['name']
    print(f'\n报表 ID: {head_id}')
    print(f'\n### 菜单 SQL（可选执行）')
    print(f"""
INSERT INTO sys_permission (
  id, parent_id, name, url, component, component_name,
  is_route, is_leaf, keep_alive, hidden, hide_tab, description,
  del_flag, rule_flag, status, internal_or_external,
  perms_type, sort_no, menu_type, route_redirect
) VALUES (
  '{head_id}', NULL, '{report_name}',
  '/online/cgreport/{head_id}',
  'modules/online/cgreport/auto/OnlCgreportAutoMain',
  NULL,
  1, 1, 0, 0, 0, NULL,
  0, 0, '1', 0,
  '0', 1.0, 1, NULL
);
""")
```

**菜单 SQL 字段说明：**

| 字段 | 值 | 说明 |
|------|-----|------|
| id | 报表 headId | 与报表配置关联 |
| parent_id | NULL | 一级菜单，也可设为某个父菜单 ID |
| name | 报表名称 | 菜单显示名 |
| url | `/online/cgreport/{headId}` | 路由路径 |
| component | `modules/online/cgreport/auto/OnlCgreportAutoMain` | 前端组件 |
| is_route | 1 | 是菜单路由 |
| is_leaf | 1 | 叶子节点 |
| menu_type | 1 | 菜单类型（1=菜单） |

### Step 8: 输出结果

```
## Online 报表创建成功

- 报表编码：{code}
- 报表名称：{name}
- 字段数量：{N} 个
- 参数数量：{M} 个
- 目标环境：{API_BASE}

### 菜单 SQL
INSERT INTO sys_permission (...) VALUES (...);

### 后续操作
1. 打开 JeecgBoot 后台 → Online报表
2. 找到该报表，点击「功能测试」预览效果
3. 如需配置菜单，执行上方 SQL 或在后台手动添加
4. 可在「编辑」中调整字段显示/查询/排序等配置
```

---

## 高级功能

### SQL 参数化查询

支持在 SQL 中使用 Velocity 模板语法的参数：

```sql
SELECT * FROM biz_sales
WHERE 1=1
${#if($startDate != '')} AND sale_date >= '$startDate' ${#end}
${#if($endDate != '')} AND sale_date <= '$endDate' ${#end}
${#if($status != '')} AND status = '$status' ${#end}
```

对应的 params 配置：
```json
[
  {"paramName": "startDate", "paramTxt": "开始日期", "paramValue": "", "orderNum": 1},
  {"paramName": "endDate", "paramTxt": "结束日期", "paramValue": "", "orderNum": 2},
  {"paramName": "status", "paramTxt": "状态", "paramValue": "", "orderNum": 3}
]
```

### 动态数据源

如果用户需要查询非默认数据源的数据：

```json
{
  "head": {
    "code": "ext_report",
    "name": "外部数据报表",
    "cgrSql": "SELECT ...",
    "dbSource": "second_db"
  }
}
```

`dbSource` 对应 JeecgBoot 后台「数据源管理」中配置的数据源编码。

### 字段宽度 (fieldWidth)

控制表格列宽（像素值）：
```json
{"fieldName": "name", "fieldWidth": 200}
{"fieldName": "description", "fieldWidth": 300}
```

---

## 与其他 Skill 的区别

| Skill | 产出物 | 适用场景 |
|-------|--------|---------|
| `jeecg-cgreport` | Online 报表配置（SQL 驱动，只读数据展示） | 数据查询报表、统计分析、数据导出 |
| `jeecg-online` | Online 表单配置（元数据驱动，CRUD） | 数据录入管理表单 |
| `jeecg-codegen` | Java + Vue3 代码 + SQL | 需要自定义业务逻辑的模块 |
| `jeecg-desform` | 设计器表单 JSON | 数据采集、审批表单 |

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `报表编码已存在` | 换一个 code 或使用 editAll 编辑 |
| parseSql 失败 | 检查 SQL 语法是否正确，表是否存在 |
| `SQL注入风险` | 不要在 SQL 中使用 DROP/DELETE/UPDATE 等危险语句 |
| `禁止 select *` | 如果系统开启了 disableSelectAll，需指定具体字段 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |

