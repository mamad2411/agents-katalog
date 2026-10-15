---
name: done-check
description: |
  开发完成验收 skill。当 agent 认为某项开发任务（功能开发、Bug 修复、重构、配置变更等）已经完成时，
  必须在提交或宣告完成前执行一轮系统性验收，逐项确认代码质量、测试通过、需求达成、文档同步、无回归风险。
  验收方式按项目类型（CLI / Web / Server）区分，各有专属检查项。
  本 skill 适用于任何涉及代码修改的任务收尾阶段。
  判断准则：agent 准备说"完成了"或准备提交代码时，即应激活本 skill。
---

# done-check — 开发完成验收

## 1. 原则声明

> **完成不是"我写完了"，而是"我验证过了"（Done means Verified）。**

"代码写完了"不等于"任务完成了"。在宣告完成之前，agent 必须对本次变更进行系统性自检，确保：

- 变更真正满足了原始需求
- 自动化测试全部通过
- 构建/编译无错误
- **按项目类型完成了手动验证**（CLI 实际运行 / Web 浏览器验证 / Server 接口请求）
- 没有引入回归或副作用
- 代码质量达标（lint、类型检查、无遗留调试代码）
- 相关文档已同步更新

**只有通过验收检查清单，才能向用户宣告任务完成。**

## 2. 适用范围

| 场景 | 是否需要验收 | 说明 |
|------|-------------|------|
| 功能开发 | ✅ 必须 | 完整需求闭环，需逐项确认 |
| Bug 修复 | ✅ 必须 | 确认 bug 已修复且无回归 |
| 重构 | ✅ 必须 | 确认行为不变、测试全过 |
| 配置变更 | ✅ 必须 | 确认配置生效、不影响其他功能 |
| 一行修复 / typo | ⚡ 轻量验收 | 至少确认构建通过、无明显副作用 |
| 纯文档更新 | ❌ 跳过 | 无代码逻辑变更 |

**核心准则**：只要修改了代码（哪怕是"一行"），就必须至少跑一遍 §5 的"快速验收"。

## 3. 识别项目类型

验收方式取决于项目类型。在开始验收前，先判断当前项目属于哪一类：

| 类型 | 识别特征 | 典型项目 |
|------|---------|---------|
| **CLI** | 有命令行入口（`bin/`、`cli.ts`、`main.go`）、解析参数、读写 stdin/stdout | 命令行工具、脚手架、devtools |
| **Web** | 有前端框架（React/Vue/Svelte）、HTML 模板、CSS/样式、用户交互界面 | Web 应用、管理后台、Landing Page |
| **Server** | 有 HTTP 路由 / API 端点、数据库连接、认证中间件 | API 服务、微服务、BFF |

**混合型项目**：Monorepo 或全栈项目可能同时包含多种类型（如 `apps/web` + `apps/server`）。此时按改动的具体模块选择对应的验收方式。

> 确定类型后，在 §8 中找到对应的分类验收要求，与 §6 的通用流程配合使用。

## 4. 验收流程总览

```
┌──────────────────────────────────────────────────────────┐
│  Step 1: 变更盘点 — 回顾改了什么、为什么改                │
│  Step 2: 需求回溯 — 逐条对照原始需求是否达成              │
│  Step 3: 自动化验证 — 测试 / 构建 / lint / 类型检查        │
│  Step 4: 手动验证 — 按项目类型实际操作验证（见 §8）       │
│  Step 5: 自审 Diff — 逐文件 review 自己的改动             │
│  Step 6: 回归排查 — 确认没有影响其他功能                  │
│  Step 7: 收尾清理 — 移除调试代码、TODO、临时代码           │
│  Step 8: 文档同步 — 确认文档已更新（配合 doc-first）       │
│  Step 9: 宣告完成 — 通过检查清单后向用户汇报              │
└──────────────────────────────────────────────────────────┘
```

## 5. 快速验收（轻量任务）

对于 typo、一行修复等微小变更，至少执行以下检查：

1. **构建通过**：项目能正常构建/编译
2. **无语法错误**：相关文件无语法问题
3. **无副作用**：改动范围极小，不影响其他逻辑
4. **diff 干净**：`git diff` 中没有意外的改动

执行完成后，向用户简述做了什么变更、验证了什么。

## 6. 完整验收（标准任务）

### 6.1 Step 1 — 变更盘点

