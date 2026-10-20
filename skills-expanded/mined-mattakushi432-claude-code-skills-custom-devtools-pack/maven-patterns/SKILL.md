---
name: maven-patterns
description: "When to activate: Maven, POM, Maven lifecycle, Maven plugins, multi-module Maven, dependency management, BOM, Maven profiles"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: java-kotlin
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Maven Patterns

## Parent POM (Multi-Module)

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>my-app-parent</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>pom</packaging>

  <modules>
    <module>core</module>
    <module>api</module>
    <module>worker</module>
  </modules>

  <properties>
    <java.version>21</java.version>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <spring-boot.version>3.3.0</spring-boot.version>
    <kotlin.version>2.0.0</kotlin.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <!-- BOM import — controls all Spring Boot transitive deps -->
      <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-dependencies</artifactId>
        <version>${spring-boot.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>3.3.0</version>
          <configuration>
            <argLine>-Xmx512m</argLine>
          </configuration>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>
```

## Child Module POM

```xml
<project>
  <parent>
    <groupId>com.example</groupId>
    <artifactId>my-app-parent</artifactId>
    <version>1.0.0-SNAPSHOT</version>
  </parent>
  <artifactId>api</artifactId>

  <dependencies>
    <dependency>
      <groupId>com.example</groupId>
      <artifactId>core</artifactId>
      <version>${project.version}</version>
    </dependency>
    <!-- Version managed by BOM — no version tag needed -->
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
        <configuration>
          <image>
            <name>my-app/api:${project.version}</name>
          </image>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

## Profiles

```xml
<profiles>
  <profile>
    <id>dev</id>
    <activation><activeByDefault>true</activeByDefault></activation>
    <properties>
      <spring.profiles.active>dev</spring.profiles.active>
    </properties>
  </profile>

  <profile>
    <id>prod</id>
    <properties>
      <spring.profiles.active>prod</spring.profiles.active>
    </properties>
    <build>
      <plugins>
        <plugin>
          <groupId>org.owasp</groupId>
          <artifactId>dependency-check-maven</artifactId>
          <version>9.2.0</version>
          <executions>
            <execution>
              <goals><goal>check</goal></goals>
            </execution>
          </executions>
        </plugin>
      </plugins>
    </build>
  </profile>

  <profile>
    <id>native</id>
    <build>
      <plugins>
        <plugin>
          <groupId>org.graalvm.buildtools</groupId>
          <artifactId>native-maven-plugin</artifactId>
        </plugin>
      </plugins>
    </build>
  </profile>
</profiles>
```

## Kotlin Maven Plugin

```xml
<build>
  <sourceDirectory>${project.basedir}/src/main/kotlin</sourceDirectory>
  <plugins>
    <plugin>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-maven-plugin</artifactId>
      <version>${kotlin.version}</version>
      <configuration>
        <args><arg>-Xjsr305=strict</arg></args>
        <compilerPlugins>
          <plugin>spring</plugin>
          <plugin>jpa</plugin>
        </compilerPlugins>
      </configuration>
      <executions>
        <execution>
          <id>compile</id>
          <goals><goal>compile</goal></goals>
        </execution>
        <execution>
          <id>test-compile</id>
          <goals><goal>test-compile</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

## Useful Commands

```bash
mvn clean install -DskipTests          # build all modules
mvn clean install -pl api -am          # build api + dependencies
mvn test -pl core                      # test specific module
mvn versions:display-dependency-updates # check for updates
mvn dependency:tree                    # visualize dependency graph
mvn spring-boot:run -pl api            # run specific module
mvn -P prod package                    # build with prod profile
```

## Key Rules
- Always define dependency versions in parent `<dependencyManagement>`, not in child POMs
- Import Spring Boot BOM via `<type>pom</type><scope>import</scope>` — eliminates version conflicts
- Use `<pluginManagement>` in parent for plugin config; child modules just declare `<plugin>` without config
- `-pl module -am` (also-make) is essential for working on a single module in a large multi-module project
- Avoid `<version>` in child dependency declarations when the parent BOM manages it
