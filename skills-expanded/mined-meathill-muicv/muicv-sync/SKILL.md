---
name: muicv-sync
description: MuiCV 平台云同步——把本地素材库整体推到云端（push）或从云端拉回来覆盖本地（pull），默认走 zip 加密路径。两个子任务：`push` 把本地素材打包成 zip（用户给密码就 PKZip 加密、不给就明文）上传到 muicv 云端；`pull` 从云端把活动版下载到本地（自动备份冲突文件）。使用场景：用户说「同步到云端」「上传简历素材」「云同步」「备份到云端」「换了新机器，把素材拉回来」「从云端恢复」「下载我的简历」「pull 远程素材」等。需要在 https://muicv.com/dashboard 创建 mui_ API key 并 export 到 `MUICV_API_KEY`；需要网络；需要本地装有 `zip` / `unzip`（三大系统通常自带）。
---

# muicv-sync

把整个本地素材库（profile / experience / projects / versions / 全部 .md 和图片）作为一份完整快照在本地和 muicv 云端之间双向同步。云端只保留一份**活动版** + 最近 5 份历史；用户可在 https://muicv.com/dashboard/sync 查看、回滚、清空。

**两条上传路径**：

- **加密路径（默认推荐）**：本地用 `zip -e` 打包加密，密文上传到新的 blob 端点。服务端只能拿到密文 + 一段不带敏感内容的摘要，dashboard 上只显示摘要 + 大小 + 时间，要看内容只能"下载 .zip 自己解密"。
- **明文路径（兜底，用户说不要密码）**：沿用老的按文件 JSON sync，服务端能按文件存，dashboard 上能看到文件列表 / 照片预览。

**边界（重要）**：
- **整库同步语义**：push 是把当前本地工作目录所有素材文件完整覆盖云端活动版；pull 是把云端活动版完整下载到本地（本地多出来的文件不动）。**没有按文件挑选 / merge / diff**——要细粒度操作请直接编辑文件。
- **last-write-wins**：每次 push 前云端会自动归档当前活动版到 history（保留最近 5 份），所以"误覆盖"可在 dashboard 一键恢复。
- **支持的文件类型**：
  - **加密路径**：`.md` + 常见图片（`.jpg / .jpeg / .png / .webp / .gif / .svg`）—— zip 内服务端不解析，啥都能塞。
  - **明文路径**：**只接受 `.md`**——服务端按文件存 JSON，dashboard 上要按文件浏览，不适合二进制。素材里有图片只能走加密路径。
  - **`.pdf` 一律忽略**：那是 muicv-render 生成的产物，pull 回新机器后用 muicv-render 现拉现渲就行，不进同步。
- **单库上限**：明文 50 MB / 1000 文件；blob 上传上限 60 MB（zip + 加密余量）。超限服务端会 413 / 400。再大就要清理（删旧 versions / critiques / 大照片）。
- **密码不持久化**：加密路径里用户给的密码只在当次 push / pull 进程里用一下，**绝不**写到任何文件 / env / store；skill 报告里也**绝不**回显密码字面值。pull 时密码记不住没法找回，只能去 dashboard 删掉重 push。

> 鉴权 / 计费 / 错误处理统一规范见 [docs/skill-api-key.md](../../docs/skill-api-key.md)。云同步本身**不扣 token**，但同样强制 Bearer 鉴权。

---

## 前置检查

> ⚠️ **教育用户优先**：如果发现 `MUICV_API_KEY` 没设，**先把下面"如何拿到 key"的步骤完整告诉用户**，不要执行任何 push/pull。这是 skill 用户和 client 用户的关键差异——skill 里 key 是用户自己 export 的，client 里登录后是自动注入的。第一次配 key 是一次性投入，但绝大多数用户没做过这件事。

### 1. 素材库根

prelude 已探查 `**/profile.md`：
- **push** 必须有根，否则报错让用户先 `muicv-core` 初始化或编辑素材
- **pull** 没有根也行——会把云端内容下载到当前工作目录，相当于在新机器恢复

### 2. 工具检查

