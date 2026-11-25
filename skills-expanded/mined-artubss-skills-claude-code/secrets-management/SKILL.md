---
name: secrets-management
description: "Práticas seguras de gestão de secrets para pipelines de CI/CD usando Vault, AWS Secrets Manager e outras ferramentas."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Gestão de Secrets

Práticas seguras de gestão de secrets para pipelines de CI/CD usando Vault, AWS Secrets Manager e outras ferramentas.

## Propósito

Implementar gestão segura de secrets em pipelines de CI/CD sem hardcodear informações sensíveis.

## Use essa skill quando

- Armazenar API keys e credenciais
- Gerenciar senhas de banco de dados
- Lidar com certificados TLS
- Rotacionar secrets automaticamente
- Implementar acesso com menor privilégio

## Não use essa skill quando

- Você planeja hardcodear secrets no controle de fonte
- Você não consegue proteger o acesso ao backend de secrets
- Você só precisa de valores locais de desenvolvimento sem compartilhamento

## Instruções

1. Identifique tipos de secrets, proprietários e requisitos de rotação.
2. Escolha um backend de secrets e modelo de acesso.
3. Integre retrieval de CI/CD ou runtime com menor privilégio.
4. Valide rotação e logging de auditoria.

## Segurança

- Nunca faça commit de secrets no controle de fonte.
- Limite o acesso e registre o uso de secrets para auditoria.

## Ferramentas de Gestão de Secrets

### HashiCorp Vault
- Gestão centralizada de secrets
- Geração dinâmica de secrets
- Rotação de secrets
- Logging de auditoria
- Controle de acesso granular

### AWS Secrets Manager
- Solução nativa da AWS
- Rotação automática
- Integração com RDS
- Suporte a CloudFormation

### Azure Key Vault
- Solução nativa do Azure
- Chaves com suporte a HSM
- Gestão de certificados
- Integração com RBAC

### Google Secret Manager
- Solução nativa do GCP
- Versionamento
- Integração com IAM

## Integração com HashiCorp Vault

### Configurar Vault

```bash
# Start Vault dev server
vault server -dev

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Store secret
vault kv put secret/database/config username=admin password=secret
```

### GitHub Actions com Vault

```yaml
name: Deploy with Vault Secrets

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Import Secrets from Vault
      uses: hashicorp/vault-action@v2
      with:
        url: https://vault.example.com:8200
        token: ${{ secrets.VAULT_TOKEN }}
        secrets: |
          secret/data/database username | DB_USERNAME ;
          secret/data/database password | DB_PASSWORD ;
          secret/data/api key | API_KEY

    - name: Use secrets
      run: |
        echo "Connecting to database as $DB_USERNAME"
        # Use $DB_PASSWORD, $API_KEY
```

### GitLab CI com Vault

```yaml
deploy:
  image: vault:latest
  before_script:
    - export VAULT_ADDR=https://vault.example.com:8200
    - export VAULT_TOKEN=$VAULT_TOKEN
    - apk add curl jq
  script:
    - |
      DB_PASSWORD=$(vault kv get -field=password secret/database/config)
      API_KEY=$(vault kv get -field=key secret/api/credentials)
      echo "Deploying with secrets..."
      # Use $DB_PASSWORD, $API_KEY
```

**Referência:** Veja `references/vault-setup.md`

## AWS Secrets Manager

### Armazenar Secret

```bash
aws secretsmanager create-secret \
  --name production/database/password \
  --secret-string "super-secret-password"
```

### Recuperar no GitHub Actions

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-west-2

- name: Get secret from AWS
  run: |
    SECRET=$(aws secretsmanager get-secret-value \
      --secret-id production/database/password \
      --query SecretString \
      --output text)
    echo "::add-mask::$SECRET"
    echo "DB_PASSWORD=$SECRET" >> $GITHUB_ENV

- name: Use secret
  run: |
    # Use $DB_PASSWORD
    ./deploy.sh
```

### Terraform com AWS Secrets Manager

```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "production/database/password"
}

resource "aws_db_instance" "main" {
  allocated_storage    = 100
  engine              = "postgres"
  instance_class      = "db.t3.large"
  username            = "admin"
  password            = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
}
```

## GitHub Secrets

### Secrets de Organização/Repositório

```yaml
- name: Use GitHub secret
  run: |
    echo "API Key: ${{ secrets.API_KEY }}"
    echo "Database URL: ${{ secrets.DATABASE_URL }}"
```

### Secrets de Environment

```yaml
deploy:
  runs-on: ubuntu-latest
  environment: production
  steps:
  - name: Deploy
    run: |
      echo "Deploying with ${{ secrets.PROD_API_KEY }}"
```

**Referência:** Veja `references/github-secrets.md`

## Variáveis de GitLab CI/CD

### Variáveis de Projeto

```yaml
deploy:
  script:
    - echo "Deploying with $API_KEY"
    - echo "Database: $DATABASE_URL"
```

### Variáveis Protegidas e Mascaradas
- Protegidas: Disponíveis apenas em branches protegidas
- Mascaradas: Ocultas nos logs de job
- Tipo arquivo: Armazenadas como arquivo

## Melhores Práticas

1. **Nunca faça commit de secrets** no Git
2. **Use secrets diferentes** por environment
3. **Rotacione secrets regularmente**
4. **Implemente acesso com menor privilégio**
5. **Ative logging de auditoria**
6. **Use secret scanning** (GitGuardian, TruffleHog)
7. **Mascare secrets nos logs**
8. **Criptografe secrets em repouso**
9. **Use tokens de curta duração** quando possível
10. **Documente os requisitos de secrets**

## Rotação de Secrets

### Rotação Automatizada com AWS

```python
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('secretsmanager')

    # Get current secret
    response = client.get_secret_value(SecretId='my-secret')
    current_secret = json.loads(response['SecretString'])

    # Generate new password
    new_password = generate_strong_password()

    # Update database password
    update_database_password(new_password)

    # Update secret
    client.put_secret_value(
        SecretId='my-secret',
        SecretString=json.dumps({
            'username': current_secret['username'],
            'password': new_password
        })
    )

    return {'statusCode': 200}
```

### Processo de Rotação Manual

1. Gere novo secret
2. Atualize secret no armazenamento de secrets
3. Atualize aplicações para usar novo secret
4. Verifique funcionalidade
5. Revogue secret antigo

## External Secrets Operator

### Integração com Kubernetes

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "production"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: database/config
      property: username
  - secretKey: password
    remoteRef:
      key: database/config
      property: password
```

## Secret Scanning

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for secrets with TruffleHog
docker run --rm -v "$(pwd):/repo" \
  trufflesecurity/trufflehog:latest \
  filesystem --directory=/repo

if [ $? -ne 0 ]; then
  echo "❌ Secret detected! Commit blocked."
  exit 1
fi
```

### Secret Scanning em CI/CD

```yaml
secret-scan:
  stage: security
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog filesystem .
  allow_failure: false
```

## Arquivos de Referência

- `references/vault-setup.md` - Configuração do HashiCorp Vault
- `references/github-secrets.md` - Melhores práticas de GitHub Secrets

## Skills Relacionadas

- `github-actions-templates` - Para integração com GitHub Actions
- `gitlab-ci-patterns` - Para integração com GitLab CI
- `deployment-pipeline-design` - Para arquitetura de pipeline