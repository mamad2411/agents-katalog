---
name: mobile-data-persistence
description: >
  Choose, design, and review local data storage in mobile apps — key-value stores,
  SQL databases, NoSQL, file storage, secure storage, and sync strategies across
  Flutter (Hive, Isar, Drift, SharedPreferences), Android (Room, DataStore, SharedPreferences),
  and iOS (Core Data, SwiftData, UserDefaults, Keychain).
  TRIGGER when: user says /mobile-data-persistence, asks about local storage in a mobile app,
  needs to choose a persistence solution, or wants to review data layer design.
argument-hint: "[data storage need or feature]"
user-invocable: true
---

# Mobile Data Persistence

You are a senior mobile engineer. Help the user choose, design, or review local data persistence strategies with platform-specific guidance.

## Process

### Step 1: Understand Storage Requirements

| Question | Why It Matters |
|----------|---------------|
| What kind of data? (settings, cached API data, user-generated content, auth tokens) | Determines storage type |
| How much data? (KB, MB, GB) | Determines storage engine |
| How is data queried? (key lookup, filtered lists, full-text search, joins) | Determines SQL vs. NoSQL vs. key-value |
| Does data need to survive app uninstall? | Cloud backup vs. local-only |
| Is data sensitive? (tokens, PII, financial) | Requires secure/encrypted storage |
| Does data need to sync with a server? | Sync and conflict resolution strategy |
| What is the read/write ratio? | Optimization focus |

### Step 2: Choose Storage Type

| Type | Use Case | Examples | Max Size |
|------|----------|---------|----------|
| **Key-value** | Settings, flags, small preferences | SharedPreferences, UserDefaults, DataStore | ~1 MB |
| **SQL database** | Structured data, relational queries, large datasets | Room, Core Data, Drift, SQLite | GBs |
| **NoSQL / document** | Flexible schemas, fast writes, object storage | Hive, Isar, Realm, SwiftData | GBs |
| **File storage** | Images, documents, large blobs, exports | File system, app sandbox | Device limit |
| **Secure storage** | Auth tokens, API keys, passwords, biometric data | Keychain, EncryptedSharedPreferences, flutter_secure_storage | KBs |
| **In-memory cache** | Temporary data, session state, computed values | LRU cache, HashMap, NSCache | ~100 MB |

### Step 3: Apply Platform-Specific Solutions

#### Flutter

| Solution | Type | Best For | Async | Reactive |
|----------|------|----------|-------|----------|
| **shared_preferences** | Key-value | Simple settings, flags, small strings | Yes | No |
| **Hive** | NoSQL (binary) | Fast read/write, type adapters, no native deps | Yes | Via Box listeners |
| **Isar** | NoSQL (embedded) | Large datasets, full-text search, complex queries | Yes | Yes (watch queries) |
| **Drift (moor)** | SQL (SQLite) | Relational data, complex queries, migrations | Yes | Yes (streams) |
| **sqflite** | SQL (SQLite) | Raw SQL, lightweight, no codegen | Yes | No |
| **ObjectBox** | NoSQL (object) | Fast CRUD, relations, sync-capable | Yes | Yes (streams) |
| **flutter_secure_storage** | Secure key-value | Auth tokens, API keys, secrets | Yes | No |
| **path_provider + File** | File | Images, documents, exports | Yes | No |
| **hydrated_bloc** | State persistence | Auto-persist BLoC state across restarts | Yes | Yes |

```dart
// shared_preferences — simple settings
final prefs = await SharedPreferences.getInstance();
await prefs.setString('theme', 'dark');
final theme = prefs.getString('theme') ?? 'light';

// Drift — reactive SQL database
@DriftDatabase(tables: [Products, Orders])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  Stream<List<Product>> watchAllProducts() =>
      select(products).watch();

  Future<void> insertProduct(ProductsCompanion product) =>
      into(products).insert(product);
}

// Hive — NoSQL with type adapters
@HiveType(typeId: 0)
class Product extends HiveObject {
  @HiveField(0)
  late String name;
  @HiveField(1)
  late double price;
}

final box = await Hive.openBox<Product>('products');
box.put('item1', Product()..name = 'Widget'..price = 9.99);

// flutter_secure_storage — secrets
final storage = FlutterSecureStorage();
await storage.write(key: 'auth_token', value: token);
final token = await storage.read(key: 'auth_token');

// Isar — full-text search
@collection
class Product {
  Id id = Isar.autoIncrement;
  @Index(type: IndexType.value)
  late String name;
  late double price;
}

final products = await isar.products
    .filter()
    .nameContains('widget')
    .sortByPrice()
    .findAll();
```

#### Android (Kotlin & Java)

