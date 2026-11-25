---
name: maven-config
description: Build Maven (e equivalentes Gradle) para Spring Boot 4 / Java 25 — parent e properties, o que o BOM gerencia e o que exige versão, starters modulares do Boot 4, Jackson 3, surefire com o agent do Mockito, Flyway plugin, como resolver versões atuais e comandos. Use quando adicionar dependencies ou plugins, resolver versões ou traduzir o build para Gradle.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) para as preferências do projeto (database, build tool), o package layout base e as convenções de code style.

# Maven Configuration

O parent é sempre `spring-boot-starter-parent` — ele herda plugin management, versões de dependencies e defaults. As versões **não** são fixadas nestas skills: resolva a última estável no momento da criação do projeto e nunca copie versões de outro projeto.

---

## Resolvendo as últimas versões

Não chute versões de memória — o Spring Boot se move rápido e várias libraries aqui têm uma linha major por geração do Boot (springdoc 3.x mira o Boot 4; a linha 2.x mira o Boot 3).

1. **Use um documentation MCP server quando disponível.** O Context7 é o recomendado: ele retorna documentação atual, específica por versão, e informações de release. Se o desenvolvedor não o tem (ou um equivalente) configurado, recomende instalá-lo antes de continuar — para o Claude Code, `npx ctx7 setup --claude`, ou adicione o plugin/MCP server do Context7 como descrito na sua documentação atual.
2. **O próprio Spring Boot:** leia `https://repo.maven.apache.org/maven2/org/springframework/boot/spring-boot-starter-parent/maven-metadata.xml` e pegue a release mais nova que não seja milestone nem RC.
3. **Libraries que o BOM gerencia** (veja abaixo) não precisam de version nenhuma — o parent decide.
4. **Libraries que o BOM não gerencia** recebem uma property nomeada com a última estável do Maven Central (ou do Context7 quando a library documenta uma linha específica para o Boot 4).
5. **Java:** a última LTS que a máquina e o runner de CI têm (`java.version`); o `scaffold` pergunta por ela e avisa sobre versões não-LTS. Faça build e execute os testes com `JAVA_HOME` apontando para esse JDK.

---

## Skeleton do pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>{latest}</version>
        <relativePath/>
    </parent>

    <groupId>br.com.padrao</groupId>
    <artifactId>rest-with-spring-boot-and-java-padrao</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>rest-with-spring-boot-and-java-padrao</name>

    <properties>
        <java.version>{latest LTS}</java.version>
        <dozer.version>{latest}</dozer.version>
        <springdoc.version>{latest 3.x}</springdoc.version>
        <rest-assured.version>{latest}</rest-assured.version>
        <greenmail.version>{latest}</greenmail.version>
        <apache.poi.version>{latest}</apache.poi.version>
        <commons-csv.version>{latest}</commons-csv.version>
        <tika.version>{latest}</tika.version>
        <jasperreports.version>{latest}</jasperreports.version>
        <zxing.version>{latest}</zxing.version>
        <java-jwt.version>{latest}</java-jwt.version>
    </properties>
```

Somente libraries **não** gerenciadas pelo Spring Boot BOM recebem uma property. Adicione uma property somente quando a feature que precisa da library está no projeto.

---

## Dependencies

Adicione somente o que as features do projeto precisam. As tabelas dizem qual skill introduz cada dependency.

### Os starters do Spring Boot 4 são modulares

O Boot 4 dividiu sua auto-configuration em módulos, então a library bruta não se auto-configura mais. Use os starters abaixo, não as libraries soltas:

| Necessidade | Artifact (sem version) | Notas |
|---|---|---|
| REST API | `spring-boot-starter-webmvc` | Não `spring-boot-starter-web` |
| JPA / Hibernate | `spring-boot-starter-data-jpa` | |
| Flyway migrations | `spring-boot-starter-flyway` + `flyway-mysql` | O `flyway-core` simples não executa mais migrations. O módulo do database (`flyway-mysql`) segue o database escolhido no Step 0 de `code-organization` |
| HATEOAS | `spring-boot-starter-hateoas` | Somente quando a API usa tipos HATEOAS (o próprio springdoc inicia sem ele) |
| Security | `spring-boot-starter-security` | |
| Mail | `spring-boot-starter-mail` | |
| Bean Validation | `spring-boot-starter-validation` | Veja `bean-validation` |
| Actuator | `spring-boot-starter-actuator` | Veja `observability` / `kubernetes` |

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-flyway</artifactId>
</dependency>
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-mysql</artifactId>
</dependency>
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
</dependency>
```

