---
name: koishi-config-edit
description: 直接识别并修改 Koishi 应用配置文件 koishi.yml，覆盖插件启停、插件组创建与整理等配置变更与验证。
---

# Koishi 配置修改

这个 skill 用于让 AI **直接修改 Koishi 应用配置文件 `koishi.yml`**，而不是只解释配置项。适用于用户明确要求“帮我改 Koishi 配置”“启用/禁用插件”“创建/整理插件组”“配置 server/selfUrl/adapter/database/auth/sandbox/console”等场景。

> 边界：如果用户还需要安装缺失插件，先转用 `koishi-plugin-install`。

## 背景原则

Koishi 建立在 Cordis 的上下文、插件、服务、生命周期与副作用回收模型之上。配置修改本质上是在调整 Koishi 应用启动时加载的插件树：

- `plugins` 下每个键是一份插件配置，值是该插件的配置对象。
- `group:*` 是特殊插件组，可嵌套，用于整理插件并批量控制组内插件行为。
- 插件名前缀 `~` 表示该插件配置存在但不启用。
- 插件名后缀 `:xxx` 是插件实例 ID / 别名，例如 `commands:ucxgnw: {}`；它用于区分同一插件的不同配置实例，也常由控制台随机生成。
- 以 `$` 开头的字段是插件或插件组元信息，例如 `$collapsed`、`$filter`、`$if`、`$isolate`。

修改时要尊重 Koishi 的可逆插件系统：停用插件应优先保留配置，避免无意删除业务配置或 secret。

## 行动目标

收到配置修改请求后，优先完成这些动作：

1. 定位 Koishi 项目和唯一配置文件 `koishi.yml`。
2. 判断现有 YAML 结构、插件分组、插件实例 ID、禁用风格和元信息。
3. 只修改用户目标相关的最小配置。
4. 保护 secret，不擅自写入真实凭据。
5. 修改后做 YAML 语法或启动级验证。
6. 用文件路径和配置项摘要报告结果。

不要把回答停留在“你应该这样配置”。只要仓库中存在可修改的 `koishi.yml`，且需求足够明确，就直接修改。

## 第一步：定位配置文件

查找 Koishi 应用目录下名为 `koishi.yml` 的配置文件。

## 第二步：识别配置结构

`koishi.yml` 常见结构类似：

```yaml
plugins:
  group:server:
    server:mw5hp6:
      port: 5140
      maxPort: 5149
    ~server-satori:91kcoc: {}
    ~server-temp:ljg4l9: {}
  group:storage:
    database-sqlite:1k8bsn:
      path: data/koishi.db
```

要点：

- `plugins` 是 YAML 对象，每个键对应一份插件配置，每个值对应该配置实例的配置对象。
- **无配置的插件一律写成 `xx: {}` 或 `xx:实例ID: {}`，不要写成空值 `xx:`。**
- `~plugin` 表示该插件不会被启用，但配置仍保留。
- `plugin:实例ID` 表示插件实例 ID / 别名，例如 `commands:ucxgnw`、`server:mw5hp6`；它用于区分同一插件的不同配置实例，控制台创建的实例通常会带随机 ID。
- 同一插件存在多份配置时，必须通过不同实例 ID 区分，例如 `adapter-telegram:main`、`adapter-telegram:backup`。
- `group:name` 表示插件组，组内结构与 `plugins` 一致，可嵌套。
- `$collapsed`、`$filter`、`$if`、`$isolate` 等以 `$` 开头的字段是元信息，不是普通插件。

行动规则：

- 先保持现有配置风格，不随意重排所有插件。
- 现有插件键带实例 ID 时，启用、禁用、移动和修改配置都必须保留该实例 ID。
- 新增插件时，优先沿用现有文件风格：如果同组插件普遍带随机实例 ID，应给新插件也补一个短实例 ID；如果项目没有实例 ID 风格，则可只用插件名。
- 有 `group:*` 时优先把新插件放进语义相近的 group。
- 不要删除未知插件、未知字段或 `$` 元信息。
- 不要因为字段没有出现在 skill 示例中就判断它无效。
- 不要把 YAML 整体重写成另一种结构，除非当前文件已损坏且用户要求修复。

## 第三步：修改插件配置

### 启用插件

启用已有插件配置时，确保对应键不带 `~` 前缀，并保留实例 ID：

```yaml
plugins:
  group:console:
    sandbox:sny8uj: {}
```

如果需要配置项：

```yaml
plugins:
  group:server:
    server-satori:91kcoc:
      path: /satori
```

若现有配置是 `~sandbox:sny8uj: {}`，启用时优先改成 `sandbox:sny8uj: {}`，保留其原有配置内容、实例 ID 与位置。

### 禁用 / 停用插件

Koishi 配置文件中的标准禁用方式是给插件配置键加 `~` 前缀：

```yaml
plugins:
  group:console:
    ~sandbox:sny8uj: {}
```

禁用规则：

- 如果用户明确要求删除配置，可以删除该插件配置块。
- 删除前确认该插件配置没有明显业务数据、复杂自定义字段或 secret；如有，优先使用 `~` 禁用或询问用户。
- 不要擅自删除 adapter token、数据库连接串等敏感配置块，除非用户明确要求。

