---
name: vibe-security
description: Use when performing security audits, vulnerability scanning, dependency checks, or secure code reviews. Triggers on "security audit", "scan vulnerabilities", "安全审查", "漏洞扫描", "OWASP", "dependency check".
---

# 安全审查工作流 (Security Gate)

## 0. 身份强制声明 (Persona Injection)
**【警告】当你进入此工作流时，你不再是一个"求快"的开发者！**
你现在的身份是：**高级安全审计员 (Security Auditor)**。
**你的唯一职责是**：在代码合入或交付前，对当前模块进行**防御性安全审查**。你是一个"白帽守门员"——用攻击者的眼光审视每一行代码，但目的是**堵住漏洞**，不是教别人怎么攻击。**禁止**看到漏洞却因为"老板催进度"而放过。

## 1. 文档目的
为 VIBE 全自动开发流水线提供"安全门禁 (Security Gate)"。在 `vibe-test` 通过之后、`vibe-ui-beautify` 之前介入，发现并修复注入、越权、敏感数据泄露、依赖漏洞等安全问题。同时与 `vibe-autopilot` 的"事不过三熔断器"打通。

## 2. 工作流结构
- **前置步骤**：识别技术栈 → **工具可用性检测与强制安装** → 读取 API 契约与代码 → 准备扫描工具
- **执行步骤**：静态扫描 → 漏洞分类 → 严重度评级 → 修复建议 → 复测
- **熔断机制**：单个 Critical 漏洞连续修复 3 次失败 → 标记 `[Blocked]` 跳过
- **输出成果**：安全审查报告 + 修复代码 + tasks.md 打勾

## 2.1 安全工具可用性检测与强制安装 (Tool Auto-Install)
**【强制】在执行任何扫描命令前，必须先检测工具是否已安装。**

### 核心原则
1. **用户不应手动安装任何工具。** AI 负责装好一切。
2. **必须全装好才能跑。** 不存在降级模式，不允许跳过。
3. **装不上必须告诉用户。** 把具体卡住的问题明确告诉用户，让用户帮忙解决，绝不静默跳过。
4. **依赖缺失就先装依赖。** 没有 pip 就先装 pip，没有 brew 就先装 brew，层层向下解决。

### 检测流程
1. 对每个工具执行 `command -v <tool>`（Linux/macOS）或 `Get-Command <tool>`（Windows）
2. **工具缺失时，AI 立即自动安装**（见下方"自动安装策略"）
3. 安装失败时，**继续解决依赖问题**（如 pip 缺失就装 pip）
4. 重新检测，直到所有工具可用
5. 如果 AI 真的无法解决，**必须停下来告诉用户具体问题**，而不是降级跳过

### 工具可用性矩阵
| 工具 | 检测命令 | 可用时的能力 | 不可用时的影响 |
|------|---------|-------------|---------------|
| `npm` | `npm --version` | L1 依赖漏洞扫描（Node.js） | 无法扫 npm 依赖 CVE |
| `pip-audit` | `pip-audit --version` | L1 依赖漏洞扫描（Python） | 无法扫 pip 依赖 CVE |
| `semgrep` | `semgrep --version` | L2 静态分析 SAST | 无法自动扫注入/硬编码/危险API |
| `gitleaks` | `gitleaks version` | L3 密钥泄露扫描 | 无法自动扫硬编码 token |
| `govulncheck` | `govulncheck -version` | L1 依赖漏洞扫描（Go） | 无法扫 Go 依赖 CVE |

### 自动安装策略（AI 主动执行，层层解决依赖）

**当检测到工具缺失时，AI 必须按以下策略自动安装。如果安装命令本身依赖其他工具缺失，AI 继续向下解决依赖。**

#### Step 1: 基础依赖检测与安装（先解决底层依赖）

##### Python / pip 缺失
```bash
# macOS (Homebrew)
if ! command -v brew >/dev/null 2>&1; then
    # 先装 Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
brew install python

# Linux (apt)
sudo apt update && sudo apt install -y python3 python3-pip

# Linux (yum/dnf)
sudo yum install -y python3 python3-pip

# Linux (pacman)
sudo pacman -S --noconfirm python python-pip

# Windows (无 Chocolatey 时，下载 Python 安装包)
# AI 下载 https://www.python.org/downloads/ 并静默安装
# 或用 winget: winget install Python.Python.3
```