```bash
zip --version 2>/dev/null | head -1
unzip -v 2>/dev/null | head -1
```

- mac / linux 通常自带；最小 linux 镜像缺则 `apt install zip unzip` / `yum install zip unzip`
- windows 下走 git-bash 自带的 zip / unzip，或装 7-zip 后用 `7z` 替代（流程要小调）
- 工具缺 → 提示安装，**不要**自己 brew install

### 3. API 地址（同 muicv-render / muicv-jobs 的优先级）

1. 用户对话明确指定的 URL（"同步到 localhost:8787"）
2. 环境变量 `MUICV_API_BASE`
3. 默认 `https://api.muicv.com`

### 4. API key 教育流程（关键）

云同步两个端点都强制 Bearer 鉴权。读 `MUICV_API_KEY` 环境变量；**没设或为空** → 别开始 push/pull，把下面整套发给用户：

> 还没看到你配置 muicv API key。云同步需要 key 来识别身份和计费（云同步本身不扣 token，但同样强制鉴权）。一次性配好就行，以后 skill 自己读：
>
> 1. 浏览器打开 **https://muicv.com/dashboard/api-keys**（如果还没注册，先去 muicv.com 注册——注册赠 10K token）
> 2. 点「创建 key」，给它起个名（比如"我的 mac"），复制弹出来的 **`mui_xxxxxxxx...`**（只显示一次，错过就只能撤销重发）
> 3. 写到 shell rc 里：
>    ```bash
>    # macOS / Linux
>    echo 'export MUICV_API_KEY="mui_刚才复制的那串"' >> ~/.zshrc
>    source ~/.zshrc
>    # bash 用户把 .zshrc 换成 .bashrc / .bash_profile
>
>    # Windows (PowerShell)
>    setx MUICV_API_KEY "mui_刚才复制的那串"
>    # 然后重开终端
>    ```
> 4. 验证：`echo $MUICV_API_KEY`（Windows: `echo %MUICV_API_KEY%`）看到 `mui_` 开头 36 字符 → 配好了
> 5. 回来跟我说"重试同步"

**已设但格式异常**（不匹配 `/^mui_[A-Za-z0-9]{32}$/`）→ 别调 API，回：

> 你这个 key 看起来不像 muicv 发的。可能复制时漏了字符或多了空格、引号；
> 去 https://muicv.com/dashboard/api-keys 重新发一份再 export 试试。

**已设格式正确** → 继续 push/pull 流程。第一次跑流程前可以选择性调一次 `GET ${MUICV_API_BASE}/me` 验证 key 有效（200 = 通过；401 = key 已被撤销/过期，让用户重新生成）。如果用户性子急可省略这一步。

---

## 子任务：push（同步到云端）

**触发**：用户说「同步到云端」「上传到 muicv」「备份素材到云端」「云同步」等。

### 步骤 1：安全检查

1. 确认素材库根存在（profile.md 父目录）。如果根不在工作目录顶层，所有路径都按**相对素材库根**计算，不是相对工作目录。
2. Glob 素材库根下所有 `.md` + 图片，过滤：
   ```
   Glob: **/*.md, **/*.{jpg,jpeg,png,webp,gif,svg}
   ```
   过滤掉路径里含以下任一段的：
   - 任何以 `.` 开头的目录段（`.git/`、`.vscode/`、`.muicv-pull-backup-*/` 等）
   - `node_modules/`
   - **`*.pdf`**（renderer 产物，不进同步——用户每次都能用 muicv-render 重新生成）
3. **若命中任何图片** → 决定必须走**加密路径**（服务端明文 API 只收 `.md`）。后面询问密码时不接受"不要密码"，要么用户给密码，要么用户先把图片移出素材库再 push。
4. 自检大小和文件数：
   - 总字节数 > 45 MB（接近 50 MB 上限）→ 提醒用户"快超上限了，建议清掉旧的 versions/ 或大照片"，但仍可继续
   - 总字节数 > 50 MB **或** 文件数 > 1000 → **不要继续**，告诉用户超限要先清理（重点提：大照片、`versions/*.md` 老快照、`critiques/*.md` 旧反馈）
