---
name: undergrad-thesis-self-check
description: 给南京大学软件学院、智能软件与工程学院**本科**毕业论文送审前的自检 skill。学生提供论文 PDF，先从 PDF 抽题目并请学生确认，自动判定"工程型 / 学术型"并请学生确认，再询问"是否团队子模块"（如是追问总项目+本人模块），按对应类别 25-28 条 checklist（含 3-4 条红线）逐项审查，给出带原文页码定位的反馈、红线高亮，最后写到 <论文同目录>/<论文题目>-review.md（题目来自 PDF 内容而非文件名）。**不做**优/良/中/及格/不及格的总分估计。仅在用户明确说"本科论文自检""本科论文自查""本科送审前自查""我的本科论文有什么问题"等触发词且提供 PDF 路径时启用。
---

# NJU SE 本科论文自检 skill

给本科生送审前自查用。本 skill 是学生视角的 checklist 逐项审查。

## 何时使用

仅在用户明确说出以下触发词之一**且**提供论文 PDF 路径时启用：
- 「本科论文自检」「本科论文自查」「本科送审前自查」
- 「我的本科论文有什么问题」「我的本科论文能过吗」
- 「undergrad self-check」「pre-defense check」（且提供 PDF）

不要只看到 PDF 就触发。

## 调用格式

```
本科论文自检 /path/to/paper.pdf
本科论文自检 /path/to/paper.pdf --type=engineering   # 跳过类型判定
本科论文自检 /path/to/paper.pdf --type=academic
本科论文自检 /path/to/paper.pdf --type=engineering --team   # 标记团队论文（仍会追问总项目+模块）
```

`--type` 可选值：`engineering`（工程型）/ `academic`（学术型）。
`--team` 标记团队子模块；不带则进入团队 Gate 询问。

## 前置依赖

- `pdfplumber`：如缺失提示用户 `pip install pdfplumber`
- 本 skill 自带 `scripts/extract_skeleton.py`，无需依赖外部 skill

## 主流程（9 步）

### 步骤 1：抽骨架 + 抽取论文题目

```bash
TITLE_HINT=$(basename "/path/to/paper.pdf" .pdf)
python3 ~/.claude/skills/undergrad-thesis-self-check/scripts/extract_skeleton.py \
  "/path/to/paper.pdf" \
  --out "/tmp/nju-undergrad-self-check-${TITLE_HINT}-skeleton.md"
```

读骨架。如脚本失败 / 骨架 < 30 页 / 章节切分退化（出现"未识别章节"）：
- 先告知用户骨架异常，列出问题，问是否继续（基于不完整骨架审查会漏检）。
- 本科论文一般 ≥ 35 页（15k 字 ÷ 约 400 字/页 ≈ 38 页），骨架 < 30 页提示偏低。

**抽取论文题目**（用于步骤 8 的报告文件名）。4 策略按优先级依次尝试：

```python
# 直接从 PDF 前 10 页提取头部文本来找题目
# 策略 1：NJU SE 本科封面 "题目：" 行（回归测试 8/9 命中，优先）
# 策略 2：摘要首页"毕业论文题目：" 行（模板备用）
# 策略 3：封面"论 文 题 目" 区段多行合并（专硕封面模板）
# 策略 4：fallback 到 PDF 文件名

import re, pdfplumber, os
PDF = "/path/to/paper.pdf"
title = None

with pdfplumber.open(PDF) as pdf:
    head_text = '\n'.join((p.extract_text() or '') for p in pdf.pages[:10])

# CID 编码检测：若头部 CID 标记过多或中文字符极少，提前警告
cid_count = head_text.count('cid:')
cjk_count = sum(1 for c in head_text if '一' <= c <= '鿿')
if cid_count > 50 or cjk_count < 100:
    print(f"警告：PDF 疑似 CID 编码（cid: 出现 {cid_count} 次，中文字符仅 {cjk_count} 个），"
          f"文字无法正常提取，题目抽取将大概率失败，建议直接使用文件名作为题目。")

# 策略 1（NJU SE 本科模板）：题目[：:] … 至下一个字段
m = re.search(
    r'题目[：:]\s*([\s\S]{1,150}?)(?=\n院系|\n学院|\n专业|\n本科生姓名)',
    head_text
)
if m:
    title = re.sub(r'\s+', '', m.group(1)).strip()

# 策略 2（备用模板）：毕业论文题目[：:] … 至下一个字段
if not title:
    m = re.search(
        r'毕业论文题目[：:]\s*([\s\S]{1,150}?)(?=(?:本科|学士学位|学生姓名|指导教师|学\s*校\s*代\s*码|软件工程专业|计算机.{0,4}专业|.{0,8}\d{4}\s*级\s*本科生))',
        head_text
    )
    if m:
        title = re.sub(r'\s+', '', m.group(1)).strip()

# 策略 3（专硕封面模板）：论 文 题 目 多行区段
if not title:
    m = re.search(r'论\s*文\s*题\s*目\s*([\s\S]{0,200}?)(?=作\s*者\s*姓\s*名|学位类别|研\s*究\s*方\s*向|学\s*生\s*姓\s*名)', head_text)
    if m:
        title = re.sub(r'\s+', '', m.group(1)).strip()

# 策略 4：fallback 到文件名
if not title or len(title) < 5:
    title = os.path.splitext(os.path.basename(PDF))[0]
    print(f"警告：未能从 PDF 内容抽取题目，回退到文件名: {title}")

# 清洗
title_clean = re.sub(r'[\\/:*?"<>|\r\n\t]', '', title).strip()
if len(title_clean) > 120:
    title_clean = title_clean[:120]
print(f"PAPER_TITLE={title_clean}")
```

