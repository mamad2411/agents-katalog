---
name: dart-oss-mason
description: 学习 felangel/mason 开源项目，通过 Mustache 模板引擎和代码生成 CLI 理解 Dart 包管理、模板系统和 CLI 开发的综合应用。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-packages-pub
    - dart-core-libraries
  project:
    url: https://github.com/felangel/mason
    stars: 1100
    difficulty: advanced
    category: cli
---

# 学习 Mason 模板引擎项目

## Contents

- [项目概览](#项目概览)
- [与 dart-packages-pub 的关联](#与-dart-packages-pub-的关联)
- [项目架构分析](#项目架构分析)
- [模板引擎实现详解](#模板引擎实现详解)
- [Workflow: 通过 Mason 学习 CLI 与模板系统](#workflow-通过-mason-学习-cli-与模板系统)
- [Examples](#examples)

## 项目概览

**项目名称**: mason
**作者**: felangel
**GitHub**: https://github.com/felangel/mason
**Stars**: 1.1k | **难度**: 进阶

一个基于 Mustache 模板的代码生成工具，允许开发者创建可复用的模板（"Bricks"）。支持从模板仓库安装 Bricks、变量替换、条件生成等。项目展示了 Dart CLI 工具、模板引擎、包管理/发布生态的综合设计。

## 与 dart-packages-pub 的关联

该项目综合应用了 `dart-packages-pub` 技能：

| dart-packages-pub 主题 | 项目中的应用 |
|----------------------|------------|
| package 结构 | Monorepo 多包（mason, mason_cli, mason_api） |
| 依赖管理 | melos 工作空间管理 |
| 发布流程 | pub.dev 发布 mason 包 |
| 模板文件结构 | __brick__ 和 brick.yaml 约定 |
| dev_dependencies | 测试与构建工具配置 |

## 项目架构分析

### 核心模块

```
mason/
├── packages/
│   ├── mason/              # 核心模板引擎
│   │   ├── lib/
│   │   │   ├── mason.dart  # 生成器 API
│   │   │   └── src/
│   │   │       ├── generator.dart
│   │   │       ├── brick_yaml.dart
│   │   │       └── hooks.dart
│   │   └── pubspec.yaml
│   ├── mason_cli/          # CLI 命令
│   │   ├── lib/
│   │   │   └── src/
│   │   │       ├── commands/
│   │   │       └── mason_cli.dart
│   │   └── pubspec.yaml
│   └── mason_api/          # HTTP API 服务
└── pubspec.yaml            # 工作空间根配置
```

### Brick 模板结构

```
my_feature/
├── brick.yaml              # Brick 元数据
│   name: my_feature
│   description: A new feature
│   vars:
│     feature_name:
│       type: string
│       description: Feature name
│       prompt: What is the feature name?
├── __brick__/              # 模板文件（Mustache）
│   └── lib/
│       └── src/
│           └── {{feature_name.snakeCase()}}.dart
└── hooks/
    ├── pre_gen.dart        # 生成前钩子
    └── post_gen.dart       # 生成后钩子
```

## 模板引擎实现详解

### Mustache 模板处理

```dart
import 'package:mustache_template/mustache_template.dart';

class BrickGenerator {
  final Map<String, dynamic> _vars;

  BrickGenerator(this._vars);

  String render(String template) {
    return Template(template).renderString(_vars);
  }

  void generate(Brick brick, Directory target) {
    for (final file in brick.files) {
      final content = render(file.content);
      final outputPath = render(file.path);
      target.childFile(outputPath).writeAsStringSync(content);
    }
  }
}
```

### brick.yaml 解析

```dart
class BrickVariable {
  final String name;
  final String type;
  final String? defaultValue;
  final String? prompt;

  const BrickVariable({
    required this.name,
    required this.type,
    this.defaultValue,
    this.prompt,
  });

  factory BrickVariable.fromYaml(Map<String, dynamic> yaml) => BrickVariable(
    name: yaml['name'] as String,
    type: yaml['type'] as String,
    defaultValue: yaml['default'] as String?,
    prompt: yaml['prompt'] as String?,
  );
}
```

## Workflow: 通过 Mason 学习 CLI 与模板系统

### Task Progress

- [ ] **Step 1: 安装 Mason CLI。** `dart pub global activate mason_cli` 体验安装流程。
- [ ] **Step 2: 创建第一个 Brick。** `mason new my_brick` 观察生成的模板结构。
- [ ] **Step 3: 运行 Brick。** `mason make my_brick` 体验变量提示和代码生成。
- [ ] **Step 4: 阅读核心生成器。** 从 `packages/mason/lib/src/generator.dart` 理解模板处理流程。
- [ ] **Step 5: 分析 Monorepo 结构。** 理解 melos 如何管理多包工作空间。
- [ ] **Step 6: 创建自定义 Hook。** 实现 `pre_gen.dart` 在生成前验证输入。
- [ ] **Step 7: 运行测试。** `dart test` 观察模板生成和变量替换的测试。
- [ ] **Step 8: Feedback Loop。** 修改 Brick → 重新 make → 验证输出 → 迭代优化。

### 条件逻辑

- **如果需要了解 Monorepo 管理：** 使用 `dart-packages-pub` 技能中的工作空间章节。
- **如果模板变量未被替换：** 检查 `{{variable}}` 的 Mustache 语法是否正确，变量名是否在 `brick.yaml` 中定义。
- **如果 Hook 执行失败：** 检查 Hook 文件的依赖是否正确，是否需要先运行 `dart pub get`。
- **如果需要发布自定义 Brick：** 参考 mason 官方的 Brick 注册和发布流程。

## Examples

### 从项目中学到的模板生成模式

```yaml
# brick.yaml
name: bluetooth_feature
description: Generate a new Bluetooth feature module
vars:
  service_name:
    type: string
    description: Bluetooth service name
    default: MyService
    prompt: What is the Bluetooth service name?
```

```dart
// __brick__/lib/src/{{service_name.snakeCase()}}_service.dart
class {{service_name.pascalCase()}}Service {
  final String deviceId;

  const {{service_name.pascalCase()}}Service({required this.deviceId});

  Future<void> connect() async {
    // 连接 {{service_name}} 设备
  }

  Future<void> disconnect() async {
    // 断开 {{service_name}} 设备
  }
}
```

### 结合 dart-packages-pub 的延伸练习：Monorepo 工作空间

```yaml
# 根 pubspec.yaml
name: my_tools_workspace

environment:
  sdk: ">=3.0.0 <4.0.0"

workspace:
  - packages/my_cli
  - packages/my_core
  - packages/my_templates
```
