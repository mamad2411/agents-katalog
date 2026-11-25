---
name: security-testing
description: "安全测试(DAST)方法论——OWASP ZAP 使用、漏洞扫描、安全报告生成、漏洞验证。用于动态应用安全测试和安全审计。"
version: "4.3.8"
updated: "2026-05-14"
---

# 安全测试 (DAST) 方法论

## 概述

动态应用安全测试（DAST）在运行时检测安全漏洞——不分析源代码，而是模拟攻击者行为探测弱点。本技能指导 DAST 的完整流程：从工具配置到漏洞验证。

**核心原则：** 安全测试必须模拟真实攻击，但不能造成实际损害。始终在隔离环境中执行，始终获得明确授权。

## 何时使用

**适用场景：**
- 发布前的安全门禁检查
- OWASP Top 10 漏洞扫描
- API 端点安全验证
- 认证/授权机制测试
- 第三方集成安全审计

**不适用场景：**
- 纯静态代码分析（用 SAST 工具如 SonarQube）
- 依赖项 CVE 扫描（用 `npm audit` / Snyk）
- 合规性审计（需要专业审计工具）

---

## 方法论

### 步骤 1：安全测试授权与准备

**必须在测试前确认：**
- [ ] 获得目标应用的测试授权（书面记录）
- [ ] 测试环境是 staging/test，不是 production
- [ ] 通知相关团队（运维、安全）
- [ ] 准备好回滚方案（如测试造成数据损坏）

### 步骤 2：OWASP Top 10 测试矩阵

| OWASP 类别 | 风险 | DAST 测试方法 | 检测工具 |
|-----------|------|-------------|---------|
| **A01: 访问控制失效** | Critical | IDOR 测试、路径遍历 | ZAP Active Scan |
| **A02: 加密失效** | High | 检查 HTTP → HTTPS 重定向、TLS 配置 | ZAP / testssl.sh |
| **A03: 注入** | Critical | SQLi、XSS、命令注入 | ZAP / sqlmap |
| **A04: 不安全设计** | High | 检查速率限制、批量分配 | 手动测试 |
| **A05: 安全配置错误** | Medium | 默认凭证、CORS 配置、HTTP 方法 | ZAP / Nikto |
| **A06: 易受攻击组件** | High | 依赖版本检查（SAST 领域） | `npm audit` / Snyk |
| **A07: 认证失效** | High | 弱密码策略、JWT 伪造、会话固定 | ZAP / 手动 |
| **A08: 软件与数据完整性** | High | 反序列化漏洞、CI/CD 管道 | 手动审查 |
| **A09: 日志与监控** | Medium | 检查敏感信息是否被记录 | grep 日志 |
| **A10: SSRF** | High | 服务器端请求伪造 | ZAP / 手动 |

### 步骤 3：OWASP ZAP 操作流程

#### 3.1 启动 ZAP
```bash
# Docker 方式
docker run -d --name zap -p 8080:8080 -p 8090:8090 \
  -v $(pwd)/zap-workdir:/zap/wrk \
  ghcr.io/zaproxy/zaproxy:stable zap.sh -daemon \
  -host 0.0.0.0 -port 8080 \
  -config api.key=changeme \
  -config api.addrs.addr.name=.* \
  -config api.addrs.addr.regex=true

# 验证启动
curl http://localhost:8080/
```

#### 3.2 配置目标
```bash
# 设置目标上下文
curl -X POST "http://localhost:8080/JSON/context/action/newContext/" \
  -d "contextName=MyApp"

curl -X POST "http://localhost:8080/JSON/context/action/includeInContext/" \
  -d "contextName=MyApp" \
  -d "regex=http://testapp.local/.*"

# 设置认证（如需要）
curl -X POST "http://localhost:8080/JSON/authentication/action/setAuthenticationMethod/" \
  -d "contextId=1" \
  -d "authMethodName=formBasedAuthentication" \
  -d "authMethodConfigParams=loginUrl=http://testapp.local/login&loginRequestData=username%3D%7B%25username%25%7D%26password%3D%7B%25password%25%7D"
```

#### 3.3 执行扫描
```bash
# 1. 传统蜘蛛爬取
curl "http://localhost:8080/JSON/spider/action/scan/" \
  -d "url=http://testapp.local" \
  -d "maxChildren=10" \
  -d "recurse=true"

# 2. AJAX 蜘蛛（SPA 应用）
curl "http://localhost:8080/JSON/ajaxSpider/action/scan/" \
  -d "url=http://testapp.local"

# 3. 主动扫描
curl "http://localhost:8080/JSON/ascan/action/scan/" \
  -d "url=http://testapp.local" \
  -d "recurse=true" \
  -d "scanPolicyName=Default Policy"
```

