---
name: render-engine
description: 从零引导用户注册 Render.com 免费账号、Fork/Clone 代码仓库、配置环境变量、部署 Docker 容器到连接 Web 终端 (ttyd+tmux) 与 EasyTier 网格直连 SSH 的完整生命周期 SOP。用于用户提到从 0 部署 Render、注册 Render、render-engine、render-box、Render 容器部署、Render 终端连接、Render EasyTier 组网、Render 防休眠保活，或要在 Render 免费层上搭建持久安全 Linux 运行时时。包含从 0 引导注册、代码 Fork、Blueprint/手动配置、日志核验、多路连接与日常运维排错。
---

# Render-Engine 从零部署与连接管理 SOP (0 到 1 全周期指南)

`render-engine` 是专为 Render.com Free Tier 打造的单容器安全 Linux Web-Box 运行环境。本 Skill 负责**从零引导用户注册 Render 账号、获取代码仓库、配置环境变量、触发部署、核验日志，直到成功连接终端与虚拟网直连**的完整生命周期。

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                Render-Engine 全生命周期流程                             │
└────────────────────────────────────────────────────────────────────────────────────────┘
  阶段 0: 账号准备       阶段 1: 仓库获取       阶段 2: 服务配置       阶段 3: 触发构建       阶段 4: 终端连接
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ 注册 Render.com │──►│ Fork/Clone 仓库 │──►│ 配置环境变量    │──►│ 启动构建部署    │──►│ 登录 Web Shell  │
│ (GitHub 快捷登录)│   │ (dengyie/       │   │ (密码/网格/探针)│   │ (核验 Build/    │   │ (ttyd+tmux/SSH) │
│ 免费 512MB 实例 │   │  render-engine) │   │ (零配置开箱即用)│   │  Deploy 日志)   │   │ (持久化会话保持)│
└─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘
```

按需查阅参考手册，避免一次性全量加载：
- `references/deployment.md`：Render Blueprint（render.yaml）、环境变量配置矩阵与控制台图文引导
- `references/network-mesh.md`：EasyTier smoltcp 用户态虚拟网格组网、Peer 连接与免密 SSH 直连
- `references/terminal-persistence.md`：ttyd+tmux 断线无损保持机制与 Agent 自动化 WebSocket 协议
- `references/troubleshooting.md`：常见排错（OverlayFS 宿主度量泄露辟谣、Spindown 保活与掉线恢复）

---

## 阶段 0：引导用户注册 Render.com 账号

接手从零部署任务时，先协助或引导用户准备平台账号：

1. **注册入口**：访问 [Render 注册页面](https://dashboard.render.com/register)。
2. **推荐方式**：选择 **"Sign up with GitHub"**。
   - **优势**：一键授权登录，无需繁琐邮箱验证，且能直接打通后续 GitHub 仓库自动同步部署权限。
3. **配额说明（给用户的安心提示）**：
   - Render 个人免费版（Free Tier）无需绑定信用卡即可部署 Docker Web Service。
   - 每个免费账号每月拥有 750 小时免费运行额度（足以全月 24 小时运行 1 个服务）。
   - 单实例配额：512 MB 内存、0.15 vCPU、单个公网端口。

---

## 阶段 1：获取代码仓库 (Fork / Clone)

Render 通过拉取 Git 仓库代码自动执行 Docker 镜像构建。引导用户将项目同步到自己的 GitHub：

1. **上游项目地址**：[`https://github.com/dengyie/render-engine`](https://github.com/dengyie/render-engine)
2. **操作指引**：
   - **方式 A（Fork 到个人 GitHub，推荐用于长期自动化更新）**：
     引导用户点击项目页面右上角 **"Fork"**，创建属于自己的副本（如 `https://github.com/<user>/render-engine`）。
   - **方式 B（直接引用公开源仓库，适合一键体验）**：
     若用户不想 Fork，Render 支持直接连接任何公开的 GitHub 仓库进行部署。

---

## 阶段 2：在 Render 创建并配置服务

