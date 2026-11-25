---
name: api-design-cn
description: RESTful API 设计规范（中文版），涵盖资源命名、统一响应、分页、错误码、版本控制、认证、OpenAPI 文档
version: "1.0"
---

# API 设计规范

## 概述

本 Skill 定义 RESTful API 的设计规范，适用于 Java/Python/Go/Node.js 等后端项目，确保 API 风格统一、文档完善、易于对接。

适用场景：
- 新项目 API 契约设计
- 已有项目 API 规范治理
- 前后端接口对接标准制定
- OpenAPI/Swagger 文档编写

---

## RESTful 资源命名

### 基本原则

```
# 资源用名词复数，不用动词
GET    /api/v1/users          # 获取用户列表
POST   /api/v1/users          # 创建用户
GET    /api/v1/users/123      # 获取单个用户
PUT    /api/v1/users/123      # 全量更新用户
PATCH  /api/v1/users/123      # 部分更新用户
DELETE /api/v1/users/123      # 删除用户

# 子资源用嵌套路径表示归属关系
GET    /api/v1/users/123/orders       # 获取用户的订单列表
POST   /api/v1/users/123/orders       # 为用户创建订单
GET    /api/v1/users/123/orders/456   # 获取用户的某个订单

# 嵌套不超过两层，超过时提升为顶级资源
GET    /api/v1/orders/456/items       # 可以
GET    /api/v1/users/123/orders/456/items/789  # 太深，应拆分
GET    /api/v1/order-items/789        # 提升为顶级资源
```

### 命名规范

```
# URL 路径：全小写，连字符分隔（kebab-case）
/api/v1/order-items        # 正确
/api/v1/orderItems         # 错误 — 不用 camelCase
/api/v1/order_items        # 错误 — 不用 snake_case

# 查询参数：snake_case
/api/v1/users?page_size=20&sort_by=created_at

# 请求/响应体字段：camelCase（前端友好）
{
  "userId": 123,
  "userName": "张三",
  "createdAt": "2026-03-14T10:00:00Z"
}
```

### HTTP 方法与状态码对照

```
方法      语义            成功状态码     幂等性
-------  --------------  -----------  ------
GET      查询资源         200          是
POST     创建资源         201          否
PUT      全量替换         200          是
PATCH    部分更新         200          否
DELETE   删除资源         204          是

常用错误状态码:
400 Bad Request        — 参数校验失败
401 Unauthorized       — 未认证（未登录）
403 Forbidden          — 已认证但无权限
404 Not Found          — 资源不存在
409 Conflict           — 资源冲突（如重复创建）
422 Unprocessable      — 业务规则校验失败
429 Too Many Requests  — 触发限流
500 Internal Server    — 服务器内部错误
```

---

## 统一响应格式

### 标准响应结构

```json
// 成功响应
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 123,
    "username": "zhangsan",
    "email": "zhang@example.com"
  }
}

// 失败响应
{
  "code": 10001,
  "message": "用户名已存在",
  "data": null
}

// 校验失败响应（携带字段级错误明细）
{
  "code": 10000,
  "message": "参数校验失败",
  "data": {
    "errors": [
      {"field": "email", "message": "邮箱格式不正确"},
      {"field": "password", "message": "密码长度不能少于8位"}
    ]
  }
}
```

### 代码实现

```java
// Java — 统一响应体
public class ApiResponse<T> {
    private int code;         // 业务状态码，0 表示成功
    private String message;   // 提示信息
    private T data;           // 响应数据

    // 成功响应
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(0, "success", data);
    }

    public static ApiResponse<Void> success() {
        return new ApiResponse<>(0, "success", null);
    }

    // 失败响应
    public static <T> ApiResponse<T> fail(int code, String message) {
        return new ApiResponse<>(code, message, null);
    }

    // 带错误码枚举的失败响应
    public static <T> ApiResponse<T> fail(ErrorCode errorCode) {
        return new ApiResponse<>(errorCode.getCode(), errorCode.getMessage(), null);
    }
}
```

```python
# Python (FastAPI) — 统一响应体
from pydantic import BaseModel, Generic
from typing import TypeVar

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    code: int = 0
    message: str = "success"
    data: T | None = None

    @classmethod
    def success(cls, data: T = None) -> "ApiResponse[T]":
        return cls(code=0, message="success", data=data)

    @classmethod
    def fail(cls, code: int, message: str) -> "ApiResponse":
        return cls(code=code, message=message, data=None)
```

