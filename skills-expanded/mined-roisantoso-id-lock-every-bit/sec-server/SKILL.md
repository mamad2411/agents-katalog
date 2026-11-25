---
name: sec-server
description: >-
  服务器加固（Linux 云服务器 / VPS，Ubuntu / Debian 为主）：云账号和云助手（泄露一把 AccessKey 就能绕过 SSH 给所有机器下命令）、SSH 只认密钥、禁止 root、公网只留 22/80/443、
  云防火墙 + 系统防火墙两层、Docker 发布的端口绕过 ufw 的坑、自动安全更新真的在装、内核更新要重启、
  数据库不上公网（四层访问控制 + TLS）、清理来历不明的登录公钥、机器之间用受限密钥。
  新开服务器、上线前、怀疑被入侵、每季度复查时用。附只读体检脚本 scripts/server-audit.sh。
  触发词：服务器加固、服务器安全、VPS 安全、SSH 安全、防火墙、ufw、fail2ban、开放端口、Docker 端口、
  自动更新、unattended-upgrades、数据库暴露、被入侵了吗、server hardening, ssh hardening, firewall, open ports, docker ufw bypass.
---

# sec-server：服务器加固

**一句话：云账号比 SSH 更要紧；公网只留 22 / 80 / 443，SSH 只认密钥，数据库永远不对公网，安全更新真的在装。**

相关：挡爬虫和扫描看 `sec-edge`，密钥和备份看 `sec-secrets`，告警看 `sec-watch`。

## 0. 先体检（只读）

```bash
sudo bash scripts/server-audit.sh            # 整机体检
sudo bash scripts/server-audit.sh /srv/app   # 顺带查这个目录里的 .env / 钥匙文件权限
```

输出每行一个 `OK` / `WARN` / `FAIL`，不改任何东西。先处理 FAIL，再看 WARN。新机器第一天跑一次，之后每季度跑一次。

## 1. 云账号和云助手：比 SSH 更大的那扇门

云服务器上通常预装了云厂商的“助手”客户端（阿里云云助手、腾讯云自动化助手 `tat_agent`、AWS SSM Agent），**默认以 root 运行**。谁能调你云账号的 API，谁就能不经 SSH、不经防火墙，给你所有的机器下发命令、传文件。这类攻击根本不碰你的 SSH：泄露一把 AccessKey，攻击者从控制台发一条命令，整批机器同一分钟被种上后门。你把 SSH 守得再严，这扇门开着也没用。

- **主账号只管账单和权限**：开 MFA（两步验证），不给主账号建 AccessKey。日常操作用子账号（阿里云 RAM / 腾讯云 CAM / AWS IAM），子账号也开 MFA。
- **AccessKey 能不建就不建**。必须建的：只给它要用的那几个接口，限制来源 IP，定期换，绝不进代码仓库（`sec-secrets`）。
- **所有 AccessKey 和日常账号的策略里，显式禁止“下发命令”和“传文件”**：阿里云 `ecs:RunCommand`、`ecs:InvokeCommand`、`ecs:SendFile`，AWS `ssm:SendCommand`；腾讯云自动化助手照它的访问管理文档写同样的禁止规则。真要用的时候，只给一个单独的、开了 MFA 的账号，并把执行用户限制成普通用户而不是 root。
- **用不到助手就停掉客户端**（按云厂商文档停用或卸载）。注意控制台的“重置密码”“免密登录”这类功能可能依赖它，停之前想好。
- **打开操作审计**（阿里云 ActionTrail、腾讯云 CloudAudit、AWS CloudTrail），对“下发命令”“创建 AccessKey”“改安全组”“控制台登录”设告警，推到告警群。
- 云厂商发来“AccessKey 疑似泄露”的通知，当成事故处理：先禁用这把 Key，再看它最近调了什么。
- 体检脚本会列出机器上在跑的助手客户端：`ps -ef | grep -E 'aliyun-service|tat_agent|amazon-ssm-agent'`。

## 2. SSH

