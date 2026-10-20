---
name: repository-understanding
description: Método somente leitura para entender um repositório desconhecido — objetivo, orientação, provar que builda e testa, entrypoints, camadas, dados pelas migrations, integrações, configuração, testes, hotspots no Git, uma fatia vertical, riscos com evidência e aderência ao padrão, entregando docs/architecture/repository-map.md. Use ao chegar a um código novo ou esquecido.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md) e [`../code-style/SKILL.md`](../code-style/SKILL.md) (o padrão contra o qual a aderência é medida), [`../project-claude-md/SKILL.md`](../project-claude-md/SKILL.md) (registrar o que foi aprendido) e [`../microservices/SKILL.md`](../microservices/SKILL.md) (sistemas com vários serviços). O que fazer **depois** de entender: `refactoring`, `test-patterns` (characterization tests), `technical-product-management` (dívida técnica) e o agent `tech-lead`.

# Entendimento de repositório — método

Ler um repositório desconhecido **arquivo por arquivo, do início ao fim** é o jeito mais lento e menos confiável de entendê-lo. O método abaixo vai **de fora para dentro**, **verifica o que afirma** e **termina em um artefato** que outra pessoa (ou agent) consegue usar. É **somente leitura**: entender **não é** mudar. Nada aqui altera arquivos do projeto; o único artefato novo é o mapa em `docs/architecture/` (gravado **com confirmação** do usuário).

> **Fato, inferência ou desconhecido.** Cada afirmação do mapa é marcada: ✅ **verificado** (li o código/executei e cito `arquivo:linha` ou o comando), 🔎 **inferido** (deduzi de nomes/estrutura — dizer em que baseei), ❓ **desconhecido** (não consegui determinar). **Nunca** descreva "o sistema faz X" sem ter lido o trecho que faz X. README e comentários **envelhecem**: o código e os testes são a fonte da verdade.

## 0. Defina o objetivo (e pare quando o atingir)

"Entender o repositório inteiro" não é um objetivo. Pergunte **para quê**: *vou corrigir um bug em X? adicionar a feature Y? avaliar a saúde antes de assumir? migrar de versão? preparar uma refatoração?* O objetivo define a **profundidade** de cada fase e o **critério de parada**. Faça **timebox** (ex.: 30 min para orientação + trace de uma fatia; 2 h para uma avaliação completa) e **registre o que ficou fora**.

## 1. Orientação (5–10 min): o terreno

Leia, nesta ordem, **só o que existir**: `README`, `CLAUDE.md`, `docs/` (incluindo `docs/adr/`, `docs/architecture/`, `docs/product/`), `CONTRIBUTING`, o `CHANGELOG`. Depois a **árvore** (profundidade 2–3) e os **arquivos de build/entrega**:
```bash
git ls-files | head -100
git ls-files | sed 's#/[^/]*$##' | sort | uniq -c | sort -rn | head -30
```
| Procure | Revela |
|---|---|
| `pom.xml` / `build.gradle(.kts)` / `settings.gradle` | Java e Spring Boot (versões), **módulos** (`<modules>`), starters (o que o app faz: `webmvc`, `data-jpa`, `kafka`, `security`…), plugins |
| `src/main/java/**` (árvore de packages) | Layout: flat-by-layer, por módulo, hexagonal (`domain/application/adapter`)? |
| `src/main/resources/application*.yml` | Profiles, portas, datasource, flags, imports de config externa |
| `src/main/resources/db/migration/` | Schema (Flyway) e o **histórico** do modelo de dados |
| `Dockerfile`, `docker-compose*.yml`, `k8s/`, `chart/`, `infra/`, `.github/workflows/` | Como é empacotado, implantado e validado |
| `src/test/**` | Tipos de teste (unit, slice, integração, contrato), Testcontainers, `*IT` |

Anote **versões e estilo de build** (Maven × Gradle, wrapper presente?, multi-módulo?).

## 2. Verifique que builda, sobe e testa (a "prova de realidade")

