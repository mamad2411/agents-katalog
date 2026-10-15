---
name: jeecg-desform
description: Use when user asks to create/generate a form using AI, design a form automatically, or says "AI设计表单", "AI生成表单", "自动创建表单", "智能表单", "生成一个表单", "帮我设计表单", "创建表单", "新建表单", "做一个表单", "ai form", "generate form", "create form", "design form". Also triggers when user describes form fields like "需要姓名、手机号、地址字段" or mentions form requirements like "做一个请假表单包含请假天数和原因". Supports generating forms from screenshots — when user provides a screenshot/image of a form and asks to reproduce it (e.g., "按照截图生成表单", "照着这个图片做表单", "根据截图创建表单", "generate form from screenshot", "recreate this form").
---

# JeecgBoot 表单设计器 AI 自动生成器

将自然语言的表单需求描述转换为 desformDesignJson，并通过 API 在 JeecgBoot 系统中自动创建表单。

> **重要：本 skill 只处理「设计器表单」（desform），不涉及 Online 表单。两者是完全独立的表单体系。**

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://boot3.jeecg.com/jeecgboot`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

## 交互流程

### Step 0: 解析用户需求

从用户描述中提取以下信息：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 表单名称 | 用户指定或自动生成 | "员工请假申请" |
| 表单编码 | 英文命名，模块名前缀 | `oa_leave_apply`（不用拼音） |
| 字段列表 | 从描述中解析 | 姓名(必填)、请假天数(数字)、请假原因(多行文本) |
| 字段属性 | 从描述中推断 | 必填、默认值、选项列表等 |

### Step 1: 识别字段并选择控件类型

**控件类型映射规则：**

| 用户描述关键词 | 控件 type | 说明 |
|---------------|-----------|------|
| 名称/标题/姓名/文本 | `input` | 单行文本 |
| 描述/备注/原因/详情/多行 | `textarea` | 多行文本 |
| 数量/数字/金额(无单位) | `number` | 数字输入 |
| 整数/个数/天数 | `integer` | 整数输入 |
| 金额/费用/价格 | `money` | 金额（带元单位） |
| 单选/性别/是否/状态 | `radio` | 单选框组 |
| 多选/标签/兴趣 | `checkbox` | 多选框组 |
| 下拉/选择/类型/类别 | `select` | 下拉选择框 |
| 日期/生日/入职日期 | `date` | 日期选择器 |
| 时间/几点 | `time` | 时间选择器 |
| 开关/启用/是否激活 | `switch` | 开关 |
| 评分/星级/打分 | `rate` | 评分 |
| 颜色 | `color` | 颜色选择器 |
| 滑块/进度/百分比 | `slider` | 滑块 |
| 手机/电话/手机号 | `phone` | 手机 |
| 邮箱/Email | `email` | 邮箱 |
| 图片/照片/头像 | `imgupload` | 图片上传 |
| 附件/文件/上传 | `file-upload` | 文件上传 |
| 富文本/HTML内容 | `editor` | 富文本编辑器 |
| Markdown | `markdown` | Markdown 编辑器 |
| 省市/地区/地址选择 | `area-linkage` | 省市级联动 |
| 地图/位置(地图) | `map` | 地图 |
| 定位/GPS | `location` | 定位 |
| 条码/二维码 | `barcode` | 条码 |
| 自动编号/流水号 | `auto-number` | 自动编号 |
| 选人/审批人/负责人 | `select-user` | 用户组件 |
| 部门/选部门 | `select-depart` | 部门组件 |
| 岗位/选岗位 | `select-depart-post` | 岗位组件 |
| 分类树/树选择 | `select-tree` | 下拉树 |
| 表字典/弹窗选择 | `table-dict` | 表字典（popup或模糊查询） |
| 关联记录/引用 | `link-record` | 关联其他表单的记录 |
| 他表字段/自动填充 | `link-field` | 显示关联记录的字段值 |
| 公式/自动计算 | `formula` | 公式计算（求和/均值/自定义） |
| 手写签名/签字 | `hand-sign` | 手写签名 |
| 大写金额/中文大写 | `capital-money` | 金额转大写 |
| 文本组合 | `text-compose` | 多字段值拼接显示 |
| 分隔符/分区 | `divider` | 表单区域分隔线 |
| 文本识别/OCR | `ocr` | 图片文字识别 |
| 子表/明细/清单 | `sub-table-design` | 设计子表 |

### Step 1.5: 字典数据源配置

对于 radio/select/checkbox 控件，数据源有两种方式：

**方式一：静态选项（默认）**
```json
"options": {
  "remote": false,
  "options": [
    { "value": "选项1", "itemColor": "#2196F3" },
    { "value": "选项2", "itemColor": "#08C9C9" }
  ]
}
```

**方式二：系统字典**
当用户描述中提到「字典」、「数据字典」或使用了 JeecgBoot 常见字典编码（如 sex、priority、valid_status 等），使用字典配置：

```json
"options": {
  "remote": "dict",
  "dictCode": "sex",
  "showLabel": true,
  "options": [],
  "remoteOptions": [],
  "props": { "value": "value", "label": "label" }
}
```