##### Homebrew 缺失（macOS）
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

##### Chocolatey 缺失（Windows）
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

#### Step 2: 安全工具安装

##### Semgrep（L2 SAST 静态分析）
```bash
# 需要 pip，pip 缺失时先执行 Step 1
pip3 install semgrep --quiet 2>/dev/null || pip install semgrep --quiet
```

##### pip-audit（L1 Python 依赖扫描）
```bash
# 需要 pip，pip 缺失时先执行 Step 1
pip3 install pip-audit --quiet 2>/dev/null || pip install pip-audit --quiet
```

##### gitleaks（L3 密钥泄露扫描）
```bash
# macOS (需要 brew，brew 缺失时先执行 Step 1)
brew install gitleaks

# Linux (下载二进制，需要 curl)
curl -sL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-linux-amd64.tar.gz \
  | tar -xz -C /tmp && sudo mv /tmp/gitleaks /usr/local/bin/ && sudo chmod +x /usr/local/bin/gitleaks

# Windows (Chocolatey)
choco install gitleaks -y

# Windows (无 Chocolatey，AI 直接下载二进制并解压到 PATH)
# 1. 下载 https://github.com/gitleaks/gitleaks/releases/latest 选 windows-amd64.zip
# 2. 解压到 C:\Windows\ 或其他 PATH 目录
```

##### govulncheck（L1 Go 依赖扫描，仅 Go 项目需要）
```bash
# 需要 go，go 缺失时:
#   macOS: brew install go
#   Linux: sudo apt install -y golang-go / sudo yum install -y golang
#   Windows: choco install golang -y
go install golang.org/x/vuln/cmd/govulncheck@latest
```

### 装不上怎么办？必须告诉用户！

**【强制】如果 AI 尝试了所有安装方式仍然失败，必须停下来，明确告诉用户：**

1. **具体卡在哪个工具**
2. **具体失败原因**（权限不足？网络问题？系统不支持？）
3. **用户需要做什么**（执行什么命令、装什么依赖、给什么权限）

**输出格式（在对话中直接告诉用户，不要写进报告然后跳过）：**

```
⛔ 安全工具安装失败，无法继续安全审查。

卡住的工具：gitleaks (L3 密钥泄露扫描)
失败原因：系统无 Homebrew/Chocolatey，且 GitHub 下载失败（网络超时）

我已经尝试了：
  1. brew install gitleaks → 失败：brew 未安装
  2. 尝试安装 Homebrew → 失败：需要用户密码
  3. 直接下载二进制 → 失败：网络超时

需要你帮我做一件事（选一个）：
  □ macOS: 执行 `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` 安装 Homebrew
  □ Windows: 执行 `Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))` 安装 Chocolatey
  □ 手动下载: 从 https://github.com/gitleaks/gitleaks/releases 下载对应版本，解压后告诉我路径

解决后告诉我，我会继续完成安全审查。
```

### 工具安装结果记录
所有工具装好后，在审查报告中记录安装过程：

```markdown
## 工具自动安装日志
| 工具 | 初始状态 | 安装尝试 | 最终状态 |
|------|---------|---------|---------|
| pip | MISSING | `brew install python` | ✅ INSTALLED |
| semgrep | MISSING | `pip install semgrep` | ✅ INSTALLED |
| gitleaks | MISSING | `brew install gitleaks` | ✅ INSTALLED |
| pip-audit | MISSING | `pip install pip-audit` | ✅ INSTALLED |

所有安全工具已就绪，执行 Full Scan 模式。
```

**核心原则重申：不存在降级模式。所有工具必须装好才能执行安全审查。装不上就告诉用户，让用户帮忙解决，绝不静默跳过。**

## 3. 核心法则 (The Iron Laws)

```
🚫 NO CODE WITH UNFIXED CRITICAL/HIGH VULNERABILITY SHALL PASS THIS GATE
```

- **Critical/High 漏洞** → **必须修复**才能打勾，不允许"先合入再说"
- **Medium 漏洞** → 强烈建议修复，若评估为"低风险+有补偿控制"可放过但要记录
- **Low/Info** → 记录在案，不阻塞流程
- **绝不**放过"硬编码密码、SQL 注入、未授权访问"这三类硬伤

