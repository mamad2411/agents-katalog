# 信息收集与侦察

## 1.1 被动侦察

| 技术 | 描述 | 工具 |
|------|------|------|
| HTTP响应头分析 | 识别服务器类型/版本/WAF | curl, fetch |
| HTML源码分析 | 技术栈标识（React/Vue/Angular等） | 浏览器开发工具 |
| WHOIS/DNS查询 | 域名注册信息、DNS记录 | whois, dig, nslookup |
| 证书透明度 | 子域名发现 | crt.sh, certspotter |
| 搜索引擎 | Google Dorking、Shodan、Censys | Google, Shodan |

### Google Dorking 常用语法
```
site:target.com filetype:pdf
inurl:admin | inurl:login | inurl:dashboard
intitle:"index of" "parent directory"
site:target.com ext:sql | ext:dbf | ext:mdb
site:target.com inurl:api | inurl:swagger | inurl:graphql
```

## 1.2 主动侦察

| 技术 | 描述 | 工具 |
|------|------|------|
| 端口扫描 | 探测常见Web端口 | nmap, masscan |
| 目录枚举 | 枚举目录和路径 | ffuf, gobuster, dirsearch |
| 子域名发现 | 子域名爆破 | subfinder, amass |
| 指纹识别 | Web应用技术栈识别 | wafw00f, whatweb |
| 敏感文件 | robots.txt/.env/.git/config泄露 | curl, wget |
| API端点发现 | REST/GraphQL接口枚举 | ffuf, arjun |

### 常用命令
```bash
# 端口扫描
nmap -sV -sC -O target.com
masscan -p1-65535 target.com --rate=10000

# 目录枚举
ffuf -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt
dirsearch -u https://target.com -e php,asp,aspx,jsp,html,js

# 子域名发现
subfinder -d target.com -o subs.txt
amass enum -d target.com -o amass_subs.txt

# 指纹识别
wafw00f https://target.com
whatweb https://target.com
```

## 1.3 技术栈识别

- **前端框架**: React(jsx)、Vue(v-cloak)、Angular(ng-)
- **后端框架**: Django(csrfmiddleware)、Flask(flask)、Spring(JSESSIONID)、PHP(PHPSESSID)
- **CMS系统**: WordPress(wp-content)、Drupal、Joomla
- **数据库**: MySQL、PostgreSQL、MongoDB、Redis

## 1.4 目标画像输出

```
目标: example.com
服务器: nginx/1.18 + Ubuntu
后端: PHP 8.1 + Laravel
数据库: MySQL (推测)
WAF: Cloudflare
攻击面: /admin, /api/v1, /upload, /.env
```

## 1.5 资产收集自动化流程

```
子域名枚举 → 存活探测 → 端口扫描 → 指纹识别 → 目录枚举 → 漏洞扫描
     ↓           ↓          ↓          ↓          ↓          ↓
  subfinder   httpx      nmap     whatweb      ffuf      nuclei
  amass       httprobe   masscan  wafw00f     dirsearch  nikto
```

### 自动化脚本
```bash
#!/bin/bash
TARGET=$1
echo "[*] 子域名枚举..."
subfinder -d $TARGET -silent | tee subs.txt
echo "[*] 存活探测..."
cat subs.txt | httpx -silent | tee alive.txt
echo "[*] 目录枚举..."
cat alive.txt | while read url; do
    ffuf -u $url/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403
done
```
