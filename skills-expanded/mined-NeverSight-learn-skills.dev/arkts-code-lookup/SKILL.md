---
name: arkts-code-lookup
description: 根据技术方案、应用需求或安卓代码片段，查找并列出所需的 HarmonyOS ArkTS public API。当用户描述想要实现的功能、需要了解该用哪些 API/Kit/接口时触发，例如："我需要什么API实现…"、"做一个拍照功能需要哪些接口"、"这个需求用哪个Kit"、"技术方案中涉及哪些HarmonyOS能力"、"查一下相机相关的API"、"我要接入地图有哪些接口可以用"。当用户描述应用需求但未明确要求写代码时也应触发，例如："我要做一个IM应用需要音视频通话"——此时应识别所有相关API。当用户携带安卓（Java/Kotlin）代码片段询问 HarmonyOS 对应 API 时也应触发，例如："这段安卓代码在鸿蒙上用什么API实现"、"帮我把这个 Android 功能迁移到鸿蒙，需要哪些接口"——此时应解析安卓代码并映射到对应的 HarmonyOS API。触发关键词：需要哪些API、用什么接口实现、查API、涉及哪些能力、哪些组件、技术方案、API文档、文档路径、鸿蒙迁移、Android迁移、安卓代码，与 ArkTS/HarmonyOS/鸿蒙/ability/UIAbility/ArkUI 或任意 Kit 名称组合出现。当用户明确要求编写或生成 .ets 代码文件时，不触发本 skill。
---

# ArkTS API 知识库查询

根据用户描述的技术方案、应用需求或安卓代码片段，从官方 API 参考文档中精准找出所需的 public API，并输出每个 API 的文档绝对路径和官方 URL。

## 参考文档位置

API 参考文档随本 skill 一起打包，位于：
```
arkts_code_lookup_references/          # 纯文档目录
├── harmonyos_references/
│   ├── 应用框架/   # 应用框架：Ability Kit、ArkUI 等（681 篇）
│   ├── 系统/       # 系统：网络、安全、文件、设备（201 篇）
│   ├── 媒体/       # 媒体：相机、音频、视频、图片（133 篇）
│   ├── 图形/       # 图形：Canvas、2D/3D 渲染（53 篇）
│   ├── 应用服务/   # 应用服务：推送、地图、账号、IAP 等（327 篇）
│   └── AI/         # AI Kits：CV、NLP、语音、ML（27 篇）
├── learning-arkts/
│   ├── ArkTS语言介绍.md        # 语言概述
│   └── ArkTS编程规范.md        # 编码规范
└── app-permissions/
    ├── permissions_list/
    │   └── *.md                # 应用权限列表（权限名 / 授权方式 / 级别 / 说明）
    └── requesting_permission/
        └── *.md                # 申请应用权限（运行时申请流程 / user_grant 处理）

arkts_code_lookup_indexes/             # 索引文件 + 构建脚本
├── INDEX_TOC.md          # ← 总目录（TOC = Table of Contents，~4 KB）：6 大分类 × Kit 列表，指向各分类索引
├── INDEX_AI.md           # ← AI 分类索引（27 篇）
├── INDEX_图形.md         # ← 图形分类索引（53 篇）
├── INDEX_媒体.md         # ← 媒体分类索引（133 篇）
├── INDEX_应用服务.md         # ← 应用服务分类索引（327 篇）
├── INDEX_应用框架.md         # ← 应用框架完整索引（681 篇，fallback 用）
├── INDEX_应用框架_TOC.md     # ← 应用框架 Kit 二级 TOC（14 个 Kit，约 3KB）
├── INDEX_应用框架_{Kit}.md   # ← 各 Kit 子索引，共 14 个：
│   # ArkUI(356) / AbilityKit(118) / ArkWeb(67) / ArkTS(48) / ArkData(25)
│   # UIDesignKit(14) / CoreFileKit(13) / FormKit(9) / IMEKit(8)
│   # LocalizationKit(7) / BackgroundTasksKit(6) / AccessibilityKit(5)
│   # DataAugmentationKit(4) / IPCKit(1)
├── INDEX_系统.md             # ← 系统分类索引（201 篇）
├── INDEX.md              # ← 完整索引（备用，2014 行）
├── VERSION_INDEX.json    # ← API 版本索引：文件路径 → 模块最低版本 + 各接口版本
├── PERMISSION_INDEX.md   # ← 权限类型速查索引（A~F 六类，含处理流程）
├── build_index.py
├── build_version_index.py
└── build_permission_index.py
```

