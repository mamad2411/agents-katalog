---
name: agent-cli-toolkit
description: 终端取证与 CLI 自动化优先：用 rg/fd、bat、sd、delta/difft、http/jq、fzf、hyperfine、dust/duf/procs/btm、gh/gh-llm、x/vp/bun/uv；多窗格/命名会话/长时并行或 layout 用 zellij。应在用户或任务出现「终端/命令行/shell/CLI」「在机器上跑/验证」「搜仓库/找文件」「看 diff 或 JSON」「查 PR/Issue/GitHub」「磁盘/进程/性能对比」「并行跑多个服务或测试」「tmux 式多会话」或 agent 需用上述工具链而非仅靠编辑器时加载。
---

## 目的

当任务需要在终端里浏览代码、改写文本、查看 diff、排查系统状态、调用 HTTP API 或管理大文件时，优先使用这组现代 CLI，而不是退回到更原始或更低效的命令。

## 不适用

- 主要任务是设计系统边界而不是用 CLI 获取现场
- 主要任务是写业务方案或项目 kickoff，而不是终端探索
- 只是单文件的小编辑，且不需要终端证据

## 工具总览

### 代码与文件

- `rg`：全文搜索首选；替代笨重的 `grep -R`。
- `fd`：按名字找文件/目录；替代 `find` 的常见场景。
- `bat`：带行号和高亮地查看文件；适合快速人工检查。
- `sd`：批量文本替换；比 `sed` 更适合简单改写。
- `lsd`：更易读的目录列表和树形视图。

### Git 与 diff

- `gh`：读 PR / Issue / checks / run logs 的首选 GitHub CLI。
- `gh-llm` / `gh llm`：给 agent 读 GitHub 对话、时间线和 review thread 的高信噪比界面。
- `git-delta`（`delta`）：更易读的 diff 输出。
- `difftastic`（`difft`）：语法感知 diff，适合看代码结构变化。
- `git-lfs`：仓库里有大文件或 LFS 指针时使用。

### API、数据与筛选

- `httpie`（`http`）：调试 HTTP API。
- `jq`：解析、过滤、格式化 JSON。
- `fzf`：在大量候选项里做交互式筛选。

### 性能与系统观测

- `hyperfine`：对两个或多个命令做基准对比。
- `bottom`（`btm`）：交互式看 CPU / 内存 / 进程。
- `procs`：更友好的进程查看。
- `dust`：看目录体积构成。
- `duf`：看磁盘占用。

### 终端多路复用与布局（zellij）

- `zellij`：终端 multiplexer；命名会话、多窗格/tab、layout（`.kdl`）编排，适合并行跑 dev server、测试、日志与 `rg` 等。
- 与「开一个 shell 顺序执行」相比：需要**可恢复的命名会话**、**同一终端里多窗格并行**、或**用 layout 一键拉起多面板**时用 zellij。
- 已在 zellij 会话内时，可用 `zellij run`（`zellij r`）在新窗格里跑命令；自动化脚本注意 `--cwd`、`--close-on-exit`、以及非交互场景下是否改用普通后台进程。

### 语言工具链

- `x-cmd`（`x`）：跨平台安装和更新 CLI 的统一入口。
- `vp`（Vite+）：Vite 项目统一入口；`vp dev` / `vp build` / `vp check` / `vp test` / `vp install`。安装：`curl -fsSL https://vite.plus | bash`。
- `bun`：安装或执行 JavaScript / TypeScript CLI。
- `uv`：Python 依赖、虚拟环境与工具安装首选。

### Vite+ 项目常用命令

```bash
vp install          # 安装依赖
vp dev              # 开发服务器
vp build            # 生产构建
vp check            # 格式化 + lint + 类型检查
vp test             # 运行测试
vp run <script>     # 执行 package.json 脚本
```

### 安装与扩展管理

- `x env use ...`：统一安装或升级常用 CLI。
- `gh extension ...`：安装、升级、列出 GitHub CLI 扩展。

## Agent 使用规则

