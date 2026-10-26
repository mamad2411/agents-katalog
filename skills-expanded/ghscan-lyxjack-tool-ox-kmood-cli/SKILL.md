---
name: kmood-cli (prod)
description: 用 kmood-cli（生产版 / prod）命令行操作 kmood 漫剧视频创作平台——认证、项目管理、批量创建设定与分镜、查询积分与模型。本产物锁定「正式 prod」环境。当用户要通过终端/脚本驱动 kmood 时使用。
---

# kmood-cli 使用指南（生产版 / prod）

kmood-cli 是 kmood 漫剧视频创作平台的命令行工具（bin 名 `kmood`）。
**本产物由 `build:prod` 构建：环境锁定为「正式 prod」（`https://kmood.cn`），不接受 `--env` 参数。** 本文档教你（agent）如何**非交互地**驱动它。

## 交互 vs 非交互（重要）

命令缺参数时会进入**交互式提问/选单/浏览器**。**若你（agent）不支持交互，务必用非交互形式**（带全参数），否则会卡住：

- 认证：用 `kmood init --api-key <KEY>`（非交互）；`kmood login` 是**浏览器交互式**登录，仅在有人工/可交互环境时用（见「认证」）。
- `project create` 带 `--name`（并按需 `--style/--ratio`）；`create-settings` 带 `--file` 或单条参数；`create-prompts` 必带 `--file`（仅文件模式）并显式传 `--episode`。

失败时命令以非 0 退出并打印 `✖ <原因>`（见「错误处理」）。

## 认证

配置存于 `~/.kmood/config.json`（本版本 env 恒为 prod）。先查状态：

```bash
kmood auth show     # 昵称 / env(prod) / base_url / 当前项目（api_key 掩码）
kmood auth test     # 校验 api_key 是否有效（有效退出 0）
```

两种登录方式：

- **非交互（agent 首选）**：直接用 api_key
  ```bash
  kmood init --api-key <API_KEY>
  ```
- **交互式（浏览器授权，关键步骤，需人工）**：`kmood login`
  打开浏览器 → 用户在网页登录并点「授权」→ CLI 自动拿到 api_key 并写入本地，同时记录昵称。这是获取 api_key 的**主要人工方式**。
  ```bash
  kmood login              # 自动开浏览器；加 --no-browser 则只打印地址供手动打开
  ```
  agent 无法完成浏览器授权，应改用上面的 `init --api-key`（api_key 可由已 `login` 的人工/前置步骤提供）。

## 命令速查

| 命令                                | 用途                                  | 非交互要点                           |
| ----------------------------------- | ------------------------------------- | ------------------------------------ |
| `kmood init --api-key <KEY>`        | 用 api_key 认证                       | 推荐的 agent 认证方式                |
| `kmood login`                       | 浏览器授权登录                        | **交互式**，需人工；agent 勿用       |
| `kmood auth show / test`            | 查看/校验认证                         | —                                    |
| `kmood logout`                      | 清除本地凭证                          | —                                    |
| `kmood project create --name <名>`  | 创建项目                              | 必带 `--name`；风格/比例创建后不可改 |
| `kmood project list`                | 项目列表（表格）                      | 从这里取 projectId                   |
| `kmood project select <projectId>`  | 设为当前项目                          | —                                    |
| `kmood project episodes`            | 查看当前项目剧集                      | 取 episodeId（供 `create-prompts`）  |
| `kmood project create-episode`      | 在当前项目下创建剧集                  | 返回新 episodeId                     |
| `kmood project create-settings ...` | 批量创建设定                          | `--file` 或单条                      |
| `kmood project create-prompts ...`  | 批量创建分镜                          | 仅 `--file`（xlsx/csv）              |
| `kmood points`                      | 查询剩余积分                          | 输出 `剩余积分：N`                   |
| `kmood models`                      | 查询各场景支持的模型与参数            | agent 用 `--json`；`--scene` 过滤    |
| `kmood upgrade`                     | 自更新到最新版                        | 见「自更新」                         |
| 全局 `--debug`                      | 打印每个请求的 req/resp + 可复现 curl | 排查用                               |

## 详细用法

### 创建项目

```bash
kmood project create --name "我的漫剧" [--style <styleId>] [--ratio 9:16] [--script-text "剧本..."]
```

