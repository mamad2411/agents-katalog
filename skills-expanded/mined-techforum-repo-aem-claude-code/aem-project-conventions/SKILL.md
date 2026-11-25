---
name: aem-project-conventions
description: Always-loaded AEM project conventions — naming patterns, package structure, utility library usage, and team-specific standards that Claude applies silently on every task
user-invocable: false
---

## Package naming

- Java packages follow `com.<org>.<project>.<module>` — e.g. `com.example.mysite.core.models`
- OSGi component classes: suffix `Impl` on implementation classes (`ProductModelImpl`)
- OSGi service interfaces: no suffix (`ProductService`)
- Servlets: suffix `Servlet` (`ProductFeedServlet`)
- Schedulers: suffix `Scheduler` (`CacheWarmupScheduler`)
- Workflow steps: suffix `Process` (`AssetIngestionProcess`)

## Sling Model conventions

- Always annotate with `@Model(adaptables = {Resource.class, SlingHttpServletRequest.class}, defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)`
- Use `@ValueMapValue` for dialog properties, not `@Inject` for JCR-backed fields
- Expose only what HTL needs — keep getters minimal and named after what they return, not how they work
- `@PostConstruct` must be fast — no JCR queries, no remote calls, no blocking I/O

## HTL conventions

- Use `data-sly-use.model` to bind the Sling Model; name the variable `model`
- Apply output context explicitly: `${model.title @ context='text'}`, `${model.linkUrl @ context='uri'}`
- Never use `context='unsafe'`
- Component root element must carry the `data-sly-use` and `data-sly-test` guard in one element

## OSGi service conventions

- Define a `@interface` annotation for every OSGi config (metatype)
- Name the config interface nested inside the `Impl` class or in a `config` sub-package
- Place `*.cfg.json` files in `ui.config/src/main/content/jcr_root/apps/<project>/osgiconfig/config/`
- Runmode-specific configs: `config.author/`, `config.publish/`, `config.dev/`

## Logging

- Always inject `private static final Logger log = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());`
- Use parameterized logging: `log.debug("Processing resource: {}", resource.getPath());`
- Log at `debug` for per-request traces, `info` for significant lifecycle events, `warn`/`error` for recoverable/unrecoverable failures

## Test conventions

- Unit tests mirror source package under `core/src/test/java/`
- Test class name: `<ClassName>Test` (not `<ClassName>Tests`)
- Use AEM Mocks (`io.wcm.testing.mock.aem`) and `MockitoExtension`
- Every Sling Model must have a unit test covering null inputs and the main happy path

## Dependency guidelines

- Internal utility libraries are in `core/src/main/java/com/<org>/<project>/core/util/`
- Do not reach into another module's source — use OSGi services for cross-module communication
- Avoid adding net-new Maven dependencies without confirming they are in the approved BOM
