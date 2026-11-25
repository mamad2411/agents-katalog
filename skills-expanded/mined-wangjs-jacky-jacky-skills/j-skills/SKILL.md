---
name: j-skills
description: "管理 Agent Skills 的 j-skills CLI 操作指南，基于本机已安装的 0.4.4 命令面。当用户要链接本地 Skill、安装到 Claude Code/Codex/Cursor 等环境、卸载、查看安装状态或管理 registry 时使用。"
---

# j-skills

`j-skills` 用于把本地 Skill 目录注册到全局 registry，再安装到指定 Agent 环境。

## 执行原则

1. 先运行 `j-skills --version` 和对应子命令的 `--help`，以当前二进制为准。
2. 优先使用 `--json` 获取可审计输出。
3. 安装时明确指定作用域和目标环境，避免交互式选择。
4. 不覆盖同名但指向其他目录的链接；先报告冲突，再让用户决定。
5. 批量初始化 `jacky-skills` 仓库时直接使用根目录 `./install.sh`。

## 安装 CLI

```bash
npm install -g @wangjs-jacky/j-skills@latest --registry=https://registry.npmjs.org/
j-skills --version
```

Apple Silicon Mac 应先确认 `node -p 'process.arch'` 输出 `arm64`。

## link：注册本地 Skill

```bash
# 链接当前目录
j-skills link

# 链接指定 Skill 目录
j-skills link /path/to/skill

# 列出已链接 Skill
j-skills link --list --json

# 取消链接
j-skills link --unlink skill-name --json
```

`link` 每次只接受一个 Skill 目录。要批量处理时逐个调用，或使用仓库 `install.sh`。

> Linux 等大小写敏感文件系统上，0.1.0 可能因检查小写 `skill.md` 而拒绝标准 `SKILL.md`。仓库 `install.sh` 已内置临时兼容链接并在执行后清理。

## install：安装到 Agent 环境

```bash
# 安装到当前项目
j-skills install skill-name --env claude-code,codex --json

# 安装到用户全局
j-skills install skill-name --global --env claude-code,codex --json
```

`--env` 接收逗号分隔的环境名。不传 `--env` 时会进入交互式多选。

## uninstall：卸载

```bash
# 卸载当前项目中的 Skill
j-skills uninstall skill-name --yes --json

# 卸载用户全局 Skill
j-skills uninstall skill-name --global --yes --json
```

## list：查看安装状态

```bash
j-skills list --local --json
j-skills list --global --json
j-skills list --all --json
j-skills list --search keyword --json
```

## config：配置 registry

```bash
j-skills config:list
j-skills config:set key value
j-skills config:reset
j-skills config:add-registry name https://example.com/registry.json
j-skills config:registries
j-skills config:use name
```

## CLI 发布流程

`@wangjs-jacky/j-skills` 已改为 GitHub Actions 自动发布。修改 CLI 源码后，不要在本机执行 `npm publish`。

1. 只更新 `jacky-skills-package/packages/cli/package.json` 的版本号。
2. 提交并推送到 `main`。
3. 创建并推送匹配版本号的 `v*` tag，例如 `v0.4.4`。
4. 等待 `.github/workflows/publish.yml` 自动测试、typecheck、build、校验 CLI 自报版本，并通过 npm Trusted Publishing / OIDC 发布。

`packages/cli/src/index.ts` 从 `package.json` 读取版本号，禁止再写死 `const VERSION = 'x.y.z'`。2026-07-12 已验证 CI 可发布 `@wangjs-jacky/j-skills@0.4.4`；后续不需要本机 `npm login`、不需要长期 `NPM_TOKEN`。

## 标准流程

```bash
# 1. 验证目录
test -f /path/to/skill/SKILL.md

# 2. 链接
j-skills link /path/to/skill --json

# 3. 安装
j-skills install skill-name --global --env claude-code,codex --json

# 4. 核验
j-skills link --list --json
j-skills list skill-name --json
```

## 故障排查

- `Skill not found`：先运行 `j-skills link --list --json`，确认 Skill 已链接。
- 同名冲突：对比 registry 路径与期望目录，不自动覆盖。
- 安装后未生效：用 `j-skills list skill-name --json` 检查目标环境路径，必要时重启 Agent 会话。
- 参数不确定：运行 `j-skills <command> --help`，不从旧文档猜测。
- `npm publish` 报 `ENEEDAUTH`：不要在本机发布。检查是否已推送匹配 `packages/cli/package.json` 的 `v*` tag，并查看 GitHub Actions 的 Publish j-skills to npm workflow。
