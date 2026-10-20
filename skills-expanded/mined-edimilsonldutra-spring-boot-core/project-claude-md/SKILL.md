---
name: project-claude-md
description: Gera ou atualiza o CLAUDE.md de um projeto Spring Boot — comandos verificados, pré-requisitos de teste, runtime setup, arquitetura não óbvia, settings que não podem sair, política de versões, notas de Docker/CI e o bloco de preferências salvas. Use após o scaffold, quando o projeto não tiver CLAUDE.md ou quando algo documentado nele mudar.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) — o Step 0 de `code-organization` produz o bloco de preferências que esta skill armazena.

# Project CLAUDE.md

O `CLAUDE.md` é o que a próxima sessão do Claude Code lê primeiro. Ele deve conter o que um novo desenvolvedor **não** conseguiria aprender com uma olhada rápida no código: os comandos que realmente funcionam, o que os testes precisam, por que uma setting de aparência estranha deve ficar, e as decisões que o projeto tomou. Não é uma listagem de arquivos, não é uma cópia do README e não é marketing.

---

## Quando executar

- Um projeto acabou de passar pelo scaffold e não tem `CLAUDE.md`.
- O projeto tem um, mas uma feature mudou como algo funciona (novo módulo, setup de testes alterado, novo stage de CI, framework atualizado).
- As preferências do Step 0 foram respondidas e o desenvolvedor concordou em salvá-las.

Nunca sobrescreva um `CLAUDE.md` existente às cegas: leia-o, mantenha o que ainda é verdade, atualize o que mudou, adicione o que falta, e mostre ao desenvolvedor um resumo das mudanças antes de escrever.

---

## Processo

1. **Preferências.** Leia a seção `## Project preferences` se presente; se não, execute o Step 0 de `code-organization` (ou, quando o desenvolvedor só quer o arquivo, use os defaults e diga isso).
2. **Inspecione, não chute.** Leia `pom.xml`/`build.gradle`, `src/main/resources/application.yml` (ou `application.properties`) e o de teste, a pasta de migrations, `Dockerfile`, `docker-compose.yml`, `.github/workflows/*`, as base classes de teste, qualquer pasta `Collections/` (Postman) e o README para as instruções de execução. Liste o que o projeto realmente tem.
3. **Verifique cada comando que você vai escrever.** Execute-o, ou pelo menos confirme que a ferramenta e o arquivo que ele usa existem (`./mvnw -v` ou `./gradlew -v`, o compose file, o Maven goal ou a Gradle task). Um comando errado no `CLAUDE.md` custa mais que um comando ausente. Marque qualquer coisa que você não conseguiu verificar como não verificada, em vez de apresentá-la como fato.
4. **Escreva o arquivo** a partir do skeleton abaixo, removendo as seções sobre as quais o projeto não tem nada a dizer.
5. **Mostre ao desenvolvedor** o resultado (ou o diff) e escreva somente depois que ele concordar. Nunca escreva secrets: dizer que existem senhas nos defaults do `application.yml` pode, tokens reais não.

---

## O que pertence a ele

| Inclua | Deixe de fora |
|---|---|
| Comandos exatos (build, run, uma test class, migrations, compose) | Qualquer coisa que `mvn -h`, `./gradlew tasks` ou o código já dizem |
| O que os testes precisam (Docker, uma porta fixa, acesso à rede) e quais dependem de ordem | Tours arquivo por arquivo da source tree |
| Variáveis de ambiente e serviços externos de que a app precisa em runtime | O texto de marketing do README |
| Peças transversais que atravessam arquivos (mapper entity↔DTO, como os links HATEOAS são adicionados, onde ficam as annotations do Swagger, como os content types são negociados, o que o JWT filter faz com um token ruim, como os erros são formatados) | Repetir o próprio Javadoc de uma classe |
| Settings que parecem removíveis mas são load-bearing — com o **motivo** | Regras de estilo que já estão nas skills e nas preferências |
| A política de versões de dependencies | Listas de versões fixadas que ficam obsoletas |
| Fatos de Docker/CI que já pegaram alguém (tags de imagem, peculiaridades do runner, portas) | Tutoriais genéricos de Docker/GitHub Actions |
| O bloco de preferências | Secrets, tokens, dados pessoais |

Mantenha-o curto o bastante para ser lido em toda sessão — por volta de 100–200 linhas. Prefira file paths (`src/main/resources/application.yml`) a descrições, e explique o **porquê**, não o quê.

---

## Skeleton

````markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview
<Stack e versões (Spring Boot x.y / Java NN, Maven ou Gradle), base package, o que a app gerencia, e qualquer coisa
sobre o histórico do projeto que mude como lê-lo (por exemplo "upgraded from Boot 3 keeping the API contract").>

## Commands
Escreva somente o bloco do build tool do projeto, com o wrapper que o projeto realmente tem (`./mvnw` / `./gradlew`; no Windows `mvnw.cmd` / `gradlew.bat`), e verifique cada comando antes de ele entrar (Step 3).
```bash
./mvnw spring-boot:run                  # run the app (needs <database>, see Runtime setup)
./mvnw clean package -DskipTests        # build the jar
./mvnw test                             # everything (needs Docker)
./mvnw test -Dtest=SomeServiceTest      # one test class
docker compose up -d --build            # app + database (run "./mvnw clean package" first, the image copies target/*.jar)
```
```bash
./gradlew bootRun                                     # run the app (needs <database>, see Runtime setup)
./gradlew clean build -x test                         # build the jar
./gradlew cleanTest test                              # everything (needs Docker)
./gradlew cleanTest test --tests SomeServiceTest      # one test class
docker compose up -d --build                          # app + database (run "./gradlew clean build" first, the image copies build/libs/*.jar)
```

## Tests
<Quais testes são unit tests puros e quais iniciam Testcontainers; a porta fixa de teste; suítes dependentes de ordem
("run the whole class, not a single method"); qualquer coisa pulada sem rede; regras de cleanup.>

## Runtime setup
<Database, nome do schema, credenciais para uso local, variáveis de ambiente (somente nomes), diretórios de upload,
login seedado usado pelos testes, onde o Swagger UI é servido.>

## Architecture
<Somente as peças que atravessam vários arquivos e não são óbvias em um único arquivo. Exemplos: mapper wrapper, métodos
de link HATEOAS que precisam ser atualizados quando um método de controller muda, onde ficam as annotations do Swagger,
content negotiation, comportamento do security filter, formatos de erro, factories que escolhem uma implementação.>

## Settings that must stay
<Cada item: a setting, e a falha que você tem sem ela. Exemplos: hibernate.check_nullability, o application.yml de teste
ser uma cópia completa do principal, o argLine do surefire, MySQL config override no container do Testcontainers,
fonts/properties necessárias para a geração de relatórios no Linux.>

## Dependency versions
<Quais versões vêm do Spring Boot parent e quais properties no pom carregam sua própria versão. Política:
resolver a mais recente estável na criação; nunca copiar versões de outro projeto.>

## Docker, Kubernetes, AWS and CI
<Base image, serviços e portas do compose, os stages do workflow de CI e secrets necessários, ressalvas de runner ou versão de ferramenta.
Quando existirem: namespace e cluster Kubernetes, como o deploy é feito (kubectl/Kustomize/Helm), a role IAM e o mecanismo de credenciais
(IRSA/Pod Identity — nunca access keys), repositório ECR, onde ficam os secrets (Secrets Manager/External Secrets) e quais probes o
Deployment usa.>

## Project preferences
- Comments in generated code: no
- Database: MySQL
- Swagger annotations: *ControllerDocs interface
- Build tool: Maven
- Java version: 25 (LTS)
- Configuration file: YAML
- Entity/DTO mapping: Dozer
- Dependency injection: field
````

Use as respostas reais no último bloco — essa seção é o que as sessões posteriores leem em vez de perguntar o Step 0 de novo. Mantenha o heading exato e uma linha por preferência, para que qualquer skill da família consiga encontrá-la.

---

## Mantendo-o verdadeiro

- Quando uma mudança altera um comando documentado, um pré-requisito de teste ou uma setting "must stay", atualize o `CLAUDE.md` na mesma mudança.
- Quando você mexer em uma setting load-bearing, escreva o porquê no arquivo, não em um comentário de código (a preferência default é nenhum comentário no código).
- Se algo no arquivo não é mais verdade, delete — uma instrução errada é pior que nenhuma.

---

## Regras principais

- Leia antes de escrever; nunca sobrescreva um `CLAUDE.md` existente sem mostrar a mudança.
- Todo comando no arquivo foi executado ou confirmado como existente.
- Somente informação não óbvia, transversal ou load-bearing — sem tours de arquivos, sem cópias do README.
- Explique o *porquê* de qualquer coisa que pareça removível.
- Sem secrets, sem listas de versões fixadas.
- O bloco `## Project preferences` mantém seu heading exato e o formato de linha.
- **Sem Lombok** — escolha deliberada, registrada uma vez nas preferências e nas skills, não por projeto.
