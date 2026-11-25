---
name: gitnexus-explorer
description: Serve an interactive codebase knowledge graph web UI.
version: 1.0.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gitnexus, code-intelligence, knowledge-graph, visualization]
    related_skills: [hermes-agent, codebase-inspection]
---

# GitNexus Explorer

可将任意代码库索引至知识图谱中，并提供一个交互式网页界面，用于查看符号、调用链、聚类以及执行流程。通过 Cloudflare 建立隧道以实现远程访问。

## 适用场景

- 用户希望直观地了解代码库的架构
- 用户需要获取某个代码仓库的知识图谱或依赖关系图
- 用户想要与他人共享这个交互式代码库探索工具

## 先决条件

- **Node.js**（v18+）——GitNexus 及代理功能所需
- **git**——代码仓库必须包含 `.git` 目录
- **cloudflared**——用于建立隧道连接（如未安装则自动安装至 ~/.local/bin）

## 容量限制提示

网页界面会在浏览器中渲染所有节点。文件数量在 5,000 个以内的代码仓库使用效果最佳。对于大型代码仓库（节点数超过 30,000 个），页面加载速度会变慢，甚至可能导致浏览器标签页崩溃。CLI 和 MCP 工具则不受此限制，仅网页可视化功能存在此类限制。

## 操作步骤

### 1. 克隆并构建 GitNexus（一次性设置）

```bash
GITNEXUS_DIR="${GITNEXUS_DIR:-$HOME/.local/share/gitnexus}"

if [ ! -d "$GITNEXUS_DIR/gitnexus-web/dist" ]; then
  git clone https://github.com/abhigyanpatwari/GitNexus.git "$GITNEXUS_DIR"
  cd "$GITNEXUS_DIR/gitnexus-shared" && npm install && npm run build
  cd "$GITNEXUS_DIR/gitnexus-web" && npm install
fi
```

### 2. 修复用于远程访问的 Web UI

Web UI 在进行 API 调用时默认使用 `localhost:4747`。需对其进行修改，使其遵循同源策略，从而能够通过隧道/代理正常工作：

**文件路径：` $GITNEXUS_DIR/gitnexus-web/src/config/ui-constants.ts`**
修改内容：
```typescript
export const DEFAULT_BACKEND_URL = 'http://localhost:4747';
```
收件人：
```typescript
export const DEFAULT_BACKEND_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost' ? window.location.origin : 'http://localhost:4747';
```

**文件：`"$GITNEXUS_DIR/gitnexus-web/vite.config.ts"`**
在 `server: { }` 块中添加 `allowedHosts: true`（仅当在开发模式运行而非生产构建时需要此设置）：
```typescript
server: {
    allowedHosts: true,
    // ... existing config
},
```

接着构建生产环境版本包：
```bash
cd "$GITNEXUS_DIR/gitnexus-web" && npx vite build
```

### 3. 对目标代码库进行索引

```bash
cd /path/to/target-repo
npx gitnexus analyze --skip-agents-md
rm -rf .claude/    # remove Claude Code-specific artifacts
```

如需进行语义搜索，请添加 `--embeddings` 参数（但速度会变慢，从秒级变为分钟级）。

索引文件存储在仓库内的 `.gitnexus/` 目录中，并会被自动标记为 Git 忽略文件。

### 4. 创建代理脚本

将该脚本内容写入一个文件中（例如 `$GITNEXUS_DIR/proxy.mjs`）。该脚本负责提供生产环境下的 Web UI，同时将 `/api/*` 的请求转发至 GitNexus 后端——由于同源策略的保障，无需处理 CORS 问题，也不需要使用 sudo 权限或 nginx 服务器。

