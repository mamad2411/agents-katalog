---
name: build-conventions
description:
  This skill should be used when creating or editing pom.xml, build.gradle.kts, managing Java
  dependencies, configuring Maven/Gradle plugins, or organizing multi-module projects.
version: 0.1.0
---

# Maven and Gradle Build Conventions

This skill defines comprehensive build conventions for Java projects, covering Gradle Kotlin DSL,
Maven POM configuration, dependency management, plugins, multi-module layouts, and build
performance.

## Gradle Kotlin DSL

### Prefer Gradle Kotlin DSL Over Groovy DSL

Use build.gradle.kts (Kotlin DSL) for type safety, IDE auto-completion, and refactoring support.

```kotlin
// CORRECT: build.gradle.kts (Kotlin DSL)
plugins {
    java
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
}

group = "com.example"
version = "1.0.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    runtimeOnly("org.postgresql:postgresql")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

```groovy
// WRONG: build.gradle (Groovy DSL) for new projects
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.3.0'
}

// Less type safety, worse IDE support
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

#### Complete Spring Boot build.gradle.kts

A comprehensive build file for a Spring Boot application.

```kotlin
// CORRECT: Complete build.gradle.kts for Spring Boot
import org.gradle.api.tasks.testing.logging.TestExceptionFormat
import org.gradle.api.tasks.testing.logging.TestLogEvent

plugins {
    java
    jacoco
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
    id("com.diffplug.spotless") version "6.25.0"
}

group = "com.example"
version = "1.0.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // Spring Boot starters
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-actuator")

    // Database
    runtimeOnly("org.postgresql:postgresql")
    runtimeOnly("org.flywaydb:flyway-core")

    // Testing
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.testcontainers:junit-jupiter")
    testImplementation("org.testcontainers:postgresql")
    testImplementation("org.assertj:assertj-core")

    // Development only
    developmentOnly("org.springframework.boot:spring-boot-devtools")
    annotationProcessor("org.springframework.boot:spring-boot-configuration-processor")
}

tasks.withType<Test> {
    useJUnitPlatform()
    testLogging {
        events(TestLogEvent.PASSED, TestLogEvent.SKIPPED, TestLogEvent.FAILED)
        exceptionFormat = TestExceptionFormat.FULL
        showStandardStreams = false
    }
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required = true
        html.required = true
    }
}

tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = "0.90".toBigDecimal()
            }
        }
    }
}

spotless {
    java {
        googleJavaFormat("1.22.0")
        removeUnusedImports()
        trimTrailingWhitespace()
        endWithNewline()
    }
}

tasks.check {
    dependsOn(tasks.jacocoTestCoverageVerification)
}
```

## BOM and Dependency Management

### Use BOM Imports with platform()

Import Bills of Materials (BOMs) to align dependency versions consistently.

```kotlin
// CORRECT: BOM imports with platform() in Gradle
dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:3.3.0"))
    implementation(platform("org.testcontainers:testcontainers-bom:1.19.7"))
    implementation(platform("software.amazon.awssdk:bom:2.25.0"))

    // No version needed when managed by BOM
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("software.amazon.awssdk:s3")
    implementation("software.amazon.awssdk:dynamodb")
    testImplementation("org.testcontainers:postgresql")
    testImplementation("org.testcontainers:kafka")
}
```

```kotlin
// WRONG: Specifying versions already managed by a BOM
dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:3.3.0"))

    // Version is redundant and can cause conflicts
    implementation("org.springframework.boot:spring-boot-starter-web:3.3.0")
}
```

#### BOM Import in Maven

Use dependencyManagement to import BOMs in Maven.

