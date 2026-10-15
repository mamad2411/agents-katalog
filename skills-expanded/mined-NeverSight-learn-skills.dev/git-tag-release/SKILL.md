---
name: git-tag-release
description: 在规划或执行打 tag、发版、推 RC tag、生成下一个 patch/minor/major 版本号，或需要回写 package.json tag 字段并推送到远端时使用；writing-plans 阶段涉及发版任务时必须使用。
---

# Git Tag Release

## writing-plans 阶段要求

当本技能用于实施计划阶段时，计划必须写清：

- 本技能约束适用于哪些任务。
- 计划的 `Required TRS skills` 中必须列出 `git-tag-release`。
- 目标仓库、remote、tag prefix、versionType、suffix、是否回写 `package.json.tag`。
- 预览、用户确认、执行脚本和推送 tag 的步骤边界。
- 验证方式：预览结果、git status、tag 是否存在、push 结果；发版前需要 `pnpm build` 时，必须先获得用户明确确认。

## 适用场景

- 用户想在当前仓库里按既有规则生成下一个 tag。
- 仓库根目录有 `package.json`，并用 `tagPrefix` 数组维护可选前缀。
- 用户希望从已有 git tags 推导下一个 `major`、`minor`、`patch` 或 `RC` 版本。
- 用户希望可选地把结果写回 `package.json.tag`，提交 `package.json`，再创建并推送 tag。

## 核心原则

- 始终先预览，再执行。
- 预览阶段把“将要打的 tag”明确展示给用户。
- 如果用户改参数，就重新预览。
- 一旦用户确认，用预览产出的最终 tag 原样传给执行脚本，避免 `RC` 时间戳漂移。

## 参考文档

- 需要判断提交粒度、提交信息或 MR/PR 说明时，读取 `references/git.md`。

## Bundled Script

使用 skill 自身目录里的 `scripts/git-tag-release.cjs`，不要手写一整串 git 命令。

不要在 bash 里写相对路径 `node scripts/git-tag-release.cjs ...`。

原因：命令通常会在目标仓库目录执行，相对路径会指向当前仓库的 `scripts/`，而不是 skill 目录本身。无论 skill 安装在项目本地还是全局目录，都必须先从当前已加载的 skill 元信息里拿到 `Base directory for this skill`，将其中的 `file://` 路径转换为本地绝对路径，再执行脚本。

示意：

```text
Base directory for this skill: file:///Users/name/.agents/skills/git-tag-release
=> 本地脚本绝对路径: /Users/name/.agents/skills/git-tag-release/scripts/git-tag-release.cjs
```

它有两个子命令：

- `preview`
  读取仓库配置、拉取 tags、计算候选 tag、输出风险和将执行的动作。
- `execute`
  再次校验并正式执行：可选回写 `package.json.tag`、提交 `package.json`、创建 tag、推送 tag。

## AI 工作流

### 1. 收集参数

至少确认：

- `cwd`
- `remote`
- `prefix`
  可为空；如果用户没指定，就先用默认前缀预览
- `versionType`
  允许值：`major`、`minor`、`patch`、`RC`
- `suffix`
- `editPkg`

默认值建议：

- `versionType=patch`
- `suffix=""`
- `editPkg=true`
- `remote` 默认取第一个 remote
- `prefix` 默认取 `package.json.tagPrefix[0]`

### 2. 运行预览

```bash
node "/absolute/path/to/git-tag-release/scripts/git-tag-release.cjs" preview --cwd /path/to/repo --remote origin --prefix v- --version-type RC --suffix "" --edit-pkg true --json
```

预览结果里重点看：

- `finalTag`
- `prefix`
- `tagPrefixes`
- `actions`
- `warnings`
- `ready`
- `problems`

### 3. 给用户确认

明确告诉用户：

- 将要打的 tag 是什么
- 当前使用的前缀是什么
- 是否会改 `package.json.tag`
- 是否会提交 `package.json`
- 将推送到哪个 remote

如果用户没有明确指定 `prefix`，还必须补充：

- 当前是按默认前缀预览的
- `tagPrefixes` 里还有哪些可选前缀
- 用户如果想切换前缀，可以直接说“改成 `<prefix>` 再预览/执行”

如果 `ready=false` 或 `problems` 非空，先解决问题，不要执行。

### 4. 用户修改参数时

- 修改 `remote`、`prefix`、`versionType`、`suffix` 或 `editPkg` 后，重新跑一次 `preview`
- 不要沿用旧的 `finalTag`

### 5. 用户确认后执行

将预览产出的 `finalTag` 作为 `--tag` 传给执行脚本：

```bash
node "/absolute/path/to/git-tag-release/scripts/git-tag-release.cjs" execute --cwd /path/to/repo --remote origin --tag "v-1.2.3-RC-20260417153045" --edit-pkg true --json
```

这样执行时不会重新生成另一个 RC 时间戳。

## 规则说明

### 1. 解析已有 tags

- 对每个 tag，从中提取首个匹配 `(\d+\.\d+\.\d+)` 的版本号参与基线计算。
- 只要 tag 在对应前缀下能解析出版本号，就会纳入该前缀的版本序列；后缀如 `-RC-*`、`-beta`、自定义说明不会阻止版本号被提取。
- 按前缀分组维护版本序列；不同前缀互不影响。
- 某个前缀下没有任何可解析版本号的历史 tag 时，基线视为 `0.0.0`。

### 2. 递增规则

- `major`：`X+1.0.0`
- `minor`：`X.Y+1.0`
- `patch`：`X.Y.Z+1`
- `RC`：基于该前缀当前解析出的最新版本号，生成
  `<latest-version>-RC-<yyyyMMddHHmmss>`

### 3. 拼接规则

最终 tag 结构：

```text
<prefix><version><suffix>
```

## 安全边界

- 在执行前，一定要给用户看 `finalTag`。
- 只处理本次发版相关文件；不要还原用户已有改动或无关文件。
- 如果 tag 已存在，不要执行。
- 如果 `editPkg=true`，要提示会修改 `package.json` 并尝试提交。
- 如果工作区有未提交修改，尤其是 `package.json` 有改动，要把 warning 明确转述给用户。
- 不要为了同步远端 tags 而删除本地全部 tags；脚本只做 `git fetch <remote> --tags`。
- 不得默认执行 `pnpm build`；如果判断发版前必须构建验证，先说明原因并等待用户确认。

## 常见失败

- `package.json` 不是合法 JSON
- `tagPrefix` 不是数组或为空
- 没有任何 remote
- `git fetch` 失败
- tag 已存在
- `git push <remote> <tag>` 被权限或保护策略拒绝

## 示例请求

- “推一个 rc 的 tag”
- “按这个仓库的 `tagPrefix` 规则生成下一个 patch tag，并推到 `origin`”
- “用 `web-` 前缀发一个 minor 版本，不要改 `package.json`”
- “把下一个 tag 算出来，我确认后再推”
