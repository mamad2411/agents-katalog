---
name: ctf-platform
description: "Use when a task involves CTF platform automation: logging into a competition platform, managing saved sessions, crawling challenges and attachments, submitting flags, or maintaining the shared platform/ directory (docs, scripts, credentials, logs) across competitions. Trigger on mentions of 平台, platform, 抓题, 爬取题目, 提交flag, 登录态, keepalive, platforms.json, or when the user asks the agent to fetch challenges from or submit flags to a CTF platform (CTFd, GZCTF, 自研平台 like ctfplus)."
---

# CTF Platform Automation

管理跨比赛共享的平台交互区 `/root/ctf/.share/platform/`（比赛目录内软链 `platform -> ../.share/platform`）。
本 skill 是平台自动化的**唯一规范来源**；AGENTS.md 只保留指向这里的引用。

## 核心原则

1. **先读文档再动手**：接入任何平台前，先读 `platform/README.md` 和对应平台目录的
   `<平台名>/README.md`。所有探查成果（认证链、API 端点、踩坑记录）都沉淀在平台 README 里，
   **新会话严禁重复探查已有内容**。
2. **机制与题目分离**：`platform/` 只存机制（文档/脚本/凭据/日志/探查缓存）；
   抓取的题目一律落盘到当前比赛目录的 `<类别>/<题目名>/`，遵守解题根目录的文件夹规范。
3. **跨比赛复用**：同一平台（如 ctfplus）多场比赛共用一个平台目录，比赛差异
   （competition_id / node_url）登记在 `auth/state.json`，不复制脚本。
4. **明确要求才自动化**：爬取、提交、保活等自动化操作只在用户明确要求时执行；
   没要求自动提交就不要写提交脚本（最小原则）。
5. **平台更新则重新探查**：接口失效（404/字段变更/认证变化）时按平台 README 的
   「平台更新流程」章节重新探查，并把新结论**写回 README**，保持文档与实现同步。

## 目录结构（强制）

```
/root/ctf/.share/platform/
├── README.md            # 总体说明 + 新会话接手流程 + 新平台接入流程
├── platforms.json       # 平台索引：名称/类型/base_url/状态
├── _common/client.py    # 统一 HTTP 封装（重试/限速≥0.5s/UA/超时/下载）
└── <平台名>/
    ├── README.md        # 【必须】平台完整文档：概况/认证链/API/脚本用法/更新流程/踩坑记录
    ├── platform.json    # 平台元数据：API 风格、端点、限速约定
    ├── scripts/         # session.py / crawl.py / instance.py / submit.py(按需) / 探查工具
    ├── auth/            # 凭据与会话，chmod 700/600
    │   ├── account.json #   账密
    │   ├── cookies.json #   会话（多比赛按短名分桶）
    │   └── state.json   #   已登记比赛（id/node_url）、活跃比赛、健康度
    ├── logs/            # 操作日志（追加式，含每次爬取/提交结果）
    └── (缓存在 platform/.cache/<平台名>/)
```

新平台接入完成前不算完成：README.md 缺失 = 接入不合格。

## 安全约束（强制）

- `auth/` 目录 `chmod 700`，内部文件 `chmod 600`，创建即设置。
- 凭据严禁出现在 steps.md、wp.md、logs 或任何对外输出；文档只写"使用了 xxx 平台的已保存登录态"。
- 凭据更新只改 `cookies.json`/`state.json`，不改 `account.json`。
- 提交 flag 前必须查 `logs/` 去重；每次提交结果（含失败）追加记录到 `logs/`。
- 爬取/提交频率遵守 `platform.json` 声明的限速（默认间隔 ≥0.5s）。

## 标准工作流

### 会话检查/恢复
```bash
cd /root/ctf/.share/platform/<平台名> && python3 scripts/session.py
```
脚本自动：读 README → 加载已存会话 → 校验 → 失效则重走认证链续期。

### 抓取题目（在比赛根目录下运行）
```bash
cd /root/ctf/<比赛名>
python3 platform/<平台名>/scripts/crawl.py            # 题目+附件
python3 platform/<平台名>/scripts/crawl.py --no-download
```
产物：`<类别>/<题目名>/{description.md, attachments/}` + `RECORD.md` 自动登记。
分类映射按平台可见标签：Web→web, Crypto→crypto, Osint→osint, Pwn→pwn,
Misc→misc, Reverse→reverse, AI→ai, 无法判定→misc/_staging。

### 容器管理（动态题）
```bash
cd /root/ctf/.share/platform/<平台名>
python3 scripts/instance.py list                  # 查看当前容器/地址/到期
python3 scripts/instance.py addr <challenge_id>  # 取地址（未启动则自动启动）
python3 scripts/instance.py delay <challenge_id> # 长时解题续期
python3 scripts/instance.py stop <challenge_id>  # 做完题释放名额（并发上限 2）
```
解题代理（子代理）打动态题时：`addr` 取地址 → 打题 → `stop` 释放；
刚启动的容器约 45s 内不能 stop，失败就稍后重试。

强制纪律（与 AGENTS.md「动态题容器生命周期纪律」同步，对未触发本 skill 的解题代理同样生效）：
- 启动前先 `list` 查槽位；`addr`/`start` 成功后立即在题目 steps.md 全局情报区登记 challenge_id、容器地址、启动时间（归属跟踪，供其它会话仲裁争用）。
- 拿到 flag 或明确放弃该题后必须 `stop` 并记入 steps.md，禁止依赖 rest_time 自然到期兜底；长时解题用 `delay` 续期。
- 槽位已满时按 steps.md 登记的归属协调：归属明确且正在打的容器不得停；已解出/已放弃的应 stop 回收；无法判断时询问用户。

### 提交 flag（仅用户明确要求时）
1. 查 `logs/` 确认该题未提交过。
2. 调用平台 submit 脚本（没有则按 README 端点现写，写完留档）。
3. 结果追加 `logs/`，更新比赛 `RECORD.md` 的提交时间列。

### 新平台接入
1. `platform/` 下建目录（结构见上），登记 `platforms.json`。
2. 探查：登录方式 → 认证载体（cookie/token/header）→ 题目列表/详情接口 →
   附件下载 →（需要时）提交接口。**每一步结论写入 README**。
3. 前端是 SPA 时优先逆向 bundle 找 API；主站有路径混淆时可参考
   `ctfplus/scripts/decrypt_endpoints.js` 的做法。
4. 探查中间产物（bundle、响应样本）放 `platform/.cache/<平台名>/`，不放比赛目录 `.cache/`。

## 当前已接入平台

- **ctfplus**（CTF+，主站 www.ctfplus.cn + 各比赛子域节点）：认证链三步走，
  节点只认 SessionStore cookie。完整文档见 `platform/ctfplus/README.md`。
  已登记比赛：0xGame2026（id 2098997646369755136，节点 0xgame2026.play.ctfplus.cn）。
