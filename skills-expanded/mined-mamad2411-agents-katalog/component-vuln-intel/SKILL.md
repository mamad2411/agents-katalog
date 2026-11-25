---
name: component-vuln-intel
description: >-
  联网情报收集:识别组件后必做CVE/搜索引擎/中文社区/GitHub PoC/资产引擎/即时情报/依赖扩展+受阻换路。Use when a framework/component/version is identified and must search before exploit.
metadata:
  tags: [渗透测试, penetration-testing, 红队]
---

## 联网情报收集（识别组件→立即全网搜；结果=线索/tentative，验证前不是 confirmed Fact）

```
🔴一识别出框架/组件/版本 → 必须停本地扫描立即联网(不搜就利用=盲打=违反铁律)。
🔴以下序列全部执行(不是选做),用{C}=组件名 {V}=版本替换。每步都用 bash（curl）实际访问:

1.CVE漏洞库(必做,找已知漏洞):
  bash: searchsploit {C} {V}
  bash: curl -s "https://cve.circl.lu/api/search/{C}/{V}" | python3 -c "import sys,json;[print(x['id'],x.get('summary','')[:80]) for x in json.load(sys.stdin)[:10]]"
  bash: curl -sk "https://github.com/advisories?query={C}+{V}"
  bash: curl -sk "https://www.cvedetails.com/google-search-results.php?q={C}+{V}&sa=Search"

2.搜索引擎(至少执行3个,找漏洞分析+PoC):
  bash: curl -sk "https://www.google.com/search?q={C}+{V}+exploit+PoC+RCE+site:github.com"
  bash: curl -sk "https://www.google.com/search?q={C}+{V}+漏洞+利用+复现"
  bash: curl -sk "https://www.baidu.com/s?wd={C}+{V}+漏洞+利用+poc+getshell"
  bash: curl -sk "https://www.bing.com/search?q={C}+{V}+CVE+exploit+poc"
  bash: curl -sk "https://duckduckgo.com/?q={C}+{V}+vulnerability+exploit"

3.中文安全社区(必做,中文首发多且深度分析好):
  bash: curl -sk "https://xz.aliyun.com/search?keyword={C}+漏洞"
  bash: curl -sk "https://www.seebug.org/search/?keywords={C}"
  bash: curl -sk "https://paper.seebug.org/search/?keyword={C}"
  bash: curl -sk "https://www.freebuf.com/search?search={C}+{V}"
  bash: curl -sk "https://ti.qianxin.com/vulnerability?keyword={C}"
  bash: curl -sk "https://www.anquanke.com/search?s={C}"

4.GitHub搜PoC/exploit代码(必做,最直接拿利用代码):
  bash: curl -s "https://api.github.com/search/repositories?q={C}+{V}+exploit+OR+poc+OR+CVE&sort=updated&per_page=10" | python3 -c "import sys,json;d=json.load(sys.stdin);[print(x['full_name'],x['html_url'],x.get('description','')[:60]) for x in d.get('items',[])]"
  bash: curl -s "https://api.github.com/search/code?q={C}+RCE+OR+shell+OR+exploit+language:python&per_page=5" | python3 -c "import sys,json;d=json.load(sys.stdin);[print(x['html_url']) for x in d.get('items',[])]"
  bash: curl -s "https://api.github.com/search/repositories?q={C}+CVE&sort=stars&per_page=5" | python3 -c "import sys,json;d=json.load(sys.stdin);[print(x['full_name'],x['stargazers_count'],'★',x.get('description','')[:50]) for x in d.get('items',[])]"
  找到仓库后: curl -s "https://api.github.com/repos/{owner}/{repo}/readme" | python3 -c "import sys,json,base64;print(base64.b64decode(json.load(sys.stdin)['content']).decode())"

5.资产引擎(找同类目标/暴露面):
  bash: curl -sk "https://fofa.info/result?qbase64=$(echo" -n 'app="{C}"' | base64)
  bash: curl -sk "https://www.shodan.io/search?query={C}+{V}"
  bash: curl -sk "https://www.zoomeye.org/searchResult?q={C}"
  bash: curl -sk "https://search.censys.io/search?resource=hosts&q=services.software.product:{C}"

6.即时情报(最新0day/在野利用):
  bash: curl -sk "https://x.com/search?q={C}+CVE+OR+0day+OR+exploit&f=live"
  bash: curl -sk "https://www.reddit.com/r/netsec/search/?q={C}&sort=new&t=month"
  bash: curl -sk "https://www.exploit-db.com/search?q={C}"

7.扩展链(必做): 搜完{C}后,提取其依赖清单(package.json/pom.xml/requirements.txt/go.mod)→对每个依赖重复1-6

🔴搜索受阻处理序列(碰到403/验证码/空结果/超时→按序执行不放弃):
  ①换UA: curl -H "User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" "{URL}"
  ②Jina读取器: bash: curl -sk "https://r.jina.ai/{原始URL}"
  ③Google缓存: bash: curl -sk "https://webcache.googleusercontent.com/search?q=cache:{域名}+{关键词}"
  ④Archive: bash: curl -sk "https://web.archive.org/web/{URL}"
  ⑤GitHub API替代(GitHub页面拦但API不拦): 用上面第4步的curl命令
  ⑥换引擎: Google拦→执行Bing/DuckDuckGo/百度; 百度拦→执行Google/Bing
  ⑦走代理: 按 `proxy-tool-bootstrap` 序列获取SOCKS5代理后重试
  全部受阻仍无结果→写负Fact"已搜{C} {V}全渠道无公开漏洞"→转 `zero-day-discovery`
```

