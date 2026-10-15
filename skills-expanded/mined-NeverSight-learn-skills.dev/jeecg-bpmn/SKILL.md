---
name: jeecg-bpmn
description: Use when user asks to create/generate a BPM workflow, design a Flowable BPMN process, or says "创建流程", "生成流程", "新建流程", "设计流程", "画流程", "审批流程", "工作流", "BPM", "BPMN", "create flow", "create process", "new workflow", "generate workflow". Also triggers when user describes an approval chain like "先经理审批再HR审批" or mentions process nodes like "开始→审批→网关→结束".
---

# JeecgBoot BPM 流程自动生成器

将自然语言的流程描述转换为 Flowable BPMN 2.0 XML，并通过 API 在 JeecgBoot 系统中自动创建流程。

## 前置条件

用户必须提供以下信息（或由 AI 引导确认）：

1. **API 地址**：JeecgBoot 后端地址（如 `https://api3.boot.jeecg.com`）
2. **X-Access-Token**：JWT 登录令牌（从浏览器 F12 获取）

如果用户未提供，提示：
> 请提供 JeecgBoot 后端地址和 X-Access-Token（从浏览器 F12 → Network → 任意请求的 Request Headers 中复制）。

## 交互流程

### Step 0: 解析用户需求

从用户描述中提取以下信息：

| 信息 | 默认值 | 示例 |
|------|--------|------|
| 流程名称 | 用户指定或自动生成 | "员工请假审批流程" |
| 流程类型 | `oa` | 字典 `bpm_process_type` 的值 |
| 节点列表 | 从描述中解析 | 开始→员工提交→经理审批→HR审批→结束 |
| 网关逻辑 | 从描述中解析 | "通过→下一步，拒绝→结束" |
| 审批人配置 | 从描述中解析 | assignee/candidateUsers/candidateGroups/表达式 |

### Step 1: 识别节点并构建流程结构

**支持的节点类型：**

| 用户描述关键词 | BPMN 节点类型 | XML 元素 |
|---------------|---------------|----------|
| 开始 | 开始事件 | `startEvent` |
| 结束 | 结束事件 | `endEvent` |
| 审批/审核/处理/提交 | 用户任务 | `userTask` |
| 条件判断/分支/通过或拒绝 | 排他网关 | `exclusiveGateway` |
| 同时/并行 | 并行网关 | `parallelGateway` |
| 条件并行/部分并行 | 包含网关 | `inclusiveGateway` |
| 子流程/嵌套 | 内嵌子流程 | `subProcess` |
| 调用子流程/主子流程 | 调用子流程 | `callActivity` |
| 会签子流程 | 调用子流程+多实例 | `callActivity` + `multiInstance` |

**审批人配置映射：**

| 用户描述 | BPMN 属性 | 示例 |
|----------|-----------|------|
| "发起人/申请人" | `flowable:assignee="${applyUserId}"` | 流程发起人自动填充 |
| "admin/指定用户名" | `flowable:assignee="admin"` | 固定指定人 |
| "经理角色/角色组" | `flowable:candidateGroups="manager"` + `groupType="role"` | 系统角色候选 |
| "审批角色" | `flowable:candidateGroups="xxx"` + `groupType="approvalRole"` | 审批专用角色 |
| "张三或李四" | `flowable:candidateUsers="zhangsan,lisi"` | 多候选人 |
| "某部门审批" | `flowable:candidateGroups="部门ID"` + `groupType="dept"` | 部门审批 |
| "某岗位审批" | `flowable:candidateGroups="岗位ID"` + `groupType="deptPosition"` | 部门岗位审批 |
| "职级审批" | 表达式 + `groupType="position"` | 职务级别审批 |
| "部门负责人（表达式）" | `flowable:assignee="${deptLeader}"` | 表达式动态 |
| "上一节点指派" | `isAssignedByPreviousNode=true` | 上一审批人选择 |
| "草稿/驳回发起人" | `flowable:assignee="${applyUserId}"` + `sameMode=2` | 草稿节点 |
| "会签/多人同时审批" | `flowable:countersignRule` + 多实例 | 并行/顺序会签 |
| "表单字段选人" | `groupType="formData"` | 从表单动态获取 |

