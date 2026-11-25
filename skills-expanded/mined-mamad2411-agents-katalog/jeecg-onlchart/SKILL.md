---
name: jeecg-onlchart
description: Use when user asks to create/edit Online graph charts, data visualization, or says "创建图表", "生成图表", "新建图表", "做一个图表", "online图表", "数据图表", "柱状图", "折线图", "饼图", "统计图", "可视化", "chart", "graph", "create chart", "generate chart", "bar chart", "line chart", "pie chart". Also triggers when user describes chart requirements like "做一个销售柱状图" or mentions data visualization like "用图表展示男女比例".
---

# JeecgBoot Online 图表 AI 自动生成器

将自然语言的图表需求描述转换为 Online 图表配置，并通过 API 在 JeecgBoot 系统中自动创建/编辑图表。

> **重要：本 skill 处理「Online 图表」（SQL 驱动的数据可视化图表），不涉及「Online 报表」（cgreport 数据列表）或「Online 表单」（cgform）。**

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

---

## 交互流程

### Step 0: 判断操作类型

| 用户意图关键词 | 操作类型 |
|---------------|---------|
| 创建/新建/做一个/生成图表 | **新增图表** → Step 1A |
| 修改图表/改字段/换图表类型 | **编辑图表** → Step 1B |

### Step 1A: 新增图表 — 解析需求

从用户描述中提取：

| 信息 | 必填 | 默认值 | 示例 |
|------|------|--------|------|
| 图表编码 (code) | 是 | 自动生成 snake_case | `tj_user_sex` |
| 图表名称 (name) | 是 | 用户指定 | "统计男女比例" |
| SQL 语句 (cgrSql) | 是 | 从需求推导或用户提供 | `select count(*) cout, sex from sys_user group by sex` |
| X 轴字段 (xaxisField) | 是 | 从 SQL 推导 | `sex` |
| Y 轴字段 (yaxisField) | 是 | 从 SQL 推导 | `cout` |
| 图表类型 (graphType) | 是 | `bar` | `bar`、`line`、`pie`、`line,bar` |
| 展示模板 (displayTemplate) | 否 | `tab` | `tab`、`single` |
| 数据源 (dbSource) | 否 | 空（默认数据源） | `second_db` |
| 数据类型 (dataType) | 否 | `sql` | `sql` |

**X/Y 轴推导规则：**
- **X 轴 (xaxisField)**：通常是分类/维度字段（如 sex、dept、month、category）
- **Y 轴 (yaxisField)**：通常是度量/聚合字段（如 count、sum、avg 的结果）

### Step 1B: 编辑图表 — 查询现有配置

1. 用户提供图表 ID 或编码
2. 通过 API 查询现有图表配置（参考 API 列表）
3. 展示现有配置，根据用户需求进行修改

### Step 2: 调用 parseSql 解析字段

**复用报表的 parseSql 接口获取 SQL 的字段列表：**

```
GET /online/cgreport/head/parseSql?sql={urlEncodedSql}&dbKey={dbKey}
```

- `sql`：URL 编码后的 SQL 语句
- `dbKey`：数据源编码，默认数据源可不传

**返回结构：**
```json
{
  "success": true,
  "result": {
    "fields": [
      {
        "id": "2033369959277633538",
        "fieldName": "cout",
        "fieldTxt": "cout",
        "fieldType": "String",
        "isShow": 1,
        "orderNum": 1
      }
    ],
    "params": []
  }
}
```

> **注意**：parseSql 返回的 `isShow` 是数字 (0/1)，但图表接口需要字符串 `"Y"/"N"`，需要转换。

### Step 3: 智能字段配置

#### 3.1 字段属性映射（图表 vs 报表的差异）

**关键差异：图表字段使用 `"Y"/"N"` 字符串，而非数字 0/1。**

