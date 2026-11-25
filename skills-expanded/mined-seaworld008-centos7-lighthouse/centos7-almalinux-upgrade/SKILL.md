---
name: centos7-almalinux-upgrade
license: MIT
description: 把老旧 CentOS 7 / CentOS 8（及 RHEL7/8 系）服务器原地升级到最新 AlmaLinux 10（经 ELevate/Leapp 7→8→9→10，CentOS 8 先用 almalinux-deploy 转换），并保证业务、容器、nginx、kubectl 等升级后照常工作。凡是用户提到 CentOS 7 / CentOS 停服 / EOL / 老系统升级 / 迁移到 AlmaLinux / Rocky / CentOS 继任者 / ELevate / leapp / 系统漏洞要升级系统、批量升级阿里云/华为云/AWS 上的 CentOS 服务器，都要使用本技能——即使用户没说"升级"而只说"系统太老了""换个新系统但业务不能停"。In-place upgrade CentOS 7 to AlmaLinux 10 safely, single server or whole fleet.
---

# CentOS 7 → AlmaLinux 10 原地升级

这是一次真实生产迁移（华为云跳板机，CentOS 7.7 → AlmaLinux 10.2，nginx/Docker/xxl-job/MySQL/NetBird/kubectl 全部保住）沉淀下来的流程。目标是**每台机器都能安全、可回滚、可验证地升上去**，同时能批量推进。

核心思路：**先摸清 → 快照兜底 → 每跳小步走（预检→升级→重启→对比基线→收尾）→ 最后现代化**。坑几乎都出在"非官方的东西"上（自编译程序、pip 包、第三方源、自打包 openssh、容器重启策略、VPN 访问路径），所以勘察阶段的价值最大。

## 什么时候不要原地升级

先看 `survey.sh` 的 BLOCKER。以下情况建议**新建 AlmaLinux 10 机器迁移业务**，而不是原地升级：
- 是 Kubernetes 节点（kubelet 在跑）——要当成**集群级变更**来做，按 `references/kubernetes.md`（已实测 kubeadm 1.21 + dockershim + flannel/ipvs 在 EL10 上可用，3m3w 集群约 6 小时）；也可以 drain 后换新节点
- 宿主机 rpm 装的数据库要跨多个大版本（MariaDB 5.5→10.11、PostgreSQL 9.2→16）且数据量大
- 非 x86_64、btrfs、系统盘极小且无法扩容
- CPU 不支持 x86-64-v3（AlmaLinux 10 标准版跑不了；可以只升到 9，或用 AlmaLinux 10 的 x86_64_v2 变体）
- 华为云 c9 规格（survey 报 HIGH）：EL10 内核在升级 initramfs 里挂死（测试机验证：与数据盘无关、黑名单 ata_piix 无效），只升到 9（升 9 本身没问题）；万一已经卡住按 `references/recovery.md` F 换盘改启动项
- 业务本身就是容器化的、配置都在 compose/k8s 里——新建机器重新部署往往比原地升级更快

拿不准时把判断依据告诉用户，让用户选。

## 工具包

技能目录 `scripts/` 下（全部在本机经 SSH 上传到目标机 `/root/os-upgrade-kit/` 执行）：

