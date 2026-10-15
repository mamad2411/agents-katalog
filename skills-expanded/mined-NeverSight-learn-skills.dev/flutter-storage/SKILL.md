---
name: flutter-storage
description: "Almacenamiento local en Flutter. Cubre SQLite con Drift (ORM), SharedPreferences para key-value, flutter_secure_storage para tokens, y Hive para datos no relacionales. Actívala al implementar persistencia offline, guardar preferencias, o almacenar datos sensibles."
---

# Flutter Local Storage

Guía de almacenamiento local. SQLite con Drift, key-value, secure storage.

---

## Decisión

| Necesidad | Herramienta |
|-----------|-------------|
| Datos relacionales (tablas, queries) | **Drift** (SQLite) |
| Preferencias simples (tema, idioma) | **SharedPreferences** |
| Tokens, passwords | **flutter_secure_storage** |
| Datos no relacionales, caché | **Hive** |

---

## Drift (SQLite)

```bash
flutter pub add drift sqlite3_flutter_libs
flutter pub add --dev drift_dev build_runner
```

```dart
// modules/orders/data/local_database.dart
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'dart:io';

part 'local_database.g.dart';  // Generado

// Tabla
class Orders extends Table {
  TextColumn get id => text()();
  IntColumn get orderNumber => integer()();
  TextColumn get customerId => text()();
  TextColumn get status => text()();
  RealColumn get totalAmount => real()();
  TextColumn get currency => text()();
  DateTimeColumn get createdAt => dateTime()();

  @override
  Set<Column> get primaryKey => {id};
}

@DriftDatabase(tables: [Orders])
class LocalDatabase extends _$LocalDatabase {
  LocalDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  // ✅ Queries tipadas
  Future<List<Order>> getByCustomer(String customerId) {
    return (select(orders)
      ..where((t) => t.customerId.equals(customerId))
      ..orderBy([(t) => OrderingTerm.desc(t.createdAt)]))
      .get();
  }

  Future<void> upsertOrders(List<Order> orderList) {
    return batch((batch) {
      for (final order in orderList) {
        batch.insert(orders, order.toCompanion(), mode: InsertMode.insertOrReplace);
      }
    });
  }

  Future<void> deleteByCustomer(String customerId) {
    return (delete(orders)..where((t) => t.customerId.equals(customerId))).go();
  }
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'miapp.sqlite'));
    return NativeDatabase(file);
  });
}

// Provider
@riverpod
LocalDatabase localDatabase(LocalDatabaseRef ref) {
  return LocalDatabase();
}
```

---

## SharedPreferences

```dart
// Preferencias de usuario (tema, idioma, columnas visibles)
final prefs = await SharedPreferences.getInstance();

// Escribir
await prefs.setString('theme', 'dark');
await prefs.setBool('notifications', true);
await prefs.setInt('selectedTab', 0);
await prefs.setStringList('visibleColumns', ['orderNumber', 'status', 'total']);

// Leer
final theme = prefs.getString('theme') ?? 'light';
final notifications = prefs.getBool('notifications') ?? false;
```

---

## flutter_secure_storage (tokens)

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = const FlutterSecureStorage();

// Guardar token (encriptado en Keychain/KeyStore)
await storage.write(key: 'access_token', value: token);
await storage.write(key: 'refresh_token', value: refreshToken);

// Leer
final token = await storage.read(key: 'access_token');

// Eliminar (logout)
await storage.deleteAll();
```

---

## Hive (datos no relacionales)

```dart
// Para caché de objetos complejos o datos no relacionales
@HiveType(typeId: 0)
class OrderCache extends HiveObject {
  @HiveField(0)
  final String id;
  @HiveField(1)
  final Map<String, dynamic> data;

  OrderCache({required this.id, required this.data});
}

final box = await Hive.openBox<OrderCache>('order_cache');
box.put(order.id, OrderCache(id: order.id, data: order.toJson()));
final cached = box.get(orderId);
```

---

## Offline-first strategy

```dart
@riverpod
Future<List<Order>> orderList(OrderListRef ref, {required String customerId}) async {
  final localDb = ref.watch(localDatabaseProvider);
  final remoteRepo = ref.watch(orderRepositoryProvider);

  try {
    // 1. Traer del servidor
    final orders = await remoteRepo.getByCustomer(customerId);

    // 2. Guardar localmente
    await localDb.deleteByCustomer(customerId);
    await localDb.upsertOrders(orders);

    return orders;
  } catch (_) {
    // 3. Si no hay red, servir de caché local
    return localDb.getByCustomer(customerId);
  }
}
```

---

## Checklist storage

- [ ] Drift para datos relacionales (tablas, queries, migraciones)
- [ ] SharedPreferences para preferencias de UI
- [ ] flutter_secure_storage para tokens y datos sensibles
- [ ] Offline-first: escribir a local después de fetch, leer de local si no hay red
- [ ] Migraciones de Drift versionadas
- [ ] Sin guardar datos sensibles en SharedPreferences o Hive