O repositório que **não compila** muda tudo o que você conclui. **Execute**, não presuma (e relate **o que de fato rodou**):
```bash
./mvnw -v
./mvnw -q -DskipTests package
./mvnw -q verify
```
- Falhou? **Registre o erro literal** e a causa provável (JDK errado, Docker parado para Testcontainers, dependência privada, variável de ambiente ausente). **Não "conserte" para continuar** sem avisar — consertar é outra tarefa.
- Se **não puder executar** (sem Docker/JDK/rede), diga **"não verificado"** e por quê; o mapa marca ❓.
- **Como rodar localmente**: `docker-compose`, `spring-boot:run`, profile `local`, banco necessário? (veja o `README` **e confirme** nos arquivos — comandos documentados quebram).
- **Variáveis e segredos necessários**: liste **os nomes** (`grep -rhoE '\$\{[A-Z_][A-Z0-9_]*' src/main/resources`), **nunca os valores**.
- **Tempo de build e de testes** e **quantidade de testes** (sinal de saúde).

## 3. Inventário de entrypoints (por onde o mundo entra)

Todo comportamento começa em um **gatilho**. Liste-os com `Grep`:
| Gatilho | Procure | Anote |
|---|---|---|
| **HTTP** | `@RestController`, `@Controller`, `@RequestMapping`, `@GetMapping`… | Método, **path**, **auth exigida**, DTO de entrada/saída, service chamado |
| **Mensagens** | `@KafkaListener`, `@RabbitListener`, `@SqsListener`, `@JmsListener` | Tópico/fila, grupo, idempotência?, DLQ? |
| **Agendados** | `@Scheduled`, `@EnableScheduling`, Quartz | Cron, lock distribuído? |
| **Startup/CLI** | `CommandLineRunner`, `ApplicationRunner`, `@PostConstruct`, `main` | O que roda ao subir |
| **Eventos internos** | `@EventListener`, `@ApplicationModuleListener`, `@TransactionalEventListener` | Quem reage a quê |
| **Serverless** | `RequestHandler`, `Function<…>` (Lambda) | Evento de origem |
| **Webhooks/filtros** | `OncePerRequestFilter`, `HandlerInterceptor`, `@ControllerAdvice` | Efeitos transversais |

**Entregue uma tabela de endpoints** (a "API pública" real, que muitas vezes difere do Swagger). **Endpoints sem autenticação/autorização aparente** vão direto ao mapa de riscos (seção 12).

## 4. Arquitetura e camadas

- **Layout** (compare com `code-organization`): `controllers/services/repository/model/data/dto` (flat-by-layer)? Por **módulo de negócio** (`modular-monolith`: `package-info.java` com `@ApplicationModule`)? **Hexagonal** (`ddd-hexagonal`)? Misto/sem padrão?
- **Direção das dependências**: controller → service → repository (correto) ou ciclos e atalhos (controller chamando repository; service importando classe de controller)? `./mvnw dependency:tree` para as bibliotecas; `jdeps` ou **ArchUnit** (se existir) para os packages.
- **Onde mora a regra de negócio**: nos services (anêmico?), nas entities/aggregates, ou espalhada em controllers/SQL/triggers? É a pergunta mais valiosa para saber **onde mexer**.
- **Configuração transversal**: `@Configuration`, `SecurityFilterChain`, `@ControllerAdvice` (contrato de erro — `exception-handling`), CORS/`WebConfig`, serialização, AOP (`@Aspect`), cache (`@Cacheable`), transações (`@Transactional`: onde estão as fronteiras?).
- **Módulos/serviços**: multi-módulo Maven? O repositório é **um** serviço de vários (`microservices`)? Quais contratos externos (clients, eventos)?
Desenhe um **diagrama de componentes** (Mermaid) com o que **verificou**.

## 5. Dados

