# AGENTS.md

This file contains build commands and code style guidelines for the Meta Projects repository (Java/Maven multi-module).

## 项目现状

当前项目包含以下模块，其中部分模块已完成开发，部分仍在开发中：

### 已完成模块
- ✅ **meta-bom**: Maven依赖版本管理
- ✅ **meta-data**: 核心数据处理库 (187个测试)
- ✅ **meta-serial**: 序列化框架，SPI接口及多种实现
- ✅ **meta-logging**: 日志记录工具
- ✅ **meta-core**: 核心功能模块 (50个测试)
- ✅ **meta-extension**: SPI扩展机制 + Spring集成 (23个测试)
- ✅ **meta-validation**: 数据验证工具 (90个测试)

### 开发中模块
- ⚠️ **meta-data-ext**: 数据模型扩展
- ⚠️ **meta-remoting**: 远程调用模块

## Build Commands

### Build all modules
```bash
cd meta-bom && mvn clean install
```

### Build single module
```bash
cd <module-name> && mvn clean install
```

### Run all tests
```bash
cd meta-bom && mvn test
```

### Run single test class
```bash
cd <module-name> && mvn test -Dtest=ClassName
```

### Run single test method
```bash
cd <module-name> && mvn test -Dtest=ClassName#methodName
```

### Generate coverage report
```bash
cd meta-bom && mvn clean test jacoco:report
```

## Code Style Guidelines

### Package Structure
- Base package: `com.softmegatron.shared.meta`
- Module pattern: `com.softmegatron.shared.meta.{module}[.{submodule}].{type}`
- Type suffixes: `common`, `http`, `enums`, `model`, `constants`, `utils`, `exception`, `annotation`, `factory`, `loader`

### Import Order
1. Standard Java imports (java.*)
2. Third-party imports (org.apache.commons, okhttp3, com.google.guava, etc.)
3. Internal imports (com.softmegatron.shared.meta.*)
4. Static imports (`import static`)

Separate each group with a blank line.

### Naming Conventions
- Classes: PascalCase (`RemoteService`, `HttpRemoteServiceImpl`)
- Interfaces: PascalCase, descriptive of type (`RemoteService`, `BaseEnum`)
- Enums: PascalCase (`ExtensionScope`, `HttpMethod`)
- Interface constants: UPPER_SNAKE_CASE (`DEFAULT_CONN_TIMEOUT`)
- Class constants: UPPER_SNAKE_CASE (`EXTENSION_TYPE_CACHE`)
- Methods: camelCase (`invoke`, `getParams`)
- Variables/parameters: camelCase (`invocation`, `builder`)
- Packages: lowercase (`http`, `utils`, `common`)

### Class Structure
```java
package ...;

import ...;
import ...;

/**
 * 类描述
 *
 * @author <a href="mailto:wei.yan@softmegatron.com">wei.yan</a>
 * @version 1.0.0
 * @since 1.0.0
 */
public class ClassName extends BaseType {
    private static final long serialVersionUID = <generated>;
    private static final Logger LOGGER = LoggerFactory.getLogger(ClassName.class);

    // Static constants
    // Instance fields
    // Constructors
    // Public methods
    // Private methods
}
```

### Base Classes & Interfaces
- Models extend `BaseModel`
- Enums implement `BaseEnum` (requires `getDesc()`)
- Responses use `BaseResponse<T>` with Builder pattern
- Exceptions extend `RuntimeException`
- Serializable classes extend `BaseSerializable`

### Required Members
- Serializable classes: `private static final long serialVersionUID`
- Classes needing logging: `private static final Logger LOGGER = LoggerFactory.getLogger(ClassName.class)`
- Javadoc for all public/protected/package-private members

### Annotations
- SPI extension points: `@Spi("defaultKey")`
- Nullability: `@Nullable`, `@NotNull` (from JetBrains annotations)
- JUnit tests: `@Test`
- Validation: JSR-303 annotations (`@NotNull`, `@NotEmpty`, etc.)

### Generics
- Single uppercase letters: `<T>`, `<R>`, `<P>`, `<I>`
- Type bounds: `I extends RemoteInvocation, R extends RemoteResponse`

### Static Imports
Preferred for: constants, Preconditions (`checkNotNull`, `checkArgument`), time units (`MILLISECONDS`)

### Error Handling
- Custom exceptions extend `RuntimeException`
- Use `Preconditions.checkNotNull()` and `checkArgument()` for validation
- Log errors at ERROR level: `LOGGER.error("message", exception)`

### Validation
- Framework: JSR-303 Bean Validation (jakarta.validation)
- Use `@NotNull`, `@NotEmpty`, `@Size`, etc. annotations on fields
- Validate with `ValidatorUtils.validate()` or manual validator
- Validation failures throw `ViolationException`