同时在**控件顶层**（与 options 同级）添加 `dictOptions`：
```json
"dictOptions": [
  { "value": "1", "label": "男" },
  { "value": "2", "label": "女" }
]
```

**常用 JeecgBoot 系统字典编码：**

| 字典编码 | 说明 | 典型值 |
|---------|------|--------|
| `sex` | 性别 | 1=男, 2=女 |
| `priority` | 优先级 | L=低, M=中, H=高 |
| `valid_status` | 有效状态 | 0=无效, 1=有效 |
| `msg_category` | 消息类型 | 1=通知, 2=系统 |
| `send_status` | 发送状态 | 0=未发送, 1=已发送 |
| `yn` | 是否 | Y=是, N=否 |

> **提示：** 当用户指定的字典编码不确定是否存在时，可通过 API `GET /sys/dict/getDictItems/{dictCode}` 查询确认。如果用户只说了"用字典"但未指定编码，需要询问具体的字典编码。

**desform_utils.py 快捷函数使用字典的正确写法：**

> **踩坑警告：** `RADIO`/`SELECT`/`CHECKBOX` 的 `options` 是**必填位置参数**，使用字典时也不能省略。
> 当指定 `dict_code` 时，`options` 参数必须传**字典项列表**（`[{value, label}]` 格式），不要传字符串列表。
> **不存在** `dict_options` 关键字参数，不要传它（会报 `unexpected keyword argument` 错误）。

```python
# 正确 ✅ — options 传字典项列表 + dict_code
RADIO('性别', [{'value': '1', 'label': '男'}, {'value': '2', 'label': '女'}], dict_code='sex')
SELECT('状态', [{'value': '0', 'label': '无效'}, {'value': '1', 'label': '有效'}], dict_code='valid_status')

# 错误 ❌ — 缺少 options 位置参数
RADIO('性别', dict_code='sex')

# 错误 ❌ — 不存在 dict_options 参数
RADIO('性别', ['男', '女'], dict_code='sex', dict_options=[...])

# 不用字典时，options 传字符串列表即可
SELECT('职称', options=['教授', '副教授', '讲师', '助教'])
```

**底层 `make_widget` 函数中字典的实现原理（仅供参考）：**
```python
# desform_utils.py 内部处理逻辑：
if dict_code:
    opts["remote"] = "dict"
    opts["dictCode"] = dict_code
    opts["showLabel"] = True
    opts["options"] = []
    extra["dictOptions"] = options if isinstance(options[0], dict) else []
```

### Step 2: 展示表单摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## 表单摘要

- 表单名称：员工请假申请
- 表单编码：yuan_gong_qing_jia_shen_qing
- 目标环境：https://boot3.jeecg.com/jeecgboot

### 字段列表

| 序号 | 字段名称 | 控件类型 | 必填 | 说明 |
|------|---------|---------|------|------|
| 1 | 姓名 | input (单行文本) | 是 | 标题字段 |
| 2 | 请假类型 | select (下拉选择) | 是 | 选项：事假/病假/年假 |
| 3 | 开始日期 | date (日期) | 是 | |
| 4 | 结束日期 | date (日期) | 是 | |
| 5 | 请假天数 | integer (整数) | 是 | |
| 6 | 请假原因 | textarea (多行文本) | 否 | |
| 7 | 附件 | file-upload (文件上传) | 否 | |

确认以上信息正确？(y/n)
```

### Step 2.5: 检查表单编码是否已存在（防覆盖规则）

> **重要安全规则：** 在执行创建/保存操作之前，**必须**先通过 `get_form_id(code)` 检查表单编码是否已存在。

**检查方式：** 在临时脚本中调用 `get_form_id(code)` 或在创建脚本中加入检查逻辑。

**如果表单已存在：**
1. **不允许默认覆盖**（不要直接执行 `create_form` 或 `update_form`）
2. 必须明确告知用户：`表单 {code} 已存在 (ID={id})，是否要覆盖更新？`
3. **只有用户明确确认后**才可以执行覆盖操作（调用 `update_form` 更新设计）
4. 如果用户拒绝覆盖，基于原编码生成 3~5 个新编码供用户选择（如原编码 `oa_leave_apply`，可提供 `oa_leave_apply_v2`、`oa_leave_request`、`oa_leave_form`、`oa_staff_leave` 等），用户选定后再重新生成

**预置脚本的防覆盖：** 所有 `scripts/` 目录下的脚本都内置了 `--force` 参数检查，不加 `--force` 时检测到已存在会自动退出。

**动态脚本的防覆盖：** 手动编写的临时脚本中，在调用 `create_form` 之前加入检查：
```python
existing_id, _ = get_form_id(code)
if existing_id:
    print(f'表单 {code} 已存在 (ID={existing_id})，需要用户确认后才能覆盖')
    sys.exit(1)