```xml
<!-- CORRECT: BOM import in Maven pom.xml -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.3.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>testcontainers-bom</artifactId>
            <version>1.19.7</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <!-- No version needed -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>postgresql</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

## Dependency Scopes

### Use Correct Gradle Dependency Configurations

Choose the right dependency configuration for each dependency.

```kotlin
// CORRECT: Proper dependency scopes in Gradle
dependencies {
    // api: exposes dependency to consumers (use sparingly, only in libraries)
    api("com.google.guava:guava:33.1.0-jre")

    // implementation: internal dependency, not leaked to consumers (default choice)
    implementation("com.fasterxml.jackson.core:jackson-databind")
    implementation("org.slf4j:slf4j-api")

    // runtimeOnly: needed at runtime but not at compile time
    runtimeOnly("org.postgresql:postgresql")
    runtimeOnly("ch.qos.logback:logback-classic")

    // compileOnly: needed at compile time only (e.g., annotations)
    compileOnly("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok")

    // testImplementation: test compile and runtime
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.assertj:assertj-core")

    // testRuntimeOnly: test runtime only
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
```

```kotlin
// WRONG: Using implementation when api or runtimeOnly is correct
dependencies {
    // This leaks PostgreSQL driver to consumers (should be runtimeOnly)
    implementation("org.postgresql:postgresql")

    // This hides a public API type from consumers (should be api)
    implementation("com.google.guava:guava:33.1.0-jre")
    // If your public API returns a Guava type, consumers can't compile
}
```

#### Maven Dependency Scopes

Use correct Maven scopes for dependencies.

```xml
<!-- CORRECT: Maven dependency scopes -->
<dependencies>
    <!-- compile (default): available everywhere -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- runtime: not needed for compilation -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>

    <!-- provided: supplied by the container -->
    <dependency>
        <groupId>jakarta.servlet</groupId>
        <artifactId>jakarta.servlet-api</artifactId>
        <scope>provided</scope>
    </dependency>

    <!-- test: only for testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

## Code Formatting with Spotless

### Configure Spotless with google-java-format

Use the Spotless plugin with google-java-format for consistent code formatting.

```kotlin
// CORRECT: Spotless configuration in build.gradle.kts
plugins {
    id("com.diffplug.spotless") version "6.25.0"
}

spotless {
    java {
        googleJavaFormat("1.22.0")
        removeUnusedImports()
        trimTrailingWhitespace()
        endWithNewline()
        targetExclude("build/**")
    }
    kotlinGradle {
        ktlint("1.2.1")
    }
}

// Run formatting check before build
tasks.check {
    dependsOn(tasks.named("spotlessCheck"))
}
```

```bash
# Apply formatting
./gradlew spotlessApply

# Check formatting (CI)
./gradlew spotlessCheck
```

#### Spotless in Maven

Configure Spotless via the Maven plugin.

```xml
<!-- CORRECT: Spotless Maven plugin -->
<plugin>
    <groupId>com.diffplug.spotless</groupId>
    <artifactId>spotless-maven-plugin</artifactId>
    <version>2.43.0</version>
    <configuration>
        <java>
            <googleJavaFormat>
                <version>1.22.0</version>
                <style>GOOGLE</style>
            </googleJavaFormat>
            <removeUnusedImports />
            <trimTrailingWhitespace />
            <endWithNewline />
        </java>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
            <phase>verify</phase>
        </execution>
    </executions>
</plugin>
```

## Static Analysis Plugins

### Configure Checkstyle

Use Checkstyle for enforcing coding standards.

```kotlin
// CORRECT: Checkstyle in build.gradle.kts
plugins {
    id("checkstyle")
}

checkstyle {
    toolVersion = "10.15.0"
    configFile = file("config/checkstyle/checkstyle.xml")
    isIgnoreFailures = false
    maxWarnings = 0
}

tasks.withType<Checkstyle> {
    reports {
        xml.required = true
        html.required = true
    }
}
```

```xml
<!-- config/checkstyle/checkstyle.xml (Google checks) -->
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">
<module name="Checker">
    <module name="TreeWalker">
        <module name="GoogleStyle"/>
    </module>
</module>
```

#### Configure SpotBugs

Use SpotBugs for finding potential bugs through static analysis.

```kotlin
// CORRECT: SpotBugs in build.gradle.kts
plugins {
    id("com.github.spotbugs") version "6.0.9"
}

spotbugs {
    toolVersion = "4.8.4"
    effort = com.github.spotbugs.snom.Effort.MAX
    reportLevel = com.github.spotbugs.snom.Confidence.MEDIUM
}

tasks.withType<com.github.spotbugs.snom.SpotBugsTask> {
    reports.create("html") {
        required = true
    }
    reports.create("xml") {
        required = false
    }
}
```

#### Configure JaCoCo

Use JaCoCo for code coverage measurement and enforcement.

```kotlin
// CORRECT: JaCoCo in build.gradle.kts
plugins {
    jacoco
}

jacoco {
    toolVersion = "0.8.11"
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required = true
        html.required = true
        csv.required = false
    }
    classDirectories.setFrom(files(classDirectories.files.map {
        fileTree(it) {
            exclude(
                "**/config/**",
                "**/dto/**",
                "**/*Application*",
                "**/*Config*",
                "**/*Properties*"
            )
        }
    }))
}

tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                counter = "LINE"
                value = "COVEREDRATIO"
                minimum = "0.90".toBigDecimal()
            }
            limit {
                counter = "BRANCH"
                value = "COVEREDRATIO"
                minimum = "0.80".toBigDecimal()
            }
        }
    }
}

tasks.check {
    dependsOn(tasks.jacocoTestCoverageVerification)
}
```

## Multi-Module Projects

### Gradle Multi-Module with Convention Plugins

Use convention plugins in buildSrc for shared configuration in multi-module Gradle projects.

```text
my-project/
  buildSrc/
    build.gradle.kts
    src/main/kotlin/
      java-conventions.gradle.kts
      spring-conventions.gradle.kts
  app/
    build.gradle.kts
  domain/
    build.gradle.kts
  infrastructure/
    build.gradle.kts
  settings.gradle.kts
  build.gradle.kts
```

```kotlin
// buildSrc/build.gradle.kts
plugins {
    `kotlin-dsl`
}

repositories {
    gradlePluginPortal()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-gradle-plugin:3.3.0")
    implementation("io.spring.gradle:dependency-management-plugin:1.1.5")
    implementation("com.diffplug.spotless:spotless-plugin-gradle:6.25.0")
}
```

```kotlin
// buildSrc/src/main/kotlin/java-conventions.gradle.kts
plugins {
    java
    jacoco
    id("com.diffplug.spotless")
}

group = "com.example"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter")
    testImplementation("org.assertj:assertj-core")
    testImplementation("org.mockito:mockito-junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.withType<Test> {
    useJUnitPlatform()
}

spotless {
    java {
        googleJavaFormat("1.22.0")
        removeUnusedImports()
    }
}
```

```kotlin
// buildSrc/src/main/kotlin/spring-conventions.gradle.kts
plugins {
    id("java-conventions")
    id("org.springframework.boot")
    id("io.spring.dependency-management")
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

```kotlin
// app/build.gradle.kts
plugins {
    id("spring-conventions")
}

dependencies {
    implementation(project(":domain"))
    implementation(project(":infrastructure"))
    implementation("org.springframework.boot:spring-boot-starter-web")
}
```

```kotlin
// domain/build.gradle.kts
plugins {
    id("java-conventions")
}

// Domain module has no Spring dependency
```

```kotlin
// infrastructure/build.gradle.kts
plugins {
    id("spring-conventions")
}

dependencies {
    implementation(project(":domain"))
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    runtimeOnly("org.postgresql:postgresql")
}
```

```kotlin
// settings.gradle.kts
rootProject.name = "my-project"

include("app", "domain", "infrastructure")
```

#### Maven Multi-Module with Parent POM

Use a parent POM for shared configuration in Maven multi-module projects.

```xml
<!-- Parent pom.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.0</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>my-project</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>app</module>
        <module>domain</module>
        <module>infrastructure</module>
    </modules>

    <properties>
        <java.version>21</java.version>
        <testcontainers.version>1.19.7</testcontainers.version>
        <assertj.version>3.25.3</assertj.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.testcontainers</groupId>
                <artifactId>testcontainers-bom</artifactId>
                <version>${testcontainers.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>domain</artifactId>
                <version>${project.version}</version>
            </dependency>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>infrastructure</artifactId>
                <version>${project.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>com.diffplug.spotless</groupId>
                    <artifactId>spotless-maven-plugin</artifactId>
                    <version>2.43.0</version>
                    <configuration>
                        <java>
                            <googleJavaFormat>
                                <version>1.22.0</version>
                            </googleJavaFormat>
                        </java>
                    </configuration>
                </plugin>
                <plugin>
                    <groupId>org.jacoco</groupId>
                    <artifactId>jacoco-maven-plugin</artifactId>
                    <version>0.8.11</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

```xml
<!-- app/pom.xml (child module) -->
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>my-project</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>

    <artifactId>app</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>domain</artifactId>
        </dependency>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>infrastructure</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

## Version Catalogs

### Use libs.versions.toml for Centralized Versions

Use Gradle version catalogs for centralized dependency version management.

```toml
# gradle/libs.versions.toml
[versions]
spring-boot = "3.3.0"
spring-dependency-management = "1.1.5"
testcontainers = "1.19.7"
assertj = "3.25.3"
mockito = "5.11.0"
spotless = "6.25.0"
spotbugs = "6.0.9"
jacoco = "0.8.11"
postgresql = "42.7.3"
flyway = "10.11.0"
jackson = "2.17.0"

[libraries]
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }
spring-boot-starter-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
spring-boot-starter-validation = { module = "org.springframework.boot:spring-boot-starter-validation" }
spring-boot-starter-actuator = { module = "org.springframework.boot:spring-boot-starter-actuator" }
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test" }
spring-boot-devtools = { module = "org.springframework.boot:spring-boot-devtools" }
spring-boot-configuration-processor = { module = "org.springframework.boot:spring-boot-configuration-processor" }

postgresql = { module = "org.postgresql:postgresql", version.ref = "postgresql" }
flyway-core = { module = "org.flywaydb:flyway-core", version.ref = "flyway" }

testcontainers-bom = { module = "org.testcontainers:testcontainers-bom", version.ref = "testcontainers" }
testcontainers-junit-jupiter = { module = "org.testcontainers:junit-jupiter" }
testcontainers-postgresql = { module = "org.testcontainers:postgresql" }

assertj-core = { module = "org.assertj:assertj-core", version.ref = "assertj" }
mockito-junit-jupiter = { module = "org.mockito:mockito-junit-jupiter", version.ref = "mockito" }

[bundles]
spring-web = [
    "spring-boot-starter-web",
    "spring-boot-starter-validation",
    "spring-boot-starter-actuator",
]
testing = [
    "spring-boot-starter-test",
    "assertj-core",
    "mockito-junit-jupiter",
]
testcontainers = [
    "testcontainers-junit-jupiter",
    "testcontainers-postgresql",
]

[plugins]
spring-boot = { id = "org.springframework.boot", version.ref = "spring-boot" }
spring-dependency-management = { id = "io.spring.dependency-management", version.ref = "spring-dependency-management" }
spotless = { id = "com.diffplug.spotless", version.ref = "spotless" }
spotbugs = { id = "com.github.spotbugs", version.ref = "spotbugs" }
```

```kotlin
// build.gradle.kts using version catalog
plugins {
    java
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dependency.management)
    alias(libs.plugins.spotless)
}

dependencies {
    implementation(libs.bundles.spring.web)
    implementation(libs.spring.boot.starter.data.jpa)
    runtimeOnly(libs.postgresql)
    runtimeOnly(libs.flyway.core)

    testImplementation(platform(libs.testcontainers.bom))
    testImplementation(libs.bundles.testing)
    testImplementation(libs.bundles.testcontainers)

    developmentOnly(libs.spring.boot.devtools)
    annotationProcessor(libs.spring.boot.configuration.processor)
}
```

```kotlin
// WRONG: Hardcoded versions in build.gradle.kts when catalog exists
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:3.3.0")  // Use catalog
    testImplementation("org.assertj:assertj-core:3.25.3")  // Use catalog
}
```

## Build Wrappers

### Always Use Gradle Wrapper

Commit the Gradle wrapper to version control for reproducible builds.

```bash
# Generate Gradle wrapper
gradle wrapper --gradle-version 8.7