| 属性 | 图表 (graphreport) | 报表 (cgreport) | 说明 |
|------|-------------------|-----------------|------|
| 关联头ID | `graphreportHeadId` | `cgrheadId` | 字段名不同 |
| 是否显示 | `isShow`: `"Y"/"N"` | `isShow`: 0/1 | 类型不同 |
| 是否合计 | `isTotal`: `"Y"/"N"` | `isTotal`: `"0"/"1"` 或 null | 类型不同 |
| 是否查询 | `searchFlag`: `"Y"/"N"` | `isSearch`: 0/1 | 字段名和类型都不同 |
| 查询模式 | `searchMode` | `searchMode` | 相同 |
| 字典 | `dictCode` | `dictCode` | 相同 |
| 排序 | `orderNum` | `orderNum` | 相同 |

#### 3.2 字段显示名称 (fieldTxt)

parseSql 返回的 fieldTxt 默认等于 fieldName，AI 需要根据语义翻译为中文：

| 字段名模式 | 推导中文名 |
|-----------|-----------|
| count / cout / cnt | 数量/人数/次数 |
| sum / total / amount | 合计/总额 |
| avg / average | 平均值 |
| sex | 性别 |
| dept / department | 部门 |
| status | 状态 |
| type / category | 类型/分类 |
| month / year / date | 月份/年份/日期 |
| name / title | 名称 |
| age | 年龄 |
| salary | 薪资 |

#### 3.3 是否显示 (isShow)

| 规则 | isShow |
|------|--------|
| 所有字段（默认） | `"Y"`（图表通常字段不多，全部显示） |
| id / 主键字段 | `"N"` |

#### 3.4 是否查询 (searchFlag) + 查询模式 (searchMode)

| 字段类型 | searchFlag | searchMode |
|---------|------------|------------|
| 分类/维度字段 | `"Y"` | `single` |
| 日期/时间字段 | `"Y"` | `range` |
| 度量/聚合字段 | `"N"` | null |

#### 3.5 是否合计 (isTotal)

| 规则 | isTotal |
|------|---------|
| 度量/聚合字段 | `"Y"` |
| 维度/分类字段 | `"N"` |

#### 3.6 字典配置 (dictCode)

同报表，支持两种方式：

**方式一：系统字典编码**
```
"dictCode": "sex"
```

**方式二：SQL 字典**
```
"dictCode": "SELECT id as value, name as text FROM sys_category"
```

常用系统字典：`sex`（性别）、`priority`（优先级）、`valid_status`（有效状态）、`yn`（是否）

### Step 4: 图表类型选择

根据数据特征推荐图表类型：

| 数据场景 | 推荐 graphType | 说明 |
|---------|---------------|------|
| 分类对比（如男女人数） | `bar` | 柱状图 |
| 趋势变化（如月度销售） | `line` | 折线图 |
| 占比分布（如部门比例） | `pie` | 饼图 |
| 趋势+对比（如月度销售对比） | `line,bar` | 组合图表 |

**组合图表配置：**
- `graphType`: `"line,bar"`（逗号分隔多种类型）
- `isCombination`: `"combination"`（标记为组合图表）
- 非组合图表 `isCombination` 为 null 或不传

### Step 5: 展示摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## Online 图表配置摘要

- 图表编码：tj_user_sex
- 图表名称：统计男女比例
- 图表类型：bar（柱状图）
- X 轴字段：sex（性别）
- Y 轴字段：cout（人数）
- 数据源：默认
- 目标环境：https://boot3.jeecg.com/jeecgboot

### SQL 语句
select count(*) cout, sex from sys_user group by sex

### 字段配置

| 序号 | 字段名 | 显示名称 | 类型 | 显示 | 查询 | 字典 | 合计 |
|------|--------|---------|------|------|------|------|------|
| 0 | cout | 人数 | String | Y | N | - | Y |
| 1 | sex | 性别 | String | Y | N | sex | N |

### 参数
（无）

