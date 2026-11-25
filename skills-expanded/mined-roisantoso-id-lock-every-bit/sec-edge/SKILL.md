---
name: sec-edge
description: >-
  挡爬虫、扫描器和撞库（网站入口这一层）：CDN（Cloudflare 等）在前、源站只接受 CDN 来的连接、真实 IP 只信 CDN 的头、
  扫描路径（.env、.git、wp-login、备份文件）直接断开、按 IP 限流和并发上限、自动拉黑（fail2ban / 打分）、
  搜索引擎爬虫放行要验证（不能只看 UA）、公开恶意名单、登录限速和人机验证、安全响应头。
  网站上线前、被爬虫打满 CPU / PHP 进程、日志里全是扫描、想加 WAF 规则时用。
  附 nginx / fail2ban 模板和外部体检脚本 scripts/exposure-check.sh。
  触发词：爬虫、扫描、被扫、WAF、Cloudflare、限流、rate limit、封 IP、自动拉黑、fail2ban、源站 IP 泄露、
  真实 IP、X-Forwarded-For、安全头、CSP、HSTS、撞库、bot defense, scanner, rate limiting, origin lockdown, security headers.
---

# sec-edge：挡爬虫和扫描

**一句话：坏请求越早拦越便宜。CDN 拦一层，nginx 拦一层，应用里只处理剩下的人。**

只要有公网 IP，扫描器每天都会来：试 `/.env`、`/.git/config`、`/wp-login.php`、`/backup.zip`、`/phpmyadmin`，猜后台地址、撞登录。现在很多扫描是程序自动跑的，会换浏览器标识、乱猜路径、速度很快。一个 IP 同时并发几十个请求，就能把 PHP / Node 的进程池占满，网站对正常人也打不开了——我们就是这样被打满过一次。

分层（从外到里）：

| 层 | 拦什么 | 本文 |
|---|---|---|
| CDN | 机房流量、扫描路径、登录狂刷、按国家限制后台 | §1 |
| 源站锁定 | 绕过 CDN 直接打服务器 IP | §2 |
| 真实 IP | 伪造 `X-Forwarded-For` 绕过限流 / 封禁 | §3 |
| nginx | 扫描路径直接断开、限流、并发上限 | §4 §5 |
| 自动拉黑 | 扫了几次、刷了很多次的 IP | §6 §7 |
| 应用 | 撞库、发验证码狂刷、批量注册 | §8 |
| 浏览器 | XSS、点击劫持、被嵌入 | §9 |

## 1. CDN（以 Cloudflare 为例，别家同理）

- DNS 开代理（橙色云），SSL 选 **Full (strict)**，开 Always Use HTTPS，最低 TLS 1.2。
- 自定义 WAF 规则（免费版条数有限，合并着写）：
  - 来自机房 / 云厂商网络（按 ASN）的访问，网页先过质询；
  - 后台域名只允许你所在的几个国家，其它先过质询；
  - 扫描路径直接 Block；
  - 登录、发验证码的 POST 限速。
- **付款回调、短信回调、机器上报这类“服务器对服务器”的地址要单独放行**（Skip 规则）。Bot Fight Mode 这类“一键防机器人”会把支付网关的回调也当机器人拦掉，钱付了单子不到账。要么关掉它用自定义规则，要么确认回调路径不受影响。
- 证书验证路径 `/.well-known/acme-challenge/` 不能被国家限制挡住（证书机构的验证服务器在美国、欧洲）。
- **规则写成脚本 + API 同步，放进代码仓库**，别在后台手点：改了什么、为什么改，都能回溯。

## 2. 源站只接受 CDN 来的连接

开了 CDN，攻击者照样能找到你的源站 IP（历史 DNS 记录、证书透明日志、邮件头），然后绕过 CDN 直接打。所以源站要拒绝一切不是 CDN 来的连接。模板 `templates/nginx/cdn-only.conf`：