各分类文件结构：
```
arkts_code_lookup_references/harmonyos_references/{category}/{Kit Name}/{ArkTS API | ArkTS组件 | REST API}/{APIName}.md
```

每个 `.md` 文件包含：源 URL、import 语句、interface/class/enum 定义，以及每个方法的完整签名。

**skill_root（本地文档绝对路径前缀）**：当前 SKILL.md 所在目录的绝对路径，即运行时的 skill 根目录。在输出文档路径时，将 INDEX 文件中的相对路径拼接到 skill_root 后面，形成完整绝对路径：
```
{skill_root}/arkts_code_lookup_references/harmonyos_references/{relative_path}
```

### REST API 使用原则

部分 Kit 目录下包含 `REST API/` 子目录（涉及 Account Kit、Push Kit、IAP Kit、Payment Kit、AppGallery Kit、Game Service Kit、Intents Kit、Device Security Kit）。

这些文档描述的是**服务端 → 华为云**的 HTTP 接口，由应用后端调用，**不属于 ArkTS 客户端 API 范畴**。

- **默认不输出**：查找 ArkTS 客户端 API 时，不引用 REST API 文档
- **仅在用户明确要求时参考**：如用户明确提到"服务端"、"后端对接"、"服务器调用华为接口"等场景，才列出对应 REST API 文档路径，并清楚标注"以下为服务端 REST API，非 ArkTS 客户端 API"
- **版本约束不适用**：REST API 文档无 HarmonyOS API version 标注

## 工作流程

请按以下步骤依序执行。

### Step 0：确认目标 API 版本

**在继续之前，始终先询问用户的目标 API 版本**，除非用户已经指定。

```
"请问您的目标 API version 是多少？（例如：API 12）"
```

目标 API 版本（一个整数，例如 `12`）是硬性约束：
- **严格禁止**：列出任何 `**起始版本：**` 超出目标版本的 API 或接口
- 若某个必需 API 仅在更高版本才可用，需清楚说明，并建议替代方案或升级版本

确认目标版本后，在后续所有步骤中均以此版本为约束。

---

### 输入类型判断

完成 Step 0 版本确认后，判断用户输入类型，据此选择对应的 Step 1 分支：

| 类型 | 判断标准 | 执行分支 |
|------|---------|---------|
| **类型 A — 自然语言需求** | 用户以自然语言描述功能或技术方案，无代码块 | 执行 Step 1-A |
| **类型 B — 安卓代码** | 用户提供含 Java/Kotlin 代码（存在 `android.`/`androidx.` 包名、安卓特有类名如 `Activity`/`Fragment`/`RecyclerView` 等，或代码块语言标记为 `java`/`kotlin`） | 执行 Step 1-B |

两种类型完成各自 Step 1 后，**在 Step 2 和 Step 3 合流**，使用相同的 API 查找与输出流程。

---

### Step 1-A：分析需求（类型 A 专用）

明确用户的实际需求，拆解如下：
- 涉及哪些 HarmonyOS 能力？（UI、网络、媒体、AI、推送等）
- 数据流入和流出分别是什么？
- 是否有约束条件：平台版本、权限要求？

若需求表述不清，先提一个澄清问题再继续。

---

### Step 1-B：安卓代码分析（类型 B 专用）

依序完成以下三步，将安卓代码转换为 HarmonyOS 能力列表，作为 Step 2 的输入。

#### 1. 提取安卓 API 列表

扫描用户提供的代码，收集：
- 所有 `import` 语句中的包名与类名
- 代码中直接使用的安卓类（如 `CameraManager`、`RecyclerView`、`LocationManager`）
- 关键方法调用（如 `.openCamera()`、`.getLastLocation()`）

#### 2. 套用映射速查表

对上一步提取的每个安卓 API，读取并参照映射表文件，找到对应的 HarmonyOS Kit 与能力：

```
Android_HarmonyOS_API_Mapping.md
```

该文件覆盖约 86 个映射条目，按以下 12 个能力域分组：
一、UI 组件 / 二、布局与导航 / 三、网络通信 / 四、数据存储 / 五、媒体能力 / 六、系统服务与硬件 / 七、后台任务与生命周期 / 八、通知与推送 / 九、广播与系统事件 / 十、权限与安全 / 十一、WebView 与 Web 能力 / 十二、调试与诊断

每条映射含**复杂度评级**（🟢 低 / 🟡 中 / 🔴 高）与完整的 HarmonyOS 模块路径（如 `@ohos.net.http`），在步骤 3 标记无法映射项时可直接引用。

