---
name: installing-dsh-plugins
description: "Use when installing, updating, removing, or verifying DeepSeek Harness (DSH) plugins or agent skills: cordis-type into a profile via dsh plugin, skill-type into the skills directory; fixing pnpm store-dir mismatches (ERR_PNPM_UNEXPECTED_STORE), verifying with dsh --dump-config, restarting the web server to activate. Trigger on install/add/enable/卸载 a DSH plugin or skill, or a shared plugin repo/tarball URL."
---

# 安装 DeepSeek Harness 插件 / Skills

把插件装进 DSH 的官方流程，以及本机（Windows 便携版，`D:\CODEX\deepseek\DeepSeek-Harness-Portable`）实测踩过的坑。核心原则：**先读仓库 README 确认类型，按官方命令安装，装完必须验证 + 重启**。

## 何时使用

- 用户要安装/添加/更新/卸载 DSH 插件或 skill，或给了一个插件仓库/下载链接（GitHub 等）
- 安装时遇到 `ERR_PNPM_UNEXPECTED_STORE`、插件装了但看不到、需要重启 web 服务生效
- 要装 agent skill（克隆到 skills 目录那种）

不要用于：装普通 npm 库（无 `dsh.bundle` 声明，装了也只是普通依赖）。

## 0. 环境侦察（先做）

```powershell
$env:DSH_HOME          # 本机 = D:\CODEX\deepseek\DeepSeek-Harness-Portable\data
Get-ChildItem "$env:DSH_HOME\profiles" -Directory   # web = GUI 用的 profile
dsh --help             # dsh CLI；`dsh plugin --profile web --help` 看插件子命令
# 运行中的 web 服务（重启时要找它）：
Get-NetTCPConnection -LocalPort 3080 -State Listen | Select OwningProcess
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'dsh-web|--profile web' } | Select ProcessId,CommandLine
```

## 1. 判断插件类型（先读仓库 README）

| 类型 | 特征 | 安装方式 |
|---|---|---|
| cordis 型 | package.json 有 `dsh.bundle`（patch 指向 cordis.patch.yml），README 写 `dsh plugin ... add` | `dsh plugin --profile <name> add <pkg>` |
| skill 型 | 仓库根有 `SKILL.md`（YAML frontmatter） | 克隆进 skills 目录 |
| 普通库 | 无 `dsh.bundle` | 装进去只是依赖，不会成为 profile 层 |

## 2. cordis 型安装

```sh
dsh plugin --profile web add <npm包|git仓库|tarball-url>
```

- `dsh plugin` 会把剩余参数**原样转发给 profile 目录里的 pnpm**（cwd = profile 目录）
- 装成功后自动 reconcile：把声明了 `dsh.bundle` 的依赖写进 `package.json` 的 `dsh.profile.bundles`
- 官方 README 常用形式：`dsh plugin --profile web add https://github.com/<owner>/<repo>/archive/refs/heads/main.tar.gz`

## 3. pnpm store 盘符坑（Windows 高频，必查）

**现象**：`ERR_PNPM_UNEXPECTED_STORE`，pnpm 提示 node_modules 链接自 A store，却想用 `D:\.pnpm-store\v11`。

**原因**（本机实证）：
- pnpm 11 **忽略 `.npmrc` 里的 `store-dir`**（该键不在配置白名单，只认 CLI/env；`pnpm config get store-dir` 返回字面量 `undefined` 属正常）
- 但 pnpm 11 **认 `pnpm-workspace.yaml` 里的 `storeDir`**：本机 web profile 已写 `storeDir: C:\Users\13720\AppData\Local\pnpm\store`，所以 `pnpm store path` 与 `.modules.yaml` 一致、不会报错。装前先看 `pnpm-workspace.yaml`，别误判
- 默认 store 在 C 盘（`%LOCALAPPDATA%\pnpm\store`），项目在 D 盘时无法硬链接，pnpm 自动回退到项目盘符根的 `D:\.pnpm-store\v11`
- 于是 pnpm 想用的 store ≠ node_modules 实际链接的 store → 报错

**诊断**：读 node_modules 实际链接的 store：

```powershell
Select-String -Path "$env:DSH_HOME\profiles\web\node_modules\.modules.yaml" -Pattern "storeDir"
# 例：storeDir: "C:\\Users\\13720\\AppData\\Local\\pnpm\\store\\v11"
```

**修复**：安装命令显式加 `--store-dir=<.modules.yaml 里的 storeDir>`（CLI 优先级最高）：

```sh
dsh plugin --profile web add --store-dir=C:\Users\<user>\AppData\Local\pnpm\store https://github.com/<owner>/<repo>/archive/refs/heads/main.tar.gz
```

后续同步 lockfile 同理：在 profile 目录 `pnpm install --store-dir=...`。

## 4. 验证注册（装完必做）