确认以上配置？(y/n)
```

### Step 6: 调用 API 创建/编辑图表

用户确认后执行。

#### 6.1 新增图表 — 请求结构

**`POST /online/graphreport/head/add`**

```json
{
    "dbSource": "",
    "name": "统计男女比例",
    "code": "tj_user_sex",
    "displayTemplate": "tab",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "dataType": "sql",
    "graphType": "bar",
    "cgrSql": "select count(*) cout, sex from sys_user group by sex",
    "onlGraphreportItemList": [
        {
            "id": "前端生成的长数字ID",
            "cgrheadId": null,
            "fieldName": "cout",
            "fieldTxt": "人数",
            "fieldWidth": null,
            "fieldType": "String",
            "searchMode": null,
            "isOrder": null,
            "isSearch": null,
            "dictCode": null,
            "fieldHref": null,
            "isShow": "Y",
            "orderNum": 0,
            "replaceVal": null,
            "isTotal": null,
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "groupTitle": null
        }
    ],
    "paramsList": []
}
```

> **注意（add 接口）**：add 时 items 中的关联ID字段名为 `cgrheadId`（值为 null），虽然查询/编辑时返回的是 `graphreportHeadId`。

#### 6.2 编辑图表 — 请求结构

**`PUT /online/graphreport/head/edit`**

```json
{
    "id": "1290934362649460737",
    "name": "统计男女比例",
    "code": "tj_user_bysex",
    "cgrSql": "select count(*) cout, sex from sys_user group by sex",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "yaxisText": "yaxis_text",
    "content": null,
    "extendJs": null,
    "graphType": "line,bar",
    "isCombination": "combination",
    "displayTemplate": "tab",
    "dataType": "sql",
    "dbSource": "",
    "tenantId": 0,
    "lowAppId": null,
    "onlGraphreportItemList": [
        {
            "id": "1290934166687383554",
            "graphreportHeadId": "1290934362649460737",
            "fieldName": "cout",
            "fieldTxt": "人数",
            "isShow": "Y",
            "isTotal": "N",
            "searchFlag": "N",
            "searchMode": null,
            "dictCode": "",
            "fieldHref": null,
            "fieldType": "String",
            "orderNum": 0,
            "replaceVal": null,
            "createBy": "admin",
            "createTime": "2020-08-05 17:03:06",
            "updateBy": null,
            "updateTime": null
        }
    ],
    "paramsList": []
}
```

**add 与 edit 字段差异：**

| 字段 | add | edit | 说明 |
|------|-----|------|------|
| `id` (head) | 不传 | 必传 | 图表头ID |
| `yaxisText` | 不传 | 可选 | Y轴标签文字 |
| `content` | 不传 | 可选 | 自定义内容 |
| `extendJs` | 不传 | 可选 | 扩展JS |
| `isCombination` | 不传 | 可选 | 组合图表标记 |
| `tenantId` | 不传 | 传回原值 | 租户ID |
| Item 关联ID字段 | `cgrheadId`: null | `graphreportHeadId`: headId | 字段名不同 |
| Item `isShow` | `"Y"/"N"` | `"Y"/"N"` | 一致 |
| Item `searchFlag` | 不存在，用 `isSearch` | `searchFlag`: `"Y"/"N"` | add 和 edit 可能不同 |

#### 6.3 字段 ID 生成规则

- add 时使用**雪花ID格式**（19位数字字符串），如 `"2033369959277633538"`
- 可用 Python 的 `str(int(time.time() * 1000) * 1000000 + random.randint(100000, 999999))` 近似生成

#### 6.4 使用 Python 调用 API

**重要限制：**
1. **Windows 环境下 curl 发送中文/长 JSON 会出错**，必须使用 Python
2. **禁止使用 `python3 -c "..."` 内联方式**
3. **必须先用 Write 工具写入 `.py` 临时文件，再用 Bash 执行，最后删除临时文件**

**完整 Python 脚本模板：**

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
sql = "select count(*) cout, sex from sys_user group by sex"
encoded_sql = urllib.parse.quote(sql, safe='')
parse_result = api_request(f'/online/cgreport/head/parseSql?sql={encoded_sql}')
print('解析结果:', json.dumps(parse_result, ensure_ascii=False, indent=2))

if not parse_result.get('success'):
    print('SQL 解析失败:', parse_result.get('message'))
    exit(1)

# ====== Step 2: 构造字段配置 ======
items = [
    {
        "id": gen_id(), "cgrheadId": None,
        "fieldName": "cout", "fieldTxt": "人数",
        "fieldWidth": None, "fieldType": "String",
        "searchMode": None, "isOrder": None, "isSearch": None,
        "dictCode": None, "fieldHref": None,
        "isShow": "Y", "orderNum": 0,
        "replaceVal": None, "isTotal": None,
        "createBy": None, "createTime": None,
        "updateBy": None, "updateTime": None, "groupTitle": None
    },
    {
        "id": gen_id(), "cgrheadId": None,
        "fieldName": "sex", "fieldTxt": "性别",
        "fieldWidth": None, "fieldType": "String",
        "searchMode": None, "isOrder": None, "isSearch": None,
        "dictCode": "sex", "fieldHref": None,
        "isShow": "Y", "orderNum": 1,
        "replaceVal": None, "isTotal": None,
        "createBy": None, "createTime": None,
        "updateBy": None, "updateTime": None, "groupTitle": None
    }
]

# ====== Step 3: 构造请求 ======
graph_data = {
    "dbSource": "",
    "name": "统计男女比例",
    "code": "tj_user_sex",
    "displayTemplate": "tab",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "dataType": "sql",
    "graphType": "bar",
    "cgrSql": sql,
    "onlGraphreportItemList": items,
    "paramsList": []
}

# ====== Step 4: 调用 add API 创建图表 ======
result = api_request('/online/graphreport/head/add', graph_data)
print('创建结果:', json.dumps(result, ensure_ascii=False, indent=2))

if result.get('success'):
    print('\n图表创建成功！')
else:
    print('\n创建失败:', result.get('message'))
```

