---
name: aws-parameter-store
description: Configuração externa na AWS — Parameter Store (String, SecureString) via spring.config.import, convenção de nomes por ambiente, Parameter Store × Secrets Manager × variáveis de ambiente, IAM e KMS, restart × refresh, e AppConfig para feature flags com rollout gradual. Use quando tirar configuração da imagem ou criar feature flags na AWS.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md), [`../aws-sdk-java/SKILL.md`](../aws-sdk-java/SKILL.md) e [`../aws-rds-secrets-manager/SKILL.md`](../aws-rds-secrets-manager/SKILL.md) (segredos que rotacionam).

# AWS Parameter Store e AppConfig

A mesma imagem roda em dev, staging e produção; **o que muda é a configuração**, e ela precisa ficar **fora da imagem e do Git**. Esta skill cobre onde guardar **configuração** (URLs, limites, nomes de filas, flags) e **segredos simples** na AWS, e como o Spring Boot os lê.

## Onde cada coisa vive

| Dado | Onde | Por quê |
|---|---|---|
| Config **não sensível** estática (URLs, timeouts, nome de bucket) | **Variável de ambiente** (ConfigMap / `environment` da task) ou **Parameter Store** (`String`) | Simples; Parameter Store centraliza e permite auditoria/versão |
| Segredo **que não rotaciona** (API key de terceiro, chave de assinatura) | **Parameter Store `SecureString`** (cifrado com KMS) | Barato (padrão é gratuito), IAM por caminho |
| Segredo **que rotaciona** (senha do banco) | **Secrets Manager** (`aws-rds-secrets-manager`) | Rotação automática gerenciada |
| **Feature flags** e config dinâmica com *rollout* gradual | **AWS AppConfig** | Validação, deploy gradual, rollback automático |
| Segredo no Git/imagem/`application.yml` | **Nunca** | — |

**Em Kubernetes/ECS**, a rota mais limpa costuma ser: segredos e parâmetros **injetados como variáveis de ambiente** pelo orquestrador (External Secrets Operator — `kubernetes`/`aws-rds-secrets-manager`; `secrets` da task — `aws-ecs-fargate`), e o Spring lê por *relaxed binding*, **sem acoplar o código à AWS**. Use o **Spring Cloud AWS** (abaixo) quando **não** houver esse mecanismo (EC2, ambientes sem injeção) ou quando quiser a aplicação lendo direto do Parameter Store.

## Parameter Store — conceitos

- **Hierarquia por caminho**: `/prod/library-api/db/url`. IAM e `GetParametersByPath` operam por **prefixo** — é o que torna "uma aplicação só lê os seus parâmetros" fácil.
- **Tipos**: `String`, `StringList`, **`SecureString`** (KMS; o valor só é devolvido decifrado a quem tem `kms:Decrypt`).
- **Tiers**: *Standard* (gratuito, valor até 4 KB, até 10.000 parâmetros) e *Advanced* (pago, até 8 KB, políticas de expiração, mais parâmetros). Comece no Standard.
- **Versionamento** automático por parâmetro (histórico) e **labels**.
- **Convenção de nomes (adote e documente):** `/<ambiente>/<aplicação>/<chave>` — `/prod/library-api/jwt-signing-key`. Nada de nome genérico sem escopo.

Criar (IaC em `aws-terraform`; CLI para ilustrar):
```bash
aws ssm put-parameter --name /prod/library-api/cors-origins --type String --value "https://app.example.com"
aws ssm put-parameter --name /prod/library-api/thirdparty-api-key --type SecureString --value "..."
```
Nunca digite um segredo real em um comando de shell compartilhado (fica no histórico): use IaC com valor vindo de um cofre, ou o console/CLI interativo com `--cli-input-json` de um arquivo fora do Git.

---

## Spring Cloud AWS — Parameter Store como fonte de configuração

```xml
<dependency>
    <groupId>io.awspring.cloud</groupId>
    <artifactId>spring-cloud-aws-starter-parameter-store</artifactId>
</dependency>
```
(BOM do Spring Cloud AWS na **linha compatível com o Boot do projeto** — `aws-sdk-java`, `aws-s3-sqs`.)

```yaml
spring:
  config:
    import: "aws-parameterstore:/prod/library-api/"
  cloud:
    aws:
      region:
        static: us-east-1
```
Cada parâmetro sob o prefixo vira uma **property** com o nome após o prefixo, com `/` trocado por `.`: `/prod/library-api/cors/origin-patterns` → `cors.origin-patterns`. Os valores `SecureString` são **decifrados** automaticamente. Assim o `@Value("${cors.origin-patterns}")` e o `@ConfigurationProperties` continuam iguais.
- **Convenção do Spring Cloud AWS** (se preferir o padrão): sem informar o prefixo ele procura `/config/application/` (comum a todos), `/config/<spring.application.name>/` e `/config/<nome>_<profile>/`. **Confirme a convenção exata na documentação da versão** que usa; o formato explícito acima é mais claro e independe dela.
- **Vários caminhos:** separe por `;` (`aws-parameterstore:/prod/common/;/prod/library-api/`) — o último vence em caso de chave repetida.
- **Fail-fast em produção:** o import **sem** `optional:` faz a aplicação **não subir** se o Parameter Store estiver inacessível ou o caminho não existir — o comportamento desejado. `optional:aws-parameterstore:...` esconde o erro e sobe sem a config (aceitável em **dev/teste**, nunca em produção).
- **Perfil só para a AWS:** ponha o import em `application-aws.yml`/`application-prod.yml` para dev local e testes **não** dependerem da AWS (o profile `test` não o ativa).
- **Os valores são lidos na inicialização.** Mudou um parâmetro? **Reinicie** (rolling restart) — é o modelo mais simples e previsível. Recarga em runtime existe (`@RefreshScope` + reload habilitado) mas adiciona complexidade e comportamentos sutis; use só com necessidade clara (para isso, **AppConfig**, abaixo, é mais indicado).
- **Cache e custo:** leituras do Parameter Store têm cota de *throughput* (TPS) e custo no tier *Advanced* com *higher throughput*; a leitura única no startup é barata. Não consulte o SSM por request.