# Files to commit
# gradlew          (Unix script)
# gradlew.bat      (Windows script)
# gradle/wrapper/gradle-wrapper.jar
# gradle/wrapper/gradle-wrapper.properties
```

```text
# .gitignore for Gradle projects
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar
!gradle/wrapper/gradle-wrapper.properties
```

```bash
# CORRECT: Use wrapper for all commands
./gradlew build
./gradlew test
./gradlew bootRun

# WRONG: Using system Gradle directly
gradle build   # May use different version
```

#### Always Use Maven Wrapper

Commit the Maven wrapper for reproducible builds.

```bash
# Generate Maven wrapper
mvn wrapper:wrapper -Dmaven=3.9.6

# Files to commit
# mvnw            (Unix script)
# mvnw.cmd        (Windows script)
# .mvn/wrapper/maven-wrapper.jar
# .mvn/wrapper/maven-wrapper.properties
```

```bash
# CORRECT: Use wrapper for all commands
./mvnw clean install
./mvnw test
./mvnw spring-boot:run

# WRONG: Using system Maven directly
mvn clean install   # May use different version
```

## Publishing to Maven Central

### Configure Publishing in Gradle

Set up publishing for Maven Central via Sonatype OSSRH.

```kotlin
// CORRECT: Publishing configuration in build.gradle.kts
plugins {
    `maven-publish`
    signing
}

