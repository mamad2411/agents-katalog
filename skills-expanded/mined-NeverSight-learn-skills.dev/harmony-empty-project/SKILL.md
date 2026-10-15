---
name: harmony-empty-project
description: Create a minimal HarmonyOS NEXT empty application project structure from scratch, including standard directories and configuration files such as oh-package.json5, build-profile.json5, AppScope/app.json5, entry module, and hvigorfile.ts. Use when the user asks to create a new HarmonyOS NEXT 空工程/空项目 从0到1 鸿蒙应用 or a minimal runnable demo project.
---

# HarmonyOS NEXT 空工程模板

## 适用场景

当用户提到以下需求时，使用本技能：

- 创建 **HarmonyOS NEXT 空工程 / 空项目 / 最小可运行工程**
- 为示例（如地图、SDK Demo 等）快速生成可运行的壳工程
- 在当前仓库中从零创建一个标准 HarmonyOS NEXT 最小工程

本技能指导代理**从零创建**一个标准的 HarmonyOS NEXT 基于 Stage 模型 + ArkTS的最小可运行工程结构。

---

## 工程结构参考（最小可运行工程）

从零创建 HarmonyOS NEXT 空工程时，建议使用如下通用结构（以 `{ProjectName}` 占位）：

- `{ProjectName}/`
  - `oh-package.json5`
  - `build-profile.json5`
  - `hvigorfile.ts`
  - `hvigor/`
    - `hvigor-config.json5`
  - `AppScope/`
    - `app.json5`
    - `resources/...`
  - `entry/`
    - `oh-package.json5`
    - `build-profile.json5`
    - `hvigorfile.ts`
    - `src/main/module.json5`
    - `src/main/ets/entryability/EntryAbility.ets`
    - `src/main/ets/entrybackupability/EntryBackupAbility.ets`（可选）
    - `src/main/ets/pages/Index.ets`
    - `src/main/resources/...`

以上结构即为一个最小可运行的 HarmonyOS NEXT 应用工程的推荐布局。

---

## 快速使用流程（为用户创建空工程）

当用户要求“创建一个标准的鸿蒙空工程 / HarmonyOS NEXT 最小工程”时，按照以下步骤执行。

### 步骤一：确认目标信息

从用户上下文中推断或向用户确认（如有必要）：

- 目标工程目录名（例如：`harmony-demo`, `harmony-map-demo`）
- 应用包名（如：`com.example.demoapp`）
- 应用显示名称（如：`DemoApp`）

**工程包名生成规则：**

- 若用户**明确给出包名**（如 `com.example.mapdemo`），则**严格使用用户指定的包名**，不要自动改写或追加后缀。
- 若用户**未指定包名**，则**优先根据应用主题 / 业务场景自动生成包名**，例如：
  - 主题为“地图 Demo”时，可生成 `com.example.mapdemo`
  - 主题为“健康记录”时，可生成 `com.example.healthrecord`
- 仅当无法从上下文推断出清晰主题时，才退回到通用占位包名（如下所示）。

如果用户未明确指定，使用合理默认值：

- 目录名：`harmony-demo`
- 包名：默认根据应用主题生成一个语义化包名；若无法识别主题，则使用 `com.example.harmonydemo`
- 应用名称：`Harmony Demo`

### 步骤二：创建工程目录与基础文件

1. 在当前工作目录下创建工程根目录，例如：
   - `{ProjectName}/`（如 `harmony-demo/`）
2. 在 `{ProjectName}/` 下创建以下文件和目录：
   - `oh-package.json5`：包含 `modelVersion`、`description`、`dependencies`、`devDependencies` 等基本字段，例如：
     - `modelVersion`: `"6.0.0"`
     - `devDependencies` 中可包含 `@ohos/hypium`、`@ohos/hamock` 以支持测试
     - **依赖写入规则**：一旦在工程中使用某个三方或系统依赖（如地图库、网络库等），必须将对应依赖显式写入到合适层级的 `oh-package.json5` 的 `dependencies` 字段中，而不是只在代码中直接 `import`。
   - `build-profile.json5`：定义 app 级产品与构建模式（`products`、`buildModeSet` 等），`targetSdkVersion`、`compatibleSdkVersion` 需与开发环境匹配
   - `hvigorfile.ts`：导入 `appTasks` 并导出默认配置：
     - `system: appTasks`
     - `plugins: []`
   - `hvigor/hvigor-config.json5`：Hvigor 全局配置文件，如果缺失会导致类似 “Hvigor config file .../hvigor/hvigor-config.json5 does not exist” 的构建错误
   - `AppScope/app.json5`：定义 `bundleName`、`vendor`、`versionCode`、`versionName`、`icon`、`label` 等
   - `AppScope/resources/`：至少包含基础字符串和图标资源（可由代理按最小配置生成占位资源）；若使用 `layered_image` 作为应用图标，须在 `AppScope/resources/base/media/` 下同时提供 `layered_image.json` 及其引用的 `background`、`foreground` 媒体文件（如 `background.svg`、`foreground.svg`），否则会报资源包错误 11211120。