| 脚本 | 作用 |
|---|---|
| `remote.py` | 本机运行：从资产表(xlsx/csv)取凭据，SSH 执行命令/上传/下载/等待重启；开了 keepalive；不打印密码 |
| `survey.sh` | 只读勘察，末尾输出分级 RISK FLAGS（BLOCKER/HIGH/MEDIUM/INFO） |
| `backup.sh` | 备份配置 + 生成业务基线 `baseline.tsv`（服务/端口/容器/各域名 HTTP 码/kubectl） |
| `state.sh` / `verify.sh` | 生成当前状态 / 与基线对比，输出 FAIL/WARN |
| `post-audit.sh` | 升级完成后的只读体检：leapp 残留、logrotate 没被调度、EL7 专用 sysctl、Leapp 改坏的 `/etc/virc`、limits 写错、失效的服务链接、写死旧版本的源、本地程序缺库等，输出 HIGH/MEDIUM/INFO |
| `prep-el7.sh` | EL7 准备：`repos` 修源、`update` 到 7.9、`pipfix`、`inhibitors` |
| `convert-el8.sh` | 源系统是 CentOS 8 时：`prep` → `run`（官方 almalinux-deploy）→ `post`，转成 AlmaLinux 8 |
| `swap-openssh.sh` | 把自编译 openssh 换回官方包（带自动兜底） |
| `hop.sh` | 每一跳：`prep`→`pre`→`report`/`answer`→`up`→`reboot`→`post`；`tidy` 是升级后的小修（post 末尾自动执行，已升级完的机器可单独跑） |
| `nginx-static-build.sh` | 自编译 nginx 同版本静态重编（过渡期一路可用） |
| `fleet_summary.py` | 本机运行：汇总多台 survey 结果 → A/B/C/D 分类、VPN/EL8 标记、金丝雀与分批建议（`--groups` 让同业务主备不同批） |
| `finalize.sh` | EL10 收尾：compose 包装、kubectl 对齐集群、helm、postfix lmdb、nginx.org 源、cgroup v1 兼容、SysV 包装、legacy iptables 模块、redis→valkey、手工启动进程转 systemd 服务、`oom-policy`（EL9+ 默认 OOMPolicy=stop） |
| `mysql-backup.sh` | 收尾后可选：替换老的 mysqldump cron 脚本——宿主机/容器 MySQL 逐库备份 + 校验 + `--check`/`--metrics` 监控 |
| `rescue-grubenv.sh` | 救援：在同可用区的救援机上（可作为 user data，无需登录）把故障机系统盘的默认启动项改回旧内核，用于卡在升级 initramfs、抢不到 GRUB 的情况 |
| `known-hosts-fill.sh` | CI/发布机到 EL10 后：经已信任的 ssh 连接读取目标机主机公钥，补齐 known_hosts 缺的类型（解决 `Host key verification failed`） |
| `k8s.sh` | K8s 节点：`backup`（etcd 快照/配置/二进制/pod 列表，自动 `pin` 版本）、`stop`、`nfs-off`/`nfs-on`、`nm`、`fix`、`check`（含 flannel.1 IPv6 丢包提示）、`pods`（与升级前对比）、`jvm-maxram`（cgroup v2 下老 JDK 的 OOM） |

本机在 Windows Git Bash 下调用时，`remote.py` 已自动处理 MSYS 把 `/root/...` 改写成 `C:/Program Files/Git/root/...` 的问题。

常用：
```bash
export FLEET_INVENTORY="/path/to/servers.xlsx"   # 列: name, host, port, username, password（含密码，切勿提交到仓库）
S=<技能目录>/scripts
python $S/remote.py HOST put $S /root/os-upgrade-kit
python $S/remote.py HOST run "bash /root/os-upgrade-kit/survey.sh > /root/os-upgrade-kit/survey.txt; sed -n '/RISK FLAGS/,\$p' /root/os-upgrade-kit/survey.txt"
python $S/remote.py HOST wait-ssh --timeout 3600
```

## 流程

### 阶段 0：开工前必须和用户确认的事（缺一不可）

这些是"用户的决定"，不要替用户假设：
1. **云快照/整机备份已做**（系统盘+数据盘）。这是唯一可靠的回滚手段，Claude 在机器内部做不了。
2. **停机窗口**：每跳一次重启，全程约 2~4 小时（多数时间在下载包，镜像源快慢决定）；业务会中断数次。
3. **带外控制台可用**：阿里云 VNC / 华为云 VNC / AWS EC2 Serial Console（各自前置条件见 `references/cloud-providers.md`）。升级卡在 initramfs 时只能从这里救。
4. **访问路径**：你（本机）是怎么连到这台机器的？如果走的 VPN/隧道就运行在这台机器上（survey 会报 BLOCKER），重启和容器操作要格外小心——我们的真实事故就是 `docker stop` 了全部容器导致 NetBird 路由容器开机不自启，整个 VPC 失联。
5. **哪些东西已经没用**：勘察完把清单给用户，让用户确认哪些组件/站点可以下线（例如 PHP、旧站点）。删之前说清楚影响面（比如"删 PHP 会导致 xxx 站点 404"），由用户拍板。

### 阶段 1：勘察 + 备份 + 基线

