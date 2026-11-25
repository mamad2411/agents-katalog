---
name: conventions
version: 1.0.0
description: 全局行为规范 — 代码注释用中文、Bash 命令附解释、英文步骤附中文翻译、思考链强制中文（可留术语但主干必须中文）。每次生成代码、执行终端命令、输出英文内容、进行内部思考推理时自动加载。触发词：写代码、生成、注释、运行命令、解释、翻译、thinking、推理、思维链。
---

# 全局行为规范

以下三条规则在**所有对话**中默认生效，除非用户明确要求例外。

---

## 规则 1：代码注释默认中文

生成任何代码（Python、Java、JS、SQL、Shell 等）时，**注释、docstring、文档字符串默认使用中文**。

```python
# ✅ 正确 — 中文注释
def calculate_score(answers: list[dict]) -> float:
    """
    根据答题结果计算最终得分。
    每道题权重相同，答对 +1，答错 +0，未答跳过。
    """
    score = 0.0
    for item in answers:
        if item.get("correct"):  # 仅统计已答且正确的题目
            score += 1.0
    return score
```

```python
# ❌ 错误 — 未经要求就写英文注释
def calculate_score(answers):
    # Calculate final score based on answers
    score = 0.0
    ...
```

**例外**：仅当用户明确说"注释写英文""用英文注释""comments in English"时，才使用英文注释。

---

## 规则 2：Bash 命令必须先解释再请求执行

每次向用户展示终端命令时，**必须附带中文解释**，说明：
- 这条命令**做什么**（功能描述）
- 为什么**需要执行它**（意图）

格式：

````text
**这条命令的作用**：<一句话中文说明>
**为什么需要**：<一句话中文说明>

```bash
<命令>
```
````

**实际示例**：

````text
**这条命令的作用**：安装 psycopg2-binary Python 数据库驱动包
**为什么需要**：本地脚本需要通过此驱动连接 PostgreSQL 数据库读写数据

```bash
python3 -m pip install psycopg2-binary
```
````

当需要用户审批权限时，解释尤为重要——让用户**不需要读 bash 代码**就能判断该不该批准。

**适用范围**：需要用户审批的命令、有副作用的命令（写入/删除/安装/网络请求）。
连续的只读探查命令（`ls`/`cat`/`grep`/语法检查）只需在一组的开头说明一次意图，
不必逐条重复——否则批量排查时解释文字会淹没实际结果。

---

## 规则 3：英文步骤附中文翻译

当你输出英文技术步骤、名词、流程时，**在括号中附带中文翻译/注释**，方便用户快速理解。

```
# ✅ 正确
Step 1: Extract the error-fix chain from the conversation.（从对话中提取错误-修复链）
Step 2: Classify each error by category — env / type / logic / external.（按类别分类）
Step 3: Write confirmed items to PgSQL and Obsidian.（写入数据库和笔记）

# ❌ 错误
Step 1: Extract the error-fix chain from the conversation.
Step 2: Classify each error by category — env / type / logic / external.
Step 3: Write confirmed items to PgSQL and Obsidian.
```

这适用于：
- 技术步骤/流程说明
- 工具/库名称的首次提及（如 "PostgreSQL（关系型数据库）"）
- 架构图中的节点和箭头标注

**例外**：纯代码块（``` 包裹的内容）不需要翻译代码本身；公认的技术缩写（API、JSON、SQL、HTTP）不需要翻译。

---

## 规则 4：思考过程使用中文

你的内部推理（thinking / reasoning）**使用简体中文**。

ALL thinking/reasoning MUST be in Simplified Chinese. Code snippets, error messages, and file paths within thinking can remain in their original language — but your own reasoning text must be Chinese.

<!-- 设计说明（对模型）：这条规则不能加"强制/最高优先级"式措辞。思考语言是表达偏好，不是执行流程约束。
用 🚫 禁止级别的强度写它，会挤占真正需要强制的规则（如流水线步骤、破坏性操作确认）的注意力权重。
语言切换不影响推理质量，但把偏好升格成铁律会让模型在语言和正确性之间做无意义的权衡。 -->

### 中文思考的具体要求

| 允许保留英文 | 禁止 |
|:---|:---|
| 关键术语：API、JSON、SQL、HTTP、CUDA、JIT | ❌ 整段、整篇思考链全用英文 |
| 专有名称：PyTorch、PostgreSQL、DeepSeek | ❌ 连续 3+ 句推理全部英文 |
| 代码/变量名/函数名（原文引用） | ❌ 仅因"懒得切换语言"而用英文思考 |
| 错误信息/堆栈追踪（原文引用） | ❌ 英文写出完整分析段落 |
| 文件路径/URL | ❌ 让用户看不懂你在想什么 |

**核心原则**：用户是中文母语者，思考链是给用户看的（方便他跟踪你的推理逻辑），必须确保用户**大致能看懂**你在想什么。可以夹杂英文术语，但主干推理必须用中文表达。

<!-- 自检：如果你的思考链扔给一个英语不太好的中国大学生看，他能否理解你的推理方向？不能就说明英文太多了。 -->

<!-- 注意：
- 这只是语言切换，不影响推理深度和质量
- 代码、错误信息、API 响应、文件路径等原文引用不需要翻译
- Skill 的 description 字段和触发关键词不受影响——思考过程不参与 Skill 匹配判定 -->

---

## 速查

| 场景 | 行为 |
|:---|:---|
| 生成代码 | 注释/文档 → 中文（除非用户要求英文） |
| 请求执行 Bash 命令 | 先附中文解释（做什么 + 为什么），再展示命令 |
| 输出英文步骤/术语 | 括号附中文翻译 |
| 纯代码块 | 不需要翻译代码本身 |
| 公认缩写（API/JSON/SQL/HTTP） | 不需要翻译 |
| 内部思考/推理 | 中文为主（术语/专名可保留英文，但主干推理必须中文，确保用户能看懂） |
| Skill 触发关键词 | 不受影响（思考过程不参与匹配） |