### Os cinco databases suportados

MySQL é o default. Para outro dos cinco escolhido no Step 0 de `code-organization`, troque o driver, o módulo do Flyway e o módulo do Testcontainers — todo o resto do pom é igual. Todos os drivers, módulos do Flyway e a versão do Testcontainers são gerenciados pelo Boot BOM (sem `<version>`):

| Database | JDBC driver (`runtime`) | Módulo do Flyway | Módulo do Testcontainers (`test`) | Imagem usada por tests/compose | JDBC URL |
|---|---|---|---|---|---|
| **MySQL** | `com.mysql:mysql-connector-j` | `flyway-mysql` | `testcontainers-mysql` | `mysql:9` | `jdbc:mysql://localhost:3306/db?useTimezone=true&serverTimezone=UTC` |
| **PostgreSQL** | `org.postgresql:postgresql` | `flyway-database-postgresql` | `testcontainers-postgresql` | `postgres:17` | `jdbc:postgresql://localhost:5432/db` |
| **SQL Server** | `com.microsoft.sqlserver:mssql-jdbc` | `flyway-sqlserver` | `testcontainers-mssqlserver` | `mcr.microsoft.com/mssql/server:2022-latest` (exige aceitar o EULA) | `jdbc:sqlserver://localhost:1433;databaseName=db;encrypt=false` |
| **Oracle** | `com.oracle.database.jdbc:ojdbc11` | `flyway-database-oracle` | `testcontainers-oracle-free` | `gvenzl/oracle-free:23-slim-faststart` | `jdbc:oracle:thin:@//localhost:1521/FREEPDB1` |
| **MariaDB** | `org.mariadb.jdbc:mariadb-java-client` | `flyway-mysql` (compartilhado com o MySQL) | `testcontainers-mariadb` | `mariadb:11` | `jdbc:mariadb://localhost:3306/db` |

Notas:
- O `driver-class-name` no `application.yml` é opcional — o Spring detecta o driver pela URL. Remova as flags `useTimezone`/`serverTimezone` do MySQL em outros databases.
- Classes de container do Testcontainers 2: `org.testcontainers.mysql.MySQLContainer`, `org.testcontainers.postgresql.PostgreSQLContainer`, `org.testcontainers.mssqlserver.MSSQLServerContainer` (chame `.acceptLicense()`), `org.testcontainers.oracle.OracleContainer`, `org.testcontainers.mariadb.MariaDBContainer`. A chamada `.withConfigurationOverride("mysql-default-conf")` é somente para MySQL.
- A própria dependency de driver do Flyway Maven plugin (abaixo) segue a mesma tabela, e sua property de versão vem do BOM: `${mysql.version}`, `${postgresql.version}`, `${mssql-jdbc.version}`, `${oracle-database.version}`, `${mariadb.version}`.
- A sintaxe SQL nas migrations difere por database — veja `flyway-migrations`.
- Qualquer outro database está fora desta lista: mantenha a arquitetura, resolva os artifacts equivalentes a partir da documentação atual, e diga ao desenvolvedor que ele não é coberto.

### Data formats do Jackson 3

O Spring Boot 4 usa Jackson 3. Os módulos XML e YAML se moveram para o group `tools.jackson.dataformat` — mesmos artifact ids, versões gerenciadas pelo BOM. Adicione-os somente se o projeto escolheu XML/YAML (veja `web-config`):
```xml
<dependency>
    <groupId>tools.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-xml</artifactId>
</dependency>
<dependency>
    <groupId>tools.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-yaml</artifactId>
</dependency>
```
O Jackson 2 ainda pode aparecer transitivamente (java-jwt, Dozer). Somente os packages `core`, `databind` e `dataformat` mudaram para `tools.jackson.*`; as annotations (`@JsonProperty`, `@JsonIgnore`, `@JsonInclude`) continuam em `com.fasterxml.jackson.annotation`.