在验收开始时，首先回顾本次变更的全貌：

```bash
# 查看所有改动
git diff --stat
git diff
```

- 列出所有新增 / 修改 / 删除的文件
- 确认每处改动都能解释"为什么改"
- 标注是否有预期之外的文件被改动（如误改配置文件、无关文件）

**如果发现无法解释的改动 → 立即排查，可能是误操作。**

### 6.2 Step 2 — 需求回溯

回到任务起点，逐条确认原始需求是否达成：

| 检查项 | 确认方式 |
|--------|---------|
| 核心功能是否实现 | 对照需求描述，列出"做了什么"，验证是否覆盖 |
| 边界条件是否处理 | 空数据？超大数据？非法输入？并发？ |
| 异常场景是否覆盖 | 失败时是否优雅降级或报错？ |
| 验收标准是否满足 | 需求中提到的"完成标准"是否逐条达成 |

**如果需求中有未实现的项 → 不要宣告完成，继续开发或明确告知用户未完成的部分。**

> 如果项目使用了 `spec-first` 技能，对照 `.specs/<requirement-name>/spec.md` 中的方案逐条核对。

### 6.3 Step 3 — 自动化验证

运行项目所有自动化检查，**全部必须通过**：

```bash
# 1. 测试套件（全量运行，不要只跑改动相关的测试）
<项目测试命令>           # 如 npm test / bun test / pytest / go test ./...

# 2. 构建
<项目构建命令>           # 如 npm run build / cargo build / go build ./...

# 3. 类型检查（如有）
<项目类型检查命令>       # 如 tsc --noEmit / mypy / pyright

# 4. Lint / 代码风格（如有）
<项目lint命令>           # 如 eslint . / ruff check . / golangci-lint run
```

**处理原则**：

- ❌ 测试失败 → **不允许**宣告完成。必须修复或明确说明原因
- ⚠️ 有 warning → 评估是否需要处理；能修尽修，不能修的在汇报中说明
- ✅ 全部通过 → 进入下一步

> **命令来源**：优先使用 `AGENTS.md` 中记录的构建/测试命令，其次是 `package.json` / `Makefile` / `pyproject.toml` 等配置文件中的 script。

### 6.4 Step 4 — 手动验证

自动化测试通过**不代表功能正常**。agent 必须按项目类型执行手动验证：

- **CLI** → 实际运行命令，检查输出、退出码、边界行为（详见 §8.1）
- **Web** → 确认页面渲染、交互流程、浏览器控制台无报错（详见 §8.2）
- **Server** → 实际发送请求，验证响应状态码、数据格式、错误处理（详见 §8.3）

> **这是最容易被跳过的步骤，也是最能发现问题的步骤。不要省略。**

### 6.5 Step 5 — 自审 Diff

agent 必须以**审查者**的视角重新审视自己的每一处改动：

```bash
git diff
```

逐文件检查：

| 审查维度 | 关注点 |
|----------|--------|
| 正确性 | 逻辑是否正确？有没有遗漏的分支？ |
| 安全性 | 有没有引入安全风险？（如硬编码密钥、SQL 注入、XSS） |
| 性能 | 有没有明显的性能问题？（如 N+1 查询、不必要的循环、全量渲染） |
| 健壮性 | 空值 / 异常输入是否处理？资源是否释放？ |
| 代码风格 | 是否符合项目既有风格？命名是否一致？ |
| 复杂度 | 是否过度设计？能否更简洁？ |
| 遗留物 | 有没有 `console.log` / `debugger` / `print` / 注释掉的代码？ |

**发现问题时**：立即修复，修复后重新回到 Step 3 验证。

### 6.6 Step 6 — 回归排查

确认本次变更**不会破坏已有功能**（通用检查 + §8 类型专属检查）：

**通用排查**：

- **搜索引用**：被修改/删除的函数、变量、接口、组件是否被其他地方引用？
  ```bash
  # 用 Grep 工具搜索被修改的标识符
  ```
- **影响范围**：改动是否涉及公共模块、工具函数、共享类型？如有，追踪所有调用方
- **配置变更**：如果改了配置文件，是否影响其他环境？

**类型专属排查**：见 §8 各类型的"回归排查"部分。

### 6.7 Step 7 — 收尾清理

在最终提交前，清理一切临时性内容：

