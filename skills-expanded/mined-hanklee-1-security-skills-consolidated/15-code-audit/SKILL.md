# 代码审计

## 代码审计分类

| 类型 | 工具/项目 | 语言 |
|------|-----------|------|
| Java审计 | java-audit-skills | Java |
| PHP审计 | PHP Code Audit Skill | PHP |
| 通用审计 | Code Audit (55+漏洞类型) | 多语言 |
| 安全审计 | Security Auditor | 多语言 |
| 白盒审计 | dfyx_code_security_review（五阶段） | 多语言 |
| 供应链投毒 | skill-audit-skills | 依赖包 |

## 常见漏洞类型（55+）

### 注入类
- SQL注入、NoSQL注入、命令注入、LDAP注入、XPath注入
- 模板注入（SSTI）、反序列化、XXE

### 认证/授权类
- 硬编码凭据、弱密码策略、Session固定
- JWT攻击、OAuth滥用、权限提升

### 数据处理类
- 路径遍历、文件上传、文件包含
- SSRF、XXE、开放重定向
- 敏感信息泄露

### 框架特定

**Spring:**
- SPEL注入
- Actuator未授权访问
- Spring Security绕过

**Django:**
- 模板注入
- ORM注入
- DEBUG模式泄露

**Laravel:**
- 反序列化（CVE-2021-3129）
- Debug模式泄露
- Env文件泄露

**PHP:**
- 伪协议利用
- 变量覆盖（extract）
- 反序列化（__wakeup/__destruct）
- 文件包含

**Node.js:**
- 原型链污染
- 模板注入（EJS/Pug/Jade）
- 命令注入（child_process）

**Python:**
- SSTI（Jinja2/Twig）
- 反序列化（pickle）
- 命令注入（os.system/subprocess）
- SSRF（requests/urllib）

## 代码审计方法论（五阶段）

```
1. 架构分析
   ├── 项目结构梳理
   ├── 技术栈识别
   └── 入口点枚举

2. 数据流分析
   ├── 污点源识别（用户输入）
   ├── 传播路径追踪
   └── 污点汇聚点（危险函数）

3. 控制流分析
   ├── 权限检查
   ├── 认证绕过
   └── 业务逻辑漏洞

4. 自动化扫描
   ├── Semgrep规则
   ├── CodeQL查询
   └── 自定义规则

5. 人工验证
   ├── PoC编写
   ├── 漏洞确认
   └── 报告输出
```

## 危险函数清单

### PHP
```php
// 命令执行
system(), exec(), passthru(), shell_exec(), popen(), proc_open()
pcntl_exec(), exec()

// 文件操作
file_get_contents(), file_put_contents(), fopen(), include(), require()
include_once(), require_once(), readfile(), file()

// 反序列化
unserialize()

// SQL注入
mysql_query(), mysqli_query(), PDO::query()

// XSS
echo, print, printf
```

### Python
```python
# 命令执行
os.system(), os.popen(), subprocess.call(), subprocess.Popen()
eval(), exec(), compile()

# 反序列化
pickle.loads(), yaml.load(), marshal.loads()

# SQL注入
cursor.execute("SELECT * FROM users WHERE id=" + user_id)
```

### Java
```java
// 命令执行
Runtime.getRuntime().exec()
ProcessBuilder

// 反序列化
ObjectInputStream.readObject()

// SQL注入
Statement.execute("SELECT * FROM users WHERE id=" + userId)

// SSTI
TemplateEngine.process(template, context)
```

## Semgrep规则示例

```yaml
rules:
  - id: sql-injection
    patterns:
      - pattern: |
          $QUERY = "SELECT * FROM " + $INPUT
          cursor.execute($QUERY)
    message: SQL injection via string concatenation
    languages: [python]
    severity: ERROR

  - id: command-injection
    patterns:
      - pattern: os.system($USER_INPUT)
    message: Command injection via os.system
    languages: [python]
    severity: ERROR

  - id: xss-django
    patterns:
      - pattern: |
          mark_safe($USER_INPUT)
    message: Potential XSS via mark_safe
    languages: [python]
    severity: WARNING
```

## CodeQL查询示例

```ql
import python

from Call call, Expr arg
where call.getCalleeName() = "os.system"
  and arg = call.getArg(0)
  and arg instanceof StringConcatenation
select call, "Potential command injection via string concatenation"
```

## 微信小程序审计

- 7个Agent协作
- 4大审计维度：代码安全、数据安全、接口安全、业务逻辑

### 小程序特有风险
```
1. API密钥泄露（app.js, config.js）
2. 接口未授权（无token验证）
3. 越权访问（IDOR）
4. 敏感数据前端存储
5. 接口重放攻击
```
