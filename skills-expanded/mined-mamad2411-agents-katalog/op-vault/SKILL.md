---
name: op-vault
description: 当 AI agent 需要凭据（密码 / token / API key / 连接串）来跑命令时，用 1Password 里存的对应 item 把命令跑起来，密钥明文不进对话或输出。检测到命令缺密码、token、API key、连接串，或环境变量名形如 *_PASSWORD / *_TOKEN / *_API_KEY 时触发；也可用昵称点名 vault（"dev vault" / "work vault" / "private vault"）或说"用 1Password 里的 X 跑 Y"。Use when an agent needs a secret from 1Password to run a command. 需要装了 op CLI 且开启 1Password 桌面 App 集成；不做密钥的存储 / 创建 / 轮换，只读取与注入。
license: MIT
metadata:
  category: secrets
  language: zh-CN, en
---

# op-vault

从 1Password 取凭据，注入到要跑的命令里，密钥明文不落进 agent 的对话 / 输出。底层全是
`op` CLI，这层封装只省去手敲 `op://` 路径，并守住一条线：**别让明文落进会被持久化的输出**。
人自己敲 `op` 不需要它，直接 `op run` 就行。

## 何时用

- agent 要跑的命令缺凭据才能继续（缺密码 / token / API key / 连接串，或环境变量名形如
  `*_PASSWORD` / `*_TOKEN` / `*_API_KEY`）。
- 用户点名 vault（"dev vault"）、说"用 1Password 里的 X 跑 Y"。

默认**先查后问**：先去 1Password 找；有把握的匹配，先说用的是哪个 item 再注入；找不到或有
歧义才问用户。绝不拿猜的凭据静默注入。

## 流程

1. **鉴权**：`op whoami`。报错就让用户解锁 1Password 桌面 App（必要时 `op signin`），然后停。
2. **找 vault / item**：
   - 有 vault 线索：`op vault list --format json | python3 -c "import json,sys;print([v.get('name') for v in json.load(sys.stdin)])"`
     模糊匹配昵称；没线索就跳过这步，找 item 时不带 `--vault` 直接跨库搜。
   - 找 item（同样只抽标题 + id + vault 名——list 的原始 JSON 里 `additional_information` 会
     带出 login 的 username，别直接打印；标题、id、vault 名不敏感，注入引用 `op://<Vault>/…`
     和归档兜底都要用）：

     ```bash
     op item list --vault <V> --format json | python3 -c "import json,sys;print([(i.get('title'),i.get('id'),(i.get('vault') or {}).get('name')) for i in json.load(sys.stdin)])"
     ```

     按服务名 / 标题模糊匹配；没把握、或跨库撞了同名，就把 vault + 标题列给用户选。
3. **看字段（只抽 label，别 dump 原始输出——关键）**：`op item get --format json` 的**原始
   输出里带明文**（不加 `--reveal` 也一样，实测会带出值），所以**绝不直接打印原始输出**，
   只把 label 抽出来看；也别用 `op read` 去"看一眼"值：

   ```bash
   op item get <ITEM> --vault <V> --format json | python3 -c "import json,sys;print([f.get('label') for f in json.load(sys.stdin).get('fields',[]) if f.get('label')])"
   ```

   从 label 列表确认 `username` / `password` / `credential` 等哪些字段在。
4. **定环境变量名**：用目标命令真正会读的名字（psql 读 `PGUSER` / `PGPASSWORD`，docker compose
   用 compose 文件里引用的名字）——名字注错，命令收不到凭据，会转头交互式要密码或直接失败。
   命令没有约定名、或自己包 `sh -c` 引用变量时，名字自己定（label 转大写或取个语义名如
   `TOKEN` 都行，引用处一致即可）；用户点名了就用用户的（"as PGUSER/PGPASSWORD"）。
5. **注入并执行**（见下）。密钥不打印，只回报退出码和命令输出。

## 注入（默认一种）

```bash
<VAR1>="op://<Vault>/<Item>/username" <VAR2>="op://<Vault>/<Item>/password" op run -- <命令>
```

明文只在 `op run` 子进程里短暂存在，不进当前 shell；命令行里只有 `op://` 引用；`op run`
默认掩码 stdout/stderr。

### 少数例外

- **命令里要引用注入的变量**（如 `$PASSWORD`）：包一层 `op run -- sh -c '...'`（单引号），
  让 `$PASSWORD` 在子进程里展开，否则会在外层 shell 展开成空值。
- **要进交互会话时**（psql / mysql 不带 `-c` / `-e` 进 REPL、ssh 开 shell）：`op run` 会影响
  终端 → 改用内联 `VAR="$(op read 'op://...')" <命令>`；带 `-c` 的一次性执行仍走 `op run`。
  注意这条路径没有 `op run` 的输出掩码兜底，更别回显变量。
- **密钥只能当命令行参数传、又没有 `--password-stdin` 之类选项**：别硬塞（会进 `ps`），
  告诉用户这个工具没有安全的传法。
- **已有用户写好的 `.env.tpl`**：直接 `op run --env-file=.env.tpl -- <命令>`。本 skill 自己
  不建、不提交模板。注意 `.env.tpl` 里的 `op://` 引用会暴露 vault / item / 字段名（不暴露
  值）——私有仓库无所谓，公开前先扫一眼命名。

## 例子

```bash
# 一次性 psql（dev vault 里某 item 的 username/password）
PGUSER="op://Dev/PG/username" PGPASSWORD="op://Dev/PG/password" op run -- psql -h db.internal -c 'select 1'

# docker compose（命令自己读环境变量）
DB_PASSWORD="op://Dev/PG/password" op run -- docker compose up

# 带 bearer token 的 curl（变量要在子进程里展开，所以包一层 sh -c + 单引号）
TOKEN="op://Work/API/credential" op run -- sh -c 'curl -H "Authorization: Bearer $TOKEN" https://api.example.com/me'
```

## 安全底线

- 发现只抽 label / 标题 / id / vault 名这类不敏感字段——`op item get --format json` 原始输出含明文、`op item list` 的
  `additional_information` 带 username，务必管道过滤，别直接打印；不 `--reveal`、不为查看而
  `op read`；缺 python3 这类过滤工具时停下来问，别裸打印原始 JSON。
- 密钥不打印、不回显、不 `set -x` / 不 dump env；靠 `op run` 默认掩码兜底。
- 不在磁盘留明文。

## 错误处理

- 未登录 → 让用户解锁 1Password 桌面 App（开机 / 重启后，CLI 要先解锁 App 才能用），必要时
  `op signin`；没装 `op` 见 <https://developer.1password.com/docs/cli/get-started/>。
- vault / item 找不到或有歧义 → 列候选问用户。
- 字段缺失（Login item 没有 `credential`）→ 只注入存在的，并说明。
- `op run` 报"item 已删除 / 归档"但 item 明明在 → 有同名的已归档 item，按标题解析撞上了它；
  换个唯一标题，或改用 item ID 引用（`op://<Vault>/<item-id>/<field>`）。

## 不做

存储 / 创建 / 轮换 / 编辑密钥；创建或提交 `.env.tpl`；service account / CI / 非交互鉴权。
