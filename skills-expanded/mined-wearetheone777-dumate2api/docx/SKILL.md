---
name: docx
description: >
  统一的 Word 文档技能，覆盖 .docx 文件的完整生命周期。
  支持三种工作流：(1) 读取/分析/转换现有 .docx 文件；
  (2) 从零创建新 Word 文档；
  (3) 编辑现有 .docx 文件，通过 XML 操作精确修改内容同时保留格式。
  当用户提及"Word 文档"、".docx"、"报告"、"合同"、"论文"、"方案"，
  或要求输出带有专业格式的文档时使用此技能。
---

# Docx Skill

本技能入口只负责环境检查、工作区准备和任务路由。必须严格按 Step 1 → Step 2 顺序执行。具体操作按任务读取对应 reference；所有中间产物保留在工作目录中。

## Step 1（必做，最先执行）：目录变量与环境检查

```bash
# 技能目录（本 SKILL.md 所在目录）
export DOCX_SKILL_DIR="<本 SKILL.md 所在目录的绝对路径>"
# 工作区根目录：当前任务工作区或仓库根目录，不得等于技能目录
export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$PWD}"
# 工作目录：本次任务的全部中间产物
export WORKDIR="$WORKSPACE_ROOT/.dumate/docx-<name>-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$WORKDIR"

# 环境预检：解析工具位置；PATH 修正值以 PATH_FIX=<目录> 单行输出到 stdout，这里解析后拼接（不经 eval）
ENV_FIX="$(sh "$DOCX_SKILL_DIR/scripts/check_environment.sh")" && case "$ENV_FIX" in PATH_FIX=?*) PATH="${ENV_FIX#PATH_FIX=}:$PATH"; export PATH ;; esac
```

- 预检未输出「0 个失败」时停止任务，按脚本打印的安装命令装完再重跑，不得绕过。拼进 `PATH` 的修正值要在同一 shell 会话里保持有效，换会话就重跑预检。
- 脚本一律写成 `python "$DOCX_SKILL_DIR/scripts/xxx.py"`，不要用相对路径（当前工作目录不是技能目录）。
- 输入文件先复制进 `$WORKDIR`，输出、解包 XML、媒体、日志和验证结果也留在这里；全部保留，只把最终交付文件复制到用户指定路径。
- 预检脚本按**当前 shell** 选，不看操作系统：bash / sh / zsh（含 Windows 上的 Git Bash、MSYS2、WSL）用 `check_environment.sh`；PowerShell 用 `$fix = & "$env:DOCX_SKILL_DIR\scripts\check_environment.ps1"`，当 `$fix` 以 `PATH_FIX=` 开头时执行 `$env:Path = $fix.Substring(9) + ';' + $env:Path`（不要用 Invoke-Expression），并把命令里的路径分隔符 `/` 换成 `\`、`$DOCX_SKILL_DIR` 换成 `$env:DOCX_SKILL_DIR`、`export X="Y"` 换成 `$env:X="Y"`（例如 `python "$env:DOCX_SKILL_DIR\scripts\create_docx\xxx.py"`）。
- `check_environment.py` 仅作跨平台诊断用途：它不输出 PATH 修正值、也不参与 PATH 注入，预检流程只用 `.sh` / `.ps1`。

## Step 2（Step 1 完成后执行）：任务路由

先读取下表对应的 reference，再按其中的步骤操作：

| 任务 | 参考文档 |
| --- | --- |
| 创建 DOCX | `$DOCX_SKILL_DIR/references/create_docx/create_docx.md` |
| 读取、分析、转换已有 Word | `$DOCX_SKILL_DIR/references/read_docx/read_docx.md` |
| 编辑已有 Word | `$DOCX_SKILL_DIR/references/edit_docx/edit_docx.md` |
