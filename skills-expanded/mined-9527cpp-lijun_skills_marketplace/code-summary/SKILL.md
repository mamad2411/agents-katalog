---
name: code-summary
description: >-
  Turns git commits into a Chinese technical feature document (API, protocol,
  flow diagrams, risks, usage examples, commit table). Default output is
  Markdown; use --type doc or --type pdf to convert. Supports start commit
  through HEAD, explicit SHA list, or default window. Use --update with
  --output to incrementally append new commits to an existing or new doc.
  All paths are relative to Claude Code's cwd. Use for 代码总结, 技术文档,
  feature doc from commits, or /code-summary with SHAs.
---

# Code Summary (Git → Technical Document)

## When to apply

Use this skill when the user wants a **code / change summary** from git, especially with any of:

- A **start commit** (inclusive range through latest / specified end)
- **Specific commits** (one or more SHAs)
- Output as a **document file** with a **short English filename** (see below)
- **Update an existing doc** with new commits via `--update` (see below)

Default language for the summary body: **Simplified Chinese** unless the user asks otherwise.

**Output format (controlled by `--type`):**

| `--type` value | Output | Description |
|---|---|---|
| *(omitted / `md`)* | `.md` | **默认**。直接输出 Markdown 文件。 |
| `doc` | `.docx` | 先生成 `.md`，再用 `pandoc` 转为 Word (`.docx`)。 |
| `pdf` | `.pdf` | 先生成 `.md`，再用 `pandoc` 转为 PDF。 |

用户可在命令中指定，例如：
- `/code-summary a1b2c3d --type doc`
- `"从 a1b2c3d 总结到现在 --type pdf"`
- `"总结最近 10 个 commit"` ← 不带 `--type`，默认输出 `.md`

**Output file (controlled by `--output`):**

| `--output` value | Behavior |
|---|---|
| *(omitted)* | 自动生成文件名（主题压缩，≤32字符）。 |
| `filename.md` | 使用指定文件名（需含扩展名 `.md`/`.docx`/`.pdf`）。 |

**Update mode (`--update <commit> --output <文件>`):**

| 参数 | 含义 |
|---|---|
| `--update <commit>` | 起始 commit（包含此 commit 及其之后的新提交）；若文件已存在，则只总结尚未在文档中的新 commit。 |
| `--output <文件>` | 输出目标文件路径（含扩展名 `.md`/`.docx`/`.pdf`）。 |

| Scenario | Behavior |
|---|---|
| 文件已存在 | 读取文档 `## 相关提交记录` 表格，找出尚未记录的新 commit（从 `--update` 指定的 commit 之后到 HEAD），仅对这些新 commit 进行总结，**追加**到原文档末尾。 |
| 文件不存在 | 从 `--update` 指定的 commit 到 HEAD，生成完整的 feature-doc 并写入指定文件。 |

> `--update` 适用于：已有文档需要增量更新新 commit，而非全量重写。
> 增量时：已有内容**原样保留**，`## 相关提交记录` 表格追加新行，其他章节（概述、实现细节等）按需扩展新 commit 相关内容。
> **不覆盖或删除原有内容**。

**Output mode (default vs optional):**

- **Default — `feature-doc`**: read like **end-user / 联调 oriented technical doc** (same section order as a good `*_snap.md`: 概述 → 实现细节 → 触发方式 → 执行步骤框图 → 风险 → 示例 → 提交表 → 平台).
- **Optional — `commit-changelog`**: only if the user explicitly asks for **变更说明 / PR 说明 / 纯提交总结** — then use the shorter “范围说明 / 变更概览 / 关键文件 …” checklist (legacy style).

---

## Inputs (resolve in this order)

0. **Update mode** (`--update <commit> --output <文件>`)  
   - **`--update <commit>`** 指定起始 commit（需要总结的范围从该 commit 到 HEAD）。  
   - **`--output <文件>`** 指定输出文件路径。  
   - **若文件已存在**：读取文件末尾 `## 相关提交记录` 表格，提取已记录的所有 commit SHA；仅对**尚未在表格中的新 commit**（从 `--update` 指定的 commit 之后到 HEAD）进行总结，**追加**到原文档末尾。  
   - **若文件不存在**：从 `--update` 指定的 commit 到 HEAD，生成完整的 feature-doc 并写入指定文件。  
   - **`--update` 与 `--output` 必须同时使用**，缺一报错。

1. **Explicit commit list**  
   If the user gives one or more SHAs (e.g. `abc1234`, `def5678` or `abc1234..def5678` as a list):  
   **Only** summarize those commits, in **chronological order** (oldest first).  
   Collect history with **one** shell command (see **Claude Code / Bash** below)—do **not** spawn **parallel** `Bash` tool calls per SHA (that often triggers `Invalid tool parameters` / `parallel tool call Bash errored`).

2. **Start commit**  
   If the user gives a **start commit** (and no conflicting explicit list):  
   Summarize **from that commit through**:
   - **HEAD**, or
   - an **end commit** if the user also names one (inclusive range).  
   Use: `git log --reverse --oneline <start>^..<end>` and `git diff <start>^..<end>` (or `<start>..<end>` if the user said “between” clearly—confirm if ambiguous).  
   Prefer **`^..`** so the start commit itself is included when the user says “从某 commit 开始”.