**编辑图表脚本差异：**

```python
# 编辑时用 PUT 方法，且 items 使用 graphreportHeadId
graph_data = {
    "id": "existing_head_id",
    "name": "统计男女比例",
    "code": "tj_user_bysex",
    "cgrSql": sql,
    "xaxisField": "sex",
    "yaxisField": "cout",
    "yaxisText": "",
    "content": None,
    "extendJs": None,
    "graphType": "line,bar",
    "isCombination": "combination",
    "displayTemplate": "tab",
    "dataType": "sql",
    "dbSource": "",
    "tenantId": 0,
    "lowAppId": None,
    "onlGraphreportItemList": [
        {
            "id": "existing_item_id",
            "graphreportHeadId": "existing_head_id",
            "fieldName": "cout", "fieldTxt": "人数",
            "isShow": "Y", "isTotal": "N",
            "searchFlag": "N", "searchMode": None,
            "dictCode": "", "fieldHref": None,
            "fieldType": "String", "orderNum": 0,
            "replaceVal": None
        }
    ],
    "paramsList": []
}
result = api_request('/online/graphreport/head/edit', graph_data, method='PUT')
```

### Step 7: 生成菜单 SQL（可选）

图表创建成功后，可生成菜单 SQL：

```python
# 查询刚创建的图表
list_result = api_request(f'/online/graphreport/head/list?code={urllib.parse.quote(report_code)}')
if list_result.get('success') and list_result['result']['records']:
    head_id = list_result['result']['records'][0]['id']
    report_name = list_result['result']['records'][0]['name']
    print(f'\n图表 ID: {head_id}')
    print(f'\n### 菜单 SQL（可选执行）')
    print(f"""
INSERT INTO sys_permission (
  id, parent_id, name, url, component, component_name,
  is_route, is_leaf, keep_alive, hidden, hide_tab, description,
  del_flag, rule_flag, status, internal_or_external,
  perms_type, sort_no, menu_type, route_redirect
) VALUES (
  '{head_id}', NULL, '{report_name}',
  '/online/graphreport/{head_id}',
  'modules/online/graphreport/auto/OnlGraphreportAutoMain',
  NULL,
  1, 1, 0, 0, 0, NULL,
  0, 0, '1', 0,
  '0', 1.0, 1, NULL
);
""")
```

### Step 8: 输出结果