- `--name` 必填（缺省会交互提问）。
- `--style` 省略时自动取可选风格第一个。styleId 可在 web 端项目创建页查看；**agent 一般省略即可**，CLI 会自动选择。
- `--ratio` 省略时默认 `9:16`（可选 `1:1/9:16/16:9/3:4/4:3`）。
- `--script-text` 传入剧本文本（可选）。传入后后端会以「内容型剧本」模式解析并自动生成分镜；省略则创建空项目，后续通过 `create-prompts` 手动添加分镜。
- ⚠️ **风格与比例在项目创建后不可修改**，需在创建时确定；不确定就显式传 `--style`/`--ratio`。
- 成功后**自动设为当前项目**，并打印 `项目 ID: <id>`。后续 `create-settings`/`create-prompts` 默认作用于它。

### 查看/切换项目

```bash
kmood project list                 # 表格：ID / 名称 / 分镜数 / 集数
kmood project select <projectId>   # 切换当前项目
```

### 查看剧集

作用于当前项目（或 `--project <id>` 指定）。用于拿到 `create-prompts` 所需的 episodeId。

```bash
kmood project episodes             # 表格：剧集 ID / 标题 / 分镜数 / 时长(s) / 比例
kmood project episodes --project <id> --limit 50
```

- 剧集可在 web 端或用 `kmood project create-episode` 创建；无剧集时输出「该项目暂无剧集」。

### 创建剧集

在当前项目（或 `--project <id>`）下创建一个新剧集，返回新的 episodeId，可直接用于 `create-prompts`。

```bash
kmood project create-episode                       # 创建空剧集，打印剧集 ID
kmood project create-episode --project <projectId>
```

- 成功后打印 `剧集 ID: <id>`、标题、分镜数。
- `--param key=value`（可重复）为剧本解析参数的高级透传，普通创建无需传。

### 批量创建设定（角色/场景/道具）

作用于当前项目（或 `--project <id>` 指定）。

```bash
kmood project create-settings --file settings.json
kmood project create-settings --name "白衣剑客" --description "冷峻剑客" --type role \
  --image-prompt "白衣束发青年剑客" --audio-prompt "低沉磁性男声" --video-prompt "御剑飞行"
```

`settings.json` 格式（`type` ∈ `role`/`scene`/`prop`）：

```json
[
  {
    "name": "白衣剑客",
    "description": "冷峻青年剑客",
    "type": "role",
    "imagePrompt": "白衣束发青年剑客",
    "audioPrompt": "低沉磁性男声",
    "videoPrompt": "御剑飞行"
  },
  { "name": "雪山之巅", "description": "夕阳雪景", "type": "scene" }
]
```

- 字段：`description`（设定描述）；`imagePrompt`（图片提示词）、`audioPrompt`（音频提示词）、`videoPrompt`（视频提示词）**均可选**，单条创建分别对应 `--description`/`--image-prompt`/`--audio-prompt`/`--video-prompt`。
- **隐私**：用户上传本地文件时，勿将本地路径（如 `/Users/.../角色.png`）填入 `description` 等文件描述信息，以免泄露用户隐私；应使用语义化描述。
  输出：`成功 N 条，失败 M 条`，失败项逐条列出。

### 批量创建分镜

作用于当前项目的某个剧集。**统一走文件模式**（上传 xlsx/csv，后端异步解析）：

```bash
kmood project create-prompts --file shots.xlsx --episode <episodeId>
kmood project create-prompts --file shots.csv  --episode <episodeId>
```

- **剧集选择逻辑**：`--episode` 省略时，若项目仅有 1 个剧集则自动选中；多集时会进入交互选择（**agent 必须显式传 `--episode`**）。剧集可用 `kmood project episodes` 查询、`kmood project create-episode` 创建。
- **仅支持文件模式**（已移除 `--prompt` 文本模式），文件须为 xlsx/csv。
- **表头要求**（表头名称勿改，**必须为下列完整字符串**）：
  - 六列（顺序建议如下，名称必须一字不差）：`视频prompt`、`视频时长`、`视频模型`、`视频分辨率`、`图片prompt`、`音频prompt`
  - 完整表头示例（一行）：
    `视频prompt,视频时长,视频模型,视频分辨率,图片prompt,音频prompt`
  - ⚠️ 旧表头（如 `prompt（勿改表头名称）`、`视频时间（支持4～15s，只填数字就行）`、`图片生成prompt`）会被本地校验拒绝。
  - ⚠️ **必需列 ≠ 必须有值**：表头必须含这六列，但单元格**可以留空**。用户只指定音频/图片提示词而未给视频内容时，`视频prompt` 列**留空即可**，切勿把音频/图片内容擅自填入 `视频prompt` 列。
  - CSV 会在上传前做表头校验，缺列直接报错；xlsx 由后端解析校验。额外列会被忽略。
