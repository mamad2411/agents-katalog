---
name: mearl-bbrowser
description: 使用 Mearl 的浏览器扩展或直连 CDP 加载、查询、更新和执行 bb-browser 格式的站点适配器。适用于用户要求运行 bb-browser site 命令、复用 bb-sites 社区或私有适配器；普通网页操作继续使用 Mearl。
install:
  description: 安装并注册 bb-browser 站点适配器兼容插件
  command: npx @mearl/setup plugin "$SKILL_DIR"
version: "3.1.0"
---

# Mearl 站点适配器

通过 `mearl bbrowser site ...` 运行原始适配器，无需安装 bb-browser CLI、扩展或 daemon。浏览器操作走 Mearl，支持扩展与直连 CDP；页面 Cookie 和站点 JS 上下文属于所选浏览器。

## 工具箱

扩展工具箱中的「站点适配器」支持按站点浏览和搜索、整库安装或更新社区适配器、填写参数执行，以及点击当前命令复制。工具箱执行定位所选适配器文件；复制命令使用适配器名称和位置参数，跳过中间参数或参数以短横线开头时使用结构化 payload 保留含义。复制的命令遵循 CLI 的当前目录优先规则。工具箱试用绑定打开工具箱的当前浏览器，使用该浏览器的登录态，可指定目标标签页 ID；参数和结果仅保留在当前页面内。安装或更新后自动重载列表；执行进度显示在按钮上，异常通过宿主 toast 提示。

## CLI 命令

```bash
mearl bbrowser site list
mearl bbrowser site search 示例
mearl bbrowser site info example-shop/whoami
mearl bbrowser site example-shop/whoami
mearl bbrowser site zhihu/hot 10
mearl bbrowser site run zhihu/hot --count 10
mearl bbrowser site update
```

不清楚参数时先查询 `site info <name>`。适配器名已知时直接调用，缺少社区库时才按需要执行 `site update`。执行操作依照用户请求；适配器的 `readOnly` 和 `capabilities` 是描述信息，不替代用户授权或 Mearl 权限检查。

插件尚未注册或入口丢失时，注册当前 Skill 目录：

```bash
npx @mearl/setup plugin "$SKILL_DIR"
```

## 来源和参数

默认按以下顺序读取，同名适配器由靠后的目录覆盖：

1. `~/.bb-browser/bb-sites`：已有 bb-browser 社区库。
2. `~/.mearl/bbrowser/bb-sites`：Mearl 管理的社区库。
3. `~/.bb-browser/sites`：已有 bb-browser 私有适配器。
4. `~/.mearl/bbrowser/sites`：Mearl 私有适配器。

执行或查看 `info` 时，先检查当前工作目录下的适配器文件，存在时优先使用，再查询上述目录。支持相对路径、绝对路径和省略 `.js` 后缀，例如在项目根目录执行：

```bash
# 加载当前项目的 example-shop/ai-agent.js
mearl bbrowser site example-shop/ai-agent
mearl bbrowser site ./example-shop/ai-agent.js
mearl bbrowser site info ./example-shop/ai-agent.js
```

同目录 `_helper.js` 随适配器一起加载；`list` 和 `search` 查询约定目录中的适配器。`site update` 固定从 `epiral/bb-sites` 克隆或快进更新到 `~/.mearl/bbrowser/bb-sites`，有本地修改时停止。私有适配器放在项目中或 `sites` 目录，不放入社区库。

兼容 `@meta` JSON、旧式 `// @tag`、元数据中的额外字段、同目录 `_helper.js` 和 `async function(args)`。`@meta.args` 的参数定义支持描述字符串和对象。位置参数按 `@meta.args` 声明顺序填入尚未命名赋值的参数；数字和布尔值转换为字符串，与 bb-browser CLI 保持一致。下划线命名参数可直接传入，其他名字或与宿主选项冲突的参数放到结构化 `args` 对象。

SDK/MCP 使用插件名 `bbrowser`、命令 `site`，input 示例：

```json
{
  "tokens": ["zhihu/hot"],
  "args": { "count": "10" },
  "tab": 12345
}
```

CLI 对应 `mearl bbrowser --payload '{"command":"site","input":{"tokens":["zhihu/hot"],"args":{"count":"10"}}}'`。`tokens` 放管理子命令、适配器名或文件路径及位置参数，`args` 放适配器参数；`tab` 指定目标标签页。

## 浏览器和结果

- `--browser`、`--session`、`--timeout`、`--output` 使用 Mearl 宿主语义。`--tab` 使用 Mearl 的数字 tabId。
- 有 domain 时后台复用该域名页面或新建页面；显式 tab 必须匹配适配器域名。没有 domain 时使用当前活动页或首个页面。默认保留页面，不主动刷新用户页面。
- 脚本在页面主世界执行，保留 helper 与页面全局状态，等待异步结果。不自动重试执行失败的适配器。
- 成功返回 `{ "result": ... }`；返回 JSON 字符串时解析为 JSON。适配器返回 error 时输出 `success:false`、`error.message`、原始 `result` 和可选 `hint`，CLI 退出码为 1。会话结果还包含 Mearl 的 `session`，新建会话后用其 sessionId 继续操作或释放。
- 登录、验证码、页面初始化和站点改版问题按返回的错误核查。适配器中的 bb-browser 操作提示可用 Mearl 对应能力完成；浏览器人工交接和会话收尾遵循 Mearl 工作流。

插件默认输出 JSON。此插件兼容站点适配器执行和上述管理命令；OpenClaw 桥接和 `--jq` 不在此入口中实现，结果筛选可使用系统 `jq`。
