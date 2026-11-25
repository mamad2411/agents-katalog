---
name: paper-explain-figures
description: 解读论文 Figure 的含义并输出一份“教会人类如何读图”的高可读性 Markdown 报告；支持输入 1 个或多个 figure 文件绝对路径与人工解读，自动尝试从图附近检索生成该图的源代码，并采用类似 parallel-vibe 的方式通过 `codex exec`/`claude -p` 以进程级隔离解读每张图（并发上限默认 3，可在 config.yaml 调整）。⚠️ 不适用：用户只是想改图尺寸/裁剪/改格式；或要求直接修改图片/源代码（本 skill 对图片与源代码全程只读，严禁修改）。
metadata:
  author: Bensz Conan
---
# paper-explain-figures

对用户提供的 1 张或多张论文 Figure：

- 将 Figure 转为 `.jpg`（用于视觉理解；转换失败则保留原图并显式说明）
- 在 Figure 附近自动检索“生成该图的源代码”（可能找不到；找不到则为 `NULL`）
- 综合三类信息输出可读性强的报告：
  - 理解 1：视觉理解（从 jpg/原图直接读图）
  - 理解 2：源代码理解（以代码为准；代码决定图的真实含义）
  - 理解 3：用户人工解读（帮助猜测用户关注点；可能有误）

### 输入

用户会输入 1 个或多个信息：

- 1 个或多个 figure 文件的**绝对路径**
- 可选：对 figure 的人工解读（全局或按 figure 分配）
- 可选：用户显式给出源代码文件绝对路径（优先作为“候选入口”）

## 流程

### 输入

按用户请求和配置文件提供必要输入；缺失信息应明确列出并停止依赖该输入的步骤。

### 执行步骤

- 因本 skill 设计缺陷导致的 bug，先用 `bensz-collect-bugs` 规范记录到 `~/.bensz-skills/bugs/`，不要直接修改用户本地已安装的 skill 源码；若有 workaround，先记 bug，再继续完成任务。
- 只有用户明确要求“report bensz skills bugs”等公开上报时，才用本地 `gh` 上传新增 bug 到 `huangwb8/bensz-bugs`；不要 pull / clone 整个仓库。

> 文件位置： xxx
> 源代码： xx.R 第xxx-xxx行

### 图表核心含义

...

### 变量定义

| 元素 | 定义 |
| --- | --- |
| ... | ... |

### 解读要点

1. ...
2. ...

### 解释

...

### 科学价值

...
```

为保证“每张图的解读相互独立”，本 skill 采用 worker 脚本在 shell 中启动独立进程执行：

- `codex exec "..."`（推荐：更容易做本地文件读取 + 视觉理解）
- `claude -p "..."`（可选）

并发上限默认 **3**（可在 `paper-explain-figures/config.yaml` 调整）。

在当前目录运行（推荐，产物会落到当前目录与 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/paper-explain-figures/`）：

```bash
python3 paper-explain-figures/scripts/paper_explain_figures.py \
  --fig /abs/path/to/figure1.png \
  --fig /abs/path/to/figure2.pdf \
  --note "你对这些图的关注点/背景解释（可选）"
```

如果该 skill 已做系统级安装（路径因平台而异，以下仅示例）：

```bash
python3 ~/.codex/skills/paper-explain-figures/scripts/paper_explain_figures.py --fig /abs/path/to/figure.png
```

常用参数（按需）：

```bash
# 启用并行（默认串行，减少 API 限流/封禁风险）
python3 paper-explain-figures/scripts/paper_explain_figures.py --fig /abs/path/to/figure.png --parallel

# 并发上限（默认 3；也可改 config.yaml:defaults.max_parallel）
python3 paper-explain-figures/scripts/paper_explain_figures.py --fig /abs/path/to/figure.png --parallel --max-parallel 3

# 指定 runner（codex/claude/local）
python3 paper-explain-figures/scripts/paper_explain_figures.py --fig /abs/path/to/figure.png --runner codex
```

⚠️ 安全提示：`--runner shell` 已禁用，因为它无法对“.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/paper-explain-figures 之外绝不泄露中间文件”提供严格保证。

在触发目录执行：

```bash
rm -rf .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/paper-explain-figures
```

### 输出

- 最终报告：默认输出到当前工作目录 `paper-explain-figures_report.md`
- 所有中间文件与日志：落到 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/paper-explain-figures/`（按 run/job 分目录保存）

每张图在同一个 Markdown 文件中以 `##` 级标题分隔：

```markdown
# Figures

### 输出管理

本 Skill 的新任务中间文件统一写入 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/{skill名}/input|output|log/`。同一任务复用一个任务根目录；多 Skill 协作才创建 `shared/`。正式交付物不写入该目录，历史隐藏目录只允许显式兼容读取、迁移或清理。

### 校验

完成后执行 Skill 已有的静态检查、脚本验证或人工复核，并记录通过标准。

### 失败与恢复

保留错误证据和已完成产物；仅在输入、环境或外部依赖恢复后从最近的失败步骤重试。

## 约束

- **目录管理硬约束**：所有中间产物必须托管在当前工作目录下的隐藏目录 **`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/paper-explain-figures/`**（该目录名在脚本中硬编码；不允许改到别处）。
- **运行时隔离硬约束**：runner / 图片转换器产生的 HOME、TMP、XDG cache/state/config 等运行时辅助文件，也必须重定向并收纳到 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/paper-explain-figures/` 内。
- **只读约束**：全程只读访问用户的 Figure 与源代码文件；严禁修改它们（包括格式化/重写/覆盖）。

### 公共硬约束

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- 仅将 Skill 或 Bensz 基础设施本身的设计缺陷交给 `bensz-collect-bugs`；先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。
<!-- End of canonical common constraints. -->

### Skill 专属约束

不得超出本 Skill description 和上方流程所声明的范围；不将未验证的信息伪装成确定结论。