**审批人数据查询：** 当用户提到具体角色/用户/部门名称时，可查数据库获取准确编码：
- 角色编码：`SELECT role_code, role_name FROM sys_role`
- 用户名：`SELECT username, realname FROM sys_user`
- 部门/岗位ID：`SELECT id, depart_name, org_category FROM sys_depart`（org_category: 1=公司, 2=部门, 3=岗位, 4=子公司）

### Step 2: 展示流程摘要并确认

**必须展示以下内容，等待用户确认后再执行：**

```
## 流程摘要

- 流程名称：员工请假审批流程
- 流程类型：oa
- 目标环境：https://api3.boot.jeecg.com

### 流程节点

| 序号 | 节点名称 | 类型 | 审批人 |
|------|---------|------|--------|
| 1 | 开始 | startEvent | - |
| 2 | 员工提交申请 | userTask | ${applyUserId} |
| 3 | 部门经理审批 | userTask | manager (角色组) |
| 4 | 审批结果 | exclusiveGateway | 条件分支 |
| 5 | HR审批 | userTask | hr (角色组) |
| 6 | 结束 | endEvent | - |

### 连线与条件

开始 → 员工提交申请 → 部门经理审批 → 审批结果
  ├─ 通过 (result==1) → HR审批 → 结束
  └─ 拒绝 (result==0) → 结束

确认以上信息正确？(y/n)
```

### Step 3: 生成 BPMN XML 并调用 API

用户确认后，执行以下步骤：

#### 3.1 生成唯一标识

```python
import time
ts = str(int(time.time() * 1000))
process_key = f"process_{ts}"
```

#### 3.2 构造 BPMN XML

阅读以下参考文件（按需）：
- `references/bpmn-xml-skeleton.md` — XML 骨架 + 基本节点模板（必读）
- `references/bpmn-assignee-types.md` — 审批人配置 + 表达式审批人 + groupType速查（必读）
- `references/bpmn-layout.md` — 节点ID命名 + 布局计算（必读）
- `references/bpmn-countersign.md` — 会签配置（需要会签时读）
- `references/bpmn-task-extend.md` — taskExtendJson + 监听器完整清单（配置节点行为时读）
- `references/bpmn-examples.md` — 完整示例 + Python脚本 + 流程模式
- `references/bpmn-advanced.md` — 条件表达式 + 抄送 + 按钮 + 服务任务 + API
- `references/bpmn-subprocess-gateway.md` — 网关 + 子流程（子流程/网关时读）
- `references/bpmn-db-config.md` — 数据库配置表
- `references/example/*.bpmn` — **生产环境真实流程示例**（生成前先阅读最相似的示例学习写法）

核心要点：
- 使用 `bpmn2:` 命名空间前缀（新版设计器规范）
- 必须包含流程结束监听器和任务创建监听器
- 必须包含 `bpmndi:BPMNDiagram` 图形布局信息
- 节点 ID 使用有意义的命名（如 `task_apply`、`gateway_result`）

#### 3.3 构造 nodes 参数

从所有 `userTask` 节点中提取，格式：
```
id=<节点ID>###nodeName=<节点名称>@@@id=<节点ID>###nodeName=<节点名称>@@@
```

#### 3.4 使用 Python 调用 API（必须用 Python，不要用 curl）

**重要限制（实战踩坑）：**
1. **Windows 环境下 curl 发送中文会乱码**，必须使用 Python 的 urllib 确保 UTF-8 编码
2. **禁止使用 `python3 -c "..."` 内联方式**，因为 BPMN XML 中的 `${applyUserId}` 等表达式会被 bash 当作 shell 变量展开，导致 `unexpected EOF` 错误
3. **必须先用 Write 工具写入 `.py` 临时文件，再用 Bash 执行，最后删除临时文件**

**执行步骤：**
```
1. Write 工具 → 写入 create_process.py（项目根目录）
2. Bash 工具 → python create_process.py
3. Bash 工具 → rm create_process.py（清理）
```

**Python f-string 中的转义要点：**
- BPMN 表达式 `${applyUserId}` → f-string 中写作 `${{applyUserId}}`（双花括号转义）
- taskExtendJson 的 `value` 属性用**单引号**包裹 JSON → `value='{{"sameMode":2,...}}'`（避免与 XML 双引号冲突，同时 JSON 花括号也需双花括号转义）
- `flowable:candidateUsers="${flowNodeExecution.getDepartLeaders(execution)}"` → f-string 中写作 `${{flowNodeExecution.getDepartLeaders(execution)}}`

