---
name: pdf
description: >
  高质量PDF生成与操作的技能，所有与pdf相关的工具优先使用该技能。只有四条路由：
  生成 PDF：从零生成精美 PDF（报告、提案、简历等），或把已有文档保留内容重新排版。
  编辑或修改 PDF：填写表单字段，原位替换文字（保留原字体与版式），合并、拆分、旋转、水印、加密/解密。
  解析 PDF：提取内容为 Markdown（PaddleOCR-VL 云端引擎，公式/表格/图表/扫描件统一识别），导出逐行版式事实为 JSON，核对文字改动。
  转换：DOC/DOCX、PPT/PPTX、XLS/XLSX、已有 HTML 直接导出 PDF，PDF 转图片/长图（可去掉文字层只留版面），图片拼成 PDF，将 PPT 导出的 PDF 恢复为 PPTX（一页一页照搬原版面，文字按行可编辑，不用于重设计演示文稿）
---

# pdf

统一的 PDF 技能，只有四条路由：**生成 / 编辑 / 解析 / 转换**。默认中文输出（除非用户要求英文）。

**使用方式**：先完成 Step 1，再按 Step 2 的路由表读取该路由**唯一**的 reference 文档并执行。SKILL.md 只负责目录变量、环境检查和路由，不含执行细节。一条路由一个文件，不需要再跳读第二份。复合需求按实际需要组合路由，复用同一项目，不重新初始化或重复解析。

## Step 1（必做，最先执行）：目录变量与环境检查

```bash
# 技能目录（本 SKILL.md 所在目录）
export PDF_SKILL_DIR="<本 SKILL.md 所在目录的绝对路径>"
# 工作区根目录：当前任务工作区或仓库根目录，不得等于技能目录
export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$PWD}"

# 环境预检：只检查最小运行条件，操作依赖按需准备（报告走 stderr，stdout 为空，不经 eval）
sh "$PDF_SKILL_DIR/scripts/check_environment.sh"
```

新任务初始化一次；已有 `$PROJECT_PATH` 则复用。

`--type` 是项目的**文档类型**（如 `general`、`report`），与生成/编辑/解析/转换路由无关。生成任务按 [generate.md](references/generate.md) 的文档类型选择 `<type>`；编辑、解析和转换任务新建项目时使用 `--type general`。不要把 `generate`、`edit`、`parse` 或 `convert` 路由名填入此参数。转换使用 `general` 只记录项目类型，不应用排版模板，也不改变转换引擎。

下面的 `<project_name>` 替换为项目名称，`<type>` 按上述规则填写：

```bash
# 项目目录（本次任务的全部中间产物）：pdf-<name>-<日期>-<uuid8>
PROJECT_JSON="$(python3 "$PDF_SKILL_DIR/scripts/project_manager.py" init <project_name> \
  --type <type> --dir "$WORKSPACE_ROOT/.dumate")"
export PROJECT_PATH="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["project_dir"])' <<< "$PROJECT_JSON")"
export PDF_SKILL_STATE_DIR="$PROJECT_PATH/cache/runtime"
```

- 预检只硬性要求 Python 3.10+，不扫描或安装 PDF/Office 包、字体及可选系统工具；Python 包由各脚本按需安装，`typst` 在生成时按需准备，降级依赖只在确定降级后检查。依赖安装或操作失败后，先排查原因，不在相同条件下反复重试。
- 脚本一律写成 `python3 "$PDF_SKILL_DIR/scripts/xxx.py"`，不要用相对路径（当前工作目录不是技能目录）。
- 文件全部写在 `$PROJECT_PATH` 内：`sources/<source-id>/` 放原始输入，`artifacts/` 放中间产物，`assets/images/` 放图片，`build/<run-id>/` 和 `exports/<run-id>/` 放渲染产物；全部保留，只把最终交付文件复制到用户指定路径。复用项目时为新产物使用新的 run-id。
- 预检脚本按**当前 shell** 选，不看操作系统：bash / sh / zsh（含 Windows 上的 Git Bash、MSYS2、WSL）用 `check_environment.sh`；PowerShell 用 `& "$env:PDF_SKILL_DIR\scripts\check_environment.ps1"`（stdout 为空，不需要管道给 Invoke-Expression），并把 `python3` 换成 `python`、`export X="Y"` 换成 `$env:X="Y"`。
- 编辑和转换使用 `import-sources "$PROJECT_PATH" <files...> --archive-only`，只归档，不识别正文。需要读取材料内容才使用普通 `import-sources`。`archived` 不等于 `parsed`。

## Step 2（Step 1 完成后执行）：路由

| 路由 | 触发条件 | 读这一份 |
|------|---------|---------|
| **1. 生成 PDF** | 产出是一份**新 PDF**：从零写，基于笔记/PDF/图片/参考资料生成报告、提案、简历，把已有文档保留内容重新排版，或要空白 PDF；保留内容与版面的直接转换走路由 4 | `$PDF_SKILL_DIR/references/generate.md`（含从零生成、重新排版两条子流程 + 设计系统） |
| **2. 编辑或修改 PDF** | 已有 PDF，产出是**它的修改版**：填表单、改文字、合并/拆分/旋转/水印/加密解密 | `$PDF_SKILL_DIR/references/edit.md`（含填表单 + `scripts/edit/pdf_edit.py` 编辑命令 + `compare-text` 核对） |
| **3. 解析 PDF** | 产出是**内容或事实**，不需要设计感 PDF：提取/转 Markdown（云端 PaddleOCR-VL，含扫描件）、分析文档、导出逐行版式 JSON | `$PDF_SKILL_DIR/references/parse.md`（含内容提取 + `dump_layout.py`） |
| **4. 转换** | 保留内容与版面，**只换格式**：DOC/DOCX、PPT/PPTX、XLS/XLSX、已有 HTML→PDF，PDF→图片/长图/去字底图，图片→PDF，将 PPT 导出的 PDF 恢复为 PPTX | `$PDF_SKILL_DIR/references/convert.md`（含 `document_convert.py` + 产物核对及本地降级） |


## 判定顺序

看**用户要的产出物**，不是看输入——输入是 PDF 不代表走 2 或 3。

1. 只需保留内容与版面进行上述格式转换 → 路由 4；Office 文件或已有 HTML 直接导出虽产生新 PDF，仍走转换。
2. 要的是一份新写、整合资料或重新排版的 PDF → 路由 1。
3. 要的是同一份 PDF 的修改版 → 路由 2。
4. 要的是文字、数据、结论、版式事实 → 路由 3；PDF→Markdown 属于解析。