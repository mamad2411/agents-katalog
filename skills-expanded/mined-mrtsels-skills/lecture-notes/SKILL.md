---
name: lecture-notes
description: 从讲座 PDF/课件生成结构化笔记。读取源 PDF 提取全文，匹配已有笔记格式风格，输出带术语表/公式/要点/快速对照表的 Markdown 笔记。适用于量化金融、编程、数学等课程。
version: 1.1.0
---

# Lecture Notes（讲座笔记）

从课程 PDF 生成结构化、可复习的 Markdown 笔记。

## 核心原则

**每条公式后面都要跟「说人话」。** 纯公式堆砌对新手不友好。必须在每个公式/模型后面附加：

1. **变量逐条注解（必做）** — 公式下方紧跟 `> 其中：` 块，按顺序解释每个符号的含义，附一句话翻译整条公式在说什么。格式：

   ```
   $$ Y = \beta_0 + \beta_1 X + \epsilon $$
   
   > 其中：$Y$ = 输出（要预测的值），$X$ = 输入（特征），$\beta_0$ = 截距（长期均值），$\beta_1$ = 斜率（$X$ 每变 1 单位 $Y$ 变多少），$\epsilon$ = 随机误差（模型解释不了的部分）
   ```

2. **直觉类比（生活中对应的例子）** — 用比喻/类比解释抽象概念

3. **具体的数值算例（用真实数字走一遍计算过程）** — 带时序的完整计算步骤，避免纯符号推导

4. **如果是可操作的（如模型选择），给出"拿到数据后怎么做"的实操指南**

> 反例：丢一个 MA(q) 的 ACF 公式就算完。
> 正例：公式 → `> 其中：` 变量解释 → 新闻冲击类比 → MA(1) 的 3 天数值算例 → "为什么 ACF 会截尾"的直观解释。

**⚠️ 检查清单：** 写完每条公式后检查——
- [ ] `> 其中：` 变量逐条解释写了吗？（每个符号一行）
- [ ] 至少有一个类比或直觉说明？
- [ ] 至少有一个带真实数字的算例？
- [ ] 如果涉及可操作流程，有实操指南吗？
- 三项缺一不可。只写公式不加注解 = 不合格。

**⚠️ 流程式内容的结构规则：** 当笔记涉及一个**可操作流程**（聚类、模型选择、回测流程等），必须按**实际执行顺序**组织小节：

   **Data Collection → Metric/Tool Definition → Run/Execute**

   而不是按概念名称（如"Similarity Measures"）独立成节。违反案例：上来就讲"距离度量"，不讲数据从哪来、怎么收集——用户会纠正为 Data collection → similarity metric definition → running the algorithm。

   > **正例（本文对话中用户的纠正）：**
   > 聚类 → 先写 Step 1 Data Collection（收数据、预处理），再写 Step 2 Similarity Metric Definition（定义距离），最后写 Step 3 Run Clustering Algorithm（指向具体算法小节）。
   >
   > **反例：** 直接以"Similarity Measures"作为 1.1 开头，跳过数据来源的交代。

## 触发条件

用户要求"写笔记"、"做笔记"、"整理笔记"、"总结这节课"、"need notes for lecture X"等，且指向 PDF 格式的课件/讲义。

## 工作流程

### 第 1 步：收集素材

1. 定位源文件：找到 `Lecture N.pdf`
2. **必做：** 读取已有的最近笔记（如 `Lecture N-1 Notes.md`）确认风格。不要猜风格，直接读文件。
3. 提取 PDF 文本：
   ```python
   import fitz
   doc = fitz.open("Lecture N.pdf")
   for i, page in enumerate(doc):
       text = page.get_text()
       if text.strip():
           print(f'--- Page {i+1} ---')
           print(text)
   doc.close()
   ```
4. 如果提取文本过少或缺失公式/图表（slide 型 PDF 常见），改用 vision 提取：
   ```python
   import fitz, os
   doc = fitz.open("Lecture N.pdf")
   os.makedirs(f"lecture{N}_frames", exist_ok=True)
   for i, page in enumerate(doc):
       pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
       pix.save(f"lecture{N}_frames/page_{i+1:02d}.png")
   doc.close()
   ```
   然后用 `vision_analyze` 逐页提取，每轮并发 5 页。全部完成后删除临时帧目录。
   
   **参考：** `references/vision-extraction-batching.md` for the exact conversion + extraction commands.

### 第 2 步：确定风格

**读同课程已有的笔记文件来匹配风格，不要假设。** 主流风格：

### 第 2b 步：确认文件名约定

检查已有笔记文件命名模式（如 `Lecture 12 Notes.md`、`Lecture 13 Notes.md`），用**单数字**（`Lecture 6 Notes.md`）而非零填充（`Lecture 06 Notes.md`）。遵循同一目录下已有文件的约定。

#### 风格 A — 英中对照式（量化金融课主流）

```
标题：     # Lecture N — Topic
章节：     ## N Topic / ### N.M Subtopic
正文：     中文，英文术语加括号标注（English Term）
Callout：  > 引号引导的数字例子和直觉类比
表格：     用于对比
公式：     $...$ 或 $$...$$
末尾：     Glossary（术语表 | 含义 两栏）
```