### Dependencies de teste

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa-test</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-mysql</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <version>${rest-assured.version}</version>
    <scope>test</scope>
</dependency>
```
- `spring-boot-starter-data-jpa-test` fornece `@DataJpaTest` e `@AutoConfigureTestDatabase` (novos packages em `org.springframework.boot.data.jpa.test.autoconfigure` e `org.springframework.boot.jdbc.test.autoconfigure`).
- Os artifacts do Testcontainers se chamam `testcontainers-<module>` e suas versões vêm do Testcontainers BOM que o Boot importa — sem property. Use o módulo do database escolhido.
- **O REST Assured não é gerenciado pelo BOM do Boot 4** — ele precisa de uma property de versão explícita.
- O GreenMail (SMTP falso para testes de e-mail) também não é gerenciado; quando o projeto envia e-mail:
```xml
<dependency>
    <groupId>com.icegreen</groupId>
    <artifactId>greenmail</artifactId>
    <version>${greenmail.version}</version>
    <scope>test</scope>
    <exclusions>
        <exclusion>
            <groupId>org.eclipse.angus</groupId>
            <artifactId>jakarta.mail</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

### Dev tools
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```

### Libraries que precisam de version explícita (fora do BOM)

| Library | Coordenadas | Introduzida por |
|---|---|---|
| Swagger / OpenAPI | `org.springdoc:springdoc-openapi-starter-webmvc-ui` (`${springdoc.version}`, 3.x para o Boot 4) | `swagger` |
| JWT | `com.auth0:java-jwt` | `authentication` |
| Mapeamento Entity ↔ DTO | `com.github.dozermapper:dozer-core` | `spring-data-jpa` (preferência Dozer) |
| Excel | `org.apache.poi:poi-ooxml` | `file-import-export` |
| CSV | `org.apache.commons:commons-csv` | `file-import-export` |
| Detecção de tipo de arquivo | `org.apache.tika:tika-core` | `file-upload-download` |
| Relatórios PDF | `net.sf.jasperreports:jasperreports`, `jasperreports-fonts`, `jasperreports-pdf`, `jasperreports-jdt` (todos `${jasperreports.version}`) | `pdf-reports` |
| QR Code | `com.google.zxing:core`, `com.google.zxing:javase` | `pdf-reports` |

Com a preferência MapStruct, substitua o Dozer por `org.mapstruct:mapstruct` (uma property `<mapstruct.version>`) mais o annotation processor `mapstruct-processor` declarado no `maven-compiler-plugin` — o processor **não** deve ser uma dependency normal:
```xml
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>${mapstruct.version}</version>
</dependency>
```
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <annotationProcessorPaths>
            <path>
                <groupId>org.mapstruct</groupId>
                <artifactId>mapstruct-processor</artifactId>
                <version>${mapstruct.version}</version>
            </path>
        </annotationProcessorPaths>
    </configuration>
</plugin>
```
Declarar `annotationProcessorPaths` substitui a descoberta default de processors do compiler, então adicione qualquer outro annotation processor que o projeto use (por exemplo o configuration processor do Spring) à mesma lista.

Cada entrada é declarada assim (a version sempre via sua property):
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>${springdoc.version}</version>
</dependency>
```

---

## Build plugins

### spring-boot-maven-plugin (sempre presente)
Mínimo — nenhuma configuração extra necessária, a menos que esteja construindo imagens Docker via Buildpacks.
```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
</plugin>
```

### maven-surefire-plugin com o agent do Mockito
O JDK 21+ avisa quando o Mockito se auto-anexa em runtime, e o Testcontainers carrega o JNA, que precisa de native access. Carregue o Mockito como um `-javaagent` e habilite o native access. O goal `properties` do `maven-dependency-plugin` expõe o path do jar do Mockito como `${org.mockito:mockito-core:jar}`:
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-dependency-plugin</artifactId>
    <executions>
        <execution>
            <goals>
                <goal>properties</goal>
            </goals>
        </execution>
    </executions>
</plugin>
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <argLine>-javaagent:${org.mockito:mockito-core:jar} --enable-native-access=ALL-UNNAMED</argLine>
    </configuration>
</plugin>
```
Deliberadamente não há token `@{argLine}` nele. Se o JaCoCo for adicionado depois, adicione `@{argLine}` no início para que os dois agents carreguem — e declare a property vazia `<argLine></argLine>` em `<properties>` para o caso de o JaCoCo ser pulado. A configuração completa (`prepare-agent`, `report`, `check`, exclusões e Gradle) está em `test-coverage`.