```
## Online 图表创建成功

- 图表编码：{code}
- 图表名称：{name}
- 图表类型：{graphType}
- X 轴：{xaxisField}
- Y 轴：{yaxisField}
- 字段数量：{N} 个
- 目标环境：{API_BASE}

### 菜单 SQL
INSERT INTO sys_permission (...) VALUES (...);

### 后续操作
1. 打开 JeecgBoot 后台 → Online图表
2. 找到该图表，点击「功能测试」预览效果
3. 如需配置菜单，执行上方 SQL 或在后台手动添加
4. 可在「编辑」中调整图表类型、字段等配置
```

---

## 高级功能

### 组合图表

支持在同一图表中展示多种图表类型：

```json
{
    "graphType": "line,bar",
    "isCombination": "combination"
}
```

组合图表会在同一坐标系中同时展示折线和柱状图。

### Y 轴标签 (yaxisText)

自定义 Y 轴显示文字：
```json
{
    "yaxisText": "人数（单位：人）"
}
```

### 扩展 JS (extendJs)

通过自定义 JS 扩展图表行为：
```json
{
    "extendJs": "option.tooltip = {trigger: 'axis'};"
}
```

### 自定义内容 (content)

用于自定义渲染模板或说明内容。

### SQL 参数化查询

同报表，支持 Velocity 模板语法的参数：

```sql
SELECT count(*) cout, dept FROM sys_user
WHERE 1=1
${#if($status != '')} AND status = '$status' ${#end}
GROUP BY dept
```

对应的 paramsList 配置：
```json
[
    {"paramName": "status", "paramTxt": "状态", "paramValue": "", "orderNum": 1}
]
```

### 动态数据源

查询非默认数据源的数据：
```json
{
    "dbSource": "second_db"
}
```

---

## API 完整列表

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| SQL 解析 | GET | `/online/cgreport/head/parseSql?sql={encodedSql}&dbKey={dbKey}` | 复用报表接口 |
| 新增图表 | POST | `/online/graphreport/head/add` | 创建图表 |
| 编辑图表 | PUT | `/online/graphreport/head/edit` | 修改图表 |
| 查询列表 | GET | `/online/graphreport/head/list?code={code}` | 查询图表列表 |
| 查询详情 | GET | `/online/graphreport/head/queryById?id={headId}` | 按ID查询 |

---

## 与其他 Skill 的区别

| Skill | 产出物 | 适用场景 |
|-------|--------|---------|
| `jeecg-graphreport` | Online 图表配置（SQL 驱动，数据可视化） | 柱状图、折线图、饼图等数据可视化 |
| `jeecg-onlreport` | Online 报表配置（SQL 驱动，数据列表） | 数据查询报表、统计列表、数据导出 |
| `jeecg-onlform` | Online 表单配置（元数据驱动，CRUD） | 数据录入管理表单 |
| `jeecg-codegen` | Java + Vue3 代码 + SQL | 需要自定义业务逻辑的模块 |
| `jeecg-desform` | 设计器表单 JSON | 数据采集、审批表单 |

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `图表编码已存在` | 换一个 code 或使用 edit 编辑 |
| parseSql 失败 | 检查 SQL 语法是否正确，表是否存在 |
| `SQL注入风险` | 不要在 SQL 中使用 DROP/DELETE/UPDATE 等危险语句 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |

---

## 实测记录

### 实测 1：新增图表（2026-03-16 验证通过）

**测试场景**：创建「系统登录用户统计分析」图表，按性别统计 sys_user 表用户数量

**配置参数**：
- 图表编码：`tj_login_user`
- 图表名称：系统登录用户统计分析
- 图表类型：`bar`（柱状图）
- X 轴：`sex`（性别）
- Y 轴：`cout`（人数）

**SQL**：
```sql
select count(*) cout, sex from sys_user group by sex
```

**Step 1 — parseSql 解析**：

请求：
```
GET /online/cgreport/head/parseSql?sql=select%20count(*)%20cout%2C%20sex%20from%20sys_user%20group%20by%20sex
```

