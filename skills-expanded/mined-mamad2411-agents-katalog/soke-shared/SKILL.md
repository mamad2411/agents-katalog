---
name: soke-shared
version: 1.0.0
description: "授客CLI共享基础：应用配置初始化、认证登录（auth login）、权限管理、错误处理、安全规则。当用户需要第一次配置（soke-cli config init）、使用登录授权（soke-cli auth login）、遇到权限不足、或首次使用soke-cli时触发。"
---

# soke-cli 共享规则

本技能指导你如何通过soke-cli操作授客AI资源，以及有哪些注意事项。

## 配置初始化

首次使用需运行 `soke-cli config init` 完成应用配置。

当你帮用户初始化配置时，引导用户按照交互式提示完成配置：

```bash
# 初始化配置
soke-cli config init
```

配置项包括：
- `app_key`: 开放平台应用Key
- `app_secret`: 开放平台应用Secret
- `api_base_url`: API地址（默认: https://opendev.soke.cn）
- `corpid`: 企业ID

配置文件保存在 `~/.soke-cli/config.json`

## 认证

### 用户登录

用户需要通过OAuth授权获取访问令牌：

```bash
# 用户登录授权
soke-cli auth login
```

登录成功后，`access_token` 和 `refresh_token` 会自动保存到配置文件中。

### Token管理

- **access_token**: 用户访问令牌，用于调用API
- **refresh_token**: 刷新令牌，用于获取新的access_token
- Token过期后需要重新执行 `soke-cli auth login`

### 查看当前配置

```bash
# 查看当前配置（不显示敏感信息）
soke-cli config show
```

## 权限不足处理

遇到权限相关错误时，通常有以下几种情况：

### 1. 未登录或Token过期

**错误特征**: 返回401 Unauthorized或Token无效

**解决方案**:
```bash
soke-cli auth login
```

### 2. 缺少必要权限

**错误特征**: 返回403 Forbidden或权限不足提示

**解决方案**:
- 联系管理员在开放平台后台为应用开通相应权限
- 确认企业ID（corpid）和应用配置正确

### 3. 参数错误

**错误特征**: 返回400 Bad Request或参数验证失败

**解决方案**:
- 检查必需参数是否提供
- 使用 `--help` 查看命令参数说明
- 参考API文档确认参数格式

## 命令结构

### Shortcuts（推荐）

Shortcuts是对常用操作的高级封装，参数友好，最适合AI Agent调用：

```bash
soke-cli <service> +<verb> [flags]
```

示例：
```bash
soke-cli exam +get-exam-user --exam-id exam123 --dept-user-id user456
soke-cli course +list-courses --page 1 --page-size 10
```

### 通用API调用

支持直接调用任意API：

```bash
soke-cli api <METHOD> <path> [--data <json>] [--params <json>]
```

示例：
```bash
soke-cli api GET /users/me
soke-cli api POST /some/endpoint --data '{"key": "value"}'
```

## 输出格式

### JSON格式（默认）

所有命令默认输出JSON格式，便于程序解析：

```bash
soke-cli exam +list-exams --format json
```

### 表格格式

部分命令支持表格格式输出，更易读：

```bash
soke-cli exam +list-exams --format table
```

## 安全规则

- **禁止输出密钥**（app_secret、access_token）到终端明文
- **写入/删除操作前必须确认用户意图**
- 敏感操作建议先使用 `--dry-run`（如果支持）预览

## 错误处理

当命令执行失败时：

1. **检查配置**: 运行 `soke-cli config show` 确认配置正确
2. **检查登录状态**: 如果是认证错误，运行 `soke-cli auth login`
3. **检查参数**: 使用 `soke-cli <service> <command> --help` 查看参数说明
4. **查看错误信息**: 错误响应中通常包含详细的错误原因

## 常见问题

### Q: 如何获取app_key和app_secret？

A: 登录授客AI开放平台（https://opendev.soke.cn），创建应用后即可获取。

### Q: Token过期了怎么办？

A: 重新执行 `soke-cli auth login` 进行授权。

### Q: 如何切换企业？

A: 运行 `soke-cli config init` 重新配置，或直接编辑 `~/.soke-cli/config.json` 文件。

### Q: 支持哪些业务模块？

A: 目前支持以下模块：
- `contact`: 组织架构（部门、用户、岗位、讲师）
- `course`: 课程管理
- `exam`: 考试管理
- `training`: 培训管理
- `learning_map`: 学习地图
- `credit`: 学分管理
- `point`: 积分管理
- `news`: 资讯管理
- `certificate`: 证书管理
- 等等...

每个模块都有对应的Skill，AI Agent会根据用户意图自动选择。

## 相关链接

- 授客AI开放平台: https://opendev.soke.cn
- NPM包: @sokeai/cli
- 代码仓库: https://codeup.aliyun.com/5edbc121d1d1abe63b55f1c7/soke/soke-cli.git