java {
    withJavadocJar()
    withSourcesJar()
}

publishing {
    publications {
        create<MavenPublication>("mavenJava") {
            from(components["java"])

            pom {
                name = "My Library"
                description = "A description of my library"
                url = "https://github.com/username/my-library"

                licenses {
                    license {
                        name = "The Apache License, Version 2.0"
                        url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
                    }
                }

                developers {
                    developer {
                        id = "username"
                        name = "Developer Name"
                        email = "dev@example.com"
                    }
                }

                scm {
                    connection = "scm:git:git://github.com/username/my-library.git"
                    developerConnection = "scm:git:ssh://github.com:username/my-library.git"
                    url = "https://github.com/username/my-library"
                }
            }
        }
    }

    repositories {
        maven {
            name = "OSSRH"
            url = uri("https://s01.oss.sonatype.org/service/local/staging/deploy/maven2/")
            credentials {
                username = findProperty("ossrhUsername") as String? ?: ""
                password = findProperty("ossrhPassword") as String? ?: ""
            }
        }
    }
}

signing {
    sign(publishing.publications["mavenJava"])
}
```

#### Publishing in Maven

Configure Maven Central publishing in pom.xml.

```xml
<!-- CORRECT: Distribution management in pom.xml -->
<distributionManagement>
    <snapshotRepository>
        <id>ossrh</id>
        <url>https://s01.oss.sonatype.org/content/repositories/snapshots</url>
    </snapshotRepository>
    <repository>
        <id>ossrh</id>
        <url>https://s01.oss.sonatype.org/service/local/staging/deploy/maven2/</url>
    </repository>
