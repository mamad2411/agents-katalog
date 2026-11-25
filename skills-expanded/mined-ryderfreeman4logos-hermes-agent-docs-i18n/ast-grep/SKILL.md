---
name: ast-grep
description: "AST-aware structural code search and rewrite via ast-grep."
version: 1.0.0
author: Yeongyu Kim (code-yeongyu), adapted by Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ast, codemod, refactoring, structural-search, code-search, rewrite, tree-sitter]
    category: software-development
    related_skills: [simplify-code, systematic-debugging]
---

# ast-grep

`ast-grep`（其二进制文件名也为 `sg`）是一款支持**25种语言的、具备AST解析能力的搜索与重写工具**。它会将用户输入的模式视为代码，以与解析项目代码相同的方式对其进行解析，并基于结构进行匹配。每当你的需求取决于**代码结构**而非文本字节时，它都是最佳选择。

该技能提供了位于 `scripts/ast_grep_helper.py` 的Python封装脚本，以及分别适用于POSIX系统的 `install.sh` 和Windows系统的 `install.ps1` 安装脚本。该辅助工具具备离线模式验证功能、两阶段重写机制以及二进制文件自动识别功能，建议将其作为默认的入口工具使用。

上游源代码源自 [code-yeongyu/ast-grep-skill](https://github.com/code-yeongyu/ast-grep-skill)（采用MIT许可证），并已包含在oh-my-openagent的共享技能包中。

---

## 何时使用此技能

当问题涉及**代码结构**而非字节内容时，可使用此技能：

- “找出所有接受 `Request` 参数的函数。”
- “将所有的 `console.log(x)` 替换为 `logger.info(x)`。”
- “移除所有 `as any` 类型转换。”
- “在整个项目中将 `require(...)` 替换为 `import`。”
- “查找空的catch块。”
- “将 `Optional[X]` 转换为 `X | None`。”
- “对这200个文件应用此代码修改规则。”
- “运行我们的YAML格式检查规则并显示违规项。”
当查询内容为文本形式时（如字符串字面量、注释、许可证头信息、文件名或跨语言正则表达式），应使用 `search_files`（或直接使用 `rg`）。如有疑问，可先自问：“答案是否依赖于该语言的语法树，还是仅取决于文件的字节内容？”若是前者，则使用 ast-grep；若是后者，则使用 search_files。

Hermes 集成注意事项：
- 通过 `terminal` 工具运行辅助工具及 `sg`。需对每个模式加上单引号，以避免 shell 解析 `$VAR` 变量。
- 对于针对匹配结果的“查找→读取”操作链，建议使用 `--json-out` 输出结果，并通过 `execute_code` 处理，而非将其传递给其他解释器。
- 该工具是 Hermes 自带 `patch` 工具的补充（而非替代）：`patch` 用于手动执行的目标化编辑，而 ast-grep 则适用于在多个站点间基于模式进行批量重写。

---

## 智能体必须牢记的三点

### 1. ast-grep 并非正则表达式

其通配符为 `$VAR`（表示一个 AST 节点）和 `$$$`（表示零个或多个节点）。正则表达式语法在此处将无法正常工作：

| 你输入的内容 | ast-grep 的解析结果 | 你的实际意图 |
|---|---|---|
| `foo\|bar` | 将 `foo` 和 `bar` 进行按位或运算 | 分别执行两次独立搜索 |
| `.*foo` | 无法解析 | 应使用 `$$$ foo`（若 `$$$` 表示节点列表），或改用 rg |
| `\w+` | 无法解析 | 应使用 `$VAR` 来匹配任意标识符 |
| `[a-z]` | 字符类，无法解析 | 应改用 rg |

完整的错误用法表详见 `references/pitfalls.md` 的第 1 节。该辅助工具的 `validate` 子命令可自动检测这些错误——在手动排查“无匹配结果”问题之前，建议先调用此命令。

### 2. 模式必须是有效的代码片段

该模式本身必须能够被解析。`def $FN($$$):` 这种写法是无效的，因为末尾的冒号导致语句不完整；应使用 `def $FN($$$)`。不包含参数或函数体的 `function $NAME` 也是无效的；应使用 `function $NAME($$$) { $$$ }`。各语言的详细列表请参见 `references/pitfalls.md` 的第2节。

### 3. `--update-all` 与 `--json` 参数互斥（且不会输出提示）

这是编写脚本时最容易犯的错误。执行 `sg run -p P -r R --json --update-all` 命令虽然会返回 JSON 数据，但**不会修改任何文件**。若需同时预览并应用更改，需分**两步**操作：

```bash
sg run -p P -r R --json=compact .   # pass 1: see what would change
sg run -p P -r R --update-all .     # pass 2: actually apply
```

当您调用 `replace --apply` 时，该辅助工具会自动执行此操作。详情请参阅 `references/pitfalls.md` 的第 9 节。

---

## 辅助脚本 — `scripts/ast_grep_helper.py`

这是一个基于 Python 3 标准库的单文件封装程序，在所有操作系统中格式一致，也是代理程序的默认入口点。

### `search` — 查找模式的所有匹配项

```bash
python scripts/ast_grep_helper.py search 'console.log($MSG)' --lang ts src/
```

首先会离线验证该模式是否有效。如果该模式属于正则表达式形式（如 `\w`、`.*`、`|` 等），该工具会给出提示后直接退出，而不会调用 `sg` 函数——从而避免不必要的往返操作。如需跳过验证，可使用 `--force` 参数。

标志选项：
- `--lang ts`（或任意 25 种语言；也支持 `js`、`py`、`rs`、`kt` 等别名）
- `--globs '!**/*.test.ts'`（可重复使用；前缀 `!` 表示排除）
- `-C 3`（上下文行数）
- `--json-out`（以原始 JSON 格式输出，而非易读格式）

### `replace` — 按模式重写内容，默认为试运行模式

```bash
# Dry-run preview (default — no files mutated)
python scripts/ast_grep_helper.py replace 'console.log($MSG)' 'logger.info($MSG)' --lang ts src/

# Actually apply
python scripts/ast_grep_helper.py replace 'console.log($MSG)' 'logger.info($MSG)' --lang ts src/ --apply
```

该辅助工具的功能如下：
1. 检查 `pattern` 和 `rewrite` 的内容，确保不存在可被提示系统识别的错误。
2. 使用 `--json=compact` 参数运行第一轮扫描，以收集匹配结果并显示预览内容。
3. 若指定了 `--apply` 参数，则会使用 `--update-all` 参数运行第二轮扫描，从而对文件进行实际修改。

### `scan` — 执行 YAML 规则扫描

```bash
# Discover sgconfig.yml from cwd and run all rules
python scripts/ast_grep_helper.py scan src/

# Run a single rule file
python scripts/ast_grep_helper.py scan -r rules/no-console.yml src/

# Apply auto-fixes
python scripts/ast_grep_helper.py scan -U src/

# CI-friendly GitHub annotations
python scripts/ast_grep_helper.py scan --report-style short src/
```

### `validate` — 离线模式检查（无需调用 `sg`）

适用于 CI 代码检查、预提交钩子以及快速合理性验证：

```bash
python scripts/ast_grep_helper.py validate '\w+' --lang ts
# → exit 2: regex \w not supported. Use $VAR for identifiers.

python scripts/ast_grep_helper.py validate 'console.log($MSG)' --lang ts
# → exit 0: pattern looks plausible for ast-grep.
```

### `langs` / `doctor` / `install`

```bash
python scripts/ast_grep_helper.py langs       # list 25 supported languages and aliases
python scripts/ast_grep_helper.py doctor      # check ast-grep binary availability
python scripts/ast_grep_helper.py install     # delegate to install.sh / install.ps1
```

`new` 和 `test` 子命令会直接调用 `sg new` 和 `sg test`。  

---

## 直接使用 `sg`（当辅助工具不够用时）

该辅助工具存在一定的固有限制。如需完全掌控操作流程，可直接使用 `sg`。该技能在 `references/cli.md` 中提供了 CLI 使用指南，其中列出了最基本的操作方式：

```bash
# Search
sg run -p 'console.log($MSG)' --lang ts src/

# Search with JSON for scripting
sg run -p 'console.log($MSG)' --lang ts --json=compact src/

# Rewrite, dry-run
sg run -p 'console.log($MSG)' -r 'logger.info($MSG)' --lang ts --json=compact src/

# Rewrite, apply
sg run -p 'console.log($MSG)' -r 'logger.info($MSG)' --lang ts --update-all src/

# Pattern from stdin (great for ad-hoc experiments)
echo 'console.log("hi")' | sg run -p 'console.log($MSG)' --lang js --stdin

# Debug a pattern that returns 0 matches
sg run -p '<your pattern>' --lang <lang> --debug-query=ast --stdin <<< '<sample-code>'

# Run YAML rules
sg scan src/

# Inline YAML rule (one-off)
sg scan --inline-rules '
id: no-todo
language: TypeScript
severity: warning
rule: { pattern: TODO }' src/
```

在 Shell 中直接使用 `sg` 命令时，**务必对模式内容加上单引号**，这样才能避免 Shell 对 `$VAR` 这类变量进行展开。

```
USER asks for "find/rewrite/codemod"
│
├─ structural pattern (function shape, call, class, import, control flow)
│  └→ ast-grep (this skill)
│
├─ text pattern (regex, alternation, character classes, file names)
│  └→ search_files / rg
│
├─ semantic question (what variable does this refer to? does this throw?)
│  └→ LSP tools, TypeScript compiler, Pyright, Semgrep with type inference
│
└─ multiple repos / federated search
   └→ a search engine + then ast-grep / rg / LSP per-repo
```

[背景信息]  
Hermes Agent 技术文档、CLI 使用指南、Agent 能力、插件、提供程序以及开发者指南。  

[目标文本翻译]  
如果用户输入“find all”或“every”，且目标为结构化元素（函数、类、调用、导入、语句），则默认使用 ast-grep 进行搜索。而当目标为文本内容（字符串、注释、许可证头、文件名、标识符子串）时，则默认使用 search_files 进行搜索。  

---

## 重写内容时务必先进行试运行  

错误的模式可能会在不知情的情况下修改错误的内容。正因如此，该工具的 `replace` 功能默认会先执行试运行。操作流程如下：  

1. 先进行搜索以确认匹配项：`helper search '<pattern>' --lang X .`  
2. 执行试运行重写：`helper replace '<pattern>' '<rewrite>' --lang X .`（不使用 `--apply` 参数）  
3. 查看试运行结果摘要：包括匹配数量、受影响的文件以及各位置的预览内容  
4. 若结果有误，则优化模式，返回步骤 1  
5. 若结果正确，则执行：`helper replace '<pattern>' '<rewrite>' --lang X . --apply`  

切勿在未进行试运行的情况下直接应用重写结果。在 Git 仓库中使用 `--apply` 参数后，应在提交前通过 `git diff --stat` 查看差异。  

---

## 当 `sg` 检索到 0 个匹配项，但你确定代码确实存在时  

请按以下优先级顺序处理：

1. **运行 `helper validate '<pattern>' --lang <lang>`** — 用于检测正则表达式使用错误、函数体缺失以及 Python 代码中多余的冒号。  
2. **检查 `--lang` 参数** — `sg` 会根据文件扩展名自动推断语言类型；若您传入 `.tsx` 文件却指定 `--lang ts`（而非 `tsx`），JSX 将无法被解析。  
3. **查看已解析的模式**：执行 `sg run -p '<pattern>' --lang <lang> --debug-query=ast --stdin <<< '<sample>'`。若输出中出现 `ERROR` 节点，说明该模式格式有误。  
4. **检查目标文件的抽象语法树（AST）**：运行 `sg run -p '$_' --lang <lang> --debug-query=cst path/to/file | head -40`，即可找到您试图匹配的节点类型。  
5. **使用在线演示工具**：<https://ast-grep.github.io/playground.html> — 仅需粘贴代码与模式，即可直观查看处理结果。

切勿盲目尝试各种变体。每次失败都有其原因，需找出问题所在。

---

## 何时使用 YAML 规则与内联 `-p` 模式

**选择内联 `-p` 模式**的情况包括：  
- 单次临时查询；  
- 模式较为简单（无约束条件，也无修复模板）；  
- 正在探索性测试。

**选择 YAML 规则**（规则文件存放在 `rules/` 目录下，通过 `sg scan` 命令运行）的情况包括：  
- 该模式会被重复使用（如代码检查规则、在 CI 环境中运行的代码修改工具）；  
- 需要使用约束条件、转换功能、复杂的 `inside`/`has` 判断或复合逻辑；  
- 希望实现自动修复（通过 `fix:` 字段）；  
- 希望对规则进行测试（通过 `sg test` 执行快照测试）。

完整的 YAML 规则架构定义见 `references/yaml-rules.md`。项目配置文件（如 `sgconfig.yml`、`ruleDirs`、`utilDirs`）的说明则位于 `references/sgconfig.md` 中。

---

## 输出规范

- 使用 `sg run --json=compact` 命令会生成一个匹配对象数组，每个对象的结构为：`{ file, range: {start, end}, text, replacement?, lines, language, ... }`。
- 若不使用 `--json` 参数，`sg` 命令会输出适合在终端中查看的彩色格式文本。
- 该辅助工具的默认输出格式为易读形式（文件名：行号：列号 + 匹配内容预览）；如需获取原始 JSON 数据，请使用 `--json-out` 参数。
- 该辅助工具在执行替换操作时，总会同步显示汇总信息：匹配总数、受影响的文件数量以及各位置的匹配内容预览。

在向用户总结结果时，**务必同时说明受影响的文件数量，而不仅仅是匹配总数**。因为用户关心的是错误影响的范围。

---

## 推荐阅读资料（按优先级排序）

1. `references/patterns.md` —— 元变量、命名规则及严格程度设置。当不确定某个模式为何无法匹配时，请查阅此文档。
2. `references/pitfalls.md` —— 失败模式指南。当发现没有匹配结果时，请先阅读此文档。
3. `references/recipes.md` —— 按编程语言分类的现成模式模板。开始新任务时，首先阅读此文档。
4. `references/cli.md` —— 包含 `sg run`、`sg scan`、`sg test`、`sg new`、`sg lsp` 等命令的使用说明。当辅助工具无法满足需求时，请查阅此文档。
5. `references/yaml-rules.md` —— YAML 规则结构说明。当内联模式已无法满足需求时，请阅读此文档。
6. `references/sgconfig.md` —— 项目级配置设置。在为实际项目配置 `sg scan` 功能时，请查阅此文档。
7. `references/install.md` —— 各操作系统的安装方法。仅当 `install.sh` / `install.ps1` 脚本执行失败时才需查阅。

---

## 不可违背的规则（严禁更改）

- **搜索前先进行验证。** 当通过编程方式生成匹配模式时，应首先调用 `helper validate` 函数。该函数能捕获约 70% 导致“未找到匹配项”的错误，这类错误大多源于正则表达式的误用。
- **应用前先进行试运行。** 在未先查看匹配结果的情况下，切勿直接运行 `sg run -r ... --update-all` 命令。该工具的 `replace` 功能会默认强制执行此步骤。
- **分两步完成写入操作。** 若需直接使用 `sg` 函数同时进行预览和实际应用，应分别执行两次调用——因为 `--json` 参数会忽略 `--update-all` 的作用。
- **在 Shell 中请使用单引号包裹模式。** 应使用 `'$VAR'` 而非 `"$VAR"`。因为在双引号中，Shell 会将 `$VAR` 替换为空字符串，从而导致匹配模式失效。
- **匹配模式属于代码而非正则表达式。** 若模式中需要使用 `|`、`.*`、`\w` 或 `[a-z]` 等符号，建议改用 `search_files` 函数。切勿强行将 ast-grep 强制转换为正则表达式格式。
- **通过标准输入时必须指定语言参数。** 当使用 `--stdin` 参数传递数据时，需明确设置 `--lang` 参数；因为 `sg` 函数无法仅通过文件扩展名推断语言类型。
- **在 Linux 系统中，建议优先使用 `ast-grep` 而非 `sg`**，原因是 `sg` 的名称可能与 `util-linux` 工具中的 `setgroups` 命令发生冲突。该辅助工具已解决了这一问题；若直接调用 `sg`，可为其设置别名：`alias sg=ast-grep`。