| Solution | Type | Best For | Language | Reactive |
|----------|------|----------|----------|----------|
| **DataStore (Preferences)** | Key-value | Settings, flags (modern replacement for SharedPrefs) | Kotlin | Yes (Flow) |
| **DataStore (Proto)** | Typed key-value | Structured settings with schema | Kotlin | Yes (Flow) |
| **SharedPreferences** | Key-value | Simple settings (legacy, still widely used) | Java/Kotlin | No (but listeners exist) |
| **Room** | SQL (SQLite) | Relational data, complex queries, migrations | Java/Kotlin | Yes (Flow/LiveData/RxJava) |
| **SQLiteOpenHelper** | SQL (raw) | Direct SQLite access (legacy) | Java | No |
| **Realm** | NoSQL (object) | Fast CRUD, cross-platform sync | Java/Kotlin | Yes |
| **EncryptedSharedPreferences** | Secure key-value | Tokens, sensitive settings | Java/Kotlin | No |
| **Android Keystore** | Secure hardware | Cryptographic keys, biometric-gated secrets | Java/Kotlin | No |
| **File (internal/external)** | File | Images, documents, exports, cache | Java/Kotlin | No |

```kotlin
// DataStore — modern key-value (Kotlin)
val THEME_KEY = stringPreferencesKey("theme")

val themeFlow: Flow<String> = dataStore.data.map { prefs ->
    prefs[THEME_KEY] ?: "light"
}

suspend fun setTheme(theme: String) {
    dataStore.edit { prefs -> prefs[THEME_KEY] = theme }
}

// Room — reactive SQL database
@Entity
data class Product(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    val price: Double
)

@Dao
interface ProductDao {
    @Query("SELECT * FROM product ORDER BY name")
    fun watchAll(): Flow<List<Product>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(product: Product)
}

// EncryptedSharedPreferences — secure storage
val securePrefs = EncryptedSharedPreferences.create(
    "secure_prefs",
    masterKey,
    context,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
securePrefs.edit().putString("auth_token", token).apply()
```

```java
// SharedPreferences — legacy Java approach
SharedPreferences prefs = getSharedPreferences("settings", MODE_PRIVATE);
prefs.edit().putString("theme", "dark").apply();
String theme = prefs.getString("theme", "light");

// Room — Java with LiveData
@Dao
public interface ProductDao {
    @Query("SELECT * FROM product ORDER BY name")
    LiveData<List<Product>> watchAll();

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insert(Product product);
}

// SQLiteOpenHelper — raw legacy approach
public class DbHelper extends SQLiteOpenHelper {
    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE product (id INTEGER PRIMARY KEY, name TEXT, price REAL)");
    }
}
```

#### iOS (Swift & Objective-C)

| Solution | Type | Best For | Language | Reactive |
|----------|------|----------|----------|----------|
| **SwiftData** | ORM (SQLite) | Modern persistence, SwiftUI integration (iOS 17+) | Swift | Yes (@Query) |
| **Core Data** | ORM (SQLite) | Complex object graphs, migrations, iCloud sync | Swift/ObjC | Yes (NSFetchedResultsController) |
| **UserDefaults** | Key-value (plist) | Simple settings, flags, small values | Swift/ObjC | No (but KVO works) |
| **Keychain Services** | Secure storage | Auth tokens, passwords, certificates, API keys | Swift/ObjC | No |
| **SQLite (direct)** | SQL (raw) | Direct SQL, lightweight, GRDB.swift wrapper | Swift/ObjC | GRDB: Yes |
| **Realm** | NoSQL (object) | Fast CRUD, cross-platform, real-time sync | Swift/ObjC | Yes |
| **File Manager** | File | Documents, images, exports, cache | Swift/ObjC | No |
| **NSUbiquitousKeyValueStore** | Key-value (iCloud) | Small settings synced via iCloud | Swift/ObjC | No |
| **CloudKit** | Cloud database | User-generated content with iCloud sync | Swift | Yes |
| **PropertyListSerialization** | Plist file | Structured settings, legacy config | ObjC/Swift | No |
| **NSCoding / NSKeyedArchiver** | Binary archive | Object serialization (legacy) | ObjC/Swift | No |

```swift
// SwiftData (iOS 17+) — modern approach
@Model
class Product {
    var name: String
    var price: Double
    var createdAt: Date

    init(name: String, price: Double) {
        self.name = name
        self.price = price
        self.createdAt = .now
    }
}

// In SwiftUI View
@Query(sort: \Product.name) var products: [Product]

// Insert
modelContext.insert(Product(name: "Widget", price: 9.99))

// UserDefaults — simple settings
UserDefaults.standard.set("dark", forKey: "theme")
let theme = UserDefaults.standard.string(forKey: "theme") ?? "light"

// Keychain — secure storage (using wrapper)
let keychain = Keychain(service: "com.myapp")
try keychain.set(token, key: "auth_token")
let token = try keychain.get("auth_token")

// Core Data — Swift
let fetchRequest: NSFetchRequest<Product> = Product.fetchRequest()
fetchRequest.sortDescriptors = [NSSortDescriptor(keyPath: \Product.name, ascending: true)]
let controller = NSFetchedResultsController(
    fetchRequest: fetchRequest,
    managedObjectContext: context,
    sectionNameKeyPath: nil,
    cacheName: nil
)
```