写一个单独的配置文件，文件名用 `00-` 开头：

```
# /etc/ssh/sshd_config.d/00-hardening.conf
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
MaxAuthTries 3
LoginGraceTime 20
X11Forwarding no
AllowUsers deploy            # 换成你的登录用户
```

- **为什么是 `00-`**：sshd 对同一个配置项只认第一次出现的值。云镜像常带一个 `50-cloud-init.conf` 写着 `PasswordAuthentication yes`，你写在主配置文件末尾的 `no` 不生效。
- 改完：`sudo sshd -t && sudo systemctl reload ssh`。**旧窗口别关**，新开一个窗口登录成功再关。
- 看最终生效的值：`sudo sshd -T | grep -Ei 'passwordauth|permitroot|kbdinteractive|maxauthtries'`。
- **每把登录公钥都要认得出是谁的**：`ssh-keygen -lf ~/.ssh/authorized_keys`。我们在一台机器上查出过两把没人认识的公钥：是云厂商控制台里绑定的密钥，重装系统时会被重新写回去。删掉之后，控制台里也要解绑。
- 机器之间的自动连接（巡检、备份）用受限密钥，只能从一个 IP 来、只能执行一个命令：
  ```
  from="10.0.0.5",command="/usr/local/sbin/status-only",no-pty,no-port-forwarding,no-agent-forwarding ssh-ed25519 AAAA... monitor
  ```
- `fail2ban` 开 sshd 规则；ufw 对 22 用 `limit`（30 秒内 6 次新连接就拒）。部署脚本连很多次的话，本机 `~/.ssh/config` 开 `ControlMaster auto` 复用连接，免得把自己限住。
- 每次 SSH 登录成功都推送到告警群（`sec-watch`）。这是发现入侵最快的办法。

## 3. 端口和防火墙

- 公网只开 22、80、443（自建收信再加 25）。**两层都要设**：云控制台的安全组 / 防火墙 + 系统里的 ufw。
  ```bash
  sudo ufw default deny incoming
  sudo ufw limit 22/tcp
  sudo ufw allow 80,443/tcp
  sudo ufw enable
  ```
- 看谁在监听公网：`sudo ss -tlnp`，监听在 `0.0.0.0` / `[::]` / 公网 IP 上的，每个都要说得出为什么。
- **Docker 发布的端口不走 ufw。** `ports: ["3306:3306"]` 会让数据库直接对公网开放，ufw 规则拦不住（Docker 自己往 iptables 里插规则，排在 ufw 前面）。办法按顺序：
  1. 能不发布就不发布：同一个 compose 网络里的容器用服务名直接互通。
  2. 必须发布就只绑本机或内网：`"127.0.0.1:3306:3306"`、`"10.0.0.5:3306:3306"`。
  3. 还要限制来源，就在 `DOCKER-USER` 链里拦，并做成开机自动加的 systemd 服务：
     ```bash
     # 只允许 10.0.0.5 连 Docker 发布的 3306，其余丢掉
     iptables -I DOCKER-USER -p tcp -m conntrack --ctorigdstport 3306 --ctdir ORIGINAL ! -s 10.0.0.5 -j DROP
     ```
- 有的云厂商的轻量服务器，控制台防火墙**连内网流量也拦**。内网互相连不上，先去控制台看。
- IPv6：确认 `/etc/default/ufw` 里 `IPV6=yes`；服务监听 `[::]` 时 IPv6 也要有规则。

## 4. 自动安全更新

- **装了 `unattended-upgrades` 不等于在装更新。** 有的云镜像把 `/etc/apt/apt.conf.d/50unattended-upgrades` 里 `-security` 那一行注释掉了，结果什么都不装。我们两台服务器各积压了 150 多个更新。
  ```bash
  grep -n 'security' /etc/apt/apt.conf.d/50unattended-upgrades   # 那一行前面不能有 //
  cat /etc/apt/apt.conf.d/20auto-upgrades                        # 两个值都要是 "1"
  sudo unattended-upgrade --dry-run -d 2>&1 | tail -20            # 看它这次会装什么
  ```