- [ ] 移除调试代码：`console.log` / `print` / `debugger` / `dump()`
- [ ] 移除注释掉的代码块（保留有意义的注释，删除无用的注释代码）
- [ ] 移除临时的 `TODO` / `FIXME` / `HACK`（如果是临时标记，已完成就删除；如果确实需要后续处理，创建 issue 并在代码中标注 issue 编号）
- [ ] 移除未使用的 import / 变量 / 死代码
- [ ] 确认没有遗留的临时文件（如 `test.txt`、`tmp/`、`.bak`）

### 6.8 Step 8 — 文档同步

> 配合 `doc-first` 技能使用。

确认本次变更涉及的所有文档已同步更新：

| 变更类型 | 需检查的文档 |
|----------|-------------|
| 新增/修改功能 | `README.md`、`docs/guide/`、用户手册 |
| 接口变更 | `docs/api/`、接口文档 |
| 架构调整 | `docs/architecture/`、`AGENTS.md` |
| 配置项变更 | `docs/CONFIGURATION.md` 或 `docs/ops/` |
| 目录结构变化 | `AGENTS.md` |
| 新增依赖 | 安装文档、`package.json` / `requirements.txt` 等 |

**如果文档与代码不一致 → 先更新文档，再宣告完成。**

### 6.9 Step 9 — 生成验收报告并宣告完成

通过全部验收后，agent 必须在 `.reports/` 目录下生成本次任务的** HTML 验收报告**，然后在对话中向用户简要汇报并附上报告路径。

详细目录约定与报告模板见 §7。

```bash
# 在 .reports/<task-name>/ 下生成 report.html
# 浏览器直接打开即可查看
```

对话中的简要汇报（附报告路径）：

> ✅ 任务完成。验收报告已生成：`.reports/<task-name>/report.html`
>
> 核心结果：测试全过、构建成功、手动验证通过（CLI / Web / Server 各项）。
> 详细内容请查看报告。

**禁止行为**：
- ❌ 只在对话中口述结果，不生成报告文件
- ❌ 生成纯文本/Mardown 报告代替 HTML（HTML 报告是必需的产出物）
- ❌ 报告内容与实际验证结果不符

## 7. 验收报告

每次验收完成后，在 `.reports/` 目录下生成本次任务的 **HTML 验收报告**。报告是验收的**必需产出物**——没有报告，验收视为未完成。

### 7.0 `.reports/` 目录约定

```
.reports/                        # 验收报告工作区（不提交到 Git）
└── <task-name>/                 # 任务目录，kebab-case 命名，如 user-export
    └── report.html              # HTML 验收报告（自包含，浏览器直接打开）
```

**规则**：

- `.reports/` 已在 `.gitignore` 中忽略，**不提交到版本控制**——它是 agent 与用户之间的验收记录。
- 目录名用 kebab-case，与任务/需求名称对应（如项目使用 `spec-first`，沿用 `.specs/` 中的需求名）。
- 每个任务一个子目录，互不干扰。

### 7.1 报告内容

HTML 报告必须包含以下板块：

| 板块 | 内容 |
|------|------|
| **任务概要** | 任务名称、日期、项目类型（CLI / Web / Server）、一句话摘要 |
| **改动文件** | 每个文件的路径 + 改动说明 |
| **验证结果** | 逐项列出，每项标注状态：✅ 通过 / ⚠️ 部分通过 / ⏳ 待验证 / ❌ 失败 |
| **需求达成** | 逐条对照原始需求，标注达成状态 |
| **类型专属验证** | 按 §8（CLI / Web / Server）展示该类型的检查结果 |
| **遗留事项** | 待跟进、已知风险、下一步建议 |