```objc
// NSUserDefaults — Objective-C
[[NSUserDefaults standardUserDefaults] setObject:@"dark" forKey:@"theme"];
NSString *theme = [[NSUserDefaults standardUserDefaults] stringForKey:@"theme"] ?: @"light";

// Core Data — Objective-C
NSFetchRequest *request = [Product fetchRequest];
request.sortDescriptors = @[[NSSortDescriptor sortDescriptorWithKey:@"name" ascending:YES]];
NSArray<Product *> *products = [context executeFetchRequest:request error:nil];

// NSKeyedArchiver — legacy object persistence
NSData *data = [NSKeyedArchiver archivedDataWithRootObject:products
                                    requiringSecureCoding:YES
                                                   error:nil];
[data writeToFile:path atomically:YES];

// Keychain — Objective-C (Security framework)
NSDictionary *query = @{
    (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
    (__bridge id)kSecAttrAccount: @"auth_token",
    (__bridge id)kSecValueData: [token dataUsingEncoding:NSUTF8StringEncoding]
};
SecItemAdd((__bridge CFDictionaryRef)query, NULL);
```

### Step 4: Design the Data Layer

**Repository pattern (recommended for all platforms):**

```
UI ← ViewModel/BLoC ← Repository ← LocalDataSource (Room/CoreData/Drift)
                                  ← RemoteDataSource (API)
```

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Cache-aside** | App checks cache, fetches from network on miss | Simple caching, read-heavy |
| **Write-through** | Write to cache and network simultaneously | Data consistency critical |
| **Write-behind** | Write to cache immediately, sync to network async | Offline-first, write-heavy |
| **Refresh-ahead** | Proactively refresh cache before expiry | Predictable access patterns |

### Step 5: Handle Migrations

| Platform | Migration Tool | Strategy |
|----------|---------------|----------|
| **Flutter (Drift)** | Schema versioning + migration steps | Forward-only SQL migrations |
| **Flutter (Hive/Isar)** | Type adapter versioning | Schema-less, handle missing fields |
| **Android (Room)** | `Migration(fromVersion, toVersion)` | SQL ALTER statements |
| **iOS (Core Data)** | Lightweight migration (automatic) or mapping models | Prefer lightweight when possible |
| **iOS (SwiftData)** | `VersionedSchema` + `SchemaMigrationPlan` | Declarative migration stages |

**Migration rules:**
- Never delete columns in production — deprecate and ignore
- Always test migrations with real production-like data
- Support skipping versions (1 → 3, not just 1 → 2 → 3)
- Back up database before destructive migrations

### Step 6: Secure Sensitive Data

| Data Type | Storage | Platform Implementation |
|-----------|---------|------------------------|
| **Auth tokens** | Secure storage | Keychain (iOS), EncryptedSharedPrefs (Android), flutter_secure_storage |
| **API keys** | Secure storage or build config | Never hardcode in source |
| **User PII** | Encrypted database | SQLCipher, encrypted Room, encrypted Core Data |
| **Biometric-gated data** | Hardware-backed secure storage | Keychain + biometric policy (iOS), Keystore + BiometricPrompt (Android) |
| **Session data** | Memory only | Never persist session tokens to disk unencrypted |

## Output Format

```markdown
## Persistence Summary
- **Platform:** [Flutter / Android / iOS]
- **Data types:** [What data needs to be stored]
- **Solutions chosen:** [key-value, SQL, NoSQL, secure storage]

## Storage Architecture
[Data flow diagram: UI → Repository → Local/Remote sources]

## Schema Design
[Core entities, relationships, indexes]

## Migration Strategy
[How schema changes are handled]

## Security
[How sensitive data is protected]

## Sync Strategy (if applicable)
[How local data syncs with server]
```

## Quality Checklist

- [ ] Storage type matches data characteristics (don't use key-value for relational data)
- [ ] Sensitive data is in secure storage, not plain SharedPreferences/UserDefaults
- [ ] Database migrations are tested with production-like data
- [ ] Repository pattern isolates data source details from business logic
- [ ] Reactive queries are used where UI needs live updates
- [ ] Cache invalidation strategy is defined (TTL, explicit, event-based)
- [ ] Data is cleaned up on logout (tokens, cached PII)
- [ ] Storage size is monitored (especially on low-storage devices)

## Edge Cases

- SharedPreferences/UserDefaults are NOT encrypted — never store tokens or PII in them
- Core Data + iCloud sync has many edge cases (conflict resolution, account switching) — test thoroughly
- Room migrations that fail will destroy the database by default — always provide migration paths or use `fallbackToDestructiveMigration()` only in dev
- On Android, `MODE_WORLD_READABLE` SharedPreferences is deprecated and insecure — always use `MODE_PRIVATE`
- iOS Keychain items persist across app reinstalls by default — set `kSecAttrAccessible` appropriately
- For large binary files (images, videos), store the file on disk and keep only the path/reference in the database
- SQLite has a practical limit of ~1GB per database on mobile — shard or archive old data for larger datasets