5. 校验 `MUICV_API_KEY` 已设、格式 OK（见前置检查）。

### 步骤 2：告知加密方式 + 询问密码

**不要默认就走加密** / **不要默认就走明文**——把选择权丢给用户：

> 我会把这份素材库打包成 zip（共 `<N>` 个文件，含 `<M>` 张照片，明文 `<X.X MB>`）。
>
> - **给一个密码** → 我用 `zip -e`（PKZip 加密）压一遍再上传，服务端只能拿到密文 + 一段不带敏感内容的摘要。Pull 时还要这个密码才能解开，**记不住没法找回**。
> - **不要密码** → 直接走老的明文路径，服务端能按文件存，dashboard 上能看到文件列表 / 照片预览。
>
> 密码请直接发给我（我只在这次同步用一下，不写到任何文件，跑完就丢）；不想加密就回"不要密码"。

**等用户回复**——拿到密码 → 走步骤 3a；用户说"不要密码" / "明文" / "不加密" → 走步骤 3b。

### 步骤 3a：加密分支（用户给了密码）

```bash
# 1. 临时暂存目录（保持相对路径）
STAGE=$(mktemp -d /tmp/muicv-sync-stage-XXXXXX)
BLOB=/tmp/muicv-blob-$$.zip

# 2. 把所有 .md + 图片按相对路径 cp 进 STAGE
#    用 rsync / cp -R + 白名单过滤，注意保留子目录
rsync -a \
  --include='*/' \
  --include='*.md' \
  --include='*.jpg' --include='*.jpeg' --include='*.png' \
  --include='*.webp' --include='*.gif' --include='*.svg' \
  --exclude='*.pdf' \
  --exclude='.*/' \
  --exclude='node_modules/' \
  --prune-empty-dirs \
  <素材库根>/ "$STAGE/"

# 3. 在 STAGE 里 zip 加密（密码字面值会出现在命令行，没关系：
#    Bash 工具的 stdout 会进对话，用户已经接受密码可以发给 AI provider）
( cd "$STAGE" && zip -rq -P "<用户给的密码>" "$BLOB" . )

# 4. 模板化摘要（默认不让 AI 看明文）
SUMMARY="快照 $(date '+%Y-%m-%d %H:%M') · <N> 文件 · <X.X> KB · 顶层: experience/, projects/, versions/"

# 5. POST blob 端点
curl -sS -X POST "$MUICV_API_BASE/resume/sync/blob" \
  -H "Authorization: Bearer $MUICV_API_KEY" \
  -F "blob=@$BLOB" \
  -F "summary=$SUMMARY"

# 6. 跑完立刻清理（不管成功失败都清）
rm -f "$BLOB"
rm -rf "$STAGE"
```

**密码不持久化的硬约束**（**违反就是 bug**）：
- 不写到 `.env` / shell rc / store / 任何文件
- 不 `export` 到全局环境
- skill 报告里**绝不**回显密码字面值
- 临时 zip blob 跑完立刻 `rm -f`，哪怕上传失败也要清
- bash 进程结束 = 密码生命周期结束

如果用户主动说"帮我描述这次的变化" / "总结一下" → 让 AI 读明文写一句话当摘要（用户自愿暴露明文给 AI）；否则用模板化摘要。

### 步骤 3b：明文分支（用户说不要密码）

沿用老的按文件 JSON sync 流程：

1. 对每个 `.md` 用 Read 拿内容（图片需要 base64 编码后塞进同一个 JSON，路径全用 `/` 分隔；服务端要求 `/`）。
2. 组装：
   ```json
   {
     "files": {
       "profile.md": "<text>",
       "experience/google-2024.md": "<text>",
       "assets/avatar.jpg": "<base64>"
     }
   }
   ```
3. 写到临时文件再 `-d @<file>`，避免大 body 在命令行被截断：
   ```bash
   curl -sS -X POST "$MUICV_API_BASE/resume/sync" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $MUICV_API_KEY" \
     -d @/tmp/muicv-sync-payload-$$.json
   rm -f /tmp/muicv-sync-payload-$$.json
   ```

