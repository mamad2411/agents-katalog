---
name: drift-persistence
description: Local database patterns for this Flutter project — drift with sqlcipher, schema definition, DAOs, migrations, watch queries, and repository integration. Load whenever writing or editing a table, DAO, or migration.
---

# drift + sqlcipher

Encrypted SQLite with a type-safe Dart query API. Schema and DAOs are colocated per feature unless a table is genuinely shared.

## Setup

```dart
// core/database/app_database.dart
@DriftDatabase(tables: [Activities, Users, Goals], daos: [ActivityDao, UserDao, GoalDao])
class AppDatabase extends _$AppDatabase {
  AppDatabase(QueryExecutor executor) : super(executor);

  @override
  int get schemaVersion => 3;

  @override
  MigrationStrategy get migration => MigrationStrategy(
        onCreate: (m) => m.createAll(),
        onUpgrade: (m, from, to) async {
          if (from < 2) await m.addColumn(activities, activities.lastSyncedAt);
          if (from < 3) await m.createIndex(Index('idx_activities_user',
              'CREATE INDEX idx_activities_user ON activities(user_id)'));
        },
      );
}
```

```dart
// core/database/executor.dart
QueryExecutor openConnection({required String passphrase}) {
  return LazyDatabase(() async {
    final dir = await getApplicationDocumentsDirectory();
    final file = File(p.join(dir.path, 'app.db'));
    return NativeDatabase.createInBackground(
      file,
      setup: (raw) => raw.execute("PRAGMA key = '$passphrase';"),
    );
  });
}
```

- `sqlcipher_flutter_libs` provides both SQLite and encryption. **Don't** also include `sqlite3_flutter_libs` — they conflict.
- The passphrase lives in `flutter_secure_storage`. Generate on first launch with `crypto.Random.secure()` + base64.
- `NativeDatabase.createInBackground` to keep opens off the UI isolate.

## Tables

Prefer per-feature table definitions; register them with the central `AppDatabase`.

```dart
// feature/activity/data/local/activities_table.dart
class Activities extends Table {
  TextColumn get id => text()();
  TextColumn get title => text()();
  TextColumn get kind => textEnum<ActivityKindRow>()();
  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get lastSyncedAt => dateTime().nullable()();

  @override
  Set<Column> get primaryKey => {id};
}
```

Rules:
- Column names: `snake_case` (drift generates them from the getter name, but you can override via `.named('...')`).
- **Store enums as text**, not as int. Enum ordering is a migration hazard.
- **DateTimes as `dateTime()`** — drift stores ISO-8601, safe across timezones if you always write UTC (`DateTime.now().toUtc()`).
- Indexes: declare in migration or via `@DataClassName` annotations. Don't skip them — unindexed `WHERE` on millions of rows is slow even with encryption.

## DAOs

```dart
// feature/activity/data/local/activity_dao.dart
@DriftAccessor(tables: [Activities])
class ActivityDao extends DatabaseAccessor<AppDatabase> with _$ActivityDaoMixin {
  ActivityDao(super.db);

  Future<ActivityRow?> getActivity(String id) =>
      (select(activities)..where((t) => t.id.equals(id))).getSingleOrNull();

  Stream<ActivityRow?> watchActivity(String id) =>
      (select(activities)..where((t) => t.id.equals(id))).watchSingleOrNull();

  Future<void> upsert(ActivityRow row) =>
      into(activities).insertOnConflictUpdate(row);

  Future<int> purgeStale(DateTime before) =>
      (delete(activities)..where((t) => t.lastSyncedAt.isSmallerThanValue(before))).go();
}
```

Rules:
- One DAO per feature/table-cluster. Don't have a god-DAO.
- Return drift's row types from DAOs; map to domain entities in the repository, not the DAO.
- `watch*` queries are cheap and first-class. Repositories that expose `Stream<Either<Failure, T>>` usually drive them from `watch`.

## Migrations

- Bump `schemaVersion` with every schema change. Never edit a past migration; always add a new step.
- Write a **schema-roundtrip test**: open a DB at version N, then upgrade to N+1, then assert the new column / index exists. Drift's `drift_dev schema dump` + `drift_dev schema generate` makes this straightforward — commit the schema snapshots under `drift_schemas/`.
- Destructive migrations (drop column, rename table) need a data copy into a new table, then rename. Don't skip it for "low-risk" columns.

## Repository + drift + remote

```dart
@override
Stream<Either<Failure, Activity>> watchActivity(String id) => _dao
    .watchActivity(id)
    .map((row) => row == null
        ? Left(const NotFoundFailure(message: 'no local record'))
        : Right(row.toDomain()));

@override
Future<Either<Failure, Activity>> refreshActivity(String id) async {
  final result = await handleApiCall(() => _api.getActivity(id: id), map: (d) => d.toDomain());
  return result.match(
    (failure) => Left(failure),
    (activity) async {
      await _dao.upsert(activity.toRow());
      return Right(activity);
    },
  );
}
```

- Reads can be offline-first (stream from drift, trigger a refresh in the background).
- Writes are optimistic or remote-first, your call per feature — but be consistent within a feature.
- **Don't** wrap drift exceptions as `NetworkFailure`; they're `CacheFailure`. Map them in the repo.

## Test seams

- Use `NativeDatabase.memory()` for unit tests — fast, isolated, no files.
- Inject an `AppDatabase` into repositories, not a DAO globally — makes fakes trivial.
- Seed data via helper builders; don't write SQL fixtures.

## Don'ts

- Raw SQL scattered across the app. Use drift's DSL; it's type-safe.
- DAO methods returning `dynamic` or `Map<String, Object?>`. Always row types.
- Long-running transactions on the UI thread. Drift's background executor covers this by default; don't block it.
- Storing secrets in drift. `flutter_secure_storage` exists for a reason.
- Skipping migrations because "dev only". Migrations are cheap to add and expensive to add later.
