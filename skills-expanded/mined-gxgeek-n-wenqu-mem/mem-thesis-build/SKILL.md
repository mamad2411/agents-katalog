---
name: mem-thesis-build
description: >-
  ZJU MEM 论文 LaTeX 编译。格式预检→环境验证→四遍编译→PDF输出验证。支持 quick/full/clean 模式。
  触发词：编译论文、build thesis、编译、生成PDF、LaTeX、xelatex。
argument-hint: "[quick|full|clean]"
allowed-tools: Read, Bash
---

# ZJU MEM 论文 LaTeX 编译

基于 zjuthesis 模板的完整编译工作流。

## 模板与环境

### 模板路径
论文 LaTeX 源码位于项目 `zjuthesis/` 目录，主文件 `zjuthesis.tex`。典型结构：
```
zjuthesis/
├── zjuthesis.tex          # 主文件
├── body/ref.bib            # 参考文献
├── body/graduate/master/   # 正文章节 (chapter1-7.tex)
├── page/graduate/          # 封面/摘要/声明等
└── config/                 # 格式/命令/宏包配置
```

### 编译环境要求
- **XeLaTeX**：TeX Live 2024+（Mac: MacTeX，Windows: TeX Live，Linux: `apt install texlive-xetex`）
- **Biber**：参考文献编译（通常随 TeX Live 安装）
- **中文字体**：宋体（SimSun/STSong）、黑体（SimHei/STHeiti）、仿宋（FangSong/STFangsong）、楷体（KaiTi/STKaiti）
  - Mac：系统自带，无需额外安装
  - Windows：系统自带
  - Linux：`apt install fonts-wqy-zenhei fonts-wqy-microhei`
- **可选**：`latexmk`（自动化编译）、`pygmentize`（代码高亮）

### 环境验证
```bash
which xelatex && xelatex --version | head -1
which biber && biber --version | head -1
fc-list :lang=zh | grep -i "song\|simsun\|宋" | head -1
fc-list :lang=zh | grep -i "hei\|simhei\|黑" | head -1
```

## 编译流程

### Step 1: 格式预检
编译前快速检查 `references/zju-format-rules.md`（完整预检清单与 PDF 输出验证清单见 `references/build-precheck-and-verification.md`）：
- [ ] 图表自明性：图题下图上方表，按章编号（图 X.Y / 表 X.Y）
- [ ] 三线表（顶线、栏目线、底线）
- [ ] 章节编号阿拉伯数字（1, 1.1, 1.1.1）
- [ ] 参考文献 GB/T 7714-2015，全文统一
- [ ] 公式独立成行，编号右对齐

### Step 2: 四遍编译
```bash
cd <项目路径>/zjuthesis
export PATH="/Library/TeX/texbin:$PATH"  # Mac 加此条

# 1. 生成 aux + toc
xelatex -interaction=nonstopmode zjuthesis

# 2. 处理参考文献
biber zjuthesis

# 3. 插入引用 + 交叉引用
xelatex -interaction=nonstopmode zjuthesis

# 4. 最终解决所有引用
xelatex -interaction=nonstopmode zjuthesis
```

### Step 3: 错误诊断
编译失败时读 `.log` 文件：

| 错误 | 原因 | 解决 |
|------|------|------|
| `Undefined control sequence` | 未定义命令 | 检查拼写，确认宏包已加载 |
| `Citation XXX undefined` | 引用 key 不存在 | 检查 .bib；重跑 biber |
| `Font ... not found` | 缺中文字体 | 安装对应字体 |
| `Overfull \hbox` | 文字超版心（警告） | 调整断词或手动断行 |
| `File XXX not found` | 缺少文件 | 检查 input/include 路径 |

### Step 4: PDF 验证
- [ ] PDF 成功生成，3-10MB
- [ ] 封面信息正确（题目/姓名/学号/导师/学院）
- [ ] **学位类型正确**（专业硕士易错，见下方陷阱）
- [ ] 目录页码与正文一致
- [ ] 图表编号连续，无空白页

> **⚠️ 专业学位封面陷阱（MEM/MBA/MPA 等）**：zjuthesis 模板用 `zjuthesis.tex` 的 `Type` 字段区分学位类型——
> - **专业学位**须设 `Type=design`：封面显示「硕士专业学位论文」+「专业学位类别／专业学位领域」（`\Major`/`\Topic` 分别填类别与领域）；
> - **学术学位**才用 `Type=thesis`：封面显示「硕士学位论文」+「学科(专业)／研究方向」。
>
> `graduate/master` 下的 `design` 分支只改封面标题与字段标签，**不会**触发本科模板里的「毕业设计」字样（那仅在本科评分表）。若封面出现「专业学位类别/领域」字段却仍写「硕士学位论文」，即为 `Type` 设成了 `thesis` 的混搭错误。

## 参数模式

| 参数 | 行为 |
|------|------|
| `quick` | 仅一遍 xelatex（快速预览） |
| `full`（默认） | 四遍编译（xelatex→biber→xelatex→xelatex） |
| `clean` | 清理辅助文件后重新四遍编译 |

构建完成后，若项目提供 `scripts/thesis_quality.py`，调用
`thesis-quality-gate` 执行 `state refresh` 和 `doctor`，使页数、PDF 哈希与构建
结果绑定到当前提交。正式交付再运行对应阶段的 `gate`。