```

### Step 3: 生成 desformDesignJson 并调用 API

用户确认后，执行以下步骤：

#### 3.0 优先使用通用脚本 + JSON 配置（推荐方式）

> **重要：优先使用 `scripts/desform_creator.py` 通用脚本 + JSON 配置文件的方式，只需生成少量 JSON 数据即可创建表单，避免每次编写大量 Python 代码。只有当通用脚本无法满足特殊需求时，才编写自定义临时脚本。**

**脚本位置：** `scripts/desform_creator.py`

**使用步骤：**
1. 根据用户需求生成 JSON 配置文件（Write 到工作目录的临时 `.json` 文件）
3. 用 Bash 执行脚本：`python "<skill目录>/scripts/desform_creator.py" --api-base <URL> --token <TOKEN> --config <config.json>`
4. 删除临时 JSON 配置文件

**脚本自动完成：**
- 防覆盖检查（不加 `--force` 时检测到已存在自动退出）
- 根据 JSON 配置构建所有控件
- 调用 `create_form` 创建/保存表单设计
- 输出菜单 SQL（如果 JSON 中配置了 `menuParent`）

**JSON 配置格式：**
```json
{
  "formName": "表单中文名称",
  "formCode": "module_form_code",
  "layout": "word",
  "titleIndex": 0,
  "fields": [
    {"name": "字段名", "type": "控件类型", ...控件参数}
  ],
  "menuParent": "父菜单名称",
  "menuIcon": "ant-design:appstore-outlined"
}
```

| JSON 字段 | 必填 | 默认值 | 说明 |
|-----------|------|--------|------|
| `formName` | 是 | - | 表单中文名称 |
| `formCode` | 是 | - | 表单编码（英文，模块名前缀） |
| `layout` | 否 | `"auto"` | 布局模式：`auto`/`half`/`full`/`word` |
| `titleIndex` | 否 | `0` | 标题字段在 fields 中的索引 |
| `fields` | 是 | - | 字段定义数组 |
| `menuParent` | 否 | - | 生成菜单 SQL 的父菜单名称 |
| `menuIcon` | 否 | `ant-design:appstore-outlined` | 父菜单图标 |

**字段定义（fields 数组中每个对象）：**

每个字段只需 `name` + `type`，其余参数可选：

```json
{"name": "工程名称", "type": "input", "required": true}
{"name": "工程类别", "type": "radio", "options": ["土建", "安装", "装饰"]}
{"name": "验收日期", "type": "date"}
{"name": "金额", "type": "money", "unit": "万元"}
{"name": "自动编号", "type": "auto-number", "prefix": "GCYS"}
{"name": "条码", "type": "barcode"}
{"name": "定位", "type": "location"}
{"name": "签字", "type": "hand-sign", "required": true}
{"name": "---", "type": "divider", "text": "分隔标题"}
{"name": "性别", "type": "radio", "dictCode": "sex",
 "options": [{"value": "1", "label": "男"}, {"value": "2", "label": "女"}]}
