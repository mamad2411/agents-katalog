---
name: maven-expert
description: Expert knowledge for Apache Maven, dependency management, BOMs, and Maven-to-Bazel migration. Use for build configuration and project lifecycle questions.
version: 1.2.0
keywords: [maven, build, dependency-management, migration, java, xml]
---

# maven-expert

> Keyword: maven | Platforms: gemini,claude,codex

Apache Maven Build Tool Expert Skill - The foundation of Java dependency management and project structure.

## Core Mandates

- **BOM Management:** Always prefer **BOM (Bill of Materials)** to manage versions (e.g., `quarkus-bom`, `jackson-bom`) to avoid dependency hell.
- **Dependency Scope:** Rigorously use `compile`, `provided`, `runtime`, and `test` scopes for cleaner artifacts.
- **Transitive Discipline:** Use `mvn dependency:tree` to identify and `exclude` conflicting transitive dependencies.
- **Reproducible Builds:** Lock down plugin versions in `<pluginManagement>`.

## pom.xml Examples

### Quarkus Project with BOM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-service</artifactId>
    <version>1.0.0-SNAPSHOT</version>

    <properties>
        <quarkus.platform.version>3.20.1</quarkus.platform.version>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <surefire-plugin.version>3.5.2</surefire-plugin.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <!-- Quarkus BOM - manages ALL Quarkus dependency versions -->
            <dependency>
                <groupId>io.quarkus.platform</groupId>
                <artifactId>quarkus-bom</artifactId>
                <version>${quarkus.platform.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- No version needed - managed by BOM -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-rest</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-arc</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-hibernate-orm-panache</artifactId>
        </dependency>

        <!-- Test dependencies -->
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-junit5</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>rest-assured</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>io.quarkus.platform</groupId>
                <artifactId>quarkus-maven-plugin</artifactId>
                <version>${quarkus.platform.version}</version>
                <extensions>true</extensions>
                <executions>
                    <execution>
                        <goals>
                            <goal>build</goal>
                            <goal>generate-code</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### Multi-Module Parent POM

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>common</module>
        <module>service-user</module>
        <module>service-order</module>
    </modules>

    <properties>
        <quarkus.platform.version>3.20.1</quarkus.platform.version>
        <maven.compiler.release>21</maven.compiler.release>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>io.quarkus.platform</groupId>
                <artifactId>quarkus-bom</artifactId>
                <version>${quarkus.platform.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <!-- Internal module versions -->
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>common</artifactId>
                <version>${project.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <!-- Plugin versions locked here, NOT in child modules -->
    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.13.0</version>
                </plugin>
                <plugin>
                    <artifactId>maven-surefire-plugin</artifactId>
                    <version>3.5.2</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

## Dependency Scope Decision Tree

```
Is this library needed at compile time AND runtime?
  YES → compile (default, usually omit <scope>)
Is it provided by the runtime container (Quarkus, app server)?
  YES → provided (e.g., jakarta.servlet-api, quarkus internals)
Is it only needed at runtime, not compiled against?
  YES → runtime (e.g., JDBC drivers, SLF4J implementations)
Is it only for tests?
  YES → test
Is it needed only at build time for annotation processing?
  YES → provided + annotation processor config in compiler plugin
```

## Version Conflict Resolution Workflow

### Step 1: Identify the conflict

```bash
# Show full dependency tree
mvn dependency:tree -Dincludes=com.fasterxml.jackson

# Output shows conflicting versions:
# [INFO] +- io.quarkus:quarkus-rest-jackson:jar:3.20.1:compile
# [INFO] |  \- com.fasterxml.jackson.core:jackson-databind:jar:2.18.2:compile
# [INFO] +- some-other-lib:jar:1.0:compile
# [INFO] |  \- com.fasterxml.jackson.core:jackson-databind:jar:2.14.0:compile  ← CONFLICT!
```

### Step 2: Analyze with verbose output

```bash
# Show why a specific version was chosen
mvn dependency:tree -Dverbose -Dincludes=jackson-databind

# Find unused or undeclared deps
mvn dependency:analyze
```

### Step 3: Resolve

```xml
<!-- Option A: Exclude transitive dependency -->
<dependency>
    <groupId>some-other-lib</groupId>
    <artifactId>some-other-lib</artifactId>
    <version>1.0</version>
    <exclusions>
        <exclusion>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<!-- Option B: Force version via BOM (preferred) -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson</groupId>
            <artifactId>jackson-bom</artifactId>
            <version>2.18.2</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<!-- Option C: Direct declaration wins (Maven nearest-first rule) -->
<dependencies>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.18.2</version>
    </dependency>
</dependencies>
```

### Resolution Priority

| Priority | Strategy | When to use |
|----------|----------|-------------|
| 1st | BOM import | When a BOM exists for the library (jackson-bom, netty-bom) |
| 2nd | `<exclusion>` | When one specific lib brings a bad transitive |
| 3rd | Direct declaration | Last resort - harder to maintain |

## Common Errors & Fixes

### "package X does not exist" after mvn compile

```bash
# Cause: Missing dependency or wrong scope
mvn dependency:tree | grep "the-missing-package"

# Fix: Add missing dependency or change scope from test/provided to compile
```

### "Non-resolvable parent POM"

```xml
<!-- Cause: relativePath not set or wrong -->
<parent>
    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <relativePath>../pom.xml</relativePath>  <!-- Must be correct -->
</parent>

<!-- If parent is from remote repo, set empty: -->
<relativePath/>
```

### Tests pass locally but fail on CI

```xml
<!-- Cause: Surefire fork reuse + static state pollution -->
<plugin>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <reuseForks>false</reuseForks>  <!-- Isolate test classes -->
        <!-- OR: control fork count -->
        <forkCount>1C</forkCount>  <!-- 1 fork per CPU core -->
    </configuration>
</plugin>
```

### "Could not find artifact" in private registry

```xml
<!-- settings.xml (~/.m2/settings.xml) -->
<settings>
    <servers>
        <server>
            <id>private-repo</id>
            <username>${env.MAVEN_USER}</username>
            <password>${env.MAVEN_TOKEN}</password>
        </server>
    </servers>
</settings>

<!-- pom.xml -->
<repositories>
    <repository>
        <id>private-repo</id>  <!-- Must match server id -->
        <url>https://nexus.example.com/repository/maven-releases/</url>
    </repository>
</repositories>
```

### Slow builds

```bash
# Parallel build (1 thread per CPU core)
mvn install -T 1C

# Skip tests when iterating
mvn install -DskipTests

# Build only specific module + its dependencies
mvn install -pl service-user -am

# Offline mode (skip remote checks)
mvn install -o
```

## Maven-to-Bazel Migration

- **Dependency Extraction:** Identify external dependencies for `maven_install` in `rules_jvm_external`.
- **Pom-to-Build:** Mapping Maven `<groupId>:<artifactId>` to Bazel `@maven//:group_artifact` targets.
- **Resource Management:** Translating Maven's `src/main/resources` convention to Bazel `resources` attributes.

### Migration Mapping Table

| Maven Concept | Bazel Equivalent |
|---------------|------------------|
| `<dependency scope="compile">` | `deps = [...]` |
| `<dependency scope="provided">` | `deps = [...]` (with `neverlink = True`) |
| `<dependency scope="runtime">` | `runtime_deps = [...]` |
| `<dependency scope="test">` | test target `deps` |
| `<module>subproject</module>` | `//subproject:target` |
| `mvn install` | `bazel build //...` |
| `mvn test` | `bazel test //...` |

## Optimization & Plugins

- **Multi-module Projects:** Efficiently managing parent-child relationships and `<relativePaths>`.
- **Essential Plugins:** Config and optimization for `maven-compiler-plugin`, `maven-surefire-plugin`, and `maven-shade-plugin`.
- **Profiles:** Using `-P` profiles for environment-specific configurations (dev, staging, prod).

## Expert Tips

- Avoid `<version>LATEST</version>` or `<version>RELEASE</version>`; it breaks build reproducibility.
- Use `mvn dependency:analyze` to find unused declared dependencies.
- Prefer `provided` scope for libraries that should be part of the runtime container (like Quarkus-core during augmentation).
- Use `mvn versions:display-dependency-updates` to check for outdated dependencies.
- Always use `<dependencyManagement>` in parent POM, never hardcode versions in child modules.

## 🌐 Maven Knowledge Sources

> **Directive:** Use `web_fetch` to analyze complex POM structures, dependency conflict resolution strategies, or Maven-to-Bazel migration patterns.

- **Maven Dependency Mechanism:** [Introduction to Dependency Mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html) - Nearest-first, scope, and mediation.
- **BOM Import Guide:** [Introduction to the Bill of Materials](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#Importing_Dependencies) - Managing versions centrally.
- **Maven-to-Bazel Migration:** [Migrating from Maven to Bazel](https://bazel.build/migrate/maven) - Strategy and tools.
- **Quarkus Maven Tooling:** [Quarkus Maven Guide](https://quarkus.io/guides/maven-tooling) - Extension management and dev mode.

## References

- [Apache Maven Official Documentation](https://maven.apache.org/guides/index.html)
- [rules_jvm_external (Bazel Maven support)](https://github.com/bazelbuild/rules_jvm_external)
- [Quarkus Official Guides](https://quarkus.io/guides/)

## Skill Interoperability

The **maven-expert** 📦 skill acts as a source for dependency management and project orchestration, supporting:
- **rules-quarkus** 🔧: Facilitates the migration of Maven-based projects to Bazel.
