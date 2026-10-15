---
name: open-source-prep
description: 帮用户把私有项目整理成可开源的仓库。核心能力：(1) 扫描源码和 git 历史中的密钥/token 泄漏；(2) 根据项目场景推荐开源协议（MIT / Apache 2.0 / GPL 等）并生成 LICENSE；(3) 补齐 README 免责声明、CONTRIBUTING.md、SECURITY.md、.gitignore 等开源必备文档；(4) 检查 bundle identifier、package.json 等所有权/商标隐患。触发词：「开源」「open source」「选择协议」「LICENSE」「准备开源」「检测密钥」「secret scan」「上传 github」。
user-invocable: true
---

# Open Source Prep

把私有项目整理成可安全开源的仓库。分 5 个阶段串行执行，**密钥扫描必须最先通过**才能进入后续步骤。

## 使用场景

用户说：
- "帮我把这个项目开源"
- "准备开源前要做什么"
- "选一个开源协议"
- "上传 GitHub 前检查一下有没有泄漏"

## 重要原则

1. **密钥扫描是 gating step** — 发现真实密钥时必须停下来让用户先清理，不能直接继续
2. **生成的文档用英文** — 面向国际贡献者；和用户对话用中文
3. **LICENSE 文件必须命名为 `LICENSE`**（大写无后缀），GitHub 才识别
4. **所有真实 token 示例必须用 `...REDACTED...` 占位符** — 即使是用户主动粘贴进来的
5. **不要直接 push 或切 public** — 先让用户检查 diff，手动 commit+push+切可见性

## 工作流

### Phase 1: 密钥 & 敏感文件扫描（BLOCKING）

**必须先做，发现问题要停下**。扫描三个地方：

1. **当前工作区文件**（包括未追踪的）
2. **已 staged / 已 committed 的内容**
3. **git 全部历史**（`git log --all -p`）

扫描模式见 `references/secrets-patterns.md`。关键模式包括：

| 类型 | 模式 |
|------|------|
| JWT | `eyJhbGc[0-9A-Za-z_-]{20,}` |
| GitHub token | `gh[posur]_[0-9A-Za-z]{36,}` |
| OpenAI / Anthropic | `sk-[a-zA-Z0-9]{20,}`, `sk-ant-[a-zA-Z0-9-]{40,}` |
| AWS access key | `AKIA[0-9A-Z]{16}` |
| Google API key | `AIza[0-9A-Za-z_-]{35}` |
| Slack token | `xox[baprs]-[0-9A-Za-z-]{10,}` |
| Stripe | `sk_live_[0-9A-Za-z]{20,}` |
| 私钥 PEM | `-----BEGIN.*PRIVATE KEY-----` |
| 通用密码 | `password\s*[:=]\s*["'][^"']{8,}` |

敏感文件名（staged 时警报）：
- `.env`, `.env.local`, `.env.production`
- `credentials.json`, `secrets.json`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa`, `id_ed25519`

**执行命令**（按项目大小自适应）：
```bash
# 工作区扫描（含未追踪）
git ls-files --others --exclude-standard -z | xargs -0 grep -lE "<pattern>" 2>/dev/null

# 已追踪文件
git grep -nE "<pattern>" 2>/dev/null

# Git 历史
git log --all -p 2>/dev/null | grep -cE "<pattern>"