```nginx
# 按原始连接地址判断（realip 替换之前的地址），伪造请求头没用
geo $realip_remote_addr $from_cdn {
    default 0;
    127.0.0.1 1;
    include /etc/nginx/cdn-ips.conf;   # 每行 "173.245.48.0/20 1;"，从 https://www.cloudflare.com/ips/ 生成
}
server {
    ...
    if ($from_cdn = 0) { return 444; }
}
```

- **以后要关掉 CDN（改回只解析）之前，必须先去掉这条**，否则网站直接打不开。在配置旁边写注释提醒。
- CDN 的 IP 段会变，用定时任务每月更新一次 `cdn-ips.conf`。
- 也可以在云防火墙只放行 CDN 的 IP 段到 443，但 Docker 发布的端口不走系统防火墙（见 `sec-server`），nginx 这一层更可靠。

## 3. 真实 IP：只信 CDN 给的那个头

不配好这个，你的限流、封禁、登录失败计数、日志统计全都是错的：看到的全是 CDN 的 IP；更糟的是应用如果读 `X-Forwarded-For` 的第一个值，攻击者随手伪造一个就绕过了所有按 IP 的限制。

```nginx
set_real_ip_from 173.245.48.0/20;   # ……CDN 的全部 IP 段
real_ip_header CF-Connecting-IP;
```

应用里只用服务器给的 `REMOTE_ADDR`（nginx 已经替换成真实 IP），不要自己去解析 `X-Forwarded-For`。

## 4. 扫描路径直接断开

你的网站上根本没有 `.env`、`.git`、`wp-login.php`，正常人不会访问这些地址。直接 `444`（不回任何内容就断开），不进 PHP / Node，省资源，也不给扫描器任何信息。模板 `templates/nginx/probes.conf`，放在 `server {}` 里最前面。

- 记日志（自动拉黑要数次数）。
- 你自己的网站如果真用到其中某个路径（比如真的用 WordPress），把那一项从正则里删掉。

## 5. 限流和并发上限

模板 `templates/nginx/limits.conf`：

- `limit_req`：每个 IP 每秒几个请求 + burst；登录、发验证码、搜索这类贵的接口单独更严。
- **`limit_conn` 限制每个 IP 同时占几个动态请求**（PHP / Node）。这条最容易漏，也最管用：限流挡不住“慢而多”的并发，并发上限能。
- 上传接口单独设 `client_max_body_size`，其余都小（几十 KB）。
- 返回 `429`，自动拉黑会数它。

## 6. 自动拉黑

最简单可靠：fail2ban 读 nginx 访问日志。模板 `templates/fail2ban/`：

- 扫描路径（状态 444）10 分钟内 ≥ 3 次 → 封 7 天；
- 10 分钟内被限流（429）很多次 → 封 1 天。
- 装好先用样例日志测正则：`fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nginx-probe.conf`。
- **开了 CDN 时别用默认的 iptables 封**：连过来的地址是 CDN 的，会把所有人一起封掉。改成在 nginx 里 `deny`，或者用 CDN 的 API 封（`jail.local` 末尾有写法）。

进阶（我们现在用的）：给每个 IP 打分，分够了才封，误伤少：

| 行为（同一个 IP，一段时间内） | 加分 |
|---|---|
| 访问敏感文件（`.env`、`.git`、私钥、云密钥、数据库备份、管理面板），每个不同的地址 | 高 |
| 访问很多个不存在的地址（404 的种类多） | 中 |
| 请求里报错（4xx / 5xx）占大多数 | 中 |
| 被限流很多次 | 中 |
| 扫描工具的标识（`python-requests`、`Go-http-client`、`curl`、`nuclei`、`sqlmap`……）且有报错 | 低 |
| 同一个 IP 换着用好几种浏览器标识 | 中 |
| 来自机房 / 云厂商网络、在公开恶意名单里 | 总分乘一个系数 |

**具体分值和阈值自己定、别公开**——公开了，攻击者会刚好卡在线下面。

不封的：

