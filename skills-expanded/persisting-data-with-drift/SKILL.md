---
name: "persisting-data-with-drift"
description: "Implements type-safe reactive SQL persistence in Flutter using Drift v2.32 (formerly Moor) built on SQLite with automatic code generation. Activates when defining table schemas with Drift DSL, writing type-safe join or subquery operations, handling schema migrations with MigrationStrategy, using reactive watch() streams for live UI updates, implementing ACID transactions, defining foreign key constraints or cascade deletes, enabling WAL mode for write performance, troubleshooting generated .g.dart type mismatches, migrating from sqflite or sqlite3 v2 to v3, using DAOs for query separation, or building offline-first apps requiring strong relational data integrity and compile-time SQL verification."
metadata:
  last_modified: "2026-04-27 17:41:00 (GMT+8)"
---

# Drift SQL Database Guide

## Goal
Implement type-safe reactive SQL database using Drift (formerly Moor). Drift provides compile-time verified SQL queries, automatic migrations, and reactive streams built on SQLite.

## Process

### Phase 1: Install Dependencies

```yaml
dependencies:
  drift: ^2.35.4
  path_provider: ^2.1.6
  path: ^1.9.1

dev_dependencies:
  drift_dev: ^2.35.3
  build_runner: ^2.17.1
```

### Phase 2: Define Database Schema

```dart
import 'dart:io';

import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

part 'database.g.dart';

// Define tables
class Users extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text().withLength(min: 1, max: 50)();
  TextColumn get email => text().unique()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

class Todos extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get title => text()();
  BoolColumn get isCompleted => boolean().withDefault(const Constant(false))();
  IntColumn get userId => integer().references(Users, #id, onDelete: KeyAction.cascade)();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

@DriftDatabase(tables: [Users, Todos])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;
  
  // Queries
  Future<List<User>> getAllUsers() => select(users).get();
  Stream<List<User>> watchAllUsers() => select(users).watch();
  
  Future<User> getUserById(int id) =>
      (select(users)..where((u) => u.id.equals(id))).getSingle();
  
  Future<int> insertUser(UsersCompanion user) => into(users).insert(user);
  
  Future<bool> updateUser(User user) => update(users).replace(user);
  
  Future<int> deleteUser(int id) =>
      (delete(users)..where((u) => u.id.equals(id))).go();
}

// Open connection
LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'app.db'));
    return NativeDatabase(file);
  });
}
```

### Phase 3: Generate Code

```bash
dart run build_runner build
```

### Phase 4: Initialize Database

```dart
late AppDatabase database;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  database = AppDatabase();
  runApp(MyApp());
}
```

### Phase 5: CRUD Operations

**Insert**:
```dart
final userId = await database.insertUser(
  UsersCompanion.insert(
    name: 'John Doe',
    email: 'john@example.com',
  ),
);
```

**Query**:
```dart
// Simple query
final allUsers = await database.getAllUsers();

// With where clause
final activeUsers = await (database.select(database.users)
  ..where((u) => u.isActive.equals(true)))
  .get();

// Join query
final query = database.select(database.todos).join([
  leftOuterJoin(database.users, database.users.id.equalsExp(database.todos.userId)),
]);

final results = await query.get();
for (final row in results) {
  final todo = row.readTable(database.todos);
  final user = row.readTable(database.users);
  print('${todo.title} by ${user.name}');
}
```

**Update**:
```dart
await database.updateUser(
  user.copyWith(name: 'Jane Doe'),
);

// Or partial update
await (database.update(database.users)
  ..where((u) => u.id.equals(userId)))
  .write(UsersCompanion(name: Value('Jane')));
```

**Delete**:
```dart
await database.deleteUser(userId);
```

### Phase 6: Reactive Streams

```dart
// Watch changes
Stream<List<User>> watchUsers() {
  return database.select(database.users).watch();
}

// In widget
StreamBuilder<List<User>>(
  stream: database.watchAllUsers(),
  builder: (context, snapshot) {
    if (!snapshot.hasData) return CircularProgressIndicator();
    return ListView(
      children: snapshot.data!.map((u) => UserTile(u)).toList(),
    );
  },
)
```

### Phase 7: Migrations