## IAM e KMS (menor privilégio)

```json
{
  "Effect": "Allow",
  "Action": ["ssm:GetParametersByPath", "ssm:GetParameters", "ssm:GetParameter"],
  "Resource": "arn:aws:ssm:us-east-1:123456789012:parameter/prod/library-api/*"
}
```
- Por **prefixo da aplicação e do ambiente** — a role de `library-api` em prod **não** lê `/prod/outra-app/*` nem `/dev/*`.
- `SecureString`: a role também precisa de **`kms:Decrypt`** na chave KMS usada (a `aws/ssm` padrão exige a permissão implícita via o próprio serviço; com **KMS gerenciada por você** conceda-a explicitamente e restrinja com `kms:ViaService`).
- Quem **grava** parâmetros (pipeline/IaC) é outra identidade, com `ssm:PutParameter` — a aplicação **só lê**.
- Credenciais via **IRSA/task role** (`aws-eks`, `aws-ecs-fargate`) — nunca access keys.

---

## AWS AppConfig — feature flags e configuração dinâmica

O **AppConfig** (do Systems Manager) serve **configuração versionada com rollout controlado**: você publica uma nova versão da config (ou flag) e ele a **implanta gradualmente** (ex.: 10% a cada 10 min), **valida** (JSON Schema/Lambda) antes e **reverte automaticamente** se um **alarme do CloudWatch** disparar. Ideal para **feature flags** (ligar/desligar sem deploy), limites operacionais ajustáveis e *kill switches*.
- A aplicação **consulta** periodicamente (SDK `appconfigdata`: `StartConfigurationSession` + `GetLatestConfiguration`, com o **token de sessão** devolvido a cada chamada) e **cacheia** — nunca por request. Em Lambda/ECS existe a **AppConfig Agent/extension** que faz cache local e expõe `http://localhost:2772`.
- Modele a flag **como configuração tipada** (um record) lida e **cacheada**; código novo atrás da flag, flag desligada por padrão; **remova a flag** quando o rollout termina (flags velhas viram dívida).
- **Quando usar o quê:** valor que muda **raramente** e vale com restart → Parameter Store/env; **ligar/desligar comportamento em produção sem deploy, com rollout seguro** → AppConfig.
- Combine com `observability`: um **alarme** de erro/latência amarrado ao deploy do AppConfig reverte uma flag ruim sozinho.

## Spring: use `@ConfigurationProperties` tipado

Agrupe a config da aplicação em uma classe validada em vez de espalhar `@Value`:
```java
@ConfigurationProperties(prefix = "app.library")
@Validated
public class LibraryProperties {

    @NotBlank
    private String corsOriginPatterns;

    @Min(1)
    private int maxPageSize = 100;

    // getters e setters
}
```
Habilite com `@EnableConfigurationProperties(LibraryProperties.class)` (ou `@ConfigurationPropertiesScan`). **Valores obrigatórios ausentes derrubam a subida** (fail-fast), em vez de falhar na primeira request. Nunca coloque defaults de **segredo** no código/`application.yml`.

## Lambda e ECS

- **ECS**: o campo `secrets` da task aceita `valueFrom` com o **ARN de um parâmetro SSM** (injetado como variável de ambiente; execution role com `ssm:GetParameters`) — veja `aws-ecs-fargate`.
- **Lambda**: o **Powertools Parameters** (`aws-lambda`) lê e **cacheia** SSM/Secrets Manager em runtime; evite segredo em variável de ambiente em texto.

## Testes

- Em testes **não** carregue o import do Parameter Store (profile `test` sem o `aws-parameterstore:`); forneça as properties por `application.yml` de teste ou `@DynamicPropertySource` (`testing`).
- Para provar a integração, **LocalStack** com `.withServices("ssm")` (`aws-s3-sqs`): crie parâmetros no `@BeforeAll` (`SsmClient.putParameter`) e suba o contexto com `spring.config.import` apontando ao endpoint do LocalStack (`spring.cloud.aws.endpoint`), verificando que a property chegou ao bean. Credenciais **falsas** só no teste.
- Teste `@ConfigurationProperties` com valores inválidos → o contexto **não sobe**.

---

## Regras principais

- Configuração **fora da imagem e do Git**; a mesma imagem em todo ambiente.
- Parameter Store: **`/<ambiente>/<aplicação>/<chave>`**, `SecureString` para segredos que **não** rotacionam; Secrets Manager para o que rotaciona.
- Em K8s/ECS, **injete por variável de ambiente** (External Secrets / `secrets` da task) e deixe o código agnóstico; Spring Cloud AWS onde não há injeção.
- `spring.config.import: aws-parameterstore:<prefixo>` **sem `optional:` em produção** (fail-fast); profile só para a AWS; leitura no **startup**, mudança = **restart**.
- IAM por **prefixo** (aplicação + ambiente), `kms:Decrypt` para SecureString, aplicação **só lê**; via IRSA/task role — **nunca access keys**.
- AppConfig para **feature flags e rollout gradual** com validação e rollback por alarme; consulte periodicamente e **cacheie**; remova flags antigas.
- `@ConfigurationProperties` + `@Validated` (fail-fast); nenhum default de segredo no código.
- Testes sem a AWS por padrão; LocalStack para o import; `@ConfigurationProperties` inválido não sobe.
- **Sem Lombok** — deliberado.
