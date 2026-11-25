---
name: kb-web-cms
description: CVE/PoC 知识库 · PHP/Python/Node 站点与 CMS：Drupalgeddon2(2018-7600)、PHP-FPM(2019-11043)、PHP-CGI Windows(2024-4577)、ThinkPHP 5.x、vBulletin(2019-16759)、Apache httpd(2021-41773)、Joomla(2023-23752)、PHPUnit eval-stdin(2017-9841)。每条都有对应 PoC；公开资料整理，verified=false。
verified: false
sources: 公开资料整理（CVE 公告 / 公开分析 / 业务逻辑类；出处见各条参考）
---

# Web / CMS（19 条）
> 条目为公开资料整理（出处见文末「参考」），`利用步骤` 属待验证假设；出报告前按目标版本自验并把 `verified` 置为 true。

这一栏全是**有 CVE 编号的框架/CMS 漏洞**（博彩包网那类业务逻辑面在 `kb-gray-market`）：

- 按版本打已知 CVE；先认组件与版本，再对区间。
- 白盒/黑盒都适用：`指纹 → 版本 → 条目`，落地物优先"无文件"（命令回显/反连），减少清理工作。

## 条目

| 文件 | 漏洞 | 严重度 | 入口 |
|---|---|---|---|
| `command-injection.md` | 命令注入（分号 / 反引号 / $() 与盲注外带） | critical | 参数被拼进 system/exec/popen |
| `cve-2017-9841-phpunit.md` | PHPUnit eval-stdin 远程代码执行 | critical | POST /vendor/phpunit/.../eval-stdin.php |
| `cve-2018-7600-drupalgeddon2.md` | Drupal 表单 API 远程代码执行（Drupalgeddon2） | critical | - |
| `cve-2019-11043-phpfpm-underflow.md` | PHP-FPM 路径信息下溢 RCE | critical | - |
| `cve-2019-16759-vbulletin.md` | vBulletin widget 配置代码执行 | critical | - |
| `cve-2021-3129-laravel-ignition.md` | Laravel Ignition 调试模式任意文件读 → RCE（CVE-2021-3129） | critical | POST /_ignition/execute-solution 的 solution 参数 |
| `cve-2021-41773-apache-path-traversal.md` | Apache HTTP Server 路径穿越 / CGI RCE | critical | /cgi-bin/.%2e/%2e%2e/bin/sh |
| `cve-2023-23752-joomla-config-leak.md` | Joomla 未授权配置泄露（API） | medium | /api/index.php/v1/config/application?public=true |
| `cve-2023-6553-backup-migration-rce.md` | WordPress Backup Migration 未授权 RCE（CVE-2023-6553） | critical | backup-heart.php 参数注入 include |
| `cve-2024-25600-bricks-rce.md` | WordPress Bricks 未授权 RCE（CVE-2024-25600） | critical | /wp-json/bricks/v1/render_element 的 queryEditor 注入 |
| `cve-2024-27956-wp-automatic-sqli.md` | WordPress WP-Automatic 未授权 SQL 注入（CVE-2024-27956） | critical | /wp-content/plugins/wp-automatic/csv.php 的 q 参数 |
| `cve-2024-4577-phpcgi-windows.md` | PHP-CGI Windows 参数注入（best-fit 编码） | critical | - |
| `lfi-to-rce.md` | 本地文件包含 → RCE（日志包含 / pearcmd / PHP filter chain） | critical | ?page=  ?file=  ?lang=  等包含参数 |
| `nginx-alias-traversal.md` | Nginx alias 路径穿越（读任意文件/源码泄露） | high | /static../  /files..;/  alias 无 / 结尾 |
| `php-object-injection.md` | PHP 反序列化（POP 链 → RCE / phar 触发） | critical | unserialize($_COOKIE) / phar:// 文件操作 |
| `sqli-union-error.md` | SQL 注入（报错 / UNION / 堆叠）通用打法 | critical | 数字/字符串型参数 |
| `ssti-rce.md` | SSTI 模板注入 → RCE（Jinja2 / Twig / Freemarker） | critical | 用户输入被拼进模板字符串 |
| `thinkphp5-rce.md` | ThinkPHP 5.x 方法注入 / 路由 RCE | critical | - |
| `xxe-file-read.md` | XXE 外部实体注入（读文件 / SSRF / OOB 外带） | high | Content-Type: application/xml 的接口 |

## 用这一页的方法

1. **先定位真实源站再谈漏洞**：这类站点普遍挂 CDN/云 WAF，`www.` 记录指向的是防护节点。证书透明（crt.sh）、favicon `icon_hash`、历史 DNS、子域、邮件头 `Received`、SPF/MX 都能翻出源站 IP，直连源站再打，成功率与稳定性完全不同。
2. **自研站的排序**：源码/备份泄露（一步拿到全站逻辑）→ 接口越权（读全量会员/订单）→ 支付回调（资金面）→ 上传（落地）→ 短信（辅助接管）。别从上传硬啃，先看有没有 `.git`。
3. **取证与扰动**：支付类只用自己的测试订单验证，报告写清"订单号 + 金额 + 状态变化"；越权只取 1-2 条记录，别把会员库拖下来当战果。