- **Schema pelas migrations, não por palpite**: leia `db/migration/V*__*.sql` em ordem — dá o **modelo atual e a evolução**. Entities (`@Entity`, `@Table`) e relacionamentos (`@ManyToOne`, `FetchType`), `@Version`, enums.
- **Repositories** e **queries custom** (`@Query`, native?), **paginação**; sinais de **N+1** (`EAGER`, loops chamando `findById`); transações longas.
- **Outros stores**: DynamoDB/Redis/Elasticsearch/S3 (`aws-dynamodb`, `caching`, `aws-s3-sqs`); **cache** e invalidação.
- **Dados pessoais** (campos como e-mail, CPF, telefone, IP): onde estão, quem lê, aparecem em **logs/eventos**? (`privacy-lgpd`) — registre, **sem copiar valores**.
- **Seeds** (determinísticas?) e como os testes preparam dados.
Entregue um **ERD** (Mermaid `erDiagram`) das tabelas principais.

## 6. Integrações (o que o sistema chama e quem o chama)

| Direção | Procure | Anote |
|---|---|---|
| **Saída HTTP** | `RestClient`, `@HttpExchange`, `WebClient`, `RestTemplate`, Feign | Destino, **timeouts?**, retry/circuit breaker? (`service-communication`, `resilience`) |
| **AWS** | `software.amazon.awssdk`, `spring-cloud-aws`, `S3Client`, `SqsTemplate` | Serviço, credenciais (default chain ou **chave fixa**?), região (`aws-sdk-java`) |
| **Mensageria** | `KafkaTemplate`, `RabbitTemplate`, `SnsTemplate`, outbox? | Tópicos produzidos, **dual write**? (`transactional-outbox`) |
| **Identidade** | JWT próprio, Cognito, OAuth2 client/resource server | Quem emite/valida tokens (`authentication`, `aws-cognito`) |
| **E-mail, pagamento, SaaS** | SES/SMTP, SDKs de terceiros | Sync/async, idempotência |
| **Config externa** | `spring.config.import`, Parameter Store, Secrets Manager | De onde vem a configuração (`aws-parameter-store`) |

Resuma em uma tabela **integração · direção · protocolo · resiliência · chave de configuração**.

## 7. Configuração e ambientes

`application.yml` e `application-<profile>.yml`: **o que muda por ambiente**; **flags** de funcionalidade; **portas e URLs**; `management.*` (Actuator exposto?). **Alerta de segurança:** se encontrar **segredo/credencial/token** em arquivo versionado, **registre apenas o local (`arquivo:linha`) e o tipo, mascarando o valor** (`AKIA…****`), e sinalize **rotacionar** (apagar do Git não basta — está no histórico). **Nunca cole o segredo no mapa nem na conversa.**

## 8. Testes e sinais de qualidade

- **Pirâmide real**: quantos unit/slice/integração/contrato? Há `Testcontainers`/H2 (`integration-testing`)? `@Disabled`? Testes `Thread.sleep`? (`test-patterns`)
- **Cobertura**: JaCoCo configurado? Gate? Valor atual (rode o relatório se puder — `test-coverage`).
- **Testes como documentação**: os nomes (`appliesTheLateFeeWhenTheLoanIsOverdue`) contam o **comportamento esperado** — leia-os **antes** do código de produção da área.
- **Qualidade estática**: Sonar/Checkstyle/SpotBugs no build? `TODO`/`FIXME`/`HACK`: `grep -rEc 'TODO|FIXME|HACK' src | …`.
- **CI**: o que o pipeline roda e **bloqueia**? Quanto tempo leva?

## 9. Histórico Git: onde o sistema dói e quem o conhece