> **映射表未覆盖的 API**：若代码中存在映射表未列出的安卓 API，在下一步标记为「待评估」。

#### 3. 标记无法映射项，生成能力列表

- **可映射**：汇总所有映射结果，形成 HarmonyOS 能力列表，直接进入 Step 2 查找对应 API
- **无法映射 / 存在差异**（⚠️ 标记）：在 Step 3 输出的迁移对照表中单独列出，注明原因：
  - 「HarmonyOS 暂无直接对应 API」
  - 「需拆分为多个 API 实现」
  - 「行为差异较大，建议评估替代方案」

---

### Step 2：查找相关 API 文档（含版本预筛选）

**选择查找策略**：

**情况 A - 已知 API 名称**（快速路径）：
- 直接搜索 `INDEX.md` 或 `VERSION_INDEX.json` 中的关键词
- 适合：明确知道要用什么 API（如 cameraPicker、http、router）
- 示例：`grep "cameraPicker" arkts_code_lookup_indexes/INDEX.md` 或在 `arkts_code_lookup_indexes/VERSION_INDEX.json` 中搜索字段名

**情况 B - 不确定用哪个 API**（分层路径）：
- 按 Phase 1/2 流程渐进查找，见下文
- 适合：探索性查找、了解某个 Kit 有哪些能力、不确定 API 名称时

---

**应用框架使用三阶段查找，其他分类使用两阶段——不要加载完整的 2014 行索引，也不要盲目搜索 1422 个文件。**

#### Phase 1 — 加载总目录，确认分类

读取 `arkts_code_lookup_indexes/INDEX_TOC.md`（约 4 KB）。该文件列出了全部 6 大分类及其下的 Kit 名称。通过扫描确定所需 API 属于哪个分类（从而确定应加载哪个索引文件）。

| 用途 | 加载文件 |
|------|----------|
| AI：语音、视觉、NLP、昇思推理等 | `arkts_code_lookup_indexes/INDEX_AI.md` |
| 图形：2D/3D绘制、AR、图形加速 | `arkts_code_lookup_indexes/INDEX_图形.md` |
| 媒体：相机、音频、视频、图片、扫码 | `arkts_code_lookup_indexes/INDEX_媒体.md` |
| 应用服务：推送、地图、支付、账号、广告、通知等 | `arkts_code_lookup_indexes/INDEX_应用服务.md` |
| 应用框架：ArkUI、Ability Kit、ArkData、ArkWeb、文件、卡片等 | → 见 Phase 2a |
| 系统：网络、蓝牙、传感器、安全、日志、窗口等 | `arkts_code_lookup_indexes/INDEX_系统.md` |

#### Phase 2 — 加载分类索引，获取精确文件路径

**非应用框架分类**：直接读取对应的 `arkts_code_lookup_indexes/INDEX_{分类}.md`。该文件列出了该分类下所有 API 文档的相对路径，从中定位所需 API 的精确路径。

**应用框架（因体量大需额外一步——14 个 Kit 共 681 篇文档）：**

- **Phase 2a**：读取 `arkts_code_lookup_indexes/INDEX_应用框架_TOC.md`（约 4 KB），该文件列出了 14 个 Kit 及其快速匹配关键词，判断 API 属于哪个 Kit。
  > 快捷路径：若关键词明确匹配（例如 `@Component` / `Text` / `Button` / `Navigation` → ArkUI；`UIAbility` / `Want` / `startAbility` → AbilityKit；`WebviewController` → ArkWeb；`relationalStore` / `preferences` → ArkData；`taskpool` / `worker` / `@arkts` → ArkTS），可直接跳过本步骤，直接到 Kit 文件。
- **Phase 2b**：读取 `arkts_code_lookup_indexes/INDEX_应用框架_{Kit}.md`（例如 `arkts_code_lookup_indexes/INDEX_应用框架_ArkUI.md`），定位精确文件路径。

若两个阶段均未找到匹配项，回退到完整的 `arkts_code_lookup_indexes/INDEX_应用框架.md`（681 篇文档）。

**然后，读取完整文档之前，先用 grep 查 VERSION_INDEX.json 进行版本预筛选。**

> ⚠️ **严禁用 Read 工具读取整个 VERSION_INDEX.json**——该文件约 532 KB / 14587 行，全量加载会严重消耗 context window。务必用 Grep 工具按文件路径关键词查询，每次只取所需条目。

