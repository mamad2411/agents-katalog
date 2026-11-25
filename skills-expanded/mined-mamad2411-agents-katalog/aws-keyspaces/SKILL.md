---
name: aws-keyspaces
description: Amazon Keyspaces (Cassandra gerenciado) com Spring Data Cassandra — conexão TLS na porta 9142, autenticação SigV4, LOCAL_QUORUM, modelagem por consulta, schema por IaC, limitações frente ao Cassandra, IAM e testes. Use quando migrar um modelo Cassandra para a AWS ou compará-lo com DynamoDB.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md) e [`../aws-sdk-java/SKILL.md`](../aws-sdk-java/SKILL.md) (credenciais e IRSA). Compare com [`../aws-dynamodb/SKILL.md`](../aws-dynamodb/SKILL.md) antes de decidir.

# Amazon Keyspaces (for Apache Cassandra)

**Amazon Keyspaces** é um serviço **serverless, gerenciado e compatível com o Apache Cassandra** (fala CQL e usa os drivers Cassandra): você não opera cluster, nós, *compaction* nem *repair*; escala sob demanda e replica em 3 AZs. É uma "porta de entrada" para quem **já tem aplicações/skills Cassandra** e quer deixar de operar o cluster.

> **Atenção:** Keyspaces é **compatível**, **não idêntico**, ao Cassandra. Há recursos **não suportados ou diferentes** (listados abaixo e que variam com o tempo). **Confirme na documentação atual da AWS** antes de migrar uma aplicação existente — não assuma paridade.

## Keyspaces ou DynamoDB?

| | Keyspaces | DynamoDB |
|---|---|---|
| Interface | **CQL** + drivers Cassandra (Spring Data Cassandra) | API própria (SDK / Enhanced Client) |
| Escolha quando | Já existe **modelo/código Cassandra** a migrar; a equipe domina CQL; portabilidade do driver importa | Greenfield na AWS; quer o serviço mais maduro, com Streams, DAX, Global Tables, transações, TTL, ecossistema AWS |
| Integração AWS | Boa (IAM, VPC endpoint, CloudWatch), menor que DynamoDB | **Nativa e mais profunda** |
| Lock-in | Menor no *modelo* de dados (CQL), mas sem paridade total | Maior |

**Regra prática:** *greenfield na AWS → DynamoDB*. *Migração de Cassandra existente → Keyspaces.* Se a necessidade é relacional/consultas flexíveis, nenhum dos dois: `spring-data-jpa` + RDS.

## Dependencies

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-cassandra</artifactId>
</dependency>
<dependency>
    <groupId>software.aws.mcs</groupId>
    <artifactId>aws-sigv4-auth-cassandra-java-driver-plugin</artifactId>
    <version>${aws-sigv4-cassandra-plugin.version}</version>
</dependency>
```
O plugin **SigV4** autentica com **IAM** (a mesma identidade do pod/task, sem senha). A versão do plugin **não** vem do BOM do Boot — declare em `<properties>` e **confirme que é compatível com o driver Java Cassandra (DataStax) 4.x** usado pelo Spring Boot da versão do projeto (`maven-config`).

---

## Conexão

Keyspaces exige **TLS** na porta **9142**, **local datacenter = a região** e consistência **`LOCAL_QUORUM`** para escritas.

```yaml
spring:
  cassandra:
    contact-points: cassandra.us-east-1.amazonaws.com:9142
    local-datacenter: us-east-1
    keyspace-name: library
    schema-action: none
    ssl:
      enabled: true
    request:
      consistency: local-quorum
      timeout: 5s
    config: classpath:cassandra-driver.conf
