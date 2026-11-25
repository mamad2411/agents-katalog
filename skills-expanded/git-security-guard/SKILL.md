---
description: Git 安全守卫。防止 API Key、Token、私钥、钱包地址、.env 文件等敏感信息被提交到 Git。在 git commit、git push、创建新 repo、PR review 时自动触发。当用户说"commit"、"push"、"安全检查"、"security check"、"有没有泄露"、"检查key"时触发。
---

# Git Security Guard — 敏感信息泄露防护

## 触发时机
- **每次 git commit 前**（自动）
- **每次 git push 前**（自动）
- **新项目/新 repo 初始化时**
- **用户要求安全检查时**

## Pre-Commit 检查清单

### Step 1: 检查暂存文件名
```bash
git diff --cached --name-only | grep -iE '\.env|\.pem|\.p12|\.jks|\.key$|\.muse/|\.agent/|\.gemini/|memory/|convo/'
```
**任何匹配 → 立即阻止 commit，报告给用户。**

### Step 2: 检查暂存内容中的 Key 模式
```bash
git diff --cached | grep -iE 'sk-[a-zA-Z0-9]{20}|AIzaSy[a-zA-Z0-9_-]{33}|gsk_[a-zA-Z0-9]{20}|sk_live_|sk_test_[a-zA-Z0-9]{20}|pk_live_|pk_test_[a-zA-Z0-9]{20}|eyJhbGci[a-zA-Z0-9_-]{50}|-----BEGIN.*(PRIVATE|RSA)|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}|whsec_|xoxb-|xoxp-|service_role'
```
**任何匹配 → 立即阻止 commit，报告给用户。**

### Step 3: 排除误报
以下不算泄露：
- `.env.example` 中的占位符（`your-api-key`、`sk_test_your-...`）
- `process.env.XXX` 引用（代码读环境变量，不是硬编码）
- `node_modules/` 中的加密库代码
- 公开合约地址（USDC/USDT 等已知合约）
- 文档中的"不要这样做"示例

## 禁止提交的文件模式

| 文件模式 | 原因 |
|----------|------|
| `.env.local` / `.env.prod*` / `.env.vercel*` | 含真实 API Key |
| `.muse/` 目录 | 含内部战略/开发状态 |
| `.agent/` 目录 | 含内部 Skill/Prompt |
| `.gemini/` 目录 | 含 AI 对话记录 |
| `memory/` / `convo/` | 对话/记忆文件 |
| `*.pem` / `*.p12` / `*.jks` / `*.key` | 私钥/证书 |

## 禁止出现在代码中的 Key 模式

| 模式 | 服务 |
|------|------|
| `sk-[a-zA-Z0-9]{20,}` | OpenAI |
| `AIzaSy[a-zA-Z0-9_-]{33}` | Google/Gemini |
| `gsk_[a-zA-Z0-9]{20,}` | Groq |
| `sk_live_` / `sk_test_[实际值]` | Stripe Secret |
| `pk_live_` / `pk_test_[实际值]` | Stripe Publishable |
| `eyJhbGci[长JWT]` | JWT Token (Supabase/Vercel) |
| `AKIA[0-9A-Z]{16}` | AWS |
| `ghp_[a-zA-Z0-9]{36}` | GitHub PAT |
| `-----BEGIN (RSA )?PRIVATE KEY` | 私钥 |
| `0x[a-fA-F0-9]{64}` | 钱包私钥（注意：40位是地址，64位才是私钥） |
| `whsec_` | Stripe Webhook Secret |
| `xoxb-` / `xoxp-` | Slack Token |

## 新项目 .gitignore 模板

新 repo 第一个 commit 前必须包含：
```gitignore
# Env files (NEVER commit real keys)
.env
.env.local
.env.*.local
.env.prod*
.env.vercel*

# Internal files
.muse/
.agent/
.gemini/
memory/
convo/

# Private keys
*.pem
*.p12
*.jks
*.key

# IDE
.idea/
.vscode/

# OS
.DS_Store
```

## 泄露应急处理

如果发现敏感信息已经被 commit（即使还没 push）：

### 1. 从全部历史中清除
```bash
git stash --include-untracked
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch [泄露的文件]' --prune-empty HEAD
```

### 2. 清除本地残留
```bash
git for-each-ref --format='%(refname)' refs/original/ | xargs -n1 git update-ref -d
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 3. Force push（如果已推远程）
```bash
git push origin main --force
```

### 4. 轮换所有泄露的 Key
- 去对应平台重新生成 Key
- 更新 Vercel/服务器环境变量
- 更新本地 .env.local

## Deep Scan（完整历史扫描）

用于定期安全审计或怀疑有泄露时：
```bash
git log --all -p | grep -inE 'sk-[a-zA-Z0-9]{20}|AIzaSy|gsk_|sk_live|sk_test_[a-zA-Z0-9]{20}|pk_test_[a-zA-Z0-9]{20}|eyJhbGci[a-zA-Z0-9_-]{50}|-----BEGIN.*PRIVATE|AKIA[0-9A-Z]{16}|0x[a-fA-F0-9]{64}' | grep -v node_modules | head -30
```
