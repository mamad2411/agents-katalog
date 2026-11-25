---
name: cloudflare-temporary-deploy
description: Deploy a Worker live, no account, via wrangler --temporary.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cloudflare, workers, wrangler, deploy, temporary, agent, serverless, web-development]
    category: web-development
---

# Cloudflare临时部署技能

无需进行任何账户设置，即可通过`wrangler deploy --temporary`命令将Cloudflare Worker部署到实时的`workers.dev`地址。Cloudflare会自动创建一个临时账户完成部署，并生成一个有效期为60分钟的访问链接；未被领取的账户将会自动删除。这样一来，代理就能在无需处理OAuth认证、注册流程或复制粘贴令牌的情况下，快速实现编写代码→部署→验证的完整循环。

该技能不支持生产环境部署（此类场景请使用`wrangler login`及永久账户），也不适用于超出上述临时账户限制的Cloudflare非Worker类产品。

## 适用场景

当用户希望实现以下操作时，可使用此技能：
- **无需先创建Cloudflare账户即可将代理编写的代码部署到实时网址**——只需“完成部署并给出链接”
- 在**后台或自动化会话中迭代开发**，避免因浏览器OAuth步骤而中断流程
- 使用可临时获取的测试地址，快速**原型设计或测试Cloudflare Worker功能**
- 构建**自我验证的部署循环**——部署后通过`curl`调用实时网址，确认输出结果与代码一致后再重新部署

## 不适用场景

- **生产环境或CI/CD流程** → 应使用永久账户（`wrangler login`或`CLOUDFLARE_API_TOKEN`）。若存在任何认证凭证，`--temporary`命令将会报错。
- **Wrangler已处于登录状态** → 按设计要求，`--temporary`会返回错误。仅当用户明确需要临时部署时，才需先运行`wrangler logout`。
- **需要长期托管的场景** → 临时部署在60分钟后会被自动删除，除非有人领取该链接。

## 先决条件

- **Wrangler 4.102.0 或更高版本**。该版本首次引入了 `--temporary` 参数，早期版本不支持此功能。可通过 `npx wrangler@latest --version` 查看当前版本号。
- **Node 18+ / npm**（或 `npx`、`yarn`、`pnpm`）。无需全局安装，直接使用 `npx wrangler@latest` 即可。
- **不得包含 Cloudflare 凭证**。`--temporary` 参数仅在 Wrangler 未进行身份验证时有效：不允许 OAuth 登录，不得设置 `CLOUDFLARE_API_TOKEN`/`CLOUDFLARE_API_KEY` 环境变量，也不得存在 `~/.wrangler`/`~/.config/.wrangler` 中的 OAuth 缓存数据。请直接使用 `terminal` 工具的现有环境，无需设置上述变量。
- 需要能够访问 `cloudflare.com` 和 `workers.dev` 的网络出口。
- 使用 `--temporary` 参数即表示您已同意 Cloudflare 的服务条款和隐私政策。

## 运行步骤

每一步均需使用 `terminal` 工具。请始终指定具体版本（如 `wrangler@latest`、`wrangler@4.102.0` 或更高版本），以避免误用旧版全局安装的 Wrangler，从而导致该参数无法使用。

1. **创建一个最简 Worker 模板**（如果项目已存在则可跳过此步骤）。Worker 需要一个 `wrangler.toml`（或 `wrangler.jsonc`）文件以及一个入口脚本。以下是一个最简的 TypeScript 示例，可通过 `write_file` 函数生成这些文件：

   `wrangler.jsonc`：
   ```jsonc
   {
     "name": "hello-agent",
     "main": "src/index.ts",
     "compatibility_date": "2025-01-01"
   }
   ```

`src/index.ts`：
   ```typescript
   export default {
     async fetch(): Promise<Response> {
       return new Response("hello cloudflare");
     },
   };
   ```

2. 从项目目录中使用 `--temporary` 参数进行部署：
   ```
   npx wrangler@latest deploy --temporary
   ```
工作量证明检查会自动添加一段短暂的延迟。验证成功后，Wrangler会输出一行信息，显示“账户：<名称>（已创建）”（或“（已复用）”），同时还会给出“领取地址”以及实时可用的 `https://<worker>.<account>.workers.dev` 地址。

3. 从上述输出中**解析出这些网址**。建议使用专用工具来准确提取，而非凭肉眼查看。
   ```
   npx wrangler@latest deploy --temporary 2>&1 | python scripts/parse_deploy_output.py
   ```
（将 `scripts/parse_deploy_output.py` 解析为该技能的绝对路径。该脚本会输出 JSON 格式的数据：`{"live_url", "claim_url", "account", "account_state", "expires_minutes", "deployed"}`。）