1. 搜代码优先 `rg`，找文件优先 `fd`，不要默认回退到 `grep -R` 或复杂 `find`。
2. 做简单文本替换时优先 `sd`，避免为纯文本改动写复杂 `sed`。
3. 看 JSON 响应时总是配合 `jq`，避免肉眼硬读一整行。
4. 比较实现差异时，先尝试 `delta` 或 `difft`，再决定是否需要更深入的人工阅读。
5. 涉及性能判断时，用 `hyperfine` 拿真实数据，不靠感觉。
6. 遇到大文件、磁盘或进程问题时，优先用 `dust`、`duf`、`procs`、`btm` 获取现场信息。
7. 读 GitHub PR / Issue 时，优先 `gh`；如果需要保留更完整的 timeline、review thread、action hints，就切到 `gh-llm`。
8. `fzf`、`btm` 这类交互式工具只在当前终端可交互时使用；自动化脚本里优先选非交互命令。
9. 需要多窗格并行、命名会话、或 layout 编排长时任务时，用 `zellij`（`ls` / `attach` / `run` / `-n`/`-l` + layout）；不要为「单条顺序命令」强行开 multiplexer。

## 常用命令模板

### 搜索与浏览

```bash
rg "TODO|FIXME" .
fd "install" skills
bat --style=plain --paging=never install.sh
lsd -la
```

### 替换

```bash
sd "old_value" "new_value" path/to/file
```

### HTTP 与 JSON

```bash
http GET :3000/health
http POST :3000/api/tasks name=demo done:=false
http GET :3000/api/tasks | jq
```

### Diff 与大文件

```bash
git diff -- . ':(exclude)dist' | delta
difft path/to/old-file path/to/new-file
git lfs ls-files
```

### GitHub 与扩展

```bash
x env use gh bun uv jq rg fd sd lsd bottom dust procs delta difft hyperfine httpie
gh auth status
gh pr view 7 --comments
gh run list
gh run view 123456 --log
gh extension list
gh extension install ShigureLab/gh-llm
gh llm pr view 7 --repo zrr1999/skills
gh llm issue view 12 --repo owner/repo
```

### gh-llm 适用场景

- 先看 PR 全貌：`gh llm pr view <编号> --repo <owner/repo>`
- 只看 checks：`gh llm pr checks --pr <编号> --repo <owner/repo>`
- 展开隐藏时间线：`gh llm pr timeline-expand 2 --pr <编号> --repo <owner/repo>`
- 开始 review：`gh llm pr review-start --pr <编号> --repo <owner/repo>`
- 提交 review：`gh llm pr review-submit --event COMMENT --body '...' --pr <编号> --repo <owner/repo>`

### 观测与基准

```bash
hyperfine 'rg agent skills' 'fd agent skills'
procs rg
dust .
duf
```

### zellij（会话与窗格）

```bash
zellij -s myproj              # 新建命名会话
zellij ls                     # 列出活动会话（同 list-sessions）
zellij attach myproj          # 附加到会话（同 zellij a myproj）
zellij kill-session myproj    # 结束指定会话
zellij -n path/to/layout.kdl  # 总是用布局新开会话（从脚本/外部调用时更明确）
zellij -l path/to/layout.kdl  # 无会话时新开；已在 zellij 内则把该布局加成新 tab
zellij run --cwd /path/to/repo -- bash -lc 'vp dev'   # 在新窗格跑命令
zellij run -c -- echo done    # 命令结束即关窗格
```

## 选择建议

- Vite 项目开发/构建/检查：`vp dev` / `vp build` / `vp check`
- 只改字面文本：`sd`
- 查 GitHub PR / Issue：`gh`
- 查 GitHub 完整对话 / review thread：`gh llm`
- 查 API：`http` + `jq`
- 查性能：`hyperfine`
- 查磁盘和进程：`dust` / `duf` / `procs` / `btm`
- 查 Git 变更可读性：`delta` / `difft`
- 多窗格/命名会话/布局并行：`zellij`