3. 在 `{ProjectName}/entry/` 下创建模块目录及以下文件：
   - `oh-package.json5`：entry 模块自身的包配置文件（与根目录 `oh-package.json5` 独立，用于避免 DevEco / 构建工具报错 “Missing file \"oh-package.json5\" in entry”）。**当某个依赖只在 entry 模块中被使用时，应优先将该依赖写入 entry 模块的 `oh-package.json5` 的 `dependencies` 中。**
   - `build-profile.json5`：定义 entry 模块构建配置
   - `hvigorfile.ts`：导入 `hapTasks` 并导出默认配置：
     - `system: hapTasks`
     - `plugins: []`
   - `src/main/module.json5`：定义模块名、类型、`mainElement`、`deviceTypes`、`pages`、`abilities` 等
   - `src/main/ets/entryability/EntryAbility.ets` 与 `src/main/ets/pages/Index.ets`：包含最小 UI 与能力入口代码
   - `src/main/resources/`：包含页面引用到的字符串、浮点值、颜色等资源 JSON

### 依赖管理与安装规则

- **依赖声明位置**：
  - 在工程中使用到的任意 ohpm 依赖（例如 `@bdmap/base`、`@bdmap/map` 等），必须写入实际使用该依赖的**具体模块**的 `oh-package.json5` 的 `dependencies` 字段中（如仅 entry 使用，则写入 `{ProjectName}/entry/oh-package.json5`）。
  - 若依赖为整个应用多个模块共享，可根据实际情况写入工程根目录 `oh-package.json5`，但仍需保证使用模块的构建能够解析到该依赖。
- **尝试安装依赖**：
  - 在为用户创建或修改工程时，代理应在对应工程目录（通常为 `{ProjectName}/`）下尝试执行 `ohpm install`，以实际安装 `oh-package.json5` 中声明的依赖。
  - 如运行环境不支持实际执行安装命令，应在回答中明确提示用户需要在工程目录手动执行 `ohpm install` 或相应安装命令，并保证 `oh-package.json5` 中的依赖列表是完整、正确的。

### 步骤三：修改应用基础信息

在新工程目录（例如 `{ProjectName}/`）中，按以下要点设置或修改配置：

- **应用范围信息：`AppScope/app.json5`**
  - 路径：`{ProjectName}/AppScope/app.json5`
  - 字段：
    - `bundleName`: 设置为目标包名（如 `com.example.harmonydemo`）
    - `label`: 通常引用字符串资源（如 `$string:app_name`），如需要可以保持不变
    - `versionCode` / `versionName`: 若用户要求特定版本号则相应调整

- **如有需要，调整工程名和产品信息：`build-profile.json5`**
  - 路径：`{ProjectName}/build-profile.json5`
  - 通常保持默认即可；如用户对产品名等有要求，可在 `products` 中微调。

### 步骤四：确认模块配置完整

在新工程目录中，检查下列关键文件是否存在且结构完整（通常只需确认，无需改动）：

- `{ProjectName}/oh-package.json5`
  - `modelVersion` 字段存在，例如 `"6.0.0"`
  - 如需使用测试框架，`devDependencies` 中包含 `@ohos/hypium` 等依赖

- `{ProjectName}/entry/src/main/module.json5`
  - `module.name` 为 `"entry"`
  - `mainElement` 指向 `"EntryAbility"`
  - `pages` 指向 `$profile:main_pages`
  - `abilities[0].srcEntry` 指向 `./ets/entryability/EntryAbility.ets`

