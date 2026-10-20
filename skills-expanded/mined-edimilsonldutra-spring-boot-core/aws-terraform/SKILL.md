---
name: aws-terraform
description: Infraestrutura como código na AWS com Terraform — módulos e ambientes, estado remoto com lock, providers fixados, exemplos (ECR, SQS com DLQ, DynamoDB, log group, IAM mínimo, RDS com senha gerenciada), segredos fora do state, prevent_destroy, plan/apply no CI com OIDC, scanners, e quando preferir CDK ou SAM. Use quando declarar ou revisar infraestrutura AWS.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md), [`../aws-eks/SKILL.md`](../aws-eks/SKILL.md), [`../aws-ecs-fargate/SKILL.md`](../aws-ecs-fargate/SKILL.md) e [`../github-actions-aws/SKILL.md`](../github-actions-aws/SKILL.md) (OIDC e pipeline). Esta skill é a base de **todo recurso AWS declarado como código** — ECR, filas, tabelas, roles, clusters, alarmes.

# Terraform na AWS

**Nada de infraestrutura criada à mão no console.** Recurso criado por clique não é versionado, não é revisado, não é reproduzível em outro ambiente e some do radar até quebrar. Toda a infraestrutura (e a **segurança** dela — IAM, security groups, criptografia) vive em **código no Git**, passa por **pull request** e é aplicada por **pipeline**. Terraform é a ferramenta padrão (declarativa, multi-cloud, enorme ecossistema).

> Os trechos usam a sintaxe estável do Terraform/provider AWS. **Versões do Terraform e do provider mudam rápido:** fixe-as (abaixo) e confirme a versão atual e atributos na documentação do provider — não copie versões de outro projeto.

## Terraform, CDK ou CloudFormation/SAM?

| | Terraform | AWS CDK (Java) | CloudFormation / SAM |
|---|---|---|---|
| Linguagem | HCL (declarativa) | **Java** (a mesma da equipe!) — gera CloudFormation | YAML/JSON |
| Estado | Você gerencia (S3) | AWS gerencia (stack) | AWS gerencia |
| Multi-cloud / ecossistema de módulos | **Sim** | Não (AWS) | Não (AWS) |
| Quando | Padrão geral, equipes de plataforma, multi-cloud, a maioria dos casos | Equipe de devs Java que prefere **código** (loops, abstrações, testes unitários da infra) e só AWS | Funções Lambda pequenas (**SAM**, `aws-lambda`), integração com o ecossistema AWS |

**Padrão do pack: Terraform.** Use **SAM** para o ciclo local de Lambda e **CDK** se a equipe é Java e quer abstrações de código. **Escolha um** por stack — misturar vira mistério de quem é dono de cada recurso.

---

## Estrutura do repositório

```
infra/
├── modules/
│   ├── app-queue/            # SQS + DLQ + alarmes (reuso)
│   └── app-ecr/              # ECR com scan, imutabilidade e lifecycle
├── envs/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── backend.tf
│   │   ├── variables.tf
│   │   └── dev.tfvars
│   ├── staging/
│   └── prod/
└── README.md
```
- **Um diretório (e um *state*) por ambiente**: dev, staging e prod **isolados** — um `apply` errado em dev **não toca** prod; permissões e contas AWS diferentes por ambiente (idealmente **contas AWS separadas**).
- **Módulos** encapsulam um padrão repetido (a fila com DLQ e alarme é sempre igual). Não crie módulo para um recurso só — abstração prematura. Versione módulos compartilhados (tag do Git).
- Prefira **módulos oficiais/comunitários** consolidados (`terraform-aws-modules`: VPC, EKS, RDS) a reescrever do zero — **fixando a versão**.

## Estado remoto, provider e versões

```hcl
terraform {
  required_version = "~> 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "padrao-terraform-state-123456789012"
    key          = "library/prod/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project     = "library"
      Environment = var.env
      ManagedBy   = "terraform"
      Owner       = "platform-team"
    }
  }
}
```
- **State no S3** (bucket **versionado**, **criptografado**, com **Block Public Access** e acesso restrito) com **lock** para impedir dois `apply` simultâneos (`use_lockfile` — lock nativo no S3 nas versões recentes do Terraform; as anteriores usavam uma tabela DynamoDB para o lock — **confirme o que a sua versão suporta**). O bucket do state é criado **uma vez**, fora deste código (bootstrap).
- **O state contém dados sensíveis** (senhas geradas, ARNs, às vezes segredos em texto): **acesso mínimo** ao bucket; **nunca** commite `terraform.tfstate`/`.terraform/` (`.gitignore`).
- **Fixe** `required_version` e a versão do provider (`~>` aceita só patch/minor compatíveis) e **commite o `.terraform.lock.hcl`** — builds reprodutíveis, sem surpresa de upgrade no CI.
- **`default_tags`**: toda a infra recebe `Project/Environment/ManagedBy/Owner` — base de **custo por projeto** (Cost Explorer) e de auditoria.
- Região e ambiente vêm de **variáveis**, nunca hardcoded no recurso.