### 步骤 4：响应

加密分支：
- `200 OK` + `{ blobId, sizeBytes, summary, updatedAt }` → 上传成功
- `413` → blob > 60 MB，让用户清理大文件再来
- `401` → key 无效或被撤销，让用户去 dashboard 重发 key
- `5xx` / 网络错 → 让用户重试一次；连续失败提示去 https://muicv.com 检查服务

明文分支：
- `200 OK` + `{ hash, sizeBytes, fileCount, updatedAt }` → 上传成功
- `400` → 路径校验失败（含 `..` / 不在白名单扩展名 / 太长）或超限。把 `error` 字段返回的具体原因转告用户

### 报告格式

加密版：
```
✓ 已加密同步 14 个文件 (密文 1.2 MB)
  blobId: a1b2c3d4...
  最后同步：2026-05-10 14:23
  在 https://muicv.com/dashboard/sync 查看 / 下载 .zip 自己解密
  ⚠ 密码我没保存，请你自己记住——pull 时还需要它
```

明文版：
```
✓ 已同步 14 个文件到云端 (1.2 MB) [明文]
  hash: a1b2c3d4...
  最后同步：2026-05-10 14:23
  在 https://muicv.com/dashboard/sync 查看历史 / 回滚
```

---

## 子任务：pull（从云端恢复）

**触发**：用户说「从云端恢复」「拉远程素材」「下载我的简历」「换了新机器把素材同步过来」等。

### 步骤 1：检查（不会破坏）

- 校验 `MUICV_API_KEY`、API 地址。
- 如果当前工作目录已有素材库，准备好"冲突文件先备份到 `.muicv-pull-backup-<YYYYMMDD-HHmmss>/`"的承诺；告诉用户："本地比云端多的文件不会动；冲突的会先备份再覆盖"。

### 步骤 2：探活动版

先试加密 blob，再 fallback 明文：

```bash
# 先看有没有加密 blob
META=$(curl -sS -w '\n%{http_code}' "$MUICV_API_BASE/resume/snapshot/blob" \
        -H "Authorization: Bearer $MUICV_API_KEY")
# 200 → 是加密版；404 → 看明文版
```

- 加密版（200）：拿到 `{ blobId, sizeBytes, summary, updatedAt }`。把摘要 + 大小 + 时间报给用户，确认是这一份。
- 明文版（blob 404 + plaintext 200）：调老的 `GET /resume/snapshot` 拿 `{ files, hash, ... }`，跳过密码询问直接走步骤 5b。
- 都没有（双 404）→ "云端还没快照，先在另一台机器或本机说'同步到云端'才能 pull"。

### 步骤 3a：下载加密 blob

```bash
PULL_ZIP=/tmp/muicv-pull-$$.zip
curl -sS -o "$PULL_ZIP" \
  "$MUICV_API_BASE/resume/snapshot/blob/<blobId>/download" \
  -H "Authorization: Bearer $MUICV_API_KEY"
```

### 步骤 4a：询问密码

> 请输入 push 时用的密码（不加密的快照直接回车）

等用户回复。**不要**自己猜 / 不要从环境变量读。

### 步骤 5a：解压 + 合并

```bash
PULL_STAGE=$(mktemp -d /tmp/muicv-pull-stage-XXXXXX)

# 加密版
unzip -P "<密码>" -q "$PULL_ZIP" -d "$PULL_STAGE"
# 不加密版（用户回车）—— blob 没加密时直接 unzip
# unzip -q "$PULL_ZIP" -d "$PULL_STAGE"

# 接管做 diff + 备份冲突 + 写入：
# 1. 列 PULL_STAGE 里所有文件
# 2. 对每个文件：本地有且不同 → cp 本地版到 .muicv-pull-backup-<ts>/<相对路径>，然后写云端版
# 3. 完全没本地 → 跳过备份直接写
# 4. 本地多余的（云端没的）不动

# 清理（不管成功失败都清）
rm -f "$PULL_ZIP"
rm -rf "$PULL_STAGE"
```