### Testing
- Framework: JUnit 4.13.2 (Surefire 3.2.5)
- Test coverage: JaCoCo 0.8.12
- Test classes naming: `*Test.java`
- Test methods: `@Test public void testMethodName()`
- Assertion library: JUnit Assert
- Mock framework: Mockito (when needed)

### Code Quality
- Checkstyle: Use Sun and Google bundled checks
- Java version: Target 17
- Encoding: UTF-8
- Line endings: LF (Unix style)

### Current Module List
```
meta-bom/                        # ✅ 完成 - 依赖版本管理
meta-data/                       # ✅ 完成 - 数据处理基础类 (187个测试)
├── base/                        # 基础数据模型和接口
├── constants/                   # 常量定义
├── enums/                       # 枚举类型
├── serial/                      # 序列化相关工具
└── utils/                       # 数据处理工具类
meta-data-ext/                   # ⚠️ 开发中 - 数据模型扩展
meta-logging/                    # ✅ 完成 - 日志记录工具
meta-core/                       # ✅ 完成 - 核心功能模块 (50个测试)
├── pattern/holder/              # 单例模式
├── pattern/chain/               # 责任链模式
└── utils/                       # 工具类
meta-extension/                  # ✅ 完成 - SPI扩展机制 (23个测试)
├── meta-extension-core/         # 核心SPI机制 (13个测试)
│   ├── annotation/              # @Spi 注解
│   ├── enums/                   # ExtensionScope 枚举
│   ├── exception/               # ExtensionException
│   ├── factory/                 # ExtensionFactory 接口
│   └── loader/                  # ExtensionLoader/Manager
└── meta-extension-spring/       # Spring集成 (10个测试)
    ├── config/                  # 自动配置
    └── factory/                 # SpringExtensionFactory
meta-remoting/                   # ⚠️ 开发中 - 远程调用模块
├── meta-remoting-api/           # API定义
├── meta-remoting-http/          # HTTP实现
└── meta-remoting-dubbo/         # Dubbo实现
meta-validation/                 # ✅ 完成 - 数据验证工具 (90个测试)
├── exception/                   # ViolationException
├── model/                       # Violation
└── utils/                       # ValidatorUtils
meta-serial/                     # ✅ 完成 - 序列化框架
├── meta-serial-spi/             # SPI接口定义
├── meta-serial-fastjson/        # FastJSON实现
├── meta-serial-jackson/         # Jackson实现
└── meta-serial-lang/            # Java原生实现
```

### Common Patterns
- Constants interfaces (e.g., `MetaConstants`) for shared constants
- Builder pattern for complex object construction (e.g., `BaseResponse.Builder`)
- Package-info.java files for package-level documentation
- Static helper methods in utility classes (e.g., `RequestUtils`)
- Reflection caching for performance optimization
- SPI-based plugin architecture for extensibility
- ExtensionFactory chain for multi-source extension loading

### Performance Considerations
- Use reflection caching for frequently accessed class metadata
- Implement lazy initialization where appropriate
- Consider thread safety in concurrent environments (DCL, ConcurrentHashMap)
- Profile performance bottlenecks before optimization

### Documentation Requirements
- All public APIs must have Javadoc
- Complex algorithms should have inline comments
- Package-level documentation in package-info.java
- README.md updates for major feature additions

## Extension Module Usage

### Basic SPI Usage
```java
// 1. Define extension interface
@Spi("default")
public interface MyService {
    String process(String input);
}

// 2. Create META-INF/extensions/com.example.MyService
// default=com.example.DefaultServiceImpl
// custom=com.example.CustomServiceImpl

// 3. Get extension
MyService service = ExtensionManager.getExtension(MyService.class, "custom");
```

### Spring Integration
```java
// 1. Add dependency: meta-extension-spring
// 2. Define interface
@Spi
public interface DataService {
    String getData();
}

// 3. Create Spring Bean
@Component("myDataService")
public class MyDataServiceImpl implements DataService {
    // ...
}

// 4. Use ExtensionManager - auto-detects Spring beans
DataService service = ExtensionManager.getExtension(DataService.class, "myDataService");
```

### Custom ExtensionFactory
```java
public class MyExtensionFactory implements ExtensionFactory {
    @Override
    public <T> T getExtension(Class<T> type, String name) {
        // Custom logic
        return null;
    }
    
    @Override
    public int getOrder() {
        return 50;  // Lower = higher priority
    }
}

// Register via META-INF/services/com.softmegatron.shared.meta.extension.core.factory.ExtensionFactory
```