```go
// Go (gin) — 统一响应体
type ApiResponse struct {
    Code    int         `json:"code"`
    Message string      `json:"message"`
    Data    interface{} `json:"data"`
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, ApiResponse{
        Code: 0, Message: "success", Data: data,
    })
}

func Fail(c *gin.Context, httpStatus int, code int, message string) {
    c.JSON(httpStatus, ApiResponse{
        Code: code, Message: message, Data: nil,
    })
}
```

---

## 分页设计

### 请求参数

```
# 标准分页参数
GET /api/v1/users?page=1&size=20&sort_by=created_at&sort_order=desc

参数说明:
- page     — 页码，从 1 开始（非 0）
- size     — 每页条数，默认 20，最大 100
- sort_by  — 排序字段（可选）
- sort_order — 排序方向 asc/desc（可选，默认 desc）
```

### 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {"id": 1, "username": "zhangsan"},
      {"id": 2, "username": "lisi"}
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 156,
      "totalPages": 8
    }
  }
}
```

### 代码实现

```java
// Java — 分页请求与响应
public record PageQuery(
    @Min(1) int page,
    @Min(1) @Max(100) int size,
    String sortBy,
    String sortOrder
) {
    public PageQuery {
        // 默认值处理
        if (page < 1) page = 1;
        if (size < 1) size = 20;
        if (size > 100) size = 100;
        if (sortOrder == null) sortOrder = "desc";
    }

    public int getOffset() {
        return (page - 1) * size;
    }
}

public record PageResult<T>(
    List<T> items,
    Pagination pagination
) {
    public record Pagination(int page, int size, long total, int totalPages) {}

    public static <T> PageResult<T> of(List<T> items, long total, PageQuery query) {
        int totalPages = (int) Math.ceil((double) total / query.size());
        return new PageResult<>(items,
            new Pagination(query.page(), query.size(), total, totalPages));
    }
}
```

### 游标分页（大数据量推荐）

```json
// 请求
// GET /api/v1/orders?cursor=eyJpZCI6MTAwfQ&size=20

// 响应
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [...],
    "cursor": {
      "next": "eyJpZCI6MTIwfQ",
      "hasMore": true
    }
  }
}
```

```java
// Java — 游标分页（Base64 编码游标）
public record CursorPageResult<T>(
    List<T> items,
    CursorInfo cursor
) {
    public record CursorInfo(String next, boolean hasMore) {}

    public static <T> CursorPageResult<T> of(List<T> items, int size, String nextCursor) {
        boolean hasMore = items.size() >= size;
        return new CursorPageResult<>(items, new CursorInfo(nextCursor, hasMore));
    }
}
```

---

## 错误码体系

### 错误码规范

```
错误码格式: 5 位整数
- 0          — 成功
- 10xxx      — 通用错误（参数校验、认证、权限）
- 2xxxx      — 用户模块错误
- 3xxxx      — 订单模块错误
- 4xxxx      — 支付模块错误
- 9xxxx      — 系统级错误

每个模块预留 1000 个错误码空间
```

### 错误码定义

```java
// Java — 错误码枚举
public enum ErrorCode {
    // 通用错误 10xxx
    VALIDATION_ERROR(10000, "参数校验失败"),
    UNAUTHORIZED(10001, "未认证，请先登录"),
    FORBIDDEN(10002, "无权限访问"),
    NOT_FOUND(10003, "资源不存在"),
    RATE_LIMITED(10004, "请求过于频繁，请稍后重试"),
    DUPLICATE(10005, "资源已存在"),

    // 用户模块 2xxxx
    USER_NOT_FOUND(20001, "用户不存在"),
    USER_DISABLED(20002, "用户已禁用"),
    USERNAME_DUPLICATE(20003, "用户名已存在"),
    EMAIL_DUPLICATE(20004, "邮箱已被注册"),
    PASSWORD_WRONG(20005, "密码错误"),

    // 订单模块 3xxxx
    ORDER_NOT_FOUND(30001, "订单不存在"),
    ORDER_STATUS_INVALID(30002, "订单状态不允许此操作"),
    ORDER_EXPIRED(30003, "订单已过期"),
    STOCK_INSUFFICIENT(30004, "库存不足"),

    // 系统错误 9xxxx
    INTERNAL_ERROR(99999, "服务器内部错误");

    private final int code;
    private final String message;

    ErrorCode(int code, String message) {
        this.code = code;
        this.message = message;
    }

    public int getCode() { return code; }
    public String getMessage() { return message; }
}
```

```python
# Python — 错误码定义
from enum import IntEnum