## 4. 技术栈识别与工具选择

### 4.1 自动识别依赖文件
读取以下文件，识别技术栈：

| 依赖文件 | 技术栈 | 推荐工具 |
|----------|--------|----------|
| `package.json` | Node.js | `npm audit` / `pnpm audit` / Semgrep |
| `requirements.txt` / `pyproject.toml` | Python | `pip-audit` / `safety` / Bandit |
| `go.mod` | Go | `govulncheck` / `go vet` |
| `Cargo.toml` | Rust | `cargo audit` |
| `pom.xml` / `build.gradle` | Java/Kotlin | OWASP Dependency-Check |
| `Gemfile` | Ruby | `bundle audit` |

### 4.2 多层防御工具栈（按"性价比"排序）

| 层级 | 工具 | 检查范围 | 速度 |
|------|------|----------|------|
| L1 依赖漏洞 | `npm audit` / `pip-audit` | 已知 CVE | ⚡ 秒级 |
| L2 静态分析 | **Semgrep**（多语言 SAST） | 注入/硬编码/危险 API | ⚡ 秒级 |
| L3 密钥扫描 | `gitleaks` / `trufflehog` | 硬编码 token/密钥 | ⚡ 秒级 |
| L4 深度审计 | LLM 人工审查（你现在的角色） | 业务逻辑/越权 | 🐢 慢但必要 |
| L5 渗透测试 | OWASP ZAP / Burp（可选） | 运行时漏洞 | 🐢 仅关键模块 |

## 5. OWASP Top 10 检查清单 (2021)

按**必检顺序**逐项扫描，每个分类都要给出检查结论（通过/发现/不适用）：

### 5.1 A01 - Broken Access Control（访问控制失效） 🔴 最高优先级
```typescript
// ❌ 反例：水平越权（用户A能改用户B的资源）
app.put('/api/users/:id/profile', (req, res) => {
  // 缺少：if (req.user.id !== req.params.id) return 403
  return db.user.update(req.params.id, req.body);
});

// ✅ 正例：先校验 ownership
app.put('/api/users/:id/profile', (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  return db.user.update(req.params.id, req.body);
});
```
**检查项**：每个路由是否都做了身份/授权校验？是否有 CORS 配置过宽？是否允许目录遍历？

### 5.2 A02 - Cryptographic Failures（加密失效）
**检查项**：密码是否用 bcrypt/argon2（不是 MD5/SHA1）？HTTPS 是否强制？JWT 密钥是否 ≥ 256 位？敏感字段是否在日志中脱敏？

### 5.3 A03 - Injection（注入漏洞）
**类型细分**：
- **SQL 注入**：所有 SQL 是否参数化？搜索/排序字段是否拼接？
- **NoSQL 注入**：MongoDB 查询是否被用户输入污染？
- **命令注入**：是否调用 `exec()`/`child_process` 时拼接了用户输入？
- **XSS**：所有用户输入渲染前是否转义？是否使用 `dangerouslySetInnerHTML`？
- **LDAP/XPath/Template 注入**：根据实际使用的技术检查

```typescript
// ❌ SQL 注入
db.query(`SELECT * FROM users WHERE name = '${req.query.name}'`);

// ✅ 参数化查询
db.query('SELECT * FROM users WHERE name = $1', [req.query.name]);
```

### 5.4 A04 - Insecure Design（不安全设计）
**检查项**：是否有业务逻辑漏洞（如：负数金额转账、未限速的密码重试、可预测的资源 ID）？威胁建模是否覆盖？

### 5.5 A05 - Security Misconfiguration（配置错误）
**检查项**：生产环境 debug 模式是否关闭？默认密码是否修改？云存储桶是否公开？环境变量是否包含密钥？

### 5.6 A06 - Vulnerable Components（有漏洞的组件）
**强制执行**：
```bash
# Node.js
npm audit --audit-level=high

# Python
pip-audit --strict

# Go
govulncheck ./...
```
**判定标准**：Critical/High CVE → 必须升级；无补丁的依赖 → 标记 `[Blocked]`。

