---
name: bun-pnpm
description: |
  Bun 项目使用 pnpm 管理依赖 skill。当 agent 在使用 Bun（bunjs）的项目中工作时，
  必须使用 pnpm（而非 bun 自带的包管理器或 npm/yarn）来安装、添加、移除依赖，
  同时继续使用 bun 作为运行时（执行脚本、运行测试、启动服务）。
  本 skill 适用于任何涉及依赖管理操作（install / add / remove / update / lockfile）的任务。
  判断准则：项目根目录存在 `bun.lockb` 或 `pnpm-lock.yaml`，或 package.json 的 packageManager 字段包含 pnpm，即应激活本 skill。
  基于 pnpm@11+，配置统一写入 `pnpm-workspace.yaml`，不再使用 `.npmrc` 管理 pnpm 设置。
---

# bun-pnpm — Bun 项目使用 pnpm 管理依赖

## 1. 原则声明

> **依赖管理用 pnpm，运行时用 bun（Runtime with Bun, Dependencies with pnpm）。**

在 Bun 项目中，**包管理（install / add / remove / update）一律使用 pnpm**，**脚本执行与运行时操作使用 bun**。两者各司其职，不混用。

### 为什么不直接用 bun install？

| 维度 | bun install | pnpm |
|------|-------------|------|
| 磁盘占用 | 每项目独立 node_modules | 全局 store + 硬链接，极大节省磁盘 |
| 幽灵依赖 | ✅ 存在（hoisting） | ❌ 严格隔离，杜绝未声明的依赖 |
| Monorepo | 原生 workspaces（基础） | 成熟的 workspace 协议、过滤、发布流程 |
| 供应链安全 | 无内置保护 | pnpm@11 默认启用发布冷却期、构建脚本白名单等 |
| 生态兼容 | 少数包对 bun.lockb 支持不佳 | 行业标准，CI / Docker / 部署工具链成熟 |
| Lockfile 可读性 | 二进制 `bun.lockb` | 文本 `pnpm-lock.yaml`，可 code review |

**结论**：用 pnpm 管理依赖可以获得更严格的依赖隔离、更低的磁盘占用、更成熟的 monorepo 支持和更强的供应链安全，同时完全不阻碍 bun 作为运行时的优势（速度、API）。

## 2. 职责划分

```
┌──────────────────────────────────────────────────────────┐
│                     Bun 项目工具链                        │
├─────────────────────┬────────────────────────────────────┤
│   依赖管理（pnpm）   │          运行时（bun）              │
├─────────────────────┼────────────────────────────────────┤
│ pnpm install        │ bun run <script>                   │
│ pnpm add <pkg>      │ bun <entry-file>  （原生 .ts）      │
│ pnpm add -D <pkg>   │ bun test                            │
│ pnpm remove <pkg>   │ bunx <command>                      │
│ pnpm update <pkg>   │ bun --bun vite / next dev           │
│ pnpm why <pkg>      │ bun build                           │
│ pnpm ls / list      │ bun create                          │
│ pnpm runtime set    │ 服务启动：bun run dev / bun run start│
│ pnpm lockfile 操作  │                                    │
├─────────────────────┴────────────────────────────────────┤
│   类型检查（typescript@rc）                                │
├──────────────────────────────────────────────────────────┤
│ tsc --noEmit  （bun 不做类型检查，需独立运行 tsc）          │
└──────────────────────────────────────────────────────────┘
```

**一句话记忆**：装包卸包用 `pnpm`，跑代码用 `bun`，bun 本身也由 `pnpm` 安装，类型检查用 `tsc`。

## 3. 命令速查对照表

| 操作 | ❌ 不要用 | ✅ 使用 |
|------|----------|---------|
| 安装所有依赖 | `bun install` | `pnpm install` |
| 添加生产依赖 | `bun add pkg` | `pnpm add pkg` |
| 添加开发依赖 | `bun add -d pkg` | `pnpm add -D pkg`（或 `pnpm add -d pkg`） |
| 添加全局依赖 | `bun add -g pkg` | `pnpm add -g pkg` |
| 移除依赖 | `bun remove pkg` | `pnpm remove pkg` |
| 更新依赖 | `bun update pkg` | `pnpm update pkg` |
| 查看依赖树 | `bun pm ls` | `pnpm ls` 或 `pnpm why pkg` |
| 执行 package.json 脚本 | `pnpm run dev` | `bun run dev`（或直接 `bun dev`） |
| 运行测试 | `pnpm test` | `bun test` |
| 临时执行 npx 命令 | `npx command` | `bunx command` |
| 清理 node_modules | 手动 `rm -rf` | `pnpm store prune`（清理全局 store） |
| 安装/管理 bun 运行时 | `curl -fsSL https://bun.sh/install \| bash` | `pnpm runtime set bun 1.3.14` |
| 类型检查 | `bunx tsc`（bun 运行时不检查类型） | `bunx tsc --noEmit`（详见 §8.7） |

