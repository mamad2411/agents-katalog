---
name: sec-watch
description: >-
  监控、告警和恢复：每 10 分钟服务器巡检（网站状态、容器、数据库、磁盘、内存、证书、备份新不新、定时任务有没有跑）、
  每次 SSH 登录成功推送、日志告警（5xx、进程池满）、外部可用性监控（整台机器挂了时）、告警群和业务群分开、
  备份用公钥加密传异地 + 定期恢复演练、封禁和安全事件进日报。
  新服务器上线、想知道“出事了我多久能知道”、做备份、上次出事很晚才发现时用。
  附 scripts/ssh-login-alert.sh、scripts/backup-encrypt.sh。
  触发词：监控、告警、巡检、健康检查、SSH 登录提醒、备份、加密备份、恢复演练、证书到期、uptime、可用性监控、
  monitoring, alerting, health check, ssh login alert, encrypted backup, restore drill.
---

# sec-watch：监控和恢复

**一句话：出事了要在几分钟内知道，数据没了要能在一小时内恢复。两件事都要真的演练过。**

## 1. 巡检（服务器自己跑，每 10 分钟）

查这些，有问题推到**告警群**：

- 每个域名打开是不是想要的状态码（不带 Key 调 API 应该是 401，这种也算正常）。**连续 3 次失败才报**，偶尔一次网络超时不报。
- 容器 / 进程在不在、意外重启了几次；数据库能不能 `SELECT 1`。
- 磁盘、内存、负载；HTTPS 证书还剩几天（< 14 天报）。
- **最近 N 小时有没有成功的备份**（备份脚本自己也要在失败时报，但它可能根本没跑）。
- 定时任务有没有按时跑（每个任务跑完写一个时间戳，巡检看时间戳有没有过期）。
- 同一个问题 6 小时内不重复报；**恢复了也报一条**。

告警群和业务群（订单、收款）分开。告警多到没人看，等于没有告警：能进日报的就别实时推（自动封了几个 IP、扫描次数），实时推的只留需要人马上处理的。

## 2. 整台机器挂了：外部监控

服务器自己的巡检，在服务器挂了的时候发不出来。再加一个外部的可用性监控（UptimeRobot、Better Stack、Grafana Cloud 的 Synthetic、云厂商的拨测，免费额度都够），**至少两个地区**，每 5 分钟打一次首页和一个关键接口，超时 10 秒。

## 3. SSH 登录推送

**每次 SSH 登录成功都推一条消息**：哪个用户、从哪个 IP、用的哪把钥匙。不是你本人登录的，就是出事了。这是发现入侵最快、最便宜的办法。

```bash
sudo install -m 755 scripts/ssh-login-alert.sh /usr/local/sbin/ssh-login-alert
sudo tee /etc/ssh-login-alert.env >/dev/null <<'EOF'
WEBHOOK_URL=https://hooks.slack.com/services/...   # 告警群机器人地址
FORMAT=slack                                        # slack / lark / discord
IGNORE_IPS="10. 192.168."                           # 内网自动连接不推（前缀匹配，空格分隔）
IGNORE_KEYS=""                                      # 自动化用的钥匙指纹不推（SHA256:...）
EOF
sudo chmod 600 /etc/ssh-login-alert.env
echo '*/2 * * * * root /usr/local/sbin/ssh-login-alert' | sudo tee /etc/cron.d/ssh-login-alert
```

## 4. 日志告警

- nginx：5xx 突然变多；错误日志里新出现的错误（去掉扫描器造成的噪音）。
- 应用：进程池满（PHP-FPM `max_children`、Node 事件循环阻塞）、进程崩溃、语法错误（部署坏了）。
- 日志推到外部日志平台（Grafana Cloud、Better Stack 等有免费额度）之前**先打码参数**（`sec-secrets` §2）。

## 5. 备份

- 频率按“最多能接受丢多少数据”定（比如每 2 小时）；本机留 14 天 + 异地一份。
- **用公钥加密后再传异地**：服务器上只有公钥，私钥只在你自己的电脑上（另存一份到加密 U 盘或密码管理器）。服务器被攻破，攻击者也解不开历史备份。
  ```bash
  sudo install -m 755 scripts/backup-encrypt.sh /usr/local/sbin/backup-encrypt
  # 生成证书和私钥见 sec-secrets §4，只把 backup-cert.pem 放到服务器
  sudo tee /etc/backup-encrypt.env >/dev/null <<'EOF'
  DUMP_CMD="mysqldump --single-transaction --routines --all-databases"   # 或 pg_dumpall
  CERT=/etc/backup/backup-cert.pem
  OUT_DIR=/var/backups/app
  KEEP_DAYS=14
  RCLONE_REMOTE=offsite:my-bucket/backups      # 可选：rclone 配好的异地存储（S3 / R2 / B2 都行）
  WEBHOOK_URL=https://hooks.slack.com/services/...
  FORMAT=slack
  EOF
  sudo chmod 600 /etc/backup-encrypt.env
  echo '30 */2 * * * root /usr/local/sbin/backup-encrypt' | sudo tee /etc/cron.d/backup-encrypt
  ```
- 数据库密码走环境变量或 `~/.my.cnf`（600），**不写在命令行上**（`ps` 能看到）。
- 备份账号只读。
- 钥匙文件（加密字段用的主钥匙）的副本单独放，不和数据库导出放一个目录。

## 6. 恢复演练

**没恢复过的备份不算备份。** 每次大改之前、以及每季度一次：

1. 从异地下载最新的一份；
2. 在你自己的电脑上解密（`openssl cms -decrypt …`，见 `sec-secrets` §4）；
3. 导入一个临时数据库（`docker run --rm -e MYSQL_ROOT_PASSWORD=… mysql:8`）；
4. 抽几张关键表对行数、最近一条记录的时间，和线上一致；
5. 记下花了多久。写成一页“出事了怎么办”放在仓库里（服务器上也放一份）。

## 7. 日报

每天一条：昨天的请求数、错误数、自动封了多少个 IP、SSH 登录了几次、备份是否都成功、证书剩几天、磁盘用了多少。异常的标红，正常的一行带过。

## 改完的检查清单

- [ ] 停掉网站容器，10 分钟内收到告警，恢复后收到恢复通知
- [ ] 关掉整台机器，外部监控报警
- [ ] 用一台新电脑 SSH 登录，收到推送
- [ ] 让备份失败一次（比如改错数据库密码），收到告警
- [ ] 最近一次恢复演练在 3 个月以内，并记下了用时