#### 3.4 监控扫描进度
```bash
# 检查蜘蛛进度
curl "http://localhost:8080/JSON/spider/view/status/?scanId=0"

# 检查主动扫描进度
curl "http://localhost:8080/JSON/ascan/view/status/?scanId=0"
```

#### 3.5 获取结果
```bash
# JSON 格式告警
curl "http://localhost:8080/JSON/core/view/alerts/?baseurl=http://testapp.local" > alerts.json

# HTML 报告
curl "http://localhost:8080/OTHER/core/other/htmlreport/" > .jarvis/YYYY-MM-DD/testing/security-report.html
```

### 步骤 4：漏洞分类与处置

```yaml
漏洞处置矩阵:
  Critical:
    处理: 必须立即修复，阻塞发布
    时间: 24小时内
    审批: 安全负责人
  High:
    处理: 必须修复，阻塞发布
    时间: 发布前
    审批: 技术负责人
  Medium:
    处理: 应在发布前修复
    时间: 本迭代
    审批: 团队自行决定
  Low:
    处理: 记录技术债务
    时间: 下迭代
    审批: 无需
  Info:
    处理: 参考信息
    时间: N/A
    审批: N/A
```

### 步骤 5：漏洞验证（防止误报）

自动化扫描的结果可能包含误报，Critical/High 必须手动验证：

```bash
# SQL 注入验证
curl "http://testapp.local/api/users?id=1' OR '1'='1"
# 真实漏洞: 返回所有用户
# 误报: 返回 400 或正常结果

# XSS 验证
curl "http://testapp.local/search?q=<script>alert(1)</script>"
# 真实漏洞: 响应中包含未转义的 script 标签
# 误报: 响应中已转义或过滤

# IDOR 验证
curl -H "Authorization: Bearer <user_A_token>" \
  "http://testapp.local/api/users/999"  # 其他用户的数据
# 真实漏洞: 返回了用户 B 的数据
# 误报: 返回 403
```

### 步骤 6：生成安全报告

```markdown
# 安全测试报告
## 扫描概览
- 目标: http://testapp.local
- 扫描时间: YYYY-MM-DD HH:MM
- 扫描工具: OWASP ZAP v2.15.0
- 扫描策略: Default Policy

## 漏洞统计
| 风险等级 | 数量 | 已验证 | 误报 |
|---------|------|--------|------|
| Critical | 0 | 0 | 0 |
| High | 2 | 2 | 0 |
| Medium | 5 | 3 | 2 |
| Low | 8 | - | - |

## 漏洞详情
### HIGH-001: SQL注入 - GET /api/users
- **OWASP**: A03 Injection
- **端点**: GET /api/users?id=
- **验证**: 已确认，可注入
- **修复**: 使用参数化查询
- **CWE**: CWE-89

### MEDIUM-003: CORS配置过宽
- **OWASP**: A05 Security Misconfiguration
- **端点**: 所有响应头 Access-Control-Allow-Origin: *
- **验证**: 误报 — staging 环境故意开放 CORS
- **说明**: 生产环境已配置白名单
```

---

## 反模式

| 反模式 | 正确做法 |
|--------|---------|
| 对生产环境直接扫描 | 始终在 staging/test 环境执行 DAST |
| 不授权就开始测试 | 安全测试是受控活动，必须有书面授权 |
| 信任所有自动化告警 | Critical/High 必须手动验证，防止误报 |
| 扫描后不撤销测试数据 | 删除测试账号和数据，恢复干净状态 |
| 只依赖 DAST | DAST + SAST + 依赖扫描 = 完整安全门禁 |
| 报告只给开发不管运维 | 运维需要知道扫描时间，避免误判为攻击 |

## 验证清单

- [ ] 已获得安全测试授权
- [ ] 测试目标为 staging/test 环境
- [ ] ZAP 或等效工具已正确配置
- [ ] 蜘蛛爬取覆盖了所有页面和 API 端点
- [ ] Critical/High 告警均已手动验证
- [ ] 已验证的漏洞有明确修复方案
- [ ] 安全报告已输出到 .jarvis/YYYY-MM-DD/testing/
- [ ] 测试数据已清理
