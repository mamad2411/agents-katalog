# 漏洞发现与扫描

## 2.1 CVE匹配
根据已识别的服务版本搜索对应CVE，优先Critical/High级别

## 2.2 Web漏洞扫描清单

| 漏洞类型 | 检测方法 | 工具 |
|----------|----------|------|
| SQL注入 | 参数注入测试、盲注检测 | sqlmap, 手动测试 |
| XSS | 反射/存储/DOM型 | XSStrike, Dalfox |
| SSRF | 内网地址探测 | curl, Burp |
| LFI/RFI | 路径遍历、伪协议 | 手动测试 |
| 命令注入 | 管道符/变量拼接 | curl, 手动测试 |
| 文件上传 | 绕过文件类型检查 | Burp, curl |
| IDOR/BOLA | 对象引用遍历 | Burp |

## 2.3 配置缺陷检测

| 检查项 | 描述 |
|--------|------|
| 默认凭据 | admin/admin, root/root等 |
| 信息泄露 | /actuator, /debug, /server-info |
| 未授权访问 | 无认证的管理接口 |
| CORS配置 | Access-Control-Allow-Origin: * |
| HTTPS配置 | 证书有效性、HSTS |
| 目录列表 | 目录浏览功能开启 |

## 2.4 SRC/众测漏洞挖掘方法论

5阶段方法论：
1. **资产收集** — 子域名、IP、端口、技术栈
2. **攻击面映射** — 参数枚举、API文档、JS分析
3. **漏洞检测** — 19个攻击类playbook、305个payload
4. **WAF绕过** — 263个绕过变体
5. **报告输出** — 参考2887份HackerOne案例

## 2.5 自动化扫描工具

```bash
# Nuclei漏洞扫描
nuclei -u https://target.com -t cves/ -severity critical,high

# Nikto Web扫描
nikto -h https://target.com

# WPScan WordPress扫描
wpscan --url https://target.com --enumerate vp,vt,u
```
