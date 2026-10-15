---
name: koishi-plugin-publish-audit
description: 审核 Koishi 插件发布与市场上架风险：package 元信息、peerDependencies、koishi 字段、服务声明、预览/隐藏状态、用户配置体验与发布结论。
---

# Koishi 插件发布审计

这个 skill 用于在 Koishi 插件合并、发版或上架插件市场前，检查 **Koishi 生态发布层** 的准备度。它不重复审计 Cordis 底座的生命周期、服务依赖、Schema 可逆性和热重载问题；这些通用插件质量请使用 `cordis-v3-plugin-dev`。

## 审计目标

优先回答三个问题：

1. **能不能被 Koishi 正确识别和安装**：包名、版本、`peerDependencies.koishi`、入口与构建产物是否合理。
2. **能不能被插件市场正确展示**：`description`、`keywords`、`koishi.description`、`koishi.service`、`preview` / `hidden` 是否准确。
3. **普通用户能不能安全配置和升级**：配置说明、服务依赖、权限、默认值、迁移风险是否清晰。

## 1. package 基础元信息

检查插件目录下的 `package.json`，不要只看应用根目录。

重点：

- `name` 符合 Koishi 插件命名：
  - `koishi-plugin-*`
  - `@scope/koishi-plugin-*`
- `version` 符合 semver，且是本次要发布的新版本。
- 没有误设 `private: true`。
- `main` / `types` / `exports` 指向实际构建产物。
- 发布前构建脚本存在且能生成对应文件。
- `files` 字段不会漏掉 `lib`、`dist`、`client`、locales 等必要产物。

严重问题：包名不合规、`private: true`、入口文件不存在、版本未更新但准备发布。

## 2. Koishi 兼容性声明

必须检查：

```json
{
  "peerDependencies": {
    "koishi": "^4.15.6"
  }
}
```

原则：

- 声明 `peerDependencies.koishi`。
- 不要把 Koishi 只放进 `dependencies` 导致重复安装或版本冲突。
- 开发和测试需要时，可同时放在 `devDependencies`。

## 3. 市场展示信息

检查：

- `description` 是否一句话说明用途。
- `keywords` 是否包含 `koishi` 和插件领域关键词。
- `license` 是否明确。
- `repository` / `homepage` / `bugs` 是否可访问。
- `contributors` / `author` 是否合理。
- README 是否包含安装、配置、使用示例和常见问题。

`koishi.description` 用于市场展示：

```json
{
  "koishi": {
    "description": {
      "zh": "示例插件。",
      "en": "Example plugin."
    }
  }
}
```

建议：

- 中文插件至少提供 `zh` 描述。
- 面向国际用户时补充 `en`。
- 描述不要只写“插件”或“工具”，要写清具体能力。

## 4. koishi.service 元信息

`koishi.service` 应与代码中的 `inject` 和自定义服务实现一致。

```json
{
  "koishi": {
    "service": {
      "required": ["database"],
      "optional": ["assets"],
      "implements": ["myService"]
    }
  }
}
```

检查：

- `required` 是否列出插件必需服务。
- `optional` 是否列出增强能力。
- `implements` 是否列出插件提供的服务。
- package 元信息与代码 `export const inject` / `ctx.inject()` / `new Service()` 一致。
- 导入服务包运行时代码时，是否有对应 peer / dev 依赖。

判断原则：

- 代码 `inject` 负责运行时生命周期。
- `koishi.service` 负责市场和安装认知。
- 两者不一致会导致“能装但不好用”或“运行时才暴雷”。

## 5. preview / hidden / locales / assets

检查：

- `koishi.preview` 是否准确表示预览状态。
- `koishi.hidden` 是否符合是否应在市场展示。
- `koishi.locales` 是否与实际语言资源一致。
- 插件包含控制台前端时，`client` / `dist` / assets 是否被发布。
- 插件包含模板或静态文件时，`files` 字段是否包含它们。
