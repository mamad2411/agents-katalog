---
name: dart-oss-formz
description: 学习 VeryGoodOpenSource/formz 开源项目，通过表单校验抽象层理解 Dart 类型系统（泛型、抽象类、不可变数据模型）的高级应用。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
  related_skills:
    - dart-type-system
    - dart-classes-objects
  project:
    url: https://github.com/VeryGoodOpenSource/formz
    stars: 481
    difficulty: intermediate
    category: library
---

# 学习 Formz 表单校验库项目

## Contents

- [项目概览](#项目概览)
- [与 dart-type-system 的关联](#与-dart-type-system-的关联)
- [项目架构分析](#项目架构分析)
- [泛型与类型系统设计](#泛型与类型系统设计)
- [Workflow: 通过 Formz 学习 Dart 类型系统](#workflow-通过-formz-学习-dart-类型系统)
- [Examples](#examples)

## 项目概览

**项目名称**: formz
**作者**: VeryGoodOpenSource
**GitHub**: https://github.com/VeryGoodOpenSource/formz
**Stars**: 481 | **难度**: 中等

Very Good Ventures 出品的统一表单校验抽象层。该项目是一个纯 Dart 库，通过泛型抽象定义表单输入、校验状态和提交状态。代码量适中，是学习 Dart 泛型设计、抽象类层级、不可变数据模型的优秀范例。

## 与 dart-type-system 的关联

该项目展示了 `dart-type-system` 技能中泛型的实战设计：

| dart-type-system 主题 | 项目中的应用 |
|---------------------|------------|
| 泛型类 | `FormzInput<T, E>` |
| 抽象类 | `FormzInput` 抽象基类 |
| 类型约束 | `E extends Object` |
| 不可变数据 | `@immutable` + `const` 构造 |
| sealed class | 表单状态枚举 |
| 类型推断 | 纯校验函数的类型推演 |

## 项目架构分析

### 核心模型层次

```
FormzSubmissionStatus (enum)
    ├── initial
    ├── inProgress
    ├── success
    ├── cancelationInProgress
    ├── canceled
    └── failure

FormzInput<T, E> (abstract class)
    ├── T: 输入值类型
    ├── E: 错误类型
    ├── pure() / dirty()
    ├── validate()
    └── displayError

Formz (mixin)
    └── validate() / status / inputs
```

### 泛型设计精髓

```dart
abstract class FormzInput<T, E> {
  final T value;

  const FormzInput._({required this.value, this.error});

  E? get error => validator(value);

  E? Function(T value) get validator;
}
```

## 泛型与类型系统设计

### 双重类型参数

`FormzInput<T, E>` 使用两个泛型参数：
- `T`：表单字段的值类型（如 `String`、`int`）
- `E`：校验错误类型（通常是自定义枚举）

```dart
enum NameValidationError { empty, tooShort }

class NameInput extends FormzInput<String, NameValidationError> {
  const NameInput.pure() : super.pure('');

  const NameInput.dirty(String value) : super.dirty(value);

  @override
  NameValidationError? validator(String value) {
    if (value.isEmpty) return NameValidationError.empty;
    if (value.length < 3) return NameValidationError.tooShort;
    return null;
  }
}
```

### 类型安全的状态管理

```dart
enum FormzSubmissionStatus {
  initial,
  inProgress,
  success,
  failure,
}

class LoginForm with Formz {
  final NameInput name;
  final EmailInput email;

  FormzSubmissionStatus get submissionStatus => _submissionStatus;

  @override
  List<FormzInput> get inputs => [name, email];
}
```

## Workflow: 通过 Formz 学习 Dart 类型系统

### Task Progress

- [ ] **Step 1: 克隆并阅读源码。** 从 `lib/formz.dart` 入手，理解入口暴露的 API。
- [ ] **Step 2: 分析泛型设计。** 标注所有使用泛型的地方，理解 `<T, E>` 的语义。
- [ ] **Step 3: 理解抽象类层级。** 画出 FormzInput 的继承树。
- [ ] **Step 4: 运行测试。** 执行 `dart test` 验证现有功能。
- [ ] **Step 5: 实现自定义输入。** 创建一个自己的 FormzInput 子类。
- [ ] **Step 6: 添加新的校验错误类型。** 为错误类型枚举添加新成员。
- [ ] **Step 7: 代码分析。** `dart analyze` 确保类型安全。
- [ ] **Step 8: Feedback Loop。** 对比你的实现与项目风格 → 优化类型设计 → 重复。

### 条件逻辑

- **如果对泛型的协变/逆变有疑问：** 使用 `dart-type-system` 技能查阅泛型约束说明。
- **如果需要新增输入类型：** 先定义错误枚举，再继承 FormzInput 实现纯校验函数。
- **如果遇到类型系统报错：** 检查泛型参数是否被正确传递，使用 `dart analyze` 定位问题。
- **如果需要理解 sealed class 替代方案：** 对比 FormzSubmissionStatus 的 enum 实现与 sealed class 的优势。

## Examples

### 从项目中学到的类型设计

```dart
enum EmailValidationError { invalid }

class EmailInput extends FormzInput<String, EmailValidationError> {
  const EmailInput.pure() : super.pure('');

  const EmailInput.dirty(String value) : super.dirty(value);

  @override
  EmailValidationError? validator(String value) {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,}$').hasMatch(value)
        ? null
        : EmailValidationError.invalid;
  }
}
```

### 结合 dart-type-system 延伸：泛型表单验证器

```dart
typedef Validator<T, E> = E? Function(T value);

class GenericInput<T, E> extends FormzInput<T, E> {
  final Validator<T, E> _validator;

  const GenericInput.pure(T value, this._validator) : super.pure(value);
  const GenericInput.dirty(T value, this._validator) : super.dirty(value);

  @override
  E? validator(T value) => _validator(value);
}

final ageInput = GenericInput<int, String>.pure(
  0,
  (value) => value < 0 ? '年龄不能为负数' : null,
);
```