- `{ProjectName}/hvigorfile.ts` 与 `{ProjectName}/entry/hvigorfile.ts`
  - 顶层使用 `appTasks`，entry 模块使用 `hapTasks`

### 步骤五：调整首页页面（可选）

如果用户希望定制一个简单首页（而不仅仅是默认 `Hello World`），可以修改：

- 路径：`{ProjectName}/entry/src/main/ets/pages/Index.ets`

保持结构为一个 `@Entry` + `@Component` 组件，内部 `build()` 返回一个基础布局（如 `RelativeContainer` 或 `Column`）和一个 `Text` 文本，确保页面结构简单且可编译。

---

## 可行性自检（代理执行时的验证要点）

在为用户创建好新的空工程目录后，代理应进行以下自查，以验证结构可行性：

1. **结构检查**
   - 必须存在：
     - `{ProjectName}/oh-package.json5`
     - `{ProjectName}/build-profile.json5`
     - `{ProjectName}/hvigorfile.ts`
     - `{ProjectName}/hvigor/hvigor-config.json5`
     - `{ProjectName}/AppScope/app.json5`
     - `{ProjectName}/entry/oh-package.json5`
     - `{ProjectName}/entry/hvigorfile.ts`
     - `{ProjectName}/entry/src/main/module.json5`
     - `{ProjectName}/entry/src/main/ets/pages/Index.ets`
   - 如果这些文件缺失，由代理补充创建缺失的文件或向用户报告当前结构不完整。

2. **配置一致性检查**
   - `AppScope/app.json5` 中的 `bundleName` 与用户目标包名一致。
   - `entry/src/main/module.json5` 中：
     - `mainElement` 指向的能力在 `abilities` 列表中真实存在。
     - `abilities[0].srcEntry` 指向的 `.ets` 文件实际存在。

3. **构建前检查（Auto Run 建议）**
   - 如果环境中已安装 HarmonyOS NEXT 构建工具链，**建议将 Hvigor 构建命令配置为 auto run 流程的一部分**：在新工程创建完成或模板被修改后，在新工程目录下自动运行 `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon`（或 DevEco Studio 提供的等效构建命令），并确认无明显结构性错误。
   - 对基于本空工程继续开发的场景，建议在仓库层面配置提交前或 CI 的 auto run 脚本，统一执行上述构建命令，确保任何基于该模板的改动都能通过基本编译检查。
   - 如果构建工具不可用，则以结构符合本技能中“工程结构参考”与“可行性自检”的要求为“可行”的判断标准，并在文档或回答中提示用户需要在本地具备工具链后手动执行 `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon` 完成最终校验。

---

## 资源包与媒体资源约束（必读）

为避免构建报错 **Error Code: 11211120, Resource Pack Error: The resource reference '$media:xxx' is not defined**，创建或复制空工程时须遵守以下约束：

1. **layered_image 与引用必须成对存在**
   - `layered_image.json` 中引用的 `$media:background`、`$media:foreground` 表示**同目录下**必须存在名为 `background`、`foreground` 的媒体文件（如 `background.svg`、`foreground.svg`）。
   - 若在 **AppScope** 使用 `icon: "$media:layered_image"`（见 `AppScope/app.json5`），则必须在 `AppScope/resources/base/media/` 下同时放置：
     - `layered_image.json`
     - `background.svg`（或 `background.png`，推荐 svg）
     - `foreground.svg`（或 `foreground.png`，推荐 svg）
   - 若在 **entry** 模块使用 `icon: "$media:layered_image"`（见 `entry/src/main/module.json5`），则必须在 `entry/src/main/resources/base/media/` 下同样放置上述三件（或至少 `background`、`foreground` 两个媒体文件 + `layered_image.json`）。
   - 仅复制 `layered_image.json` 而不复制或创建 `background`、`foreground` 媒体文件会导致 11211120 报错。

2. **其他 $media 引用**
   - 配置中出现的任意 `$media:资源名`（如 `$media:startIcon`）都必须在对应模块的 `resources/base/media/` 下存在同名文件（如 `startIcon.svg`），否则同样会触发资源包错误。
   - `$media:资源名` 的解析只发生在**工程自身**的资源目录（如 `entry/src/main/resources/base/media/`、`AppScope/resources/base/media/`），不会从 `.cursor/skills/...` 等技能目录读取；技能文档仅用于指导代理生成/拷贝资源源码。

