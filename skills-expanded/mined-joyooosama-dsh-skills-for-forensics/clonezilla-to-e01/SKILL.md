---
name: clonezilla-to-e01
description: 把 Clonezilla 备份镜像文件夹内的所有磁盘转换为 E01 取证镜像(调用火眼 BootMagix 后端完成转换)。输入 Clonezilla 镜像文件夹路径,自动查询其中包含的全部磁盘并串行逐一转换为 E01 格式输出,实时输出 NDJSON 进度(标注当前盘序号/盘名/进度);另提供 info 子命令查询镜像内各磁盘名与大小。需要 BootMagix 已在本机处于运行状态。
metadata:
  version: 4.7.1.2882
---

# Clonezilla 转 E01 Skill

## 何时使用

当用户希望把 Clonezilla 备份得到的镜像文件夹转成取证常用的 E01 格式、或描述类似下面这些需求时使用本 skill:

- "把这个 Clonezilla 镜像转成 E01"
- "D:/2025-02-04-13-img 是 Clonezilla 备份的,帮我转成 E01"
- "调证拿到一个 Clonezilla 镜像,要转成 E01 给取证工具打开"

镜像内若包含多块磁盘,本 skill 会**自动串行逐一转换**,无需用户指定 `--disk`。

> 如果目标是把镜像"启动起来"做仿真,请改用 `create-vm` skill。本 skill 只做格式转换。

## 前置条件

1. **操作系统**:Windows
2. **BootMagix 已运行**:用户已经启动 BootMagix(以管理员权限),master 进程已就绪
3. **CLI 已就位**:`bootmagix-cli.exe` 与本文件在**同级目录**
4. **Clonezilla 镜像文件夹**:包含 `disk`、`<盘名>-pt.sf`、`<盘名>-ptcl-img.*` 等 Clonezilla 标准文件的目录

## 调用方式

通过 Bash 工具执行:

```
.claude/skills/clonezilla-to-e01/bootmagix-cli.exe convert --src "<Clonezilla镜像文件夹绝对路径>"
```

参数:

- `--src <dir>` **必填**:Clonezilla 镜像文件夹路径
- `--dest <dir>` 输出目录;留空则默认为 `--src` 的父目录。每块盘生成一个文件:`<src目录名>-<disk>.e01`

> master 端口由 skill 自动发现,无需手动指定。
> 镜像内所有磁盘自动串行处理,无需指定 `--disk`。

不确定镜像里有几块盘时,先用 `info` 子命令查询:

```
.claude/skills/clonezilla-to-e01/bootmagix-cli.exe info --src "<Clonezilla镜像文件夹绝对路径>"
```

## 多盘处理与进度

`convert` 会先查询镜像内全部磁盘(按盘名字典序),然后**一块一块串行转换**。每块盘的进度独立从 0 走到 100。NDJSON 进度事件会带上当前盘的上下文(`src`/`disk`/`index`/`total`),见下表。

## 输出格式

CLI 把进度通过 stdout 写成 **NDJSON 行流**,每行一条 JSON 事件。**必须按行解析**。字段:

| 字段 | 说明 |
|---|---|
| `ts` | ISO8601 时间戳 |
| `type` | `stage`(阶段开始) / `progress`(当前盘进度 0-100) / `info`(信息) / `warn`(非致命警告) / `error`(致命) / `result`(终态) |
| `stage` | 阶段名,见下表 |
| `progress` | 0-100,仅 `type=progress` 有;表示**当前盘**的转换进度 |
| `message` | 中文提示 |
| `code` | `type=error` 时的错误码 |
| `src` | 当前 `--src` 路径(progress / result 均有) |
| `disk` | 当前盘名(如 `sda`) |
| `index` | 当前盘序号(1-based) |
| `total` | 盘总数 |
| `results` | `type=result`(convert)时各盘结果数组,每项含 `disk` / `dest` / `sizeBytes` / `status`(`success`/`failed`) / `error` |
| `disks` | `type=result`(info)时磁盘列表,每项含 `name` / `sizeBytes` / `sizeHuman` |

### 阶段(stage)

依次出现:

```
discovering          发现 master 端口
connecting           连接 master HTTP
auth                 登录
querying             查询镜像内磁盘信息、确定输出目录
converting           转换中(每块盘开始时各 emit 一行 stage,带 [index/total] disk)
done                 全部结束
```