> **pnpm@11 新增短参数**：`pnpm add -d` 等价于 `--save-dev`，`-p` 等价于 `--save-prod`，`-o` 等价于 `--save-optional`，`-e` 等价于 `--save-exact`。`-F` 是 `--filter` 的短别名。

> **运行时管理（项目级）**：`pnpm runtime set bun <version>` 将 bun 版本声明写入 `package.json` 的 `devEngines.runtime`，解析的具体版本和完整性校验写入 `pnpm-lock.yaml`。`pnpm install` 时自动下载到项目 `node_modules/.bin/`，每个项目独立锁定版本，不污染全局环境。别名：`pnpm rt set`。

## 4. 配置：一切写入 pnpm-workspace.yaml

### 4.1 pnpm@11 配置架构变化

pnpm@11 对配置做了重大调整：

| 配置类型 | 存放位置 | 说明 |
|----------|----------|------|
| pnpm 设置（hoist、peer、build 等） | `pnpm-workspace.yaml` | **不再从 `.npmrc` 读取** |
| 注册源与认证（registry、token） | `.npmrc`（仅此用途） | 仅保留 auth/registry 相关 |
| 全局 pnpm 设置 | `~/.config/pnpm/config.yaml` | 替代旧的 `~/.config/pnpm/rc` |

**核心规则**：

- ❌ 不要在 `.npmrc` 中写 `shamefully-hoist`、`auto-install-peers`、`node-linker` 等 pnpm 设置——pnpm@11 **会忽略**它们
- ❌ 不要在 `package.json` 的 `pnpm` 字段中写配置——pnpm@11 **不再读取** `package.json#pnpm`
- ✅ 所有 pnpm 配置统一写入 `pnpm-workspace.yaml`（即使是单包项目也要用这个文件）

### 4.2 pnpm-workspace.yaml 配置

即使不是 monorepo，单包项目也使用 `pnpm-workspace.yaml` 作为 pnpm 配置文件：

```yaml
# pnpm-workspace.yaml

# ── 依赖隔离 ──
# pnpm 默认严格隔离，通常无需额外配置
# autoInstallPeers 默认已启用，无需手动设置

# ── 构建脚本白名单（pnpm@11 新特性） ──
# pnpm@11 默认阻止所有依赖的构建脚本（postinstall 等）
# 需要显式声明哪些包允许执行构建脚本
allowBuilds:
  esbuild: true
  sharp: true

# ── 注册源（替代 .npmrc 中的 registry 配置） ──
registries:
  default: https://registry.npmjs.org/
  "@my-org": https://npm.pkg.github.com/

# ── 供应链安全（pnpm@11 默认值） ──
# 新发布的包至少经过 1 天才允许安装（默认 1440 分钟）
# 如需禁用，设为 0
minimumReleaseAge: 1440
```

### 4.3 .npmrc — 仅用于 auth/registry（可选）

仅在需要配置私有 registry 认证时才创建 `.npmrc`，且**只写 auth 相关内容**：

```ini
# .npmrc — 仅认证配置，不写 pnpm 设置
//npm.pkg.github.com/:_authToken=${GH_TOKEN}
```

> **安全提示**：pnpm@11 不再展开 `.npmrc` 中的 `${ENV_VAR}` 环境变量（安全修复），认证 token 推荐使用 `pnpm_config_` 前缀的环境变量或 `auth.ini`。

如果已通过 `pnpm-workspace.yaml` 的 `registries` 配置了 registry 地址，`.npmrc` 中只需要补充 token 即可。

### 4.4 package.json

