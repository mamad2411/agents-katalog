---
name: sdk-bsp-secure-boot
description: Axera SoC Secure Boot — 签名/加密启动链、eFuse PKH/Root Key/FEK 规划、FIT 镜像生产、dm-verity、密钥替换、各阶段失败诊断。通过路由自动适配平台（m57、ax637）。
metadata:
  author: Axera BSP Team
  tags: [axera, secure-boot, rsa, aes, fit, dm-verity, efuse, hsm]
  data-classification: public
---

# Axera Secure Boot

## When to use

- 使能或验证 `SECURE_BOOT`、固件加密、rootfs dm-verity
- 生成/替换签名或加密镜像；替换 RSA 密钥并同步 U-Boot DTB 公钥
- 规划 eFuse Root Key / PKH / FEK 写入
- 诊断签名、解密、FIT 或 dm-verity 启动失败

不用于与安全启动无关的 eFuse 编程、TEE 应用开发或普通镜像构建。

## Resource paths

`<SKILL_ROOT>` 表示本技能 `SKILL.md` 所在目录。直接使用源码技能时，从加载结果的 `Base directory` 或 `SKILL.md` 绝对路径取得根目录；通过本包安装脚本安装时，此记号会展开为工作区内的部署路径，直接使用展开后的路径。

- 路由表：`<SKILL_ROOT>/routing.yaml`。
- 平台文档：`<SKILL_ROOT>/platforms/<id>.md`，包括 `extends` 指定的父平台。
- 参考文档：先读取 `<SKILL_ROOT>/reference/<id>/_index.md`，再按其路由读取文档；表内资源路径相对同一技能根目录。

读取和搜索时保持完整技能路径；搜索前先确认目录存在。SDK 标志目录、源码、`config.mk` 和用户输出文件相对工作区解析。平台摘要已提供所需事实时直接据此答复，仅在尚缺具体事实时继续搜索手册。

## Routing

1. 若 args 传入 `platform=<id>`，直接使用；否则按 `routing.yaml` 从上到下匹配，具体 board/SDK 条目必须排在通用架构条目前面。不得用 `mach-axera/m57`、`m57-keys.dtsi`、`SafetyIsland/sbl` 等 M57/AX637 共用路径区分平台；优先使用 SDK 特有的 `mcal` 或 RT-Thread（`SafetyIsland/rt-thread`、`configs_ax637*`）标志。
2. 命中带 `extends` 的平台，先加载父平台的 `<SKILL_ROOT>/platforms/<parent>.md`，再叠加当前平台，同名条目由当前平台覆盖。
3. 以一句话汇报识别到的平台（display 名 + 命中路径/来源），便于用户纠正误判。后续 `PLAT` 示例、命令和路径均限定在该 SDK 家族；尚未确认具体目标时使用 `<PLAT>` 占位符。
4. 无匹配时执行 `fallback`（当前为 ask），只汇报未识别平台并询问板型/SDK。用户要求文件答复时先写入待确认问题，再给出一句完成回复结束本轮，待平台确认后再加载平台文档。
5. 按 Resource paths 的根目录读取选中平台的 `<SKILL_ROOT>/platforms/<id>.md`；仅在具体步骤需要时，才打开其参考文档。`reference/<id>/_index.md` 是**文档路由表**，声明该平台文档的实际路径（哪些本地维护、哪些复用其他平台目录）——读取前先查该表，不要假设文档就在本平台目录下。禁止跨平台引用路径或日志关键字。

## Platform and target confirmation

- 用户未显式指定 `PLAT`/具体平台时，只能识别 SDK 家族，不能自行选择 `demo_only_nand`、`*_emmc` 或其他具体目标，也不能修改任何 `config.mk`。先询问一次并等待回复。
- “帮我配置 Secure Boot”这类请求在开始修改前必须一次收集：板型（AX637/AX637R/M57）、`PLAT`/启动介质（eMMC/NAND）、eFuse（未烧写/已启用）、RSA（2048/3072）、固件加密（是/否）、dm-verity（是/否）。如果用户已提供其中部分，只询问缺失项；仍不得替用户补默认值。缺少参数时，输出平台识别结果和一次汇总的待确认项即结束本轮，待目标确认后再展开配置、密钥及烧写步骤。
- 只有在目标确认后才读取并修改对应 `build/platforms/.../<PLAT>/config.mk`。仅回答信任链、密钥或日志问题时，不要把“识别 SDK”误当成“选择 PLAT”。
- 只读咨询只回答本题所需的要点与命令，参考文档按问题查阅；用户指定输出文件时，先用文件存在性检查（例如 `if test -f out/response.md; then echo exists; else echo new; fi`）判断是更新还是新建：已有文件才先 `read`，新文件直接 `write`。答复内容在写入前核对完毕；写入后直接以一句“已写入 `<输出路径>`”作为最终文本回复结束本轮。
- 查询 SDK 源码前，先通过工作区目录列表或 `test -d <目录>` 确认 `boot/`、`tools/` 等查找根目录存在，再对存在的目录使用 `glob`/`grep`。精简 SDK 缺少源码时，依据选中平台文档给出建议并注明未核验的实现，完成本次咨询。RSA 密钥、公钥同步、构建命令及 AES/eFuse 工具入口均见 `<SKILL_ROOT>/platforms/m57.md` 对应章节；仅说明操作方法时先查该摘要，仅为解决尚缺的具体事实才展开参考手册或源码。