`info` 子命令只走 `discovering → connecting → auth → querying`,无 `converting`。

### 错误码(error.code)

- `discovery_failed` — 无法连接 BootMagix 服务器,提示用户先启动 BootMagix
- `auth_failed` — 登录失败
- `info_failed` — 查询磁盘信息失败(路径不是有效 Clonezilla 镜像 / 文件缺失)
- `disk_not_found` — 镜像内无有效磁盘
- `dest_invalid` — 输出目录不存在或不可写
- `convert_failed` — 某块盘转换失败;`message` 含 `[index/total] disk` 与详情,该盘在 `results` 中标 `failed`,**继续转换后续盘**

### 退出码

- `0` 全部磁盘转换成功
- `1` 有磁盘转换失败(或查询失败);`results` 数组详列每盘状态
- `2` 参数错误(`--src` 缺失 / 文件夹不存在 / 输出目录无效)
- `3` master 未运行或无法连接

## NDJSON → 中文进度对照

每收到一行 NDJSON,**立刻**转成对用户友好的中文进度,不要等全部跑完。示例:

| NDJSON | 给用户的回复 |
|---|---|
| `{"type":"stage","stage":"discovering",...}` | "正在连接火眼后端..." |
| `{"type":"info","stage":"querying","message":"镜像内发现 2 块磁盘: sda, sdb,将依次转换"}` | "镜像内有 2 块磁盘:sda、sdb,将依次转换" |
| `{"type":"stage","stage":"converting","message":"[1/2] 开始转换磁盘 sda → ..."}` | "开始转换第 1/2 块:sda" |
| `{"type":"progress","stage":"converting","progress":42,"src":"...","disk":"sda","index":1,"total":2}` | "sda 转换中 42%(第 1/2 块)" |
| `{"type":"info","stage":"converting","message":"[1/2] 磁盘 sda 转换完成"}` | "sda 完成(1/2)" |
| `{"type":"stage","stage":"converting","message":"[2/2] 开始转换磁盘 sdb → ..."}` | "开始转换第 2/2 块:sdb" |
| `{"type":"progress","stage":"converting","progress":80,"disk":"sdb","index":2,"total":2}` | "sdb 转换中 80%(第 2/2 块)" |
| `{"type":"result","status":"success","src":"...","results":[{"disk":"sda","dest":"D:\\...-sda.e01","status":"success"},{"disk":"sdb","dest":"D:\\...-sdb.e01","status":"success"}]}` | "全部完成:sda → ...-sda.e01,sdb → ...-sdb.e01" |
| `{"type":"error","stage":"converting","code":"convert_failed","message":"[1/2] 磁盘 sda 转换失败: ..."}` | "sda 转换失败(第 1/2 块),继续处理后续盘;最终结果见 result" |

## 示例对话

### 多盘串行

> **用户**:把 `D:\2025-02-04-13-img` 这个 Clonezilla 镜像转成 E01

> **Claude**:好的,正在通过 BootMagix 转换...
>
> *(调用 `bootmagix-cli.exe convert --src D:\2025-02-04-13-img`,边读 NDJSON 边汇报)*
>
> - 连接火眼后端 ✓
> - 镜像内有 2 块磁盘:sda(120 GiB)、sdb(500 GiB),将依次转换
> - [1/2] sda 转换中 → 30% → 70% → 100% ✓
> - [2/2] sdb 转换中 → 20% → 60% → 100% ✓
>
> 全部完成:
> - sda → `D:\2025-02-04-13-img-sda.e01`
> - sdb → `D:\2025-02-04-13-img-sdb.e01`
>
> 可用 FTK Imager / ewfverify 打开校验。

### 先查盘

> **用户**:这个 Clonezilla 镜像我不确定有几块盘

> **Claude**:
>
> *(调用 `info --src D:\case\img`)*
>
> 镜像内包含 2 块磁盘:
>
> | 盘名 | 大小 |
> |---|---|
> | sda | 120.00 GiB |
> | sdb | 500.00 GiB |
>
> 直接 `convert` 即可,两块盘会自动依次转换。

## 范围之外(本 skill 暂不处理)

- 直接转成 dd / vmdk / vhdx 等其他格式(后端目前只提供 E01 输出)
- BitLocker 解密、RAID 重组(需先在 BootMagix UI 中处理)
- 并行转换多盘(当前为串行,保证进度输出清晰)