---

## Exemplos da stack

**ECR** (imutável, com scan e lifecycle — `aws-eks`):
```hcl
resource "aws_ecr_repository" "app" {
  name                 = "library-api"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "KMS"
  }
}

resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep the last 30 images"
      selection    = { tagStatus = "any", countType = "imageCountMoreThan", countNumber = 30 }
      action       = { type = "expire" }
    }]
  })
}
```

**SQS com DLQ** (`aws-sns-sqs`, `messaging`):
```hcl
resource "aws_sqs_queue" "dlq" {
  name                      = "library-search-index-dlq-${var.env}"
  message_retention_seconds = 1209600
  sqs_managed_sse_enabled   = true
}

resource "aws_sqs_queue" "main" {
  name                       = "library-search-index-${var.env}"
  visibility_timeout_seconds = 60
  receive_wait_time_seconds  = 20
  sqs_managed_sse_enabled    = true

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 5
  })
}
```

**Log group com retenção** (`aws-observability` — nunca deixe o padrão infinito):
```hcl
resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/library-api-${var.env}"
  retention_in_days = 30
}
```

**IAM com menor privilégio** (a policy da aplicação — ações e ARNs exatos):
```hcl
data "aws_iam_policy_document" "app" {
  statement {
    effect    = "Allow"
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes", "sqs:GetQueueUrl"]
    resources = [aws_sqs_queue.main.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"]
    resources = [aws_dynamodb_table.books.arn, "${aws_dynamodb_table.books.arn}/index/*"]
  }
}

resource "aws_iam_policy" "app" {
  name   = "library-api-${var.env}"
  policy = data.aws_iam_policy_document.app.json
}
```
A **trust policy** da role (IRSA — `aws-eks`; task role — `aws-ecs-fargate`; OIDC do GitHub — `github-actions-aws`) também é código. **Nunca** `Action = "*"` / `Resource = "*"` (`code-reviewer` 🔴).

**RDS com a senha gerenciada pela AWS** (nunca no state nem no Git — `aws-rds-secrets-manager`):
```hcl
resource "aws_db_instance" "main" {
  identifier                  = "library-${var.env}"
  engine                      = "postgres"
  instance_class              = var.db_instance_class
  allocated_storage           = 50
  db_name                     = "library_api"
  username                    = "library_admin"
  manage_master_user_password = true
  storage_encrypted           = true
  multi_az                    = var.env == "prod"
  publicly_accessible         = false
  db_subnet_group_name        = aws_db_subnet_group.main.name
  vpc_security_group_ids      = [aws_security_group.db.id]
  backup_retention_period     = 14
  deletion_protection         = var.env == "prod"
  skip_final_snapshot         = var.env != "prod"
}
```
`manage_master_user_password = true`: o RDS cria e **rotaciona** a senha no Secrets Manager — o Terraform **não conhece** o valor (não vai para o state). Se precisar passar um segredo, nunca em `.tfvars` versionado: use `TF_VAR_*` do cofre do CI, ou data source de um segredo existente.

---

## Variáveis, outputs e tfvars

```hcl
variable "env" {
  type        = string
  description = "Environment name"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.env)
    error_message = "env must be dev, staging or prod."
  }
}

variable "db_instance_class" {
  type    = string
  default = "db.t4g.medium"
}

output "queue_url" {
  value = aws_sqs_queue.main.url
}
```
- **Tipos e `validation`** nas variáveis; `description` sempre. Valores por ambiente em `dev.tfvars`/`prod.tfvars` (**sem segredos**).
- **Outputs** expõem o que outros stacks/pipelines precisam (URL da fila, ARN da role) — **marque `sensitive = true`** se for sensível. Para entregar ao app, use IaC → Parameter Store/Secrets Manager/ConfigMap (`aws-parameter-store`), em vez de copiar à mão.
- **`count`/`for_each`** para repetição (prefira `for_each` com chave estável a `count` — remover um item do meio de `count` recria os seguintes).

## Proteção de recursos com estado

