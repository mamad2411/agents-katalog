---
name: ges-case-management
description: 当用户需要选择单机版或平台版火眼案件，或导入手机、电脑、服务器等镜像并等待解析时使用。支持列出和打开案件、按完整路径判断检材能否复用、查看解析状态，以及在单机版中创建案件并导入检材。
metadata:
  requires:
    bins: ["ges" ]
  cliHelp: "ges --help"
allowed-tools: Bash(ges*)
---

# 火眼案件准备与检材导入

用本 skill 选择案件、初始化上下文、导入检材并等待解析。单机版可创建和打开本地案件；平台版通过 GES 地址和 token 列出并选择远程案件。只有完整检材路径一致时才能复用旧检材。准备完成后切到 `ges-case-analysis`，先执行 `ges status`。

## 决策流程

### 1. 先看案件列表

先尝试读取当前上下文：

```bash
ges status
```

如果 `status` 成功，记录其中的当前 `cid` 和 `GES URL`，并显式执行：

```bash
ges --cid <status中的cid> --ges-url <status中的GES URL> case ls
```

如果 `status` 失败、当前没有上下文，才执行裸命令 `ges case ls` 查看本机案件：

```bash
ges case ls
```

单机版 `case ls` 输出 `case_number`、`name`、`location`、`ges_url`、`evidences`：

- `ges_url` 显示已发现的后台地址，可直接用于 `ges init --ges-url`；未发现地址时显示 `未打开`。
- `evidences` 会列出检材名称、镜像路径，并在存在时显示持有人和身份证。

如果显式传入当前 `cid/URL` 后有唯一一行 `ges_url` 与当前 `GES URL` 完全一致，该行就是当前案件。若仍没有 URL 匹配，执行 `ges evidence ls`，把当前所有非空 `path` 与各案件的 `evidences[].镜像路径` 逐字比较；只有所有当前检材路径恰好唯一匹配一个案件时，才把它认定为当前案件。禁止按案件名、检材名、持有人、`cid`、`eid`、相似路径或单个重复路径猜测。

如果用户提供了检材路径，先用 `case ls` 检查 `evidences` 中是否存在完全一致的 `镜像路径`。只有完全一致才复用该案件/检材；不一致就按新检材处理。

平台版配置了 `GES_MASTER_URL` 和 `GES_MASTER_TOKEN` 后，`case ls` 输出 `cid`、`case_number`、`name`、`evidence_count`、`record_count`、`updated_at`。平台案件参数可用 `cid`、完整案件编号或完整案件名称；名称重名时必须改用 `cid` 或案件编号。用户给出案件参数时直接精确选择；未给出时列出案件并询问用户，不要默认选择第一个。

### 2. 打开或选择案件

直接执行：

```bash
ges case open <cid|case_number|case_name>
```

单机版会先按案件编号检查是否已经打开：已打开则复用现有 `ges_url` 并自动 `ges init`；未匹配到后台时才启动 `.gec`、发现随机端口并初始化，默认 `cid=1`。平台版精确匹配案件并写入用户级上下文，不启动本地程序。两种模式都会自动初始化；完成后执行：

```bash
ges status
```

平台凭据未设置为环境变量时，可在首次选择时显式传入：

```bash
ges --ges-url <platform_url> --ges-token <认证信息> case open <cid|case_number|case_name>
```

不要在日志或最终回答中输出 token。平台 `storage_host` 会自动发现，无需用户提供。

### 3. 用户没有提供案件

平台版先执行 `ges case ls` 并询问用户选择。单机版如果用户只提供了检材路径，检查 `case ls` 输出：

- 路径完全一致：执行 `ges case open <case_number>` 复用该案件/检材。
- 路径不完全一致：不要根据相似文件名或相似案件名复用旧案件。询问用户是创建新案件导入该检材，还是指定一个已有案件导入。

如果用户明确表示这是新问题、新检材、新镜像或新竞赛，且没有完全一致路径，优先创建新案件或等待用户指定已有案件。

### 4. 上游已经提供 cid 和 ges_url

```bash
ges init --cid <cid> --ges-url <ges_url> --scope user
ges status
```

平台上游提供案件编号或名称时，也可直接初始化：

