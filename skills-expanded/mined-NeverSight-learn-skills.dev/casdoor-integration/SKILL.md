---
name: casdoor-integration
description: |
  通用的 Casdoor SSO/IAM 集成指南。支持跨语言 OAuth2/OIDC 认证逻辑。
  Use when: (1) 需要集成 Casdoor 单点登录 (2) 需要实现 OAuth2/OIDC 认证 (3) 需要用户组和组织架构同步 (4) 需要处理 Session 管理和权限映射 (5) 需要解决 OAuth 回调 401 错误
---

# Casdoor 全功能通用集成指南

## 安装命令

```bash
npx skills add ayflying/ai-skills --skill casdoor-integration
```

## 1. OAuth2 登录流程 (手动模式)

### 第一步：生成登录跳转

手动构建 URL，不依赖后端插件：

```
GET <CASDOOR_ENDPOINT>/login/oauth/authorize
  ?client_id=<ID>
  &response_type=code
  &redirect_uri=<自动获取的回调地址>
  &scope=read:users+openid+profile+email
  &state=<随机字符串>
```

**重要**: 必须传递 `state` 参数防止 CSRF 攻击。

**回调地址自动获取（无需手动配置）**：

`redirect_uri` **不需要在代码中硬编码或单独配置**，而是根据当前请求的访问域名自动生成：

```python
def get_callback_url(request) -> str:
    """
    自动从当前请求的 Host/Referer 中获取回调地址
    规则：直接使用当前网页的协议+域名+固定路径 /auth/casdoor/callback
    """
    scheme = request.headers.get("X-Forwarded-Proto", "https")
    host = request.headers.get("Host") or request.headers.get("Referer", "").split("://")[1].rstrip("/")
    return f"{scheme}://{host}/auth/casdoor/callback"
```

Casdoor 后台只需配置一个通配回调路径（如 `https://*.example.com/auth/casdoor/callback`），或通过泛匹配支持多域名场景。

### 第二步：回调处理 (Code Exchange)

1. 接收 `code` 和 `state`
2. 交换 Token：`POST <ENDPOINT>/api/login/oauth/access_token`
3. 获取用户信息：使用 `access_token` 调用 `<ENDPOINT>/api/get-account`
4. 手动注入 Session

**请求正文**:
```json
{
  "grant_type": "authorization_code",
  "client_id": "...",
  "client_secret": "...",
  "code": "..."
}
```

### 第三步：解析用户信息（重要）

从 Casdoor 响应中提取用户信息时，**必须使用 `uid` 作为登录标识**，**禁止使用 email 作为登录标识**：

- `uid` / `id` - **用户唯一标识，作为登录凭证**
- `name` - 用户名
- `email` - 邮箱（可能为空），**禁止用作登录标识**
- `avatar` - 头像 URL
- `groups` - 用户组列表

## 2. 账户关联 (Account Linking)

当系统已有内置用户体系时，遵循"身份合并"原则：

### 工作流

1. **外部 ID 查找** (最高优先级): 检查是否存在 `Casdoor Provider + ProviderUserID` 关联记录
2. **用户编号匹配**: 通过 `uid` 查找系统现有用户
3. **静默绑定**: 找到则建立关联关系
4. **自动创建**: 都找不到才创建新用户

### 字段映射

| Casdoor 字段 | 内部字段 | 说明 |
| :--- | :--- | :--- |
| `uid` | `user_id` | **唯一标识，用于登录判断** |
| `name` | `username` | 用户名（可变更） |
| `email` | `email` | **非必填**。联系方式，不用于身份判断。如果项目不使用邮箱，直接忽略不进行同步 |
| `displayName` | `nickname` | 前端显示名称 |
| `avatar` | `avatar_url` | 头像链接 |

### 无邮箱用户处理与可选同步 (重要)

由于 Casdoor 中的用户（尤其是来自微信、钉钉等第三方认证源的用户）**可能没有填写邮箱**，在集成时必须遵守以下原则：

1. **邮箱必须是非必填项**：在系统的用户表、注册校验、同步逻辑中，`email` 字段必须允许为空（Nullable），切勿强制校验邮箱。
2. **按需同步**：如果当前项目本身不需要使用邮箱功能，在接入和同步用户数据时，**不需要同步邮箱**到项目中，直接丢弃该字段即可。
3. **数据库兜底（仅限遗留系统强制非空限制）**：如果项目底层数据库遗留了强制邮箱非空的限制且难以修改结构，首次注册时才自动生成占位邮箱进行兜底：

```python
def generate_fallback_email(uid: str, provider: str) -> str:
    return f"{provider}_{uid}@placeholder.local"
```

## 3. 用户组与权限映射

### 结构映射

- **Organization** → 系统的"租户"或"顶级企业实例"
- **Group** → 系统的"部门"、"团队"或"空间"（支持父子层级）
- **Role** → 系统的"功能权限集"

### 用户组匹配

Casdoor 用户组格式为 `组织/用户组名`（如 `MyOrg/Engineering`）：

```python
def extract_group_name(casdoor_group: str) -> str:
    if "/" in casdoor_group:
        return casdoor_group.split("/", 1)[1]
    return casdoor_group
```

### 权限同步模式

- **全量同步**: 用户登录时重置所有角色，严格与 Casdoor 返回的 `roles` 一致
- **增量补丁**: 仅同步 Casdoor 返回的角色，保留本地手动扩展角色

## 4. Session 存储冲突解决

### 问题

OAuth 跳转前报错：`Cannot read properties of undefined (reading 'user')`

### 原因

某些框架的 Session 存储层强制要求 `session.user` 存在，但 OAuth 初始化阶段用户尚未登录。

### 解决方案

必须放宽 Session 存储校验：

```python
def save_session(sid, session_data):
    user_id = session_data?.passport?.user?.id

    if user_id:
        update_user_session_cache(user_id, sid)

    # 必须保证 OAuth state 能被存储
    commit_to_database(sid, session_data)
```

## 5. 回调 401 错误排查清单

1. **回调地址自动获取**: `redirect_uri` 应从当前请求自动派生，确保与实际访问域名一致。Casdoor 后台配置的 `Redirect URLs` 应使用通配符或包含所有可能域名的列表
2. **容器内网络**: 确保后端容器能访问 Casdoor 服务器
3. **Secret 转义**: 检查 `clientSecret` 是否包含特殊字符导致转义错误
4. **协议匹配**: `http` 与 `https` 必须与 Casdoor 后台配置完全匹配

## 6. 前端构建陷阱

### 问题

容器运行期配置了环境变量，但前端 SSO 按钮不显示。

### 原因

前端项目在 `npm run build` 期间固化环境变量，构建时缺失会导致逻辑被永久禁用。

### 解决方案

- 不依赖环境变量判断 SSO 是否启用
- 通过后端接口（如 `/api/auth/config`）动态获取支持的认证方式

## 7. 混合认证设计

- **多源登录**: 前端同时提供"内置账户登录"和"SSO 登录"入口
- **权限继承**: 关联用户同时拥有内置权限和 Casdoor 同步的新权限

## 详细资源

- [认证逻辑与 Session 稳定性](references/auth-logic.md)
- [账户关联与无邮箱处理](references/account-linking.md)
- [用户组与权限映射](references/group-mapping.md)
- [前端构建与环境变量](references/frontend-traps.md)
- [手动 OAuth 实现细节](references/logic.md)
- [跨语言集成详解](references/implementation-logic.md)
- [Session 陷阱详解](references/session-pitfalls.md)