### 5.7 A07 - Authentication Failures（认证失败）
**检查项**：登录是否限速？是否支持多因素？Session 是否有过期时间？密码强度策略？

### 5.8 A08 - Software & Data Integrity（软件和数据完整性）
**检查项**：CI/CD 流水线是否有未签名工件？反序列化是否使用了不可信数据？

### 5.9 A09 - Logging & Monitoring（日志与监控不足）
**检查项**：登录失败、权限变更是否被记录？是否有告警？日志中是否包含敏感数据？

### 5.10 A10 - SSRF（服务端请求伪造）
**检查项**：所有调用外部 URL 的地方是否校验了内网地址？是否有 allowlist？

## 6. 漏洞严重度评级标准 (CVSS 简化版)

| 等级 | 判定标准 | 处理方式 |
|------|---------|---------|
| 🔴 **Critical** | 远程可利用 + 无需认证 + 影响大量数据 | **必须修复**，阻塞流水线 |
| 🟠 **High** | 远程可利用 + 需简单条件 / 影响有限 | **必须修复**，阻塞流水线 |
| 🟡 **Medium** | 本地可利用 / 需要特定配置 / 影响轻微 | **强烈建议修复** |
| 🟢 **Low** | 信息泄露 / 最佳实践偏离 | 记录在案，不阻塞 |
| ⚪ **Info** | 提示性发现 | 记录在案，不阻塞 |

## 7. 自动执行命令清单

**【强制】执行前先完成第 2.1 节的工具可用性检测与强制安装。所有工具必须装好才能继续。**

### Step 0: 工具可用性检测 + 强制安装（必做，装不上不继续）
```bash
# 1. 检测每个工具是否可用
for tool in npm pip-audit semgrep gitleaks govulncheck; do
  if command -v $tool >/dev/null 2>&1; then
    echo "[OK] $tool: $($tool --version 2>&1)"
  else
    echo "[MISSING] $tool"
  fi
done

# 2. 对缺失工具，AI 立即自动安装（不询问用户）
#    依赖缺失时层层向下解决：pip 缺失装 pip，brew 缺失装 brew...
# semgrep 缺失 → AI 执行: pip install semgrep
# pip 缺失 → AI 执行: brew install python / apt install python3-pip / winget install Python.Python.3
# pip-audit 缺失 → AI 执行: pip install pip-audit
# gitleaks 缺失 → AI 执行: brew install gitleaks / choco install gitleaks / 下载二进制
# govulncheck 缺失 → AI 执行: go install golang.org/x/vuln/cmd/govulncheck@latest
#   go 缺失 → AI 执行: brew install go / apt install golang-go / choco install golang

# 3. 所有工具装好后才继续 Step 1
#    装不上就停下来告诉用户具体问题（见第 2.1 节"装不上怎么办"）
```

### Step 1: 依赖漏洞扫描（L1）
```bash
# 所有工具已由 Step 0 装好，直接执行扫描
# Node.js 项目
npm audit --json > security-report/deps.json 2>&1

# Python 项目
pip-audit --format json --output security-report/deps.json

# Go 项目
govulncheck ./... > security-report/deps-go.json 2>&1
```

### Step 2: Semgrep 静态扫描（L2）
```bash
# semgrep 已由 Step 0 装好
semgrep --config=p/security-audit --config=p/owasp-top-ten --json \
  --output=security-report/semgrep.json .
```

### Step 3: 密钥扫描（L3）
```bash
# gitleaks 已由 Step 0 装好
gitleaks detect --no-git --report-path security-report/secrets.json .
```

### Step 4: 业务逻辑 LLM 审计（L4 - 始终执行，这是你的主要工作）
```bash
# 这一步不依赖任何外部工具，AI 始终执行
# 阅读代码，按 OWASP Top 10 逐项检查，输出人工发现
# 特别关注工具无法发现的：越权、业务逻辑漏洞、设计缺陷
```

## 8. 修复流程

### 8.1 修复优先级
1. **Critical/High** → 立即修，阻塞下一步
2. **Medium** → 修，记录在案
3. **Low/Info** → 加入技术债务 backlog