```hcl
resource "aws_dynamodb_table" "books" {
  # ...
  deletion_protection_enabled = true

  lifecycle {
    prevent_destroy = true
  }
}
```
`prevent_destroy` e `deletion_protection` em tudo que guarda **dados** (RDS, DynamoDB, buckets S3 com dados, KMS keys) — um `terraform destroy` ou uma renomeação acidental **não** apagam produção. **Renomear** um recurso no HCL = destruir e recriar: use `moved { from = ... to = ... }` para refatorar sem recriar. **Imports** (`import {}`) trazem recursos existentes para o código. **`terraform plan` é lido com atenção** antes de cada `apply`: `-/+` (replace) e `-` (destroy) em recurso com estado são alarme vermelho.

---

## Workflow: tudo pelo pipeline (OIDC, sem chaves)

```bash
terraform fmt -check -recursive
terraform init
terraform validate
tflint
trivy config .
terraform plan -var-file=prod.tfvars -out=tfplan
terraform apply tfplan
```
1. **Pull request** → o CI roda `fmt`, `validate`, `tflint`, scanner de segurança e **`terraform plan`**, e **posta o plan** como comentário. A revisão (`code-reviewer`) lê o **plan**, não só o diff do HCL.
2. **Merge na `main`** → `apply` em **dev/staging** automático; **produção com aprovação manual** (`environment` do GitHub — `github-actions-aws`) aplicando **o mesmo `tfplan`** revisado (`-out`).
3. **Autenticação por OIDC** (role assumida pelo workflow, **sem access keys** — `github-actions-aws`). A role do Terraform tem as permissões dos recursos que gerencia — separada por ambiente e **mais restrita em prod**; a trust policy limita repositório **e** environment.
4. **Scanners de segurança** no PR: **tflint** (erros de provider), **Trivy/Checkov** (`trivy config`/`checkov`: bucket público, SG `0.0.0.0/0`, sem criptografia, IAM `*`) — falha o pipeline em achado alto.
5. **Drift:** rode `terraform plan` agendado (EventBridge Scheduler/GitHub cron — `aws-eventbridge`) e alarme se houver diferença: alguém mexeu à mão no console.

Pipeline mínimo (trecho):
```yaml
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check -recursive
      - run: terraform init -input=false
      - run: terraform validate
      - run: terraform plan -input=false -var-file=dev.tfvars -out=tfplan
```
(Confirme as versões atuais das actions e fixe por SHA.)

## CDK (Java) — quando preferir

Com o **AWS CDK em Java** a infraestrutura é código Java comum: o `ECS` + ALB + Fargate do `aws-ecs-fargate` vira poucas linhas com *constructs* de alto nível (`ApplicationLoadBalancedFargateService`), com **testes unitários da infra** (assertions) e a mesma linguagem/IDE do time. `cdk synth` gera CloudFormation; `cdk diff` mostra o impacto; `cdk deploy` aplica. Mesmas regras: **IaC no Git, deploy por pipeline com OIDC, menor privilégio, prevent-destroy (`RemovalPolicy.RETAIN`) em dados**.

---

## Regras principais

- **Nada à mão no console**: toda infra (e IAM/SG/criptografia) como código no Git, revisada por PR, aplicada por pipeline.
- Terraform por padrão (SAM p/ Lambda local; CDK se a equipe é Java e só AWS); **uma ferramenta por stack**.
- **Um diretório e um state por ambiente** (idealmente contas separadas); módulos só para padrões repetidos e **versionados**.
- State no **S3 versionado, criptografado, com lock**, acesso mínimo; **nunca** commitar state; fixar `required_version`, provider (`~>`) e **commitar `.terraform.lock.hcl`**.
- `default_tags` em tudo (custo/auditoria); região/ambiente por variável.
- **Segredos nunca em `.tfvars`/código/state**: `manage_master_user_password`, Secrets Manager/Parameter Store, `TF_VAR_*` do cofre do CI.
- IAM de **menor privilégio** (ações e ARNs exatos); trust policies como código; nunca `*`.
- Recursos com dados: `prevent_destroy` + `deletion_protection`; renomear com `moved {}`; ler o **plan** (replace/destroy = alarme).
- CI: `fmt` → `validate` → `tflint` → Trivy/Checkov → `plan` (comentado no PR) → `apply` do **mesmo plan**, prod com aprovação; OIDC, sem access keys; detecção de **drift**.
- Retenção em log groups, SSE/KMS, `publicly_accessible = false`, Multi-AZ e backups em prod — por código.
- **Sem Lombok** — deliberado.
