---
name: cn-patent-drafter
description: 起草、修订或合规自检中国发明专利（CNIPA 发明专利）申请文件——请求书、说明书摘要、权利要求书、说明书、说明书附图。当用户提及"发明专利""权利要求""说明书""CNIPA""[0001]""分案""答复审查意见"，或要求修改 patent-tex 项目下任意 .tex 文件时触发。仅处理 CN 发明专利申请材料；软件著作权 / 实用新型 / 外观设计不在范围内。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# CN 发明专利起草助手

本 Skill 帮助起草符合 CNIPA 2025–2026 现行规范的中国发明专利申请文件。Skill 内置：

- 4 套 LaTeX 模板（请求书 / 摘要 / 权利要求书骨架 / 说明书六小节段号阶梯）
- 1 套 10 大类 CNIPA 2026 合规清单
- 1 套结构化工作流，把"读清单 → 援引代码事实 → 套模板 → 写前自检 → 出 PDF"串起来

## 工作流

任何专利章节起草/修订任务都按以下顺序执行：

1. **加载合规清单** — 读本 Skill 目录下的 `checklists/cnipa-2026.md`，把每条要求加载到工作记忆里。
2. **定位目标章节** — 用户的请求映射到下列文件之一（约定项目里 LaTeX 源放在 `docs/patent-tex/sections/`）：
   - 请求书：`docs/patent-tex/sections/01-request.tex`
   - 摘要 + 摘要附图：`docs/patent-tex/sections/02-abstract.tex`
   - 权利要求书：`docs/patent-tex/sections/03-claims.tex`
   - 说明书：`docs/patent-tex/sections/04-specification.tex`
   - 说明书附图：`docs/patent-tex/sections/05-drawings.tex`
   先 Read 该文件再决定改动范围。如果项目里还没有这些文件，按本 Skill 目录下的 `templates/` 与下方"项目脚手架"小节自建。
3. **援引代码事实** — 任何对算法、数据结构、阈值、参数的描述都要直接对应实际源码。Grep 用户项目里的实现文件，把函数名、变量名、常量取值原样写入"具体实施方式"小节，最大化"充分公开"防绕设计。如果项目尚无实现，提示用户先实现再写专利。
4. **使用模板** — 生成新内容时优先以下骨架（位于本 Skill 目录下的 `templates/`），按需替换 `__PLACEHOLDER__`：
   - `templates/claim-skeleton.tex` — 独立权 + 从权 + 系统权骨架
   - `templates/spec-section-headers.tex` — 说明书六小节 + 段号 [0001] 阶梯
   - `templates/abstract-skeleton.tex` — 摘要 ≤ 300 字范本
   - `templates/request-form.tex` — 请求书表格
5. **写前自检** — 把草稿对照 `checklists/cnipa-2026.md` 逐条核验，特别关注：
   - 五文档顺序：请求书 → 摘要 → 权利要求书 → 说明书 → 附图
   - 说明书段号 `[0001]` 全文连续，不按小节重置
   - 摘要 ≤ 300 汉字、摘要附图最多 1 张
   - 权利要求逐条阿拉伯数字编号，禁用"如权利要求……所述"循环引用
   - 不出现商标、第三方品牌、竞品截图、源码 URL
   - AI 不得列发明人；起草中如使用 AI 辅助应限于排版/润色，技术构思与参数由发明人独立完成
6. **写入并提示编译** — 用 Write/Edit 落盘后，告知用户用 `xelatex`/`latexmk -xelatex` 重新出 PDF；若用户尚未填发明人/申请人等字段，提示在项目根的本地配置（如 `docs/soft-copyright.local.json` 或自定义路径）填 `inventionTitle` / `inventor` / `applicant` / `filingDate` 四项。

## 项目脚手架（首次使用时建议结构）

```
your-project/
├── docs/
│   └── patent-tex/
│       ├── main.tex                  # 用 ctexart + fontset=windows + xelatex 编译
│       ├── local-config.tex          # \renewcommand 覆盖默认占位宏（gitignore）
│       └── sections/
│           ├── 01-request.tex
│           ├── 02-abstract.tex
│           ├── 03-claims.tex
│           ├── 04-specification.tex
│           └── 05-drawings.tex
└── .claude/
    └── skills/
        └── cn-patent-drafter/        # 本 Skill clone 到这里
```

`main.tex` 主壳推荐 preamble：

```latex
\documentclass[UTF8,fontset=windows,zihao=-4]{ctexart}
\usepackage[a4paper,left=22mm,right=22mm,top=24mm,bottom=22mm]{geometry}
\usepackage{graphicx,array,booktabs,longtable,tabularx,enumitem,fancyhdr}
\usepackage{hyperref,caption,float,setspace,xcolor,amsmath,amssymb}
\setstretch{1.45}\setlength{\parindent}{2em}

\newcommand{\paragraphno}[1]{\noindent[\textbf{#1}]\hspace{0.5em}\ignorespaces}
\newenvironment{claimitem}{\begin{enumerate}[label=\arabic*., leftmargin=2em, itemsep=0.4em]}{\end{enumerate}}
\newcommand{\zonecode}[1]{\texttt{#1}}
\newcommand{\redblank}[1]{{\color{red}\underline{\hspace{#1}}}}
```

完整 working 示例见 `examples/sample-output.pdf`，对应原仓库参考实现：
[handsomeZR-netizen/eldercare-monitor 智慧养老监护系统](https://github.com/handsomeZR-netizen) 的 `docs/patent-tex/`。

## 常见任务速查

- 「补一条从权」→ 读 03-claims.tex，按现有 `\item` 节奏在 `\begin{claimitem}…\end{claimitem}` 内追加；从权必须明确"根据权利要求 N 所述"且 N 严格小于本条号
- 「扩写 [0033] 段」→ 读 04-specification.tex，找到对应段号；若需新增段号，把后续所有段号顺次 +1（先 Grep 再 Edit 全替换确保一致）
- 「换发明名称」→ 改本地配置（如 `docs/soft-copyright.local.json` 的 `inventionTitle`）；不要直接改 main.tex（其只承担默认值）
- 「画新附图」→ 把图文件放到 `docs/diagrams/` 或 `docs/screenshots/`，再编辑 05-drawings.tex 增加 `\begin{figure}` 块，并在 04-specification.tex 的「附图说明」段追加一行 `\paragraphno{...} 图 N 是…`
- 「合规自检」→ 直接对照 `checklists/cnipa-2026.md` 逐条核验当前 PDF；不通过项要在响应中明确列出

## 输出风格

- 中文为主、术语规范："实施方式"不写"实现方式"；"特征在于"不写"特点是"；"包括以下步骤"不写"包含如下步骤"
- 段落首行缩进由 LaTeX `\setlength{\parindent}{2em}` 自动处理，正文不要手动空格缩进
- 列号用 `(1) (2) (3)`（半角括号 + 阿拉伯数字），见现有 03-claims.tex 内 `enumerate label=(\\arabic*)` 用法
- 不使用模糊词："大约""等等""诸如此类"——必须给出确定范围或穷举集合