4. **验证部署内容是否真正已上线**——切勿仅凭部署日志来判断。请使用 `curl` 访问实时 URL，并确认其返回的内容与代码输出的结果一致：
   ```
   curl -sS <live_url>
   ```

5. **迭代优化。**编辑代码后，使用相同的命令 `npx wrangler@latest deploy --temporary` 进行重新部署。在60分钟的时间窗口内，Wrangler会重用已缓存的临时账户（显示为“Account: <name> (reused)”），从而保持URL的稳定性。此时可再次使用 `curl` 命令来确认更改是否生效。

6. **将获取链接告知用户。**需告知用户：必须在60分钟内打开该链接，才能保留部署内容及所有相关资源；若未及时操作，所有内容将会自动删除。请将此获取链接视为机密信息——它决定了账户的所有权。

## 快速参考

| 步骤 | 命令 |
|---|---|
| 检查版本（需4.102.0及以上） | `npx wrangler@latest --version` |
| 无账户部署 | `npx wrangler@latest deploy --temporary` |
| 部署并解析URL | `npx wrangler@latest deploy --temporary 2>&1 \| python scripts/parse_deploy_output.py` |
| 验证链接是否可用 | `curl -sS <live_url>` |
| 清除缓存的临时账户 | `npx wrangler@latest logout` |

### 临时账户的产品限制

| 产品类型 | 临时账户的限制 |
|---|---|
| Workers | 可部署到 `workers.dev` 地址 |
| 静态资源 | 最多1,000个文件，每个文件大小不超过5 MiB |
| KV存储 | 支持使用 |
| D1实例 | 允许创建1个数据库，每个数据库容量为100 MB，总计上限为100 MB |
| 持久对象 | 支持使用 |
| Hyperdrive | 允许配置2种设置，最多支持10个连接 |
| 队列 | 最多可创建10个队列 |
| SSL/TLS证书 | 支持使用 |

## 常见问题与注意事项

- **`--temporary` 并未出现在 `wrangler deploy --help` 的列表中，也不属于全局标志。**该标志是刻意隐藏的，会动态显示：当未经身份验证的 `wrangler deploy` 操作失败时，Wrangler 会提示“使用 `--temporary` 重新运行”。切勿仅因 `--help` 中未列出该标志就认为其不存在——应检查软件版本。
- **过旧的全局 Wrangler 版本。** 已过时的全局安装版 Wrangler（版本 `< 4.102.0`）会默认不支持该标志。务必使用 `npx wrangler@latest`（或指定版本号 `>=4.102.0`）的命令来确保使用特定版本。
- **已登录状态 → 严重错误。** 如果曾经执行过 `wrangler login` 操作，或者设置了 `CLOUDFLARE_API_TOKEN`/`CLOUDFLARE_API_KEY`，则使用 `--temporary` 会引发错误。此时要么为当前终端取消设置相关变量，要么执行 `wrangler logout`。绝不能在未告知用户的情况下删除其真实凭证。
- **速率限制。** 过快创建临时账户会导致操作失败。建议在 60 分钟时间内重复使用已缓存的账户（只需重新部署），而非强制创建新账户；若遇到速率限制，可等待片刻或使用永久账户。
- **60 分钟的硬性截止时间，不可延长。** 如果需要让部署结果持续超过一小时，用户必须主动接管该部署任务。相关提示应清晰明确地展示出来。
- **重新部署后，`curl` 可能会短暂显示旧内容。** `workers.dev` 拥有短暂的边缘缓存机制；即便 `curl` 显示过时的内容几秒钟，出现“(reused)”字样以及新的“当前版本号”即可证明部署已成功。在判定重新部署失败之前，建议再次执行 `curl` 命令，或添加用于清除缓存的查询字符串。
- **切勿将索赔链接仅作为“普通链接”记录在共享的日志中**。实际上它具有与凭证相同的敏感度。

## 验证步骤

- 运行 `npx wrangler@latest --version`，输出结果应大于或等于 `4.102.0`。
- 执行 `npx wrangler@latest deploy --temporary`，系统会输出 `workers.dev` 的实时访问地址以及带有 `claim-preview?claimToken=` 参数的索赔链接。
- 使用 `curl -sS <live_url>` 命令，可获取 Worker 代码生成的完整内容。
- 进行第二次部署时，系统会显示 `Account: <name> (reused)` 的提示，且实时访问地址保持不变。
- 解析脚本的自检功能可通过测试：运行 `python scripts/parse_deploy_output.py --selftest`。