## Instructions

1. **确认安全状态**：板型、SDK 版本、启动介质、eFuse 生命周期、RSA 位数、是否加密、是否 dm-verity。在签名链完整跑通前保留非量产恢复路径。

2. **理解信任链**：各阶段划分与校验机制见路由后加载的 `<SKILL_ROOT>/platforms/<id>.md` §信任链。任一阶段失败，后续不得继续。

3. **离线准备密钥**：在受控 Linux 服务器上生成传统 PEM 格式 RSA 密钥；公钥必须是 PKCS#1 格式
   （`openssl rsa -in private.pem -pubout -RSAPublicKey_out -out public.pem`），不能用默认 SPKI 格式；
   需加密固件时用 `openssl rand -hex 32 > tools/imgsign/aes-256.key` 准备 32-byte AES Key。
   替换路径见 `<SKILL_ROOT>/platforms/<id>.md`。私钥与 AES 材料永不入源码/日志/工单。

4. **谨慎规划 eFuse**：Root Key 先于依赖项写入且写后不可读回；按选定公钥写入 PKH；FEK 仅加密启动时需要。
   所有 eFuse 写入视为不可逆，先在测试样片验证再量产。烧写密钥用 `sample_efuse_key`，烧写 bondoption
   用 `sample_efuse`（`-w <blk> <data>`）；`sample_efuse_key` 源码 `EFUSE_WRITE_ENABLE` 为 0 时只打印
   不写入，需改 1 重新编译。工具分工与烧写顺序见 `<SKILL_ROOT>/platforms/m57.md`。

5. **配置构建**：目标为 `ax637_demo_only_emmc` 时，先执行 `<SKILL_ROOT>/platforms/ax637.md` 的 HSM 分区检查并确认固件打包，再配置签名。在用户确认的 `PLAT` 对应 `build/platforms/<vendor>/<platform>/config.mk` 中设置关键变量。组合约束、产物命名、Download/AXDL 和 eFuse 规则见 `<SKILL_ROOT>/platforms/m57.md`；board 差异见 `<SKILL_ROOT>/platforms/<id>.md`。

6. **构建各组件**：SBL 用 `build/scripts/imgsign` 工具；SPL/RTOS 走 image-signing；ATF/OP-TEE/U-Boot 用 U-Boot FIT（SHA-256 + RSA 签名，加密时加 AES-256 cipher 节点）。

7. **替换验签公钥**：SPL/U-Boot 从自身 DTB 的公钥验签而不读 eFuse PKH。替换 PEM 后必须用 SDK 工具抽取参数写入 DTS 节点，并重新构建 SPL/U-Boot。公钥、PKH、私钥、镜像必须属于同一版本集合。

8. **构建 dm-verity**：`veritysetup` 生成 hash tree/root hash 后签名。U-Boot 校验 root hash，Linux 按块校验——U-Boot 通过不等于全 rootfs 已校验。只读 EXT4/SQUASH 可用。

9. **分阶段使能与诊断**：先跑软件签名链（eFuse 未使能），逐级验证后再进 eFuse 编程。失败时定位以最早出现的错误为准；日志关键字与故障字段布局见 `<SKILL_ROOT>/platforms/<id>.md` §故障定位。

## Safety

- eFuse 编程与密钥替换可能永久砖化设备；不可逆写入前显式再次确认。
- 永不提交私钥、AES Key、FEK、Root Key 或未脱敏密钥参数。
- 未验证 Root Key/FEK 前不启用 `ENABLE_CIPHER`；rootfs 可写时不启用 dm-verity。
- PKH、DTB 公钥、签名私钥、镜像必须构成一致的版本化集合。

## 平台矩阵

| 平台 id | 说明 | 参考文档 |
|---|---|---|
| `m57` | M57 SDK/架构公共层（BootROM/SBL/FIT/config、产物、Download、eFuse、fault.c） | `<SKILL_ROOT>/platforms/m57.md`, `reference/m57/` |
| `ax637` | AX637/AX637R SDK board 差异（RTT、PLAT 命名、board 路径；extends m57） | `<SKILL_ROOT>/platforms/ax637.md`, `reference/ax637/` |

新增平台：`routing.yaml` + `<SKILL_ROOT>/platforms/<id>.md` + `reference/<id>/` + evals 矩阵条目。