</distributionManagement>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-source-plugin</artifactId>
            <version>3.3.1</version>
            <executions>
                <execution>
                    <id>attach-sources</id>
                    <goals>
                        <goal>jar-no-fork</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-javadoc-plugin</artifactId>
            <version>3.6.3</version>
            <executions>
                <execution>
                    <id>attach-javadocs</id>
                    <goals>
                        <goal>jar</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-gpg-plugin</artifactId>
            <version>3.2.2</version>
            <executions>
                <execution>
                    <id>sign-artifacts</id>
                    <phase>verify</phase>
                    <goals>
                        <goal>sign</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## Build Performance

### Enable Gradle Build Cache

Enable build caching for faster incremental builds.

```text
# gradle.properties
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.daemon=true
org.gradle.jvmargs=-Xmx2g -XX:+UseParallelGC
org.gradle.configureondemand=true
```

```kotlin
// settings.gradle.kts - enable local build cache
buildCache {
    local {
        isEnabled = true
        directory = File(rootDir, ".gradle/build-cache")
        removeUnusedEntriesAfterDays = 30
    }
}
```

```text
# WRONG: gradle.properties without performance tuning
# (missing all performance flags)
```

#### Enable Parallel Builds in Maven

Configure Maven for parallel builds.

```bash
# CORRECT: Parallel Maven builds
./mvnw -T 1C clean install        # 1 thread per CPU core
./mvnw -T 4 clean install         # 4 threads
./mvnw -T 1C -pl app -am install  # Build specific module with dependencies

# CORRECT: Skip tests for faster builds during development
./mvnw -DskipTests clean package  # Skip test execution
./mvnw -Dmaven.test.skip clean package  # Skip compilation and execution
```