### 7.2 报告模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>验收报告 - <task-name></title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, "PingFang SC", sans-serif;
           background: #f5f5f5; color: #333; line-height: 1.6; }
    .container { max-width: 860px; margin: 0 auto; padding: 32px 24px; }
    h1 { font-size: 28px; margin-bottom: 8px; }
    h2 { font-size: 20px; margin: 32px 0 12px; padding-bottom: 8px;
         border-bottom: 2px solid #e8e8e8; }
    .meta { color: #999; font-size: 14px; margin-bottom: 24px; }
    .summary { background: #fff; border-radius: 8px; padding: 20px;
               margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    .summary p { font-size: 16px; }
    .badge { display: inline-block; padding: 2px 10px; border-radius: 12px;
             font-size: 13px; font-weight: 500; margin-left: 8px; }
    .badge-cli { background: #e6f7ff; color: #1890ff; }
    .badge-web { background: #f6ffed; color: #52c41a; }
    .badge-server { background: #fff7e6; color: #fa8c16; }
    table { width: 100%; border-collapse: collapse; background: #fff;
            border-radius: 8px; overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 16px; }
    th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #f0f0f0; }
    th { background: #fafafa; font-weight: 600; font-size: 14px; }
    td { font-size: 14px; }
    td:first-child { font-family: monospace; font-size: 13px; }
    .status { font-weight: 600; white-space: nowrap; }
    .pass { color: #52c41a; }
    .warn { color: #faad14; }
    .pending { color: #1890ff; }
    .fail { color: #f5222d; }
    .file-list { background: #fff; border-radius: 8px; padding: 16px 20px;
                 box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    .file-list li { list-style: none; padding: 8px 0;
                    border-bottom: 1px solid #f5f5f5; }
    .file-list li:last-child { border-bottom: none; }
    .file-list code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px;
                      font-size: 13px; }
    .notes { background: #fffbe6; border: 1px solid #ffe58f; border-radius: 8px;
             padding: 16px 20px; margin-top: 16px; }
    .notes li { margin-left: 20px; margin-top: 4px; }
    .stat-bar { display: flex; gap: 24px; margin: 16px 0; }
    .stat { text-align: center; }
    .stat-num { font-size: 28px; font-weight: 700; }
    .stat-label { font-size: 12px; color: #999; margin-top: 4px; }
  </style>
</head>
<body>
<div class="container">

  <!-- 标题 -->
  <h1>验收报告 <span class="badge badge-cli">CLI</span></h1>
  <p class="meta">任务：<task-name>　|　日期：2025-01-15　|　项目类型：CLI</p>

  <!-- 概要 -->
  <div class="summary">
    <p>实现了用户数据导出功能，支持 CSV / JSON 格式，包含异步任务处理。</p>
    <div class="stat-bar">
      <div class="stat"><div class="stat-num pass">12</div><div class="stat-label">通过</div></div>
      <div class="stat"><div class="stat-num pending">1</div><div class="stat-label">待验证</div></div>
      <div class="stat"><div class="stat-num warn">0</div><div class="stat-label">部分通过</div></div>
      <div class="stat"><div class="stat-num fail">0</div><div class="stat-label">失败</div></div>
    </div>
  </div>

  <!-- 改动文件 -->
  <h2>改动文件</h2>
  <ul class="file-list">
    <li><code>src/commands/export.ts</code> — 新增导出子命令</li>
    <li><code>src/services/export-service.ts</code> — 导出逻辑（CSV/JSON）</li>
    <li><code>src/utils/async-task.ts</code> — 异步任务封装</li>
  </ul>

  <!-- 验证结果 -->
  <h2>验证结果</h2>
  <table>
    <thead><tr><th>项目</th><th>命令 / 操作</th><th>状态</th><th>备注</th></tr></thead>
    <tbody>
      <tr><td>测试</td><td><code>bun test</code></td><td class="status pass">✅ 通过</td><td>24/24 通过</td></tr>
      <tr><td>构建</td><td><code>bun build</code></td><td class="status pass">✅ 通过</td><td></td></tr>
      <tr><td>类型检查</td><td><code>tsc --noEmit</code></td><td class="status pass">✅ 通过</td><td></td></tr>
      <tr><td>Lint</td><td><code>eslint .</code></td><td class="status pass">✅ 通过</td><td></td></tr>
      <tr><td>--help</td><td><code>my-tool export --help</code></td><td class="status pass">✅ 通过</td><td>用法说明完整</td></tr>
      <tr><td>非法参数</td><td><code>my-tool export --bad</code></td><td class="status pass">✅ 通过</td><td>退出码 1，错误提示清晰</td></tr>
      <tr><td>API 调用</td><td><code>my-tool export --from api</code></td><td class="status pending">⏳ 待验证</td><td>已引导用户配置 API_KEY，等待后继续</td></tr>
    </tbody>
  </table>

  <!-- 需求达成 -->
  <h2>需求达成</h2>
  <table>
    <thead><tr><th>需求项</th><th>状态</th><th>备注</th></tr></thead>
    <tbody>
      <tr><td>支持 CSV 格式导出</td><td class="status pass">✅ 达成</td><td></td></tr>
      <tr><td>支持 JSON 格式导出</td><td class="status pass">✅ 达成</td><td></td></tr>
      <tr><td>大数据量异步处理</td><td class="status pass">✅ 达成</td><td>1000 条以上自动异步</td></tr>
    </tbody>
  </table>

  <!-- 遗留事项 -->
  <h2>遗留事项</h2>
  <div class="notes">
    <ul>
      <li>⏳ API 调用验证：已引导用户配置 <code>OPENAI_API_KEY</code>，配置完成后继续验证</li>
      <li>📝 建议后续补充导出进度条交互</li>
    </ul>
  </div>

</div>
</body>
</html>
```

> **模板说明**：
> - 报告为**自包含 HTML**（内联 CSS，无外部依赖），浏览器直接打开即可查看
> - `<span class="badge badge-cli">` 根据项目类型替换：CLI → `badge-cli`，Web → `badge-web`，Server → `badge-server`
> - 状态标注：`pass`（✅ 通过）/ `warn`（⚠️ 部分通过）/ `pending`（⏳ 待验证）/ `fail`（❌ 失败）
> - 多任务可拆分多个 HTML，或在同一报告中用分隔区块展示

## 8. 按项目类型验收

不同类型的项目，验收重点截然不同。找到对应类型，执行该类型的全部检查项。

### 8.1 CLI 工具

#### 手动验证

agent 必须将 CLI **作为最终用户来运行**，而非只读代码：

| 验证项 | 操作 | 预期 |
|--------|------|------|
| **基本功能** | 用真实参数运行命令 | 输出符合预期 |
| **`--help` / `-h`** | 运行帮助命令 | 显示用法说明、参数列表、示例 |
| **`--version` / `-v`** | 运行版本命令 | 正确显示版本号 |
| **无参数** | 不传参数直接运行 | 显示帮助或合理的默认行为，不应崩溃 |
| **非法参数** | 传入不存在的 flag 或无效值 | 显示友好的错误提示，退出码非 0 |
| **退出码** | 正常 / 错误场景分别运行 | 成功 = `0`，失败 = 非 `0` |
| **stdin 输入** | 通过管道传入数据 | 正确读取并处理 |
| **stdout / stderr 分离** | 重定向验证 `1>` 和 `2>` | 正常输出 → stdout，错误/日志 → stderr |
| **输出格式** | 管道场景下检查输出 | 可被其他命令消费（如 `| jq`、`| grep`） |

```bash
# 示例：CLI 手动验证
my-tool --help                    # 检查帮助信息
my-tool --version                 # 检查版本号
my-tool                           # 无参数行为
my-tool --invalid-flag            # 错误处理 + 退出码
echo "data" | my-tool process     # stdin 输入
my-tool run > /dev/null 2>err.log # stderr 分离
my-tool --json output | jq .      # 输出可被消费
```

#### 密钥与环境变量

CLI 工具常依赖外部密钥或环境变量才能实际运行（如 `OPENAI_API_KEY`、`GITHUB_TOKEN`）。agent **不得经手密钥**——密钥只在用户手中，由用户自行配置，agent 验证配置是否就绪后继续验收。

**铁律：agent 绝不要求用户在对话中提供密钥值，也绝不将密钥写入文件或命令。**

**Step 1：识别所需配置**

在运行命令前，扫描代码和配置，列出 CLI 运行所需的全部环境变量/密钥：

```bash
# 用 Grep 工具搜索 process.env / os.environ / getenv / dotenv 等
```

区分两类：

| 类别 | 示例 | 由谁配置 |
|------|------|---------|
| **密钥型**（API key、token、密码） | `OPENAI_API_KEY`、`GITHUB_TOKEN` | 用户自行配置，agent **不经手** |
| **配置型**（URL、端口、开关） | `DATABASE_URL`、`PORT`、`DEBUG` | agent 可用本地测试值 |

**Step 2：引导用户自行配置**

根据 CLI 的配置方式，引导用户完成设置（给出具体命令，让用户**在自己的终端执行**）：

```
CLI 提供了 config 子命令：

  my-tool config set openai-api-key

或直接写入环境变量（在您的终端中执行）：

  export OPENAI_API_KEY=sk-xxxx

配置完成后告诉我，我继续验收。
```

- 根据 CLI 已有的配置机制选择引导方式（`config` 子命令 / `.env` 文件 / `export` / 系统钥匙串等）
- 给出**具体命令**，不要只说"请配置一下"
- 让用户**自行执行**，完成后告知 agent

**禁止行为**：
- ❌ 要求用户在对话中直接粘贴密钥值
- ❌ 替用户把密钥写入 `.env` 文件或配置文件
- ❌ 在命令行参数中传递密钥（会泄露到 shell history / 进程列表）
- ❌ 用占位符（如 `test`、`fake-key`）假装验证通过
- ❌ 在代码中硬编码密钥来绕过验证

**Step 3：分层验证**

即使用户尚未完成配置，也要**先验证不依赖密钥的部分**：

| 可独立验证（无需密钥） | 需密钥才能验证 |
|----------------------|---------------|
| `--help` / `--version` | 调用外部 API 的命令 |
| 无参数 / 非法参数处理 | 数据库读写操作 |
| 参数校验与错误提示 | 需要认证的子命令 |
| stdout / stderr 分离 | 发送通知 / 邮件 |
| 本地数据处理流程 | 连接远程服务 |

用户完成配置后，继续验证剩余项。如果用户暂时无法提供，如实标注。

**Step 4：如实汇报**

在完成报告中明确区分**已验证**和**因缺少密钥未能验证**的项：

```
### 验证结果
- ✅ `--help` / `--version` — 正常
- ✅ 非法参数处理 — 错误提示友好，退出码正确
- ✅ 本地数据处理 — 输出正确
- ⏳ API 调用 — 待验证（已引导用户配置 `OPENAI_API_KEY`，等待完成后继续）
- ⚠️ 数据库操作 — 未验证（需要 `DATABASE_URL`，已用本地 SQLite 做了部分测试）
```

> 密钥未配置不是跳过验收的借口，而是**区分验收阶段**的依据：先验能验的，引导用户配置后继续验剩余的，最终如实汇报每项状态。

#### 回归排查

- **参数兼容性**：是否删除/重命名了已有参数？已有用户的命令行脚本是否会报错？
- **输出格式**：输出格式是否变化？下游脚本是否依赖当前输出格式？
- **退出码**：退出码语义是否变化？调用方是否依赖退出码判断？
- **配置文件**：配置文件格式是否变化？旧配置是否兼容？

---

### 8.2 Web 前端

#### 手动验证

agent 必须在**浏览器中实际打开页面**，验证用户可感知的行为：

| 验证项 | 操作 | 预期 |
|--------|------|------|
| **页面渲染** | 打开涉及的页面 | 内容正确渲染，无布局错乱、白屏 |
| **核心交互** | 按用户流程实际操作（点击/输入/提交） | 交互行为符合预期 |
| **响应式** | 调整窗口宽度或使用 DevTools 模拟移动端 | 不同断点下布局正常 |
| **浏览器控制台** | 打开 DevTools Console | 无 error、无 warning |
| **网络请求** | 打开 DevTools Network | 请求成功、响应格式正确、无 4xx/5xx |
| **加载状态** | 观察数据加载过程 | 有 loading 指示，不会长时间空白 |
| **空状态** | 数据为空时的页面 | 显示友好的空状态提示，非空白 |
| **错误状态** | 模拟接口失败 | 显示错误提示，不崩溃、不白屏 |

```bash
# 示例：启动开发服务器进行手动验证
bun run dev    # 或 npm run dev
# → 在浏览器中打开，逐项验证上表
```

> 如果 agent 无法在真实浏览器中操作，至少应：
> 1. 启动开发服务器，用 `curl` 验证页面可访问
> 2. 检查控制台错误（通过 headless 浏览器或 puppeteer）
> 3. 向用户说明无法自动验证的项，请用户手动确认

#### 回归排查

- **组件影响范围**：修改的共享组件被哪些页面使用？这些页面是否受影响？
- **样式全局影响**：修改的 CSS/样式是否会泄漏到其他页面？（全局样式、z-index、CSS 变量）
- **路由变更**：路由是否变化？书签/外链是否会 404？
- **状态管理**：store/context 变更是否影响不相关的组件？
- **浏览器兼容**：是否使用了新 CSS/JS API？目标浏览器是否支持？
- **无障碍**：修改是否破坏了键盘导航、ARIA 属性、焦点管理？

---

### 8.3 Server / API

#### 手动验证

agent 必须**实际发送 HTTP 请求**，验证 API 行为：

| 验证项 | 操作 | 预期 |
|--------|------|------|
| **正常路径** | 发送合法请求 | 200/201，响应体格式正确 |
| **认证** | 无 token / 过期 token / 无效 token 请求受保护接口 | 401 Unauthorized |
| **授权** | 有权限/无权限的用户分别请求 | 200 / 403 Forbidden |
| **参数校验** | 缺少必填字段 / 非法值 / 类型错误 | 400 Bad Request + 明确的错误信息 |
| **资源不存在** | 请求不存在的资源 ID | 404 Not Found |
| **错误不泄露** | 触发服务端错误 | 500 但不暴露堆栈/SQL/内部路径 |
| **响应格式** | 检查 Content-Type、JSON 结构 | 与 API 文档一致 |
| **数据库写入** | POST/PUT/DELETE 后查询确认 | 数据正确持久化 |
| **并发/幂等** | 重复请求 / 并发请求 | 无脏数据、幂等性正确 |

```bash
# 示例：Server 手动验证
curl -s http://localhost:3000/api/health          # 健康检查
curl -s http://localhost:3000/api/items            # 正常路径
curl -s http://localhost:3000/api/items/99999      # 404
curl -s -X POST http://localhost:3000/api/items \  # 创建
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'
curl -s http://localhost:3000/api/items            # 无 token
curl -s -H "Authorization: Bearer expired" \       # 过期 token
  http://localhost:3000/api/items
```

> 数据库变更的额外验证：
> - 迁移脚本在空库上可正常执行
> - 迁移脚本在已有数据上可正常执行（不丢数据）
> - 回滚脚本可正常执行（如有）

#### 回归排查

- **API 兼容性**：是否修改了已有接口的请求/响应结构？会破坏调用方吗？
> - 检查是否删除了响应字段、修改了字段类型、变更了 URL 路径或 HTTP 方法
> - 这些都是 breaking change，需与调用方协调
- **数据库**：Schema 变更是否需要迁移？是否兼容旧数据？索引是否需要更新？
- **中间件/拦截器**：修改的中间件是否影响所有经过的路由？
- **环境变量/配置**：新增的配置项在不同环境（dev/staging/prod）是否有默认值？
- **日志/监控**：日志格式是否变化？告警规则是否需要更新？
- **依赖服务**：下游服务（数据库、缓存、第三方 API）的连接配置是否正确？

## 9. 常见验收陷阱

### 9.1 "测试通过就行"

❌ **错误**：只跑了测试就宣告完成。

✅ **正确**：测试通过只是 Step 3 的一部分。还需手动验证（Step 4）、diff 自审、回归排查、文档检查。

### 9.2 "只改了一行不用验证"

❌ **错误**：跳过验证。

✅ **正确**：至少执行 §5 快速验收——确认构建通过、diff 干净、无副作用。一行代码也可能破坏构建或引入 bug。

### 9.3 "代码看着没问题"

❌ **错误**：只读代码不实际运行。

✅ **正确**：CLI 要实际执行命令；Web 要在浏览器打开页面；Server 要发 HTTP 请求。**没有跑过的功能不算验证过。**

### 9.4 "warning 不重要"

❌ **错误**：忽略 lint warning 或编译 warning。

✅ **正确**：warning 往往是 bug 的前兆。逐条评估，能修尽修；无法修复的，在报告中说明原因。

### 9.5 "文档稍后再补"

❌ **错误**：先宣告完成，文档"以后再说"。

✅ **正确**：文档是完成标准的一部分。没有文档的变更视为未完成（配合 `doc-first` 技能）。

### 9.6 "只测了我改的部分"

❌ **错误**：只运行与改动相关的测试。

✅ **正确**：运行**全量**测试套件。改动可能在预期之外影响其他模块。

### 9.7 "响应能拿到数据就行"

❌ **错误**：Server 只验证了 200 正常路径。

✅ **正确**：还需验证错误路径（400/401/403/404/500）、参数校验、认证授权。错误路径往往是最容易出 bug 的地方。

## 10. 验收检查清单

宣告完成前，逐项确认。**通用项 + 当前项目类型的专属项，都需要通过。**

### 通用（所有类型）

#### 代码质量
- [ ] 已审阅完整 diff，每处改动都能解释原因
- [ ] 无硬编码的密钥、密码、token
- [ ] 无遗留调试代码（`console.log` / `print` / `debugger`）
- [ ] 无注释掉的代码 / 死代码 / 未使用的 import
- [ ] 无临时文件残留
- [ ] 代码风格符合项目规范

#### 功能验证
- [ ] 原始需求逐条核对，全部达成
- [ ] 边界条件已处理（空数据、大数据、非法输入）
- [ ] 异常场景已处理（失败时有合理行为）

#### 自动化验证
- [ ] 全量测试通过
- [ ] 构建成功
- [ ] 类型检查通过（如适用）
- [ ] Lint / 代码检查通过（如适用）

#### 文档与配置
- [ ] 相关文档已同步更新
- [ ] `README.md` / `AGENTS.md` 已更新（如涉及）
- [ ] 变更日志已更新（如项目维护）

#### 验收报告
- [ ] 已在 `.reports/<task-name>/` 下生成 `report.html`
- [ ] 报告包含改动文件、验证结果、需求达成、遗留事项
- [ ] 验证结果逐项标注状态（✅ / ⚠️ / ⏳ / ❌）
- [ ] 报告在浏览器中可正常打开查看

### CLI 专属

- [ ] 实际运行命令，输出正确
- [ ] `--help` / `--version` 正常显示
- [ ] 无参数 / 非法参数时退出码正确（非 0）且错误提示友好
- [ ] stdout / stderr 正确分离
- [ ] 输出格式可通过管道被其他命令消费
- [ ] 已识别 CLI 所需的全部密钥/环境变量
- [ ] 密钥由用户自行配置（agent 不经手），已给出具体配置命令
- [ ] 不依赖密钥的验证项已全部验证
- [ ] 依赖密钥的验证项已验证（或已标注"待用户配置后验证"）
- [ ] 已有参数的兼容性无 breaking change（或已明确说明）

### Web 专属

- [ ] 页面在浏览器中正确渲染
- [ ] 核心交互流程（点击/输入/提交）正常
- [ ] 响应式布局在不同宽度下正常
- [ ] 浏览器控制台无 error / warning
- [ ] 加载中 / 空数据 / 错误状态正确展示
- [ ] 修改的共享组件未影响其他页面
- [ ] 无明显的性能问题（无白屏闪烁、无不必要的重渲染）

### Server 专属

- [ ] 正常请求返回正确数据
- [ ] 认证失败 → 401，授权失败 → 403
- [ ] 参数校验失败 → 400 + 明确错误信息
- [ ] 资源不存在 → 404
- [ ] 服务端错误 → 500 但不泄露堆栈/SQL/内部路径
- [ ] 数据库写入正确持久化
- [ ] 响应格式与 API 文档一致
- [ ] API 变更不破坏向后兼容（或已标记为 breaking change）
- [ ] 数据库迁移脚本可正常执行（如涉及）
- [ ] 无 N+1 查询等明显性能问题

## 11. 与其他 skill 配合

```
需求输入
  │
  ▼
[spec-first] 澄清需求、确认方案 → .specs/<name>/spec.md
  │
  ▼  ← 用户确认
  │
[doc-first] 先更新文档 → docs/
  │
  ▼
编码实现
  │
  ▼
[done-check] 验收检查（本文档）→ 对照 spec.md 逐条核对
  │
  ▼
  生成验收报告 → .reports/<task-name>/report.html
  │
  ▼
✅ 宣告完成，提交变更
```

### 与 spec-first 的衔接

- 验收时回到 `.specs/<name>/spec.md`，逐条核对"方案概要""关键决策""影响范围"是否都已落实
- spec.md 中的"待确认"项是否已全部解决

### 与 doc-first 的衔接

- §6.8 的文档同步检查与 `doc-first` 的检查清单一致
- 如果 doc-first 要求的文档未更新，done-check 视为**不通过**

## 12. 完成的定义（Definition of Done）

> **一句话**：当且仅当以下条件**全部**满足时，任务才算完成——
>
> 1. 所有需求项已实现并通过验证
> 2. 全量测试通过、构建成功
> 3. **按项目类型完成了手动验证**（CLI 实际运行 / Web 浏览器验证 / Server 接口请求）
> 4. diff 已自审，无遗留问题
> 5. 无回归风险
> 6. 代码干净，无调试残留
> 7. 文档已同步
> 8. 已在 `.reports/<task-name>/report.html` 生成验收报告
> 9. 已向用户简要汇报并附上报告路径
