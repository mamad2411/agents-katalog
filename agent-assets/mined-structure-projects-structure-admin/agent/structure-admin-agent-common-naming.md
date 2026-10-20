---
name: common-naming
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 naming Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/naming.md`（完整规范）。以下为操作要点：


# 通用命名与注释规范

> 完整规范详见 `wiki/_common/naming.md`

## 通用命名规则（MUST）

- **MUST** 使用有意义的英文单词，禁止拼音、无意义缩写。
- **MUST** 类名/接口名：`UpperCamelCase`（如 `UserService`、`OrderRepository`）。
- **MUST** 方法名/变量名：`lowerCamelCase`（如 `findById`、`userName`）。
- **MUST** 常量名：`UPPER_SNAKE_CASE`（如 `MAX_RETRY_COUNT`）。
- **MUST** 包名：全小写，单词间无分隔符（如 `com.example.admin.biz.service`；structure-boot 项目用 `cn.structured.*`）。
- **MUST** 数据库表名/字段名：`lower_snake_case`（如 `user_role`、`create_time`）。
- **SHOULD** REST API URL：`kebab-case`（如 `/api/user-roles`）。

## Java 注释规范（MUST）

### 类头注释

```java
/**
 * 用户管理服务实现
 *
 * @author zhangsan
 * @version 1.2.0
 * @since JDK 17 2025-07-31
 */
```

- **MUST** `@version` 与项目版本号同步更新。
- **SHOULD** `@since` 记录首次创建的 JDK 版本与日期。

### 方法注释

每个 public/protected 方法 MUST 包含 JavaDoc：

```java
/**
 * 根据用户 ID 查询用户信息
 *
 * @param userId 用户 ID
 * @return 用户视图对象，不存在返回 null
 */
```

- **MUST** `@param` 描述每个参数的含义与约束。
- **MUST** `@return` 描述返回值的含义与可能为 null 的情况。

完整规则以 `wiki/_common/naming.md` 为准。