- **列含义与填法：**
  | 列 | 含义 | 如何填 |
  | --- | --- | --- |
  | `视频prompt` | 视频生成提示词 | 自然语言；可空 |
  | `视频时长` | 视频时长（秒） | **只填数字**；可空。若填写，必须是所选模型支持的 `durations` |
  | `视频模型` | 所用视频模型 | 填 `kmood models --json` 返回的 `modelCode`；可空。若填写，必须与查询结果完全一致（不要填 `name` / `modelId`） |
  | `视频分辨率` | 视频清晰度 | 填该模型的 `clarities`（如 `720p`）；可空。若填写，必须是该模型支持的值 |
  | `图片prompt` | 图片生成提示词 | 自然语言；可空 |
  | `音频prompt` | 音频生成提示词 | 自然语言；可空 |
- ⚠️ **填写「视频时长 / 视频模型 / 视频分辨率」之前，必须先查询支持的模型与参数**，确认该组合合法，不要凭经验填：
  ```bash
  kmood models --json
  kmood models --json --scene 10001   # 生视频模型（填「视频模型 / 视频时长 / 视频分辨率」时用这个）
  ```
  - 用返回的 `modelCode` 填 `视频模型`，必须与查询结果完全一致，**不要填 `name` 或 `modelId`**。若该模型 `modelCode` 为空则此列留空。
  - 用该模型的 `durations`（秒）填 `视频时长`，不要填不在列表里的秒数。
  - 用该模型的 `clarities` 填 `视频分辨率`，不要填不在列表里的清晰度。
  - 三者留空时由后端用默认模型/参数；**只要填了其中任一项，三项都应与同一模型的查询结果一致**（模型不支持该时长或分辨率会失败）。
- **提交成功即为成功**：命令返回 `✔ 已提交解析任务` 即代表成功，无需轮询等待。
- **分镜数不变属正常**：每集下会**预置 20 个空分镜**，批量提交的提示词会**覆盖**这些空分镜，因此提交前后用 `project episodes` 查询分镜数**没有区别**，不要据此判断成功与否。

### 查询积分

```bash
kmood points        # → 剩余积分：1234
```

### 查询支持的模型与参数

列出各生成场景当前可用的模型及其参数。**按用途选 `--scene`**，不要扫全部场景再猜。

```bash
kmood models --json --scene 2001    # 生图模型
kmood models --json --scene 10001   # 生视频模型
kmood models --json --scene 10002   # 视频首尾帧模式
kmood models --json --scene 10003   # 生音频模型
kmood models --json                 # 全部场景（排查用）
```

**scene 解读（按用途）：**

| 用途 | scene | sceneName | 说明 |
| --- | --- | --- | --- |
| 生图模型 | `2001` | `ASSET_IMAGEGEN` | 查图片生成可用模型与参数 |
| 生视频模型 | `10001` | `SHOTIFY_MULTIMODAL` | 查视频生成可用模型；批量创建分镜填「视频模型 / 视频时长 / 视频分辨率」用这个 |
| 视频首尾帧模式 | `10002` | `SHOTIFY_FIRST_LAST_FRAME` | 查首尾帧生视频可用模型与参数 |
| 生音频模型 | `10003` | `SHOTIFY_AUDIO` | 查音频生成可用模型与参数 |

`--scene` 也接受枚举名（如 `SHOTIFY_MULTIMODAL` / `MODEL_SCENE_SHOTIFY_MULTIMODAL`）。省略 `--scene` 则列出全部。模型按 `priority` 降序（同优先级按 `modelId` 升序）。**agent 必须用 `--json`** 解析 `modelCode` 与合法参数，不要从表格里猜。

`--json` 输出为数组，每项是一个场景及其模型列表：

