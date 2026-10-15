---
name: local-resources
description: "本地资源库导航——字典库(Dic)、Payload库、POC库的结构和使用方法。当需要使用 ffuf/spray 目录爆破、密码爆破、或构造 Fuzz payload 时必读。覆盖字典选择策略、payload 模板调用、POC 库搜索方法。字典库统一安装在 /pentest 目录下"
metadata:
  category: "general"
  tags: "dictionary,wordlist,payload,poc,ffuf,spray,resource,字典,工具"
---

# 本地资源库导航

⚠️ **核心规则：字典统一在 /pentest 目录** — aboutsecurity 字典库和 nuclei 模板库均安装在 `/pentest/` 下。

## 📁 字典库 (Dic/) — 目录爆破 / 密码爆破 / 参数 Fuzz

### 工具链
```bash
# 查看字典库分类
ls /pentest/AboutSecurity/Dic/
# 查看 Web 字典子分类
ls /pentest/AboutSecurity/Dic/web/
# 使用字典（示例）
spray -u http://target -d /pentest/AboutSecurity/Dic/web/directory/common.txt
ffuf -u http://target/FUZZ -w /pentest/AboutSecurity/Dic/web/directory/common.txt
```

### 常用字典速查表

| 场景 | 路径 | 行数 |
|------|-------------------|------|
| 通用目录爆破 | `Dic/web/directory/common.txt` | 5378 |
| PHP 文件发现 | `Dic/web/directory/php/php.txt` | 48094 |
| PHP Top100 | `Dic/web/directory/php/top100-php.txt` | 93 |
| CTF URI Fuzz | `Dic/web/ctf/uri.txt` | 222 |
| CTF 参数 Fuzz | `Dic/web/ctf/param.txt` | 44 |
| CTF SQL Fuzz | `Dic/web/ctf/sql.txt` | 94 |
| 后台路径 | `Dic/web/directory/admin-dir.txt` | 2166 |
| API 路径 | `Dic/web/directory/api.txt` | 341 |
| 备份文件 | `Dic/web/file-backup/` | — |
| 密码 Top100 | `Dic/auth/password/password-top100.txt` | 172 |
| DNS 子域名 | `Dic/web/dns/` | — |

### 决策树：该用哪个字典？

```
目标是 Web 应用？
├── CTF/靶场 → Dic/web/ctf/uri.txt（小而精）
├── PHP 站 → Dic/web/directory/php/php.txt（全面）
├── 通用站 → Dic/web/directory/common.txt
├── 找后台 → Dic/web/directory/admin-dir.txt
├── 找 API → Dic/web/directory/api.txt
└── 找备份 → Dic/web/file-backup/

目标是认证服务？
├── 密码爆破 → Dic/auth/password/password-top100.txt
├── 用户名枚举 → Dic/auth/username/
└── 特定服务 → Dic/port/{mysql,ssh,rdp,...}/
```

## 📁 Payload 库 — 漏洞验证 payload

### 工具链
```bash
# 查看 aboutsecurity payload 分类
ls /pentest/AboutSecurity/Payload/
# 查看 nuclei 模板库
ls ~/nuclei-templates/
# 读取具体 payload 文件
cat /pentest/AboutSecurity/Payload/sqli/payload.txt        # 通用 SQLi Fuzz payload
cat /pentest/AboutSecurity/Payload/sqli/sql-inj.md         # 快速查阅速查手册（含 WAF 绕过技巧）
```

### 可用分类
sqli | xss | lfi | ssrf | xxe | rce | access-bypass | upload | cors | hpp | ssi

## ⚠️ 使用外部工具的正确流程

```
❌ 错误：ffuf -u http://target/FUZZ -w /usr/share/wordlists/common.txt
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                        猜测路径，大概率不存在

✅ 正确：
1. ls /pentest/AboutSecurity/Dic/web/directory/  → 确认字典存在
2. ffuf -u http://target/FUZZ -w /pentest/AboutSecurity/Dic/web/directory/common.txt
```

## 💡 高效使用提示

1. **spray / ffuf 已封装字典** — 如果只是简单目录爆破，直接用 `spray -u target -d wordlist.txt` 或 `ffuf -u target/FUZZ -w wordlist.txt`
2. **自定义参数用 ffuf** — 需要自定义参数（如 -e .bak -mc 200）时用 `ffuf -u target/FUZZ -w /pentest/AboutSecurity/Dic/...`
3. **CTF 场景优先用小字典** — Dic/web/ctf/ 下的字典精简且针对性强，避免大字典浪费时间