- 内核更新要重启才生效：`/var/run/reboot-required` 存在就排时间重启，巡检里提醒。
- Docker 官方源装的 `docker-ce` 不在安全更新范围里，单独定期升级。
- 镜像钉版本号（`nginx:1.27-alpine`，不用 `latest`），定期主动升级，升级前看更新说明。

## 5. 数据库

- **永远不对公网开放**，最好单独一台机器，四层都要有：
  1. 云防火墙只放行应用服务器的内网 IP；
  2. 主机防火墙（Docker 的话是 `DOCKER-USER`）也只放行这个 IP；
  3. 数据库账号限定来源：`CREATE USER 'app'@'10.0.0.5' ... REQUIRE SSL;`；
  4. 连接走 TLS，客户端校验 CA。
- 账号分开：应用账号只能动自己的库；备份账号只读；root 只能在数据库机器本机登录。
- 自己用的时候走 SSH 隧道：`ssh -L 3307:127.0.0.1:3306 db-host`，不要为了方便临时开公网端口。

## 6. Web 服务器和应用的基本设置

- nginx：`server_tokens off`；未知域名的 `default_server` 直接 `return 444;`（拿 IP 直接扫的扫描器什么站都看不到）。扫描路径、限流、源站只认 CDN 见 `sec-edge`。
- `.env` 权限 `600`，不进 git，部署时不被覆盖（`rsync --exclude .env --exclude data/`）。
- 数据目录、钥匙文件目录 `700`，只有运行用户能读。
- PHP：`expose_php = Off`、`display_errors = Off`；Node / Python：生产环境不把异常栈返回给浏览器。
- 能不以 root 跑应用就不用 root；容器里也一样。
- 定时任务写在代码仓库里（一个任务一个文件，开头写时间、做什么、为什么），部署时统一装到 `/etc/cron.d/`，服务器上多出来的删掉。服务器上就不会有“没人知道是谁加的 cron”。

## 7. 怀疑被入侵时先看这些

```bash
last -a | head -30                                   # 最近谁登录过、从哪来
sudo journalctl -u ssh --since "7 days ago" | grep Accepted
for u in $(cut -d: -f1 /etc/passwd); do sudo crontab -l -u "$u" 2>/dev/null | sed "s/^/$u: /"; done
ls -la /etc/cron.d /etc/cron.*/ /var/spool/cron 2>/dev/null
sudo find / -xdev -newer /etc/hostname -type f -perm -u+x 2>/dev/null | grep -v -E '^/(proc|sys|var/lib/docker)' | head -50
sudo ss -tunp | grep ESTAB                           # 有没有奇怪的外连
cat ~/.ssh/authorized_keys /root/.ssh/authorized_keys 2>/dev/null
```

再去云控制台的操作审计里看最近有没有“下发命令”“创建 AccessKey”的记录——攻击者可能根本没走 SSH。

真有问题：先断网（云控制台改安全组），保留现场（快照），从干净的镜像重装，所有密钥全部换掉（`sec-secrets` 第 5 节），再从加密备份恢复。

## 改完的检查清单

- [ ] `server-audit.sh` 没有 FAIL
- [ ] 云主账号开了 MFA、没有 AccessKey；所有 Key 都禁止下发命令；操作审计对“下发命令”有告警
- [ ] 密码登录、root 登录都关了，新窗口用密钥能登录
- [ ] `ss -tlnp` 公网上只剩 22 / 80 / 443
- [ ] 没有 Docker 端口发布在 `0.0.0.0`，或者有 `DOCKER-USER` 规则
- [ ] `unattended-upgrade --dry-run` 能看到安全更新
- [ ] 数据库从公网连不上（从另一台机器 `nc -vz 公网IP 3306` 应该失败）
- [ ] 每把 authorized_keys 都认得出是谁的
- [ ] SSH 登录成功会推送告警
