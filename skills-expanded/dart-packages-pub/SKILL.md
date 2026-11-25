---
name: dart-packages-pub
description: 管理 Dart 包生态（Pub 仓库），掌握创建、使用、发布 Package 及工作空间的多包管理。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T10:00:00Z
---
# 管理 Dart 包生态

## Contents
- [使用 Package](#使用-package)
- [创建 Package](#创建-package)
- [发布 Package](#发布-package)
- [依赖管理与版本策略](#依赖管理与版本策略)
- [工作空间 (Workspace)](#工作空间-workspace)
- [Hooks 机制](#hooks-机制)
- [Workflow: 创建并发布一个 Dart Package](#workflow-创建并发布一个-dart-package)
- [Examples](#examples)

## 使用 Package

### 添加依赖

```bash
dart pub add http        # 添加常规依赖
dart pub add dev:test    # 添加开发依赖
dart pub add http:^1.0.0 # 指定版本约束
```

### pubspec.yaml 中的依赖声明

```yaml
name: my_app
environment:
  sdk: ^3.6.0

dependencies:
  http: ^1.2.0
  path: ^1.9.0

dev_dependencies:
  test: ^1.25.0
  lints: ^5.0.0
```

### 依赖类型

| 类型 | 声明位置 | 用途 |
|------|---------|------|
| 常规依赖 | `dependencies` | 运行时需要的包 |
| 开发依赖 | `dev_dependencies` | 开发工具、测试框架 |
| 依赖覆盖 | `dependency_overrides` | 临时覆盖传递依赖版本 |

## 创建 Package

### 使用 dart create 命令

```bash
dart create -t package my_package
```

生成的文件结构：

```
my_package/
├── lib/
│   └── my_package.dart          # 公开 API
├── lib/src/                      # 内部实现
│   └── my_package_base.dart
├── test/
│   └── my_package_test.dart
├── pubspec.yaml
├── README.md
├── CHANGELOG.md
├── LICENSE
└── analysis_options.yaml
```

### pubspec.yaml 完整示例

```yaml
name: my_package
description: A sample Dart package
version: 1.0.0
repository: https://github.com/user/my_package

environment:
  sdk: ^3.6.0

dependencies:
  meta: ^1.15.0

dev_dependencies:
  test: ^1.25.0
  lints: ^5.0.0
```

### 包的文件结构规范

- `lib/` — 公开 API，所有 `import 'package:xxx/yyy.dart'` 的入口
- `lib/src/` — 内部实现，不应对用户暴露
- `test/` — 测试文件，命名以 `_test.dart` 结尾
- `example/` — 用法示例
- `bin/` — 可执行入口（若为命令行工具）
- `benchmark/` — 性能测试

## 发布 Package

### 发布前检查

```bash
dart pub publish --dry-run   # 模拟发布，检查问题
dart analyze                  # 确保零错误
dart test                     # 确保测试通过
dart doc                      # 生成文档
```

### 发布到 pub.dev

```bash
dart pub publish
```

**发布前必须确保**：
1. `pubspec.yaml` 包含 `description`、`version`、`repository` 和 `environment`
2. `CHANGELOG.md` 已更新
3. `LICENSE` 文件存在
4. 分析器零错误零警告

### 版本管理

Dart 使用语义化版本 (semver)：`MAJOR.MINOR.PATCH`

| 版本号变更 | 含义 |
|-----------|------|
| `1.2.3` → `1.2.4` | 修复 bug（PATCH） |
| `1.2.3` → `1.3.0` | 新增功能，兼容旧版（MINOR） |
| `1.2.3` → `2.0.0` | 破坏性变更（MAJOR） |

```bash
dart pub version major   # 1.0.0 → 2.0.0
dart pub version minor   # 1.0.0 → 1.1.0 (加 prerelease: --preid=alpha)
dart pub version patch   # 1.0.0 → 1.0.1
```

## 依赖管理与版本策略

### 版本约束写法

```yaml
dependencies:
  package_a: ^1.2.3       # >=1.2.3 <2.0.0（caret 约束）
  package_b: '>=2.0.0 <3.0.0'  # 显式范围
  package_c: any          # 任意版本（不推荐）
```

### 依赖覆盖

用于临时替换传递依赖的版本：

```yaml
dependency_overrides:
  some_package: ^2.0.0     # 强制使用指定版本
```

**注意**：`dependency_overrides` 仅在开发时使用，不应在发布包中使用。

### 传递依赖

```bash
dart pub deps              # 查看依赖树
dart pub deps --json       # JSON 格式输出
dart pub outdated          # 检查可更新的依赖
dart pub upgrade           # 更新到最新兼容版本
```

## 工作空间 (Workspace)

Pub 工作空间支持在单个开发环境中管理多个相互依赖的包（monorepo）。

### 配置工作空间

根目录 `pubspec.yaml`：

```yaml
name: my_workspace
publish_to: none

environment:
  sdk: ^3.6.0

workspace:
  - packages/package_a
  - packages/package_b
  - packages/shared
```

子包 `packages/package_a/pubspec.yaml`：

```yaml
name: package_a
environment:
  sdk: ^3.6.0

dependencies:
  shared: any    # 工作空间内的包自动解析
```

### 工作空间命令

```bash
# 在工作空间任意位置运行
dart pub get       # 为所有成员解析依赖
dart test          # 运行当前包的测试
dart run build_runner build  # 在所有成员中运行
```

### 使用场景

- 大型项目拆分为多个子包
- 共享代码库（models、utils、api client）
- Flutter 应用的模块化开发

## Hooks 机制

Dart Hooks 允许在开发工作流的特定节点自动执行脚本。

### 配置文件 `.agents/hooks.json`

```json
{
  "dart-format": {
    "Stop": [
      {
        "type": "command",
        "command": "dart format .",
        "timeout": 30
      }
    ]
  },
  "dart-analyze": {
    "Stop": [
      {
        "type": "command",
        "command": "dart analyze",
        "timeout": 90
      }
    ]
  }
}
```

**事件类型**：
- `Stop` — Agent 停止编辑后触发
- `Start` — Agent 开始编辑前触发

## Workflow: 创建并发布一个 Dart Package

### Task Progress

- [ ] **Step 1: 创建包骨架。** 运行 `dart create -t package <name>` 生成项目结构。
- [ ] **Step 2: 配置 pubspec.yaml。** 填写 `name`、`description`、`version`、`repository`、SDK 约束和依赖。
- [ ] **Step 3: 实现功能。** 在 `lib/` 下编写公开 API，在 `lib/src/` 下编写内部实现。使用 `library` 或 barrel file 导出。
- [ ] **Step 4: 编写测试。** 在 `test/` 目录创建 `*_test.dart` 文件，确保核心功能有测试覆盖。
- [ ] **Step 5: 编写文档。** 使用 `///` 文档注释，编写 README.md 和 CHANGELOG.md。
- [ ] **Step 6: 运行质量检查。** 依次执行 `dart analyze`、`dart test`、`dart doc`。
- [ ] **Step 7: 模拟发布检查。** 运行 `dart pub publish --dry-run` 确认所有必需文件就位。
- [ ] **Step 8: 正式发布。** 运行 `dart pub publish` 发布到 pub.dev。
- [ ] **Step 9: 版本迭代。** 使用 `dart pub version <major|minor|patch>` 更新版本号后重复发布流程。
- [ ] **Step 10: Feedback Loop。** 审查发布输出 → 修复警告 → 更新 CHANGELOG → 重新发布。

### 条件逻辑

- **如果创建 NEW Package：** 使用 `dart create -t package` 命令生成标准骨架。
- **如果创建命令行工具：** 使用 `dart create -t console-full` 并在 `executables` 字段声明入口。
- **如果配置工作空间 (monorepo)：** 在根目录 `pubspec.yaml` 中添加 `workspace` 字段列出所有成员包路径。
- **如果依赖工作空间内的子包：** 使用 `any` 作为版本约束，pub 自动解析到本地版本。
- **如果发布到 pub.dev：** 确保 `dependency_overrides` 已移除，version 字段不为空。
- **如果遇到版本冲突：** 运行 `dart pub outdated` 查看可更新依赖，使用 `dependency_overrides` 临时解决。

## Examples

### 创建和发布一个完整的 Package

```bash
dart create -t package dart_math_utils
cd dart_math_utils
```

```dart
// lib/dart_math_utils.dart
export 'src/math_utils_base.dart';

// lib/src/math_utils_base.dart
extension MathUtils on num {
  double percentOf(num total) => this / total * 100;
  
  bool isBetween(num min, num max) => this >= min && this <= max;
}

int factorial(int n) {
  if (n < 0) throw ArgumentError('n must be non-negative');
  if (n == 0) return 1;
  return n * factorial(n - 1);
}
```

```dart
// test/dart_math_utils_test.dart
import 'package:dart_math_utils/dart_math_utils.dart';
import 'package:test/test.dart';

void main() {
  group('factorial', () {
    test('factorial(0) returns 1', () {
      expect(factorial(0), equals(1));
    });
    
    test('factorial(5) returns 120', () {
      expect(factorial(5), equals(120));
    });
  });
  
  group('percentOf', () {
    test('25.percentOf(100) returns 25', () {
      expect(25.percentOf(100), equals(25.0));
    });
  });
}
```

```yaml
# pubspec.yaml
name: dart_math_utils
description: Useful math utility functions and extensions for Dart.
version: 1.0.0
repository: https://github.com/user/dart_math_utils

environment:
  sdk: ^3.6.0

dev_dependencies:
  test: ^1.25.0
  lints: ^5.0.0
```

### 工作空间配置示例

```yaml
# 根目录 pubspec.yaml
name: my_monorepo
publish_to: none

environment:
  sdk: ^3.6.0

workspace:
  - packages/shared
  - packages/api
  - packages/app
```

```yaml
# packages/api/pubspec.yaml
name: my_api
environment:
  sdk: ^3.6.0

dependencies:
  shared: any
  http: ^1.2.0
```