1. 上传工具包，跑 `survey.sh`，逐条看 RISK FLAGS，结合 `references/app-compat.md` 给每条定处理方案。
2. 跑 `backup.sh`（默认放非系统盘如 /data），记下 `BACKUP_DIR`。`baseline.tsv` 是后面每跳对比的依据——升级前就已经异常的项目（如 502）要在报告里注明"升级前即如此"，免得事后说不清。
3. 把勘察结论、处理方案、需要用户决定的事一次性告诉用户（见阶段 0）。

### 阶段 2：EL7 准备

```bash
bash prep-el7.sh repos <MIRROR>      # 国内推荐 https://mirrors.aliyun.com；阿里云内网 http://mirrors.cloud.aliyuncs.com；海外 upstream
bash prep-el7.sh update              # 到 7.9；出现 Failed 的包基本是 pip 冲突
bash prep-el7.sh pipfix
bash prep-el7.sh inhibitors
bash swap-openssh.sh                 # 仅当 survey 报 openssh 非官方包；完成后用【新连接】验证
```
自编译 nginx 等依赖 EL7 库的程序：EL7 上就用 `nginx-static-build.sh` 静态重编（或接受过渡期停用，最后装官方包）。
宿主机数据库：先逻辑备份。

**源系统是 CentOS Linux 8 / CentOS Stream 8 时**（survey 会报 BLOCKER）：ELevate 不支持以它为源，跳过上面的 EL7 准备，先做同版本转换，然后从阶段 3 的 8→9 开始：
```bash
bash convert-el8.sh prep <MIRROR>                    # 修源（vault、EPEL8）、pip 冲突、多余 kernel-devel
bash convert-el8.sh update                           # 升到 8.5（almalinux-deploy 要求 ≥8.4）
bash convert-el8.sh run  <MIRROR> <almalinux-deploy.sh>   # 官方 almalinux-deploy：-d 允许降级，-l 用镜像
bash hop.sh reboot && python remote.py HOST wait-ssh   # 重启进入 AlmaLinux 内核
bash convert-el8.sh post                             # 删除非 AlmaLinux 内核，dnf upgrade
```
国内服务器通常访问不了 GitHub raw，需要先在本机下载 `almalinux-deploy.sh` 再上传。

### 阶段 3：每一跳（7→8、8→9、9→10 各做一遍）

```bash
bash hop.sh prep <MIRROR>     # 装本跳 ELevate、目标源和 docker-ce/epel 厂商源改镜像、关掉 test/nightly 段、pip 清理、探测可达
bash hop.sh pre               # 后台 preupgrade 并等待 → 自动 report
bash hop.sh answer            # 已知安全问题自动回答；其余阻断项按 report 里的修复命令处理，再 pre，直到 0 阻断
bash hop.sh report            # 重点看"将被删除的包"和"关键包去向"——有业务依赖的要先想办法
bash hop.sh up                # 后台下载+生成升级环境
bash hop.sh reboot [额外要停的容器名]   # 只停 restart=always 的有状态容器；VPN 容器和 unless-stopped 容器不碰；业务方说"别动"就用 --no-stop
python remote.py HOST wait-ssh --timeout 3600   # 本机等；超时 → 控制台，见 references/recovery.md
bash hop.sh post <MIRROR>     # 检查失败标记、清 leapp/旧内核/残留源、dnf upgrade
bash verify.sh <BACKUP_DIR>   # FAIL 必须处理；WARN 判断是否预期
```
每跳之后修复业务问题再进下一跳，不要攒到最后。各跳特有的阻断项和处理见 `references/pitfalls.md` 的"按跳分类"。

**长任务一律后台跑**：脚本已用 `systemd-run` 执行 leapp/dnf，SSH 断了不影响；你只管轮询。自己写命令时也照此办理，不要让一个 SSH 会话挂几十分钟。

### 阶段 4：EL10 收尾与现代化

