---
name: docx
description: 创建、编辑、校验和转换 Word DOCX，支持数学建模论文模板、原生公式、三线表、修订和批注。
---

# DOCX 工具

许可：专有；完整条款见 `LICENSE.txt`。

## 路径与写入

- 当前目录为本工具根目录，只读。
- 模板和脚本从本目录读取。
- 生成或修改后的 DOCX 必须写入用户 `PROJECT_ROOT`。
- 默认不覆盖输入文件或 Skill 文件。

## 数学建模论文推荐流程

采用“当届官方参考模板 + `python-docx` 构建 + OMML 公式 + OOXML 校验 + 渲染抽检”。官方模板控制页面、样式、分节、页眉页脚和编号；代码负责稳定写入内容。

```python
from pathlib import Path
import sys

scripts = Path("<SKILL_ROOT>") / "tools" / "docx" / "scripts"
sys.path.insert(0, str(scripts))
import paper_format as pf

doc = pf.new_document(
    contest="cumcm",
    template_path=Path("<PROJECT_ROOT>") / "当届官方模板.docx",
    preserve_template_content=False,
)
# 此示例只借用模板样式后追加正文。
# 若官方模板包含固定摘要页或编号页，应改为 True 并在原位置填充。
pf.title(doc, "论文题目")
pf.abstract_title(doc)
pf.body(doc, "摘要正文。")
pf.keywords(doc, "优化；预测")
pf.equation(doc, r"\min f(x)=\sum_{i=1}^{n}x_i^2")
pf.three_line_table(doc, [["符号", "说明"], ["x", "决策变量"]])
pf.save_document(doc, Path("<PROJECT_ROOT>"), filename="论文候选稿.docx", contest="cumcm")
```

## 公式

### 直接写入

`scripts/equations.py` 把常用 LaTeX 子集转成 Word 原生 OMML。未知命令、未闭合分组和不支持环境会报错，不会静默生成错误文本。

```powershell
python scripts/equations.py replace "输入.docx" `
  --replace "EQ_OBJECTIVE" "\min f(x)=\sum_{i=1}^{n}x_i^2" `
  --output "<PROJECT_ROOT>/输出.docx"
```

同一占位符出现多次时会全部替换。支持分式、上下标、根式、n 次根、常用希腊字母与关系符号、反三角函数和常见矩阵，包括 `\nu`、`\mu`、`\approx`、`\arcsin`、`\arccos`、`\arctan`。

### 复杂公式

复杂 LaTeX 优先使用 Pandoc 的成熟转换：

```powershell
python scripts/equations.py generate "论文.md" `
  --output "<PROJECT_ROOT>/论文.docx" `
  --template "官方模板.docx"
```

转换后仍须校验和渲染抽检。

## 解包、校验与重打包

DOCX/XLSX 共用的 OOXML 基础工具只保留在 `scripts/office/`：

```powershell
python scripts/office/unpack.py "输入.docx" "<PROJECT_ROOT>/unpacked"
python scripts/office/validate.py "<PROJECT_ROOT>/输出.docx"
python scripts/office/pack.py "<PROJECT_ROOT>/unpacked" "<PROJECT_ROOT>/输出.docx" --original "输入.docx"
```

不要在不理解 OOXML 关系和内容类型的情况下直接修改压缩包。

## 修订

```powershell
python scripts/accept_changes.py "输入.docx" "<PROJECT_ROOT>/已接受修订.docx"
```

工具使用隔离的 LibreOffice 配置。超时、非零退出或残留修订标记都会失败，失败时不发布输出文件。

## 批注

先解包，再添加批注元数据和文档标记。父批注不存在或批注 ID 重复时，工具会在写入前失败。

默认批注与修订作者使用中性值 `Reviewer`。如需写入真实作者名，必须由用户明确指定；不得默认写入模型或厂商名称。不自动添加、删除或推断 AI 使用披露；是否披露及披露内容由用户依据目标任务的官方规则决定，规则强制要求时必须遵守。

```powershell
python scripts/comment.py "<PROJECT_ROOT>/unpacked" 0 "批注意见"
python scripts/comment.py "<PROJECT_ROOT>/unpacked" 1 "回复意见" --parent 0
```

## 必做验证

```powershell
python scripts/check_env.py
python scripts/self_check.py
python scripts/office/validate.py "<PROJECT_ROOT>/论文候选稿.docx"
```

调用 `validate_paper_structure()` 时，显式传入目标竞赛当届规则和项目质量目标。校验可覆盖官方前置结构、摘要语义与可选版面区间、正文篇幅、公式/图/表、图表编号与正文引用、参考文献双向对应、渲染页数和电子文件大小；未配置的数量或篇幅目标不应被工具猜测为硬门槛。官方模板中的徽标、摘要布局表等非论文图表须在发布清单中用 `excluded_figure_objects`、`excluded_table_objects` 明确计数，不能让工具把装饰对象误判为论文证据。内置参考文献双向解析针对数字编号制；若官方要求作者—年份等格式，将 `check_numeric_reference_bijection` 设为 `false`，并以单独的机器可读引用核对结果作为红队证据。结构校验后，把 DOCX 用发布清单指定的渲染器转换为 PDF 或图片，抽检分页、公式、表格、图片、页眉页脚和字体替换。

最终发布必须额外运行：

```powershell
python scripts/paper_release_gate.py `
  --manifest "<PROJECT_ROOT>/results/paper_release_manifest.json" `
  --candidate "<PROJECT_ROOT>/论文候选稿.docx" `
  --rendered-pdf "<PROJECT_ROOT>/rendered/论文候选稿.pdf" `
  --output "<PROJECT_ROOT>/完整论文.docx"
```

若 `official_rules.submission_format` 为 `pdf` 或 `both`，再传入 `--submission-pdf-output "<PROJECT_ROOT>/完整论文.pdf"`；门禁会从已经锁定的渲染 PDF 发布该文件，不能另行转换一份未核验 PDF。

先把 2.1 版 `references/paper_release_manifest.example.json` 复制到 `PROJECT_ROOT/results/paper_release_manifest.json`，再按当前竞赛、题目子问题和实际文件逐项替换。示例中的两个子问题仅演示动态数组结构，必须增删为当前题的真实数量；每个摘要必答项须写明 `requirement` 并登记互不冒充的摘要原文证据，禁止保留占位文本。空的 `quality_target` 表示没有另设非官方数量或篇幅门槛。

发布清单必须记录竞赛与届次、官方规则来源与核验日期、模板路径与 SHA-256、分页结构、适用的硬约束和质量目标、动态摘要必答项、渲染器，以及候选稿、渲染 PDF、结果注册表和红队审计的 SHA-256。备用模板未经用户明确批准、锁定文件被修改、红队未通过、摘要必答项缺失或任何阻断级检查失败时，门禁返回失败且不得交付。没有来源的页数、字数、填充率、公式/图/表数量不得作为通用默认门槛。
