---
name: pnpm-local-overrides
description: 本地开发时在 pnpm-workspace.yaml 用 overrides + link 接入工作区外的兄弟包做实时联调。
---

# 本地开发：用 `overrides` + `link:` 接入外部包

## 何时使用

monorepo 要临时联调**不在当前 `packages/*` 范围**内的兄弟项目，配置沉淀在 `pnpm-workspace.yaml`，团队成员 clone 后 `pnpm i` 即可工作。

**不适用**：覆盖某个传递依赖版本（普通版本号 override 即可）；monorepo 内部包互相引用（用 `workspace:*`）。

## 怎么写

在 `pnpm-workspace.yaml` 加 `overrides`，**key 是依赖图里出现的包名**，**value 是 `link:` + 相对路径**：

```yaml
packages:
  - 'packages/*'

overrides:
  example-pkg: link:../example-pkg/packages/example-pkg
```

要点：

- `link:` 后面跟**含 `package.json` 的目录**（不是 `src/index.ts` 之类的源码文件）。
- 相对路径基准是 `pnpm-workspace.yaml` 所在目录，不是终端 `cwd`。
- Windows 路径统一用正斜杠，避免 YAML 转义和 PowerShell 解析差异。
- **只加本次要联调的那一个**：只改了 `pkg-b` 就只写 `pkg-b`，不要把兄弟 monorepo 里的包全 link 进来——override 越多，污染越多，他人 clone 时也要准备越多无关项目。

## 完整示例

```yaml
packages:
  - 'packages/*'

overrides:
  # 本地联调：实时生效
  example-pkg: link:../example-pkg/packages/example-pkg

  # 普通版本 override 与 link: 共存
  vite: 8.0.1
```

## 坑与边界

- **改了兄弟包代码不生效**：`link:` 指到了 `dist/` 而不是源码目录，或链接断了——`pnpm install --force` 重置。
- **`pnpm i` 报找不到包**：key 拼错、路径错、路径下没有 `package.json`，对照下游 `package.json#name` 排查。
- **TS 找不到类型**：link 的包没构建 / 没出 `.d.ts`，让它 build，或改它的 `package.json#exports` 指向源码。
- **CI build 失败**：CI 环境没有那个 `../example-pkg`——`link:` 仅供本地开发，发布前去掉或换成 `workspace:*` / 真实版本号。
- **不要混用 `npm link`**：全局 link 与 `overrides + link:` 一起用容易产生幽灵引用。