查询方式（以 `cameraPicker.md` 为例）：
```bash
# 用 Grep 工具搜索候选文件的路径关键词
grep "cameraPicker.md" arkts_code_lookup_indexes/VERSION_INDEX.json
# 若结果跨多行，加 -A 参数获取后续字段
grep -A 6 "cameraPicker.md" arkts_code_lookup_indexes/VERSION_INDEX.json
```

`VERSION_INDEX.json` 的结构：每条记录映射 `文件相对路径 → 模块最低版本 + 各接口版本差异`：

```json
// VERSION_INDEX.json 结构
{
  "files": {
    "harmonyos_references/媒体/Camera Kit（相机服务）/ArkTS API/cameraPicker.md": {
      "v": 11,                                    // ← 模块最低版本
      "permissions": ["ohos.permission.CAMERA"],  // ← 该文档中出现的所有 ohos.permission.* 权限名
      "api_version_overrides": {                  // ← 仅列出与模块版本不同的接口
        "PickerProfile": 12
      }
    }
  }
}
```

**版本预筛选规则**（目标版本 = T）：
1. 用 Grep 工具在 `VERSION_INDEX.json` 中搜索候选文件路径，获取 `"v"` 和 `"permissions"` 等字段
2. 若 `"v" > T` → **跳过整个模块**（该文件版本过高）
3. 若 `"v" <= T` → 读取文件，但**排除 `"api_version_overrides"` 中版本 > T 的接口**
4. 若文件为 `"v": null` → 读取文档并手动检查 `**起始版本：**` 注解

```
# 典型查找流程（非应用框架，例如 媒体）：
# 1. 读取 arkts_code_lookup_indexes/INDEX_TOC.md → 确认分类（媒体）
# 2. 读取 arkts_code_lookup_indexes/INDEX_媒体.md → 找到候选文件路径
# 3. grep 候选路径关键词 → arkts_code_lookup_indexes/VERSION_INDEX.json → 确认模块版本 <= T，记录需排除的接口
# 4. 读取 arkts_code_lookup_references/<相对路径> → 仅提取可用接口

# 典型查找流程（应用框架，例如 ArkUI Button 组件）：
# 1. 读取 arkts_code_lookup_indexes/INDEX_TOC.md → 确认分类（应用框架）
# 2a. 读取 arkts_code_lookup_indexes/INDEX_应用框架_TOC.md → 确认 Kit（ArkUI——通过关键词 "Button" 匹配）
#     或若关键词明确指向某 Kit，直接跳过此步骤（参见快捷路径规则）
# 2b. 读取 arkts_code_lookup_indexes/INDEX_应用框架_ArkUI.md → 找到候选文件路径
# 3. grep 候选路径关键词 → arkts_code_lookup_indexes/VERSION_INDEX.json → 确认模块版本 <= T
# 4. 读取 arkts_code_lookup_references/<相对路径> → 仅提取可用接口
```

若分类索引中未找到匹配项，回退到关键词搜索：

```bash
grep -r "关键词" arkts_code_lookup_indexes/INDEX.md
# 或在实际文档中搜索：
grep -rl "keyword" arkts_code_lookup_references/harmonyos_references/ --include="*.md"
```

务必读取所有计划引用的 API 文件——不要凭猜测补充方法签名或接口结构。文档中包含每个成员的精确参数类型、返回类型、所需权限及 `**起始版本：**` 注解。

---

### Step 3：输出 API 清单

针对 Step 2 中找到的每个相关 API 文档，提取以下字段并输出结构化清单：

| 字段 | 来源 |
|-----|-----|
| API / 组件名 | 文档文件名 / 文档内 class/interface/function 名 |
| 所属 Kit | 文件路径中的 Kit 目录名 |
| 起始版本 | VERSION_INDEX.json 的 `"v"` 字段，或文档内 `**起始版本：**` |
| Import 语句 | 文档内 import 代码块 |
| 本地文档绝对路径 | `{skill_root}/arkts_code_lookup_references/` + INDEX 文件中的相对路径 |
| 官方文档 URL | 每个 .md 文件头部的 `source:` 字段 |
| 所需权限 | VERSION_INDEX.json 的 `"permissions"` 字段，或文档内 `**需要权限：**` |
| 在本需求中的用途 | 根据需求分析推断 |

**输出格式模板**（每次查询都使用此固定格式）：

````markdown
## 所需 ArkTS Public API 清单

### 需求分析
[1-3 句话说明涉及哪些 HarmonyOS 能力，以及为何选择这些 API]

### API 汇总表

