---
name: aws-rds-secrets-manager
description: Amazon RDS e AWS Secrets Manager para Spring Boot — banco em subnet privada com TLS verificado, Multi-AZ e backups, dimensionamento do pool e RDS Proxy, senha entregue por External Secrets ou Spring Cloud AWS, rotação e IAM mínimo. Use quando conectar a aplicação a um banco na AWS sem senha no Git.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md) e [`../aws-eks/SKILL.md`](../aws-eks/SKILL.md) (IRSA/Pod Identity: sem ele a aplicação não tem permissão para ler o segredo).

# AWS RDS + Secrets Manager

Dois problemas: **onde o database mora** (RDS gerenciado, privado, com backup) e **como a senha chega à aplicação** (Secrets Manager, nunca em Git/imagem/ConfigMap).

---

## 1. Amazon RDS

**Criação (resumo das decisões, não da UI):**
- Engine: o database escolhido no Step 0 (`code-organization`) — RDS MySQL, PostgreSQL, MariaDB, SQL Server ou Oracle. **Aurora** (MySQL/PostgreSQL-compatible) quando precisar de réplicas de leitura rápidas e failover mais rápido; custa mais.
- **Subnets privadas** (DB subnet group), **`Publicly accessible: No`**. O database nunca recebe IP público.
- **Security group** do RDS: regra de entrada na porta do database (3306/5432) com **origem = o security group dos nodes/pods do EKS**, não um CIDR e jamais `0.0.0.0/0`.
- **Multi-AZ** em produção (standby síncrono em outra AZ, failover automático em 1–2 min); single-AZ só em dev.
- **Backups automáticos** com retenção (7–35 dias) + *point-in-time recovery*; **snapshot manual** antes de migrations arriscadas; **deletion protection** ligada em produção.
- **Criptografia em repouso** (KMS) — só se escolhe na criação; **em trânsito**: force TLS (PostgreSQL `rds.force_ssl=1` no parameter group; MySQL `require_secure_transport=ON`).
- **Parameter group** próprio (não o default, que é imutável) para ajustar `max_connections`, charset (`utf8mb4`) e timezone (UTC).
- Instâncias `db.t4g`/`db.t3` (burstable) para dev; `db.m6g/m6i`/`r6g` em produção.

**Conexão da aplicação** (em variáveis de ambiente, via relaxed binding — o `application.yml` não muda):
```
SPRING_DATASOURCE_URL=jdbc:mysql://library.abc123.us-east-1.rds.amazonaws.com:3306/library_api?useTimezone=true&serverTimezone=UTC&sslMode=VERIFY_IDENTITY
SPRING_DATASOURCE_URL=jdbc:postgresql://library.abc123.us-east-1.rds.amazonaws.com:5432/library_api?sslmode=verify-full
```
- Use **TLS verificando o certificado**: importe o *bundle* de CAs do RDS no truststore da imagem (a AWS publica o `global-bundle.pem`) e use `sslMode=VERIFY_IDENTITY` (MySQL) / `sslmode=verify-full` (PostgreSQL). `sslmode=require` cifra mas **não** verifica o servidor.
- Use o **endpoint** DNS do RDS (ele muda de IP no failover); nunca o IP.

### Dimensionamento do pool de conexões

O RDS tem um teto de conexões (`max_connections`, função da memória da instância). Cada pod do Spring abre o **seu** pool Hikari (padrão 10). Conta que derruba produção:

> `réplicas × maximumPoolSize` ≤ `max_connections` − folga para admin/migrations/jobs.

Com HPA em `maxReplicas: 10` e pool de 10 → 100 conexões só da API. Defina conscientemente:
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 5000
      max-lifetime: 1500000
```
`max-lifetime` **menor** que o timeout de conexão ociosa do servidor/proxy (evita `Communications link failure` por conexão morta). Pools menores costumam ser *mais rápidos* — veja `jvm-performance`. Quando muitas réplicas ou funções efêmeras esgotam as conexões, coloque o **RDS Proxy** na frente: ele agrupa conexões, absorve picos e acelera o failover (a aplicação aponta para o endpoint do proxy; ele também pode ler o segredo e autenticar por IAM).

**Autenticação IAM** (opcional): o pod gera um token de curta duração (`rds-db:connect`) em vez de usar senha — sem segredo para rotacionar, mas exige TLS e um *wrapper* de driver (AWS Advanced JDBC Wrapper) ou geração do token no startup.

**Migrations (Flyway):** o Flyway roda com o usuário configurado no datasource; veja `flyway-migrations` para usuário de migration separado e para Job em Kubernetes.

---

## 2. AWS Secrets Manager

Guarde as credenciais como um **segredo JSON** (um por aplicação/ambiente), por exemplo `library/prod/db`:
```json
{
  "username": "library_app",
  "password": "…gerada pelo Secrets Manager…"
}
```
```bash
aws secretsmanager create-secret --name library/prod/db \
  --secret-string '{"username":"library_app","password":"..."}'
