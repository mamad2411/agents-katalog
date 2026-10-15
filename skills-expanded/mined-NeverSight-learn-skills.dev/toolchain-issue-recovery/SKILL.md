---
name: toolchain-issue-recovery
description: "当开发、测试、文档生成、技能创建或修改、文件编辑、浏览器操作、截图、构建、校验、脚本运行、PowerShell/Python/Node 命令执行等过程中遇到工具链问题时必须使用本技能。适用于沙箱 helper 异常、权限或路径问题、apply_patch 失败、初始化脚本部分失败、依赖缺失、校验工具无法运行、Windows PowerShell 中文乱码、编码误判、命令参数不兼容、网络或安装失败、替代验证、以及用户要求“记录刚才的问题”“把解决方式沉淀下来”的场景。若本技能没有覆盖当前问题，解决后必须把可复用经验写回本技能或其 eval/使用说明。"
---

# Toolchain Issue Recovery

本技能用于处理工具链故障：先判断问题是否来自工具、环境或执行通道，再选择保守恢复方案，并把新的可复用经验沉淀下来。

<HARD-GATE>
以下规则不可违反：

1. **先区分工具链问题与业务问题。**
   不要把脚本缺依赖、沙箱 helper 异常、编码误读、路径兼容或命令参数差异误判为用户需求、代码逻辑或文件内容本身的问题。

2. **不要伪造验证结果。**
   如果官方校验、测试或构建工具因为环境问题无法运行，必须说明真实失败原因，并使用替代验证补充证据。不要声称原工具通过。

3. **不要绕过权限与安全边界。**
   遇到权限、网络、安装或破坏性操作需求时，按当前 agent 的审批规则申请授权；不要用旁路方式规避审批。

4. **替代方案必须可解释、可验证。**
   使用替代命令、不同编辑工具或手工检查时，记录原始失败、替代动作、验证证据和残余风险。

5. **解决后沉淀可复用经验。**
   如果本技能没有覆盖当前工具链问题，而你已经找到稳定解决方式，必须把通用规则写回 `skills/toolchain-issue-recovery/` 的 `SKILL.md`、`USAGE.md` 或 `evals/evals.json`。一次性项目细节不要写入技能。

6. **全程使用中文。**
   除非用户明确要求使用其他语言，所有与用户的交互、问题记录、恢复说明、测试记录、审计结论和产物说明都必须使用中文。代码、文件路径、命令、API 名、错误原文、技术术语和第三方库名可以保留英文。

</HARD-GATE>

## 处理流程

### 1. 捕获故障事实

记录最小事实：

- 失败命令或工具。
- 关键错误信息。
- 发生位置和目标文件。
- 是否已经产生部分产物。
- 当前权限、沙箱、网络或依赖限制。

不要急着重试同一命令。先判断失败类型。

### 2. 分类并选择方案

优先匹配下面的已知类别。

| 类别 | 判断信号 | 优先方案 |
|---|---|---|
| 编码与中文乱码 | 出现 `椤圭洰鍚嶇О`、`闇€姹傛枃妗` 等 mojibake | 显式 UTF-8 读取/写入，见“编码与中文乱码” |
| 补丁工具失败 | `apply_patch` 报 sandbox/helper/read/update 错误 | 缩小补丁；仍失败时用工作区内原生命令写入，并记录偏离原因 |
| 初始化脚本部分失败 | 目录或模板已创建，但 UI 元数据、校验或后续步骤失败 | 保留有效产物，检查残留，再补齐目标文件 |
| 校验工具缺依赖或解码失败 | `ModuleNotFoundError`、缺少 `yaml`、`UnicodeDecodeError: 'gbk' codec can't decode` 等 | 不宣称校验通过；补齐依赖或启用 UTF-8 模式后重跑；仍不可用时执行替代结构检查 |
| 命令参数不兼容 | 参数不存在、版本差异、PowerShell/cmd 行为差异 | 查询本地帮助或改用更通用命令 |
| 权限或网络限制 | access denied、DNS、registry/index 失败 | 按审批规则申请权限或说明无法完成 |
| 路径与 shell 差异 | 空格路径、反斜杠、通配符、重定向失败 | 使用 `-LiteralPath`、显式工作目录和单一 shell |

### 3. 执行保守恢复

恢复动作要尽量小：

- 优先保留已经正确生成的产物。
- 先读现状，再补齐缺失文件。
- 避免为了“清理现场”删除用户未确认的内容。
- 对目录删除、覆盖、批量移动等操作，只有在用户明确要求或审批通过后执行。

### 4. 替代验证

如果原校验工具不可用，用可观察证据补齐：

- 文件存在性：目标文件和目录是否存在。
- frontmatter：`name` 与 `description` 是否存在且目录名匹配。
- JSON/YAML：能否被本地解析器解析。
- 关键文本：硬门禁、路径约束、中文约束、触发场景是否存在。
- 模板残留：用 `rg` 搜索 待办占位标记 等占位词。
- 范围检查：是否只修改了预期目录。

替代验证通过时，只能说“替代验证通过”；不要说“官方校验通过”。

### 5. 写回经验

当遇到新问题时，解决后判断是否值得写回：

- 未来复现概率较高。
- 恢复步骤可泛化。
- 不是某个项目的一次性路径或临时状态。
- 能帮助 agent 避免误判或不安全操作。

写回位置：