```xml
<!-- .mvn/maven.config for default options -->
-T 1C
--no-transfer-progress
```

#### Avoid Unnecessary Rebuilds

Configure proper inputs and outputs to avoid unnecessary work.

```kotlin
// CORRECT: Custom task with proper inputs/outputs for caching
tasks.register<Exec>("generateOpenApi") {
    inputs.file("src/main/resources/openapi.yaml")
    outputs.dir("build/generated/openapi")
    commandLine("./gradlew", "openApiGenerate")
}
```

```kotlin
// WRONG: Task always runs because no inputs/outputs defined
tasks.register<Exec>("generateOpenApi") {
    commandLine("./gradlew", "openApiGenerate")  // Runs every time
}
```

## Complete pom.xml Example

### Full Maven Project Configuration

A comprehensive pom.xml for a Spring Boot application.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.0</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>my-service</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <name>my-service</name>
    <description>My Spring Boot Service</description>

    <properties>
        <java.version>21</java.version>
        <testcontainers.version>1.19.7</testcontainers.version>
        <spotless.version>2.43.0</spotless.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.testcontainers</groupId>
                <artifactId>testcontainers-bom</artifactId>
                <version>${testcontainers.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- Spring Boot -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-core</artifactId>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>postgresql</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
            <plugin>
                <groupId>com.diffplug.spotless</groupId>
                <artifactId>spotless-maven-plugin</artifactId>
                <version>${spotless.version}</version>
                <configuration>
                    <java>
                        <googleJavaFormat>
                            <version>1.22.0</version>
                        </googleJavaFormat>
                        <removeUnusedImports />
                    </java>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>check</goal>
                        </goals>
                        <phase>verify</phase>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <version>0.8.11</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>prepare-agent</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>report</id>
                        <phase>verify</phase>
                        <goals>
                            <goal>report</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>check</id>
                        <phase>verify</phase>
                        <goals>
                            <goal>check</goal>
                        </goals>
                        <configuration>
                            <rules>
                                <rule>
                                    <element>BUNDLE</element>
                                    <limits>
                                        <limit>
                                            <counter>LINE</counter>
                                            <value>COVEREDRATIO</value>
                                            <minimum>0.90</minimum>
                                        </limit>
                                    </limits>
                                </rule>
                            </rules>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

## Existing Repository Compatibility

### Respect Established Build Conventions

When contributing to existing repositories, follow their established build tool and conventions.

```bash
# Discover build conventions
ls build.gradle.kts build.gradle pom.xml 2>/dev/null   # Build tool
cat gradle/libs.versions.toml 2>/dev/null               # Version catalog
cat gradle.properties 2>/dev/null                        # Build properties
ls buildSrc/ 2>/dev/null                                 # Convention plugins
cat .mvn/maven.config 2>/dev/null                        # Maven defaults
```

```text
# Before making changes:
# - Check if project uses Maven or Gradle
# - Check Gradle DSL: Kotlin (.kts) or Groovy
# - Look for version catalogs (libs.versions.toml)
# - Look for convention plugins (buildSrc/)
# - Check for Spotless/Checkstyle configuration
# - Verify Java version in build configuration
# - Follow the established dependency declaration style
```

This skill ensures consistent, performant, and maintainable build configurations across Java
projects using Maven or Gradle. Apply these conventions for reproducible builds, proper dependency
management, and enforced code quality standards.
