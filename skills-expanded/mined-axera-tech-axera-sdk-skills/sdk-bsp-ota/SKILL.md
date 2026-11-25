---
name: sdk-bsp-ota
description: Axera SoC OTA — SWU 生成与签名、SWUpdate 定制、A/B 升级、首次启动验证、差分升级、失败回退与同步恢复诊断。通过路由适配 M57 Linux/QNX、AX637 Linux。
version: 0.2.0
metadata:
  author: Axera BSP Team
  tags: [axera, bsp, ota, swupdate, ab, m57, ax637, qnx]
  data-classification: public
---

# Axera OTA

## When to use

- 生成、签名或定制 SWU；规划全量、差分、分区或文件升级。
- 排查 SWUpdate 校验、handler、升级状态、首次启动验证和失败恢复问题。
- 开发平台 OTA handler、定制升级钩子，检查部署和错误传播。
- 验证 A/B 双向升级、跨重启 successful、fallback 和可选内容同步。

纯启动链问题使用可用的 `sdk-bsp-boot`；独立 Secure Boot/eFuse 配置使用可用的 `sdk-bsp-secure-boot`。

## Routing

1. args 显式提供 `platform=<id>` 时采用该目标并核对冲突；否则按 [routing.yaml](routing.yaml) 自上而下匹配，第一匹配生效。不要凭目录相似度推断。
2. 命中 `extends` 时，先加载父平台事实，再叠加当前平台；同名条目由子平台覆盖。标注 OS 或平台专属的事实只在该环境使用。
3. 汇报 display 名和检测证据。路由只确定 SDK 家族，OS 与构建 `PLAT` 另行确认；不能从已有产物替用户选择目标。
4. 无匹配按 fallback 询问目标；概念问题可继续解释公共机制，但不猜平台路径或执行修改。
5. 按选中平台的 `reference/<id>/_index.md` 加载所需资料。跨目录复用只能由文档索引声明；平台事实文件不直接引用另一平台的文档。

## Platform and target confirmation

配置或打包前一次确认缺失的板型、SDK 版本、OS、`PLAT`、介质、AB 状态、当前/目标版本及升级范围。用户已有信息不重复询问；缺少 PLAT 时只读枚举候选，等待选择后再修改。概念问答无需收齐构建参数。

## Instructions

1. **确定环境和操作范围**：完成路由与目标确认。修改前核实主机 OS、工具链和现有构建入口，记录源码基线。
2. **识别问题层次**：区分包生成/签名、SWUpdate core、平台 handler、OTA 阶段脚本、AB 选槽和内容复制。源码入口见选中平台的“源码位置”。
3. **收集最小证据**：按平台“信息收集清单”获取相关输入，至少交叉核对两类状态或日志；区分已证实原因与待验证假设。
4. **核对升级包契约**：检查版本、布局、签名、artifact 和差分基线，确认 A/B 描述对称且目标为 inactive 槽。构建命令与定制参数按平台“构建配置与验证”。
5. **检查写入前保护**：所有目标擦写和复制前保护目标槽，确保错误可中止；核对 core 实际调度，不能只凭模板排列认定掉电安全。
6. **保持状态机边界**：安装完成只标 active；首次启动功能验证通过后才 successful。BCB OTA 阶段、AB metadata 和实际启动槽分别读取，具体字段以平台“核心知识”为准。
7. **定位失败与恢复**：按平台“常见问题排查表”检查校验、写入、首次验证与 fallback；把内容复制失败和 AB 选槽问题分开，保留旧 successful 槽。
8. **实施和验证**：作最小修改，运行目标 SDK 已有的语法、构建或测试入口；升级授权明确时才操作板端，并记录双向升级、跨重启验证和失败恢复证据。
9. **交付结果**：报告目标环境、修改/结论、证据与未验证项。按选中平台 eval 矩阵判定；离线检查、构建、行为评测和实板结果分别记录。

## Safety

- 验签失败、布局冲突、差分基线不明或唯一成功槽可能被覆盖时停止写入，说明具体阻碍；不以关闭校验作为修复。
- 写完不等于升级成功；缺少业务验证脚本而默认通过不能代表业务已验证。
- 同步会改写旧槽内容，只能在新槽验证成功后进行；恢复时先确定失败目标，避免禁用救援中的旧成功槽。
- 私钥不进入日志或交付物。文件升级和共享分区的掉电安全需单独核实，不能因存在 A/B 就作通用保证。

## 平台矩阵

| 平台 id | 说明 | 平台事实 / 文档索引 |
|---|---|---|
| `m57` | 公共 OTA 架构、M57 Linux/QNX 环境差异 | [platforms/m57.md](platforms/m57.md)、[reference/m57/_index.md](reference/m57/_index.md) |
| `ax637` | AX637/AX637R Linux 差异；extends m57，排除 QNX 专属事实 | [platforms/ax637.md](platforms/ax637.md)、[reference/ax637/_index.md](reference/ax637/_index.md) |

新增平台：补充 routing 条目、平台事实、reference 索引与分平台 eval。六类知识章节在平台层维护，主文件保持通用流程。资料来源见 [reference/sources.md](reference/sources.md)。