`unzip` 报 "incorrect password" → 走错误处理小抄。

### 步骤 5b：明文分支

沿用老逻辑：拿到 `{ files: {...} }` 后 Read 比对 + 备份 + Write，过程跟旧版本一致。

### 步骤 6：报告

```
✓ 从云端拉取了 14 个文件 (1.2 MB) [加密]
  blobId: a1b2c3d4...
  最后同步：2026-05-10 14:23

  📦 5 个本地文件已被覆盖；旧版备份在 .muicv-pull-backup-20260510-142300/
  ➕ 9 个新文件已写入
  💡 本地还有 3 个云端没有的文件，未触碰（如要完全镜像请手动删除）
```

---

## 子任务：status（可选，看一眼云端状态）

**触发**：用户问「云端有多少东西」「最后什么时候同步的」等只想看不想动的需求。

直接引导去 https://muicv.com/dashboard/sync —— 那里有完整的状态卡 + 历史列表 + 一键回滚 / 清空。skill 不重复造 UI。

如果用户坚持要 skill 报，调 `GET /resume/snapshot/blob`（先）或 `GET /resume/snapshot`（fallback）后**只显示 metadata**（blobId / hash、sizeBytes、fileCount、updatedAt、summary），不要把 files 内容写到本地。

---

## 错误处理小抄

每条响应都尽量翻译成"用户能直接行动"的话，不要原样抛 HTTP 状态码。规范见 [docs/skill-api-key.md](../../docs/skill-api-key.md)。

通用映射（同所有联网 skill）：

| 现象 | 给用户怎么说 |
|---|---|
| `MUICV_API_KEY` 没 export | 走前置检查里的「API key 教育流程」，五步详细发给用户 |
| `MUICV_API_KEY` 格式异常（不匹配 `/^mui_[A-Za-z0-9]{32}$/`）| "你这个 key 看起来不像 muicv 发的。可能复制时漏了字符或多了空格、引号；去 https://muicv.com/dashboard/api-keys 重新发一份再 export 试试。" |
| `401 missing-api-key` / `401 unauthorized` | "muicv 拒了这个 key（可能在 dashboard 撤销过、或者过期）。去 https://muicv.com/dashboard/api-keys 重新发一份，更新 shell rc 后 `source` 一下再来。" **不要重试**。 |
| `429 rate-limited` | "调太频了，等 60s 再试。" |
| 网络错 / 超时 | API 一般 <1s；超时多半是网络。"试一次没通常就别再硬试，先看看 https://status.muicv.com 或检查本地网络（dashboard 能正常打开吗？）" |

业务特有：

| 现象 | 给用户怎么说 |
|---|---|
| `zip` / `unzip` 没装 | mac 自带；linux `apt install zip unzip`；windows 用 git-bash 自带，或装 7-zip |
| `400` 路径 / 类型 / 超限（明文路径）| 把 server 的 `error` 字段原话转给用户（例如「only .md and image files are supported: foo.pdf」「total size exceeds 50 MB」）；超限就建议清 versions/ critiques/ 大照片 |
| `413` blob 超限（加密路径）| "blob 超过 60 MB——清理大照片 / `versions/` 里的旧快照再来" |
| `404 no-snapshot`（pull）| "云端还没有这个账号的快照——先在另一台机器或本机说'同步到云端'才能 pull" |
| pull 时 `unzip` 报 "incorrect password" | "密码不对——push 时记错了？没法找回。两个出路：① 去 https://muicv.com/dashboard/sync 删掉这份快照，重新 push 一份用记得住的密码；② 在源机器上再 push 一次（这次记牢密码）。" **不要重试 unzip**。 |
| 加密 push 上传失败但本地 zip 已生成 | 立刻 `rm -f /tmp/muicv-blob-*.zip`，告诉用户"上传失败已清理临时文件，重试请重新输密码（我没保存）"。 |

---

## 调用示例

### 例 1：第一次加密 push

