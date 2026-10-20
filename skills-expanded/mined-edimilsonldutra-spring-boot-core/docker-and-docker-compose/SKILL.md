---
name: docker-and-docker-compose
description: Containerização de Spring Boot — Dockerfile simples ou multi-stage com layers (jarmode tools), usuário não-root, flags de JVM para container, .dockerignore, o plain jar do Gradle, docker-compose com o database e healthcheck por banco. Use quando dockerizar o projeto, subir app e banco localmente ou revisar um Dockerfile.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) para as preferências do projeto (database, build tool), o package layout base e as convenções de code style.

# Docker e docker-compose

**Pergunte primeiro** (uma vez, e salve nas preferências): *Dockerfile simples* (copia o jar já construído; rápido, ideal para CI que já faz o build) ou *multi-stage* (faz o build dentro do Docker; reprodutível, não exige JDK na máquina). O default recomendado é **multi-stage com layers**.

Comentários em Dockerfile/YAML seguem a preferência salva (default: sem comentários).

---

## .dockerignore

Sem ele, o `COPY . .` leva `.git`, `target/`, IDE e até `.env` para o contexto de build (lento e vaza segredo):
```
.git
.gitignore
.idea
.vscode
*.iml
target
build
.gradle
.env
*.md
docker-compose*.yml
```
Em um Dockerfile **simples** que copia `target/*.jar`, **não** ignore `target`.

---

## Dockerfile simples (jar já construído)

Rode `./mvnw clean package -DskipTests` antes (Gradle: `./gradlew clean build -x test`).

```dockerfile
FROM eclipse-temurin:25-jre
WORKDIR /app
RUN groupadd --system app && useradd --system --gid app app
COPY target/*.jar app.jar
USER app
EXPOSE 8080
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75", "-jar", "app.jar"]
```
**Gradle:** o `build/libs` tem **dois** jars (`bootJar` e `-plain.jar`); `COPY build/libs/*.jar` falharia ou copiaria o errado. Copie pelo nome: `COPY build/libs/meu-app-0.0.1-SNAPSHOT.jar app.jar`, ou desabilite o plain jar (`tasks.named<Jar>("jar") { enabled = false }`).

---

## Dockerfile multi-stage com layers (recomendado)

O Spring Boot separa o jar em camadas (dependencies, loader, snapshot-dependencies, application). Dependencies mudam raramente; o código muda sempre. Com camadas, um rebuild só recopia a camada `application` (poucos KB) e o cache do Docker/registry reaproveita o resto.

```dockerfile
FROM eclipse-temurin:25-jdk AS build
WORKDIR /workspace
COPY .mvn .mvn
COPY mvnw pom.xml ./
RUN ./mvnw -q dependency:go-offline
COPY src src
RUN ./mvnw -q clean package -DskipTests
RUN java -Djarmode=tools -jar target/*.jar extract --layers --destination extracted

FROM eclipse-temurin:25-jre
WORKDIR /app
RUN groupadd --system app && useradd --system --gid app app
COPY --from=build /workspace/extracted/dependencies/ ./
COPY --from=build /workspace/extracted/spring-boot-loader/ ./
COPY --from=build /workspace/extracted/snapshot-dependencies/ ./
COPY --from=build /workspace/extracted/application/ ./
USER app
EXPOSE 8080
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75", "-jar", "app.jar"]
```
- `COPY pom.xml` e `dependency:go-offline` **antes** de `COPY src`: o download das dependencies fica em cache enquanto o `pom.xml` não mudar.
- O `-Djarmode=tools ... extract --layers` é o comando do Boot 3.3+/4 (o antigo `-Djarmode=layertools` foi removido). Ele cria `extracted/` com as pastas das camadas e o `app.jar` fino na `application`. Confirme os nomes das pastas gerados na versão do projeto antes de fixá-los no `COPY`.
- Rode os testes **no CI**, não dentro do `docker build` (`-DskipTests`), onde o Docker-in-Docker para o Testcontainers é um problema.
- **Tag da imagem base:** use a LTS que o projeto escolheu (`java.version`). Para produção, fixe também o digest ou uma tag de patch e atualize com Dependabot/Renovate — `latest` nunca.

**Alternativa sem Dockerfile:** `./mvnw spring-boot:build-image` (Buildpacks) gera uma imagem otimizada, com layers e memória calculada, sem escrever nada (veja `maven-config`).

---

## Flags de JVM em container

