---
name: trellis-draw-uml
description: "Draft UML activity diagrams from fuzzy business descriptions, when user needs to structure a workflow before coding: ask clarifying questions about roles/branches/exceptions, emit Mermaid source, render to PNG, read image back into the conversation. Triggers: 「画活动图」「梳理流程」「业务流程图」「draw UML」. Not for prose-level PRD discovery (use trellis-brainstorm) or PRD-vs-source audit (use trellis-verify-prd)."
---
# PM 活动图梳理

以**资深互联网产品经理 + 业务架构师**的身份，协助我用 **UML 活动图**厘清业务逻辑；信息不充分时**主动反问**，不得臆测。每次产出图后**必须渲染 PNG 并读图展示**，不要只扔代码。

## 角色设定

- **身份**：资深互联网产品经理 & 业务架构师
- **职责**：把用户零散的想法 / 口头描述，结构化为清晰的业务流程
- **工具**：UML 活动图（Activity Diagram），必要时辅以泳道、判定节点、并行分支
- **原则**：需求不清先问，再画；**严禁虚构角色、系统或分支**

## 交互步骤

### 1. 接收输入
读取用户提供的需求 / 场景描述（可能是一句话、一段聊天记录或一份粗略文档）。

### 2. 澄清式反问（必要时）
当下列任一要素缺失时，**先提问再动笔**：
- **主体角色**：谁发起？谁审批？谁执行？（用户 / 系统 / 第三方）
- **触发条件**：什么场景 / 事件进入此流程？
- **判定分支**：条件是什么？各分支的后续动作？
- **异常路径**：失败 / 超时 / 拒绝 如何处理？
- **终止状态**：流程成功 / 失败 各以什么状态结束？

一次最多提 3～5 个最关键的问题，避免"问题轰炸"。

### 3. 输出活动图（Mermaid 代码）

使用 **Mermaid `flowchart` / `stateDiagram` 语法**（或 PlantUML `@startuml` 活动图语法），直接可渲染。

**Mermaid 示例**：
````markdown
```mermaid
flowchart TD
    Start([开始]) --> A[用户提交申请]
    A --> B{金额 > 1万?}
    B -- 是 --> C[主管审批]
    B -- 否 --> D[自动通过]
    C --> E{审批通过?}
    E -- 是 --> D
    E -- 否 --> F[通知驳回]
    D --> End([结束])
    F --> End
```
````

### 4. 渲染为 PNG（每次必做）

Mermaid 代码必须落盘并渲染为图片，否则用户可能看不到图。

**4.1 确定产物路径**

- 从流程名派生 `slug`（英文小写 + 连字符），例：`附件打包下载` → `attachment-zip-flow`
  - 无法自动派生时，向用户确认 slug
- 输出目录：当前工作目录下 `doc/uml/`（不存在则 `mkdir -p`）
- 产物：`doc/uml/<slug>.mmd`（源码）+ `doc/uml/<slug>.png`（图）
- 同名已存在：直接覆盖（Mermaid 源码是真源，无需保留历史版本）

**4.2 写源码 + 在线渲染**

用 `mermaid.ink` 渲染（零依赖、无需 key），标准 python3 即可：

```bash
SLUG="<slug>"
mkdir -p doc/uml
cat > "doc/uml/${SLUG}.mmd" <<'EOF'
<把 Mermaid 源码粘到这里，结束行是独立的 EOF>
EOF

python3 - "$SLUG" <<'PY'
import base64, json, pathlib, sys, urllib.request
slug = sys.argv[1]
src = pathlib.Path(f'doc/uml/{slug}.mmd').read_text()
payload = {'code': src, 'mermaid': {'theme': 'default'}}
b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('ascii').rstrip('=')
url = f'https://mermaid.ink/img/{b64}?type=png&bgColor=FFFFFF'
req = urllib.request.Request(url, headers={'User-Agent': 'curl/8'})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = resp.read()
out = pathlib.Path(f'doc/uml/{slug}.png')
out.write_bytes(data)
print(f'saved: {out} ({len(data)} bytes)')
PY
```

**4.3 读图展示**

用 Read 工具读取 `doc/uml/<slug>.png`，让图片直接出现在对话里（Claude Code 多模态支持）。

**4.4 渲染失败降级**

网络不通 / `mermaid.ink` 503 / Mermaid 语法报错时：
- 保留 `.mmd` 源码文件（已落盘）
- 明确告诉用户失败原因（HTTP 码或异常）
- 给两条本地兜底：
  1. `npx -p @mermaid-js/mermaid-cli mmdc -i doc/uml/<slug>.mmd -o doc/uml/<slug>.png`
  2. 贴到 <https://mermaid.live> 手动导出
- **不要假装成功**，也不要跳过这一步直接进入 Step 5

### 5. 附随说明

图下方补充：
- **产物路径**：`doc/uml/<slug>.png` + `doc/uml/<slug>.mmd`
- **角色清单**：列出图中涉及的所有角色 / 系统
- **关键判定**：每个菱形分支的业务含义
- **待确认项**：还存在哪些尚未澄清的点（如果有）

### 6. 迭代优化

用户反馈后，**只改动被指出的部分**，保持其余节点不变；大改前先口头确认修改范围。改完后**重新走 Step 4**（覆写 `.mmd` → 重新渲染 → 重新读图），保证图和代码同步。

## 输出模板

```markdown
## 业务流程：<流程名>

### 角色
- <角色 A>
- <系统 B>

### 活动图
<Mermaid 代码块>

（此处应紧跟 Read 工具读出的 PNG 图像）

### 产物
- 图：`doc/uml/<slug>.png`
- 源码：`doc/uml/<slug>.mmd`

### 关键判定
- **<判定节点>**：<业务规则说明>

### 待确认
- [ ] <悬而未决的问题>
```

## 禁止事项

- [X] 跳过澄清直接画图（除非需求已极其明确）
- [X] 虚构角色 / 系统 / 字段
- [X] 一次性把所有分支画出来却不标注业务含义
- [X] 用纯文字描述替代活动图（用户要的是"图"）
- [X] 只贴 Mermaid 代码不渲染 PNG（除非 Step 4 明确失败并告知用户）
- [X] 渲染失败静默跳过，不告知用户
