---
name: code-annotation
description: >
  代码输出中文标注——AI 输出代码块时，对变量名/函数名/类名首次出现处附加中文翻译。
  翻译格式固定：`原名`（中文译名）→ 一句话解释。每名只译一次，行业缩写不译。
  当用户要求"解释代码""加点注释""翻译变量名""变量名看不懂"或在对话中频繁出现
  英文变量名导致理解困难时使用。也适用于 code review、新人 onboarding 等场景。
  触发词：代码标注、变量翻译、中文注释、变量名看不懂、翻译变量名、
  加点注释、解释这段代码、代码可读性、新人看不懂、code annotation。
---

# 代码输出中文标注

## 核心规则

AI 在输出代码块时，对**首次出现的**变量名、函数名、类名附加中文翻译。
格式固定，不增加代码本身，只在 AI 的解释文本中出现。

```
`原名`（中文译名）→ 一句话解释
```

## 何时触发

- AI 输出任何包含英文变量名/函数名/类名的代码块
- 用户问"这段代码做了什么"、"解释一下"
- code review 场景
- 用户明确说"翻译变量名"、"变量名看不懂"

## 翻译格式

### 标准格式

```
`authenticateUser`（用户认证）→ 校验用户登录凭据，返回 token
`validateEmail`（邮箱格式校验）→ 检查邮箱地址是否符合标准格式
`processOrder`（订单处理）→ 扣减库存、生成订单、触发支付
`isExpired`（是否过期）→ 检查 token 或会话是否超过有效期
```

### 格式要点

- 用反引号包裹英文原名，紧接中文译名在中文括号里
- 箭头 `→` 后跟一句话解释（不是翻译名，是这个变量/函数**做了什么事**）
- 不修改代码本身，只在 AI 的解释文本中标注
- 函数名解释"做什么"，变量名解释"存什么"，布尔值解释"判断什么"

## 翻译规则

### 规则 1：每个名只译一次

同一变量在回复中多次出现时，只翻译**首次出现**处。后续直接用英文原名，不重复翻译。

### 规则 2：行业缩写不翻译

以下类别保持英文原名，不翻译：

**协议/格式**：`HTTP`、`HTTPS`、`API`、`REST`、`JSON`、`XML`、`CSV`、`YAML`、`GraphQL`、`gRPC`

**认证/安全**：`JWT`、`OAuth`、`OAuth2`、`SAML`、`SSO`、`CORS`、`CSRF`、`XSS`、`TLS`、`SSL`

**数据库/存储**：`SQL`、`NoSQL`、`Redis`、`MySQL`、`PostgreSQL`、`MongoDB`、`ORM`

**前端/框架**：`HTML`、`CSS`、`JS`、`TS`、`DOM`、`SPA`、`SSR`、`CSR`、`JSX`、`TSX`

**运维/部署**：`AWS`、`GCP`、`Azure`、`K8s`、`Docker`、`CI`、`CD`、`CICD`、`DevOps`

**通用缩写**：`ID`、`UUID`、`URL`、`URI`、`IP`、`TCP`、`UDP`、`DNS`、`CPU`、`RAM`、`IO`

**HTTP 方法**：`GET`、`POST`、`PUT`、`DELETE`、`PATCH`、`OPTIONS`、`HEAD`

**常见短变量**：`req`、`res`、`ctx`、`db`、`fn`、`cb`、`err`、`ok`、`msg`、`arg`、`ret`

> 不确定是否翻译时，问自己：这个词在中文技术文档里一般用中文还是英文？如果中文文档也直接用英文（如"JWT token"），就不翻译。

### 规则 3：中文译名要准确简洁

- 译名用中文技术圈普遍接受的叫法，不自己造词
- 控制在 2-6 个字
- 函数名翻译动作（"用户认证"），变量名翻译内容（"订单列表"），布尔值翻译判断（"是否登录"）

### 规则 4：一句话解释说清"做了什么"

- 不是重复译名，而是补充译名没表达的信息
- 函数：输入什么 → 输出什么
- 变量：存储什么数据，从哪里来
- 布尔值：true 代表什么，false 代表什么

## 示例

### 示例 1：解释函数

**用户问**：这段代码做了什么？

**AI 回复**：

```python
def authenticateUser(credentials):
    ...
```

这里 `authenticateUser`（用户认证）→ 接收登录凭据，校验用户名密码，成功返回 JWT token，失败抛出 `AuthError`。

### 示例 2：解释多个变量

```javascript
const userList = await fetchUsers();
const isAdmin = checkPermission(user);
const orderTotal = calcPrice(items);
```

这里：
- `fetchUsers`（获取用户列表）→ 从数据库查询所有活跃用户
- `userList`（用户列表）→ 存储 `fetchUsers` 的返回结果
- `checkPermission`（权限检查）→ 判断用户是否有管理员权限，返回布尔值
- `isAdmin`（是否管理员）→ `true` 表示有管理权限，`false` 表示普通用户
- `calcPrice`（价格计算）→ 根据商品列表计算总价，含折扣
- `orderTotal`（订单总价）→ 存储 `calcPrice` 的计算结果

### 示例 3：行业缩写不翻译

```javascript
const jwtToken = signJWT(payload);
const apiUrl = `${BASE_URL}/api/v1/users`;
const dbConn = await connectDB();
```

这里：
- `signJWT`（JWT 签名）→ 用密钥对 payload 签名，生成 JWT token
- `jwtToken`（JWT 令牌）→ 存储生成的 JWT 字符串
- `apiUrl`（API 地址）→ 拼接完整的 API 请求 URL
- `BASE_URL`（基础地址）→ 环境变量中的 API 根路径
- `connectDB`（数据库连接）→ 建立数据库连接并返回连接对象
- `dbConn`（数据库连接）→ 存储活跃的数据库连接实例

> 注意：`JWT`、`API`、`URL` 等缩写不翻译，但包含它们的复合变量名仍翻译其余部分。

## 与其他 skill 的衔接

- 涉及 commit message → 用 `chinese-commit-messages`