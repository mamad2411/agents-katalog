---
name: thesis-ref-analysis
description: >-
  批量提取参考学位论文 PDF → 自动定位章节结构 → 与自己的论文对比分析。
  从参考学位论文目录中选取相关论文，用 pdftotext 提取全文，自动识别章节标题和结构，
  然后按章节逐段对比写作手法、论述逻辑、数据呈现方式。
  触发词：参考论文分析、对比参考论文、参考论文提取、论文对比、范文结构、参考范文、对标范文结构、ref analysis。
  边界：范文的**语体/口吻**对标（句子怎么写）→ thesis-style；本 skill 做**结构/章节/论述手法**的
  PDF 提取与逐章对比。
argument-hint: "[论文目录路径] [--chapters 1,2,3] [--compare mine]"
allowed-tools: Read, Bash, Write, Glob
triggers:
  - 参考论文分析
  - 对比参考论文
  - 参考论文提取
  - 论文对比
  - 参考论文结构
  - 范文结构
  - 参考范文
  - 对标范文结构
  - ref analysis
  - ref compare
---

# 参考论文批量提取与对比分析

从参考学位论文 PDF 中提取全文，自动定位章节结构，与自己的论文逐章对比。

## 工作流

### Step 1: 定位参考论文

```bash
REF_DIR="<MEM_ROOT>/参考学位论文"
ls "$REF_DIR"/*.pdf
```

根据用户需求选取相关论文（默认全部）。每篇论文用 `论文作者` 标识。

### Step 2: 批量提取全文

对每篇参考论文执行：

```bash
pdftotext "<pdf_path>" /tmp/ref_<author>_full.txt
wc -l /tmp/ref_<author>_full.txt
```

输出存放在 `/tmp/ref_<author>_full.txt`，后续步骤直接读取。

### Step 3: 自动定位章节结构

用 grep 识别章节标题模式：

```bash
grep -n "第.*章\|本章小结\|总结和展望\|研究结论\|研究局限\|展望\|摘要\|Abstract\|目录" /tmp/ref_<author>_full.txt | head -30
```

典型章节模式：
- `第1章 绪论` / `第1章 引言`
- `第2章 ...理论基础` / `第2章 ...现状分析`
- `第3章 ...问题分析` / `第3章 ...方案设计`
- `第N章 总结与展望` / `结论`
- `本章小结` — 各章末尾

输出每篇论文的章节映射表：`章节编号 → 起止行号 → 标题`

### Step 4: 按章节提取对比文本

根据章节映射，用 `sed -n 'start,endp'` 提取各章节文本：

```bash
sed -n '<start>,<end>p' /tmp/ref_<author>_full.txt > /tmp/ref_<author>_ch<N>.txt
```

### Step 5: 与自己的论文对比

读取用户自己的论文章节：

```bash
MY_THESIS="<PROJECT_ROOT>/zjuthesis/body/graduate/master"
ls "$MY_THESIS"/chapter*.tex
```

逐章对比维度：
1. **章节摘要写法**：是否有本章小结、位置、篇幅、承上启下方式
2. **论述结构**：问题→分析→方案→验证的逻辑链
3. **数据呈现**：表格/图表引用方式、数据解读深度
4. **过渡衔接**：章间过渡、段落衔接技巧
5. **语言风格**：学术用语规范、过度自信用语（"显著""充分证明"等）

### Step 6: 输出对比报告

输出格式：

```markdown
## 参考论文对比分析报告

### 论文概览
| 论文 | 作者 | 总页数 | 章节数 | 研究方法 |
|------|------|--------|--------|----------|

### 逐章对比
#### 第X章 [主题]
- **参考论文写法**：...
- **你的论文现状**：...
- **差距与建议**：...

### 可借鉴的写作模式
1. ...
2. ...

### 需要避免的问题
1. ...
```

## 注意事项

- pdftotext 提取中文 PDF 可能有乱码，遇到问题用 `-layout` 参数重试
- 参考论文目录路径固定为 `<MEM_ROOT>/参考学位论文/`
- 用户论文章节路径固定为 `<PROJECT_ROOT>/zjuthesis/body/graduate/master/`
- 对比时保持客观，指出差距但不贬低
- 重点关注可操作的改进建议，而非泛泛而谈
