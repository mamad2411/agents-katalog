---
name: whitelabel-claude
description: 一键为 Claude Code 接入任意兼容 Anthropic Messages API 的大模型服务（DeepSeek、Kimi、OpenRouter、自建中转等），同时支持换皮为自定义品牌。自动探测已安装的 Claude Code 或从用户提供的 zip 包提取 cli.js，patch 后生成启动脚本和可分发包。当用户说"白标"、"换皮"、"接 DeepSeek/Kimi/OpenRouter"、"rebrand"、"/whitelabel"、"打包分发" 时触发。
---

# Claude Code 一键白标 & 多 API 接入

## 触发场景

- "白标 claude code"、"换皮"、"rebrand"、"/whitelabel"
- "帮我接 DeepSeek / Kimi / OpenRouter / 硅基流动"
- "打包一个可以分发的版本"

---

## 执行流程

### Step 0：收集配置

| 参数 | 说明 | 默认 |
|------|------|------|
| 品牌名 | 替换 UI 中的 "Claude Code"，不改就留空 | 可选 |
| API 端点 | 目标服务 base URL | 必填（接第三方时）|
| API Key | 第三方 API 的 key | 必填（接第三方时）|
| 中文 UI | 欢迎页汉化 | N |
| 品牌色 | 欢迎框边框 + 图标颜色，填 R,G,B 三个数字 | `215,119,87`（官方橙褐色）|
| 自定义 Logo | 替换欢迎页那个小机器人 | 可选 |
| 是否打包 | 打成 zip 分发 | 看用户需求 |

**常用 API 端点**：

| 服务 | base URL |
|------|----------|
| DeepSeek | `https://api.deepseek.com` |
| Kimi Code | `https://api.kimi.com/coding/` |
| OpenRouter | `https://openrouter.ai/api/v1` |
| 硅基流动 | `https://api.siliconflow.cn/v1` |
| 自建中转 | `https://your-domain.com` |
| 官方（默认） | 留空 |

---

### Step 1：找到 cli.js

cli.js 是 Claude Code 的核心文件，所有 patch 都在这一个文件上做。按以下优先级查找，命中第一个就停：

**情况 A：用户已安装 Claude Code（最常见）**

大部分人通过 npm、winget、brew 装过 Claude Code，cli.js 已经在系统里了。

```bash
# npm 全局安装路径
node -e "try{console.log(require.resolve('@anthropic-ai/claude-code/cli.js'))}catch{}"

# 或者通过 which/where 找到 claude 命令，再找同目录的 cli.js
which claude 2>/dev/null || where claude 2>/dev/null
# claude 命令通常是个 shim，实际 cli.js 在 npm 全局 node_modules 里
```

找到后复制到工作目录：
```bash
mkdir -p {brand}-dist
cp <找到的cli.js> {brand}-dist/cli.js
cp <同目录的package.json> {brand}-dist/package.json
cp -r <同目录的vendor/> {brand}-dist/vendor/
```

**情况 B：用户有 claude-code-sourcemap-main.zip**

这个 zip 里有现成的 `package/cli.js`（v2.1.88），直接提取：

```bash
mkdir -p {brand}-dist
unzip -j claude-code-sourcemap-main.zip \
  "claude-code-sourcemap-main/package/cli.js" \
  "claude-code-sourcemap-main/package/package.json" \
  -d {brand}-dist/
# vendor 按当前平台提取（如 Windows x64）：
unzip claude-code-sourcemap-main.zip \
  "claude-code-sourcemap-main/package/vendor/*" \
  -d tmp-extract/
cp -r tmp-extract/claude-code-sourcemap-main/package/vendor/ {brand}-dist/vendor/
rm -rf tmp-extract/
```

> 注：另一个文件 `claudecode.zip` 是还原出来的 TypeScript 源码，只用于阅读理解结构，本流程不需要它。

**情况 C：用户什么都没有**

引导安装 Claude Code：

```bash
# 方式一：npm（需要 Node.js）
npm install -g @anthropic-ai/claude-code

# 方式二：Windows winget
winget install Anthropic.ClaudeCode

# 方式三：macOS brew
brew install claude-code
```

安装完成后按情况 A 定位 cli.js。

---

### Step 2：patch

读取本 skill 目录下的 `scripts/patch.template.js`，将这些占位符替换为实际值：

```
__BRAND_NAME__   → 品牌名（不改品牌就填 "Claude Code"）
__API_BASE_URL__ → API 端点（如 "https://api.deepseek.com"）或 ""
__ENABLE_I18N__  → true 或 false
__BRAND_R__      → 品牌色 R（默认 215）
__BRAND_G__      → 品牌色 G（默认 119）
__BRAND_B__      → 品牌色 B（默认 87）
__LOGO_STYLE__   → default | look-left | look-right | arms-up | custom
__CUSTOM_LOGO__  → 自定义 logo 对象；非 custom 时填 null
```

写入 `{brand}-dist/patch.js`，然后执行：

```bash
# 先备份
cp {brand}-dist/cli.js {brand}-dist/cli.js.bak
# 执行 patch
node {brand}-dist/patch.js {brand}-dist/cli.js
```