O histórico mostra **intenção** e **risco** que o código não mostra (somente leitura):
```bash
git log --oneline -30
git shortlog -sn --since="12 months ago"
git log --since="6 months ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
git log --since="6 months ago" --pretty=format:'%h %s' -- <caminho>
git blame -L 1,80 <arquivo>
```
- **Hotspots** = arquivos com **alto churn** (mudam muito) **e alta complexidade/tamanho** — é onde estão os **bugs e a dívida**. Combine a lista de mais alterados com os **maiores** (`git ls-files | xargs wc -l | sort -rn | head -20`).
- **Quem conhece o quê** (`shortlog`, `blame`): **bus factor** (uma pessoa dona de um módulo crítico?).
- **Mudanças recentes grandes**, **reversões** (`revert`), **tags/releases**: o ritmo e a estabilidade.
- **Co-change**: arquivos que **sempre mudam juntos** revelam acoplamento escondido.
- **Mensagens de commit** explicam o **porquê** de decisões estranhas — leia antes de "consertar" algo esquisito (*Chesterton's fence*: não remova uma cerca sem saber por que foi posta).

## 10. Operação e entrega

`Dockerfile` (usuário não-root? JRE? layers — `docker-and-docker-compose`), manifests/chart (`kubernetes`, `helm-charts`, `argocd`), IaC (`aws-terraform`), pipeline (`github-actions-aws`), **observabilidade** (Actuator, logs JSON, métricas, tracing — `observability`), **probes**, **runbooks**, SLOs. Como é implantado e **revertido**?

## 11. Rastreie uma fatia vertical (a técnica mais reveladora)

Escolha **uma requisição representativa** (ex.: `POST /api/book/v1`) e siga-a **de ponta a ponta**: controller → validation → service → regra → repository → SQL → (evento/outbox) → resposta; depois o **caminho de erro** (um 404, um 400, uma falha do banco). Isso revela, **em um só traço**, as convenções reais, os pontos de transação, os efeitos colaterais e as lacunas. Documente como **diagrama de sequência** (Mermaid `sequenceDiagram`) com `arquivo:linha` nos passos.

## 12. Mapa de riscos e dívida (com evidência)

Liste achados **ordenados por severidade**, cada um com **evidência (`arquivo:linha`)** e **impacto**; **não** invente. Sinais que valem procurar:
| Área | Sinais |
|---|---|
| **Segurança** | Endpoint sem authz; `permitAll`/`csrf.disable` sem justificativa; entity exposta em controller; segredo em arquivo; JPQL concatenado; `decode` em vez de `verify` de JWT; dado pessoal em log |
| **Confiabilidade** | Chamada externa **sem timeout**; retry em `POST`; **dual write** (salvar + publicar); consumer não idempotente; sem DLQ; exception engolida |
| **Dados** | N+1; falta de índice/paginação; migration destrutiva; seed aleatória; sem `@Version` onde há concorrência |
| **Manutenção** | God service/classe; lógica em controller; duplicação; ciclos de dependência; Lombok (o pacote proíbe); `@SuppressWarnings` em massa; código morto |
| **Plataforma** | Java/Spring Boot fora de suporte; dependências com CVE conhecido; `latest` em imagem; container root |
| **Testes** | Sem testes na regra crítica; `@Disabled` em massa; H2 no lugar do banco real; flaky |
| **Operação** | Sem health/probes corretas; sem métricas/alertas; logs sem correlação; sem rollback |

Para cada achado: **o que, onde, por que importa, esforço estimado (P/M/G)**. Priorize por **risco × probabilidade** e aponte **o primeiro passo barato** (`prioritization`, `technical-product-management`).

## 13. Aderência ao padrão do pacote (gap analysis)

Compare o repositório com as skills — **sem reescrever nada**, só mapear **diferenças** (a decisão de adequar é de produto/engenharia):
| Tema | Skill de referência | Conferir |
|---|---|---|
| Estrutura e preferências | `code-organization`, `code-style` | Layout, `Startup`, sem Lombok, DTOs (entity não exposta), injection, comentários |
| Persistência e migrations | `spring-data-jpa`, `flyway-migrations` | `ddl-auto: none`, `check_nullability`, `open-in-view: false`, `@Transactional` no service, migrations expand → contract |
| Erros e validação | `exception-handling`, `bean-validation` | `ExceptionResponse`/`ProblemDetail`, `@Valid`, 4xx vs 500 |
| API | `swagger`, `web-config` | OpenAPI, CORS, content negotiation |
| Segurança | `authentication`/`aws-cognito` | Stateless, `denyAll` por padrão, validação de token, IDOR |
| Testes | `testing`, `integration-testing`, `test-coverage` | Pirâmide, banco real, **cobertura de 90%** |
| Resiliência e mensageria | `resilience`, `idempotency`, `transactional-outbox`, `messaging` | Timeouts, idempotência, DLQ, outbox |
| Entrega e operação | `docker-and-docker-compose`, `kubernetes`, `observability`, `github-actions-aws` | Imagem, probes, logs JSON, CI |

Marque cada linha: ✅ aderente · 🟡 parcial · ❌ divergente · ❓ não verificado — **com evidência**. Divergência **não é erro** por si: pode ser decisão consciente (procure ADR/commit) — **pergunte antes de "corrigir"**.

## 14. Glossário e perguntas em aberto

- **Domínio**: os 10–20 termos centrais (entidades, estados, regras), **como o código os chama** e se há **sinônimos conflitantes** (`Member` × `User` × `Customer`).
- **Regras de negócio** e onde vivem (`arquivo:linha`).
- **Perguntas em aberto** para quem conhece o sistema (dono do produto, autores do histórico): decisões que o código não explica, comportamentos suspeitos, código aparentemente morto. **Pergunte antes de remover ou "consertar".**

---

## O artefato: `docs/architecture/repository-map.md`

Mostre o conteúdo ao usuário e **peça confirmação antes de gravar** (nunca sobrescreva um mapa existente sem ler e mostrar a diferença). Estrutura:
```markdown
# Mapa do repositório: <nome>
> Gerado em AAAA-MM-DD por <quem>, commit <sha>. Legenda: ✅ verificado · 🔎 inferido · ❓ desconhecido.

## 1. Resumo (5 linhas)
O que é, para quem, estágio, saúde geral e o risco nº 1.

## 2. Stack e versões
Java ___ · Spring Boot ___ · Build ___ · Banco ___ · Mensageria ___ · Nuvem ___ (✅ pom/gradle:linha)

## 3. Como construir, subir e testar
| Passo | Comando | Resultado | Verificado? |
|---|---|---|---|

## 4. Arquitetura
Diagrama (Mermaid) · layout de packages · onde mora a regra de negócio · transações

## 5. Entrypoints
| Tipo | Gatilho | Auth | Chama | Arquivo:linha |
|---|---|---|---|---|

## 6. Dados
ERD (Mermaid) · stores · migrations (nº, última versão) · campos com dado pessoal

## 7. Integrações
| Integração | Direção | Protocolo | Timeout/Resiliência | Configuração |
|---|---|---|---|---|

## 8. Configuração e ambientes (nomes, nunca valores)
| Variável / propriedade | Para quê | Obrigatória? |
|---|---|---|

## 9. Testes e qualidade
Pirâmide real · cobertura atual vs 90% · CI/gates · flaky/@Disabled

## 10. Histórico e hotspots
| Arquivo | Mudanças (6 m) | Tamanho | Dono principal | Observação |
|---|---|---|---|---|

## 11. Fatia vertical rastreada
Diagrama de sequência (Mermaid) do fluxo <X>, com arquivo:linha · e o caminho de erro

## 12. Riscos e dívida (ordenados)
| # | Severidade | Achado | Evidência (arquivo:linha) | Impacto | Esforço | Primeiro passo |
|---|---|---|---|---|---|---|

## 13. Aderência ao padrão do pacote
| Tema | Status | Evidência / observação |
|---|---|---|

## 14. Glossário
| Termo | Significado | Onde no código |
|---|---|---|

## 15. Perguntas em aberto
| # | Pergunta | Para quem | Por que importa |
|---|---|---|---|

## 16. Como mudar X (guia rápido)
Passos curtos para as 2–3 mudanças mais prováveis (ex.: adicionar um endpoint, uma migration).
```
**Depois do mapa:** (1) ofereça atualizar o `CLAUDE.md` via `project-claude-md` (**só com confirmação** e **só com o que foi verificado**); (2) entregue os achados ao `tech-lead` (plano), ao `architect` (se houver decisão estrutural) ou ao `product-manager` (dívida a priorizar); (3) antes de qualquer mudança em área sem teste, **characterization tests** (`test-patterns`) e `refactoring`.

## Eficiência: como ler menos e entender mais

- **Top-down e por perguntas**: cada leitura responde a uma pergunta do objetivo (seção 0). Se não responde, **pare**.
- **Comece pelos testes e pelas migrations** da área: contam o comportamento e o modelo **com menos ruído** que o código de produção.
- **Ignore o gerado/vendorizado** (`target/`, `build/`, `node_modules/`, código gerado por MapStruct/protobuf, `*.min.js`).
- **Use busca antes de leitura**: `Grep` por anotação/nome/chave de configuração; leia **só** os arquivos que o resultado indica.
- **Os maiores e os mais alterados** primeiro (hotspots); **os menores e estáveis** raramente guardam o risco.
- **Registre enquanto lê** (rascunho do mapa): a memória falha; o mapa vira o produto.
- **Sistemas distribuídos**: mapeie **um serviço por vez** e some o **mapa de contratos** entre eles (`contract-testing`, `microservices`).
- **Pergunte a humanos** o que o código não responde (histórico, intenção); **não** adivinhe.

## Anti-patterns

- **Ler linearmente** arquivo por arquivo; ler só o código de produção e **ignorar testes, migrations e histórico**.
- **Confiar no README/comentários** sem confirmar no código; **afirmar sem evidência** ("provavelmente faz X" apresentado como fato).
- **Não executar** build/testes e **concluir** sobre um repositório que talvez nem compile.
- **Mudar o código enquanto explora** ("já que estou aqui") — entendimento e mudança são **tarefas separadas**.
- **Presumir convenções** (a do último projeto) em vez de **observar as deste**.
- **Remover o que "parece morto"** sem investigar (*Chesterton's fence*).
- **Vazar segredos ou dados pessoais** no mapa/conversa; **copiar valores** de configuração sensível.
- **Mapa gigante e raso**; **mapa sem data/commit** (não se sabe se envelheceu); **nunca atualizá-lo**.
- **"Gap analysis" como acusação** em vez de **mapa de decisões a tomar**.

---

## Regras principais

- **Somente leitura**; objetivo claro com **timebox**; o único artefato novo é `docs/architecture/repository-map.md`, **gravado com confirmação**.
- **De fora para dentro**: orientação → **builda/sobe/testa de verdade** → entrypoints → arquitetura → dados (**pelas migrations**) → integrações → configuração → testes → **histórico/hotspots** → operação → **uma fatia vertical rastreada** → riscos → aderência → glossário e perguntas.
- **Marque cada afirmação**: ✅ verificado (`arquivo:linha`/comando) · 🔎 inferido · ❓ desconhecido; **nunca** apresente inferência como fato; **relate o que de fato rodou**.
- **Hotspots = churn × complexidade**; **Chesterton's fence** (não remova o que não entende); leia **testes e commits** antes de "consertar" algo estranho.
- **Segredos e dados pessoais**: registrar **local e tipo, valor mascarado**, recomendar rotação; **nunca** copiar valores.
- **Riscos com evidência, severidade e primeiro passo**; **aderência ao padrão** como mapa de decisões (✅/🟡/❌/❓), **perguntando antes de "corrigir"**.
- **Entender ≠ mudar**: depois do mapa, `tech-lead` planeja, `refactoring` e `test-patterns` (characterization) protegem a mudança, `project-claude-md` registra o que foi **verificado**.
- **Sem Lombok** — deliberado (e sua presença num repositório é um achado de aderência).