```json
{
  "packageManager": "pnpm@11.7.0",
  "type": "module",
  "devEngines": {
    "runtime": {
      "name": "bun",
      "version": "1.3.14",
      "onFail": "download"
    }
  },
  "scripts": {
    "dev": "bun run --hot src/index.ts",
    "build": "bun build src/index.ts --target bun --outdir dist",
    "test": "bun test",
    "typecheck": "bunx tsc --noEmit",
    "start": "bun run dist/index.js"
  }
}
```

**字段说明**：

- `packageManager`：锁定 pnpm 版本，由 Corepack 识别。
- `devEngines.runtime`：声明项目所需的 bun 运行时版本。`onFail: "download"` 表示当系统未安装指定版本时，pnpm 自动下载到项目本地。
- `pnpm runtime set bun 1.3.14` 会自动将该声明写入 `devEngines.runtime`（pnpm@11.4+ 默认行为），解析的具体版本与完整性校验写入 `pnpm-lock.yaml`。后续 `pnpm install` 自动下载到 `node_modules/.bin/bun`，保证团队环境一致。

> **pnpm@11 变化**：`pnpm init` 默认写入 `"type": "module"`。不再读取 `package.json` 的 `pnpm` 字段——所有 pnpm 配置移至 `pnpm-workspace.yaml`。

### 4.5 .gitignore

```gitignore
node_modules/
# ↓ lockfile 必须提交，不要忽略
# pnpm-lock.yaml
```

## 5. 项目初始化

### 5.1 全新项目

```bash
# 1. 初始化项目
pnpm init

# 2. 创建 pnpm-workspace.yaml（即使单包项目也需要）
touch pnpm-workspace.yaml

# 3. 声明 bun 运行时版本（写入 devEngines.runtime + pnpm-lock.yaml）
pnpm runtime set bun 1.3.14

# 4. 安装依赖（自动下载 bun 到 node_modules/.bin/）
pnpm add hono
pnpm add -D typescript@rc @types/bun
pnpm install

# 5. 验证
pnpm exec bun --version    # 1.3.14
pnpm --version             # 11.x
pnpm exec tsc --version    # 7.x (rc)
```

> **也可以**：直接在 `package.json` 中手写 `devEngines.runtime`（见 §4.4），`pnpm install` 时自动下载。`pnpm runtime set` 命令的作用就是帮你自动写入这个字段并锁定到 lockfile。

### 5.2 从 bun 迁移到 pnpm

```bash
# 1. 删除 bun 的 lockfile
rm -f bun.lockb

# 2. 创建 pnpm-workspace.yaml（空文件即可）
touch pnpm-workspace.yaml

# 3. 更新 package.json 的 packageManager 字段
#    改为 "packageManager": "pnpm@11.7.0"

# 4. 如果有 .npmrc，将 pnpm 设置迁移到 pnpm-workspace.yaml
#    .npmrc 仅保留 auth/registry 配置

# 5. 声明 bun 运行时版本（写入 devEngines.runtime + pnpm-lock.yaml）
pnpm runtime set bun 1.3.14

# 6. 用 pnpm 重新安装依赖（自动下载 bun 到 node_modules/.bin/）
pnpm install

# 7. 提交
git add pnpm-lock.yaml pnpm-workspace.yaml package.json
git commit -m "chore: migrate dependency management from bun to pnpm"
```

迁移后检查：

- [ ] `bun.lockb` 已删除
- [ ] `pnpm-lock.yaml` 已生成并提交
- [ ] `pnpm-workspace.yaml` 已创建并包含必要配置
- [ ] `.npmrc` 中不再有 pnpm 专属设置（仅保留 auth/registry）
- [ ] `package.json` 的 `packageManager` 字段已设置为 pnpm 版本
- [ ] `package.json` 中不再有 `pnpm` 字段
- [ ] `devEngines.runtime` 已声明 bun 版本
- [ ] CI 流水线已切换为 `pnpm install`
- [ ] `bun run` / `bun test` 等运行时命令仍正常工作

### 5.3 从 pnpm@10 升级到 pnpm@11

pnpm 提供了自动迁移 codemod：

```bash
# 全局升级 pnpm
pnpm self-update 11

# 在项目中运行 codemod（自动迁移 .npmrc → pnpm-workspace.yaml）
cd /path/to/your/project
pnpm dlx codemod run pnpm-v10-to-v11
```

