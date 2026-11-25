# CTF技能

## CTF分类（40+子技能）

| 类别 | 技能 |
|------|------|
| Web | SQL注入、XSS、SSRF、反序列化、模板注入 |
| Pwn | 栈溢出、堆利用、格式化字符串、ROP |
| Crypto | RSA、AES、古典密码、哈希碰撞 |
| Reverse | ELF分析、PE分析、脱壳、混淆 |
| Forensics | 内存取证、磁盘取证、流量分析、隐写 |
| OSINT | 社工、信息收集、图片分析 |
| Cloud | AWS/GCP/Azure安全 |
| Container | Docker逃逸、K8s安全 |
| AD | 域渗透、Kerberos攻击 |
| Mobile | APK逆向、iOS安全 |

## 常用CTF工具

| 工具 | 用途 |
|------|------|
| pwntools | Pwn利用开发 |
| z3 | 约束求解 |
| CyberChef | 编解码 |
| John the Ripper | 密码破解 |
| Volatility | 内存取证 |
| Wireshark | 流量分析 |
| steghide/zsteg | 隐写分析 |
| hashcat | GPU密码破解 |
| Ghidra | 逆向分析 |
| GDB+GEF/pwndbg | 调试器 |

## Pwn工具链

```python
from pwn import *

# 连接目标
p = remote('target.com', 1337)
# p = process('./binary')

# 构造payload
payload = b'A' * offset
payload += p64(0x4011b0)  # 返回地址
payload += p64(0)         # padding
payload += p64(system_addr)
payload += p64(binsh_addr)

# 发送payload
p.sendline(payload)
p.interactive()
```

## Crypto常见题型

```python
# RSA分解
from Crypto.PublicKey import RSA
from sympy import factorint

# AES ECB模式
# 相同明文块 → 相同密文块

# XOR加密
plaintext = bytes([c ^ key[i%len(key)] for i, c in enumerate(ciphertext)])

# 维吉尼亚密码
# 频率分析 → 找密钥长度 → 逐字符破解
```

## Forensics工具

```bash
# 流量分析
tshark -r capture.pcap -Y "http.request"
wireshark capture.pcap

# 内存取证
volatility -f mem.dump imageinfo
volatility -f mem.dump --profile=Win7SP1x64 pslist
volatility -f mem.dump --profile=Win7SP1x64 filescan
volatility -f mem.dump --profile=Win7SP1x64 dumpfiles -Q <offset> -D output/

# 隐写分析
steghide extract -sf image.jpg
zsteg image.png
stegsolve image.png
binwalk -e file
```