3. **代理创建空工程时的要求**
   - 使用本技能模板创建新工程时，凡涉及 `layered_image.json` 的目录，必须一并生成或说明需要放置的 `background`、`foreground` 媒体文件（推荐使用最小可用的 svg 占位图），不得只创建 `layered_image.json`。
   - **图标统一使用 svg**：应用/能力图标相关媒体资源（包括但不限于 `layered_image` 的 `background/foreground`、`startWindowIcon` 的 `startIcon`）应优先生成 **svg** 格式文件。
   - **生成优先级规则**：优先根据用户 app 场景（应用名称/主题/业务类型，如地图、出行、工具等）自动生成符合场景的 svg；若生成失败或用户未提供任何场景信息，再从本技能文档中提供的示例源码**拷贝一份**作为兜底占位资源（并仍写入到工程的 `resources/base/media/` 下）。

更多说明见 [HarmonyOS 资源工具 restool](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/restool)。

---

## 参考模板代码

本节以仓库中提供的标准最小可执行示例工程为蓝本，给出最小可执行工程的模板代码与配置。代理在生成文件时应**与此保持一致**（仅替换目录名 / 包名等标识），并确保图标等媒体资源使用 **svg** 而非 png。

### 1. 根目录 `oh-package.json5`

```markdown
```json
{
  "modelVersion": "6.0.0",
  "description": "Please describe the basic information.",
  "dependencies": {
  },
  "devDependencies": {
    "@ohos/hypium": "1.0.24",
    "@ohos/hamock": "1.0.0"
  }
}
```
```

### 2. 根目录 `build-profile.json5`

```markdown
```json
{
  "app": {
    "signingConfigs": [],
    "products": [
      {
        "name": "default",
        "signingConfig": "default",
        "targetSdkVersion": "6.0.0(20)",
        "compatibleSdkVersion": "5.0.4(16)",
        "runtimeOS": "HarmonyOS",
        "buildOption": {
          "strictMode": {
            "caseSensitiveCheck": true,
            "useNormalizedOHMUrl": true
          }
        }
      }
    ],
    "buildModeSet": [
      {
        "name": "debug",
      },
      {
        "name": "release"
      }
    ]
  },
  "modules": [
    {
      "name": "entry",
      "srcPath": "./entry",
      "targets": [
        {
          "name": "default",
          "applyToProducts": [
            "default"
          ]
        }
      ]
    }
  ]
}
```
```

### 3. 根目录 `hvigorfile.ts`

```markdown
```ts
import { appTasks } from '@ohos/hvigor-ohos-plugin';

export default {
  system: appTasks, /* Built-in plugin of Hvigor. It cannot be modified. */
  plugins: []       /* Custom plugin to extend the functionality of Hvigor. */
}
```
```

### 4. 根目录 `hvigor/hvigor-config.json5`

```markdown
```json5
{
  "modelVersion": "6.0.0",
  "dependencies": {
  },
  "execution": {
    // "analyze": "normal",
    // "daemon": true,
    // "incremental": true,
    // "parallel": true,
    // "typeCheck": false,
    // "optimizationStrategy": "memory"
  },
  "logging": {
    // "level": "info"
  },
  "debugging": {
    // "stacktrace": false
  },
  "nodeOptions": {
    // "maxOldSpaceSize": 8192,
    // "exposeGC": true
  }
}
```
```

### 5. `AppScope/app.json5`

```markdown
```json
{
  "app": {
    "bundleName": "com.example.application",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "icon": "$media:layered_image",
    "label": "$string:app_name"
  }
}
```
```

### 6. `AppScope/resources/base/element/string.json`

```markdown
```json
{
  "string": [
    {
      "name": "app_name",
      "value": "Harmony Demo"
    }
  ]
}
```
```

### 7. `AppScope/resources/base/media/layered_image.json`

```markdown
```json
{
  "layered-image": {
    "background": "$media:background",
    "foreground": "$media:foreground"
  }
}
```
```

> **约束**：`$media:background`、`$media:foreground` 必须在**同目录** `AppScope/resources/base/media/` 下存在对应文件（如 `background.svg`、`foreground.svg`），否则构建报错 11211120。详见上文「资源包与媒体资源约束」。推荐使用 svg，勿仅创建本 JSON 而不创建 background/foreground 文件。

### 8. entry 模块 `oh-package.json5`