codemod 会自动处理：
- 将 `package.json#pnpm` 设置迁移到 `pnpm-workspace.yaml`
- 将 `.npmrc` 中的非 auth 设置迁移到 `pnpm-workspace.yaml`
- 将 `onlyBuiltDependencies` 等旧设置合并为 `allowBuilds`
- 更新 `packageManager` 版本号

## 6. CI 配置示例（GitHub Actions）

使用 `pnpm/setup` 安装 pnpm，bun 运行时由 `pnpm install` 根据 `devEngines.runtime` 自动下载到项目本地：

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # 安装 pnpm（bun 由 devEngines.runtime + pnpm install 自动管理）
      - uses: pnpm/setup@v0
        with:
          version: 11
          cache: true
      # 安装依赖，同时自动下载项目锁定的 bun 版本
      - run: pnpm install --frozen-lockfile
      # 类型检查（bun 运行时不检查类型，需独立运行 tsc）
      - run: pnpm exec bun run typecheck
      # 通过 pnpm exec 调用项目内的 bun
      - run: pnpm exec bun test
      - run: pnpm exec bun run build
```

> bun 版本由 `package.json` 的 `devEngines.runtime` 声明、`pnpm-lock.yaml` 锁定，`pnpm install` 自动下载到 `node_modules/.bin/bun`。CI 无需单独配置 bun 安装步骤。

## 7. Monorepo（pnpm workspace）

### 7.1 目录结构

```
my-app/
├── pnpm-workspace.yaml      # workspace + pnpm 配置（唯一配置入口）
├── package.json
├── pnpm-lock.yaml           # 唯一的 lockfile（根目录）
├── packages/
│   ├── server/
│   │   └── package.json
│   ├── client/
│   │   └── package.json
│   └── shared/
│       └── package.json
```

### 7.2 pnpm-workspace.yaml（monorepo 完整示例）

```yaml
packages:
  - 'packages/*'
  - 'apps/*'

# pnpm@11 构建脚本白名单
allowBuilds:
  esbuild: true
  sharp: true

# 注册源
registries:
  default: https://registry.npmjs.org/
  "@my-org": https://npm.pkg.github.com/
```

### 7.3 常用 workspace 命令

| 操作 | 命令 |
|------|------|
| 安装所有 workspace 依赖 | `pnpm install` |
| 在指定包中添加依赖 | `pnpm -F <pkg-name> add <dep>` |
| 在所有包中运行脚本 | `pnpm -r run build` |
| 在指定包中运行脚本 | `pnpm -F <pkg-name> run test` |
| 添加本地包间依赖 | `pnpm -F client add shared@workspace:*` |
| 列出所有包 | `pnpm ls -r --depth -1` |

### 7.4 workspace 间依赖

包之间互相引用时，在子包的 `package.json` 中：

```json
{
  "name": "client",
  "dependencies": {
    "shared": "workspace:*"
  }
}
```

`workspace:*` 表示始终使用本地 workspace 中的版本，发布时自动替换为真实版本号。

## 8. 常见场景规范

### 8.1 新增依赖

```bash
# 生产依赖
pnpm add hono
pnpm add @hono/zod-validator

# 开发依赖
pnpm add -D typescript@rc @types/bun
pnpm add -D vitest
```

**禁止行为**：
- ❌ `bun add hono`
- ❌ `npm install hono`
- ❌ `yarn add hono`

### 8.2 安装项目依赖（clone 后 / pull 后）

```bash
pnpm install
```

**CI 环境中使用**：

```bash
pnpm install --frozen-lockfile
```

### 8.3 运行开发服务器

```bash
# ✅ 正确：用 bun 执行脚本
bun run dev

# 也等价于
bun dev
```

**禁止行为**：
- ❌ `pnpm dev`（多一层不必要的进程开销，且无法利用 bun 的热重载）

### 8.4 执行测试

```bash
# ✅ bun test 速度最快
bun test

# 如果测试脚本本身依赖 vitest/jest
bun run test
```

### 8.5 升级依赖

```bash
# 查看过期依赖
pnpm outdated

# 升级单个包（在 semver 范围内）
pnpm update hono

# 升级到最新大版本（忽略 semver 范围）
pnpm update hono --latest

# 升级所有依赖
pnpm update --latest
```

### 8.6 排查依赖问题

```bash
# 为什么安装了这个包（pnpm@11 显示反向依赖树）
pnpm why hono

# 查看依赖树
pnpm ls --depth 2