### flyway-maven-plugin (sempre presente)
Usado para executar migrations manualmente contra o database local. A dependency do driver é explícita porque o plugin roda fora do classloader do Spring Boot; sua versão vem da property do Boot BOM (`${mysql.version}` para MySQL). Exclua o `slf4j-api` para evitar conflitos de classpath.
```xml
<plugin>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-maven-plugin</artifactId>
    <configuration>
        <url>jdbc:mysql://localhost:3306/{db_name}?useTimezone=true&amp;serverTimezone=UTC</url>
        <user>root</user>
        <password>admin123</password>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <version>${mysql.version}</version>
            <exclusions>
                <exclusion>
                    <groupId>org.slf4j</groupId>
                    <artifactId>slf4j-api</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
    </dependencies>
</plugin>
```
A URL, o user e a password são valores de desenvolvimento local — nunca aponte este plugin para um database compartilhado ou de produção.

---

## Qualidade do build (opcional, recomendado em equipe e CI)

**maven-enforcer-plugin** — falha o build cedo, com mensagem clara, quando o JDK ou o Maven estão errados, ou quando aparecem dependencies duplicadas/conflitantes:
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-enforcer-plugin</artifactId>
    <executions>
        <execution>
            <id>enforce</id>
            <goals>
                <goal>enforce</goal>
            </goals>
            <configuration>
                <rules>
                    <requireJavaVersion>
                        <version>[${java.version},)</version>
                    </requireJavaVersion>
                    <dependencyConvergence/>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```
Se `dependencyConvergence` reclamar de uma dependency transitiva do Boot, resolva com `<dependencyManagement>`/`<exclusions>` apontando a versão do BOM — não desligue a regra.

**Imagem de container direto do Maven.** O `spring-boot-maven-plugin` também monta uma imagem OCI com Cloud Native Buildpacks, sem Dockerfile: `./mvnw spring-boot:build-image -Dspring-boot.build-image.imageName=meu-app:1.0.0` (precisa de Docker). Para Dockerfile controlado à mão, layers e imagens mínimas, veja `docker-and-docker-compose`.

**Vulnerabilidades.** Rode um scanner de dependencies no CI (OWASP `dependency-check-maven`, ou o Dependabot/Renovate no repositório) e atualize o Boot por patch release regularmente — as versões gerenciadas pelo BOM recebem as correções de segurança junto.

---

## Comandos Maven comuns

Projetos criados pelo `scaffold` carregam o Maven wrapper: execute `./mvnw` (Windows `mvnw.cmd`) onde um comando abaixo diz `mvn` — os argumentos são os mesmos. Sem o wrapper, use o `mvn` do sistema com `JAVA_HOME` apontando para o JDK do projeto.

```bash
mvn clean package
mvn clean package -DskipTests
mvn test
mvn test -Dtest=PersonServicesTest
mvn flyway:migrate
mvn spring-boot:run
```

- `mvn clean package` compila e executa **todos** os testes, incluindo os integration tests, então o Docker precisa estar rodando (Testcontainers).
- `mvn test` também executa tudo — não há divisão unit/integration (sem Failsafe, sem naming `*IT`). Use `-Dtest=ClassName` para uma classe.
- `-DskipTests` é para steps de CI em que os testes já rodaram.
- `mvn spring-boot:run` precisa que o database do `application.yml` esteja acessível.

---

## Gradle (se escolhido no Step 0)

Ambos os build tools são suportados. O `scaffold` gera o projeto Gradle (Groovy ou Kotlin DSL) e ele foi construído, testado e iniciado de verdade — seu build file é a base. O que outras skills adicionam depois mapeia do Maven como abaixo; todo mapeamento desta seção foi compilado em um build Gradle real. **Todo bloco `<dependency>` nestas skills é escrito em XML do Maven — com Gradle, escreva o equivalente por estas regras.**

### Maven para Gradle

| Maven | Gradle, Groovy DSL | Gradle, Kotlin DSL |
|---|---|---|
| `<dependency>` com compile scope | `implementation 'group:artifact'` | `implementation("group:artifact")` |
| `<scope>runtime</scope>` (JDBC driver) | `runtimeOnly '…'` | `runtimeOnly("…")` |
| `<scope>test</scope>` | `testImplementation '…'` | `testImplementation("…")` |
| devtools (`runtime` + `optional`) | `developmentOnly '…'` | `developmentOnly("…")` |
| version em `<properties>` (`${x.version}`) | `ext { set('xVersion', '1.2.3') }` e `"group:artifact:${xVersion}"` | `val xVersion = "1.2.3"` e `"group:artifact:$xVersion"` |
| sem `<version>` (gerenciada pelo Boot BOM) | sem version — o plugin `io.spring.dependency-management` decide | igual |
| `<exclusions>` | `testImplementation('…') { exclude group: 'g', module: 'a' }` | `testImplementation("…") { exclude(group = "g", module = "a") }` |
| `annotationProcessorPaths` (MapStruct) | `annotationProcessor 'org.mapstruct:mapstruct-processor:…'` | `annotationProcessor("…")` |
| `<java.version>` | `java { toolchain { languageVersion = JavaLanguageVersion.of(N) } }` | igual |
| `spring-boot-maven-plugin` | o plugin `org.springframework.boot`, já em `plugins` | igual |
| `argLine` do surefire (agent do Mockito) | a configuration `mockitoAgent` e os `jvmArgs` que o `scaffold` escreve | igual |
| `flyway-maven-plugin` | o plugin `org.flywaydb.flyway` (abaixo) | igual |

As tabelas de dependencies desta skill dão as coordenadas; somente a sintaxe de declaração muda. Algumas libraries, declaradas do jeito Gradle:

```groovy
ext {
    set('springdocVersion', '{latest 3.x}')
    set('restAssuredVersion', '{latest}')
    set('greenmailVersion', '{latest}')
}