3. **Neither**  
   If nothing is specified: ask once, or use a small default (e.g. last **10** commits or **7 days**) and state it in the doc.

---

## What to collect (run relative to cwd)

- 所有 git 操作相对于 **Claude Code 打开时的当前工作目录 (cwd)**，而不是 repo 根目录。
- `git status -sb` and current branch name (context only).
- For **ranges**: `git log --reverse --oneline <range>`, then `git diff --stat <range>`, then targeted `git diff <range> -- <paths>` for hot files.
- For **listed SHAs**: prefer **one** `Bash` invocation (loop below), not N parallel calls.
- Optionally: `git diff-tree --no-commit-id --name-only -r <sha>` per commit for file lists.

Read **actual file contents** when the diff alone is unclear (renames, generated code, large moves).

---

## Default Markdown structure (`feature-doc`)

Produce **one** `.md` file. Section **order and depth** should match a strong feature write-up (reference style: `jpeg_snap.md`):

### Title

`# <功能名> 技术文档` — 功能名用中文，具体、可搜索（例如「JPEG 快照功能」）。

### 1. `## 概述`

2–5 句：做什么、谁会用、和主流程（如远程桌面/主码流）的关系。**可在一句话里带分支名 + 时间范围**（代替单独大段「范围说明」）。

### 2. `## 实现细节`

#### `### 1. 核心接口`

对每个**对外**入口（C/C++ API、全局函数等）列出：

- **签名**（从源码复制）
- **位置**：`路径:行号`（打开文件核对）
- **功能**、**参数**、**返回值**

#### `### 2. 协议 / 命令 / 配置`（若本次变更涉及）

例如 UDS 命令码、JSON 字段、默认值；写清 **头文件/常量定义位置**。

#### `### 3. 主要实现文件`

| 文件 | 说明 |

### 3. `## 触发方式`

分小节（如「UDS」「直接调用 SDK」），给出**可复制**的 JSON / 命令行 / 伪代码示例。默认值、可选字段写清楚。

### 4. `## 函数执行步骤`

用 **ASCII 框图**（`┌──…──┐`）按**调用链**分层，例如：UDS 回调 → `board_sdk_*` → 平台实现 → MPI 调用。

- 每一步标注 **仓库内真实路径**（函数名必须与源码一致）。
- **禁止臆造**代码中不存在的函数、宏、模块名、芯片 API 名；若未在已读文件中看到，写「以仓库 `path/to/file` 实现为准」或省略该层。

### 5. `## 潜在风险`

编号列表；每条包含 **风险** + **缓解措施**（可含并发、权限、阻塞、分辨率切换、资源争用等——按 diff 实际能支撑的内容写，不要空泛堆砌）。

### 6. `## 使用示例`

- Shell / 测试命令（路径、socket 名与项目一致）
- 可选 C/C++ 片段（需与头文件、类型一致）

### 7. `## 相关提交记录`

| 提交（短 SHA） | 说明 |

说明列：**一句人话**，优先结合 diff；可按时间从上到下。

### 8. `## 平台支持`（如适用）

写清哪些 SoC / `board_sdk_api_*` 已实现，其他平台是 stub 还是未实现。

---

### Code citations

When quoting code, use workspace line format only:

```12:18:path/from/repo/root.cpp
// excerpt
```

No HTML entities inside fences.

---

### Legacy structure (`commit-changelog` only)

If the user explicitly wants **纯变更说明**，再用旧模板：**范围说明 → 变更概览 → 按模块分组 → 关键文件 → 行为与兼容性 → 未决与后续**。

---

## Output file naming

- **格式**: 纯英文小写（或数字），**仅** `[a-z0-9_-]`，**最多 32 个字符**，扩展名根据 `--type` 决定（`.md` / `.docx` / `.pdf`）。  
- **含义**: 压缩功能主题，例如 `uds-auto-chn-alloc.md`、`mpi-so-dlopen.docx`、`jpeg-grap-vi-feed.pdf`。  
- **长度**: 不含扩展名的 stem ≤ **32**。若过长，缩写关键词（`feat`→`f`, `refactor`→`ref`, `video-server`→`vsrv`）并保持可读。  
- **位置**: 相对于 **Claude Code 打开时的当前工作目录 (cwd)**，不是 repo 根目录。未指定则写在该 cwd 下，或用户说的 `docs/`；不要擅自创建用户未提及的大型目录结构。
- **`--output <name>`**: 显式指定输出文件名（需含扩展名）。路径相对于 cwd。若配合 `--update` 使用，文件不存在时会创建新文件（不是报错）。若未指定 `--output` 且未指定 `--update`，行为照旧（自动生成文件名）。

**`--update` 与文件名**：  
- `--update <commit> --output <文件>` 时，若文件已存在则追加内容，若不存在则创建新文件。  
- 文件名由 `--output` 指定，原样不变。

---

## Quality bar (align with user expectations)