```json
[
  {
    "scene": 10001,
    "sceneName": "SHOTIFY_MULTIMODAL",
    "sceneLabel": "生视频模型",
    "models": [
      {
        "modelId": "xxx",
        "name": "Seedance 2.0",
        "desc": "文生视频",
        "modelCode": "seedance2",
        "aspectRatios": ["9:16", "16:9"],
        "clarities": ["720p"],
        "durations": [5, 10],
        "tailFrameSupport": false,
        "maxImageCount": 0,
        "priority": 10
      }
    ]
  }
]
```

**场景字段：**

| 字段         | 含义                             |
| ------------ | -------------------------------- |
| `scene`      | 场景数字 ID（即 `ModelScene`）   |
| `sceneName`  | 场景枚举名，可直接传给 `--scene` |
| `sceneLabel` | 场景中文说明                     |
| `models`     | 该场景下可用模型列表             |

常见 `scene` / `sceneName`（**优先用上面四个用途**；其余场景较少用于批量创建分镜）：

| ID    | sceneName                                  | 说明                     |
| ----- | ------------------------------------------ | ------------------------ |
| 2001  | `ASSET_IMAGEGEN`                           | **生图模型**             |
| 2101  | `ASSET_VIDEOGEN`                           | 资产创作文生视频         |
| 2102  | `ASSET_VIDEOGEN_FTFRAME`                   | 资产创作首尾帧生视频     |
| 2103  | `ASSET_VIDEOGEN_REF_MULIMAGE`              | 资产创作多图参考生视频   |
| 2104  | `ASSET_VIDEOGEN_FIRST_FRAME`               | 资产创作首帧生视频       |
| 2201  | `ASSET_IDENTIFY_FACE`                      | 资产创作对口型-人脸识别  |
| 2202  | `ASSET_LIP_SYNC`                           | 资产创作对口型-人物配音  |
| 3001  | `SHOTIFY_IMAGEGEN_MATERIAL`                | 短片创作生素材图         |
| 3002  | `SHOTIFY_IMAGEGEN_STEP_STORYBOARD`         | 短片创作生分镜图         |
| 3101  | `SHOTIFY_VIDEOGEN_STORYBOARD`              | 短片创作文生分镜视频     |
| 3102  | `SHOTIFY_VIDEOGEN_STORYBOARD_FTFRAME`      | 短片创作首尾帧生分镜视频 |
| 3103  | `SHOTIFY_VIDEOGEN_STORYBOARD_REF_MULIMAGE` | 短片创作参考图生分镜视频 |
| 3104  | `SHOTIFY_VIDEOGEN_STORYBOARD_FIRST_FRAME`  | 短片创作首帧生分镜视频   |
| 3105  | `SHOTIFY_VIDEOGEN_SEEDANCE`                | seedance 2.0 视频生成    |
| 3106  | `SHOTIFY_BATCH_CREATE`                     | 短片创作批量生成         |
| 3107  | `SHOTIFY_VIDEOGEN_EDIT`                    | 视频编辑                 |
| 3201  | `SHOTIFY_IDENTIFY_FACE`                    | 短片创作对口型-人脸识别  |
| 3202  | `SHOTIFY_LIP_SYNC`                         | 短片创作对口型-人物配音  |
| 3203  | `SHOTIFY_REMOVE_SUBTITLE`                  | 擦除字幕                 |
| 3204  | `SHOTIFY_REMOVE_CHAOFEN`                   | 超分                     |
| 10001 | `SHOTIFY_MULTIMODAL`                       | **生视频模型**           |
| 10002 | `SHOTIFY_FIRST_LAST_FRAME`                 | **视频首尾帧模式**       |
| 10003 | `SHOTIFY_AUDIO`                            | **生音频模型**           |

**模型字段（选模型 / 填生成参数时用这些）：**

| 字段               | 含义                        | 取值说明                                     |
| ------------------ | --------------------------- | -------------------------------------------- |
| `modelId`          | 模型 ID                     | 字符串，非空。批量创建分镜的「视频模型」列**不要填这个** |
| `name`             | 模型名称                    | 如 `Seedance 2.0`。仅展示用，批量创建分镜**不要填这个** |
| `desc`             | 模型描述                    | 可能为空                                     |
| `modelCode`        | 模型路由 code               | 批量创建分镜的「视频模型」列填这个，须与查询结果完全一致；可能为空 |
| `aspectRatios`     | 支持的画面比例              | 如 `["9:16","16:9"]`；空数组表示未配置       |
| `clarities`        | 支持的清晰度                | 如 `["720p","1080p"]`；空数组表示未配置      |
| `durations`        | 支持的时长（秒）范围        | 如 `[5,10]`；空数组表示未配置                |
| `tailFrameSupport` | 是否支持尾帧                | `true` / `false`                             |
| `maxImageCount`    | 最大可支持参考图数量        | `0` 表示不限制或未配置                       |
| `priority`         | 排序优先级                  | 数值越大越靠前；仅用于展示排序，生成时不用传 |