| # | API / 组件 | Kit | 起始版本 | 所需权限 | 在本需求中的用途 |
|---|-----------|-----|---------|---------|----------------|
| 1 | `cameraPicker.pick()` | Camera Kit | API 11 ✅ | CAMERA | 调起系统相机 Picker UI 完成拍照 |
| 2 | `Image` 组件 | ArkUI Kit | API 7 ✅ | 无 | 在页面上显示拍摄的图片 |

> ✅ = 版本符合目标 API T；❌ = 超出目标版本，需升级或替换

### 详细 API 说明

#### 1. cameraPicker（Camera Kit）

- **Import**: `import { cameraPicker } from '@kit.CameraKit'`
- **核心接口**:
  - `pick(ctx: Context, mediaTypes: Array<PickerMediaType>, pickerProfile: PickerProfile): Promise<PickerResult>`
- **起始版本**: API 11（目标 API 12 ✅）
- **所需权限**: `ohos.permission.CAMERA`
- **本地文档绝对路径**:
  `/path/to/skill/arkts_code_lookup_references/harmonyos_references/媒体/Camera Kit（相机服务）/ArkTS API/cameraPicker.md`
- **官方文档 URL**: `https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-cameraPicker`
- **用途**: 通过系统 Picker UI 调起相机拍照或录像，无需手动管理相机设备生命周期

#### 2. Image 组件（ArkUI Kit）

- **Import**: 无需单独 import（ArkUI 内置组件）
- **核心接口**:
  - `Image(src: string | Resource | PixelMap)`
  - 属性: `.width()` `.height()` `.objectFit(ImageFit)`
- **起始版本**: API 7（目标 API 12 ✅）
- **所需权限**: 无
- **本地文档绝对路径**:
  `/path/to/skill/arkts_code_lookup_references/harmonyos_references/应用框架/ArkUI（方舟UI框架）/ArkTS组件/基础组件/Image.md`
- **官方文档 URL**: `https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-basic-components-image`
- **用途**: 在页面上渲染拍摄的图片（接受 PixelMap 或 URI 字符串）

### 权限汇总

| 权限名 | 来源 API | 说明 |
|--------|---------|------|
| `ohos.permission.CAMERA` | cameraPicker | 访问相机设备，需在 module.json5 中声明并运行时申请（user_grant） |

### Android → HarmonyOS 迁移对照（仅类型 B 时输出）

> **本区块仅在用户输入包含安卓代码时输出**，自然语言需求（类型 A）不输出此区块。

| Android API | HarmonyOS 对应 API | 迁移说明 |
|---|---|---|
| `CameraManager.openCamera()` | Camera Kit `CameraManager` | 功能对等，需适配设备生命周期与会话管理 |
| `RecyclerView` | ArkUI `List` 组件 | 声明式写法，无需 Adapter/ViewHolder |

> ⚠️ **以下 Android API 在 HarmonyOS 上无直接对应，需评估替代方案**：
> - `WorkManager`：BackgroundTasksKit 提供后台任务能力，但系统管控策略差异较大，建议重新评估使用场景
> - （如无此类 API，省略本警告块）

### ArkTS 语言参考

> 以下文档包含 ArkTS 语言基础知识与编码规范，建议在编写代码前阅读。

| 文档 | 说明 | 本地路径 |
|------|------|---------|
| ArkTS 语言介绍 | 语言概述：声明、类型、运算符、语句、函数、类、接口、泛型、空安全、模块、装饰器 | `{skill_root}/arkts_code_lookup_references/learning-arkts/ArkTS语言介绍.md` |
| ArkTS 编程规范 | 编码规范：命名约定（lowerCamelCase / UpperCamelCase / ALL_CAPS）、格式规则、编程实践 | `{skill_root}/arkts_code_lookup_references/learning-arkts/ArkTS编程规范.md` |
````

**注意事项**：
- 版本列必须标注 ✅ / ❌，并在汇总表下方说明目标 API 版本
- 如某 API 超出目标版本（❌），在该行注明并在详细说明中给出低版本替代方案
- 本地文档绝对路径必须使用运行时实际的 skill_root 绝对路径，不得使用占位符
- 官方 URL 从每个 `.md` 文件头部 `source:` 字段读取，不得猜测或拼接
- 不生成、不输出任何 .ets 代码文件
- **类型 B 专项**：「Android → HarmonyOS 迁移对照」区块必须输出；对照表中的 HarmonyOS API 列须与 API 汇总表中的条目一一对应
- 「ArkTS 语言参考」区块始终输出，无论输入类型 A 或类型 B——该区块为固定内容，不依赖 API 查找结果
