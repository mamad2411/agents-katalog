---
name: paper-softdepend-hook
description: "安全使用第三方軟依賴（Vault、PlaceholderAPI、packetevents）：softdepend 宣告、isPluginEnabled 先檢查再建構、Hook + Bridge 分離、避開 Bukkit 監聽器簽名陷阱、接 LinkageError、Vault 消費端／提供端、PlaceholderAPI expansion 快照 / Safe soft dependencies on third-party plugins with Hook + Bridge split and class-load boundary tests"
---

# Paper Softdepend Hook

## Skill Name

`paper-softdepend-hook`

## Purpose

Let a plugin gain extra features when a third-party plugin (Vault, PlaceholderAPI, packetevents, ...) **is installed**, and still start normally when it **is not**.
This is the third-party counterpart of [`paper-service-api`](../paper-service-api/SKILL.md) (which covers your own plugins): the difference is that third-party types are **not in your jar**, so when the plugin is missing, the JVM throws `NoClassDefFoundError` as soon as it loads any class that references them.

The solution is a three-layer split:

1. **Hook**: contains no third-party types at all (no fields, no method signatures, no method bodies; it only calls the Bridge's static factory), so it can always be loaded safely. It does the `isPluginEnabled` check, catches `LinkageError`, warns once, and degrades.
2. **Bridge**: the **only** class that touches third-party types, and it is only touched after the check passes.
3. **Your own interface (Port)**: the interface the Bridge implements and the rest of the code depends on. It contains only JDK/Paper types, so business code never knows the third party exists.

## Paper Version Requirements

- Paper 1.21.11 / 26.3 (identical on both versions, no version-specific lines)
- Pure Paper API; soft dependencies are obtained via `compileOnly`: VaultAPI 1.7.1, PlaceholderAPI 2.11.6, packetevents-spigot 2.13.0
- Paperweight is not required
- **Spigot**: Core portable — Vault and PlaceholderAPI support Spigot; replace Adventure messages

## Triggers

- 「軟依賴」「softdepend」「soft dependency」「Hook」「Bridge」
- 「Vault」「經濟插件」「Economy provider」「PlaceholderAPI」「expansion」「packetevents」
- 「NoClassDefFoundError」「Failed to register events for class」「監聽器沒註冊」
- 「沒裝某插件也要能啟動」「optional plugin integration」

## Inputs

| Parameter | Example | Description |
|------|------|------|
| `dependency` | `Vault` | The third-party plugin's `plugin.yml name` (case must match exactly) |
| `integration_package` | `com.example.market.integration` | Package containing the Hook/Bridge/Port |
| `role` | `consumer` / `provider` / `expansion` / `packet` | Consume (Vault balance lookup), provide (register an Economy), PAPI placeholders, packet listening |
| `port_name` | `MoneyPort` | Name of your own interface (JDK/Paper types only) |
| `required` | `false` | `false` -> `softdepend`; `true` -> use `depend` instead (the plugin will not start without it, and this skill is not needed) |

## Outputs

- `softdepend` in `plugin.yml` and the `compileOnly` dependencies
- `MoneyPort.java`, `NoMoney.java` — your own interface and its no-op implementation for when the dependency is absent
- `VaultHook.java` / `VaultBridge.java` — Vault consumer (balance lookup, withdrawal, formatting)
- `LedgerPort.java` / `LedgerEconomy.java` / `VaultProviderBridge.java` — optional: provider side that registers your own `Economy`
- `SnapshotPublisher.java` / `PlaceholderSnapshot.java` / `MarketExpansion.java` / `PapiHook.java` / `PapiBridge.java` — PlaceholderAPI expansion
- `JoinListener.java` — demonstrates a listener that never touches soft-dependency types
- `MarketPlugin.java` — enable order and disable cleanup
- Boundary test (`examples.md`): reflectively load the Hook on a classpath without the dependency

## Build Setup

See [`references/paper-api-platform.md`](references/paper-api-platform.md). Soft dependencies are always `compileOnly` and **must not be shaded into the jar**:

```groovy
dependencies {
    compileOnly 'io.papermc.paper:paper-api:26.3.build.258-stable'
    compileOnly('com.github.MilkBowl:VaultAPI:1.7.1') { exclude group: 'org.bukkit' }
    compileOnly 'me.clip:placeholderapi:2.11.6'
    compileOnly 'com.github.retrooper:packetevents-spigot:2.13.0'
}
```

`plugin.yml` (the name must match the other plugin's `name` exactly, including case; `packetevents` is lowercase):

```yaml
name: Market
main: com.example.market.MarketPlugin
api-version: '26.3'
softdepend: [Vault, PlaceholderAPI, packetevents]
```

`softdepend` only guarantees "if the other plugin exists, it is enabled before this plugin". It does **not guarantee it exists**, nor that the economy plugin behind Vault has registered its service.

## Code Template

The full source lives in [`template.md`](template.md) (about 800 lines, compiled against Paper 1.21.11 and 26.3 in CI). **Read `template.md` before writing any code for this skill**, and copy from it instead of rebuilding the classes from the table below.

| File | Package | Role |
|------|---------|------|
| `MoneyPort.java` | `.integration` | Your own money interface, JDK/Paper types only |
| `NoMoney.java` | `.integration` | No-op implementation when Vault is absent |
| `VaultBridge.java` | `.integration` | Only consumer-side class that touches Vault types |
| `VaultHook.java` | `.integration` | Consumer-side hook, no Vault types |
| `LedgerPort.java` | `.integration` | Optional provider side: your ledger interface |
| `LedgerEconomy.java` | `.integration` | Optional provider side: implements Vault `Economy` |
| `VaultProviderBridge.java` | `.integration` | Optional provider registration |
| `PlaceholderSnapshot.java` | `.integration` | Immutable placeholder snapshot |
| `SnapshotPublisher.java` | `.integration` | Publishes on the main thread, read from any thread |
| `MarketExpansion.java` | `.integration` | PlaceholderAPI expansion (bridge layer) |
| `PapiBridge.java` | `.integration` | Only class that registers with PlaceholderAPI |
| `PapiHook.java` | `.integration` | PlaceholderAPI hook, safe to load without it |
| `JoinListener.java` | `.integration` | Listener with no Vault types in member signatures |
| `MarketPlugin.java` | root | Enable order and cleanup |

### Core Rules

1. `isPluginEnabled(name)` comes **before** any code that would load third-party types (calling a Bridge static method, `new` on a Bridge).
2. The Hook's fields, method signatures, and lambda-captured variables must not contain third-party types; it holds only your own Port.
3. No class other than the Bridge may `import` a third-party package.
4. Every call into the Bridge is wrapped in `try { ... } catch (LinkageError e)`: on a version mismatch or load failure, degrade and **warn only once**.
5. A `Listener` class registered with Bukkit **must not** have a third-party type in any member signature (see "The Listener Trap" below).

### The Listener Trap (Bukkit's `registerEvents`)

`PluginManager.registerEvents(listener, plugin)` calls `getDeclaredMethods()` on the listener class, and the JVM must resolve the signature types of **all** declared methods (including the synthetic `lambda$xxx` methods generated for lambdas). If the parameter, return value, or captured variable of any one method is an uninstalled third-party type (including "your own class that implements a third-party interface"), a `NoClassDefFoundError` is thrown. Bukkit only prints one line to the console,
`Failed to register events for class X because Y does not exist`, and **the whole listener silently stops working**, even for unrelated events.

```text
// Wrong: announce takes a Vault type as a parameter, so when Vault is not installed the whole JoinListener fails to register
public final class JoinListener implements Listener {
    private void announce(Player p, Economy economy) { ... }   // <- third-party type in the signature
}
```

The correct approach: the Listener holds only **your own Port** (this skill's `MoneyPort`), and all third-party types stay in the Bridge.

### Applying This to packetevents

packetevents is the same Hook + Bridge pattern: the Hook holds an `Object listener` (not the `PacketListenerCommon` type), `install()` first checks `isPluginEnabled("packetevents")`, and the Bridge does `PacketEvents.getAPI().getEventManager().registerListener(...)`. Packet listeners run on the **Netty IO thread**, so likewise they only read an immutable snapshot and call no Bukkit API. See Example 2 in [`examples.md`](examples.md) for the full template.

## Recommended Directory Structure

```
src/main/java/com/example/market/
├── MarketPlugin.java                 ← Assembly: build Hooks, register Listener, cleanup in onDisable
└── integration/
    ├── MoneyPort.java                ← Own interface (business code depends only on this)
    ├── NoMoney.java
    ├── VaultHook.java                ← No third-party types, public
    ├── VaultBridge.java              ← Only consumer-side class touching Vault, package-private
    ├── LedgerPort.java / LedgerEconomy.java / VaultProviderBridge.java   ← Optional: provider side
    ├── PapiHook.java                 ← public
    ├── PapiBridge.java               ← package-private
    ├── MarketExpansion.java          ← Touches PlaceholderAPI, package-private
    ├── PlaceholderSnapshot.java
    ├── SnapshotPublisher.java
    └── JoinListener.java             ← Listener: no third-party types in signatures
src/test/java/com/example/market/
└── SoftDependBoundaryTest.java       ← The test classpath deliberately has no third-party jars
```

Keep the Bridge and Expansion package-private: they cannot be misused from outside the integration package.

## Thread Safety

- Vault `Economy` providers are mostly designed for the main thread and are not guaranteed thread-safe: call all `MoneyPort` methods **on the main thread only**, and state this in the Javadoc
- PlaceholderAPI's `onRequest` / `onPlaceholderRequest` **may run on any thread**: only read `SnapshotPublisher.current()`; calling the Bukkit API or Vault is forbidden
- The snapshot is rebuilt in full by the main thread (`runTaskTimer`) and swapped in through a `volatile` reference; the snapshot object never changes after construction (`Map.copyOf`)
- The packetevents listener runs on the Netty IO thread: likewise only read the immutable snapshot, and modify only a clone of a packet
- See [`references/paper-threading.md`](references/paper-threading.md)

## Fallback

| Error | Cause | Fix |
|------|------|------|
| `NoClassDefFoundError: net/milkbowl/vault/economy/Economy` | Vault is not installed, but some loaded class references a Vault type (fields, signatures, and bodies all count) | Only the Bridge touches third-party types; the Bridge is touched only after `isPluginEnabled` is true |
| `Failed to register events for class X because ... does not exist`, and events are never received | A Listener method signature (including lambda-captured variables) contains an uninstalled third-party type | The Listener holds only your own Port; reproduce it with the boundary test |
| Plugin startup order is wrong, Vault is not yet enabled | `softdepend` is not declared, or the name's case does not match | `softdepend: [Vault, PlaceholderAPI, packetevents]`, with names matching the other plugin's `name` exactly |
| `Economy` is null (Vault is installed) | Vault is only a bridge; the economy plugin has not registered yet or has been disabled | Call `getRegistration` again on every operation; use `MoneyPort.available()` to check, and do not cache `Economy` |
| Messages show `§a` or `&6` literally and colors are broken | The `Economy.format()` string was concatenated into MiniMessage | Convert to a Component with `LegacyComponentSerializer.legacySection()`, then use `Placeholder.component` |
| `NoSuchMethodError` / `AbstractMethodError` (third-party API version mismatch) | The version compiled against differs from the version on the server | The Hook catches `LinkageError`, degrades, and warns only once |
| PlaceholderAPI placeholders occasionally race or throw | `onRequest` called the Bukkit API off the main thread | Only read the snapshot; the main thread publishes data periodically |
| Placeholders vanish after `/papi reload` | `persist()` returns false, so the expansion is unregistered as if it were an external jar | `persist()` returns true, and call `unregister()` yourself in `onDisable` |
| `register()` returns false | The same identifier is already registered, or `canRegister()` returns false | Check for a duplicate identifier; implement external conditions in `canRegister()` |
| Exception on disable | The third-party plugin was disabled before this plugin | `uninstall()` catches `LinkageError \| RuntimeException`; logging at FINE is enough |
