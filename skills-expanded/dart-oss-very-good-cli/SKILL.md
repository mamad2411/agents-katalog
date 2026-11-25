---
name: dart-oss-very-good-cli
description: 学习 VeryGoodOpenSource/very_good_cli 开源项目，通过企业级 CLI 工具理解 Dart 包管理、命令行开发和 Monorepo 工作空间的实战设计。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-packages-pub
    - dart-core-libraries
  project:
    url: https://github.com/VeryGoodOpenSource/very_good_cli
    stars: 2400
    difficulty: advanced
    category: cli
---

# 学习 Very Good CLI 项目

## Contents

- [项目概览](#项目概览)
- [与 dart-packages-pub 的关联](#与-dart-packages-pub-的关联)
- [项目架构分析](#项目架构分析)
- [CLI 开发模式详解](#cli-开发模式详解)
- [Workflow: 通过 very_good_cli 学习 Dart 包管理](#workflow-通过-very_good_cli-学习-dart-包管理)
- [Examples](#examples)

## 项目概览

**项目名称**: very_good_cli
**作者**: VeryGoodOpenSource (Very Good Ventures)
**GitHub**: https://github.com/VeryGoodOpenSource/very_good_cli
**Stars**: 2.4k | **难度**: 进阶

Very Good Ventures 出品的全功能 Dart CLI 工具，用于创建、管理和维护 Dart/Flutter 项目。支持模板生成、测试运行、包发布等完整开发流程。该项目是学习 Dart 命令行开发、pub package 设计、包管理最佳实践的一流范例。

## 与 dart-packages-pub 的关联

该项目是 `dart-packages-pub` 技能的最佳实践：

| dart-packages-pub 主题 | 项目中的应用 |
|----------------------|------------|
| pubspec.yaml 配置 | 多命令入口定义（executables） |
| package 发布 | 版本管理、发布流程 |
| 依赖管理 | 精确的依赖版本约束 |
| 工作空间 | 多包 Monorepo 结构 |
| CLI 入口 | `dart create` / `dart run` |
| Hooks | 项目模板生命周期钩子 |

## 项目架构分析

### 核心架构

```
very_good_cli/
├── bin/
│   └── very_good_cli.dart        # CLI 入口
├── lib/
│   ├── src/
│   │   ├── commands/             # 命令实现
│   │   │   ├── create/
│   │   │   ├── test/
│   │   │   ├── packages/
│   │   │   └── update/
│   │   ├── templates/            # 模板定义
│   │   ├── generators/           # 代码生成器
│   │   └── utils/                # 工具函数
│   └── very_good_cli.dart        # 公共 API
├── test/
│   └── src/commands/             # 命令测试
└── pubspec.yaml
```

### CLI 命令树

```
very_good
├── create <project_name>     # 创建新项目
│   ├── --template <name>     # 模板选择
│   ├── --org-name <org>      # 组织名称
│   └── --desc <description>  # 项目描述
├── test                      # 运行测试
│   ├── --coverage            # 覆盖率报告
│   └── --recursive           # 递归运行
├── packages                  # 包管理
│   ├── get                   # 获取依赖
│   └── upgrade               # 升级依赖
└── update                    # 更新 CLI 本身
```

## CLI 开发模式详解

### pubspec.yaml 命令入口

```yaml
name: very_good_cli
version: 0.24.0
description: A Very Good CLI for Dart

environment:
  sdk: ">=3.0.0 <4.0.0"

executables:
  very_good: very_good_cli

dependencies:
  args: ^2.4.0
  mason: ^0.1.0
  path: ^1.8.0
```

### 命令注册模式

```dart
import 'package:args/command_runner.dart';

class VeryGoodCommandRunner extends CommandRunner<int> {
  VeryGoodCommandRunner()
      : super('very_good', 'A Very Good CLI for Dart') {
    addCommand(CreateCommand());
    addCommand(TestCommand());
    addCommand(PackagesCommand());
    addCommand(UpdateCommand());
  }
}

class CreateCommand extends Command<int> {
  @override
  String get name => 'create';

  @override
  String get description => 'Create a new project';

  @override
  Future<int> run() async {
    final projectName = argResults!.rest.first;
    // 模板生成逻辑
    return 0;
  }
}
```

## Workflow: 通过 very_good_cli 学习 Dart 包管理

### Task Progress

- [ ] **Step 1: 安装全局 CLI。** `dart pub global activate very_good_cli` 体验完整的安装流程。
- [ ] **Step 2: 创建示例项目。** `very_good create my_app` 观察生成的目录结构。
- [ ] **Step 3: 阅读 CLI 入口。** 从 `bin/very_good_cli.dart` 理解 CommandRunner 的初始化。
- [ ] **Step 4: 跟踪一个命令。** 选择 `create` 命令，从参数解析到模板生成的完整链路。
- [ ] **Step 5: 分析 pubspec.yaml。** 理解 `executables` 字段如何映射到命令行。
- [ ] **Step 6: 运行测试。** `dart test` 观察如何使用 `test_process` 测试 CLI 输出。
- [ ] **Step 7: 创建自定义命令。** Fork 项目后添加一个 `very_good analyze` 命令。
- [ ] **Step 8: Feedback Loop。** 实现命令 → `dart run` 测试 → `dart analyze` 验证 → 提交。

### 条件逻辑

- **如果需要创建自己的 CLI 工具：** 参考 very_good_cli 的 CommandRunner 模式和 args 包用法。
- **如果使用 `dart pub global activate` 失败：** 检查 `$HOME/.pub-cache/bin` 是否在 PATH 中。
- **如果需要测试 CLI 命令：** 使用 `test_process` 包模拟终端交互。
- **如果需要发布自己的 package：** 参照项目 `pubspec.yaml` 中的版本管理和发布配置。

## Examples

### 从项目中学到的 CLI 命令模式

```dart
import 'package:args/args.dart';

class AnalyzeCommand extends Command<int> {
  @override
  String get name => 'analyze';

  @override
  String get description => 'Run Dart static analysis';

  AnalyzeCommand() {
    argParser
      ..addFlag('fatal-infos', help: 'Treat infos as fatal')
      ..addFlag('fatal-warnings', help: 'Treat warnings as fatal');
  }

  @override
  Future<int> run() async {
    final args = ['analyze'];
    if (argResults!['fatal-infos'] as bool) args.add('--fatal-infos');
    if (argResults!['fatal-warnings'] as bool) args.add('--fatal-warnings');

    final result = await Process.run('dart', args);
    print(result.stdout);
    return result.exitCode;
  }
}
```

### 结合 dart-packages-pub 的延伸：发布前检查

```dart
Future<bool> isReadyToPublish(Directory projectDir) async {
  final analysis = await Process.run('dart', ['analyze'],
      workingDirectory: projectDir.path);
  if (analysis.exitCode != 0) {
    print('分析失败:\n${analysis.stderr}');
    return false;
  }

  final dryRun = await Process.run(
    'dart', ['pub', 'publish', '--dry-run'],
    workingDirectory: projectDir.path,
  );
  if (dryRun.exitCode != 0) {
    print('发布检查失败:\n${dryRun.stderr}');
    return false;
  }

  return true;
}
```