控制台中的“停用插件”不会删除插件代码，也不会删除插件配置；手动改 `koishi.yml` 时也应遵循这个原则。

### 创建插件组

插件组是名为 `group` 的特殊插件，键名格式为 `group:组名:`。在 `plugins` 下创建新组：

```yaml
plugins:
  group:console:
    console:wsiqhe:
      open: true
    config:7cetf5: {}
    logger:hon33i: {}
    status:32moou: {}
    sandbox:sny8uj: {}
```

创建规则：

- 组名使用能表达用途的短名称，例如 `server`、`console`、`adapter`、`storage`、`basic`、`develop`、`official`。
- 保持 YAML 键名末尾的冒号，例如 `group:console:`。
- 将插件移动进组时，只改变所在层级，不改变插件自身配置、实例 ID、启停状态或元信息。
- 如果用户要求批量管理一组插件，优先创建插件组，而不是复制多份配置。

嵌套示例：

```yaml
plugins:
  group:official:
    help:tpg7um: {}
    group:console:
      market:yrk7to:
        search:
          endpoint: https://registry.koishi.chat/index.json
      config:7cetf5: {}
```

### 插件组和插件元信息

以 `$` 开头的字段记录插件或插件组元信息，应该保留并按需补充。

折叠插件组：

```yaml
plugins:
  group:console:
    $collapsed: true
    console:wsiqhe:
      open: true
    logger:hon33i: {}
```

按条件启用插件：

```yaml
plugins:
  group:console:
    desktop:2eskdh:
      $if: env.KOISHI_AGENT?.includes('Desktop')
```

会话过滤器示例：

```yaml
plugins:
  group:console:
    status:32moou:
      $filter:
        $eq:
          - $: platform
          - telegram
```

服务隔离示例：

```yaml
plugins:
  group:isolated-db:
    $isolate:
      - database
    database-mysql:7dbt5b:
      database: koishi
    github:abc123: {}
```

规则：

- 不要把 `$` 字段当作插件启停对象处理。
- 移动插件或插件组时，必须带上其内部 `$` 元信息。
- 只有用户明确要求隔离服务时才添加 `$isolate`；错误隔离 database 等核心服务可能导致其他插件访问不到服务。
- 过滤器可作用于插件组，适合“这一组插件只在某些平台 / 群 / 用户中生效”的需求。

### 修改配置项

只改目标字段。例如用户要求改公网地址，只改 server 插件里的 `selfUrl`：

```yaml
plugins:
  group:server:
    server:mw5hp6:
      selfUrl: https://bot.example.com
```

不要顺手改 `port`、adapter、auth 等无关配置。

## 常见配置任务

### server / selfUrl

```yaml
plugins:
  group:server:
    server:mw5hp6:
      host: 0.0.0.0
      port: 5140
      maxPort: 5149
      selfUrl: https://bot.example.com
```

规则：

- `host` 是 server 插件监听地址。
- `port` 是 server 插件监听的初始端口。
- `maxPort` 是端口被占用时允许尝试的最大端口。
- `selfUrl` 是 Koishi 服务暴露在公网的地址。
- webhook、server-satori、assets-local 等通常需要正确 `selfUrl`。
- 公网控制台应提醒启用 `auth`，不要直接暴露未认证控制台。

## Secret 和外部凭据规则

- 不要从日志、截图、历史文件中复制 secret 到新位置。
- 不要把真实 secret 写入可能提交的配置文件，除非用户明确要求这样做。
- 优先使用环境变量占位：`${{ env.NAME }}` 或项目已有写法。
- Koishi 原生支持 dotenv，通常可使用 `.env.local` 存放真实隐私信息；不要默认提交真实 `.env.local`。
- 如果需要真实凭据才能完成配置，询问用户提供或让用户之后自行填写。
- 报告时隐藏 secret，只显示字段已配置或使用了哪个环境变量名。

## 编辑规则

- 修改前必须读取目标文件。
- 只编辑 `koishi.yml`。
- 保留注释、缩进、插件分组、插件实例 ID、元信息和原有顺序。
- 使用最小 diff。
- YAML 中不要随意改变字符串引号风格。
- 无配置插件一律写成 `{}`，不要写成空值。
- 不要把未知插件从配置中移除。
- 不要把 `$` 开头元信息当成插件删除或禁用。
- 禁用插件优先加 `~` 前缀，而不是删除配置块。
- 如果当前配置明显损坏，先报告损坏点，再提出修复；不要静默大规模重写。

## 验证步骤

按项目可用能力从轻到重验证：

1. YAML 语法检查。
2. 如果用户要求确认可运行，可使用项目启动命令。

不要为了验证而执行高风险外部动作，例如修改 DNS、防火墙、线上数据库，除非用户明确授权。

## 常见失败处理

- 找不到 `koishi.yml`：报告未找到配置文件，并询问 Koishi 应用目录；不要改其他疑似配置文件。
- 插件未安装：不要只写配置；转 `koishi-plugin-install` 安装后再启用。
- 缺少 secret：写环境变量占位或询问用户。
- 启动失败：保留修改，报告日志关键错误；如果是配置错误，继续修复。
- 用户要求删除复杂配置：先确认是否保留备份或改为 `~` 禁用。