### 步骤 2：题目确认 Gate

告诉用户抽取到的题目，让用户确认或纠正：

```
从 PDF 抽取到的论文题目：
《{title_clean}》

报告将写到：<论文同目录>/{title_clean}-review.md

确认输入 y 继续；如题目错误请直接给出正确题目。
```

### 步骤 3：类型判定 Gate（工程型 / 学术型）

读骨架的元信息 + 各章首页文本，按以下规则判别：

| 信号 | 工程型 | 学术型 |
|---|---|---|
| 题目关键词 | "系统/平台/工具的设计与实现"、"模块"、"管理系统" | "方法研究"、"基于 X 的 Y 方法"、"X 算法/模型"、"面向 X 的 Y" |
| 第二章篇幅与重心 | 偏"技术栈介绍"（Spring、K8s、LLM 框架等） | 偏"相关工作综述"（按方法/路线分类） |
| 第三/四章 | "需求分析 / 系统架构 / 详细设计 / 实现" | "问题形式化 / 方法设计 / 实验设计" |
| 是否有"系统测试"或"运行截图"章 | 通常有 | 通常无 |
| 是否有"实验对比"章 | 弱（功能验证为主） | 强（基线对比 + 评价指标） |
| 关键句信号词 | "本系统"、"模块"、"部署"、"接口" | "提出"、"实验表明"、"结果表明"、"基线" |
| 摘要核心 | 系统的功能与工程价值 | 方法的创新与实验结论 |

**输出格式（无 emoji）**：

```
论文类型判别
------------------------------------------------------------
论文标题：《...》
我判定为：【工程型 / 学术型】
判定依据：
1. [一条具体证据，含章节或页码]
2. [第二条]
3. [第三条]

请确认：
- 输入 y / 工程 / 学术 来确认或纠正
- 如果是混合型，请告诉我重心偏向哪一类
```

如果用户提供了 `--type=...` 跳过本 Gate。

### 步骤 4：团队子模块 Gate

**默认问，不自动猜**：

```
团队论文判定
------------------------------------------------------------
本论文是否为团队项目中的一个子模块？
（团队项目 = 多人协作、各自负责一个模块、各写一份论文，
  例如 SELABS 类的"统计安全 / 空间预约 / 资产管理"四模块拆分）

输入 y / 是 / team / n / 否 / solo
```

如答 yes，追问：

```
请提供两条信息（用 / 分隔）：
  1. 团队总项目名称（如：SELABS）
  2. 你负责的模块名（如：统计与安全管理模块）

格式示例：SELABS / 鉴权与数据中心管理模块
```

把 `team_project` / `my_module` 存为 shell 变量供后续使用。

### 步骤 5：加载对应 reference + 应用 overrides

按确认的类别读取：
- 工程型：`~/.claude/skills/undergrad-thesis-self-check/references/engineering-30.md`（28 条）
- 学术型：`~/.claude/skills/undergrad-thesis-self-check/references/academic-30.md`（26 条）

如团队 = yes：再读 `~/.claude/skills/undergrad-thesis-self-check/references/team-submodule-overrides.md`，对若干条目应用 patch（替换 / 放宽 / 追加 UND-TEAM-DECL）。

**学术型读取的特殊性**：academic-30.md 中前 18 条（RED-1/2/4 + UND-ENG-A-01..10 + UND-ENG-B-01..04,B-10 + UND-ENG-C-02..04）是"占位指引"，加载时应回到 engineering-30.md 读取对应 ID 条目的完整 yaml；只有 UND-ACA-S-01..05 的 5 条专属条目在 academic-30.md 中完整定义。

