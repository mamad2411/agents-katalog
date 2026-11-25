# 供应链与API安全

## 供应链安全

### 检查项
| 检查 | 描述 | 工具 |
|------|------|------|
| SBOM | 软件物料清单 | syft, cyclonedx |
| SCA | 依赖漏洞扫描 | snyk, grype, trivy |
| 容器安全 | 镜像漏洞 | trivy, anchore |
| CI/CD安全 | 构建管道安全 | checkov, tfsec |
| 构建完整性 | 签名验证 | cosign, sigstore |

### 依赖投毒防护
- 锁定依赖版本（package-lock.json, requirements.txt）
- 验证包签名
- 检查包名相似性（typosquatting）
- 使用私有镜像源
- 定期扫描依赖漏洞

### 常见供应链攻击
```
1. Typosquatting: 发布相似包名的恶意包
2. Dependency Confusion: 利用私有包名在公共仓库注册
3. Maintainer Takeover: 控制包维护者账号
4. Malicious Code Injection: 向合法包注入恶意代码
5. Build Pipeline Compromise: 篡改构建流程
```

## API安全测试

### 10阶段方法论
1. API发现（Swagger/OpenAPI文档）
2. 认证测试（API Key/JWT/OAuth）
3. 授权测试（BOLA/IDOR）
4. 输入验证（注入/溢出）
5. 业务逻辑（竞态/绕过）
6. 速率限制
7. 数据泄露
8. 配置错误
9. 日志与监控
10. 第三方集成

### 常见API漏洞

| 漏洞 | 描述 |
|------|------|
| BOLA/IDOR | 越权访问其他用户数据 |
| JWT攻击 | 弱密钥/算法混淆/未验证签名 |
| OAuth滥用 | redirect_uri篡改 |
| GraphQL注入 | 内省查询、深度嵌套 |
| WebSocket劫持 | 跨站WebSocket劫持 |
| 速率限制缺失 | 暴力破解/枚举 |
| 批量分配 | 修改不应修改的字段 |
| 功能级别授权缺失 | 普通用户访问管理API |

### API测试工具
```bash
# Burp Suite - API测试
# Postman - API调试
# Arjun - 参数发现
arjun -u https://target.com/api/endpoint

# Kiterunner - API路径发现
kr scan https://target.com -w api-routes

# JWT工具
# jwt_tool
python3 jwt_tool.py <token> -X k -pk public.pem

# GraphQL
# 内省查询
{__schema{types{name,fields{name}}}}

# 深度嵌套DoS
query { user { friends { friends { friends { ... } } } } }
```