- 通用恢复规则写入 `SKILL.md`。
- 面向人的快速说明写入 `USAGE.md`。
- 可测试场景写入 `evals/evals.json`。

## 编码与中文乱码

这是从旧 `powershell-chinese-encoding` 技能迁移来的方案。

### 快速判断

如果中文显示成类似下面的内容，通常不是文件内容真的坏了，而是读取或输出时用了错误编码：

```text
椤圭洰鍚嶇О
闇€姹傛枃妗
浣滆€?
```

优先怀疑：UTF-8 中文文件被 Windows PowerShell 按 ANSI/GBK 读取。

### 读取中文文件

读取中文 Markdown、JSON、YAML、日志、配置或技能文件时，优先显式指定 UTF-8：

```powershell
Get-Content -Raw -Encoding UTF8 path\to\file.md
```

不要只依赖：

```powershell
Get-Content -Raw path\to\file.md
```

Windows PowerShell 5.1 的默认编码可能不是 UTF-8。

### 写入中文文件

写入或覆盖中文文本时，也要显式指定编码：

```powershell
Set-Content -Path path\to\file.md -Value $content -Encoding UTF8
```

追加内容时：

```powershell
Add-Content -Path path\to\file.md -Value $content -Encoding UTF8
```

如果目标是 PowerShell 7，默认 UTF-8 行为更稳定；但为了跨环境可复现，仍推荐显式写 `-Encoding UTF8`。

### 输出到终端

如果文件读取正确，但外部命令或终端输出仍乱码，可在当前会话设置控制台输出编码：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

这主要影响 PowerShell 与外部程序之间的文本传递，不替代 `Get-Content -Encoding UTF8`。

### 编码诊断

1. 先用 `Get-Content -Raw -Encoding UTF8 <path>` 读取一次。
2. 如果 UTF-8 正常显示，记录结论为“默认读取编码导致乱码”，不要判定文件损坏。
3. 如果 UTF-8 仍乱码，再检查文件实际编码或内容是否已被错误转码。
4. 在测试记录或排查结论中写清楚 PowerShell 版本、读取命令和观察结果。

注意：`Format-Hex` 在不同 PowerShell 版本中的参数不完全一致，不要假设所有环境都支持 `-Count`。

## 已知恢复方案

### apply_patch 在 Windows 沙箱失败

现象示例：

```text
windows sandbox failed: helper_unknown_error: setup refresh had errors
```

处理：

1. 先缩小补丁范围，例如只改一个文件或只新增一个文件。
2. 如果仍然失败，确认目标路径位于工作区可写范围内。
3. 改用同一 shell 的原生命令写入，例如 PowerShell `Set-Content -Encoding UTF8`。
4. 在最终说明中记录：原本应使用 `apply_patch`，但因沙箱 helper 错误改用替代写入。
5. 运行替代验证，确认内容、编码和范围正确。

### 初始化脚本部分失败

现象示例：

```text
[OK] Created skill directory
[OK] Created SKILL.md
[ERROR] short_description must be 25-64 characters
```

处理：

1. 不要重复初始化导致覆盖或混乱。
2. 检查已生成的文件和目录。
3. 保留有效的目录和模板。
4. 补齐缺失产物或替换模板内容。
5. 检查是否生成了多余的 `agents/`、`scripts/`、`references/`、`assets/` 等目录；如需删除，确认它们确实是本次生成且不需要。

### 校验脚本缺依赖

现象示例：

```text
ModuleNotFoundError: No module named 'yaml'
```

处理：

1. 不要声称校验脚本通过。
2. 如果安装依赖需要网络或权限，按审批规则处理。
3. 若不安装依赖，执行替代验证：frontmatter、JSON、关键文本、模板残留、目录范围。
4. 最终说明写清楚“原校验未运行成功，替代验证通过/失败”。


### Windows Python 默认 GBK 解码 UTF-8 文件

现象示例：

```text
UnicodeDecodeError: 'gbk' codec can't decode byte ...
```

常见于 Windows 上运行 Python 校验脚本读取中文 Markdown、YAML 或 JSON 文件时。即使文件本身是正确的 UTF-8，脚本若依赖系统默认文本编码，也可能按 GBK 解码而失败。

处理：

1. 不要判定文件损坏，也不要声称校验通过。
2. 先确认文件可用 UTF-8 正常读取，例如 `Get-Content -Raw -Encoding UTF8 <path>`。
3. 运行 Python 脚本前启用 UTF-8 模式：

   ```powershell
   $env:PYTHONUTF8='1'
   .\.venv\Scripts\python.exe path\to\script.py path\to\target
   ```

4. 如果脚本随后提示 `No YAML frontmatter found`，检查文件是否带 UTF-8 BOM；某些严格校验脚本要求文件第一个字符就是 `-`。
5. 需要重写文件编码时，优先使用 UTF-8 no BOM，并明确记录这是为适配严格校验工具，不是内容变更。
6. 如果仍无法运行原校验，执行替代验证，并说明原校验失败原因与替代验证结果。
## 完成前检查

结束前确认：

- 已记录原始错误和失败工具。
- 已说明使用了哪种恢复方案。
- 没有绕过权限、安全或用户确认。
- 如果使用替代验证，已明确它不是原工具校验。
- 如果问题是新类型，已判断是否需要写回技能。
- 中文乱码处理已显式使用 UTF-8 读写策略。