```

**支持的 type 及可选参数：**

| type | 可选参数 | 说明 |
|------|---------|------|
| `input` | `required`, `placeholder`, `unique` | 单行文本 |
| `textarea` | `required` | 多行文本 |
| `number` | `required`, `unit`, `precision` | 数字 |
| `integer` | `required`, `unit` | 整数 |
| `money` | `required`, `unit` | 金额 |
| `date` | `required`, `fmt` | 日期（fmt 默认 `yyyy-MM-dd`） |
| `time` | `required` | 时间 |
| `switch` | - | 开关 |
| `slider` | - | 滑块 |
| `rate` | - | 评分 |
| `color` | - | 颜色 |
| `radio` | `options`(必填), `required`, `dictCode` | 单选 |
| `select` | `options`(必填), `required`, `multiple`, `dictCode` | 下拉 |
| `checkbox` | `options`(必填), `required`, `dictCode` | 多选 |
| `select-user` | `required`, `multiple` | 选人 |
| `select-depart` | `required`, `multiple` | 选部门 |
| `phone` | `required` | 手机 |
| `email` | `required` | 邮箱 |
| `area-linkage` | `required` | 省市级联 |
| `file-upload` | `required` | 文件上传 |
| `imgupload` | `required` | 图片上传 |
| `hand-sign` | `required` | 手写签名 |
| `auto-number` | `prefix` | 自动编号 |
| `barcode` | `codeType`(`barcode`/`qrcode`) | 条码 |
| `location` | `required` | 定位 |
| `formula` | `mode`, `expression`, `decimal`, `unit` | 公式 |
| `divider` | `text` | 分隔符（name 会被忽略，用 text） |
| `editor` | `required` | 富文本 |
| `markdown` | `required` | Markdown |
| `link-record` | `sourceCode`, `titleField`, `showFields`, `showMode`, `showType` | 关联记录 |
| `link-field` | `linkRecordKey`, `showField`, `fieldType`, `fieldOptions` | 他表字段 |

**完整示例（工程竣工验收申请表）：**
```json
{
  "formName": "工程竣工验收申请表",
  "formCode": "eng_completion_acceptance",
  "layout": "word",
  "fields": [
    {"name": "自动编号", "type": "auto-number", "prefix": "GCYS"},
    {"name": "条码", "type": "barcode"},
    {"name": "工程名称", "type": "input", "required": true},
    {"name": "工程编号", "type": "input"},
    {"name": "工程类别", "type": "radio", "options": ["土建工程", "安装工程", "装饰工程", "市政工程"]},
    {"name": "建设单位", "type": "input"},
    {"name": "工程地址", "type": "input"},
    {"name": "施工单位", "type": "input"},
    {"name": "开工时间", "type": "date"},
    {"name": "完工时间", "type": "date"},
    {"name": "工程量清单", "type": "textarea"},
    {"name": "图片上传", "type": "imgupload"},
    {"name": "定位", "type": "location"},
    {"name": "验收类别", "type": "radio", "options": ["竣工验收", "分部验收", "专项验收"]},
    {"name": "施工单位项目经理签字", "type": "hand-sign"},
    {"name": "---", "type": "divider", "text": "广电工程完工验收报告"},
    {"name": "工程名称(报告)", "type": "input"},
    {"name": "工程编号(报告)", "type": "input"},
    {"name": "建设单位(报告)", "type": "input"},
    {"name": "施工单位(报告)", "type": "input"},
    {"name": "开工时间(报告)", "type": "date"},
    {"name": "完工时间(报告)", "type": "date"},
    {"name": "验收时间", "type": "time"},
    {"name": "验收类别(报告)", "type": "radio", "options": ["竣工验收", "分部验收", "专项验收"]},
    {"name": "---", "type": "divider", "text": "竣工项目分项审查情况"},
    {"name": "立项手续完整性", "type": "radio", "options": ["合格", "不合格", "整改后合格"]},
    {"name": "项目主体组签字(立项)", "type": "hand-sign"},
    {"name": "竣工资料完整性", "type": "radio", "options": ["合格", "不合格", "整改后合格"]},
    {"name": "项目主体组签字(资料)", "type": "hand-sign"},
    {"name": "施工工艺合规性", "type": "radio", "options": ["合格", "不合格", "整改后合格"]},
    {"name": "项目主体组签字(工艺)", "type": "hand-sign"},
    {"name": "技术指标达标情况", "type": "radio", "options": ["合格", "不合格", "整改后合格"]},
    {"name": "项目主体组签字(技术)", "type": "hand-sign"},
    {"name": "材料设备核定结果", "type": "radio", "options": ["合格", "不合格", "整改后合格"]},
    {"name": "项目主体组签字(材料)", "type": "hand-sign"},
    {"name": "工程量核量结果", "type": "radio", "options": ["合格", "不合格", "整改后合格"]},
    {"name": "项目主体组签字(核量)", "type": "hand-sign"},
    {"name": "验收问题清单", "type": "textarea"},
    {"name": "验收结论", "type": "radio", "options": ["合格", "不合格", "整改后复验"]},
    {"name": "技术部负责人签字", "type": "hand-sign"},
    {"name": "施工单位签字", "type": "hand-sign"},
    {"name": "分管领导组签字", "type": "hand-sign"}
  ],
  "menuParent": "工程验收管理"
}
```

**调用示例：**
```bash
# 1. Write 工具生成 JSON 配置文件
# 2. 执行脚本
python "C:/Users/moe/.claude/skills/jeecg-desform/scripts/desform_creator.py" \
    --api-base http://192.168.1.233:3100/jeecgboot \
    --token eyJhbGciOiJIUzI1NiJ9... \
    --config eng_acceptance.json

# 如需覆盖已存在的表单
python "C:/Users/moe/.claude/skills/jeecg-desform/scripts/desform_creator.py" \
    --api-base http://192.168.1.233:3100/jeecgboot \
    --token eyJhbGciOiJIUzI1NiJ9... \
    --config eng_acceptance.json \
    --force

