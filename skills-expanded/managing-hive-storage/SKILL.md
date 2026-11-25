---
name: "managing-hive-storage"
description: "Hive CE (Community Edition v2.19.x) NoSQL object database for Flutter providing blazing-fast key-value and object storage with TypeAdapters. Use this skill when implementing offline-first architecture, high-performance local data caching, NoSQL document-style object stores, custom TypeAdapter serialization for complex objects, lazy loading boxes for memory efficiency, encrypted boxes (HiveAES encryption), database compaction for size optimization, storing large datasets without SQL schema overhead, implementing local-first sync patterns, or migrating from SQLite to NoSQL. Supports primitive types, custom objects, lists, and maps. Ideal for apps requiring ultra-fast read/write operations (microsecond latency), object persistence without ORM complexity, or local-first data architecture."
metadata:
  last_modified: "2026-04-27 17:41:00 (GMT+8)"
---

# Hive CE NoSQL Database Guide

## Goal
Implement high-performance NoSQL object storage using Hive CE (Community Edition). Hive offers blazing-fast synchronous operations, custom type adapters, and lazy loading for efficient local data persistence.

## Process

### Phase 1: Install Dependencies

```yaml
dependencies:
  hive_ce: ^2.23.3
  hive_ce_flutter: ^2.5.0

dev_dependencies:
  hive_ce_generator: ^1.12.1
  build_runner: ^2.17.1
```

### Phase 2: Initialize Hive

```dart
import 'package:hive_ce_flutter/hive_ce_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Hive.initFlutter();
  
  // Register adapters
  Hive.registerAdapter(UserAdapter());
  Hive.registerAdapter(TodoAdapter());
  
  // Open boxes
  await Hive.openBox<User>('users');
  await Hive.openBox<Todo>('todos');
  
  runApp(MyApp());
}
```

### Phase 3: Define Models with TypeAdapters

**Using Code Generation (Recommended)**:

```dart
import 'package:hive_ce/hive.dart';

part 'user.g.dart';

@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  final String id;
  
  @HiveField(1)
  final String name;
  
  @HiveField(2)
  final String email;
  
  @HiveField(3)
  final DateTime createdAt;
  
  User({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });
}

// Generate adapter: dart run build_runner build
```

**Manual TypeAdapter**:

```dart
class UserAdapter extends TypeAdapter<User> {
  @override
  final int typeId = 0;

  @override
  User read(BinaryReader reader) {
    return User(
      id: reader.readString(),
      name: reader.readString(),
      email: reader.readString(),
      createdAt: DateTime.fromMillisecondsSinceEpoch(reader.readInt()),
    );
  }

  @override
  void write(BinaryWriter writer, User obj) {
    writer.writeString(obj.id);
    writer.writeString(obj.name);
    writer.writeString(obj.email);
    writer.writeInt(obj.createdAt.millisecondsSinceEpoch);
  }
}
```

### Phase 4: CRUD Operations

**Create/Update**:
```dart
final box = Hive.box<User>('users');

// Add with auto-key
await box.add(User(id: '1', name: 'John', email: 'john@example.com', createdAt: DateTime.now()));

// Put with custom key
await box.put('user_1', user);

// Update (if model extends HiveObject)
user.name = 'Jane';
await user.save();
```

**Read**:
```dart
// Get by key
final user = box.get('user_1');

// Get all values
final allUsers = box.values.toList();

// Filter
final activeUsers = box.values.where((u) => u.isActive).toList();

// Get at index
final firstUser = box.getAt(0);
```

**Delete**:
```dart
// Delete by key
await box.delete('user_1');

// Delete at index
await box.deleteAt(0);

// Delete if model extends HiveObject
await user.delete();

// Clear all
await box.clear();
```

### Phase 5: Advanced Patterns

**Lazy Boxes** (for large data):
```dart
// Open lazy box (loads data on demand)
final lazyBox = await Hive.openLazyBox<User>('users_lazy');

// Async get (only loads when accessed)
final user = await lazyBox.get('user_1');
```

**Encrypted Boxes**:
```dart
import 'package:hive_ce/hive.dart';
import 'dart:convert';
import 'dart:typed_data';

final key = Hive.generateSecureKey(); // Store this securely!

final encryptedBox = await Hive.openBox<User>(
  'secure_users',
  encryptionCipher: HiveAesCipher(key),
);
```

**Reactive Listening**:
```dart
// Listen to box changes
box.watch().listen((event) {
  print('Box changed: ${event.key}');
  if (event.deleted) {
    print('Item deleted');
  } else {
    print('Item added/updated: ${event.value}');
  }
});

// Listen to specific key
box.watch(key: 'user_1').listen((event) {
  print('User 1 updated: ${event.value}');
});
```

**Compaction** (reduce file size):
```dart
// Compact box to reclaim space
await box.compact();

// Auto-compact on close
await box.close();
```

### Phase 6: Integration with State Management

**With Riverpod**:
```dart
final userBoxProvider = Provider<Box<User>>((ref) {
  return Hive.box<User>('users');
});

final usersProvider = StreamProvider<List<User>>((ref) {
  final box = ref.watch(userBoxProvider);
  return box.watch().map((_) => box.values.toList());
});

// Usage in widget
final users = ref.watch(usersProvider);
users.when(
  data: (list) => ListView(children: list.map((u) => UserTile(u)).toList()),
  loading: () => CircularProgressIndicator(),
  error: (e, _) => Text('Error: $e'),
);
```

---

## Constraints

* **TypeId Uniqueness**: TypeIds must be unique across all models (0-223 for user types).
* **Schema Evolution**: Adding fields is safe. Removing fields requires migration logic.
* **Synchronous by Default**: Most operations are sync. Use lazy boxes for large data.
* **No Relations**: Hive is NoSQL. Store object references (IDs) manually.
* **Close Boxes**: Always close boxes when no longer needed to free resources.
* **Backup Key**: For encrypted boxes, ALWAYS backup the encryption key securely.
