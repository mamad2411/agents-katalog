---
name: koishi-plugin-install
description: 直接为 Koishi 项目安装插件并写入配置，覆盖包管理器识别、官方/第三方插件包名解析、依赖安装、配置启用、secret 占位、最小验证和失败回滚报告。
---

# Koishi 插件安装

这个 skill 用于让 AI **直接安装并启用 Koishi 插件**。适用于用户明确要求“安装插件”“加一个官方插件”“接入平台插件”“加数据库/控制台/sandbox/auth/server”等场景。

> 边界：只修改已有配置、不涉及依赖安装时用 `koishi-config-edit`。

## 行动目标

收到插件安装请求后，优先完成这些动作：

1. 识别 Koishi 项目、包管理器、workspace 和 `koishi.yml`。
2. 确定插件包名与插件名。
3. 检查依赖是否已安装。
4. 安装缺失依赖。
5. 写入或更新 Koishi 配置。
6. 保护 token/password/secret 等敏感字段。
7. 运行最小验证。
8. 报告安装、配置、验证和待补充事项。

不要只给用户安装命令。只要项目可修改且用户目标明确，就实际编辑文件并运行合适命令。

## 触发场景

使用本 skill 的典型请求：

- “帮我安装 Koishi 插件。”
- “装一下 sandbox / logger / status / auth / server。”
- “给项目加 SQLite 数据库插件。”
- “安装并启用 Telegram adapter。”
- “我要控制台插件组合，帮我配好。”
- “给 Koishi 加 proxy-agent。”
- “安装第三方 koishi-plugin-xxx 并启用。”

## 第一步：识别项目

先读取并判断：

```text
package.json
pnpm-lock.yaml
yarn.lock
package-lock.json
bun.lockb
koishi.yml
```

判断内容：

- 使用 npm / yarn / pnpm / bun。
- 是否 workspace。
- 现有插件配置结构。

## 第二步：确定插件包名和插件名

Koishi 插件通常有两层名称：

| npm 包名 | 插件名 |
|---|---|
| `@koishijs/plugin-sandbox` | `sandbox` |
| `@koishijs/plugin-database-sqlite` | `database-sqlite` |
| `@koishijs/plugin-adapter-telegram` | `adapter-telegram` |
| `koishi-plugin-example` | `example` |
| `@scope/koishi-plugin-example` | `@scope/example` |

规则：

- 官方插件列表如下：
  - adapter：`adapter-dingtalk`、`adapter-discord`、`adapter-kook`、`adapter-lark`、`adapter-line`、`adapter-mail`、`adapter-matrix`、`adapter-qq`、`adapter-satori`、`adapter-slack`、`adapter-telegram`、`adapter-wechat-official`、`adapter-wecom`、`adapter-whatsapp`、`adapter-zulip`。
  - database：`database-memory`、`database-mongo`、`database-mysql`、`database-postgres`、`database-sqlite`。
  - common：`admin`、`bind`、`broadcast`、`callme`、`echo`、`help`、`inspect`。
  - console：`analytics`、`auth`、`commands`、`config`、`console`、`explorer`、`insight`、`locales`、`logger`、`market`、`sandbox`、`status`。
  - develop：`hmr`、`http`、`mock`、`notifier`、`proxy-agent`、`server`、`server-satori`、`server-temp`、`server-proxy`。
- 用户给出插件名时，先判断是否属于官方插件；如果是，推测 npm 包名为 `@koishijs/plugin-<插件名>`。
- 用户给出的插件名不属于官方插件时，先按第三方插件推测 npm 包名：`example` 对应 `koishi-plugin-example`，`@s/a` 对应 `@s/koishi-plugin-a`。
- 不确定包名时先搜索项目已有依赖和用户提供名称；仍不确定再向用户确认。

## 第三步：选择安装命令

根据锁文件和 package manager 字段选择：

| 项目特征 | 命令 |
|---|---|
| `pnpm-lock.yaml` | `pnpm add <pkg>` |
| `yarn.lock` | `yarn add <pkg>` |
| `package-lock.json` | `npm install <pkg>` |
| `bun.lockb` | `bun add <pkg>` |
| 无锁文件但 packageManager 指定 | 使用指定包管理器 |
| 都没有 | 默认 npm，并在报告中说明 |

workspace 项目：

- 先判断 Koishi 应用包所在 workspace。
- 依赖应安装到 Koishi 应用包，而不是仓库根，除非根就是应用包。
- npm workspace 可使用：`npm install <pkg> -w <workspace>`。
- yarn workspace 可使用：`yarn workspace <workspace> add <pkg>`。
- pnpm 可在目标包目录运行 `pnpm add <pkg>` 或使用 filter。

不要把运行时插件误装成 devDependency；除非插件只用于测试，例如 `@koishijs/plugin-mock`。

## 第四步：写入 Koishi 配置

安装后使用 `koishi-config-edit` 的规则修改配置。

## Secret 处理

以下字段默认敏感：

```text
token
secret
password
appSecret
accessKey
accessToken
refreshToken
```

规则：

- 不要把真实 token/password 写入仓库，除非用户明确授权。
- 优先写环境变量占位，或提醒用户在控制台中填写。
- 如果项目已有 `.env.local`，可以补环境变量名；不要擅自创建真实 `.env` 存放 secret。
- 终端输出和最终报告隐藏 secret。

## 验证步骤

安装与配置后，按可用性验证：

1. `koishi.yml` 语法有效。
2. 用户要求确认运行时，可启动 Koishi 或使用 `run` skill。

常用命令：

```bash
npm install <pkg>
yarn add <pkg>
pnpm add <pkg>
npm run build
npm test
npm start
```

如果安装命令失败：

- 不要继续写入“已安装”结论。
- 检查包名、网络、registry、包管理器、workspace 目标。
- 如果已经改了配置但依赖未安装，报告配置处于“需要补安装”的状态，必要时回滚配置修改。

## 回滚与安全

安装或配置过程中出现问题：

- 如果依赖安装失败且配置尚未修改，不需要回滚。
- 如果配置已修改但插件未安装，优先回滚配置或明确报告不一致状态。
- 不要删除用户原有复杂配置块。
- 不要删除锁文件。
- 不要运行破坏性包管理命令，例如清空 node_modules、重置 lockfile，除非用户明确授权。

## 常见失败处理

### 插件已安装但未启用

直接写入配置启用，不重复安装。

### 配置已启用但依赖缺失

安装依赖，然后验证。

### 用户给的是插件名不是包名

先判断是否为官方插件名：

- 是官方插件：推测为 `@koishijs/plugin-<插件名>`。
- 不是官方插件：先按第三方插件推测为 `koishi-plugin-<插件名>`；若带 scope，则推测为 `@scope/koishi-plugin-<名称>`。

例如用户说 `sandbox`，它是官方插件，解析为：

```text
sandbox -> @koishijs/plugin-sandbox
```

### 第三方包名无法确认

先询问用户确认包名，不要猜一个可能不存在的包。