# 3. 删除临时 JSON 文件
```

#### 3.1 生成唯一标识

- key 和 model 使用当前时间戳毫秒数 + 6 位随机数
- 格式参见 `references/desform-design-json-schema.md`

#### 3.2 构造 desformDesignJson

阅读以下参考文件（按需）：
- `references/desform-design-json-schema.md` — JSON Schema 结构、控件类型清单、通用字段（必读）
- `references/desform-widget-options.md` — 每种控件的完整 options 配置（必读）
- `references/desform-examples.md` — 常见表单模式示例 + Python 脚本模板（必读）
- `references/desform-real-samples.md` — 真实业务表单案例（字典、半行、分区、公式、关联）

核心要点：
- 每个普通控件必须包裹在 `card` 容器中（除了 editor、markdown、divider、map、sub-table-design、link-record(多条/表格模式)、grid、tabs）
- `config.titleField` 指向标题字段的 model（优先 input，也可以是 select-user 等其他控件）
- `config.hasWidgets` 必须列出所有使用到的控件 type（包括 card）
- key 格式：`{timestamp}_{6位随机数}`（源码中实际是 randomKey，但时间戳格式也兼容）
- model 格式：`{type}_{timestamp}_{6位随机数}`（type 中的 `-` 转为 `_`，如 `link_record_xxx`）
- model 必须全局唯一（保存时会检查重复 model）

**className / icon 易错控件（实测验证）：**
- `link-record`: className=`form-link-record`, icon=**`icon-link`**（不是 `icon-link-record`）
- `link-field`: className=`form-link-field`, icon=**`icon-field`**（不是 `icon-link-field`）
- `sub-table-design`: className=**`form-sub-table`**, icon=**`icon-table`**（不是 `form-sub-table-design` / `icon-sub-table-design`）

**link-record / link-field 关键配置：**
- link-record 的 `advancedSetting.defaultValue.customConfig` 必须为 `true`
- link-record 的 `allowView`、`allowEdit`、`allowAdd`、`allowSelect` 必须全部设为 `true`（4 个操作选项默认全部勾选）
- link-record 的 `titleField` 必须填源表真实标题字段 model，`showFields` 填源表展示字段 model 列表
- link-field **没有 `advancedSetting`**（与其他控件不同）
- link-field 的 `linkRecordKey` 填 link-record 的 **key**（不是 model）
- link-field 的 `fieldType` 必须填源字段的真实控件类型（不能一律写 `"input"`）
- link-field 的 `fieldOptions` 需包含源字段类型相关的 options（如 select-user 需 `{"multiple": false, "customReturnField": "username"}`）

**sub-table-design 关键配置：**
- options 必须包含 `allowAdd: true`，否则子表没有"添加"按钮
- 完整 options 见 `references/desform-widget-options.md`（showCheckbox、showNumber、operationMode 等缺一不可）
- 子表内可放 link-record + link-field 实现行级关联选择

**跨表单批量创建流程：**
1. 先创建基础表单 → 2. 查询获取字段 model → 3. 构建业务表单时引用这些 model

#### 3.3 使用 Python 调用 API（必须用 Python，不要用 curl）

**优先使用共通工具库 `desform_utils.py`**（位于 `scripts/desform_utils.py`）。

**使用共通工具库的执行步骤：**
```
1. Write 工具 → 写入业务脚本 create_xxx.py（scripts/ 目录，import desform_utils）
2. Bash 工具 → cd <skill目录>/scripts && python create_xxx.py
3. Bash 工具 → rm create_xxx.py（清理临时脚本）
```

**共通工具库使用示例：**
```python
import sys
sys.path.insert(0, r'{后端项目根目录}')
from desform_utils import *

init_api('https://boot3.jeecg.com/jeecgboot', 'your-token')

# 简单表单（含字典用法）
create_form('员工信息', 'employee_info', [
    INPUT('姓名', required=True),
    RADIO('性别', [{'value': '1', 'label': '男'}, {'value': '2', 'label': '女'}], dict_code='sex'),
    PHONE('电话'),
    EMAIL('邮箱'),
    DEPART('部门'),
    SELECT('职称', options=['教授', '副教授', '讲师', '助教']),
    TEXTAREA('备注'),
])

# 带关联的表单
form_id, title = create_form('客户信息', 'customer_info', [
    INPUT('客户名称', required=True),
    PHONE('电话'),
])
# 查询字段用于关联
tf, fields = get_form_fields('customer_info')
create_form('联系人', 'contact_info', [
    INPUT('姓名', required=True),
    LINK_RECORD('所属客户', 'customer_info', tf, [fields['客户名称']['model']]),
])

# 菜单SQL（ID 自动生成 UUID，只需传菜单名和子项）
print(gen_menu_sql('CRM系统', [
    ('客户信息', 'customer_info', 1),
    ('联系人', 'contact_info', 2),
]))

# 查询表单
form = query_form('customer_info')
print(form['id'], form['updateCount'])

# 修改已有表单设计（自动获取 updateCount）
update_form('customer_info', [
    INPUT('客户名称', required=True),
    PHONE('电话'),
    EMAIL('邮箱'),
    TEXTAREA('备注'),
])

