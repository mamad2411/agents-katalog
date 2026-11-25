---
name: dart-oss-design-patterns
description: 学习 scottt2/design-patterns-in-dart 开源项目，通过 GoF 设计模式的纯 Dart 实现，深入理解类与对象的设计（继承、混入、接口、抽象类）。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-classes-objects
  project:
    url: https://github.com/scottt2/design-patterns-in-dart
    stars: 479
    difficulty: beginner
    category: patterns
---

# 学习 Dart 设计模式项目

## Contents

- [项目概览](#项目概览)
- [与 dart-classes-objects 的关联](#与-dart-classes-objects-的关联)
- [项目结构导读](#项目结构导读)
- [设计模式分类](#设计模式分类)
- [Workflow: 通过设计模式学习面向对象](#workflow-通过设计模式学习面向对象)
- [Examples](#examples)

## 项目概览

**项目名称**: design-patterns-in-dart
**作者**: scottt2
**GitHub**: https://github.com/scottt2/design-patterns-in-dart
**Stars**: 479 | **难度**: 入门级

GoF（Gang of Four）23 种经典设计模式的纯 Dart 实现。每个模式独立目录，包含完整可运行的代码示例。该项目是学习 Dart 面向对象特性（类、继承、混入、抽象类、接口）的最佳实践集合。

## 与 dart-classes-objects 的关联

该项目是 `dart-classes-objects` 技能的直接应用案例：

| dart-classes-objects 主题 | 项目对应模式 |
|--------------------------|------------|
| 抽象类与接口 | Strategy, Observer, Command |
| 继承 extends | Template Method, Decorator |
| 混入 Mixin | 行为复用场景 |
| 工厂构造方法 | Factory Method, Abstract Factory |
| sealed class | State, Visitor |
| 扩展方法 | Adapter, Composite 的便利接口 |

## 项目结构导读

```
design-patterns-in-dart/
├── lib/
│   ├── creational/         # 创建型模式
│   │   ├── factory_method/
│   │   ├── abstract_factory/
│   │   ├── builder/
│   │   ├── prototype/
│   │   └── singleton/
│   ├── structural/          # 结构型模式
│   │   ├── adapter/
│   │   ├── bridge/
│   │   ├── composite/
│   │   ├── decorator/
│   │   ├── facade/
│   │   ├── flyweight/
│   │   └── proxy/
│   └── behavioral/          # 行为型模式
│       ├── chain_of_responsibility/
│       ├── command/
│       ├── iterator/
│       ├── observer/
│       ├── strategy/
│       └── ...
└── pubspec.yaml
```

## 设计模式分类

### 创建型模式（5 种）

| 模式 | Dart 关键特性 |
|------|-------------|
| Factory Method | `factory` 构造方法 |
| Abstract Factory | `abstract class` + `factory` |
| Builder | 命名参数 + 级联 `..` |
| Prototype | `copyWith` 模式 |
| Singleton | `static final` + 私有构造 |

### 结构型模式（7 种）

| 模式 | Dart 关键特性 |
|------|-------------|
| Adapter | `extension` 扩展方法 |
| Decorator | Mixin + 委托 |
| Facade | 封装复杂子系统 |
| Proxy | `implements` 接口 |

### 行为型模式（11 种）

| 模式 | Dart 关键特性 |
|------|-------------|
| Strategy | 函数类型 + `typedef` |
| Observer | Stream / `Listenable` |
| Command | 函数对象 + `call()` |
| State | `sealed class` + switch |

## Workflow: 通过设计模式学习面向对象

### Task Progress

- [ ] **Step 1: 选择模式类别。** 从创建型模式开始，逐步到结构型和行为型。
- [ ] **Step 2: 阅读单个模式代码。** 打开对应目录，先看接口/抽象类，再看具体实现。
- [ ] **Step 3: 识别 Dart 特性。** 标注代码中用到的 abstract / extends / implements / mixin / factory / sealed 等。
- [ ] **Step 4: 运行并验证。** 执行 `dart run lib/<pattern_dir>/main.dart` 观察输出。
- [ ] **Step 5: 手写复现。** 关闭源码，尝试自己用 Dart 重写同一模式。
- [ ] **Step 6: 对比差异。** 将自己的实现与项目源码对比，理解 Dart 特性的不同用法。
- [ ] **Step 7: 状态分析。** 运行 `dart analyze` 确保实现无类型错误。
- [ ] **Step 8: Feedback Loop。** 总结该模式使用的 Dart 特性 → 查阅 dart-classes-objects 技能 → 优化实现。

### 条件逻辑

- **如果对某个模式的类图不理解：** 先用纸笔画出 UML，理清类之间的继承和组合关系。
- **如果遇到不熟悉的 Dart 语法：** 使用 `dart-classes-objects` 技能查阅对应的类修饰符说明。
- **如果源码使用了较新的 Dart 特性：** 检查项目 pubspec.yaml 中的 sdk 版本约束。
- **如果需要理解模式的适用场景：** 对照 GoF 原书描述，理解"为什么"要用这个模式。

## Examples

### 从项目中学到的策略模式实现

```dart
typedef SortStrategy = List<int> Function(List<int>);

class Sorter {
  final SortStrategy strategy;
  const Sorter(this.strategy);

  List<int> sort(List<int> data) => strategy(data);
}

List<int> bubbleSort(List<int> data) {
  final list = List<int>.from(data);
  for (var i = 0; i < list.length; i++) {
    for (var j = 0; j < list.length - i - 1; j++) {
      if (list[j] > list[j + 1]) {
        final temp = list[j];
        list[j] = list[j + 1];
        list[j + 1] = temp;
      }
    }
  }
  return list;
}

void main() {
  final sorter = Sorter(bubbleSort);
  print(sorter.sort([3, 1, 4, 1, 5, 9])); // [1, 1, 3, 4, 5, 9]
}
```

### 用 sealed class 实现状态模式

```dart
sealed class ConnectionState {
  const ConnectionState();
}

class Disconnected extends ConnectionState {
  const Disconnected();
}

class Connecting extends ConnectionState {
  const Connecting();
}

class Connected extends ConnectionState {
  final String address;
  const Connected(this.address);
}

String describe(ConnectionState state) => switch (state) {
  Disconnected() => '未连接',
  Connecting() => '连接中...',
  Connected(address: final addr) => '已连接到 $addr',
};
```