```javascript
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const API_PORT = parseInt(process.env.API_PORT || '4747');
const DIST_DIR = process.argv[2] || './dist';
const PORT = parseInt(process.argv[3] || '8888');

const MIME = {
  '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.wasm': 'application/wasm',
};

function proxyToApi(req, res) {
  const opts = {
    hostname: '127.0.0.1', port: API_PORT,
    path: req.url, method: req.method, headers: req.headers,
  };
  const proxy = http.request(opts, (upstream) => {
    res.writeHead(upstream.statusCode, upstream.headers);
    upstream.pipe(res, { end: true });
  });
  proxy.on('error', () => { res.writeHead(502); res.end('Backend unavailable'); });
  req.pipe(proxy, { end: true });
}

function serveStatic(req, res) {
  let filePath = path.join(DIST_DIR, req.url === '/' ? 'index.html' : req.url.split('?')[0]);
  if (!fs.existsSync(filePath)) filePath = path.join(DIST_DIR, 'index.html');
  const ext = path.extname(filePath);
  const mime = MIME[ext] || 'application/octet-stream';
  try {
    const data = fs.readFileSync(filePath);
    res.writeHead(200, { 'Content-Type': mime, 'Cache-Control': 'public, max-age=3600' });
    res.end(data);
  } catch { res.writeHead(404); res.end('Not found'); }
}

http.createServer((req, res) => {
  if (req.url.startsWith('/api')) proxyToApi(req, res);
  else serveStatic(req, res);
}).listen(PORT, () => console.log(`GitNexus proxy on http://localhost:${PORT}`));
```

### 5. 启动服务

```bash
# Terminal 1: GitNexus backend API
npx gitnexus serve &

# Terminal 2: Proxy (web UI + API on one port)
node "$GITNEXUS_DIR/proxy.mjs" "$GITNEXUS_DIR/gitnexus-web/dist" 8888 &
```

验证方法：执行命令 `curl -s http://localhost:8888/api/repos`，应能返回已索引的仓库列表。 

### 6. 使用 Cloudflare 建立隧道（可选——用于远程访问）

```bash
# Install cloudflared if needed (no sudo)
if ! command -v cloudflared &>/dev/null; then
  mkdir -p ~/.local/bin
  curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o ~/.local/bin/cloudflared
  chmod +x ~/.local/bin/cloudflared
  export PATH="$HOME/.local/bin:$PATH"
fi

# Start tunnel (--config /dev/null avoids conflicts with existing named tunnels)
cloudflared tunnel --config /dev/null --url http://localhost:8888 --no-autoupdate --protocol http2
```

隧道地址（例如 `https://random-words.trycloudflare.com`）会输出到标准错误流中。请将该地址分享出去——拥有该链接的任何人都可以查看对应的图表结构。

### 7. 清理工作

```bash
# Stop services
pkill -f "gitnexus serve"
pkill -f "proxy.mjs"
pkill -f cloudflared

# Remove index from the target repo
cd /path/to/target-repo
npx gitnexus clean
rm -rf .claude/
```

## 常见问题

- **对于 cloudflared，必须使用 `--config /dev/null`**。如果用户已在 `~/.cloudflared/config.yml` 中配置了命名隧道设置，就会出现此问题。否则，配置文件中的通用接入规则会导致所有快速隧道请求均返回 404 错误。

- **进行隧道连接时必须使用生产环境构建版本**。Vite 开发服务器默认会通过 `allowedHosts` 设置阻止非本地主机访问。而使用生产环境构建版本结合 Node 代理则完全可以避免这一问题。

- **Web 界面不会自动创建 `.claude/` 或 `CLAUDE.md` 文件**。这些文件是由 `npx gitnexus analyze` 命令生成的。若希望不生成 Markdown 文件，可使用 `--skip-agents-md` 参数，随后再通过 `rm -rf .claude/` 删除相关文件。这些内容属于 Claude Code 的集成功能，Hermes Agent 用户并无需求。

- **浏览器内存限制**。Web 界面会将整个项目结构加载到浏览器内存中。文件数量超过 5,000 个的仓库可能会导致运行缓慢，而超过 30,000 个文件的仓库很可能会使浏览器标签页崩溃。

- **嵌入向量是可选功能**。使用 `--embeddings` 参数可启用语义搜索，但对于大型项目来说，该操作可能需要数分钟时间。如需快速浏览项目，可跳过此参数；若希望通过 AI 聊天面板进行自然语言查询，则可添加该参数。

- **多个仓库管理**。`gitnexus serve` 会加载所有已索引的仓库。只需先为多个仓库建立索引，再启动一次服务，Web 界面即可支持在这些仓库之间切换。