```
Melhor ainda: ao criar o RDS, deixe o **RDS gerenciar a senha do master no Secrets Manager** (`--manage-master-user-password`) — a senha nunca passa por você e é rotacionada.

**Rotação automática** (Lambda de rotação oficial por engine, a cada 30–90 dias): a aplicação precisa **reler** o segredo — ou reiniciar — quando a senha muda. Estratégia *alternating users* (dois usuários que se revezam) evita janela de indisponibilidade. Teste a rotação em staging antes de ligar em produção.

**Permissão mínima** na role da aplicação (IRSA — `aws-eks`):
```json
{
  "Effect": "Allow",
  "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
  "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:library/prod/db-*"
}
```
O sufixo `-*` é porque o ARN do segredo termina com 6 caracteres aleatórios. Se o segredo usa uma KMS key própria, a role também precisa de `kms:Decrypt` nela.

---

## 3. Entregando o segredo à aplicação — duas opções

### Opção A — External Secrets Operator (recomendada: zero mudança no código)

O operador roda no cluster, lê o Secrets Manager (com IRSA) e **cria/atualiza um `Secret` do Kubernetes**, que o Deployment já consome por `envFrom` (veja `kubernetes`). A aplicação continua lendo `SPRING_DATASOURCE_PASSWORD` do ambiente.

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: library-api-secret
  namespace: library
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: library-api-secret
  data:
    - secretKey: SPRING_DATASOURCE_USERNAME
      remoteRef:
        key: library/prod/db
        property: username
    - secretKey: SPRING_DATASOURCE_PASSWORD
      remoteRef:
        key: library/prod/db
        property: password
```
(O `SecretStore` aponta para o provedor `aws`/`SecretsManager` e a região, autenticando com a ServiceAccount do operador — confira a versão atual da `apiVersion` na documentação do External Secrets.) Vantagens: o segredo **não está no Git**, a rotação é propagada pelo `refreshInterval`, e a aplicação é agnóstica de AWS. Variáveis de ambiente só são lidas no start do pod: após a rotação, faça um *rollout restart* (ou use *Reloader*).

### Opção B — Spring Cloud AWS lendo direto do Secrets Manager

Quando não há Kubernetes (EC2/ECS) ou quando se quer o valor sempre fresco, a aplicação lê o segredo por conta própria.

```xml
<dependency>
    <groupId>io.awspring.cloud</groupId>
    <artifactId>spring-cloud-aws-starter-secrets-manager</artifactId>
</dependency>
```
Gerencie as versões pelo BOM `io.awspring.cloud:spring-cloud-aws-dependencies` (no `dependencyManagement`), na **linha compatível com o Boot do projeto** — Spring Cloud AWS tem uma linha por geração do Boot; confirme a correta no Context7/documentação (veja `maven-config`, "Resolving the latest versions") em vez de copiar de um projeto Boot 3.

```yaml
spring:
  config:
    import: "aws-secretsmanager:library/prod/db"
  cloud:
    aws:
      region:
        static: us-east-1
  datasource:
    username: ${username}
    password: ${password}
```
As chaves do JSON (`username`, `password`) viram properties — as placeholders acima as consomem. Para reduzir colisão de nomes, prefixe: `import: "aws-secretsmanager:library/prod/db?prefix=db."` e use `${db.username}`.
- As credenciais AWS vêm da *default provider chain* (IRSA no EKS, role da task no ECS); **nenhuma access key** na configuração.
- Use um **profile** (`prod`) só no `application-prod.yml`, para o import não rodar em dev/teste local sem AWS. Em testes, desligue: `spring.cloud.aws.secretsmanager.enabled=false`/não use o profile.
- O import é lido **no startup**; para refresh em runtime é preciso `@RefreshScope` + actuator/Spring Cloud — complexidade que raramente vale; prefira restart controlado após a rotação.
- Falha de leitura do segredo faz a aplicação **não subir** (comportamento desejado: fail-fast). Evite `spring.config.import: optional:aws-secretsmanager:...` em produção — ele esconderia o erro e subiria sem credenciais.

---

## Regras principais

- RDS em subnet privada, sem IP público; o security group aceita **somente** o SG do cluster; Multi-AZ, backup/PITR e deletion protection em produção.
- TLS verificado (`verify-full`/`VERIFY_IDENTITY`) com o CA bundle do RDS; use o endpoint DNS, nunca o IP.
- `réplicas × maximumPoolSize` ≤ `max_connections`; `max-lifetime` abaixo do timeout do servidor; RDS Proxy quando as conexões apertam.
- Senhas **só** no Secrets Manager (preferencialmente geridas/rotacionadas); **nunca** em Git, imagem, ConfigMap ou `application.yml`.
- Prefira External Secrets Operator (sem acoplar o código à AWS); Spring Cloud AWS quando não há Kubernetes — com a versão compatível com o Boot do projeto.
- IAM de menor privilégio: `GetSecretValue` só no ARN do segredo (+ `kms:Decrypt` se KMS própria), via IRSA/Pod Identity.
- Fail-fast: nunca `optional:` no import de segredos em produção.
- Teste a rotação de credenciais em staging antes de ligá-la em produção.