具体实现：审查每条时，按 ID 前缀决定从哪个文件取条目内容：
- UND-RED-* / UND-ENG-* → engineering-30.md
- UND-ACA-S-* → academic-30.md

### 步骤 6：红线扫描

先把红线（工程 4 条 / 学术 3 条）跑一遍。每条按 reference 文件里的"检查方法"操作：
- 若全文有 grep 类检查 → 用 Bash 在骨架文件上 grep
- 若涉及篇幅 → 从骨架元信息读 page_start / page_end + 字符密度估算
- 若涉及章节内容 → Read 骨架对应章节段落

记录红线命中数，**不要在此停下**，继续步骤 7。

### 步骤 7：全量审查（剩余 ~25 条）

按 reference 文件中的顺序逐条审查。每条遵循"评判 + 定位 + 修改建议"模式：

**单条审查的内部模板**（合格项写一行；警告/不合格项展开）：

```yaml
- id: UND-ENG-A-05
  状态: ✅ / ⚠️ / ❌
  位置: P.42-44, §3.2.1（仅警告/不合格时给）
  评语: "评审专家口吻，1-3 句"（仅警告/不合格时给）
  修改建议: "具体怎么改"（仅警告/不合格时给）
```

**评语口吻参考**：
- 不写"你应该……"，写"建议在 X 章节补充 Y……"
- 不写"这里错了"，写"X 表述与 Y 不一致，建议……"
- 不堆套话；每条建议必须包含至少一处可定位的位置（章节号或页码）

**当某条审查需要更细节时**：用 Read 跳读骨架对应章节，必要时 Read 原 PDF（用页码范围）。但 80% 的判断应该在骨架上完成。

### 步骤 8：生成报告

按下面格式拼装报告。**不要在对话里贴完整报告**，写到磁盘：

```
<论文 PDF 同目录>/<论文题目>-review.md
```

如同名文件已存在 → 改写到 `<论文题目>-review-YYYYMMDD-HHMMSS.md` 避免覆盖。

#### 报告模板

```markdown
# 本科论文自检报告 — YYYY-MM-DD

**论文**：<原 PDF 文件名>
**抽取题目**：《...》
**类别**：工程型 / 学术型（已确认）
**团队论文**：是 / 否
  - 团队项目：SELABS（仅 yes 时）
  - 本人模块：统计与安全管理模块（仅 yes 时）
**生成**：本报告由 undergrad-thesis-self-check skill 生成，仅供学生自查参考

---

## 一、首页摘要

| 项 | 数 |
|---|---|
| 🔴 红线命中 | X |
| ⚠️ 警告 | Y |
| ✅ 通过 | Z |
| 总条目 | 28（工程型）/ 26（学术型）|

### 必须先修的红线项

[命中时逐条展开；未命中写"✅ 无红线命中"]

---

## 二、🔴 红线条目（工程 4 / 学术 3 条全列）

[逐条展开]

---

## 三、学术质量（10 条）

按 ❌ → ⚠️ → ✅ 顺序排列，警告与不合格在前。

[逐条展开]

---

## 四、结构内容（工程 10 / 学术 5 条）

[逐条展开]

---

## 五、格式细节（工程 4 / 学术 3 条）

[逐条展开]

---

## 六、（仅学术型）实验与方法专项（5 条）

[仅学术型展开]

---

## 七、（仅团队论文）团队论文专项检查

[override 命中条目 + UND-TEAM-DECL 状态]

---

## 八、修改 checklist（待勾选）

- [ ] [UND-RED-2] 字数补到 15,000 以上
- [ ] [UND-ENG-A-07] 图 3-2 / 图 4-5 在正文未被引用，补"见图 X-Y"或删图
- ...
```

### 步骤 9：对话输出摘要

只贴：

```
论文自检完成。

报告路径：/Users/.../<题目>-review.md

类别：工程型（团队论文 — SELABS / 统计与安全管理模块）
统计：🔴 红线 1 条 / ⚠️ 警告 5 条 / ✅ 通过 22 条 / 共 28 条

🔴 必须先修：
  1. [UND-RED-2] 正文字数约 12,800，未达 15,000 底线
     建议在第 3 章需求分析扩充约 2,200 字

详细分项与修改建议见报告。
```

**不输出**：
- 评议结论估计（本科版不做）
- 28 条逐条状态（避免刷屏）
- 独立的免责声明段（报告头部一句话即可）

## 红线触发后的特别提醒

报告顶部和对话里都要明确提醒：

> 🔴 命中 X 条红线。这些是评审"一票否决"或"严重影响通过"的项，建议优先修改完毕后再处理其他警告项。
