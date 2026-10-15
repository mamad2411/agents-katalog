---
name: deploy-nextjs-ecs
description: 将本地 Next.js 项目通过 PM2 部署到阿里云 ECS。当用户想把 Next.js 应用部署或重新部署到 ECS 实例时使用。
argument-hint: "[ECS_IP] [远程用户] [应用名称]"
allowed-tools: Bash Read Write Edit
---

# 部署 Next.js 到阿里云 ECS（PM2 方案）

用中文与用户交流，按以下步骤逐步完成部署。

## 第 0 步 — 收集配置

如有缺失，请先向用户询问以下信息：

| 变量 | 示例 |
|---|---|
| `ECS_IP` | `123.45.67.89` |
| `REMOTE_USER` | `root` |
| `APP_NAME` | `my-app` |
| `REMOTE_DIR` | `/apps/my-app` |
| `APP_PORT` | `3000` |
| `SSH_KEY` | `~/.ssh/id_rsa` |

如果用户通过参数传入，按顺序解析为：ECS_IP、REMOTE_USER、APP_NAME。

## 第 1 步 — 本地检查

```bash
# 确认是 Next.js 项目
test -f package.json && grep -q '"next"' package.json && echo "✓ Next.js 项目确认" || echo "✗ 非 Next.js 项目，请检查目录"

# 测试 SSH 连通性
ssh -i $SSH_KEY -o ConnectTimeout=10 -o BatchMode=yes $REMOTE_USER@$ECS_IP "echo '✓ SSH 连接正常'"
```

若 SSH 失败，提示用户检查：ECS 安全组是否开放 22 端口、SSH 密钥路径是否正确。

## 第 2 步 — 本地构建

```bash
npm ci --prefer-offline 2>/dev/null || npm install
npm run build
```

构建失败时停止并清晰展示错误信息，不继续执行后续步骤。

## 第 3 步 — 服务器初始化（首次部署执行）

```bash
ssh -i $SSH_KEY $REMOTE_USER@$ECS_IP << 'EOF'
# 安装 Node.js（通过 nvm）
if ! command -v node &>/dev/null; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"
  nvm install --lts && nvm alias default node
fi
echo "Node 版本: $(node -v)"

# 安装 PM2
if ! command -v pm2 &>/dev/null; then
  npm install -g pm2
fi
echo "PM2 版本: $(pm2 -v)"

mkdir -p $REMOTE_DIR
EOF
```

## 第 4 步 — 传输文件

先检测是否使用了 standalone 模式：

```bash
grep -r "standalone" next.config.* 2>/dev/null && echo "standalone 模式" || echo "标准模式"
```

**standalone 模式（推荐）：**
```bash
rsync -avz --delete \
  .next/standalone/ $REMOTE_USER@$ECS_IP:$REMOTE_DIR/

rsync -avz .next/static/ $REMOTE_USER@$ECS_IP:$REMOTE_DIR/.next/static/
rsync -avz public/       $REMOTE_USER@$ECS_IP:$REMOTE_DIR/public/
```

**标准模式：**
```bash
rsync -avz --delete \
  --exclude='.git' --exclude='node_modules' --exclude='.next' \
  . $REMOTE_USER@$ECS_IP:$REMOTE_DIR/

rsync -avz .next/ $REMOTE_USER@$ECS_IP:$REMOTE_DIR/.next/

ssh -i $SSH_KEY $REMOTE_USER@$ECS_IP "cd $REMOTE_DIR && npm ci --only=production"
```

## 第 5 步 — 上传环境变量

```bash
if [ -f .env.production ]; then
  scp -i $SSH_KEY .env.production $REMOTE_USER@$ECS_IP:$REMOTE_DIR/.env.production
  echo "✓ 已上传 .env.production"
elif [ -f .env.local ]; then
  echo "⚠ 发现 .env.local，这通常是本地开发配置，是否确认上传？请检查其中的变量值是否适合生产环境。"
fi
```

## 第 6 步 — PM2 启动 / 重启

```bash
ssh -i $SSH_KEY $REMOTE_USER@$ECS_IP << EOF
cd $REMOTE_DIR

[ -f server.js ] && START_CMD="node server.js" || START_CMD="npm start"

if pm2 list | grep -q "$APP_NAME"; then
  pm2 reload $APP_NAME --update-env && echo "✓ 已热重载"
else
  PORT=$APP_PORT pm2 start \$START_CMD --name "$APP_NAME"
  pm2 save
  echo "✓ 已启动"
fi

pm2 show $APP_NAME
EOF
```

## 第 7 步 — 验证部署

```bash
curl -s -o /dev/null -w "HTTP 状态码: %{http_code}\n" http://$ECS_IP:$APP_PORT/
```

若非 200，自动拉取日志帮助排查：
```bash
ssh -i $SSH_KEY $REMOTE_USER@$ECS_IP "pm2 logs $APP_NAME --lines 30 --nostream"
```

## 常见问题

| 现象 | 解决方法 |
|---|---|
| SSH 连接超时 | 检查 ECS 安全组，开放 22 端口 |
| PM2 启动后立即退出 | 查看日志 `pm2 logs $APP_NAME`，检查 .env 是否存在 |
| 端口无法访问 | 检查 ECS 安全组是否开放 $APP_PORT |
| 本地构建失败 | 先执行 `npm ci && npm run build` 确保本地通过 |

## 部署完成

打印部署摘要：

```
✓ 部署成功：$APP_NAME
  服务器：$REMOTE_USER@$ECS_IP
  目录　：$REMOTE_DIR
  端口　：$APP_PORT
  访问　：http://$ECS_IP:$APP_PORT
  日志　：pm2 logs $APP_NAME
```