# 删除表单（支持 3 种方式）
delete_form('customer_info')                    # 传 code，自动查找 ID
delete_form('customer_info', '123456789')       # 传 code + 已知 ID，跳过搜索（最快）
delete_form('123456789012345678')               # 只传 ID
```

**可用的快捷函数（大写命名）：**
- 基础: `INPUT`, `TEXTAREA`, `NUMBER`, `INTEGER`, `MONEY`, `DATE`, `TIME`, `SWITCH`, `SLIDER`, `RATE`, `COLOR`
- 选择: `RADIO`, `SELECT`, `CHECKBOX`（支持 dict_code 字典）
- 系统: `USER`, `DEPART`, `PHONE`, `EMAIL`, `AREA`
- 文件: `FILE`, `IMGUPLOAD`, `HANDSIGN`
- 高级: `AUTONUMBER`, `FORMULA`, `LINK_RECORD`, `LINK_FIELD`
- 不需要 card: `DIVIDER`, `EDITOR`, `MARKDOWN`
- 子表内: `SUB_INPUT`, `SUB_INTEGER`, `SUB_NUMBER`, `SUB_MONEY`, `SUB_SELECT`, `SUB_DATE`, `SUB_LINK_RECORD`, `SUB_LINK_FIELD`, `SUB_FORMULA`
- 容器: `make_card`, `make_sub_table`
- API: `init_api`, `create_form`, `update_form`, `delete_form`, `query_form`, `get_form_id`, `get_form_fields`, `find_or_create_form`, `save_design`

> **`create_form` 的 `layout` 参数：**
> - `'auto'`（默认）：字段数 >= 6 时自动使用半行两列布局
> - `'half'`：强制半行布局
> - `'full'`：强制整行布局（不做半行处理）
> - `'word'`：Word 风格布局（表格边框样式，见下方详细说明）
> - textarea/editor/file-upload/imgupload 等宽控件自动保持整行
>
> **Word 风格表单（`layout='word'`）：**
>
> Word 风格模拟传统 Word 文档表格样式，适用于审批单、申请表等正式场景。
>
> **实现原理（JeecgBoot 表单设计器内置支持）：**
> - `formStyle: "word"` — 表单风格设为 Word（设计器右侧「表单属性」→「表单风格」→「Word风格」）
> - 栅格布局 `grid`，className = `form-grid form-grid-word-theme` — 每行一个栅格容器
> - 标签列：独立的 `text` 控件（16px、居中），放在栅格的第一列
> - 控件列：实际控件设置 `hideTitle: true`（隐藏标题），放在栅格的第二列
> - 顶部标题：独立的 `text` 控件（24px、加粗、居中），不使用内置 header
> - 外部 CSS：加载 `/desform/expand/css/theme-word.css` 提供表格边框样式
> - `showHeaderTitle: false`、`disabledAutoGrid: true`
>
> **栅格 span 分配规则：**
> - 两列行（半行控件配对）：标签1 span=6 + 控件1 span=6 + 标签2 span=4 + 控件2 span=8
> - 单列行（textarea/file-upload 等宽控件）：标签 span=6 + 控件 span=18
>
> **使用示例：**
> ```python
> create_form('提成申请单', 'oa_commission_apply', [
>     USER('申请人', required=True),
>     DEPART('部门', required=True),
>     DATE('申请日期', required=True),
>     INPUT('项目名称', required=True),
>     MONEY('合同金额', required=True),
>     MONEY('提成金额', required=True),
>     TEXTAREA('提成说明'),
>     FILE('附件'),
> ], layout='word')
> ```
>
> **注意事项：**
> - `_apply_word_layout` 会自动生成顶部标题 text、栅格行、text 标签
> - hand-sign/textarea/file-upload/divider 等宽控件自动独占一行
> - 标签列 flex 垂直居中对齐
>
> **`gen_menu_sql` 的 `icon` 参数：**
> - 默认值 `'ant-design:appstore-outlined'`，一级菜单自动带图标
> - 可自定义：`gen_menu_sql('费用管理', [...], icon='ant-design:dollar-outlined')`
- 字典: `query_dict(code)` 查询字典项, `search_dict(keyword)` 按名称/编码模糊搜索字典
- SQL: `gen_menu_sql`

**如果共通工具库不存在，则使用以下方式：**

**重要限制（实战踩坑）：**
1. **Windows 环境下 curl 发送中文/长JSON会出错**，必须使用 Python 的 urllib/requests 确保 UTF-8 编码
2. **禁止使用 `python3 -c "..."` 内联方式**，因为 JSON 中的特殊字符会被 bash 解析出错
3. **必须先用 Write 工具写入 `.py` 临时文件，再用 Bash 执行，最后删除临时文件**

**执行步骤：**
```
1. Write 工具 → 写入 create_desform.py（项目根目录）
2. Bash 工具 → python create_desform.py
3. Bash 工具 → rm create_desform.py（清理）
```

**API 踩坑记录（实战验证）：**

> **关键踩坑：**
> 1. `POST /desform/add` 现已直接返回表单实体（含 ID），`desform_utils.py` 已优先从返回值获取 ID，旧版后端不返回时自动 fallback 到 list 搜索
> 2. `GET /desform/queryByCode` **不可靠**（部分表单查不到），推荐用 `GET /desform/queryByIdOrCode?desformCode={code}`
> 3. `queryByIdOrCode` 对新创建但未保存设计的表单也可能返回失败，此时需通过 list API 全量搜索
> 4. list API 的 `desformCode` 过滤参数**不可靠**（有时匹配不到），必须全量搜索后手动精确匹配
> 5. `PUT /desform/edit` 的 `updateCount` 必须传**当前数据库中的值**（不是 +1），后端会自动递增
> 6. `DELETE /desform/deleteBatch` 是**逻辑删除**（放入回收站），表单 code 仍被占用
> 7. `DELETE /desform/recycleBin/deleteByIds` 可彻底删除回收站中的表单，释放 code。`delete_form` 已封装完整流程，支持传 code 或 ID
> 8. `PUT /desform/recycleBin/recoverByIds` 可从回收站恢复表单
> 9. `DELETE /desform/recycleBin/empty` 清空回收站（在演示环境中可能不完全生效）
> 10. **删除后重建时序问题：** 彻底删除表单后，code 释放可能有延迟。如果 `add` 返回 `该code已存在`，说明该 code 之前被另一个表单占用（同 code 可能存在多条记录）。此时应通过 list 全量搜索找到占用该 code 的表单，对其执行 `deleteBatch` + `recycleBin/deleteByIds` 彻底删除后再重建
> 11. **`save_design` 报「未找到对应实体」：** 通常是因为使用了已被删除的旧表单 ID。`find_or_create_form` 可能返回旧 ID（缓存或竞态），此时需通过 list API 重新搜索获取最新有效 ID
>
> **`create_form` vs `save_design` 使用区别：**
> - **推荐始终使用 `create_form`**（一站式：查找/创建 + 保存设计），它会自动解包 tuple、确定标题字段、处理 updateCount
> - `save_design` 是底层函数，签名为 `save_design(form_id, form_code, widgets, title_model, update_count)`
>   - `widgets` 参数需要传**解包后的 widget dict 列表**（不是 tuple），tuple 需先 `[w[0] for w in widgets_tuples]` 解包
>   - `title_model` 是标题字段的 model 字符串（不是 index），可通过 `widgets_tuples[0][2]` 获取
>   - 如需直接调用 `save_design`，务必先通过 `queryByIdOrCode` 获取最新 `updateCount`
>
> **命名规则：**
> - 表单编码使用英文命名（不用拼音），模块名作为前缀
> - 格式：`{模块}__{实体}`，如 `crm_customer`、`crm_contact`、`oa_leave_apply`
> - 同一模块的表单共享前缀，便于分组管理
>
> **find_or_create_form 策略（desform_utils.py 中已实现）：**
> 1. 先尝试 `POST /desform/add` 创建
> 2. 若 add 成功且返回值含 ID → 直接使用（新版后端已支持）
> 3. 若 add 成功但返回值无 ID → 通过 list API 全量搜索获取 ID（旧版兜底）
> 4. 若 add 失败（code已存在）→ 尝试 `queryByIdOrCode` 获取 ID
> 5. 若 queryByIdOrCode 也失败 → 通过 list API 全量搜索获取 ID

#### 3.4 检查结果

- `success: true` → 表单创建成功
- `success: false` → 输出错误信息，检查 desformCode 是否重复等

### Step 4: 输出结果

```
## 表单创建成功