```bash
ges init --ges-url <platform_url> --ges-token <认证信息> --case <cid|case_number|case_name>
ges status
```

调试端口示例：

```bash
ges init --cid 1 --ges-url http://127.0.0.1:8999
```

### 5. 向已有案件导入检材

只在用户指定了案件编号，或已明确确认要导入当前案件时，才向已有案件导入检材。先打开目标案件并确认上下文：

```bash
ges case open <case_number>
ges status
```

确认上下文后导入检材：

```bash
ges evidence create --evidence-path <path>
```

默认会先按完整 `--evidence-path` 检查当前案件是否已存在该检材；完全一致才不重复添加，并在任务仍在运行时继续等待。未存在时会自动生成检材名称和编号，`autoTask=true`，并阻塞等待解析完成。进度输出是粗粒度的，适合外部 agent 读取。

如果 `evidence create` 报错、超时或输出不确定，不要直接重试。先检查同一路径检材是否已经创建：

```bash
ges evidence ls --path <path>
```

如果输出中存在完全一致路径，且状态为排队、解析中或已添加等待任务生成，说明首次导入已经生效，等待或稍后再查；不要再次导入。只有查不到完全一致路径时，才考虑重试 `evidence create`。

### 6. 没有案件上下文，直接用检材创建新案件

当没有 init 配置、没有显式 `--ges-url`，且用户提供了检材路径时，或 `case ls` 中没有完全一致的镜像路径且用户同意创建新案件时：

```bash
ges evidence create --evidence-path <path> --case-name "刑侦案件" --investigator "调查员"
```

该命令会在 Windows 单机版下启动火眼、创建案件、导入检材、发现端口并自动 `ges init`。可选 `--case-location <dir>` 指定案件保存目录；不传时使用 `~/Documents/GoldenEyes/<case-name>_<case-number>`。

注意：如果显式传了 `--ges-url`，或环境变量已有 `GES_MASTER_URL`/`GES_URL` 但服务不可用，命令会失败，不会自动创建新案件，避免导入到错误案件。

## 常用参数

```bash
# 指定检材编号后 6 位
ges evidence create --evidence-path <path> --number-suffix MP1001

# 确实需要重复添加同一路径检材
ges evidence create --evidence-path <path> --no-dedupe

# 查看当前案件检材和解析状态
ges evidence ls
ges evidence ls --path <path>

# 补充持有人和备注
ges evidence create --evidence-path <path> --person-name "张三" --person-id "320721200203011111" --person-phone "16651847927" --remark "备注" --case-location ""
```

可重复提供 `--person-phone` 和 `--password`。`--case-location` 是选填参数：留空或不传时使用默认位置 `~/Documents/GoldenEyes/<case-name>_<case-number>`；用户指定案件保存目录时，将空字符串替换为目标目录。

## 输出与后续

成功导入会输出检材信息和解析进度，例如：

```text
Evidence created: eid=1 name=VivoBackupFS.zip evidence_number=20260622133811MP1001
Progress: [1/5] 自动识别证据完成
Progress: [100/500] 插件解析中
Evidence analysis completed: [500/500] 解析完成
```

不要自行轮询任务 API。解析完成后切到 `ges-case-analysis`，先运行 `ges status`。

## 排障

- 想导入已有案件：必须先 `ges case open <case_number>` 或 `ges init --cid <cid> --ges-url <ges_url>`。
- 缺少案件编号：先 `ges status`；成功时把当前 `cid/URL` 显式传给 `case ls`，失败时再执行裸 `ges case ls`。
- 复用检材：必须要求用户路径与 `case ls` 中的 `evidences[].镜像路径` 完全一致。
- 新镜像路径：不要复用旧案件或旧上下文，除非用户明确指定要导入哪个已有案件。
- 导入报错或超时：先 `ges evidence ls --path <path>`，看到同路径检材仍在排队/解析中时不要重复导入。
- 上下文不确定：先 `ges status`，失败再按案件编号或 cid/url 初始化。
- 多开火眼：先用 `ges status` 获取当前 `cid/URL`，再显式执行 `ges --cid <cid> --ges-url <ges_url> case ls`；然后用 `ges case open <case_number>` 复用或打开目标案件。默认用户配置同一时间只代表一个生效案件。