dependencies {
    implementation "org.springdoc:springdoc-openapi-starter-webmvc-ui:${springdocVersion}"
    implementation 'tools.jackson.dataformat:jackson-dataformat-yaml'
    testImplementation "io.rest-assured:rest-assured:${restAssuredVersion}"
    testImplementation("com.icegreen:greenmail:${greenmailVersion}") {
        exclude group: 'org.eclipse.angus', module: 'jakarta.mail'
    }
}
```
```kotlin
val springdocVersion = "{latest 3.x}"
val restAssuredVersion = "{latest}"
val greenmailVersion = "{latest}"

dependencies {
    implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:$springdocVersion")
    implementation("tools.jackson.dataformat:jackson-dataformat-yaml")
    testImplementation("io.rest-assured:rest-assured:$restAssuredVersion")
    testImplementation("com.icegreen:greenmail:$greenmailVersion") {
        exclude(group = "org.eclipse.angus", module = "jakarta.mail")
    }
}
```

### O que é diferente no Gradle

- **O Gradle ignora os repositories que o próprio POM de uma dependency declara; o Maven os segue.** O `jasperreports-pdf` precisa do OpenPDF do repository da Jaspersoft, então com Gradle o build para com `Could not find com.github.librepdf:openpdf:…jaspersoft…` até que o repository seja adicionado ao lado de `mavenCentral()` (detalhes na skill `pdf-reports`):
```groovy
repositories {
    mavenCentral()
    maven { url 'https://jaspersoft.jfrog.io/jaspersoft/third-party-ce-artifacts/' }
}
```
No Kotlin DSL: `maven("https://jaspersoft.jfrog.io/jaspersoft/third-party-ce-artifacts/")`.
- **Annotation processors não são descobertos pelo classpath** — o processor do MapStruct (e qualquer outro, como o `spring-boot-configuration-processor`) deve ser declarado com `annotationProcessor`.
- **Dois jars são construídos**: o `bootJar` escreve `build/libs/<name>-<version>.jar` (o executável) e o `jar` escreve `<name>-<version>-plain.jar`. Qualquer coisa que copie "o jar" (um Dockerfile, um step de CI) não deve pegar o plain — veja `docker-and-docker-compose`.
- **Testes são pulados quando nada mudou** (`:test UP-TO-DATE`). Para forçá-los, execute `cleanTest test`.
- **O Flyway plugin roda fora do classpath da aplicação**, então o módulo do database e o JDBC driver vão em `buildscript`, com versions explícitas (o Boot BOM não alcança o `buildscript`). Use as versões que o BOM resolve: `./gradlew dependencies --configuration runtimeClasspath` lista `flyway-core` e o driver. A versão do plugin é igual à versão do Flyway. Somente valores de desenvolvimento local — nunca aponte-o para um database compartilhado ou de produção:
```groovy
buildscript {
    dependencies {
        classpath 'org.flywaydb:flyway-mysql:{flyway version of the BOM}'
        classpath 'com.mysql:mysql-connector-j:{driver version of the BOM}'
    }
}

