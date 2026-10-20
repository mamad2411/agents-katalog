---
name: definition-registry-helper-cache
description: Static helper class with ConcurrentHashMap caches populated at startup by @PostConstruct providers, enabling zero-allocation hot-path lookups via static getters
triggers:
  - static helper cache
  - ConcurrentHashMap static cache
  - PostConstruct populate static map
  - definition helper lookup
  - zero allocation hot path cache
scope: user
source_project: lucida-domain-sms
version: 0.1.0-draft
tags: [spring, cache, static, concurrenthashmap, performance]
category: arch
---

# Definition Registry Helper Cache

## Problem
Domain definition objects (measurement definitions, configuration definitions, OID-to-provider mappings) are immutable after startup and queried on every inbound data message. Fetching them through Spring beans on each call adds unnecessary allocation and indirection. A static helper with pre-built maps provides O(1) lookups with no object allocation in hot paths.

## Pattern
- A non-instantiable utility class holds `private static Map<K, V>` fields backed by `ConcurrentHashMap`.
- Spring `@Component` providers call static `addXxx(key, value)` mutators inside their `@PostConstruct` methods to populate the maps once at startup.
- All reads go through `public static V getXxx(K key)` — no Spring context access required at call time.
- A `private` constructor prevents instantiation.
- Supporting state (reference sets for runtime context like OS type, filesystem names) can also live here, written by data-processing code and read by providers.

## Example (sanitized)

```java
// Static helper class
@Slf4j
public class DomainDefinitionHelper {

    // OID -> provider class name
    private static final Map<String, String> providerByOid = new ConcurrentHashMap<>();

    // resourceType -> { configKey -> ConfigurationDefinition }
    private static final Map<String, Map<String, ConfigurationDefinition>> configDefByType =
        new ConcurrentHashMap<>();

    // definitionId -> MeasurementDefinition
    private static final Map<String, MeasurementDefinition> measurementDefById =
        new ConcurrentHashMap<>();

    // runtime reference data: "orgId_agentId_osType" -> Set<String>
    private static final Map<String, Set<String>> referenceInfo = new ConcurrentHashMap<>();

    private DomainDefinitionHelper() {}  // non-instantiable

    // --- Write (called from @PostConstruct) ---

    public static void addProviderOid(String oid, String providerName) {
        providerByOid.put(oid, providerName);
    }

    public static void addConfigDef(String resourceType,
                                     Map<String, ConfigurationDefinition> defs) {
        configDefByType.put(resourceType, defs);
    }

    public static void addMeasurementDefs(Set<MeasurementDefinition> defs) {
        for (MeasurementDefinition d : defs) {
            measurementDefById.put(d.getResourceType() + "_" + d.getProtocolInfo(), d);
        }
    }

    // --- Read (called in hot paths) ---

    public static String getProviderNameByOid(String oid) {
        return providerByOid.get(oid);
    }

    public static Map<String, ConfigurationDefinition> getConfigDefByType(String resourceType) {
        return configDefByType.get(resourceType);
    }

    public static MeasurementDefinition getMeasurementDef(String definitionKey) {
        return measurementDefById.get(definitionKey);
    }

    // --- Runtime reference data helpers ---

    public static void addReferenceInfo(String key, String value, boolean overwrite) {
        if (overwrite || !referenceInfo.containsKey(key)) {
            Set<String> set = new HashSet<>();
            set.add(value);
            referenceInfo.put(key, set);
        } else {
            referenceInfo.get(key).add(value);
        }
    }

    public static Set<String> getReferenceInfo(String key) {
        return referenceInfo.get(key);
    }

    public static String getFirstReferenceInfo(String key) {
        Set<String> set = referenceInfo.get(key);
        return (set == null || set.isEmpty()) ? null : set.iterator().next();
    }
}

// Provider that populates the cache at startup
@Component
public class WidgetProvider implements ResourceProvider {

    @PostConstruct
    public void registerDefinitions() {
        DomainDefinitionHelper.addProviderOid("4.99.1.0", getClass().getSimpleName());
        DomainDefinitionHelper.addConfigDef(getResourceType(), getConfigurationDefinitions());
        DomainDefinitionHelper.addMeasurementDefs(getMeasurementDefinitions());
    }

    // ... ResourceProvider implementation
}
```

## When to Use
- Definition data is fully known at startup and never changes during the process lifetime.
- The same lookup is invoked on every inbound message (high-frequency hot path).
- You want to avoid injecting a registry bean into every class that needs a definition lookup.

## Pitfalls
- **Write-after-startup**: static maps are effectively singletons. Any write after `@PostConstruct` completes (except to the runtime reference-data section) is a bug — mutating them concurrently with reads risks inconsistency.
- **Test isolation**: static state persists across test cases in the same JVM. Clear or re-populate maps in `@BeforeEach` / `@AfterEach` when unit testing consumers of this helper.
- **Circular startup ordering**: if two providers depend on each other's definitions being present at `@PostConstruct` time, you get an ordering hazard. Use an `ApplicationReadyEvent` listener to populate if ordering matters.
- **`null` returns**: callers must handle `null` from `getXxx()` gracefully — a missing key means the definition was never registered, not that the entity is absent.

## Related
- `resource-provider-registry` — the `@Component` providers that call the static `addXxx` mutators in their `@PostConstruct`.