**原理（Protect → Replace → Restore）**：
1. 先把 50+ 个协议层字符串换成占位符（User-Agent `claude-cli/`、npm 包名、所有环境变量名、SDK 类名）
2. 做品牌替换（占位符保护下不会误伤协议层）
3. 还原占位符

> 不保护直接替换，会把 HTTP User-Agent 改掉，Kimi 等服务端校验客户端标识会 403。

**视觉定制也在这一步做**：
- 欢迎框边框色和机器人身体色，官方默认是 `rgb(215,119,87)` / `#D77757`
- skill 会把这个颜色改成你提供的 `品牌色`
- 欢迎页小机器人支持这些内置姿态 / 图标：`default`、`look-left`、`look-right`、`arms-up`、`bot-mini`、`pixel-cat`、`star`
- 如果用户提供了自定义 logo，就填 `__LOGO_STYLE__ = custom`，并把 `__CUSTOM_LOGO__` 写成：

```js
{
  r1L: ' 左上 ',
  r1E: '中间上半',
  r1R: ' 右上 ',
  r2L: '左下',
  r2R: '右下',
  feet: '底部一行'
}
```

比如官方默认 logo 实际就是：

```js
{
  r1L: ' ▐',
  r1E: '▛███▜',
  r1R: '▌',
  r2L: '▝▜',
  r2R: '▛▘',
  feet: ' ▗   ▖ '
}
```

如果用户只是想改颜色，不想改图标，就保留 `default`。

---

### Step 3：生成启动脚本

读取 `templates/launcher.bat`（Windows）或 `templates/launcher.sh`（macOS/Linux），替换占位符后写入 `{brand}-dist/`：

```
__BRAND__        → 品牌名
__BRAND_LOWER__  → 小写
__API_KEY__      → API Key
__API_BASE_URL__ → API 端点
```

**写入 .bat 文件时必须注意**：
1. **纯 ASCII 注释**：bat 里的 `rem` 注释和 `echo` 输出只用英文，不写中文。Windows cmd 默认编码是 GBK，中文 Unicode 字符（包括 `──` 这种）会导致 `不是内部或外部命令` 报错
2. **CRLF 行尾**：bat 必须是 `\r\n` 行尾。如果在 macOS/Linux/Git Bash 环境下生成，写入后执行 `sed -i 's/$/\r/' {brand}.bat` 或用 Node.js 写入时确保 `\r\n`
3. **chcp 65001**：脚本开头加 `chcp 65001 >nul 2>&1`，让 node 进程的 stdout 能正确显示 UTF-8（cli.js 输出中文需要这个）

启动脚本里两个关键设计：
- `CLAUDE_CONFIG_DIR=~/.{brand_lower}` — 隔离配置目录，避免全局 OAuth token 抢占
- `ANTHROPIC_AUTH_TOKEN`（不是 API_KEY）— 认证优先级最高，确保走第三方 API

---

### Step 4：验证

```bash
node {brand}-dist/cli.js --version
# 期望: 2.1.xx (BrandName)  或  2.1.xx（不改品牌时无后缀）

# User-Agent 必须在（否则第三方 API 会 403）
node -e "const c=require('fs').readFileSync('{brand}-dist/cli.js','utf8'); console.log(c.includes('claude-cli/') ? 'UA ✓' : 'UA 丢失！')"
```

---

### Step 5（可选）：打包分发

```
{brand}-dist/
├── cli.js            ← 已 patch
├── package.json
├── vendor/           ← 当前平台的 native addon
├── {brand}.bat       ← Windows 启动脚本（含 API key）
├── {brand}.sh        ← macOS/Linux 启动脚本
└── patch.js          ← 留着，方便以后重新 patch
```

打包：
```bash
cd {brand}-dist && zip -r ../{brand}-release.zip . && cd ..
```

接收方要求：有 Node.js 即可（无需安装 Claude Code）。如果目标用户连 Node.js 都没有，可以从 nodejs.org/dist/ 下载对应平台的便携版 `node.exe`，放进分发包根目录，启动脚本里优先使用它。

---

## 完成后告知用户

```
完成 ✓

启动:     ./{brand}.bat（Windows）/ bash {brand}.sh（macOS/Linux）
配置目录: ~/.{brand_lower}（与全局 Claude Code 完全隔离）

两个实例可同时运行：
  ./{brand}.bat  → 第三方 API
  claude         → 官方 Anthropic（如有）
```

---

## 常见问题

| 症状 | 原因 | 解法 |
|------|------|------|
| 403 "客户端异常" | User-Agent 被改 | 检查 `claude-cli/` 是否在 cli.js 里 |
| 401 明明 key 对 | 全局 OAuth 抢占 | 确认用 `ANTHROPIC_AUTH_TOKEN` |
| AUTH_TOKEN 也 401 | OAuth 文件被直接读 | 确认 `CLAUDE_CONFIG_DIR` 指向独立空目录 |
| 工具调用报 400 | 中转不支持 tool_search | 加 `ENABLE_TOOL_SEARCH=false` |
| vendor 报错 | 平台 native addon 缺 | 确认提取了对应平台的 vendor/ |