# 检查重复依赖
pnpm ls --depth Infinity | grep -A2 "<pkg>"
```

> **pnpm@11 变化**：`pnpm why` 现在输出**反向依赖树**——被查询的包在根节点，其依赖者作为分支，更直观地回答"谁依赖了这个包"。

### 8.7 TypeScript 类型检查

Bun 原生支持直接运行 `.ts`/`.tsx` 文件——它在运行时**转译** TypeScript（剥离类型），但**不做任何类型检查**。这意味着类型错误不会阻止代码运行，也不会被 `bun test` 发现。

因此，项目必须**独立运行 `tsc --noEmit`** 进行类型检查：

```bash
# 安装 typescript（使用 rc 版本，紧跟最新语言特性）
pnpm add -D typescript@rc

# 运行类型检查
bunx tsc --noEmit

# 或通过 package.json script
bun run typecheck   # "typecheck": "bunx tsc --noEmit"
```

**职责分工**：

| 环节 | 工具 | 说明 |
|------|------|------|
| 运行 `.ts` 代码 | `bun` | 原生支持，零配置，速度极快 |
| 类型检查 | `bunx tsc --noEmit` | 独立步骤，不产出文件，只报类型错误 |
| 测试 | `bun test` | 运行时测试，不包含类型检查 |
| 构建 | `bun build` | 打包，不做类型检查 |

**tsconfig.json 要点**：

```jsonc
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["@types/bun"],
    "strict": true,
    "noEmit": true,           // 类型检查专用，不产出文件
    "skipLibCheck": true,
    "allowImportingTsExtensions": true,
    "noUncheckedSideEffectImports": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

> **为什么用 `typescript@rc` 而非 stable**：rc 版本当前对应 TypeScript 7，紧跟最新语言特性，适合追求最新工具链的 Bun 项目。如果 rc 版本不稳定，可随时回退到 stable：`pnpm add -D typescript`。

**在 CI 中集成类型检查**：

```yaml
- run: pnpm install --frozen-lockfile
- run: pnpm exec bun run typecheck   # tsc --noEmit
- run: pnpm exec bun test
```

> 类型检查应在测试之前运行——如果类型有错，后续测试和构建无意义。

## 9. Docker 部署

使用 pnpm 官方基础镜像，bun 运行时由 `pnpm install` 根据 `devEngines.runtime` 自动下载到项目本地：

```dockerfile
# ---- 阶段 1：安装依赖（含 bun 运行时） ----
FROM ghcr.io/pnpm/pnpm:11 AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
# 如有 workspace 子包，一并拷贝
COPY packages/ ./packages/
# pnpm install 自动根据 devEngines.runtime 下载 bun 到 node_modules/.bin/
RUN pnpm install --frozen-lockfile --prod

# ---- 阶段 2：运行 ----
FROM ghcr.io/pnpm/pnpm:11 AS runtime
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
# 通过 pnpm exec 调用项目锁定的 bun 版本
CMD ["pnpm", "exec", "bun", "run", "src/index.ts"]
```

**关键点**：
- 使用 `ghcr.io/pnpm/pnpm:11` 官方镜像（基于 debian:stable-slim），仅含 pnpm 独立二进制，不捆绑 Node
- bun 版本由 `devEngines.runtime` 声明、`pnpm-lock.yaml` 锁定，`pnpm install` 自动下载到 `node_modules/.bin/bun`，无需全局安装
- 必须拷贝 `pnpm-workspace.yaml`（pnpm@11 配置入口）
- `--prod` 跳过 devDependencies，减小镜像体积
- 运行时通过 `pnpm exec bun` 调用，确保使用项目锁定的版本

## 10. pnpm@11 构建脚本白名单

pnpm@11 默认**阻止所有依赖的构建脚本**（postinstall、preinstall 等），这是供应链安全措施。如果安装时报 `ERR_PNPM_IGNORED_BUILDS`，需要将相关包加入 `allowBuilds`。

### 10.1 常见需要加入白名单的包

```yaml
# pnpm-workspace.yaml
allowBuilds:
  esbuild: true        # 需要下载平台二进制
  sharp: true          # 需要 native 构建
  @biomejs/biome: true # 需要 native 二进制
  better-sqlite3: true # 需要 node-gyp 构建
  swc: true            # 需要 native 二进制
```