**Callout 标签惯例（量化金融）：**

| 标签 | 用法 | 示例 |
|------|------|------|
| `> **类比：**` | 通俗比喻解释抽象概念 | 两个人绑在一起蹦极，一个人偏离时会被拉回来 |
| `> **用数字看：**` | 具体数字演示计算 | spread=2.5 → 卖空 → 回归0 → 获利2.5 |
| `> **数值举例：**` | 带时间序列的实际数据演示 | 股票价格 [100,102,105,103,101] → 差分后的结果 |
| `> **思考题：**` | 触发读者思考的问题 | 一个异常区间对MAE/MSE的影响各多大？ |
| `> **对比：**` | 两种概念的对比 | 高相关但不协整 vs 低相关但协整 |
| `> **分析：**` | 深入拆解 | 各指标受冲击程度排名 |
| `> **直观理解：**` | 直觉解释 | Kalman Gain = 可信度权重 |
| `> **实操指南：**` | 拿到数据后怎么按步骤做 | 看 ACF 截尾还是拖尾 → 选模型 → 诊断残差 |

**KaTeX pitfalls:** See `references/katex-pitfalls.md` — bare `*` inside `$...$` causes parse errors; use `\ast` instead.

**完整样例（量化金融风格）：**

```markdown
### 2.2 衡量「走在一起」—— 相关 vs 协整

**Correlation（相关）：** 衡量两个序列之间的线性关系强度。

$$r = \frac{\frac{1}{n}\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\dots}}$$

> $r$ 越接近 1 或 -1 说明线性关系越强，但它不能衡量「两只股票是否贴在一起走」。

**Cointegration（协整）：** 如果 $z_t = y_{1,t} - \gamma y_{2,t}$ 是**平稳的**（围绕一个均值长期波动），则称两时间序列是协整的。

> **对比：**
> - 相关性高但**不**协整：两只股票走势看起来像，但价差越拉越大
> - 相关性低但**协整**：价差围绕均值随机波动，偏离后会回归

| 形式 | 含义 |
|------|------|
| **Weak Form** | 历史价格数据不能预测未来 |
```

#### 风格 B — 纯英文

全英文，章节标题 Title Case，表格/公式/代码块同上，无末尾术语表。

### 第 3 步：撰写笔记

按 slide 顺序组织，合并逻辑相关的内容：

1. **标题信息** — 课程名、讲师、版本、页码
2. **目录**（如有 TOC slide）
3. **各章节内容**
4. **公式** — LaTeX 排版，**每条公式后紧跟：**
   - `> 其中：` 变量逐条注解（每个符号一行，含数值含义和一句话翻译）
   - `> **直觉：**` 类比/直觉解释（可选，但推荐）
   - `> **数值举例：**` 带真实数字的算例（可选，但推荐）
5. **图表说明** — 从 Figure caption 重建对比表。对于需要视觉还原的复杂图表（dendrogram、流程图、示意图），使用 `svg-from-pdf-figure` skill 将 PDF 中的图片重建为独立 SVG 文件，嵌入 Markdown 笔记中。SVG 文件存放规则：
   - 和笔记放在同一目录下
   - 文件名全小写 + 连字符（如 `lecture15-dendrogram.svg`）
   - 在笔记中用 `![Alt Text](filename.svg)` 相对路径引用
   - 同一次 commit 提交 .md 和 .svg 文件
6. **Glossary（术语表）** — 风格 A 必加

**⚠️ 防公式堆砌检查：** 写完每条公式后问自己「一个从没学过这课的人看完这段能懂吗？」如果不能，至少加一个类比或数值算例。理想情况是三者都加：公式 → 类比直觉 → 数字走一遍。

### 第 4 步：检查遗漏

PDF 文本提取通常会遗漏：
- 图表/示意图的文字说明 → 从 vision 分析结果提取 Figure caption
- 表格数据 → 提取文本中表格可能变形，根据上下文重建对比表
- 对比图 → 从 slide 文字描述重建表格

### 第 5 步：验证 + 清理

- 确认所有 slide 都覆盖到
- 确认风格 A 关键术语都有中文对照
- 确认公式表述清晰
- 确认 Glossary 表齐全
- 清理临时帧目录：`rm -rf lecture{N}_frames`

## 格式模板（风格 A）

### 章节标题
```
## N Topic

### N.M Subtopic
```

### 术语表（全文末尾）
```markdown
| 术语 | 含义 |
|------|------|
| **English Term** | 中文解释 |
```

### 公式 + 数字例子
```markdown
$$ r = \frac{1}{n}\sum (X_i - \bar{X})(Y_i - \bar{Y}) / \dots $$

> **用数字看：** 如果 X=[1,2,3], Y=[2,4,6]，r=1 完美正相关。
```

### 直觉 Callout
```markdown
> **类比：** 通俗比喻解释概念
> **用数字看：** 具体数字演示计算过程
```
