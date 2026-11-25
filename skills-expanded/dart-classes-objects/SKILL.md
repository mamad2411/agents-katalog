---
name: dart-classes-objects
description: 设计 Dart 类与对象的层次结构（构造方法、继承、混入、扩展方法），构建可维护的面向对象架构。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-10T10:00:00Z
---
# 设计 Dart 类与对象

## Contents
- [类的基本结构](#类的基本结构)
- [构造方法](#构造方法)
- [继承](#继承)
- [混入 (Mixin)](#混入-mixin)
- [枚举](#枚举)
- [扩展方法与扩展类型](#扩展方法与扩展类型)
- [类型修饰符](#类型修饰符)
- [Workflow: 设计类的层次结构](#workflow-设计类的层次结构)
- [Examples](#examples)

## 类的基本结构

### 定义类

```dart
class Point {
  // 实例变量
  final double x;
  final double y;

  // 构造方法
  const Point(this.x, this.y);

  // 命名构造方法
  Point.origin()
      : x = 0,
        y = 0;

  // 实例方法
  double distanceTo(Point other) {
    final dx = x - other.x;
    final dy = y - other.y;
    return _sqrt(dx * dx + dy * dy);
  }

  // Getter
  double get magnitude => _sqrt(x * x + y * y);

  // 操作符重载
  Point operator +(Point other) => Point(x + other.x, y + other.y);

  // 重写方法
  @override
  String toString() => 'Point($x, $y)';

  // 静态方法
  static double _sqrt(double v) => v < 0 ? 0 : v * v;
}
```

### 抽象类

```dart
abstract class Shape {
  double get area;           // 抽象 getter
  double get perimeter;      // 抽象 getter

  // 具体方法可以在抽象类中实现
  String describe() => '面积: $area, 周长: $perimeter';
}
```

### Getter 与 Setter

```dart
class Rectangle {
  double _width;
  double _height;

  Rectangle(this._width, this._height);

  double get width => _width;
  set width(double value) {
    if (value <= 0) throw ArgumentError('宽度必须为正数');
    _width = value;
  }

  double get area => _width * _height;  // 计算属性
}
```

## 构造方法

### 构造方法类型

```dart
class User {
  final String name;
  final int age;

  // 标准构造方法（使用 this 简写）
  User(this.name, this.age);

  // 命名构造方法
  User.guest() : name = 'Guest', age = 0;

  // 初始化列表
  User.fromJson(Map<String, dynamic> json)
      : name = json['name'] as String,
        age = json['age'] as int;

  // 工厂构造方法（可以返回缓存实例）
  static final _cache = <String, User>{};

  factory User.cached(String name, int age) {
    return _cache.putIfAbsent(name, () => User(name, age));
  }

  // const 构造方法（编译时常量）
  const User.empty() : name = '', age = 0;
}

// 使用 const 构造方法
const emptyUser = User.empty();
```

### 重定向构造方法

```dart
class Vector2D {
  final double x;
  final double y;

  Vector2D(this.x, this.y);

  // 重定向到主构造方法
  Vector2D.zero() : this(0, 0);
  Vector2D.diagonal(double value) : this(value, value);
}
```

## 继承

```dart
class Animal {
  final String name;
  Animal(this.name);

  void makeSound() => print('...');
}

class Dog extends Animal {
  final String breed;

  Dog(String name, this.breed) : super(name);

  @override
  void makeSound() => print('Woof!');

  void fetch() => print('$name is fetching');
}

void main() {
  Dog dog = Dog('Buddy', 'Golden Retriever');
  dog.makeSound();   // Woof!
  dog.fetch();       // Buddy is fetching
}
```

### super 参数传递

```dart
class Employee extends Person {
  final String company;

  // Dart 3 支持在子类构造方法中直接向 super 传递参数
  Employee(super.name, this.company);

  // 完整的 super 初始化
  Employee.withId(super.id, super.name, this.company);
}
```

## 混入 (Mixin)

### 定义和使用 Mixin

```dart
mixin Logger {
  void log(String message) => print('[${DateTime.now()}] $message');
}

mixin Persistence {
  void save() => print('Saving...');
  void load() => print('Loading...');
}

class UserService with Logger, Persistence {
  void createUser(String name) {
    log('Creating user: $name');
    save();
  }
}
```

### Mixin 约束

```dart
mixin Flyer on Animal {
  void fly() => print('$name is flying');
}

class Bird extends Animal with Flyer {
  Bird(String name) : super(name);
}

// 错误：Git 没有继承 Animal
// class Airplane with Flyer {}  // 编译错误！
```

### Mixin Class

```dart
// 既可以作为类使用，也可以作为 mixin
mixin class Animatable {
  void animate() => print('Animating...');
}

// 作为类
var anim = Animatable();

// 作为 mixin
class MyWidget with Animatable {}
```

## 枚举

### 增强枚举 (Enhanced Enums)

```dart
enum Status {
  pending('⏳'),
  inProgress('🔄'),
  completed('✅'),
  cancelled('❌');

  final String icon;
  const Status(this.icon);

  bool get isActive => this == pending || this == inProgress;
}

void main() {
  final s = Status.completed;
  print('${s.icon} ${s.name}');  // ✅ completed
  print(s.isActive);              // false
  print(Status.values);           // [Status.pending, Status.inProgress, ...]
}
```

## 扩展方法与扩展类型

### 扩展方法

```dart
// 为现有类型添加方法
extension StringExtension on String {
  String get capitalized =>
      isEmpty ? '' : '${this[0].toUpperCase()}${substring(1)}';

  bool get isEmail => contains('@') && contains('.');

  String repeat(int times) => List.filled(times, this).join();
}

void main() {
  print('hello'.capitalized);   // Hello
  print('a@b.com'.isEmail);    // true
  print('Hi'.repeat(3));        // HiHiHi
}
```

### 扩展类型 (Extension Types)

用于为现有类型创建零成本的包装类型：

```dart
extension type IdNumber(int id) {
  bool isValid() => id > 0 && id < 999999;
}

extension type Email(String value) {
  bool get isValid => value.contains('@');
  String get domain => value.split('@').last;
}

void main() {
  var id = IdNumber(42);
  print(id.isValid());  // true

  var email = Email('user@example.com');
  print(email.domain);  // example.com
}
```

## 类型修饰符

Dart 3 引入了类修饰符来控制类的继承关系：

| 修饰符 | 可构造 | 可继承 | 可实现 | 可混入 |
|--------|--------|--------|--------|--------|
| 无修饰符 | ✅ | ✅ | ✅ | ✅ |
| `interface` | ✅ | ❌ | ✅ | ❌ |
| `final` | ✅ | ❌ | ❌ | ❌ |
| `base` | ✅ | ✅ | ❌ | ❌ |
| `sealed` | ❌ | ✅ | ❌ | ❌ |
| `mixin class` | ✅ | ✅ | ✅ | ✅ |

### 使用示例

```dart
// interface: 只能实现，不能继承
interface class DataSource {
  Future<String> fetch();
}

// base: 只能被同库的类继承
base class BaseViewModel {
  void dispose() {}
}

// final: 不能被继承或实现（最严格的封装）
final class ImmutableData {
  final int value;
  const ImmutableData(this.value);
}

// sealed: 限制子类在同一文件中（适合 exhaustiveness check）
sealed class Result {
  const Result();
}

class Success extends Result {
  final dynamic data;
  const Success(this.data);
}

class Failure extends Result {
  final String error;
  const Failure(this.error);
}

// 使用 sealed 的 exhaustive switch
String handleResult(Result result) => switch (result) {
  Success(data: var d) => '成功: $d',
  Failure(error: var e) => '失败: $e',
}; // 无需 default 分支
```

## Workflow: 设计类的层次结构

### Task Progress

- [ ] **Step 1: 分析领域模型。** 识别实体、行为、关系。画出 UML 类图或树形图。
- [ ] **Step 2: 定义基类或接口。** 使用 `abstract class` 定义公共契约，使用 `interface class` 仅暴露实现接口。
- [ ] **Step 3: 实现具体类。** 按单一职责原则拆分。使用 `final` 字段和初始化列表。
- [ ] **Step 4: 使用 Mixin 复用行为。** 将可共享的行为（如 Logging、Validation）提取为 Mixin。
- [ ] **Step 5: 添加扩展方法。** 为第三方类或核心库类型添加便利方法。保持扩展方法简短。
- [ ] **Step 6: 选择合适的类型修饰符。** `sealed` 用于有限子类，`final` 用于不可变数据，`interface` 用于纯契约。
- [ ] **Step 7: 编写单元测试。** 测试每个类的主要行为和方法，包括边界情况。
- [ ] **Step 8: 运行分析器。** `dart analyze` 检查类型正确性。
- [ ] **Step 9: Feedback Loop。** 审查代码 → 检查是否违反 SRP → 提取重复代码为 Mixin → 重新测试。

### 条件逻辑

- **如果类有多个可选属性：** 使用命名参数构造方法，提供合理默认值。
- **如果需要在构造时计算值：** 使用初始化列表（initializer list），不要在构造体内初始化 final 字段。
- **如果需要对实例缓存：** 使用 `factory` 构造方法 + 静态缓存 Map。
- **如果多个类共享相同行为：** 提取为 Mixin，不要用继承。
- **如果子类集合是已知且有限的：** 使用 `sealed class` 确保 switch 穷举检查。
- **如果类只作为契约使用（无实现代码）：** 使用 `abstract class` 或 `interface class`。
- **如果需要为现有类型添加功能但不修改原类：** 使用扩展方法（extension），如需类型安全包装则使用扩展类型。

## Examples

### 完整的领域模型设计

```dart
// 基础抽象
abstract class Entity {
  final String id;
  final DateTime createdAt;

  const Entity({required this.id, DateTime? createdAt})
      : createdAt = createdAt ?? DateTime.now();
}

// Mixin 行为复用
mixin Auditable {
  DateTime? updatedAt;

  void markUpdated() => updatedAt = DateTime.now();
}

// sealed 结果类型
sealed class PaymentResult {
  const PaymentResult();
}

class PaymentSuccess extends PaymentResult {
  final String transactionId;
  const PaymentSuccess(this.transactionId);
}

class PaymentFailure extends PaymentResult {
  final String reason;
  const PaymentFailure(this.reason);
}

// 具体实体类
class Order extends Entity with Auditable {
  final List<OrderItem> items;
  OrderStatus status;

  Order({
    required super.id,
    required this.items,
    this.status = OrderStatus.pending,
  });

  double get total => items.fold(0, (sum, item) => sum + item.subtotal);

  PaymentResult checkout(PaymentMethod method) {
    if (items.isEmpty) return const PaymentFailure('购物车为空');
    try {
      final txId = method.process(total);
      status = OrderStatus.completed;
      markUpdated();
      return PaymentSuccess(txId);
    } catch (e) {
      return PaymentFailure('支付失败: $e');
    }
  }
}

// 枚举
enum OrderStatus {
  pending('待支付'),
  completed('已完成'),
  cancelled('已取消');

  final String label;
  const OrderStatus(this.label);
}

// 值对象
class OrderItem {
  final String name;
  final int quantity;
  final double price;

  const OrderItem({
    required this.name,
    required this.quantity,
    required this.price,
  });

  double get subtotal => quantity * price;
}

// 接口
interface class PaymentMethod {
  String process(double amount) =>
      throw UnimplementedError('process() must be implemented');
}
```

### 扩展方法与工厂模式

```dart
extension DateTimeFormatting on DateTime {
  String get ymd => '$year-${month.toString().padLeft(2, '0')}-${day.toString().padLeft(2, '0')}';

  String timeAgo() {
    final diff = DateTime.now().difference(this);
    if (diff.inDays > 365) return '${diff.inDays ~/ 365}年前';
    if (diff.inDays > 30) return '${diff.inDays ~/ 30}个月前';
    if (diff.inDays > 0) return '${diff.inDays}天前';
    if (diff.inHours > 0) return '${diff.inHours}小时前';
    return '刚刚';
  }
}

class ServiceFactory {
  static final _instances = <Type, Object>{};

  static T get<T>(T Function() builder) {
    return _instances.putIfAbsent(T, builder) as T;
  }
}
```