- **搜索引擎和 AI 搜索的爬虫**——封了别人就搜不到你。但**不能只看浏览器标识放行**，标识谁都能填成 Googlebot。要验证：反查域名 + 正查回来一致（脚本见下），或者用官方公布的 IP 段。
  ```bash
  ip=66.249.66.1
  name=$(dig +short -x "$ip" | sed 's/\.$//')            # crawl-66-249-66-1.googlebot.com
  case "$name" in *.googlebot.com|*.google.com|*.search.msn.com|*.applebot.apple.com) ;; *) echo "不是真的"; esac
  dig +short "$name" | grep -qx "$ip" && echo "真的"      # 正查要回到同一个 IP
  ```
- 最近登录成功过的管理员和客户的 IP（手机网络很多人共用一个 IP）；
- 内网地址、服务器自己；
- 手动白名单（一个文件，一行一个 IP）。

要有**解封入口**（后台一个按钮或一个文件），并且封禁记录进日报，不要每封一个推一条消息刷屏。

## 7. 公开恶意名单

每天拉一次，**只加分、不直接封**（直接封误伤太多）：

- FireHOL level1（含 Spamhaus DROP 等）恶意 IP 段；
- Tor 出口节点；
- 一次性邮箱域名（`disposable-email-domains`）：注册时直接拒收。

下载失败、行数明显不对就保留旧文件，不要把名单清空。

## 8. 应用这一层

- **登录失败锁定，按 IP 和按账号各算一份**：比如 IP 15 分钟失败 5 次锁 15 分钟，账号失败 10 次锁定 + 告警 + 邮件通知本人。
- **登录成功不要清掉这个 IP 的失败次数**——攻击者试 4 次密码，登一下自己的号清零，再试 4 次，永远不锁。让失败记录自己过期。
- IPv6 按 `/64` 算同一个网络（一个用户手里有几十亿个 IPv6 地址）。
- 人机验证（Cloudflare Turnstile、hCaptcha）放在：密码登录、发验证码、注册。验证服务连不上时放行（fail-open）还是拒绝，提前想好，并留一个紧急关闭开关。
- 发验证码：每个邮箱 / 手机号、每个 IP 都限次数；验证码有效期短、输错几次作废。
- 后台单独域名，必须两步验证；能限制国家就限制。

## 9. 安全响应头

模板 `templates/nginx/security-headers.conf`：HSTS、CSP、`X-Frame-Options`、`X-Content-Type-Options`、`Referrer-Policy`、`Permissions-Policy`、`Cross-Origin-Opener-Policy`。

- CSP 从严到松：`default-src 'self'`，第三方只放你真用到的（字体、人机验证、支付页）；`form-action` 只允许本站和支付网关；`frame-ancestors 'none'` 防被嵌入。
- 第三方脚本库下载到本站、钉版本，不从公共 CDN 引（CSP 也更好写）。
- 后台和客户后台加 `Cache-Control: no-store, private`。

## 10. 从外面体检

```bash
bash scripts/exposure-check.sh https://你的域名              # 敏感路径、安全头、版本号泄露、HTTP 跳 HTTPS
bash scripts/exposure-check.sh https://你的域名 源站IP        # 再测一下能不能绕过 CDN 直连源站
```

**先把你自己的 IP 加进自动拉黑的白名单，或者用手机热点跑**——这个脚本访问的正是自动拉黑盯着的路径，跑完你自己就被封了。只对你自己的网站用。

## 改完的检查清单

- [ ] 直接用源站 IP 访问（`curl -k https://源站IP -H 'Host: 你的域名'`）连不上
- [ ] 伪造 `X-Forwarded-For` / `CF-Connecting-IP` 不能绕过限流
- [ ] `exposure-check.sh` 没有 FAIL
- [ ] 付款回调、机器上报的地址在 CDN 规则下照常能打进来（拿网关后台的“发送测试通知”试）
- [ ] 证书续期演练能过（`certbot renew --dry-run`）
- [ ] 真 Googlebot 不会被封，假的会
