---
name: qiniu-kodo
description: |
  七牛云 KODO 图床上传技能：将本地生成的图片（如封面图）上传到七牛云并返回公开 URL。
  仅保留“上传图片”这一条主链路，适配 generate-cover / content-creator 等工作流。
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["node"] },
        "install":
          [
            { "id": "qiniu-sdk", "kind": "node", "package": "qiniu", "label": "Install qiniu Node.js SDK" },
          ],
      },
  }
---

# ☁️ 七牛云 KODO 图床上传 Skill

此 Skill 用于把本地生成的图片（最常见是封面 `cover.png`）上传到七牛云 KODO，并返回可用于 Hugo/Markdown 的公开 URL。

## 你需要提供的信息

- `local`：要上传的本地图片绝对路径（通常来自 generate-cover 的输出）
- `key`：上传到 KODO 的对象 Key（推荐统一使用 `image/` 前缀，例如 `image/<slug>-cover.png`）
- `domain`：用于拼接公开访问 URL 的 CDN 域名（强烈建议配置）

## 配置方式

优先读取 `~/.kodo-config/qiniu-config.json`，其次读取 `qiniu-kodo/config/qiniu-config.json`（向后兼容），否则读取环境变量：
- `QINIU_ACCESS_KEY`
- `QINIU_SECRET_KEY`
- `QINIU_BUCKET`
- `QINIU_REGION`（可选，默认 `z0`）
- `QINIU_DOMAIN`（可选，但若不配置则无法返回 `url`）

`~/.kodo-config/qiniu-config.json` 示例：

```json
{
  "accessKey": "YOUR_ACCESS_KEY",
  "secretKey": "YOUR_SECRET_KEY",
  "bucket": "mybucket",
  "region": "z0",
  "domain": "https://cdn.example.com"
}
```

## 运行方式（唯一主流程：上传图片）

```bash
node scripts/qiniu_node.mjs upload \
  --local "/abs/path/to/cover.png" \
  --key "image/my-post-cover.png" \
  --cache-dir ./.qiniu-deps  # (可选) 自定义依赖缓存目录，默认 ~/.cache/qiniu-kodo-skill
```

*提示：`qiniu-kodo` 使用了和 `gen-cover-skill` 一致的依赖管理策略，首次运行时会自动静默安装 `qiniu` 依赖并进行缓存，不再需要手动执行 `npm install`。*

也可以不传 `--key`，此时会按 `--prefix` 与文件名自动生成：

```bash
node scripts/qiniu_node.mjs upload \
  --local "/abs/path/to/cover.png" \
  --prefix "image/"
```

## 输出格式

默认输出为单行 JSON，便于其它 Skill/Agent 稳定解析：

```json
{"success":true,"key":"image/my-post-cover.png","hash":"...","url":"https://cdn.example.com/image/my-post-cover.png","size":12345,"bucket":"mybucket"}
```

如需仅输出 URL，可加 `--format text`（若未配置 domain，则输出为空行）：

```bash
node scripts/qiniu_node.mjs upload --local "/abs/path/to/cover.png" --key "image/x.png" --format text
```