```markdown
```json
{
  "name": "entry",
  "version": "1.0.0",
  "description": "Please describe the basic information.",
  "main": "",
  "author": "",
  "license": "",
  "dependencies": {}
}
```
```

### 9. entry 模块 `build-profile.json5`

```markdown
```json5
{
  "apiType": "stageMode",
  "buildOption": {
    "resOptions": {
      "copyCodeResource": {
        "enable": false
      }
    }
  },
  "buildOptionSet": [
    {
      "name": "release",
      "arkOptions": {
        "obfuscation": {
          "ruleOptions": {
            "enable": false,
            "files": [
              "./obfuscation-rules.txt"
            ]
          }
        }
      }
    },
  ],
  "targets": [
    {
      "name": "default"
    },
    {
      "name": "ohosTest",
    }
  ]
}
```
```

### 10. entry 模块 `hvigorfile.ts`

```markdown
```ts
import { hapTasks } from '@ohos/hvigor-ohos-plugin';

export default {
  system: hapTasks, /* Built-in plugin of Hvigor. It cannot be modified. */
  plugins: []       /* Custom plugin to extend the functionality of Hvigor. */
}
```
```

### 11. entry 模块 `src/main/module.json5`

```markdown
```json5
{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": [
      "phone"
    ],
    "deliveryWithInstall": true,
    "installationFree": false,
    "pages": "$profile:main_pages",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntry": "./ets/entryability/EntryAbility.ets",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:layered_image",
        "label": "$string:EntryAbility_label",
        "startWindowIcon": "$media:startIcon",
        "startWindowBackground": "$color:start_window_background",
        "exported": true,
        "skills": [
          {
            "entities": [
              "entity.system.home"
            ],
            "actions": [
              "ohos.want.action.home"
            ]
          }
        ]
      }
    ],
    "extensionAbilities": [
      {
        "name": "EntryBackupAbility",
        "srcEntry": "./ets/entrybackupability/EntryBackupAbility.ets",
        "type": "backup",
        "exported": false,
        "metadata": [
          {
            "name": "ohos.extension.backup",
            "resource": "$profile:backup_config"
          }
        ],
      }
    ]
  }
}
```
```

### 12. `EntryAbility.ets`（入口能力）

```markdown
```ts
import { AbilityConstant, ConfigurationConstant, UIAbility, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { window } from '@kit.ArkUI';

const DOMAIN = 0x0000;

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    try {
      this.context.getApplicationContext().setColorMode(ConfigurationConstant.ColorMode.COLOR_MODE_NOT_SET);
    } catch (err) {
      hilog.error(DOMAIN, 'testTag', 'Failed to set colorMode. Cause: %{public}s', JSON.stringify(err));
    }
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onCreate');
  }

  onDestroy(): void {
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onDestroy');
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    // Main window is created, set main page for this ability
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onWindowStageCreate');

    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(DOMAIN, 'testTag', 'Failed to load the content. Cause: %{public}s', JSON.stringify(err));
        return;
      }
      hilog.info(DOMAIN, 'testTag', 'Succeeded in loading the content.');
    });
  }

  onWindowStageDestroy(): void {
    // Main window is destroyed, release UI related resources
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onWindowStageDestroy');
  }

  onForeground(): void {
    // Ability has brought to foreground
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onForeground');
  }

  onBackground(): void {
    // Ability has back to background
    hilog.info(DOMAIN, 'testTag', '%{public}s', 'Ability onBackground');
  }
}
```
```

### 13. `EntryBackupAbility.ets`（备份扩展能力）

```markdown
```ts
import { hilog } from '@kit.PerformanceAnalysisKit';
import { BackupExtensionAbility, BundleVersion } from '@kit.CoreFileKit';

const DOMAIN = 0x0000;

export default class EntryBackupAbility extends BackupExtensionAbility {
  async onBackup() {
    hilog.info(DOMAIN, 'testTag', 'onBackup ok');
    await Promise.resolve();
  }

  async onRestore(bundleVersion: BundleVersion) {
    hilog.info(DOMAIN, 'testTag', 'onRestore ok %{public}s', JSON.stringify(bundleVersion));
    await Promise.resolve();
  }
}
```
```

### 14. `pages/Index.ets`（首页页面）

```markdown
```ts
@Entry
@Component
struct Index {
  @State message: string = 'Hello World';