# 敏感文件名
git ls-files | grep -E "(^|/)(\.env|credentials\.json|.*\.(pem|key|p12|pfx))$"
```

**区分真密钥 vs 占位符**：
- ✅ 占位符：包含 `...` / `REDACTED` / `example` / `test` / `xxx` / `dummy`
- ❌ 真密钥：没有明显占位符标记，且符合真实格式（如 JWT 是三段点分 base64url、AWS 是 20 字符全大写 + 数字等）

**发现真密钥时**：
1. 列出文件 + 行号 + 截断显示（`eyJhbGc...[12 chars]...abcd` 前后各 4 位，中间省略）
2. 提供处理建议：
   - 如果在工作区 → 移到 `.env` 并加入 `.gitignore`
   - 如果已 commit 未 push → `git filter-repo` 或 `git reset --soft HEAD~1`
   - 如果已 push → **必须立即撤销这个 token**（本工具无法从 GitHub 删除已泄漏的 commit），然后 `git filter-repo --invert-paths` + force push
3. **停止后续步骤**，让用户处理后再重跑

### Phase 2: 协议选择（交互式）

根据决策树推荐，不要一上来就问所有问题：

**第一问**：项目性质？
- 个人工具 / 小库 / 应用 → 继续问第二
- 商业产品对外开源 / 希望企业安心使用 → **Apache 2.0**
- 想让所有衍生作品也开源 → 继续问第三

**第二问**（针对个人项目）：涉及可申请专利的新颖技术？
- 否 → **MIT** ⭐
- 是 → **Apache 2.0**

**第三问**（针对 copyleft 偏好）：SaaS 形态（用户通过网络用不下载）？
- 是 → **AGPL v3**
- 否 → **GPL v3**

**默认推荐 MIT** — 95% 个人项目合适。生成的 `LICENSE` 使用 `templates/LICENSE-MIT.txt` 模板，版权人从 `git config user.name` 读取，年份是当前年份。

协议对比速查：

| 协议 | 长度 | 专利 | 商标 | copyleft | 场景 |
|------|------|------|------|----------|------|
| **MIT** | 20 行 | 无 | 无 | 无 | 个人工具首选 |
| **Apache 2.0** | 200 行 | 显式 | 保护 | 无 | 企业/专利场景 |
| **GPL v3** | 长 | 有 | - | 强 | 病毒式开源 |
| **AGPL v3** | 长 | 有 | - | 极强 | SaaS 场景 |

### Phase 3: 必备文档生成

生成以下文件（如已存在则显示 diff，用户确认后再改）：

1. **`LICENSE`** — 协议文本，填入版权人 + 年份
2. **`CONTRIBUTING.md`** — 开发环境、PR 流程、测试命令（用 `templates/CONTRIBUTING.md`）
3. **`SECURITY.md`** — 漏洞上报流程（用 `templates/SECURITY.md`）
4. **`README.md` 补充**（用 Edit tool 插入）：
   - 顶部：第三方免责声明（如果项目涉及第三方服务）
   - Privacy & Security 章节（如果处理敏感数据）
   - License 章节指向 `LICENSE` 文件

### Phase 4: 配置审计

检查并提示修改：

1. **`.gitignore`** — 确保包含：
   ```
   src-tauri/target/   # Tauri
   target/             # Rust 通用
   node_modules/       # Node
   dist/ build/ out/   # 构建产物
   .env*               # 环境变量
   .DS_Store Thumbs.db # OS
   coverage/ *.lcov    # 覆盖率报告
   ```

2. **Bundle identifier / package name 检查**：
   - `src-tauri/tauri.conf.json` 的 `identifier` 字段
   - `package.json` 的 `name` 字段
   - `Cargo.toml` 的 `[package] name`
   - 如果包含第三方公司名（如 `com.google.*`、`com.factory.*`）→ 警告商标风险
   - 建议改为 `com.<github-username>.<project-name>`

3. **第三方服务引用**：
   - grep 项目名里有没有商标（"Google X", "Apple X" 等）
   - README 是否说明这是 **unofficial third-party tool**

### Phase 5: 可选增强

询问用户是否要做：

- [ ] CHANGELOG.md（从 git log 生成初始版本）
- [ ] GitHub Actions release workflow（`.github/workflows/release.yml`）
- [ ] Issue/PR 模板（`.github/ISSUE_TEMPLATE/`）
- [ ] 仓库可见性切换（`gh repo edit --visibility public`）

**注意**：切换为 public 是**不可逆的信息公开**，必须用户明确确认后才执行，且要再跑一次 Phase 1 密钥扫描。

## 输出格式

每个阶段结束后向用户报告：

```markdown
## Phase N: xxx

✅ 通过：[...]
⚠️ 警告：[...]
❌ 需处理：[...]

下一步：[...]
```

最后给一个完整 checklist。

## 工具文件

- `templates/LICENSE-MIT.txt` — MIT 协议模板（用 `{{YEAR}}` `{{AUTHOR}}` 占位）
- `templates/LICENSE-Apache-2.0.txt` — Apache 2.0 模板
- `templates/LICENSE-GPL-3.0.txt` — GPL v3 模板（较长，可用 `gh api` 拉官方文本）
- `templates/LICENSE-AGPL-3.0.txt` — AGPL v3 模板
- `templates/CONTRIBUTING.md` — 贡献指南模板
- `templates/SECURITY.md` — 安全策略模板
- `references/secrets-patterns.md` — 完整的密钥正则表达式清单
- `references/disclaimer-templates.md` — 不同场景的免责声明范文
