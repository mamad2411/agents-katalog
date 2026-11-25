---
name: vite-plus-config
description: Vite+ library config reference for dep externals, entry design, layout, and fmt per scenario.
---

# Vite+ 配置参考（库项目）

## 适用场景

- 使用 `vite-plus` / `vp pack` 打包库项目。
- 需要多入口导出（如 `index`、`monaco`、`other`）。
- 需要避免不必要的依赖内联（尤其 `monaco-editor`）。

## 使用方式（先判断场景，再给方案）

本技能不是硬性规则集合，而是配置参考。

当用户描述完目标后，先判断当前诉求属于哪一类，再选用对应建议：

- 诉求是“这个库不要被打包 / 不要进入 `inlinedDependencies`”
- 诉求是“我要新增导出入口，但不想直接改 `package.json.exports`”
- 诉求是“项目结构混乱，需要规范入口与目录职责”
- 诉求是“格式配置不统一，需要一个稳定基线”

## 场景参考

### 依赖是否外置：按需求触发，不是默认强制

仅当用户明确表达以下意图时再使用：

- 不要打包某个依赖
- 不要把某依赖写进 `inlinedDependencies`
- 产物体积或类型体积因某依赖异常膨胀

可参考在 `vite.config.ts` 的 `pack` 中配置：

```ts
defineConfig({
  pack: {
    deps: {
      neverBundle: ['monaco-editor']
    }
  }
})
```

说明：

- 这是“按场景启用”的策略，不是所有项目都必须配置。
- 不建议用 build 后删文件的方式绕过问题。

### 导出入口调整：优先改 `pack.entry`

当用户要新增/调整导出入口时，优先调整 `vite.config.ts` 的 `pack.entry`。

示例：

```ts
defineConfig({
  entry: {
    index: 'src/index.ts',
    other: 'src/other/index.ts'
  }
})
```

默认建议：

- 尽量不手改 `package.json.exports`。
- 通过 entry 驱动导出关系，避免手工维护漂移。

### 入口与目录组织：优先语义清晰

可参考以下组织方式：

- `src/index.ts` 只做导出聚合，不放复杂实现
- 实现按职责分目录：`src/core`、`src/lib`、`src/monaco`、`src/language`
- 若要分目录，目录名要表达业务含义，避免无语义命名

### fmt 配置：作为默认基线

在 `vite.config.ts` 中保持：

```ts
defineConfig({
  fmt: {
    singleQuote: true,
    semi: false,
    trailingComma: 'none'
  }
})
```