```
`cassandra-driver.conf` (configuração do driver, com o provedor SigV4 — **sem credenciais no arquivo**; a região vem do ambiente):
```
datastax-java-driver {
  advanced.auth-provider {
    class = software.aws.mcs.auth.SigV4AuthProvider
    aws-region = us-east-1
  }
}
```
- **`schema-action: none`** — **obrigatório**: o Spring Data não deve criar/alterar schema. DDL no Keyspaces é **assíncrono** (a tabela leva segundos para ficar `ACTIVE`) e a aplicação não deve ter permissão de DDL em produção. Schema por **IaC/scripts** (seção 5).
- **Autenticação:** *preferida* — **IAM via SigV4** (credenciais temporárias da role: IRSA/task role, `aws-eks`/`aws-ecs-fargate`). *Alternativa* — **credenciais específicas de serviço** (usuário/senha gerados pelo IAM): `spring.cassandra.username/password` por variável de ambiente/Secrets Manager (`aws-rds-secrets-manager`); funcionam, mas são segredo de longa duração a rotacionar.
- **Certificado TLS:** o endpoint usa certificados da **Amazon Trust Services**, que os JDKs atuais já confiam; versões antigas de documentação pedem importar o "Starfield" para um truststore — **confirme** o que a documentação atual pede para a sua versão de JDK antes de montar truststore à mão.
- `local-datacenter` **tem que** ser o nome da região (`us-east-1`), senão o driver recusa o nó.
- **Idempotência e retry do driver:** marque statements como idempotentes só se forem de fato; o driver re-tenta statements idempotentes e *speculative execution* duplicaria escritas não idempotentes.
- Acesso **privado**: crie um **VPC interface endpoint** para Keyspaces (`com.amazonaws.<região>.cassandra`) e mantenha a aplicação em subnets privadas (`aws-eks`) — tráfego não passa pela internet nem pela NAT.

---

## Modelagem (Cassandra: tabela por consulta)

Como no DynamoDB, **comece pelas consultas**. Em Cassandra você **denormaliza**: uma tabela por padrão de acesso, **sem JOINs**.

| Conceito | Papel |
|---|---|
| **Partition key** | Define a partição (hash) — o acesso eficiente **sempre** informa a partition key |
| **Clustering columns** | Ordenam as linhas **dentro** da partição e permitem *range* |
| `ALLOW FILTERING` | **Evite**: varre partições; lento e caro |

- **Partição saudável:** distribuição uniforme e **tamanho limitado** (não deixe uma partição crescer indefinidamente — ex.: `PRIMARY KEY (customer_id, order_date)` com anos de pedidos; use *bucket* por mês: `(customer_id, month)`).
- **Evite hot partitions** e chaves de baixa cardinalidade (mesma lógica de `aws-dynamodb`).
- Consulta nova → **nova tabela** (ex.: `books_by_id` e `books_by_author`), mantidas **ambas** pela aplicação (escreva nas duas; um `BATCH` *logged* entre tabelas tem restrições no Keyspaces — confirme).

## Entity e repository (Spring Data Cassandra, sem Lombok)

```java
@Table("books_by_author")
public class Book {

    @PrimaryKeyColumn(name = "author", ordinal = 0, type = PrimaryKeyType.PARTITIONED)
    private String author;

    @PrimaryKeyColumn(name = "title", ordinal = 1, type = PrimaryKeyType.CLUSTERED)
    private String title;

    @PrimaryKeyColumn(name = "id", ordinal = 2, type = PrimaryKeyType.CLUSTERED)
    private UUID id;

    private BigDecimal price;

    private Instant createdAt;

    public Book() {}

    // getters, setters, equals, hashCode
}
```
```java
public interface BookRepository extends CassandraRepository<Book, MapId> {

