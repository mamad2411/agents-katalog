# AVG-AdventurerTavern (冒险者酒馆)

## 项目概况

AdventurerTavern 是一款高保真视觉小说（Visual Novel）风格的角色扮演游戏框架，结合 LLM 技术提供沉浸式的异世界酒馆经营与恋爱模拟体验。

- 堆栈：Vite + React 19 + TypeScript + Tailwind 4
- 部署：前端镜像**本地构建**，推送到私有镜像仓库 NyaaDockerHUB（endpoint 见 `.env` 的 `PRIVATE_DOCKER_REGISTRY_*`，不入库），容器从私有仓库拉取运行
- 辅助服务：`database-server/` + `file-server/`（各独立管理，含子模块）
- 仓库：https://github.com/NyaaCaster/AVG-AdventurerTavern.git
- 主分支：main（⚠️ 不是 master！曾误记为主分支 master 导致 push origin master 失败）
- 访问：HTTP `localhost:3098` / HTTPS `localhost:3096`

## 交流语言

默认始终以**简体中文**与用户交流，除非用户在某次对话中明确要求改用其他语言。

## 重新编译 Docker 镜像并重启容器

前端镜像**本地构建**并推送到私有镜像仓库 NyaaDockerHUB（GitHub Actions 线上构建已停用，`docker-publish.yml` 已删除）：

- 标准流程：`python rebuild.py` —— 读 `.env`（registry 端点 + Vite build-args）→ docker build（tag = git short SHA + latest）→ push 私有仓库 → 仓库端只保留当前 SHA + latest → `docker compose pull` + `up -d` 重启 → 清理本项目旧 tag 与悬空镜像。
- 注意：镜像**不再包含证书私钥**，SSL 证书改由运行时 `:ro` 卷挂载提供（见「HTTPS 自动续期」）；构建无 SSL secret、不依赖 `SSL/`。
- 强制无缓存重建：`python rebuild.py --no-cache`。
- 仅本地构建调试（不推送）：`python rebuild.py --skip-push`。
- 私有仓库为 HTTP，本机 Docker 需已将 registry host 加入 `insecure-registries`（本机已配置）。
- macmini 侧仅拉取远端最新镜像并重启（不构建）：`python restart.py`。
- ⚠️ macmini 各服务部署目录 `.env` 的 `PRIVATE_DOCKER_REGISTRY_HOST` 必须为 `192.168.31.142:5000`（不是 `localhost:5000`）——写错会让 `restart.py` 的 `docker compose pull` 失败、`up -d` 直接打挂线上（2026-09-12 前端部署目录即为此残留，已修）。
- ⚠️ 根目录 `rebuild.py` 末尾会执行 `docker compose pull + up -d`（启动**本机**容器）。按工作空间规则本机不承接对外服务，若只需构建推送，请用 `file-server/rebuild.py` / `database-server/rebuild.py` 的同类流程（仅 build+push），或临时手动 build+push。
- ⚠️ **注册表清理只可按 digest 删除，且必须先保护保留 tag 的 digest**：Docker Registry 拒绝按 tag 删除（`DIGEST_INVALID`），而**内容完全相同**的重建会让新旧 tag 共用同一 manifest digest —— 直接按 digest 删过期 tag 会把 `latest`/当前 sha tag 一起删光（2026-09-12 在 `adv-tavern-db` 上真实发生，仓库 `tags` 变 `null`，macmini 下一次 pull 就会失败）。三个 `rebuild.py` 的 `registry_cleanup` 已加固：先解析保留 tag 的 digest，共用者一律 SKIP。
- 数据库服务和文件服务器独立管理，分别通过各自目录下的 `rebuild.py` 操作。

## Git 提交与推送

> ⚠️ **本项目默认分支是 `main`（不是 master！）**。push 一律用 `git push origin main`；
> `push origin master` 会报 `src refspec master does not match any`。
> （2026-08-22 踩坑：CLAUDE.md 曾误写"主分支：master"，导致别名替换提交时推错分支名。）

每当用户明确要求提交/推送，使用 `commit-push` skill 完成。要点：

- **未经用户明确请求，绝不自动 commit / push**。
- 提交信息使用 **Conventional Commits**（英文，小写起首）；**不**附加 `Co-Authored-By` 行。
- 始终用 `git add <file>` 明确指定文件，**禁止** `git add -A` / `git add .`。
- `.env`（含 API 密钥）、`.claude/settings.local.json` **绝不入库**——已在 `.gitignore` 中排除，但提交前仍要肉眼复核 `git status` 输出。
- 严禁：force push、`--amend` 已推送的 commit、`--no-verify`、修改 `git config`、`reset --hard` 等高破坏性操作（除非用户显式同意）。
- 注意子模块 (`file-server`) 和独立服务 (`database-server`) 的改动需分别提交。

## HTTPS 自动续期（Let's Encrypt + acme.sh）

证书改为 **Let's Encrypt 单张 SAN 证书**（覆盖 `h.hony-wen.com` + `h.nyaa.host`，ec-256），由 **macmini 宿主 acme.sh** 管理，**不再构建期烤进镜像、不再手动换 TrustAsia 证书**。完整方案见 `.docs/自动续期SSL改造计划.md`。