```powershell
# 组合配置树里应有 "# == <包名>" 段和对应 "- id:" 条目：
dsh --profile web --dump-config | Select-String -Pattern "<包名>"
# profile manifest 的 bundles 列表应包含该包：
Get-Content "$env:DSH_HOME\profiles\web\package.json"
```

`--dump-config` 是**只读**的组合演练（不启动服务器），验证不通过不要继续。

## 5. 重启 web 服务（必须，README 都要求）

插件 host 半区和客户端 bundle 只在**启动时**组合，必须重启才生效。

**关键点：重启会杀掉托管当前会话的服务进程——当前这轮回复会丢失。** 正确姿势：

1. 先把回复写完（本步之前）
2. 用**分离的延迟脚本**执行重启（脚本独立于会话进程，杀服务不影响它）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill目录>\scripts\restart-dsh-web.ps1" -Port 3080 -DelaySeconds 60
```

3. 脚本逻辑：睡 `DelaySeconds`（让当前回复送达）→ 杀掉匹配 `dsh-web.js` / `--profile web --port N` 的 node 进程 → `node dsh-web.js --port N` 重新拉起 → 轮询 `http://127.0.0.1:N/` 出现 `__DSH_BOOT__` → 写状态日志
4. 告诉用户：**页面会断连约 N 秒，刷新浏览器即可**；重启状态看 `data\logs\dsh-restart-status.txt` 最后一行 `ok=True`
5. 杀服务会触发一次自动备份（`backup.cmd`），属正常设计，不用管

兜底：万一新服务没起来，用开始菜单「DeepSeek Harness」快捷方式或根目录 `dsh-web.cmd` 重新拉起。

## 6. skill 型安装

- 克隆/复制到本 harness 的 skills 目录：`$env:DSH_HOME\skills`（本机 = `data\skills`，就是本会话技能列表的目录）
- 结构：`<name>\SKILL.md`，frontmatter 必须含 `name` + `description`（description 写触发条件，不写流程摘要）
- 可带 `scripts/`、`references/` 子资源
- **新 skill 从下一个会话起才出现在可用技能列表**（available_skills 在会话开始时快照）；本机未使用 `~/.agents/skills`（那是 Codex/Copilot 的跨运行时别名）

## 踩坑速查（本机实证）

| 现象 | 原因 | 处理 |
|---|---|---|
| `ERR_PNPM_UNEXPECTED_STORE` | store 盘符不匹配；`.npmrc` 的 store-dir 被 pnpm 11 忽略（但 `pnpm-workspace.yaml` 的 `storeDir` 生效） | 先查 profile 的 `pnpm-workspace.yaml` 是否已写 `storeDir`；没有则显式 `--store-dir=<.modules.yaml 的 storeDir>`（见步骤 3） |
| `ERR_PNPM_IGNORED_BUILDS`（pnpm add 退出码 1） | pnpm 11 默认忽略依赖构建脚本（安全策略）；**且 pnpm 退出非 0 时 reconcile 被跳过**，依赖进了 package.json 但 `dsh.profile.bundles` 没写 | 在 profile 的 `pnpm-workspace.yaml` → `allowBuilds` 把对应包（如 `protobufjs`）设为 `true`，再重跑 `dsh plugin add`。注意：pnpm 11.21 已**不再读** package.json 的 `pnpm` 字段（`pnpm.onlyBuiltDependencies` 被忽略并告警），设置新家就是 `pnpm-workspace.yaml` |
| 装完 `--dump-config` 看不到插件 | 运行中的旧 web 服务带启动快照，可能回写覆盖 profile manifest | 重新注册并等 ~90 秒确认稳定；手动改 manifest 前先停服务 |
| 装完 manifest 里插件"消失" | 同上（服务回写） | 重写 manifest（保留原有插件）+ `pnpm install --store-dir=...` 同步 lockfile，再重启 |
| 重启后页面断连/白屏 | 服务进程被杀 | 刷新浏览器；下次用延迟分离脚本（步骤 5）避免丢回复 |

## 持续改进（反馈回路，必须做）

**本技能是一个会自更新的文档。** 每次用本技能安装，如果遇到**踩坑速查表里没有的新问题/新失败**：

1. 当场解决后，**必须把这次经验沉淀回本文件**——在「踩坑速查」表追加一行（现象 / 原因 / 处理），不要只口头提一句
2. 若本次还发现流程步骤、命令、路径或行为有变化（与本文件描述不一致），同步更新对应步骤
3. 与现有行重复的教训**不要重复追加**；若现有行描述不准确，直接改写该行
4. 更新后，在回复里明确告诉用户「技能已更新：xxx」（让用户知道技能在进化）

失败不算完：**修好本次安装是第一目标，把教训写回技能是同等重要的第二目标**，两步都完成才能收尾。

## 装完怎么用（告诉用户）

- 插件各自的用法看 README 和它的设置页；如 dsh-notification：**Settings → Notifications**，授权通知权限 → 测试通知 → 按需开关各结束原因 / 关键词规则；偏好存在浏览器 localStorage