class ErrorCode(IntEnum):
    """业务错误码"""
    # 通用错误
    VALIDATION_ERROR = 10000     # 参数校验失败
    UNAUTHORIZED = 10001         # 未认证
    FORBIDDEN = 10002            # 无权限
    NOT_FOUND = 10003            # 资源不存在
    RATE_LIMITED = 10004         # 限流
    DUPLICATE = 10005            # 资源重复

    # 用户模块
    USER_NOT_FOUND = 20001       # 用户不存在
    USER_DISABLED = 20002        # 用户已禁用
    USERNAME_DUPLICATE = 20003   # 用户名已存在
    PASSWORD_WRONG = 20005       # 密码错误

    # 订单模块
    ORDER_NOT_FOUND = 30001      # 订单不存在
    ORDER_STATUS_INVALID = 30002 # 订单状态不允许操作


# 错误码 -> 消息映射
ERROR_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.VALIDATION_ERROR: "参数校验失败",
    ErrorCode.UNAUTHORIZED: "未认证，请先登录",
    ErrorCode.USER_NOT_FOUND: "用户不存在",
    # ...
}
```

---

## 版本控制

### URL Path 版本（推荐，简单直观）

```
# 推荐方式 — URL 路径中包含版本号
GET /api/v1/users
GET /api/v2/users

# 优点：直观、易调试、CDN 友好
# 缺点：版本升级时需要新路由
```

```java
// Java — 多版本控制器
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 {
    @GetMapping("/{id}")
    public ApiResponse<UserVO> getUser(@PathVariable Long id) {
        // v1 返回基础字段
        return ApiResponse.success(userService.getUserBasic(id));
    }
}

@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 {
    @GetMapping("/{id}")
    public ApiResponse<UserDetailVO> getUser(@PathVariable Long id) {
        // v2 返回完整字段，含新增的 profile 信息
        return ApiResponse.success(userService.getUserDetail(id));
    }
}
```

### Header 版本（适合字段级变更）

```
# 通过 Accept 头指定版本
GET /api/users
Accept: application/vnd.myapp.v2+json

# 或自定义头
GET /api/users
X-API-Version: 2
```

### 版本策略建议

```
1. 新项目从 v1 开始
2. 非破坏性变更（新增字段）不升版本
3. 破坏性变更（删除/改名字段、修改语义）升大版本
4. 最多同时维护 2 个版本（当前版本 + 上一版本）
5. 旧版本至少保留 6 个月后下线，提前通知调用方
```

---

## 认证方式

### JWT + 刷新令牌

```
认证流程:
1. 用户登录 → 返回 accessToken（短期）+ refreshToken（长期）
2. 请求携带 accessToken → Authorization: Bearer <token>
3. accessToken 过期 → 用 refreshToken 换取新 accessToken
4. refreshToken 过期 → 重新登录
```

### 接口设计

```
POST /api/v1/auth/login          # 登录
POST /api/v1/auth/refresh        # 刷新令牌
POST /api/v1/auth/logout         # 登出（废弃当前令牌）
```

### 代码实现

```java
// Java — 登录响应
public record LoginResponse(
    String accessToken,      // 访问令牌，有效期 30 分钟
    String refreshToken,     // 刷新令牌，有效期 7 天
    long expiresIn,          // accessToken 过期时间（秒）
    String tokenType         // 固定 "Bearer"
) {}

// 登录接口
@PostMapping("/api/v1/auth/login")
public ApiResponse<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
    // 1. 验证用户名密码
    User user = authService.authenticate(request.getUsername(), request.getPassword());

    // 2. 生成令牌对
    String accessToken = jwtService.generateAccessToken(user);
    String refreshToken = jwtService.generateRefreshToken(user);

    // 3. 将 refreshToken 存入 Redis（支持主动废弃）
    redisService.setRefreshToken(user.getId(), refreshToken, Duration.ofDays(7));

    return ApiResponse.success(new LoginResponse(
        accessToken, refreshToken, 1800, "Bearer"
    ));
}