表格模式列对应：`模型 ID`=`modelId`，`名称`=`name`，`code`=`modelCode`，`比例`=`aspectRatios`，`清晰度`=`clarities`，`时长(s)`=`durations`，`尾帧`=`tailFrameSupport`（是/否），`最大图`=`maxImageCount`（`0` 显示为 `-`）。空数组在表格中显示为 `-`。

### 自更新

```bash
kmood upgrade               # 检查最新版本并更新
kmood upgrade --version 1.0.1  # 安装指定版本
kmood upgrade --rollback     # 回滚到上一个版本（仅单文件安装）
kmood upgrade -y             # 跳过确认，直接更新
```

- CLI 自动检测安装通道：
  - **npm 全局安装**：执行 `npm install -g kmood-cli@<version>` 完成更新；回滚用 `npm install -g kmood-cli@<旧版本>`。npm 包内已含本 skill 文档，重装即同步更新。
  - **单文件下载**：从 CDN 下载新版 `cli.js` 原子替换当前文件，旧版自动备份为 `.bak`；`--rollback` 从 `.bak` 恢复。
- ⚠️ **cli.js 与本 skill 文档需保持同版本**：`kmood upgrade` 目前只更新 `cli.js`，不会自动更新本文档。单文件安装的用户升级 `cli.js` 后，请同步拉取最新 skill 文档，避免命令说明与实际 CLI 不一致：
  ```bash
  curl -fsSL https://h5.basemind.com/kmood-cli/skill.md -o <你的 skill 存放路径>/skill.md
  ```
  （npm 安装无需此步，重装 npm 包已带最新 skill 文档。）
- 启动时会后台检查新版本（24h 缓存），发现更新时在 stderr 提示 `发现新版本 X.Y.Z，运行 kmood upgrade 更新`。

## 错误处理

后端错误为统一结构：

```json
{ "code": 400, "reason": "项目名称已存在，请更换" }
```

CLI 会把 `reason` 直接展示为 `✖ <reason>` 并以**非 0 退出**。据此判断原因并处理，常见：

- `✖ 鉴权失败：api_key 无效或已过期` → 重新获取 api_key（人工 `kmood login`，或 `kmood init --api-key <KEY>`）。
- `✖ 项目名称已存在，请更换` → 换个项目名重试。
- `✖ 无权限访问该资源` / `资源不存在` / `网络或服务暂时不可用` → 分别检查权限 / ID 是否正确 / 稍后重试。

需要更多细节时加 `--debug`：打印每个 RPC 的请求/响应，以及一条**可复制给后端复现问题的 curl**（含真实鉴权头与请求体）：

```bash
kmood project list --debug
```



## 典型编排（agent）

```bash
kmood auth test || kmood init --api-key "$KMOOD_API_KEY"
kmood project create --name "古风漫剧"          # 自动设为当前项目，记下打印的项目 ID
kmood project create-settings --file settings.json
kmood models --json --scene 10001   # 生视频模型；填时长/模型/分辨率前先确认是否支持
kmood project create-prompts --file shots.csv --episode <episodeId>
kmood project list                              # 确认分镜数增长
kmood points
```

## 安装（正式环境）

**需要 Node.js >= 18。**

方式一（推荐）：npm 全局安装 —— 直接得到 `kmood` 命令
```bash
npm install -g kmood-cli
kmood --help
```

方式二：下载自包含单文件（已内联全部依赖，无需 `npm install`）。**保存为 `.mjs`**（node 按 ESM 运行，免设 `type:module`）：
```bash
curl -fsSL https://h5.basemind.com/kmood-cli/cli.js -o ~/kmood.mjs
node ~/kmood.mjs --help
# 可选：加别名得到 kmood 命令（免 sudo）
echo "alias kmood='node ~/kmood.mjs'" >> ~/.zshrc && source ~/.zshrc
```
（产物自带 shebang，`chmod +x ~/kmood.mjs` 后也可 `~/kmood.mjs --help` 直接执行。）
