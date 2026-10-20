---
name: resource-provider-registry
description: Spring DI plugin registry where @Component implementations of a typed interface are auto-discovered and looked up at runtime by a string type key
triggers:
  - plugin registry
  - provider lookup by type
  - auto-discovered handlers
  - resource provider pattern
scope: user
source_project: lucida-domain-sms
version: 0.1.0-draft
tags: [spring, plugin, registry, interface, component]
category: arch
---

# Resource Provider Registry

## Problem
A domain needs to support multiple pluggable handler types (e.g. different resource categories) without hardcoding dispatch logic. New types must be addable without modifying the dispatcher, and each handler must be retrievable at runtime by a stable string key.

## Pattern
- Define a `ResourceProvider` interface with `String getResourceType()` (the key) plus domain-specific methods.
- Each variant is a `@Component` class implementing the interface. Spring auto-discovers all implementations.
- A cache/registry component (`@Component ResourceProviderCacheProcessor`) receives `List<ResourceProvider>` injected by Spring and builds a `Map<String, ResourceProvider>` at startup (`@PostConstruct`).
- Callers look up `providerMap.get(resourceType)` — no `if/else` chains needed.
- Default methods on the interface supply sensible fallbacks so implementors only override what differs.

## Example (sanitized)

```java
// Interface
public interface ResourceProvider {
    String getResourceType();   // lookup key, e.g. "domain.Widget"
    int getOrder();
    String getDisplayKey();
    boolean hasAvailability();
    Set<MeasurementDefinition> getMeasurementDefinitions();
    Map<String, ConfigurationDefinition> getConfigurationDefinitions();

    // default behaviour — override only when needed
    default boolean isMonitoring() { return true; }
    default boolean isAcl()        { return false; }
}

// One concrete provider
@Component
public class WidgetProvider implements ResourceProvider {
    public static final String PROVIDER_KEY = "domain.Widget";

    @Override public String getResourceType() { return PROVIDER_KEY; }
    @Override public int getOrder()           { return 5; }
    // ... implement domain methods
}

// Registry built at startup
@Component
public class ResourceProviderCacheProcessor {
    private final Map<String, ResourceProvider> providerMap = new ConcurrentHashMap<>();
    private final List<ResourceProvider> providers;

    public ResourceProviderCacheProcessor(List<ResourceProvider> providers) {
        this.providers = providers;
    }

    @PostConstruct
    public void init() {
        for (ResourceProvider p : providers) {
            providerMap.put(p.getResourceType(), p);
            // also populate static helper caches here if needed
        }
    }

    public ResourceProvider getProvider(String resourceType) {
        return providerMap.get(resourceType);
    }
}
```

## When to Use
- The set of handler types is open-ended or grows over releases.
- Dispatch logic would otherwise require a long `if/else` or `switch` on a type string.
- Each handler has meaningfully different behaviour (not just data differences).
- You want to add a new type by adding one class with no changes to dispatcher code.

## Pitfalls
- **Key collisions**: two providers returning the same `getResourceType()` string silently overwrite each other in the map. Add a duplicate-key check in `@PostConstruct`.
- **Circular dependencies**: if a provider injects the registry and the registry injects all providers, you get a cycle. Use `@Lazy` or a separate lookup service.
- **Interface bloat**: resist adding every domain concern to the interface. Use default methods or sub-interfaces for optional capabilities.
- **Static vs instance**: the registry is an instance bean; avoid exposing static accessors on it unless read performance is critical (see `definition-registry-helper-cache`).

## Related
- `definition-registry-helper-cache` — for static zero-allocation lookups populated from this registry at startup.