提供两种配置路径，优先推荐 **路径 A（一键 Blueprint）**：

### 路径 A：一键快速部署 (Render Blueprint，最快最准)

1. 点击或引导用户在浏览器中打开专属部署入口：
   ```text
   https://render.com/deploy?repo=https://github.com/dengyie/render-engine
   ```
   *(若用户已 Fork，将链接中的 repo 替换为用户个人仓库地址)*
2. 页面会自动识别项目根目录下的 `render.yaml` 规格文件。
3. 提示用户核对或填入以下参数：
   - **Service Name**：默认 `render-engine`（可自命名，例如 `my-box`）。
   - **Region**：选择就近机房（推荐 `Oregon (US West)`、`Singapore (Southeast Asia)` 或 `Frankfurt (EU Central)`）。
   - **Plan**：确认选中 **`Free`**。
4. 点击 **"Apply"** 即可全自动创建服务。

### 路径 B：手动创建 Web Service

若通过控制台手动添加：
1. 登录 [Render Dashboard](https://dashboard.render.com/)，点击右上角 **"New +"** -> 选择 **"Web Service"**。
2. 选择 **"Build and deploy from a Git repository"**，搜索并选中 `render-engine`。
3. 配置基本属性：
   - **Name**：`render-engine`
   - **Region**：推荐 `Oregon (US West)`
   - **Branch**：`main`
   - **Runtime**：选择 **`Docker`**
   - **Instance Type**：选择 **`Free`** (512 MB / 0.15 CPU)
4. 高级配置（Advanced）：
   - **Health Check Path**：填入 `/health`（极其重要：平台借此判断容器启动完毕，杜绝 502）。
5. **环境变量按需注入（渐进式原则）**：
   - **纯净开箱模式（零配置）**：无需添加任何环境变量！容器会自动生成随机 18 位强密码并在日志打印。
   - **固定凭据模式（推荐新手）**：
     - `SSH_PASS`：设置固定密码（如 `YourStrongPass2026!`，用于 Web 终端与 SSH）。
     - `TTYD_USER`：设置 Web 终端用户名（默认 `admin`）。
   - **虚拟网格模式（可选加入 EasyTier）**：
     - `ENABLE_EASYTIER`：`true`
     - `ET_NAME`：网格名称（如 `my-mesh`）
     - `ET_SECRET`：通信密钥
     - `ET_PEERS`：核心节点（如 `tcp://hub1.example.com:11010`）
   - **监控探针模式（可选加入 Komari / MangoHub）**：
     - `KOMARI_ENDPOINT`：监控服务端地址（如 `https://hub.example.com`）
     - `KOMARI_TOKEN`：探针通信 Token
     - `KOMARI_FORCE_DISK_TOTAL`：`5368709120`（消除宿主机 OverlayFS 虚假度量泄露）

---

## 阶段 3：触发构建与部署日志核验

点击 **"Create Web Service"**，进入部署流程：

1. **查看构建日志 (Build Logs)**：
   - 观察 Alpine 基础镜像拉取、Caddy/ttyd/EasyTier 二进制注入。
   - 确认无构建报错，直至输出 `=> exporting to image`。
2. **查看运行日志 (Deploy / Service Logs)**：
   - 观察 `entrypoint.sh` 启动流程：
     - **提取随机密码**（若未自定义 `SSH_PASS`）：
       ```text
       ========================================================
         Root/Web password set to: XXXXXXXXXXXXXXXXXX
       ========================================================
       ```
       *提醒用户妥善复制该 18 位密码！*
     - 确认组件顺序拉起：`Caddy` (Port 10000)、`OpenSSH`、`ttyd`。
     - 确认探活放行：Render 平台发起 `/health` 探测并收到 `200 OK`，服务状态变更为绿色的 **"Live"**。

---

## 阶段 4：连接并使用 Render 容器

提供 3 种连接使用方式，适应不同场景：

### 方式 1：Web 浏览器直接访问 (零客户端门槛)
1. 在 Render 控制台顶部获取已分配的 HTTPS 公网域名（如 `https://render-engine.onrender.com`）。
2. 在浏览器打开：
   ```text
   https://<your-service-name>.onrender.com/shell/
   ```
3. 弹出 BasicAuth 认证弹窗：
   - 用户名：`admin`（或自定义的 `TTYD_USER`）
   - 密码：日志打印的随机密码或自定义的 `SSH_PASS`
4. 成功登入内置持久化终端：
   - 会话由 `tmux` 常驻守护（`main` 会话），断线、刷新或关掉浏览器，任务不中断；
   - 再次打开链接无缝恢复工作区（Attach）；
   - 支持鼠标滚轮滚动浏览历史（50,000 行缓冲区）。

### 方式 2：通过 EasyTier 虚拟网格直连 SSH (安全无公网暴露)
若配置了 EasyTier，容器接入私有网格，IP 为 `10.144.144.90`：
```bash
# 密码认证直接登录
sshpass -p "<SSH_PASS>" ssh -o StrictHostKeyChecking=no root@10.144.144.90

# 或通过网格跳板机 (如 pxed) 免密登录
ssh -o ProxyJump=pxed root@10.144.144.90
```

### 方式 3：AI Agent 自动化无头连接 (WebSocket)
Agent 本地无浏览器时，可使用 Python 通过标准 WebSocket RFC 6455 发送二进制指令与捕获回显，详见 `references/terminal-persistence.md`。

---

## 阶段 5：日常运维、防休眠保活与常见排错

### 1. 免费版 15 分钟休眠防断与 24/7 运行 (Keep-Alive)
- **平台休眠机制**：Render Free Tier 若连续 15 分钟无入站公网 HTTP 请求，容器将自动挂起进入 Spindown（下次请求需 15~30 秒冷启动重建 Pod，且会重置临时文件与 tmux 会话）。
- **额度核算**：Render 每个免费账号每月分配 **750 小时** 运行时长。即使按全月 31 天无休持续跑满，`31 天 × 24h = 744h`，单实例 24/7 运行完全处于免费额度内，不会产生成本。
- **内置自主保活（默认开启）**：`render-engine` 容器启动时会自动读取平台注入的 `RENDER_EXTERNAL_URL`，拉起轻量后台守护进程（`ENABLE_KEEPALIVE=true`，默认周期 300 秒），通过外部公网域名循环请求自身的 `/health`。此举可自动向 Render 边缘网关产生真实的入站 HTTP 流量，重置闲置计时器，开箱即用实现 24/7 常驻。
- **外部兜底拨测（可选备份）**：为防止容器被手动重启后的冷启动滞后，亦可在外部 [UptimeRobot](https://uptimerobot.com/) 或各类定时服务（Cron / 自建 VPS Crontab）中配置辅助 HTTP 探活任务：
  - 监控类型：`HTTP(s)`
  - URL：`https://<your-service-name>.onrender.com/health`
  - 监控频率：每 `5 分钟` 或 `10 分钟` 一次
  - 预期响应：`200 OK`。

### 2. 线上掉线诊断三步法
1. 先查公网：`curl -s https://<render-host>/health`。若返回 200，定性为容器在线，仅为私有网格或监控断流。
2. 检查环境变量：核实 Render 控制台是否遗漏注入 `ET_PEERS` 或 `KOMARI_ENDPOINT`。
3. 临时热修复：在 Web Shell 执行 `easytier-cli connector add tcp://<hub-ip>:11010` 即可实时拉起虚拟网。

### 3. 辟谣“386G 磁盘占用 86%”告警
- **真相**：`df -h` 汇报的 386GB 盘已用 315GB 实为 Kubernetes 多租户节点的底层宿主 OverlayFS 泄露。
- **验证**：在终端运行 `du -sh / --exclude=/proc --exclude=/sys --exclude=/dev` 确认实际占用仅约 **191.7 MB**。
- **处置**：严禁误删系统文件；探针配置 `KOMARI_FORCE_DISK_TOTAL=5368709120` 即可归一化面板度量。