plugins {
    id 'org.flywaydb.flyway' version '{flyway version of the BOM}'
}

flyway {
    url = 'jdbc:mysql://localhost:3306/{db_name}?useTimezone=true&serverTimezone=UTC'
    user = 'root'
    password = 'admin123'
}
```
O `buildscript` vem primeiro no arquivo, antes de `plugins`. O módulo do Flyway e o driver seguem o database escolhido no Step 0 (a tabela acima). No Kotlin DSL a sintaxe é `classpath("…")`, `id("org.flywaydb.flyway") version "…"` e `url = "…"`.

### Comandos

| Tarefa | Maven (`./mvnw`, ou `mvn`) | Gradle (`./gradlew`) |
|---|---|---|
| build e execução de todos os testes | `mvn clean package` | `./gradlew clean build` |
| build, pulando os testes | `mvn clean package -DskipTests` | `./gradlew clean build -x test` |
| todos os testes | `mvn test` | `./gradlew cleanTest test` |
| uma test class | `mvn test -Dtest=PersonServicesTest` | `./gradlew cleanTest test --tests PersonServicesTest` |
| executar a aplicação | `mvn spring-boot:run` | `./gradlew bootRun` |
| aplicar as migrations | `mvn flyway:migrate` | `./gradlew flywayMigrate` |
| árvore de dependencies | `mvn dependency:tree` | `./gradlew dependencies --configuration runtimeClasspath` |
| o jar executável | `target/<name>-<version>.jar` | `build/libs/<name>-<version>.jar` |

No Windows o wrapper é `mvnw.cmd` / `gradlew.bat`. O Dockerfile e os steps de CI mudam de acordo (veja `docker-and-docker-compose` e `github-actions-aws`).

---

## Regras principais

- O parent é sempre `spring-boot-starter-parent` — nunca gerencie versões de dependencies do Spring manualmente.
- Todas as versões de terceiros são declaradas em `<properties>` com uma property nomeada — nunca inline em `<dependency>`.
- Dependencies gerenciadas pelo BOM nunca declaram `<version>` — deixe o BOM vencer. Nunca assuma que uma library é gerenciada: REST Assured, springdoc, GreenMail, java-jwt, Dozer, POI, commons-csv, Tika, JasperReports e ZXing **não** são.
- Os starters do Boot 4 são modulares: `spring-boot-starter-webmvc`, `-flyway`, `-hateoas`, `-validation`, `-data-jpa-test`. Uma library solta normalmente deixa de se auto-configurar.
- Jackson 3: `tools.jackson.dataformat` para XML/YAML; as annotations continuam em `com.fasterxml.jackson.annotation`.
- O driver do database é `<scope>runtime</scope>` — não é necessário em tempo de compilação.
- `spring-boot-devtools` é `<scope>runtime</scope>` + `<optional>true</optional>` — nunca empacotado no jar final.
- **Sem Lombok** — nunca adicione `lombok` a este projeto. Esta é uma escolha deliberada.
- O `flyway-maven-plugin` sempre carrega sua própria dependency de driver com a exclusão do `slf4j-api`.
- Sempre `mvn clean package` no CI — nunca `mvn install` (evita poluir o cache do repo local no runner). Com Gradle: `./gradlew clean build`.
- Maven e Gradle são ambos suportados: toda `<dependency>` nestas skills mapeia para Gradle pela tabela da seção Gradle.