返回（成功）：
```json
{
  "success": true,
  "code": 200,
  "result": {
    "fields": [
      {
        "id": "2033372375880409089",
        "fieldName": "cout",
        "fieldTxt": "cout",
        "fieldType": "String",
        "isShow": 1,
        "orderNum": 1
      },
      {
        "id": "2033372375880409090",
        "fieldName": "sex",
        "fieldTxt": "sex",
        "fieldType": "String",
        "isShow": 1,
        "orderNum": 2
      }
    ],
    "params": []
  }
}
```

**Step 2 — add 创建图表**：

请求：
```
POST /online/graphreport/head/add
```

请求体：
```json
{
    "dbSource": "",
    "name": "系统登录用户统计分析",
    "code": "tj_login_user",
    "displayTemplate": "tab",
    "xaxisField": "sex",
    "yaxisField": "cout",
    "dataType": "sql",
    "graphType": "bar",
    "cgrSql": "select count(*) cout, sex from sys_user group by sex",
    "onlGraphreportItemList": [
        {
            "id": "1773628737000000123456",
            "cgrheadId": null,
            "fieldName": "cout",
            "fieldTxt": "人数",
            "fieldWidth": null,
            "fieldType": "String",
            "searchMode": null,
            "isOrder": null,
            "isSearch": null,
            "dictCode": null,
            "fieldHref": null,
            "isShow": "Y",
            "orderNum": 0,
            "replaceVal": null,
            "isTotal": null,
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "groupTitle": null
        },
        {
            "id": "1773628737000000654321",
            "cgrheadId": null,
            "fieldName": "sex",
            "fieldTxt": "性别",
            "fieldWidth": null,
            "fieldType": "String",
            "searchMode": null,
            "isOrder": null,
            "isSearch": null,
            "dictCode": "sex",
            "fieldHref": null,
            "isShow": "Y",
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
    "paramsList": []
}
```

返回（成功）：
```json
{
  "success": true,
  "message": "添加成功！",
  "code": 200,
  "result": null,
  "timestamp": 1773628737956
}
```

**关键发现**：
1. parseSql 返回的 `fieldTxt` 默认等于 `fieldName`（如 `"cout"`），需 AI 翻译为中文（如 `"人数"`）
2. parseSql 返回的 `isShow` 是数字 `1`，add 时需转为字符串 `"Y"`
3. parseSql 返回的 `fieldType` 全部是 `"String"`，需根据语义修正
4. add 时 items 的 `orderNum` 从 0 开始正常工作
5. add 时 items 中关联 ID 字段名为 `cgrheadId`（值 null），而非 `graphreportHeadId`
6. gen_id() 生成的 19 位数字字符串被 API 正常接受
7. `dictCode: "sex"` 可正确关联系统字典实现值翻译
8. 不需要的字段值传 `null` 即可，不需要传空字符串

### 实测 2：编辑图表（用户提供的接口数据，已验证）

**测试场景**：修改已有图表，将单一柱状图改为组合图表（折线+柱状）

**请求**：
```
PUT /online/graphreport/head/edit
```

**关键字段变化**：
- `graphType` 从 `"bar"` 改为 `"line,bar"`
- 新增 `isCombination: "combination"`
- items 中关联 ID 字段名变为 `graphreportHeadId`（与 add 时的 `cgrheadId` 不同）
- items 中使用 `searchFlag`（`"Y"/"N"`）替代 `isSearch`

**返回**：
```json
{
  "success": true,
  "message": "修改成功!",
  "code": 200,
  "result": null,
  "timestamp": 1773628040311
}
```

**关键发现**：
1. edit 使用 `PUT` 方法（非 POST）
2. edit 时 items 关联字段名为 `graphreportHeadId`，add 时为 `cgrheadId` — **这是最容易踩的坑**
3. edit 时查询字段用 `searchFlag`（`"Y"/"N"`），add 时用 `isSearch`
4. 组合图表需同时设置 `graphType: "line,bar"` 和 `isCombination: "combination"`
5. edit 时需传回 `tenantId`、`createTime`、`createBy` 等系统字段原值