### 10.2 交互式审批

安装后如发现有构建脚本被跳过，可交互式审批：

```bash
# 查看哪些包有被阻止的构建脚本
pnpm approve-builds
```

### 10.3 显式拒绝

```yaml
allowBuilds:
  core-js: false   # 明确拒绝（不执行构建脚本）
  esbuild: true    # 明确允许
```

## 11. 常见陷阱与避坑

### 11.1 幽灵依赖

**问题**：项目代码引用了 `package.json` 中未声明的包（因为其他依赖间接安装了它）。

**pnpm 的优势**：默认严格隔离，未声明的包无法被 import，在开发阶段就能暴露问题。

**修复方式**：将缺失的依赖显式添加：

```bash
pnpm add missing-package
```

### 11.2 bunx vs pnpm dlx

| 场景 | 命令 | 说明 |
|------|------|------|
| 临时执行 CLI 工具 | `bunx create-hono` | 用 bun 运行，更快 |
| 临时执行需要 Node 兼容的工具 | `pnpm dlx create-hono` | pnpm 的 npx 等价物 |

**建议**：优先用 `bunx`，除非工具不兼容 bun 运行时。

### 11.3 scripts 中的包管理命令

在 `package.json` 的 scripts 中，如果需要调用包管理器，**统一用 pnpm**：

```json
{
  "scripts": {
    "postinstall": "pnpm run build:prepare",
    "prepack": "pnpm run build"
  }
}
```

**禁止**在 scripts 中混用 `bun install`。

### 11.4 全局 store 磁盘清理

长期使用后 pnpm 全局 store 可能积累无用文件：

```bash
# 查看 store 路径
pnpm store path

# 清理未被任何项目引用的包
pnpm store prune
```

### 11.5 pnpm@11 环境变量

pnpm@11 不再读取 `npm_config_*` 环境变量，改用 `pnpm_config_*` 前缀：

```bash
# ❌ 旧写法（pnpm@11 不再识别）
npm_config_registry=https://my.registry.com pnpm install

# ✅ 新写法
pnpm_config_registry=https://my.registry.com pnpm install
```

### 11.6 overrides 和 patches 迁移

pnpm@11 **不再读取** `package.json` 中的 `pnpm.overrides` 和 `pnpm.patchedDependencies`，必须迁移到 `pnpm-workspace.yaml`：

```yaml
# pnpm-workspace.yaml
overrides:
  lodash: 4.17.21

patchedDependencies:
  hono: patches/hono.patch
```

> **重要**：如果忘记迁移，pnpm@11 会**静默忽略**这些配置，不会报错也不会警告，可能导致安全补丁失效。

## 12. 检查清单

每次涉及依赖操作时，确认：

- [ ] 安装/添加/移除/更新依赖使用的是 `pnpm` 命令，而非 `bun install` / `bun add`
- [ ] 执行脚本、运行测试、启动服务使用的是 `bun` 命令
- [ ] bun 运行时通过 `pnpm runtime set bun <version>` 在项目内管理（不加 `-g`），而非 `curl` 脚本
- [ ] `package.json` 的 `devEngines.runtime` 已声明 bun 版本
- [ ] `pnpm-lock.yaml` 已锁定 bun 运行时版本（含完整性校验）
- [ ] `pnpm-lock.yaml` 已提交到版本控制
- [ ] `bun.lockb` 不再存在（迁移后应删除）
- [ ] `package.json` 的 `packageManager` 字段已设置 pnpm@11 版本
- [ ] pnpm 配置写入 `pnpm-workspace.yaml`，而非 `.npmrc` 或 `package.json#pnpm`
- [ ] `.npmrc` 仅包含 auth/registry 配置（如需要）
- [ ] `allowBuilds` 已声明需要构建脚本的依赖
- [ ] `overrides` / `patchedDependencies` 已从 `package.json` 迁移到 `pnpm-workspace.yaml`
- [ ] `typescript@rc` 已作为 devDependency 安装，`typecheck` 脚本配置为 `bunx tsc --noEmit`
- [ ] CI / Docker 中通过 `pnpm install` 自动获取项目锁定的 bun 版本，无需单独安装
- [ ] 新增依赖后，代码能正常 import（无幽灵依赖问题）
- [ ] Monorepo 场景下使用 `pnpm -F` 而非 `cd <dir> && pnpm add`