- 表单ID：{id}
- 表单名称：{desformName}
- 表单编码：{desformCode}
- 目标环境：{API_BASE}

请在表单设计器中查看：打开 JeecgBoot 后台 → 表单设计器 → 找到该表单
```

**同时输出菜单 + 角色授权 SQL（用于将设计器表单加入系统菜单）：**

`gen_menu_sql` 函数会同时生成 `sys_permission`（菜单）和 `sys_role_permission`（角色授权）的 SQL。
**所有 ID（菜单 ID、授权记录 ID）均自动生成 32 位无横线 UUID，无需手动指定。**

```python
# 调用方式：只需传父菜单名称 + 子菜单列表
sql = gen_menu_sql('物业管理', [
    ('小区信息', 'pm_community', 1),
    ('楼栋信息', 'pm_building', 2),
    ('房屋信息', 'pm_house', 3),
])
print(sql)
```

生成的 SQL 格式（每条 INSERT 都带完整列名，避免列错位）：
```sql
-- 父菜单（ID 自动生成 UUID）
INSERT INTO sys_permission(id, parent_id, name, url, component, component_name, redirect, menu_type, perms, perms_type, sort_no, always_show, icon, is_route, is_leaf, keep_alive, hidden, hide_tab, description, status, del_flag, rule_flag, create_by, create_time, update_by, update_time, internal_or_external)
VALUES ('{uuid}', NULL, '{parentName}', '/{uuid}', 'layouts/RouteView', NULL, NULL, 0, NULL, '1', 1.00, 0, NULL, 1, 0, 0, 0, 0, NULL, '1', 0, 0, 'admin', now(), NULL, NULL, 0);
INSERT INTO sys_role_permission (id, role_id, permission_id, data_rule_ids, operate_date, operate_ip)
VALUES ('{uuid}', '{roleId}', '{parentUuid}', NULL, now(), '127.0.0.1');

-- 子菜单（ID 自动生成 UUID）
INSERT INTO sys_permission(id, parent_id, name, url, component, component_name, redirect, menu_type, perms, perms_type, sort_no, always_show, icon, is_route, is_leaf, keep_alive, hidden, hide_tab, description, status, del_flag, rule_flag, create_by, create_time, update_by, update_time, internal_or_external)
VALUES ('{uuid}', '{parentUuid}', '{desformName}', '/online/desform/list/{desformCode}', 'super/online/desform/auto/AutoDesformDataList', 'AutoDesformDataList', NULL, 0, NULL, '1', 1.00, 0, NULL, 0, 1, 0, 0, 0, NULL, '1', 0, 0, 'admin', now(), NULL, NULL, 0);
INSERT INTO sys_role_permission (id, role_id, permission_id, data_rule_ids, operate_date, operate_ip)
VALUES ('{uuid}', '{roleId}', '{menuUuid}', NULL, now(), '127.0.0.1');
```

**菜单 SQL 关键字段说明：**

| 字段 | 值 | 说明 |
|------|-----|------|
| id | 自动生成 32 位 UUID | 如 `d0ca42ae976a4dfbbff491e304858fe1` |
| url | `/online/desform/list/{desformCode}` | 设计器表单数据列表路由，desformCode 是表单编码 |
| component | `super/online/desform/auto/AutoDesformDataList` | 固定值，设计器表单自动数据列表组件 |
| component_name | `AutoDesformDataList` | 固定值 |
| is_route | `0` | 不走普通路由 |
| is_leaf | `1` | 叶子节点 |
| parent_id | `NULL` 或父菜单UUID | NULL=一级菜单，指定父UUID=子菜单 |

**角色授权 SQL 说明：**

| 字段 | 值 | 说明 |
|------|-----|------|
| id | 自动生成 32 位 UUID | 每条授权记录独立 UUID |
| role_id | `f6817f48af4fb3af11b9e8bf182f618b` | 默认角色 ID（desform_utils.py 中 ROLE_ID 常量），可通过参数覆盖 |
| permission_id | 对应的菜单 UUID | 关联 sys_permission.id |

> **重要：输出菜单 SQL 时，必须直接使用 `gen_menu_sql` 函数的完整输出，不要手动缩写或省略列名，否则会因列错位导致执行报错。**

### 本地环境自动执行菜单 SQL 规则

**判断条件：** `init_api` 传入的 api_base 以 `http://127.0.0.1` 或 `http://localhost` 开头（不区分大小写）。