  build() {
    RelativeContainer() {
      Text(this.message)
        .id('HelloWorld')
        .fontSize($r('app.float.page_text_font_size'))
        .fontWeight(FontWeight.Bold)
        .alignRules({
          center: { anchor: '__container__', align: VerticalAlign.Center },
          middle: { anchor: '__container__', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          this.message = 'Welcome';
        })
    }
    .height('100%')
    .width('100%')
  }
}
```
```

### 15. entry 关键资源示例

- `entry/src/main/resources/base/element/string.json`

```markdown
```json
{
  "string": [
    {
      "name": "module_desc",
      "value": "module description"
    },
    {
      "name": "EntryAbility_desc",
      "value": "description"
    },
    {
      "name": "EntryAbility_label",
      "value": "label"
    }
  ]
}
```
```

- `entry/src/main/resources/base/element/float.json`

```markdown
```json
{
  "float": [
    {
      "name": "page_text_font_size",
      "value": "50fp"
    }
  ]
}
```
```

- `entry/src/main/resources/base/element/color.json`

```markdown
```json
{
  "color": [
    {
      "name": "start_window_background",
      "value": "#FFFFFF"
    }
  ]
}
```
```

- `entry/src/main/resources/base/profile/main_pages.json`

```markdown
```json
{
  "src": [
    "pages/Index"
  ]
}
```
```

- `entry/src/main/resources/base/profile/backup_config.json`

```markdown
```json
{
  "allowToBackupRestore": true
}
```
```

- `entry/src/main/resources/base/media/layered_image.json`

```markdown
```json
{
  "layered-image": {
    "background": "$media:background",
    "foreground": "$media:foreground"
  }
}
```
```

> **约束**：entry 的 `resources/base/media/` 下也须存在 `background.svg`、`foreground.svg`（或同名 png），否则 11211120。详见「资源包与媒体资源约束」。

- `entry/src/main/resources/base/media/startIcon.svg`

```markdown
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108" width="108" height="108">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2F7DFF"/>
      <stop offset="100%" stop-color="#0A59F7"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="108" height="108" rx="24" fill="url(#bg)"/>
  <rect x="28" y="28" width="22" height="22" rx="6" fill="#EAF1FF"/>
  <rect x="58" y="28" width="22" height="22" rx="6" fill="#DDE9FF"/>
  <rect x="28" y="58" width="22" height="22" rx="6" fill="#DDE9FF"/>
  <rect x="58" y="58" width="22" height="22" rx="6" fill="#BFD6FF"/>
</svg>
```
```

> **约束**：若 `entry/src/main/module.json5` 中存在 `"startWindowIcon": "$media:startIcon"`，则 entry 的 `resources/base/media/` 下必须存在 `startIcon.svg`（或 `startIcon.png`），并且**文件名大小写需与 `$media:` 引用一致**（受 `caseSensitiveCheck` 影响）。

代理在创建空工程时，应直接以本节模板为基础生成文件，并根据用户给定的 `{ProjectName}`、`bundleName` 等做相应替换，且在引入媒体资源时统一采用 svg 格式。

---

## 使用示例

### 示例一：创建默认空工程

用户：  
> @harmony 帮我创建一个 HarmonyOS NEXT 的空工程，用来做后续 SDK Demo。

代理应当：

1. 按“快速使用流程”在当前目录下创建 `{ProjectName}`（如 `harmony-demo`）工程结构。
2. 将包名设置为 `com.example.harmonydemo`。

### 示例二：创建带自定义包名的空工程

用户：  
> 基于现在这个最小工程结构，帮我再创建一个包名为 `com.example.mapdemo` 的鸿蒙空工程。

代理应当：

1. 在当前目录下创建 `{ProjectName}`（如 `harmony-map-demo`）工程结构。
2. 在新工程中修改：
   - `{ProjectName}/AppScope/app.json5` 中的 `bundleName` 为 `com.example.mapdemo`。
3. 按“可行性自检”章节检查关键文件与字段。

---

## 总结

- 本技能基于当前仓库自带的 `harmony` 最小可运行示例工程，通过**结构复制 + 少量配置修改**，快速为用户创建 HarmonyOS NEXT 标准空工程。
- 代理在执行时应始终对照模板工程结构进行检查，确保新工程在文件布局与关键配置上与模板保持一致，从而保证可行性。