按用户需要选用 `finalize.sh` 子命令，并参考 `references/app-compat.md`：
- 自编译 nginx → nginx.org 官方 stable 包（`ssl on;` 改 `listen 443 ssl;`、TLS1.2/1.3、证书放 /etc/nginx/ssl、systemd 自启）
- `docker-compose` v1 → 包装到 compose v2；cgroup v1 老应用加 shim
- kubectl → pkgs.k8s.io 源、与集群同 minor；helm → 最新 v3
- postfix hash → lmdb；rc.local 里的启动项改成 systemd unit
- 设了内存上限的 unit → `finalize.sh oom-policy`（否则 OOM 一次整个服务就停了、不会再起来）
- 数据库备份：确认 cron 备份脚本升级后真的在产出完整文件（结尾有 `-- Dump completed`），不行就换 `mysql-backup.sh`
- `dnf -y upgrade` 全量更新，确认 `dnf check-update` 为空
- 跑 `post-audit.sh` 做升级后体检（`verify.sh` 只比业务基线，发现不了"日志不轮转"这类过几天才出问题的项）：能自动修的 `hop.sh tidy` 已处理，其余按 `references/pitfalls.md` 第 6 节处理；升级前就坏的项（如云厂商插件）在报告里注明。用旧版本技能升级完的机器也可以补跑 `post-audit.sh` + `hop.sh tidy`
- **最后再重启一次做开机自启测试**，跑 `verify.sh`，全部服务自己起来才算完成

### 阶段 5：交付报告

用 `assets/report-template.md` 的结构写给用户：版本对比、业务对比表（升级前/后）、做过的兼容性改动、遗留与需要用户处理的事（证书到期、没修好的云厂商插件等）、备份位置。批量场景同时更新资产跟踪表（`assets/fleet-tracker.csv`）。

### 阶段 6：沉淀经验（回馈技能仓库）

这个技能靠真实执行不断进化，项目地址：https://github.com/seaworld008/centos7-lighthouse 。每次真实执行之后（成功、失败、回滚都算）：
- 按仓库的 `field-reports/TEMPLATE.md` 写一份**脱敏**实战报告（不写真实 IP、域名、主机名、凭据）。
- 新问题写进 `references/pitfalls.md`；能自动检测的加进 `survey.sh`；能自动处理的改进脚本。
- 如果当前工作目录就是该仓库，按其 `AGENTS.md` 执行；否则把报告交给用户，建议提交 issue 或 PR。

## 关键原则（每条都对应一次真实踩坑）

- **重启前绝不 `docker stop $(docker ps -q)`**：`unless-stopped` 的容器被手动停过就不会自启；VPN 容器停了你就失联。用 `hop.sh reboot`。
- **pip 装进系统 site-packages 的东西必须在每跳前挪走**：它们和 rpm 文件冲突时，升级会在 initramfs 里半途失败，系统卡在紧急模式且处于"半升级"状态。
- **不认识的、非官方的东西都要先处理**：自编译 openssh、自编译 nginx、第三方 repo、`mysql-community-libs` 替换了 `mariadb-libs`……leapp 不管它们，升级后它们就坏。
- **国内用国内镜像，并关掉厂商源的 test/nightly 段**：mirrorlist/metalink 常年慢或超时，docker nightly 源超时会直接让 leapp 失败。华为云镜像会 429 限流，阿里云最稳。
- **`pkill -f` / `pgrep -f` 的模式不能出现在你自己的命令行里**，否则把自己的 SSH 会话杀掉（我们中招两次）。用 PID、用脚本文件、或 `[l]eapp` 这种写法。
- **每跳都对比基线**：业务问题当跳发现当跳修，比如 cgroup v2 让 Yearning 崩、docker-compose v1 失效。
- **改变业务行为的决定交给用户**：删组件、下线站点、关 TLS1.0/1.1、换大版本数据库。

## 参考文档（按需读取）

- `references/pitfalls.md` — 全部坑：现象 → 原因 → 处理，按跳分类 + 通用。遇到报错先查这里。
- `references/app-compat.md` — 各类应用跨 EL7→EL10 的兼容处理：nginx、Docker/compose/cgroup v2、Java、Python、PHP、数据库、postfix、网络、SSH、kubectl/helm、SysV、TLS 加密策略。
- `references/cloud-providers.md` — 阿里云/华为云/AWS 差异：快照、带外控制台前置条件、镜像源、云厂商 agent、cloud-init。
- `references/recovery.md` — 卡在 initramfs 紧急模式、开机失联、半升级状态时怎么救（含 VNC 操作技巧）。
- `references/fleet.md` — 几十上百台批量推进：资产表、并行勘察、分类、金丝雀、分批、记录。
- `references/kubernetes.md` — K8s 节点原地升级：开工前必须弄清的事（访问路径/控制面入口/etcd/存储）、兼容性结论、推荐顺序、踩过的坑、恢复检查清单。