**自动执行方式：** 在 `gen_menu_sql` 生成 SQL 后，通过 Bash 工具逐条执行 MySQL 命令：

```bash
# 先检查菜单是否已存在，避免重复插入
mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3 -e "SELECT id FROM sys_permission WHERE id='{menuId}'"
# 不存在则执行插入（包括 sys_permission 和 sys_role_permission）
mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3 -e "INSERT INTO sys_permission(...) VALUES (...);"
mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3 -e "INSERT INTO sys_role_permission(...) VALUES (...);"
```

**注意事项：**
- 将 `gen_menu_sql` 的每条 INSERT 语句拆分后逐条通过 MySQL CLI 执行
- 执行前先检查父菜单 ID 是否已存在，避免重复插入
- 如果 MySQL 执行失败，回退为输出 SQL 让用户手动执行，不中断整体流程
- 数据库连接参数默认 `mysql -h127.0.0.1 -P3306 -uroot -proot jeecgboot3`，与 jeecg-codegen 保持一致
- 输出结果中标注 `菜单 SQL：已自动执行 ✓`

---

## 编辑已有表单

如果用户要修改已有表单，需提供表单 ID 或编码，然后：
1. 查询现有表单设计 JSON
2. 根据用户需求修改 JSON
3. 调用 `PUT /desform/edit` 保存（注意带上正确的 `updateCount`）

---

## 删除表单

`delete_form` 已封装完整的删除流程（查找 → 逻辑删除 → 物理删除），支持 3 种调用方式：

```python
from desform_utils import *
init_api('https://boot3.jeecg.com/jeecgboot', 'your-token')

# 方式1：传 code（自动查找 ID，优先 queryByIdOrCode 快速查找）
delete_form('edu_teacher')

# 方式2：传 code + 已知 ID（跳过搜索，最快）
delete_form('edu_teacher', '2032994312457920514')

# 方式3：只传 ID（纯数字且长度>15 自动识别为 ID）
delete_form('2032994312457920514')
```

**内部执行流程：**
1. 确定表单 ID（传了 ID 直接用，传 code 则优先 `queryByIdOrCode` 快速查找，查不到再 fallback 到 list 全量搜索）
2. `DELETE /desform/deleteBatch?ids={id}` — 逻辑删除（放入回收站）
3. `DELETE /desform/recycleBin/deleteByIds?ids={id}` — 物理删除

**删除注意事项：**
- **不能跳过逻辑删除：** `recycleBin/deleteByIds` 只删除 `del_flag=1` 的记录，必须先执行 `deleteBatch`
- **同一 code 可能存在多条记录：** 传 code 时会自动处理多条记录全部删除
- **批量删除时传 ID 更快：** 创建时已获取 ID，删除时直接传入可跳过查询

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `该code已存在` | **不要直接覆盖**，提示用户确认是否覆盖（参见 Step 2.5 防覆盖规则），用户确认后再用 `update_form` 更新设计 |
| `未找到对应实体` | 表单数据不一致（存在于 list 但无法编辑），需用 `deleteBatch` + `recycleBin/deleteByIds` 彻底删除后重建 |
| `表单编码过长` | desformCode 缩短到 200 字符以内 |
| `当前版本已过时，请刷新重试` | updateCount 传值错误，必须传当前值（通过 queryByIdOrCode 或 list 获取） |
| `add` 返回 `result: null` | 旧版后端行为，`desform_utils.py` 已自动 fallback 到 list 搜索；新版后端已直接返回实体 |
| `queryByCode` 返回 false | 该接口不可靠，改用 `queryByIdOrCode` 或 list 全量搜索 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |
| 连接超时 | 确认后端地址可达，检查网络 |

## 参考文档

- `scripts/desform_creator.py` — **通用表单创建脚本**，优先使用此脚本 + JSON 配置文件
- `scripts/desform_utils.py` — **共通工具库**（控件工厂、API 封装、布局引擎）
- `references/desform-design-json-schema.md` — JSON Schema 结构、控件类型清单、通用字段
- `references/desform-widget-options.md` — 每种控件的完整 options 配置
- `references/desform-examples.md` — 常见表单模式示例 + Python 脚本模板
- `references/desform-real-samples.md` — 真实业务表单案例（字典、半行、分区、公式、关联）