```
用户：把我的素材同步到云端
Claude:
  1. Glob **/*.md + 图片 → 14 个文件（11 个 .md + 3 张照片），明文 1.2 MB
  2. 自检通过（< 50 MB / < 1000 文件）
  3. 报告大小 + 询问密码：
     "我会打包 14 个文件成 zip（明文 1.2 MB）。给一个密码 → 加密上传；
      不要密码 → 走明文路径。"
用户：密码用 hunter2025
Claude:
  4. mktemp -d → /tmp/muicv-sync-stage-AbCdEf
  5. rsync 进 STAGE（保留子目录，过滤 .pdf / 隐藏）
  6. cd STAGE && zip -rq -P hunter2025 /tmp/muicv-blob-12345.zip .
  7. 摘要 = "快照 2026-05-10 14:23 · 14 文件 · 1.2 MB · 顶层: experience/, projects/, assets/"
  8. curl POST /resume/sync/blob → { blobId: "a1b2c3", sizeBytes: 1238291, ... }
  9. rm -f /tmp/muicv-blob-12345.zip && rm -rf STAGE
  10. 报告：✓ 已加密同步 14 个文件 (密文 1.2 MB)，blobId a1b2c3
      ⚠ 密码我没保存，请你自己记住
```

### 例 2：换新机器加密 pull

```
用户：换了台 Mac，把我的简历拉回来
Claude:
  1. 检查 MUICV_API_KEY 已 export
  2. GET /resume/snapshot/blob → 200，summary "14 文件 · 1.2 MB · 2026-05-10 14:23"
  3. 报告摘要 + 询问密码：
     "云端有一份加密快照（1.2 MB，2026-05-10 14:23）要拉吗？
      请输入 push 时的密码"
用户：hunter2025
Claude:
  4. curl 下载 blob → /tmp/muicv-pull-67890.zip
  5. mktemp -d STAGE
  6. unzip -P hunter2025 → STAGE/ 全部 14 个文件解出来
  7. 当前工作目录没有素材 → 跳过冲突备份
  8. cp -R STAGE/* <工作目录>/
  9. rm -f /tmp/muicv-pull-67890.zip && rm -rf STAGE
  10. 报告：✓ 从云端拉取了 14 个文件 (1.2 MB) [加密]
```

### 例 3：明文 push（用户不在乎）

```
用户：同步一下，不要密码我懒得记
Claude:
  1. Glob → 11 个 .md（明文 43 KB；用户没放图片）
  2. 自检通过
  3. Read + 组装 JSON → /tmp/muicv-sync-payload-12345.json
  4. POST /resume/sync → { hash, sizeBytes: 44213, fileCount: 11, ... }
  5. rm -f payload
  6. 报告：✓ 已同步 11 个文件 (43.2 KB) [明文]
      在 https://muicv.com/dashboard/sync 看历史 / 回滚
```

### 例 4：本地改过又 pull（备份场景）

```
用户：从云端覆盖本地
Claude:
  1. GET /resume/snapshot/blob → 拿到加密 blob 元数据
  2. 询问密码 → 用户给 hunter2025
  3. 下载 + unzip 到 STAGE
  4. 对比：experience/google-2024.md 本地内容 ≠ 云端 → 先 cp 到 .muicv-pull-backup-20260510-143022/experience/google-2024.md
  5. 写云端版到 experience/google-2024.md
  6. 其他没改的不备份
  7. 报告：✓ 拉取 14 个文件，1 个本地版本已备份到 .muicv-pull-backup-...
```

---

## 与其他 skill 的协作

- `muicv-core` 初始化 / 增删素材 → push 上云
- 换机器 → pull 把素材库重建
- 本地编辑后 → 再次 push 覆盖云端（旧版自动归档到 history）
- `muicv-render` 生成的 PDF **不**进同步——pull 回新机器后再用 `muicv-render` 重渲就行
- `muicv-git` 是平行选项（白盒 git workflow），可以同时用：git 主仓做版本管理，muicv-sync 做加密二级备份
- dashboard `/dashboard/sync` 一键回滚 / 清空（skill 不做这些破坏性动作的 UI，让用户去 web 端）