- **完整句**、结构清晰；面向「要看懂怎么用、怎么排错」的读者，而不仅是「提交了哪些文件」。
- **只写与变更相关的内容**；不扩写无关重构。
- 若某 commit 消息为空或含糊，以 **diff + 当前文件内容** 为准。
- **准确性优先于篇幅**：宁可少写一个子流程，也不要编造 RK_MPI / 驱动层不存在的调用名；所有命令码、路径、默认文件名以 **grep/读文件** 核实。

---

## Quick examples (for the agent)

**Range:**  
User: “从 `a1b2c3d` 总结到现在”  
→ Summarize `a1b2c3d^..HEAD` (include `a1b2c3d`), filename e.g. `summary-a1b2c3d-to-head.md` only if ≤32 chars; else shorter theme name.

**Explicit SHAs:**  
User: “总结 `e1e1e1`、`f2f2f2` 两个 commit”  
→ Default: full **`feature-doc`** (概述…提交表…); filename e.g. `jpeg-snap-uds-api.md` (theme, ≤32 chars).

**Conflict:**  
User gives both start commit and explicit list → **prefer explicit list**; mention the ignored range briefly under **概述** or **相关提交记录** 表头说明。

**Update existing doc:**  
User: “`/code-summary --update abc1234 --output ./docs/jpeg-snap-uds-api.md`”  
→ If `./docs/jpeg-snap-uds-api.md` exists: read it, extract SHAs from `## 相关提交记录`, find commits newer than the newest recorded SHA, only summarize those new commits, append to the same file.  
→ If the file does not exist: generate a full doc from `abc1234^..HEAD` and write to that path.

**Update with explicit range:**  
User: “`/code-summary --update abc1234..def5678 --output my-doc.md`”  
→ Same as above, but limit the new commits to the range `abc1234..def5678`.

---

## Claude Code / Bash (avoid tool errors)

Claude Code’s `Bash` tool often **fails or cancels** when the model issues **several parallel** `git show` calls. Follow this:

1. **Single `Bash` call** for multiple SHAs — loop and print separators:

```bash
# git 操作相对于 Claude Code 的当前工作目录 (cwd)，不需要 cd
for c in \
  9a717be50f2ed23814ea731fce8d2ddca4305251 \
  33b564894c7831b3d9de36824af41dd34ba4bbcd \
  88a7c63497b67f62a10167ebf44583d334ad80d8 \
  330f60af9b7bfb1958242bdece86e044c0a3a7ca
do
  echo "======== COMMIT $c ========"
  git show --no-patch --stat --format=fuller "$c" && git show "$c"
done
```

2. **Sort chronologically** before writing the doc (oldest first). In **one** shell, e.g.:

```bash
for c in SHA1 SHA2 SHA3 SHA4; do git show -s --format="%ct %H" "$c"; done | sort -n
```

Use the resulting commit order as section order in the Markdown.

3. **Do not** pass empty command, or malformed quoting; keep the command as a **single string** with newlines only inside the script if the tool allows, or use `;` between statements.

4. If `/code-summary` passes args as one line of space-separated SHAs, **split on whitespace** and substitute into the `for c in ...` list.

---

## Format conversion (`--type doc` / `--type pdf`)

When the user specifies `--type doc` or `--type pdf`, follow this two-stage pipeline:

### Stage 1: Generate Markdown (always)

Write the full `.md` file to disk first, exactly as in the default flow. This intermediate file is the single source of truth.

### Stage 2: Convert with pandoc

**Prerequisites check** — before converting, verify `pandoc` is installed:

```bash
command -v pandoc >/dev/null 2>&1 || { echo "ERROR: pandoc not found. Install: sudo apt install pandoc (Debian/Ubuntu) or brew install pandoc (macOS)"; exit 1; }
```

**For `--type doc` (Word .docx):**

```bash
pandoc "<stem>.md" -o "<stem>.docx" \
  --from markdown \
  --to docx \
  -V lang=zh-CN \
  --toc
```

**For `--type pdf`:**

PDF 转换需要 LaTeX 引擎（推荐 `xelatex`，对中文友好）:

```bash
command -v xelatex >/dev/null 2>&1 || { echo "ERROR: xelatex not found. Install: sudo apt install texlive-xetex texlive-lang-chinese (Debian/Ubuntu)"; exit 1; }

pandoc "<stem>.md" -o "<stem>.pdf" \
  --from markdown \
  --pdf-engine=xelatex \
  -V CJKmainfont="Noto Sans CJK SC" \
  -V geometry:margin=2.5cm \
  -V lang=zh-CN \
  --toc
```

如果 `xelatex` 不可用，回退到 `wkhtmltopdf`：

```bash
pandoc "<stem>.md" -o "<stem>.pdf" \
  --from markdown \
  --pdf-engine=wkhtmltopdf
```

### Stage 3: Clean up

- 转换成功后，**保留** 中间 `.md` 文件（方便后续编辑或再次转换）。
- 向用户报告最终文件路径和文件大小。
- 如果 pandoc 转换失败，输出错误信息并告知用户 `.md` 文件已就绪可手动转换。

---

## Cursor

The same skill lives under `~/.cursor/skills/code-summary/` for Cursor agents.