- **`-XX:MaxRAMPercentage=75`** — a JVM dimensiona o heap a partir do **limite de memória do container**. O default (25%) desperdiça 75% da memória que você pagou; 100% estoura o limite (o heap não é a única memória: metaspace, threads, buffers nativos) e o container leva `OOMKilled`. 70–75% é o ponto de partida.
- Não fixe `-Xmx` em imagem que roda com limites diferentes em cada ambiente — o percentual acompanha o limite.
- Passe flags extras sem rebuild via `JAVA_TOOL_OPTIONS` no ambiente do container.
- `--enable-native-access=ALL-UNNAMED` só se alguma library nativa avisar.
- Mais tuning (GC, CDS, pool de conexões): `jvm-performance`.

## Segurança da imagem

- **Não rode como root** (`USER app`), mesmo em dev. Um escape do container vira root no host.
- Imagem **JRE**, não JDK, em runtime: menor e menos superfície de ataque.
- Nunca coloque segredo em `ENV`/`ARG` no Dockerfile — ficam no histórico da imagem. Segredos entram em runtime (compose `env_file`/Secrets, Kubernetes Secret, Secrets Manager).
- Escaneie a imagem no CI (Trivy/Grype, ou o scan do ECR — veja `aws-eks`).

---

## docker-compose (app + database)

Exemplo MySQL; troque o serviço do database pela tabela abaixo. A aplicação só deve subir **depois** que o database aceitar conexões: `healthcheck` + `depends_on` com `condition: service_healthy`.

```yaml
services:
  db:
    image: mysql:9
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD:-admin123}
      MYSQL_DATABASE: library_api
    ports:
      - "3306:3306"
    volumes:
      - db-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-p${DB_PASSWORD:-admin123}"]
      interval: 5s
      timeout: 5s
      retries: 20
      start_period: 20s

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/library_api?useTimezone=true&serverTimezone=UTC
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: ${DB_PASSWORD:-admin123}
    ports:
      - "8080:8080"

volumes:
  db-data:
```
- A URL usa o **nome do serviço** (`db`), não `localhost` — dentro da rede do compose, `localhost` é o próprio container da app.
- O Spring converte `SPRING_DATASOURCE_URL` em `spring.datasource.url` (relaxed binding): o `application.yml` não muda entre local, compose e Kubernetes.
- O `docker compose` moderno ignora a chave `version:` — não a escreva.
- Senha de dev no compose é aceitável; **a de produção nunca**. Use `.env` fora do Git (`.gitignore`) ou secrets.
- `docker compose up -d --build` sobe tudo; `docker compose logs -f app`; `docker compose down -v` apaga também o volume (os dados).

### Imagem, healthcheck e porta por database

| Database | Imagem | Healthcheck (`test`) | Porta |
|---|---|---|---|
| MySQL | `mysql:9` | `["CMD", "mysqladmin", "ping", "-h", "localhost", "-p$$MYSQL_ROOT_PASSWORD"]` | 3306 |
| PostgreSQL | `postgres:17` | `["CMD-SHELL", "pg_isready -U postgres -d library_api"]` | 5432 |
| MariaDB | `mariadb:11` | `["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]` | 3306 |
| SQL Server | `mcr.microsoft.com/mssql/server:2022-latest` | `["CMD-SHELL", "/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U sa -P \"$$MSSQL_SA_PASSWORD\" -Q 'SELECT 1'"]` | 1433 |
| Oracle | `gvenzl/oracle-free:23-slim-faststart` | `["CMD", "healthcheck.sh"]` | 1521 |

Variáveis: PostgreSQL `POSTGRES_PASSWORD`/`POSTGRES_DB`; MariaDB `MARIADB_ROOT_PASSWORD`/`MARIADB_DATABASE`; SQL Server `ACCEPT_EULA=Y` + `MSSQL_SA_PASSWORD` (senha forte) e **não cria o database** (crie-o antes da primeira execução); Oracle `ORACLE_PASSWORD`/`APP_USER`/`APP_USER_PASSWORD`. A JDBC URL de cada um está em `maven-config`.

---

## Regras principais

- Pergunte simples vs multi-stage; o default é multi-stage com layers (`-Djarmode=tools extract --layers`).
- `.dockerignore` sempre; `pom.xml` copiado antes de `src` para cachear dependencies.
- Imagem JRE, usuário **não-root**, tag fixa (nunca `latest`), sem segredo em `ENV`/`ARG`.
- `-XX:MaxRAMPercentage=75` em vez de `-Xmx` fixo.
- Gradle: nunca copie o `-plain.jar`.
- Compose: `healthcheck` + `depends_on: service_healthy`; URL com o nome do serviço, não `localhost`; sem `version:`.
- Testes rodam no CI, não no `docker build`.
- A mesma imagem vai para dev, staging e produção — só as variáveis de ambiente mudam.