**Python 脚本模板：**

```python
import urllib.request
import urllib.parse
import json
import time

API_BASE = '{用户提供的后端地址}'
TOKEN = '{用户提供的 X-Access-Token}'

ts = str(int(time.time() * 1000))
process_key = f'process_{ts}'
process_name = '流程名称'

# 用 f-string 构造 XML，注意 ${{}} 双花括号转义
bpmn_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<bpmn2:definitions ...>
  <bpmn2:process id="{process_key}" name="{process_name}">
    ...
    <bpmn2:userTask id="task_apply" name="申请人填写" flowable:assignee="${{applyUserId}}">
      <bpmn2:extensionElements>
        <flowable:taskExtendJson value='{{"sameMode":2,...}}' />
        ...
      </bpmn2:extensionElements>
    </bpmn2:userTask>
    ...
  </bpmn2:process>
  <bpmndi:BPMNDiagram>...</bpmndi:BPMNDiagram>
</bpmn2:definitions>'''

nodes_str = 'id=task_apply###nodeName=申请人填写@@@...'

data = {
    'processDefinitionId': '0',
    'processName': process_name,
    'processkey': process_key,
    'typeid': 'oa',
    'lowAppId': '',
    'params': '',
    'nodes': nodes_str,
    'processDescriptor': bpmn_xml,
    'realProcDefId': '',
    'startType': 'manual'
}

encoded_data = urllib.parse.urlencode(data).encode('utf-8')

req = urllib.request.Request(
    f'{API_BASE}/act/designer/api/saveProcess',
    data=encoded_data,
    headers={
        'X-Access-Token': TOKEN,
        'X-Sign': '00000000000000000000000000000000',
        'X-Tenant-Id': '1',
        'X-Timestamp': str(int(time.time() * 1000)),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    },
    method='POST'
)

resp = urllib.request.urlopen(req)
result = json.loads(resp.read().decode('utf-8'))
print(json.dumps(result, ensure_ascii=False, indent=2))
print(f'\\nProcess Key: {process_key}')
```

#### 3.5 检查结果

- `success: true` → 流程创建成功，记录返回的 `obj`（流程ID）
- `success: false` → 输出错误信息，检查 processkey 是否重复等

### Step 4: 输出结果

```
## 流程创建成功

- 流程ID：{obj}
- 流程名称：{processName}
- 流程Key：{processkey}
- 目标环境：{API_BASE}

请在流程设计器中查看：打开 JeecgBoot 后台 → 流程管理 → 流程设计 → 找到该流程
```

---

## 编辑已有流程

如果用户要修改已有流程，需提供 `processDefinitionId`（流程数据表ID），调用同一接口，将 `processDefinitionId` 改为实际ID 即可。

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| Token 过期（401/认证失败） | 提示用户重新获取 X-Access-Token |
| `流程ID重复` | 重新生成时间戳作为 processkey |
| `不是最新版本` | 先查询最新的 processDefinitionId 再保存 |
| 中文乱码 | 确认使用 Python urllib（不要用 curl） |
| 连接超时 | 确认后端地址可达，检查网络 |

## 数据库配置表

流程创建后，可通过以下数据库表进一步配置节点行为、表单绑定和字段权限：

| 表名 | 说明 | 用途 |
|------|------|------|
| `ext_act_process` | 流程主表 | 流程属性、XML、发起方式、催办/撤回/通知等 |
| `ext_act_process_form` | 表单绑定 | 流程与业务表单关联，标题表达式，表单类型（1=Online/2=DesForm/3=自定义） |
| `ext_act_process_node` | 节点配置 | 每个审批节点的功能开关（编辑/抄送/转办/加签/驳回等） |
| `ext_act_process_node_auth` | 字段权限 | 每个节点上表单字段的显示/隐藏/可编辑/禁用控制 |

详细的字段说明和取值参见 `references/bpmn-db-config.md`。

## 参考文档

- 阅读 `references/bpmn-templates.md` 获取参考文件索引（已拆分为 8 个子文件）