// 刷新令牌接口
@PostMapping("/api/v1/auth/refresh")
public ApiResponse<LoginResponse> refresh(@RequestBody RefreshRequest request) {
    // 1. 验证 refreshToken
    Claims claims = jwtService.parseRefreshToken(request.getRefreshToken());

    // 2. 检查 Redis 中是否存在（已登出的会被删除）
    String stored = redisService.getRefreshToken(claims.getUserId());
    if (!request.getRefreshToken().equals(stored)) {
        throw new BusinessException(ErrorCode.UNAUTHORIZED);
    }

    // 3. 生成新的令牌对（令牌轮换，提高安全性）
    User user = userService.getById(claims.getUserId());
    String newAccessToken = jwtService.generateAccessToken(user);
    String newRefreshToken = jwtService.generateRefreshToken(user);

    // 4. 替换 Redis 中的 refreshToken
    redisService.setRefreshToken(user.getId(), newRefreshToken, Duration.ofDays(7));

    return ApiResponse.success(new LoginResponse(
        newAccessToken, newRefreshToken, 1800, "Bearer"
    ));
}
```

### 安全建议

```
1. accessToken 有效期短（15-30 分钟）
2. refreshToken 有效期长（7-30 天），存 Redis 支持主动废弃
3. 每次 refresh 时轮换 refreshToken（防重放攻击）
4. 登出时删除 Redis 中的 refreshToken
5. accessToken 只放必要信息（userId、role），不放敏感数据
6. 使用 HTTPS，防止令牌被截获
7. 前端 accessToken 存内存，refreshToken 存 httpOnly cookie
```

---

## OpenAPI/Swagger 文档规范

### 文档要求

```
1. 每个接口必须包含：summary（一句话描述）、description（详细说明）
2. 所有参数必须有 description 和示例值
3. 所有响应码必须有对应的 schema 定义
4. 使用 tags 对接口分组
5. 请求/响应示例必须是真实可用的数据
```

### OpenAPI 示例

```yaml
# api/openapi.yaml
openapi: 3.0.3
info:
  title: 用户服务 API
  description: 用户注册、登录、信息管理等接口
  version: 1.0.0

servers:
  - url: https://api.example.com
    description: 生产环境
  - url: https://api-staging.example.com
    description: 预发布环境

tags:
  - name: 用户管理
    description: 用户 CRUD 操作
  - name: 认证
    description: 登录、登出、刷新令牌

paths:
  /api/v1/users:
    post:
      tags: [用户管理]
      summary: 创建用户
      description: 注册新用户，用户名和邮箱不可重复
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            example:
              username: zhangsan
              email: zhang@example.com
              password: "Abc12345"
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          description: 参数校验失败
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                code: 10000
                message: 参数校验失败
                data:
                  errors:
                    - field: email
                      message: 邮箱格式不正确

    get:
      tags: [用户管理]
      summary: 获取用户列表
      description: 分页查询用户列表，支持按用户名模糊搜索
      operationId: listUsers
      parameters:
        - name: page
          in: query
          description: 页码（从 1 开始）
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: size
          in: query
          description: 每页条数
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - name: keyword
          in: query
          description: 搜索关键词（模糊匹配用户名）
          schema:
            type: string
      responses:
        '200':
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'

components:
  schemas:
    CreateUserRequest:
      type: object
      required: [username, email, password]
      properties:
        username:
          type: string
          minLength: 3
          maxLength: 32
          description: 用户名
        email:
          type: string
          format: email
          description: 邮箱地址
        password:
          type: string
          minLength: 8
          description: 密码

    UserResponse:
      type: object
      properties:
        code:
          type: integer
          example: 0
        message:
          type: string
          example: success
        data:
          $ref: '#/components/schemas/UserVO'

    UserVO:
      type: object
      properties:
        id:
          type: integer
          format: int64
          description: 用户ID
        username:
          type: string
          description: 用户名
        email:
          type: string
          description: 邮箱

    ErrorResponse:
      type: object
      properties:
        code:
          type: integer
          description: 业务错误码
        message:
          type: string
          description: 错误提示信息
        data:
          type: object
          nullable: true

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: "JWT 访问令牌，格式: Bearer {token}"

security:
  - BearerAuth: []
```

---

## API 设计检查清单

| 检查项 | 说明 |
|--------|------|
| 资源命名 | 名词复数、kebab-case、嵌套不超过两层 |
| HTTP 方法 | GET 查询、POST 创建、PUT 全量更新、PATCH 部分更新、DELETE 删除 |
| 状态码 | 成功 200/201/204，客户端错误 4xx，服务端错误 5xx |
| 响应格式 | 统一 code/message/data 结构 |
| 分页 | page 从 1 开始，size 有上限，返回 total 和 totalPages |
| 错误码 | 5 位整数，按模块分段，message 面向用户 |
| 版本 | URL 路径版本 /api/v1/，最多维护两个版本 |
| 认证 | JWT + refreshToken，accessToken 短期有效 |
| 文档 | OpenAPI 3.0，每个接口有 summary/description/example |
| 安全 | HTTPS、输入校验、限流、错误信息不泄露内部细节 |
| 幂等性 | POST 用业务唯一键去重，PUT/DELETE 天然幂等 |
| 时间格式 | ISO 8601（`2026-03-14T10:00:00Z`），统一 UTC |