- **证书来源与续期**：macmini（192.168.31.141）宿主 `/root/.acme.sh/` 每日 cron 自动续期同一张 SAN 证书（DNSPod `dns_dp` 验证，凭据仅在 `/root/.acme.sh/account.conf`，**绝不进仓库 / `.env` / 容器**）。
- **运行时挂载**：compose 以 `:ro` 卷将宿主 `certs/`（`/root/DockerContainer/AVG-AdventurerTavern/certs`，可用 `CERT_DIR` 覆盖，默认 `./certs`）挂到容器 `/etc/nginx/ssl`。**前端容器与 file-server 容器共用同一份 `certs/`**（file-server 侧变量名 `AVG_CERT_DIR`，默认 `./SSL`，仅本地开发用）。**数据库服务另用 `db-certs/`**（变量 `AVG_DB_CERT_DIR`）：它以非 root（`uid=1001 gid=65533`）运行，`certs/privkey.pem` 的 `0600 root` 会 `EACCES`，故由 hook 同步一份 `privkey 0640 root:65533` 的副本。
- **nginx.conf / 服务端证书路径**：前端两个 443 server 块与 `file-server/nginx.conf`、`nginx-no-upload.conf` 统一指向 `/etc/nginx/ssl/fullchain.pem` + `privkey.pem`；`database-server/config.js` 默认 `SSL/fullchain.pem` + `SSL/privkey.pem`（可用 `SSL_CERT_PATH`/`SSL_KEY_PATH` 覆盖）。
- **续期 reload 链路（生产一致）**：权威源在宿主机 `/etc/letsencrypt/h.hony-wen.com/{fullchain.pem,privkey.pem}`（acme.sh 的 dsh install-cert 更新，dsh nginx、酒馆、file-server、database-server 共用同一条 install-cert）。acme.sh 续期后 reloadcmd 执行 `acme/reload_certs.py` → 宿主 `nginx -t` → 同步到 AVG `certs/`（644/600 root）、MyToken `certs/`、AVG `db-certs/`（640 root:65533）→ 宿主 dsh `nginx -s reload` → 依次热加载 `adventurertavern`、`adv-file-server`、`mytoken-web` 容器 nginx，以及 **`adventurertavern-db`（Node：`docker kill -s HUP` + 健康探针，失败回退 `docker restart`）** → 链式调用 Caddy hook → 写日志 `acme/reload.log`。零重建、零停机。
  - 💡 `database-server` 的 SIGHUP 热加载依赖 `index.js` 里注册的 `process.on('SIGHUP')`（`setSecureContext`）；**若对该容器发 SIGHUP 而镜像里没有该 handler，Node 会直接退出**（靠 `restart: unless-stopped` 拉起，也能读到新证书，但有一次中断）。
  - ⚠️ **前端镜像与 file-server 镜像都要重建才生效**：改 nginx.conf 后需 `python rebuild.py`（前端根目录 / `file-server/` 各一次）+ macmini 侧对应 `restart.py`。
  - ⚠️ **踩坑（2026-09-12 已修）**：`file-server` 原先挂载宿主 `ssl/`（旧 TrustAsia 证书，硬编码文件名 `h.nyaa.host_bundle.crt`），且**未被 acme reload hook 覆盖** → 该证书 2026-08-31 过期后，浏览器拒绝加载 `https://h.nyaa.host:5102/files/**`（美术/音频资源全灭），而酒馆页面 3096 正常，表现为「页面能开、无美术」。现已统一为共用 `certs/` + 纳入 hook；旧目录留档为 `ssl.deprecated-20260912/`。**排查口诀**：美术/音频取不到时先 `curl -v https://h.nyaa.host:5102/files/README.txt`（不加 `-k`）看是否 `SEC_E_CERT_EXPIRED`。
- **部署注意事项**：
  - `restart.py` 启动前会校验 `certs/fullchain.pem` + `privkey.pem` 存在，缺失即报错退出（先完成首次签发）。
  - 续期/刷新统一以 `acme/reload_certs.py` 为准（随代码入库、与 macmini 生产一致），脚本内 `PATH` 追加 `/snap/bin`。
  - 容器若未运行，`reload_certs.py` 只警告并跳过容器 reload（宿主已刷新），不致命。
  - 首次正式签发必须带 `--server letsencrypt --force`（防被 staging 续期时间跳过），见计划文档 §5。

## 本地开发

```bash
npm install        # 安装依赖
npm run dev        # Vite 开发服务器
npm run build      # 生产构建
npm run lint       # TypeScript 类型检查（无 emit）
npm run test       # Vitest 测试
```

## Vibo Coding 工作规范

> 本项目为存量项目，适用"**部分适用**"级别——跳过初始设计和审核阶段，从当前 P 阶段续接。

### 版本与阶段（V + P）

- **V（闭环版本）**：一个对外可用、功能闭环的版本。
- **P（功能模块阶段）**：一个 V 内部按功能模块拆分的最小交付单元，每个 P 必须**可独立验证、可独立提交**。

### Plan 模式开发

所有 P 阶段的实现工作在 **plan 模式**下进行：
1. 针对当前 P 阶段用 `EnterPlanMode` 进入 plan 模式
2. 明确本 P 的实现方案、涉及文件、验证步骤
3. 用户批准 plan 后执行实现
4. 完成验证

### P 阶段收尾（每 P 必做）

每个 P 阶段完成后，**必须**执行：

1. **Git 提交与推送** — 通过 `commit-push` skill，提交前必须做 `git status` 和 secret 检查
2. **更新或创建交接文档** — 落于 `.docs/阶段交接-XXX.md`，使用以下结构：
   - 交接目的 + 必读文档列表
   - 当前进度（本 P 完成了什么）
   - 本轮已修复/已实现（按文件列出）
   - 仍需验证/已知问题
   - **续接提示词**（可直接粘贴给新对话的提示词，约 10-20 行，含必读文档、当前进度、下一步行动、关键约束）
3. **更新 Memory** — 关键节点写入 memory 跟踪进度

### 跨对话接续

新对话继续开发时：读取本 CLAUDE.md → 读取最新交接文档 → 根据"续接提示词"确定下一步 → plan 模式进入。