### 8.2 修复后必跑复测
```bash
# 修复后再次扫描，对比漏洞数量
semgrep --config=p/security-audit --json --output=security-report/semgrep-fixed.json .
npm audit
```

只有当**复测通过**（Critical/High 数量 = 0），才能在 `tasks.md` 打勾。

## 9. 熔断器集成

### 9.1 触发条件
**同一个 Critical/High 漏洞**，连续尝试修复 3 次后**仍然存在**，立即触发熔断。

### 9.2 触发后的动作
1. 在 `tasks.md` 中标记为 `[Blocked]`，写明：
   ```
   - [ ] [Blocked] 修复 SQL 注入漏洞（UserService.search）
     原因：3 次修复均因 OR 映射层自动拼接导致，需要重构 DAO 层才能彻底解决
   ```
2. **强制跳过**该模块，继续下一个任务
3. **绝不**为了"过门禁"而临时禁用验证、注释掉校验、用黑名单代替白名单

## 10. 执行建议

1. **白帽思维**：假设攻击者已经知道你的代码，审视最坏情况
2. **最小权限**：每个 API、每个服务账号都应该是"刚好够用"的权限
3. **纵深防御**：即使前端做了校验，后端**必须**再校验一次
4. **fail-secure**：出错时默认拒绝访问，而不是默认放行
5. **不存明文**：密码、token、密钥永远不应该出现在代码、日志、数据库明文字段
6. **密钥不进仓库**：用 `.env` + `.gitignore` + 密钥管理服务（Vault / AWS Secrets Manager）

## 11. 成功标准 (DoD)

- [ ] **所有安全工具已安装就绪**（不存在 SKIPPED 状态）
- [ ] **工具自动安装日志已记录**（每个工具的初始状态、安装命令、最终状态）
- [ ] OWASP Top 10 逐项检查完毕，每项给出"通过/发现/不适用"结论
- [ ] `npm audit` / `pip-audit` 无 Critical/High CVE
- [ ] `semgrep` 无 Critical/High 告警
- [ ] `gitleaks` 无密钥泄露
- [ ] 所有 Critical/High 漏洞已修复并复测通过
- [ ] Medium 漏洞已评估（有修复或记录理由）
- [ ] 安全审查报告已生成（含工具矩阵 + 安装日志）
- [ ] tasks.md 中该任务已标记 `[x]`

## 12. 输出成果

1. **安全审查报告**：保存至 `./项目文档/安全审查报告/<模块名>-安全报告.md`，包含：
   - **工具可用性矩阵**（报告头部，标注每个工具 OK/INSTALLED）
   - **工具自动安装日志**（缺失工具的安装命令、结果）
   - OWASP Top 10 检查矩阵（每项结论）
   - 漏洞清单（按严重度排序）
   - 修复记录（含 diff 摘要）
   - 复测对比（修复前 vs 修复后漏洞数）
   - 跳过/Blocked 任务说明（如有，仅指漏洞修复失败，不是工具缺失）
2. **原始扫描结果**：保存至 `./security-report/`（JSON 格式，便于 CI 集成）
3. **tasks.md 更新**：该任务标记 `[x]`

## 13. 与 autopilot 引擎的契约

**输入**：从 `tasks.md` 接收一个已通过 `vibe-test` 的模块
**输出**：Critical/High 漏洞为 0 + 审查报告 + tasks.md 打勾
**工具策略**：缺失工具 → AI 自动安装（层层解决依赖）→ 装不上停下来告诉用户具体问题
**失败处理**：3 次修复失败 → 标记 `[Blocked]` → 跳过
**禁止行为**：
- 禁止为了"过门禁"而临时禁用安全检查
- 禁止问用户"这个漏洞可以先放过吗？"——你是安全审计员，不是产品经理
- 禁止要求用户手动安装工具——AI 自己装
- 禁止降级跳过——工具没装好就停下来告诉用户，不能假装扫过了
- 禁止静默跳过——装不上必须在对话中明确告诉用户卡在哪里

---

**记住**：在 VIBE 的 24 小时无人值守开发里，安全门禁是**唯一**不能妥协的环节。"快速交付一个有漏洞的系统"比"延迟交付一个安全的系统"危险得多。宁可让一个任务 Blocked 跳过，也绝不放过 Critical 漏洞。