    Slice<Book> findByAuthor(String author, Pageable pageable);
}
```
- Chave composta: use `@PrimaryKeyClass` + `@PrimaryKey` (classe de chave) quando preferir um tipo de chave dedicado em vez de `MapId`.
- **Paginação por `Slice`** com `CassandraPageRequest` (o *paging state*, não `OFFSET` — Cassandra não tem offset): devolva ao client o **token de página** (`slice.getPageable()` → `PagingState`), nunca "página N".
- Query só pela **partition key** (+ clustering). Métodos derivados que exigem `ALLOW FILTERING` **não** devem existir no repositório.
- DTO + mapper continuam: a entity não vai ao controller (`code-organization`). `BigDecimal` para dinheiro; `Instant` para datas.

## Consistência e escrita

- Escritas no Keyspaces são sempre **LOCAL_QUORUM** (3 réplicas, 2 confirmam); leituras podem ser `LOCAL_ONE` (eventual, mais barata) ou `LOCAL_QUORUM` (fortemente consistente, 2× o custo). Escolha por caso de uso.
- **Transações leves (LWT):** `INSERT ... IF NOT EXISTS`/`UPDATE ... IF` são suportadas com **limitações** e custo maior — use para idempotência/unicidade (`eventId`), não em *hot paths*.
- **Sem `JOIN`, sem agregações pesadas, sem *materialized views* nem *triggers*** (confirme a lista atual). Contadores, UDFs e outros recursos têm suporte limitado. Teste cada recurso que o seu modelo usa.
- **TTL** por linha/tabela é suportado (expira sem custo de delete); cuidado com **tombstones** em padrões de muitos deletes.

## Capacidade, custo e proteção

| Modo | Use |
|---|---|
| **On-demand** | Carga imprevisível, início de projeto (default razoável) |
| **Provisioned** (+ auto scaling) | Carga estável e previsível → mais barato |

Cobra por **leituras e escritas** (unidades por request), armazenamento e backups. **PITR** (point-in-time recovery) ligado em produção; **criptografia em repouso sempre ligada**; tags de custo. Alarmes de *throttling* (`WriteThrottleEvents`/`ReadThrottleEvents`) e latência (`aws-observability`). Tente **requests em lote por partição** e evite *scans*.

## 5. Schema por IaC/scripts

Keyspaces e tabelas são **recursos AWS**: declare por Terraform (`aws_keyspaces_keyspace`, `aws_keyspaces_table` — `aws-terraform`) ou scripts CQL aplicados pelo pipeline com credenciais de **deploy** (não pela aplicação). O Flyway **não** suporta Cassandra; para versionar schema por CQL use ferramentas próprias (Cassandra migration/Liquibase com extensão) **ou IaC**. Mudanças de schema seguem expand → contract (`flyway-migrations`): adicione colunas (`ALTER TABLE ... ADD`), nunca remova colunas que a versão anterior da aplicação usa. Antes de usar a tabela, **verifique que está `ACTIVE`** (`system_schema_mcs.tables`) — DDL é assíncrono.

## IAM de menor privilégio

```json
{
  "Effect": "Allow",
  "Action": ["cassandra:Select", "cassandra:Modify"],
  "Resource": [
    "arn:aws:cassandra:us-east-1:123456789012:/keyspace/library/table/*",
    "arn:aws:cassandra:us-east-1:123456789012:/keyspace/system*"
  ]
}
```
O acesso a `system*` é necessário para o driver descobrir o *schema/topologia*. A aplicação **não** recebe `cassandra:Create/Alter/Drop`. Via IRSA/task role — **nunca access keys**.

## Testes

**Não existe emulador fiel do Keyspaces.** Estratégia:
1. **Lógica e queries CQL** contra um **Apache Cassandra em Testcontainers** (`org.testcontainers.cassandra.CassandraContainer`, imagem `cassandra:5`) — rápido e útil, mas **só prova CQL padrão**: não pega diferenças do Keyspaces (recursos não suportados, consistência fixa, DDL assíncrono).
2. **Testes de integração reais** em uma **conta/keyspace de desenvolvimento** (job separado no pipeline, `github-actions-aws`) para validar o que o Cassandra local não prova.
3. Unit tests do service com o repository mockado (`testing`).
Em testes locais com o container: `schema-action: create_if_not_exists` **só no profile de teste**; **nunca** em produção.

---

## Regras principais

- *Greenfield na AWS → DynamoDB; migração de Cassandra → Keyspaces.* Keyspaces é **compatível, não idêntico**: valide os recursos usados na documentação atual.
- TLS na **9142**, `local-datacenter` = região, `local-quorum`; **IAM via SigV4** (sem senha) preferido; acesso por **VPC endpoint**.
- **`schema-action: none`**; schema por IaC/scripts de deploy; a aplicação sem permissão de DDL; confirme a tabela `ACTIVE`.
- **Tabela por consulta**, partition key uniforme e **partição limitada** (bucket temporal); **sem `ALLOW FILTERING`**; sem JOIN.
- Paginação por **paging state** (token), nunca offset; só queries por partition key (+ clustering).
- LWT só onde necessário; leituras `LOCAL_ONE` quando eventual basta; cuidado com tombstones.
- On-demand por padrão; PITR em produção; alarmes de throttling.
- IAM mínimo (`Select`/`Modify` nos recursos + `system*`), via IRSA/task role — nunca access keys.
- Testes: Cassandra em container para CQL + ambiente de dev real para as diferenças do Keyspaces.
- Entity nunca exposta (DTO + mapper); `BigDecimal` para dinheiro.
- **Sem Lombok** — deliberado.