```dart
@DriftDatabase(tables: [Users, Todos])
class AppDatabase extends _$AppDatabase {
  @override
  int get schemaVersion => 2;  // Increment version
  
  @override
  MigrationStrategy get migration => MigrationStrategy(
    onCreate: (Migrator m) async {
      await m.createAll();
    },
    onUpgrade: (Migrator m, int from, int to) async {
      if (from == 1) {
        // Add new column
        await m.addColumn(users, users.phoneNumber);
      }
    },
  );
}
```

### Phase 8: Transactions

```dart
await database.transaction(() async {
  final userId = await database.insertUser(userCompanion);
  await database.into(database.todos).insert(
    TodosCompanion.insert(
      title: 'First todo',
      userId: userId,
    ),
  );
});
```

---

## Drift 2.32+ Migration & Performance

### ⚠️ Breaking Changes in Drift 2.32

**Migrated to sqlite3 package v3.x:**
- Web apps **must update** `sqlite3.wasm` file in `web/` directory
- Encrypted databases need PRAGMA adjustments
- Native platforms: `drift_flutter` already depends on the `sqlite3_flutter_libs` placeholder (EOL). Do not add it yourself.

**Migration checklist:**
```yaml
dependencies:
  drift: ^2.35.4
  drift_flutter: ^0.3.1  # brings in the sqlite3 3.x native setup
```

### WAL Mode Performance Optimization

**Enable Write-Ahead Logging for 10x better write performance:**

```dart
LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'app.db'));

    // NativeDatabase has no customStatement; run PRAGMAs in the setup callback
    return NativeDatabase(file, setup: (rawDb) {
      rawDb.execute('PRAGMA journal_mode=WAL;');
    });
  });
}
```

**WAL Mode Benefits:**
- ✅ Concurrent reads while writing
- ✅ ~10x better write performance
- ✅ Reduced I/O blocking
- ✅ Better crash recovery

**⚠️ WAL Mode Caveats:**
- WAL file can grow large over time
- Run periodic checkpoints in production:
  ```dart
  // Run checkpoint every app launch or periodically
  await database.customStatement('PRAGMA wal_checkpoint(TRUNCATE);');
  ```
- Not suitable for network-mounted filesystems
- Monitor WAL file size in production apps

### Type Safety Best Practices

**⚠️ NEVER manually edit generated files (`*.g.dart`)**

**ALWAYS follow this workflow:**
1. Update table definitions in `.dart` or `.drift` files
2. Run code generator:
   ```bash
   dart run build_runner build
   ```
3. Review generated code for warnings
4. Test migrations thoroughly in development
5. Commit both source and generated files

**Common type safety errors:**
```dart
// ❌ Wrong - nullable/non-nullable mismatch
TextColumn get name => text().nullable()();
final user = UsersCompanion.insert(name: null);  // Type error

// ✅ Correct - use Value wrapper for nullable updates
await database.update(users).replace(
  user.copyWith(name: Value(newName)),  // or Value.absent()
);
```

### Common Errors & Solutions

**Error: "Table X doesn't exist in the database"**
- ✅ Increment `schemaVersion` and add migration
- ✅ Rerun build_runner after schema changes
- ✅ Clear app data or uninstall/reinstall during development

**Error: "column Y has no value"**
- ✅ Use `Companion.insert()` with required fields
- ✅ Add `.withDefault()` to column definition
- ✅ Provide default in migration when adding new column

**Error: "Nested transactions causing deadlocks"**
- ✅ Avoid calling `transaction()` inside another transaction
- ✅ Use single transaction for multi-step operations
- ✅ Check call stack for nested transaction patterns

**Error: "Type mismatch after migration"**
- ✅ Delete generated `.g.dart` files
- ✅ Run `build_runner clean` then rebuild
- ✅ Verify column types match between old/new schema

**Performance issues with watch() streams:**
- ✅ Enable WAL mode (see above)
- ✅ Use indexes on frequently queried columns
- ✅ Limit watch() to visible data only
- ✅ Dispose streams when widgets unmount

---

## Constraints

* **Type Safety**: All queries are type-checked at compile time.
* **Schema Migrations**: Always increment `schemaVersion` when changing schema.
* **Async Operations**: All database operations are async.
* **Close Database**: Call `database.close()` when app terminates.
* **Unique TypeIds**: Drift table names must be unique.
* **Foreign Keys**: Enable foreign key constraints in SQLite configuration.
* **Generated Files**: Never manually edit `*.g.dart` files - always regenerate with build_runner.
* **WAL Mode**: Enable for production apps but monitor WAL file size and run periodic checkpoints.
